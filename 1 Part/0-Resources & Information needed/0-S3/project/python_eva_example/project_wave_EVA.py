# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 15:48:49 2022

@author: marissa.yates
"""

# extreme value analysis using pyextreme
import matplotlib
matplotlib.rc('text', usetex = True)
import numpy as np
from scipy import stats
import seaborn as sns
import scipy.ndimage
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from pyextremes import EVA


def main(): 
    # import data set with col0=time and col1=WL data
    series = pd.read_csv(
        "battery_wl.csv",
        index_col=0,
        parse_dates=True,
    ).squeeze()
    
    # clean up the data set (remove trend, data gaps, etc.)
    series = (
        series
        .sort_index(ascending=True)
        .astype(float)
        .dropna()
        .loc[pd.to_datetime("1925"):]
    )
    print(series.index.array)
    #series = series - (series.index.array - pd.to_datetime("1992")) / pd.to_timedelta("365.2425D") * 2.87e-3

    print(series.head)
    
    # load the interface to use to do the EVA
    model = EVA(series)
    
    # use block method (BM) to find one year extreme values
    model.get_extremes(method="BM", block_size="365.2425D")
    
    # print to screen to see values
    print(model.extremes.head())
    
    # graphically visualize the extremes
    model.plot_extremes()
    
    # find the optimal model parameters
    model.fit_model()
    
    # calculate the return values
    summary = model.get_summary(
        return_period=[1, 2, 5, 10, 25, 50, 100, 250, 500, 1000],
        alpha=0.95,
        n_samples=1000,
    )
    print(summary)
    
    # plot the diagnostics
    model.plot_diagnostic(alpha=0.95)
    
    
    
if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    main()  # execute this only when run directly, not when imported!