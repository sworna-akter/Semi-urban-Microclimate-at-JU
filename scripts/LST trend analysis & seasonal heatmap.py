# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:30:20 2026

@author: Admin
"""


#### LST Trend analysis, Monthly, Seasonal Combined
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import theilslopes
import pymannkendall as mk

# =========================================================
# FONT SIZE SETTINGS
# =========================================================
TITLE_SIZE = 28
LABEL_SIZE = 22
TICK_SIZE = 22
LEGEND_SIZE = 22

# =========================================================
# LOAD DATASET 1: TREND ANALYSIS
# =========================================================
file_path = r"D:/Project_3/JU_shp/Climate data/LST/JU_LST_statistics_2011-2025_Final.xlsx"

df1 = pd.read_excel(file_path, sheet_name="Sheet2")

# Keep only required columns
df1 = df1.iloc[:, :2]

# Rename columns
df1.columns = ["Year", "Annual Max LST (°C)"]

# Convert datatype
df1["Year"] = pd.to_numeric(df1["Year"], errors='coerce')
df1["Annual Max LST (°C)"] = pd.to_numeric(
    df1["Annual Max LST (°C)"],
    errors='coerce'
)

# Remove missing values
df1 = df1.dropna()

# =========================================================
# LINEAR REGRESSION TREND
# =========================================================
slope, intercept, r_value, p_value, std_err = linregress(
    df1["Year"],
    df1["Annual Max LST (°C)"]
)

df1["Trend_Line"] = intercept + slope * df1["Year"]

# =========================================================
# MANN-KENDALL TEST
# =========================================================
mk_test = mk.original_test(df1["Annual Max LST (°C)"])

# =========================================================
# SEN'S SLOPE
# =========================================================
sen_slope, sen_intercept, lower_slope, upper_slope = theilslopes(
    df1["Annual Max LST (°C)"],
    df1["Year"],
    0.95
)

df1["Sen_Trend"] = sen_intercept + sen_slope * df1["Year"]

# =========================================================
# MOVING AVERAGE
# =========================================================
df1["Moving_Avg_3yr"] = df1["Annual Max LST (°C)"].rolling(window=3).mean()

# =========================================================
# LOAD DATASET 2: MONTHLY & SEASONAL CLIMATOLOGY
# =========================================================
df2 = pd.read_excel(file_path, sheet_name="Sheet3")

# Rename columns
df2 = df2.rename(columns={
    df2.columns[0]: "Month",
    df2.columns[1]: "Max LST (°C)"
})

# Convert datatype
df2["Max LST (°C)"] = pd.to_numeric(
    df2["Max LST (°C)"],
    errors='coerce'
)

df2 = df2.dropna(subset=["Max LST (°C)"])

# =========================================================
# ORDER MONTHS
# =========================================================
month_order = [
    "December","January","February","March","April","May",
    "June","July","August","September","October","November"
]

df2["Month"] = pd.Categorical(
    df2["Month"],
    categories=month_order,
    ordered=True
)

df2 = df2.sort_values("Month")

# =========================================================
# DEFINE SEASONS
# =========================================================
seasons = [
    "Winter","Winter","Pre-Monsoon","Pre-Monsoon",
    "Pre-Monsoon","Monsoon","Monsoon","Monsoon",
    "Post-Monsoon","Post-Monsoon","Post-Monsoon","Winter"
]

df2["Season"] = seasons

# =========================================================
# MONTHLY STATISTICS
# =========================================================
mean_lst = df2["Max LST (°C)"].mean()
std_lst = df2["Max LST (°C)"].std()

# =========================================================
# CREATE MAIN FIGURE (1 ROW × 2 COLUMNS)
# =========================================================
fig = plt.figure(figsize=(28, 10))

gs = fig.add_gridspec(
    1, 2,
    width_ratios=[1, 1.2],
    wspace=0.10
)

# =========================================================
# LEFT PLOT: TREND ANALYSIS
# =========================================================
ax1 = fig.add_subplot(gs[0])

# Original Data
ax1.plot(
    df1["Year"],
    df1["Annual Max LST (°C)"],
    marker='o',
    linewidth=3,
    markersize=8,
    label="Annual Mean Max LST"
)

# Linear Trend
ax1.plot(
    df1["Year"],
    df1["Trend_Line"],
    linestyle="--",
    linewidth=3,
    label="Linear Trend"
)

# Sen's Slope
ax1.plot(
    df1["Year"],
    df1["Sen_Trend"],
    linestyle=":",
    linewidth=3,
    label="Sen's Slope"
)

# Moving Average
ax1.plot(
    df1["Year"],
    df1["Moving_Avg_3yr"],
    linewidth=3,
    label="3-Year Moving Average"
)

# Labels
ax1.set_xlabel("Year", fontsize=LABEL_SIZE)
ax1.set_ylabel("Max LST (°C)", fontsize=LABEL_SIZE)

# Title
ax1.set_title(
    "(a)",
    fontsize=TITLE_SIZE,
    fontweight='bold'
)

# Tick size
ax1.tick_params(axis='both', labelsize=TICK_SIZE)

# Legend
ax1.legend(
    fontsize=LEGEND_SIZE,
    loc='lower left',
    bbox_to_anchor=(0.0, -0.03)
)

# Grid
ax1.grid(True)

# =========================================================
# RIGHT PLOT: MONTHLY & SEASONAL CLIMATOLOGY
# =========================================================
subgs = gs[1].subgridspec(
    2, 1,
    height_ratios=[2, 1],
    hspace=1.0
)

ax2 = fig.add_subplot(subgs[0])

# Monthly Line Plot
ax2.plot(
    df2["Month"],
    df2["Max LST (°C)"],
    marker='o',
    linewidth=3,
    markersize=8,
    label="Mean Max LST"
)

ax2.axhline(
    mean_lst,
    linestyle="--",
    linewidth=3,
    label="Annual Mean"
)

ax2.set_ylabel("Max LST (°C)", fontsize=LABEL_SIZE)

ax2.set_title(
    "(b)",
    fontsize=TITLE_SIZE,
    fontweight='bold'
)

ax2.grid(True)

ax2.legend(fontsize=LEGEND_SIZE)

ax2.set_xticks(range(len(month_order)))

ax2.set_xticklabels(
    month_order,
    rotation=85,
    fontsize=TICK_SIZE
)

ax2.tick_params(axis='y', labelsize=TICK_SIZE)

# =========================================================
# SEASONAL HEATMAP
# =========================================================
ax3 = fig.add_subplot(subgs[1])

heatmap_data = df2.set_index("Month")["Max LST (°C)"].values.reshape(1, -1)

im = ax3.imshow(
    heatmap_data,
    aspect='auto',
    cmap='YlOrRd'
)

# Month labels
ax3.set_xticks(range(len(month_order)))

ax3.set_xticklabels(
    month_order,
    rotation=85,
    fontsize=TICK_SIZE
)

ax3.set_yticks([])

# Colorbar
cbar = plt.colorbar(
    im,
    ax=ax3,
    orientation='vertical'
)

cbar.set_label(
    "Max LST (°C)",
    fontsize=LABEL_SIZE
)

cbar.ax.tick_params(labelsize=TICK_SIZE)

# Season labels
season_positions = {
    "Winter": np.mean([0, 1, 2]),
    "Pre-Monsoon": np.mean([3, 4, 5]),
    "Monsoon": np.mean([6, 7, 8]),
    "Post-Monsoon": np.mean([9, 10, 11])
}

for season, pos in season_positions.items():
    ax3.text(
        pos,
        1.75,
        season,
        ha='center',
        va='center',
        fontsize=24,
        fontweight='bold'
    )

ax3.set_title(
    "(c)",
    fontsize=TITLE_SIZE,
    fontweight='bold'
)

# =========================================================
# FINAL LAYOUT
# =========================================================
plt.tight_layout()

# =========================================================
# SHOW PLOT
# =========================================================
plt.show()

