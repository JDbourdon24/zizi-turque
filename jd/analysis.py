"""Wave climate analysis for Report I (Part I.A: mean conditions and seasonality).

Reads the Copernicus GLOBAL_MULTIYEAR_WAV_001_032 subset from the project repo,
selects the grid point nearest the site, and writes every figure and number
used in main.tex (figures/*.pdf, results.json).

Usage: python analysis.py <path/to/cmems_...nc>
"""
import json
import os
import sys
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

SITE_LON, SITE_LAT = -5.49359, 47.96920   # site (Global Wind Atlas / EMODnet)
DEPTH = 68.53                              # m, EMODnet mean depth at the site
G = 9.81
RES = {}


def circ_mean(deg):
    r = np.deg2rad(np.asarray(deg))
    return float(np.rad2deg(np.arctan2(np.sin(r).mean(), np.cos(r).mean())) % 360)


def circ_std(deg):
    r = np.deg2rad(np.asarray(deg))
    R = np.hypot(np.sin(r).mean(), np.cos(r).mean())
    return float(np.rad2deg(np.sqrt(-2 * np.log(R)))), float(R)


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), bbox_inches="tight")
    plt.close(fig)


def main():
    # ------------------------------------------------------------ data
    ds = xr.open_dataset(sys.argv[1])
    pt = ds.sel(longitude=SITE_LON, latitude=SITE_LAT, method="nearest")
    df = pt[["VHM0", "VTM02", "VMDR"]].to_dataframe()[["VHM0", "VTM02", "VMDR"]].dropna()
    RES["grid_lat"] = float(pt.latitude)
    RES["grid_lon"] = float(pt.longitude)
    RES["n"] = len(df)
    RES["start"], RES["end"] = str(df.index[0]), str(df.index[-1])

    # ---------------------------------------------------------------- A1 mean conditions + trends
    RES["mean_hs"] = float(df.VHM0.mean())
    RES["median_hs"] = float(df.VHM0.median())
    RES["std_hs"] = float(df.VHM0.std())
    RES["max_hs"] = float(df.VHM0.max())
    RES["max_hs_date"] = str(df.VHM0.idxmax())
    RES["mean_tm02"] = float(df.VTM02.mean())
    RES["std_tm02"] = float(df.VTM02.std())
    RES["mean_dir"] = circ_mean(df.VMDR)
    RES["dir_spread"], RES["dir_R"] = circ_std(df.VMDR)

    year = df.index.year
    annual = pd.DataFrame({
        "hs": df.VHM0.groupby(year).mean(),
        "hs99": df.VHM0.groupby(year).quantile(0.99),
        "tm02": df.VTM02.groupby(year).mean(),
        "dir": df.VMDR.groupby(year).apply(circ_mean),
    })

    trends = {}
    for col in ["hs", "hs99", "tm02", "dir"]:
        y = annual[col].values
        x = annual.index.values.astype(float)
        lr = stats.linregress(x, y)
        tau, p_mk = stats.kendalltau(x, y)
        sen = stats.theilslopes(y, x)[0]
        trends[col] = dict(slope_decade=lr.slope * 10, p_lr=lr.pvalue,
                           tau=tau, p_mk=p_mk, sen_decade=sen * 10,
                           mean=float(np.mean(y)), min=float(np.min(y)),
                           max=float(np.max(y)), ymin=int(x[np.argmin(y)]),
                           ymax=int(x[np.argmax(y)]))
    RES["trends"] = trends

    # winter (DJFM) means to see interannual (NAO-like) variability
    w = df[df.index.month.isin([12, 1, 2, 3])]
    wyear = np.where(w.index.month == 12, w.index.year + 1, w.index.year)
    winter = w.VHM0.groupby(wyear).mean()
    winter = winter[(winter.index > df.index.year.min()) & (winter.index <= df.index.year.max())]
    RES["winter_hs_min"] = (int(winter.idxmin()), float(winter.min()))
    RES["winter_hs_max"] = (int(winter.idxmax()), float(winter.max()))
    RES["winter_hs_cv"] = float(winter.std() / winter.mean())

    fig, axes = plt.subplots(3, 1, figsize=(10, 8.2), sharex=True)
    specs = [("VHM0", "hs", "$H_{m0}$ (m)", "tab:blue"),
             ("VTM02", "tm02", "$T_{m02}$ (s)", "tab:orange"),
             ("VMDR", "dir", r"$\theta_m$ (° from N)", "tab:green")]
    for ax, (var, col, lab, c) in zip(axes, specs):
        if var == "VMDR":
            ax.plot(df.index, df[var], ",", color=c, alpha=0.25)
            ax.set_ylim(0, 360)
            ax.set_yticks([0, 90, 180, 270, 360])
        else:
            ax.plot(df.index, df[var], color=c, lw=0.25, alpha=0.6)
        xs = pd.to_datetime([f"{y}-07-01" for y in annual.index])
        ax.plot(xs, annual[col], "k-o", ms=3, lw=1.2, label="annual mean")
        lr = stats.linregress(annual.index.values.astype(float), annual[col].values)
        ax.plot(xs, lr.intercept + lr.slope * annual.index.values, "r--", lw=1.2,
                label=f"linear trend ({lr.slope*10:+.3f}/decade, p={lr.pvalue:.2f})")
        ax.set_ylabel(lab)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
    axes[0].set_title(f"3-hourly CMEMS reanalysis at {RES['grid_lat']:.1f}°N, "
                      f"{abs(RES['grid_lon']):.1f}°W (1996–2025)")
    save(fig, "wave_timeseries.pdf")

    # ---------------------------------------------------------------- A2 histogram, regimes, rose
    t_deep = np.sqrt(4 * np.pi * DEPTH / G)          # h = L0/2
    t_shallow = np.sqrt(40 * np.pi * DEPTH / G)      # h = L0/20 (shallow limit)
    RES["t_deep"] = float(t_deep)
    RES["t_shallow"] = float(t_shallow)

    L0 = G * df.VTM02 ** 2 / (2 * np.pi)
    steep = df.VHM0 / L0
    RES["frac_deep"] = float((df.VTM02 < t_deep).mean())
    RES["frac_deep_tp"] = float((1.28 * df.VTM02 < t_deep).mean())
    RES["frac_lin"] = float((steep < 0.02).mean())
    RES["frac_weak"] = float(((steep >= 0.02) & (steep < 1 / 7)).mean())
    RES["frac_brk"] = float((steep >= 1 / 7).mean())
    RES["steep_median"] = float(steep.median())
    RES["hs_over_h_max"] = float(df.VHM0.max() / DEPTH)


    def wavelength(T, h):
        """Linear dispersion relation, Newton iterations."""
        k = (2 * np.pi / T) ** 2 / G
        for _ in range(50):
            f = G * k * np.tanh(k * h) - (2 * np.pi / T) ** 2
            df_ = G * np.tanh(k * h) + G * k * h / np.cosh(k * h) ** 2
            k -= f / df_
        return 2 * np.pi / k


    # Ursell number of the extreme sea state, to show it remains small
    RES["ursell_max"] = float(df.VHM0.max() * wavelength(df.VTM02[df.VHM0.idxmax()], DEPTH) ** 2 / DEPTH ** 3)

    h_edges = np.arange(0, 12.75, 0.25)
    t_edges = np.arange(2, 13.5, 0.5)
    counts, _, _ = np.histogram2d(df.VTM02, df.VHM0, bins=[t_edges, h_edges])
    it, ih = np.unravel_index(np.argmax(counts), counts.shape)
    RES["mode_hs"] = float((h_edges[ih] + h_edges[ih + 1]) / 2)
    RES["mode_tm02"] = float((t_edges[it] + t_edges[it + 1]) / 2)
    RES["mode_count"] = int(counts[it, ih])
    RES["mode_pct"] = float(counts[it, ih] / len(df) * 100)
    inbox = (df.VHM0.between(1, 3)) & (df.VTM02.between(5, 7))
    RES["pct_box"] = float(inbox.mean() * 100)

    fig, ax = plt.subplots(figsize=(9, 5.6))
    pct = counts.T / len(df) * 100
    pct[pct == 0] = np.nan
    m = ax.pcolormesh(t_edges, h_edges, pct, cmap="viridis", shading="auto")
    fig.colorbar(m, ax=ax, label="Occurrence (% of 3-h sea states)")
    tl = np.linspace(2, 13.5, 200)
    l0 = G * tl ** 2 / (2 * np.pi)
    ax.plot(tl, l0 / 7, "r-", lw=1.5, label=r"$H/L_0=1/7$ (steepness/breaking limit)")
    ax.plot(tl, l0 * 0.02, "w--", lw=1.5, label=r"$H/L_0=0.02$ (linear-wave limit)")
    ax.axvspan(2, t_deep, color="orange", alpha=0.10)
    ax.axvline(t_deep, color="orange", ls=":", lw=2,
               label=fr"deep-water limit $h=L_0/2$ ($T={t_deep:.1f}$ s, $h={DEPTH:.1f}$ m)")
    ax.plot(RES["mode_tm02"], RES["mode_hs"], "w*", ms=14, mec="k",
            label=fr"mode: $H_{{m0}}={RES['mode_hs']:.2f}$ m, $T_{{m02}}={RES['mode_tm02']:.2f}$ s")
    ax.text(3.0, 11.2, "deep water", color="darkorange", fontsize=10)
    ax.text(t_deep + 0.2, 11.2, "intermediate depth", color="darkorange", fontsize=10)
    ax.text(2.6, 0.5, "linear", color="w", fontsize=9, rotation=8)
    ax.text(5.0, 4.5, "weakly non-linear\n(Stokes 2nd order)", color="k", fontsize=9)
    ax.set(xlabel=r"$T_{m02}$ (s)", ylabel=r"$H_{m0}$ (m)", xlim=(2, 13.5), ylim=(0, 12.5),
           title="Joint occurrence of $H_{m0}$ and $T_{m02}$ (1996–2025)")
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.93), framealpha=0.9)
    save(fig, "wave_histogram.pdf")

    # wave rose
    nsec = 16
    edges = np.arange(-11.25, 360, 22.5)
    d = (df.VMDR + 11.25) % 360 - 11.25
    sector = pd.cut(d, edges, labels=np.arange(0, 360, 22.5), right=False)
    hb = [0, 1, 2, 3, 4, 6, np.inf]
    hl = ["0–1", "1–2", "2–3", "3–4", "4–6", "≥6"]
    hbin = pd.cut(df.VHM0, hb, labels=hl, right=False)
    tab = pd.crosstab(sector, hbin, normalize="all").reindex(
        index=np.arange(0, 360, 22.5), columns=hl, fill_value=0) * 100
    sec_tot = tab.sum(axis=1)
    names = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    order = sec_tot.sort_values(ascending=False)
    RES["rose_top"] = [(names[int(k / 22.5)], float(v)) for k, v in order.head(4).items()]
    RES["pct_W_sector"] = float(df.VMDR.between(225, 315).mean() * 100)
    RES["pct_east"] = float(df.VMDR.between(22.5, 157.5).mean() * 100)
    big = df[df.VHM0 >= 6]
    RES["dir_big"] = circ_mean(big.VMDR)
    RES["pct_big_W"] = float(big.VMDR.between(225, 315).mean() * 100)

    fig, ax = plt.subplots(figsize=(6.6, 6.6), subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    bottom = np.zeros(nsec)
    cols = plt.cm.viridis(np.linspace(0, 1, len(hl)))
    for lab, c in zip(hl, cols):
        v = tab[lab].values
        ax.bar(np.deg2rad(tab.index.values.astype(float)), v, width=np.deg2rad(22.5) * 0.95,
               bottom=bottom, color=c, edgecolor="k", lw=0.3, label=lab)
        bottom += v
    ax.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
    ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    ax.set_rlabel_position(135)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_title("Wave rose (direction waves come from)", pad=18)
    ax.legend(title="$H_{m0}$ (m)", loc="upper left", bbox_to_anchor=(1.05, 1.0), fontsize=8)
    save(fig, "wave_rose.pdf")

    # ---------------------------------------------------------------- A3 seasonal cycle
    mon = df.index.month
    monthly = pd.DataFrame({
        "hs": df.VHM0.groupby(mon).mean(),
        "hs10": df.VHM0.groupby(mon).quantile(0.1),
        "hs90": df.VHM0.groupby(mon).quantile(0.9),
        "tm": df.VTM02.groupby(mon).mean(),
        "tm10": df.VTM02.groupby(mon).quantile(0.1),
        "tm90": df.VTM02.groupby(mon).quantile(0.9),
        "dir": df.VMDR.groupby(mon).apply(circ_mean),
        "R": df.VMDR.groupby(mon).apply(lambda s: circ_std(s)[1]),
        "pW": df.VMDR.groupby(mon).apply(lambda s: s.between(225, 315).mean() * 100),
    })
    RES["monthly"] = monthly.round(3).to_dict(orient="index")
    win = df[df.index.month.isin([12, 1, 2])]
    sumr = df[df.index.month.isin([6, 7, 8])]
    RES["djf"] = dict(hs=float(win.VHM0.mean()), tm=float(win.VTM02.mean()),
                      dir=circ_mean(win.VMDR), p_hs4=float((win.VHM0 > 4).mean() * 100))
    RES["jja"] = dict(hs=float(sumr.VHM0.mean()), tm=float(sumr.VTM02.mean()),
                      dir=circ_mean(sumr.VMDR), p_hs4=float((sumr.VHM0 > 4).mean() * 100))

    fig, axes = plt.subplots(3, 1, figsize=(8, 7.6), sharex=True)
    x = monthly.index
    axes[0].fill_between(x, monthly.hs10, monthly.hs90, color="tab:blue", alpha=0.2, label="10–90 %")
    axes[0].plot(x, monthly.hs, "o-", color="tab:blue", label="mean")
    axes[0].set_ylabel("$H_{m0}$ (m)")
    axes[1].fill_between(x, monthly.tm10, monthly.tm90, color="tab:orange", alpha=0.2, label="10–90 %")
    axes[1].plot(x, monthly.tm, "o-", color="tab:orange", label="mean")
    axes[1].set_ylabel("$T_{m02}$ (s)")
    axes[2].plot(x, monthly.dir, "o-", color="tab:green", label="circular mean")
    axes[2].set_ylabel(r"$\bar\theta_m$ (°)")
    ax2 = axes[2].twinx()
    ax2.bar(x, monthly.pW, color="tab:green", alpha=0.15, label="% from W sector (225–315°)")
    ax2.set_ylabel("% W sector")
    ax2.set_ylim(0, 100)
    ax2.grid(False)
    axes[2].set_zorder(ax2.get_zorder() + 1)
    axes[2].patch.set_visible(False)
    for a in axes[:2]:
        a.legend(fontsize=8, loc="upper center")
    h1, l1 = axes[2].get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    axes[2].legend(h1 + h2, l1 + l2, fontsize=8, loc="lower left")
    axes[2].set_xticks(range(1, 13))
    axes[2].set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    axes[2].set_xlabel("Month")
    axes[0].set_title("Monthly wave climatology (1996–2025)")
    save(fig, "wave_monthly_climatology.pdf")

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in RES.items() if k != "monthly"}, indent=1, default=str))
    print(monthly.round(2))


if __name__ == "__main__":
    main()
