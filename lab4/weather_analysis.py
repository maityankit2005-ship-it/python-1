"""
weather_analysis.py
Mini project: Weather Data Visualizer
Usage:
    python weather_analysis.py --input weather.csv --outdir outputs --save-plots
"""

import os
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Helper functions
# -----------------------
def ensure_outdir(outdir):
    Path(outdir).mkdir(parents=True, exist_ok=True)

def load_data(path):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, columns: {list(df.columns)}")
    return df

def preprocess(df, date_col='date'):
    # Standard datetime conversion
    df = df.copy()
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)
    else:
        raise KeyError(f"Expected a date column named '{date_col}'")

    # Fill or drop missing numeric columns - strategy: forward fill then mean
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        if df[c].isna().any():
            df[c] = df[c].fillna(method='ffill').fillna(df[c].mean())

    return df

def compute_stats(df, date_col='date', freq='D'):
    df = df.set_index(date_col)
    daily = df.resample('D').agg(['mean','min','max','std'])
    # Also global statistics
    stats = df.describe()
    return daily, stats

# -----------------------
# Visualization helpers
# -----------------------
def plot_line_temperature(df, date_col='date', temp_col='temperature', outpath=None):
    plt.figure(figsize=(10,4))
    plt.plot(df[date_col], df[temp_col])
    plt.xlabel('Date')
    plt.ylabel(temp_col.capitalize())
    plt.title('Daily Temperature Trend')
    plt.tight_layout()
    if outpath: plt.savefig(outpath)
    plt.close()

def plot_bar_monthly_rainfall(df, date_col='date', rain_col='rainfall', outpath=None):
    df['month'] = pd.to_datetime(df[date_col]).dt.month
    monthly = df.groupby('month')[rain_col].sum()
    plt.figure(figsize=(8,4))
    plt.bar(monthly.index, monthly.values)
    plt.xlabel('Month')
    plt.ylabel('Total Rainfall')
    plt.title('Monthly Rainfall Totals')
    plt.xticks(range(1,13))
    plt.tight_layout()
    if outpath: plt.savefig(outpath)
    plt.close()

def plot_scatter_humidity_temp(df, temp_col='temperature', hum_col='humidity', outpath=None):
    plt.figure(figsize=(6,5))
    plt.scatter(df[temp_col], df[hum_col], alpha=0.6)
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.title('Humidity vs Temperature')
    plt.tight_layout()
    if outpath: plt.savefig(outpath)
    plt.close()

def combined_plots_example(df, date_col='date', temp_col='temperature', rain_col='rainfall', outpath=None):
    fig, axs = plt.subplots(2,1, figsize=(10,8))
    axs[0].plot(df[date_col], df[temp_col])
    axs[0].set_title('Daily Temperature')
    axs[0].set_ylabel(temp_col.capitalize())

    df['month'] = pd.to_datetime(df[date_col]).dt.month
    monthly = df.groupby('month')[rain_col].sum()
    axs[1].bar(monthly.index, monthly.values)
    axs[1].set_title('Monthly Rainfall')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Rainfall')

    plt.tight_layout()
    if outpath: plt.savefig(outpath)
    plt.close()

# -----------------------
# Grouping & Aggregation
# -----------------------
def grouping_aggregation(df, date_col='date', season_map=None):
    df = df.copy()
    df['month'] = pd.to_datetime(df[date_col]).dt.month
    # Seasons (Northern hemisphere example)
    if season_map is None:
        season_map = {12:'Winter',1:'Winter',2:'Winter',
                      3:'Spring',4:'Spring',5:'Spring',
                      6:'Summer',7:'Summer',8:'Summer',
                      9:'Autumn',10:'Autumn',11:'Autumn'}
    df['season'] = df['month'].map(season_map)
    agg = df.groupby('season').agg(['mean','median','std'])
    return agg

# -----------------------
# Export helpers
# -----------------------
def export_cleaned(df, outpath):
    df.to_csv(outpath, index=False)
    print(f"Saved cleaned CSV to {outpath}")

# -----------------------
# Main pipeline
# -----------------------
def main(args):
    ensure_outdir(args.outdir)
    df = load_data(args.input)

    # Assume CSV has at least: date, temperature, humidity, rainfall. If names differ, adjust args.
    df_clean = preprocess(df, date_col=args.date_col)

    # Compute stats
    daily_resampled, summary_stats = compute_stats(df_clean, date_col=args.date_col)
    summary_stats.to_csv(os.path.join(args.outdir, 'summary_stats.csv'))
    daily_resampled.to_csv(os.path.join(args.outdir, 'daily_resampled.csv'))

    # Visualizations
    if args.save_plots:
        plot_line_temperature(df_clean, date_col=args.date_col, temp_col=args.temp_col,
                              outpath=os.path.join(args.outdir,'daily_temperature.png'))
        plot_bar_monthly_rainfall(df_clean, date_col=args.date_col, rain_col=args.rain_col,
                                  outpath=os.path.join(args.outdir,'monthly_rainfall.png'))
        plot_scatter_humidity_temp(df_clean, temp_col=args.temp_col, hum_col=args.hum_col,
                                   outpath=os.path.join(args.outdir,'humidity_vs_temp.png'))
        combined_plots_example(df_clean, date_col=args.date_col, temp_col=args.temp_col, rain_col=args.rain_col,
                               outpath=os.path.join(args.outdir,'combined_plots.png'))

    # Grouping and aggregation
    agg = grouping_aggregation(df_clean, date_col=args.date_col)
    agg.to_csv(os.path.join(args.outdir,'seasonal_aggregation.csv'))

    # Export cleaned dataset
    export_cleaned(df_clean, os.path.join(args.outdir,'weather_cleaned.csv'))

    # Print small report summary
    print("Top-level insights (saved to outputs/summary_report.txt):")
    with open(os.path.join(args.outdir,'summary_report.txt'),'w') as f:
        f.write("Summary insights\n")
        f.write("================\n\n")
        f.write("Global statistics:\n")
        f.write(summary_stats.to_string())
        f.write("\n\nSeasonal aggregation:\n")
        f.write(agg.to_string())
    print("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to input CSV (e.g. weather.csv)')
    parser.add_argument('--outdir', default='outputs', help='Directory to save outputs')
    parser.add_argument('--save-plots', action='store_true', help='Save plots as PNGs')
    parser.add_argument('--date-col', default='date', help='Name of date column')
    parser.add_argument('--temp-col', default='temperature', help='Name of temperature column')
    parser.add_argument('--hum-col', default='humidity', help='Name of humidity column')
    parser.add_argument('--rain-col', default='rainfall', help='Name of rainfall/precipitation column')
    args = parser.parse_args()
    main(args)
