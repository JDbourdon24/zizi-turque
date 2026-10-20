# Your offshore wind turbine project — Step-by-step guide from zero

You don't need to know Python, oceanography or wave modelling yet. I'll guide your team through the project in the order you actually need to do things, including which websites to use, what data to download, what to calculate and what to submit.

First, an important clarification: the PDFs, Python notebooks and example data uploaded to this project are teaching materials. They are not your team's results. You need to download data for your own selected location and use the examples to learn how to analyse it.

## 1. What is the project actually about?

Imagine you want to install an offshore wind turbine somewhere in the ocean. Before designing it, you need to understand the conditions it will experience.

Your course divides this into three main stages:

Part I — Understand the ocean conditions

Determine how large the waves normally are, their periods and directions, seasonal changes, and how extreme they can become during storms.

Part II — Model wave propagation

Simulate how waves change as they travel over different water depths toward the turbine site.

Part III — Analyse the turbine

Investigate forces, turbine motion and anchoring requirements under normal and extreme waves.

Right now, focus only on Part I. Your first individual report is due October 23, 2026, with a maximum length of 10 pages according to the P3 project slides.

Your wind speed of approximately 9 m/s and depth of 68 m make the new location a reasonable candidate, assuming the wind speed is representative of turbine hub height. You do not need to select a turbine model yet.

## 2. What data do you need?

You will work with four main types of data.

| Data             | What it tells you                                 | Website                                                                                                                          |
| ---------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Bathymetry       | Water depth and seabed shape                      | [EMODnet](https://emodnet.ec.europa.eu/en/bathymetry?utm_source=chatgpt.com)                                                     |
| Historical waves | Wave height, period and direction over many years | [Copernicus Marine](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/services?utm_source=chatgpt.com)      |
| Wind             | Wind speed and direction                          | [ERA5](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries?tab=download\&utm_source=chatgpt.com) |
| Ocean currents   | Water movement, speed and direction               | [Copernicus Physics](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/services?utm_source=chatgpt.com)     |

The first two are your immediate priority. The wind and current time series are needed later in Part I.A to produce the wind and current roses requested by your assignment.

The Global Wind Atlas value of 9 m/s is useful for site selection, but a single average wind speed is not enough to construct a wind rose.

## 3. Follow these steps in order

## Your project checklist

8 steps

1 of 8 completed

13%

1\.

Confirm and record your new site coordinates

2\.

Save site information from Global Wind Atlas and EMODnet

3\.

Create a free Copernicus Marine account

4\.

Download the historical wave NetCDF file

5\.

Set up Python and verify the downloaded file

6\.

Generate the mean wave analysis figures

7\.

Calculate extreme wave conditions and add wind/current analyses

8\.

Prepare and submit your individual reports

### Step 1 — Finalize your location

One of you needs to record the exact coordinates of the new location where you found the 9 m/s wind speed and 68 m water depth.

Keep a small record like this:

| Information             | Your value         |
| ----------------------- | ------------------ |
| Latitude                | New coordinate     |
| Longitude               | New coordinate     |
| Country / sea           | Your selected area |
| Mean wind speed         | ≈ 9 m/s            |
| Wind measurement height | To be checked      |
| Water depth             | ≈ 68 m             |
| Distance to shore       | To be calculated   |

Save a screenshot of the site on a map. Do not worry about calculating wave statistics yet.

### Step 2 — Verify your site's wind and depth

[Global Wind Atlas: Alles über den Wind! | #geoObserver](https://images.openai.com/static-rsc-4/IHE90ICPeVwuBSuV0bMi1l2NyXY9SFmCmzdRM6lyk3ilQ3AP1vO_e6qfWTFe2QXUPvMUGdEqPa1mdp7aV8UZ2BHURtlixLtdOB4eQR8a9saDjHKPuHxs2u_WGDwQMSB5u2pHK5j-qpvR9CNXZhu9eDIkIm2EfEUutbUDhkMPLP0?purpose=inline)

[Global Wind Atlas](https://globalwindatlas.info/?utm_source=chatgpt.com)

Open the map, find your coordinates, select Mean Wind Speed, and record the speed and measurement height. Save a screenshot.

[EMODnet’s Central Map Viewer Unveils new visualization and technical Upgrades | European Marine Observation and Data Network (EMODnet)](https://images.openai.com/static-rsc-4/sTQXx2LLLYjy-BJXArhXOmG467eb8HEWERBcrKzkP3TEkq6K2hHJiZEapjtxSvQWl7GgBwTL4vViyjvhteJMHvRaRZyOsWq6OJ1e6sbAoPjii2G12O9qMO51ixkgkaiyvZR3BNx6Qn0X4tpy_-2fTj3HDLoPwwqWyhhr33m7tXE?purpose=inline)

[EMODnet Bathymetry](https://emodnet.ec.europa.eu/en/bathymetry?utm_source=chatgpt.com)

Open the map viewer, locate your coordinates, select a depth layer and inspect the local seabed. Record the 68 m depth estimate and save a map image.

EMODnet provides seabed-depth maps, downloadable bathymetry and depth profiles. Later, you may need a small bathymetry grid for the wave propagation model.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://emodnet.ec.europa.eu\&sz=32)

emodnet.ec.europa.eu



### Step 3 — Create your Copernicus Marine account

[image](https://www.google.com/s2/favicons?domain=https://data.marine.copernicus.eu\&sz=32)

[Copernicus Marine Data Store](https://data.marine.copernicus.eu/?utm_source=chatgpt.com)

This is the main source for your ocean-wave data.

Go to the website, create a free account, and sign in. You only need one person to perform the initial wave-data download and share the resulting file with the team.

In your course materials, the relevant product is called Global Ocean Waves Reanalysis.

Use this exact product

Product: `GLOBAL_MULTIYEAR_WAV_001_032`

Dataset: `cmems_mod_glo_wav_my_0.2deg_PT3H-i`

Open the wave dataset&#x20;

### Step 4 — Download the historical wave data

This is the most important step.

When you open the product page:

1. Go to Data access.
2. Find the 3-hourly dataset and choose the Subset → Form option. Alternatively, use the map-based download in MyOcean Pro.
3. Enter a small area surrounding your new coordinates, not your previous location.
4. Set the time period to January 1, 1996 – December 31, 2025 (30 years), provided the selected dataset offers these dates.
5. Select the four variables shown below and download in NetCDF format.

These are the parameters to select:

| Variable | Meaning                           | Unit    |
| -------- | --------------------------------- | ------- |
| `VHM0`   | Significant wave height \\(H_s\\) | m       |
| `VTM02`  | Mean wave period \\(T\_{m02}\\)   | s       |
| `VMDR`   | Mean wave direction               | degrees |
| `VTPK`   | Peak wave period \\(T_p\\)        | s       |

The first three are explicitly required in your P2 assignment. The fourth is useful for your P3 extreme-wave analysis because your lecturer asks for peak periods associated with extreme conditions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://help.marine.copernicus.eu\&sz=32)

Copernicus Marine Help Center



Only download your small study region—not the entire ocean. Copernicus allows you to choose the coordinates, variables and dates directly.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://help.marine.copernicus.eu\&sz=32)

Copernicus Marine Help Center



What should you obtain?

A file ending in `.nc`, such as `waves_our_site.nc`.

Think of this file as a large table containing 30 years of wave measurements calculated by an ocean model, with a new record every three hours.

Important: Copernicus data are stored on a geographical grid. Your exact coordinates might fall between grid points. We will check which nearby ocean grid point is used before analysing the results.

### Step 5 — Install Python and open your data

Your teacher has already supplied Python_Environment_Setup_Guide.pdf, which recommends Miniconda and Jupyter.

[Example analysis - DataLabs Documentation](https://images.openai.com/static-rsc-4/Ab17qPFEYi3sTp0Vmpq5xu1Wk3GoqPn0vSbsJAtstuP6kIVm2KrbTz6md4IK8KsT7oMdg0UTkPgPBeyv20z1ftc48BDtsnsrmlB2H2Ex96rlfVb9A5Fo32av2SnF7FPWAhpSlozKI34Rn85_6zE9JdqcP4sZVur-sZq0L3fDO84?purpose=inline)

You can use JupyterLab or VS Code with its Jupyter extension.

The PDF recommends creating an environment like this:

```
conda create -n copernicus-notebook -c conda-forge python=3.11 numpy pandas scipy xarray netcdf4 matplotlib cartopy jupyterlab ipykernel -y
conda activate copernicus-notebook
pip install copernicusmarine pyextremes
jupyter lab
```

These commands install the tools you need to read the files and generate figures.

Once you have your NetCDF file, the first check in Python is very simple:

```
import xarray as xrds = xr.open_dataset("waves_our_site.nc")print(ds)
```

This prints information about the data, including variables, coordinates and dates. We will use it to verify that the download was successful.

Don't try to understand every command now. The aim is simply to get the correct file opened.

### Step 6 — Analyse normal wave conditions (Part I.A)

Once the file is working, Python can generate the graphs requested by your assignment.

Time series

Show how wave height, period and direction change over the years. Calculate their long-term means and discuss trends.

Wave-height versus period histogram

Identify which combinations of wave height and period occur most often. Assess deep-water and linear-wave conditions using your site depth.

Wave rose

A circular graph showing which directions the waves usually come from and how their heights vary.

Seasonal variations

Calculate the mean values for January, February, March, etc., combining all years. Explain whether winter and summer conditions differ.

We will use your lecturer's existing notebook, `read_Copernicus_waves_plot_timeseries_waverose.ipynb`, as a reference, but adapt it to your own data rather than run its example settings unchanged.

### Step 7 — Extreme waves, wind and currents

For extreme waves, your teacher provided `project_wave_EVA.py` and introduced the `pyextremes` package.

You will estimate the significant wave heights associated with 1-year and 50-year return periods. In simple terms, these describe wave heights with annual exceedance probabilities of approximately 100% and 2%, respectively, under the assumed statistical model; a 50-year event can happen more than once in 50 years.

Your third team member will adapt the EVA script to use your wave-height time series instead of the example water-level data in `battery_wl.csv`.

For wind and currents, download time-series velocity components later using:

- [ERA5 hourly time-series data](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries?tab=download\&utm_source=chatgpt.com) — select 100 m eastward and northward wind components.
- [Global Ocean Physics Reanalysis](https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/services?utm_source=chatgpt.com) — select eastward and northward surface-current components (`uo`, `vo`) from the daily product.

You can then calculate speeds and directions and produce the required wind and current roses.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://cds.climate.copernicus.eu\&sz=32)

cds.climate.copernicus.eu

+1



### Step 8 — Write Report I

Each team member writes their own report, based on your shared calculations. The suggested structure in your course is: introduction and site description, methods, results, discussion, conclusion and references.

The reports should explain what you did, why the results make physical sense and what uncertainties remain. Do not just paste graphs without interpretations.

## 4. How the three of you should work together

| Team member                     | Start now                                                | Once wave data are ready                                      |
| ------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Person 1 — Site and environment | Verify coordinates, wind speed and bathymetry; save maps | Download wind and current series, make roses                  |
| Person 2 — Wave climate         | Create Copernicus account and download the wave file     | Make time series, histogram, wave rose and seasonal graphs    |
| Person 3 — Extreme waves        | Set up Python and read the lecturer's EVA example        | Calculate 1-year/50-year return levels and associated periods |

Have one shared folder where everyone can access the downloaded data, scripts and figures.

## 5. What I want you to do today

For now, don't try to complete all eight steps.

Your immediate goal is just to confirm your new coordinates and obtain the correct wave file. Once you have that file, I can help you adapt the supplied Python notebooks and guide you through each figure and calculation.

Send me your new latitude and longitude (the location with 9 m/s wind and 68 m depth).

Then I'll help you with the exact Copernicus download form, including which coordinate values to enter, so you don't accidentally download data for the wrong location again.