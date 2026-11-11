# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:31:31 2026

@author: Admin
"""



##### Survey Scatter & Horizontal Bar chart Combined (Temperature Only)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 1. Load Excel File
# -----------------------------
file_path = r"D:/MY RE/Project_3/JU_shp/Climate data/JU_Survey/Microclimate_Study_SurveyData.xlsx"
sheet_name = "Sheet5"

df = pd.read_excel(file_path, sheet_name=sheet_name)


# -----------------------------
# 2. Font Size Settings
# -----------------------------
TITLE_SIZE = 28
LABEL_SIZE = 24
TICK_SIZE = 24
LEGEND_SIZE = 24


# =========================================================
# DATA FOR SCATTER PLOT
# =========================================================

df_selected = df[[
    "Temperature_On_Spot",
    "Temperature_On_Web"
]].dropna()


# -----------------------------
# Calculate R²
# -----------------------------
def calc_r2(x, y):
    correlation_matrix = np.corrcoef(x, y)
    r = correlation_matrix[0, 1]
    return r**2


r2_temp = calc_r2(
    df_selected["Temperature_On_Web"],
    df_selected["Temperature_On_Spot"]
)


# =========================================================
# DATA FOR BAR CHART
# =========================================================

df_bar = df.dropna(
    subset=[
        "Land_Cover_Categories",
        "Temperature_On_Spot",
        "Temperature_On_Web"
    ]
).copy()


# -----------------------------
# Standardize Land Cover Names
# -----------------------------
df_bar["Land_Cover_Categories"] = (
    df_bar["Land_Cover_Categories"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# -----------------------------
# Rename Land Cover Categories
# -----------------------------
category_mapping = {
    "shaded_area_with_significant_vegetation": "Shaded Vegetation",
    "surrounded_by_buildings": "Dense Built-up",
    "inside_building_but_in_open_space": "Semi-Open Indoor",
    "direct_sunlight": "Open Sunlight",
    "on_road": "Road Surface",
    "adjacent_to_a_lake__river__or_pond": "Near Wetlands",
    "inside_vehicle": "Inside Vehicle",
    "inside_a_forest_with_dense_vegetation": "Dense Forest",
    "other": "Other"
}


df_bar["Land Cover Category"] = (
    df_bar["Land_Cover_Categories"]
    .map(category_mapping)
)


# -----------------------------
# Desired Category Order
# -----------------------------
category_order = [
    "Dense Built-up",
    "Dense Forest",
    "Inside Vehicle",
    "Near Wetlands",
    "Open Sunlight",
    "Road Surface",
    "Semi-Open Indoor",
    "Shaded Vegetation",    
    "Other"
]


# Keep only categories included in the mapping
df_bar = df_bar[
    df_bar["Land Cover Category"].isin(category_order)
]


# -----------------------------
# Group by Land Cover Category
# -----------------------------
grouped = (
    df_bar
    .groupby("Land Cover Category")[
        ["Temperature_On_Spot", "Temperature_On_Web"]
    ]
    .mean()
    .reindex(category_order)
)


# =========================================================
# CREATE MAIN FIGURE
# =========================================================

fig = plt.figure(figsize=(25, 10))


# -----------------------------
# Create Grid
# -----------------------------
gs = fig.add_gridspec(
    1,
    2,
    width_ratios=[1.2, 1.2],
    wspace=0.45
)


# =========================================================
# LEFT: SCATTER PLOT
# =========================================================

ax1 = fig.add_subplot(gs[0])


# -----------------------------
# Temperature Scatter
# -----------------------------
ax1.scatter(
    df_selected["Temperature_On_Web"],
    df_selected["Temperature_On_Spot"],
    s=90,
    label=f"Temperature (°C) (R²={r2_temp:.2f})"
)


# -----------------------------
# Add 1:1 Reference Line
# -----------------------------
min_val = min(
    df_selected["Temperature_On_Web"].min(),
    df_selected["Temperature_On_Spot"].min()
)

max_val = max(
    df_selected["Temperature_On_Web"].max(),
    df_selected["Temperature_On_Spot"].max()
)


ax1.plot(
    [min_val, max_val],
    [min_val, max_val],
    linestyle="--",
    linewidth=2.5,
    color="black",
    label="1:1 Reference Line"
)


# -----------------------------
# Labels and Formatting
# -----------------------------
ax1.set_xlabel(
    "Web Data Values",
    fontsize=LABEL_SIZE
)

ax1.set_ylabel(
    "On Spot Data Values",
    fontsize=LABEL_SIZE
)


ax1.set_title(
    "(a)",
    fontsize=TITLE_SIZE,
    fontweight="bold"
)


ax1.tick_params(
    axis="both",
    labelsize=TICK_SIZE
)


ax1.legend(
    fontsize=LEGEND_SIZE
)


ax1.grid()


# =========================================================
# RIGHT: HORIZONTAL BAR CHART
# =========================================================

ax2 = fig.add_subplot(gs[1])


# -----------------------------
# Bar Colors
# -----------------------------
colors = [
    "#E64B35",
    "#4DBBD5"
]


spot = "Temperature_On_Spot"
web = "Temperature_On_Web"

title = "Temperature (°C)"


# -----------------------------
# Y Positions
# -----------------------------
y = np.arange(len(category_order))

bar_height = 0.35


spot_vals = grouped[spot]

web_vals = grouped[web]


# -----------------------------
# On-Spot Temperature
# -----------------------------
ax2.barh(
    y - bar_height / 2,
    spot_vals,
    height=bar_height,
    label="On Spot",
    color=colors[0]
)


# -----------------------------
# Web Temperature
# -----------------------------
ax2.barh(
    y + bar_height / 2,
    web_vals,
    height=bar_height,
    label="Web",
    color=colors[1]
)


# -----------------------------
# Y-axis: Land Cover Categories
# -----------------------------
ax2.set_yticks(y)

ax2.set_yticklabels(
    category_order,
    fontsize=20,
    rotation=0
)


# -----------------------------
# X-axis: Temperature
# -----------------------------
ax2.set_xlabel(
    title,
    fontsize=LABEL_SIZE
)


ax2.tick_params(
    axis="x",
    labelsize=TICK_SIZE
)


# -----------------------------
# Y-axis Label
# -----------------------------
ax2.set_ylabel(
    "Land Cover Types",
    fontsize=LABEL_SIZE,
    rotation=90,
    labelpad=15,
    va="center"
)


# -----------------------------
# Grid
# -----------------------------
ax2.grid(
    axis="x"
)


# -----------------------------
# Temperature Axis Range
# -----------------------------
ax2.set_xlim(
    18,
    28
)


ax2.set_xticks(
    np.arange(18, 28, 2)
)


# -----------------------------
# Keep First Category at Top
# -----------------------------
ax2.invert_yaxis()


# =========================================================
# SUBPLOT LABEL (b)
# =========================================================

fig.text(
    0.75,
    0.89,
    "(b)",
    ha="center",
    fontsize=TITLE_SIZE,
    fontweight="bold"
)


# =========================================================
# COMMON LEGEND
# =========================================================

handles, labels = ax2.get_legend_handles_labels()


fig.legend(
    handles,
    labels,
    loc="lower center",
    bbox_to_anchor=(0.73, -0.04),
    ncol=2,
    fontsize=LEGEND_SIZE,
    frameon=False
)


# =========================================================
# FINAL LAYOUT
# =========================================================

plt.tight_layout(
    rect=[0.2, 0.08, 0.5, 0.93]
)


# -----------------------------
# Show Plot
# -----------------------------
plt.show()






##### Survey Box Plot
##### Temperature Only


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


# =========================================================
# 1. LOAD DATA
# =========================================================

file_path = r"D:/MY RE/Project_3/JU_shp/Climate data/JU_Survey/Microclimate_Study_SurveyData.xlsx"
sheet_name = "Sheet5"

df = pd.read_excel(
    file_path,
    sheet_name=sheet_name
)


# =========================================================
# 2. FONT SETTINGS
# =========================================================

TITLE_SIZE = 28
LABEL_SIZE = 24
TICK_SIZE = 24
LEGEND_SIZE = 24


# =========================================================
# 3. LAND-COVER CATEGORY MAPPING
# =========================================================

category_map = {

    "shaded_area_with_significant_vegetation":
        "Shaded Vegetation",

    "surrounded_by_buildings":
        "Dense Built-up",

    "inside_building_but_in_open_space":
        "Semi-Open Indoor",

    "on_rooftop_of_a_building":
        "Rooftop",

    "direct_sunlight":
        "Open Sunlight",

    "on_road":
        "Road Surface",

    "adjacent_to_a_lake__river__or_pond":
        "Near Wetlands",

    "agricultural_land":
        "Agricultural Land",

    "inside_vehicle":
        "Inside Vehicle",

    "inside_a_forest_with_dense_vegetation":
        "Dense Forest",

    "other":
        "Other"
}


# =========================================================
# 4. DESIRED LAND-COVER CATEGORY ORDER
# =========================================================

category_order = [

    "Dense Built-up",
    "Dense Forest",
    "Inside Vehicle",
    "Near Wetlands",
    "Open Sunlight",
    "Road Surface",
    "Semi-Open Indoor",
    "Shaded Vegetation",
    "Other"
]


# =========================================================
# 5. CLEAN DATA FOR BOXPLOT
# =========================================================

df_box = df[
    [
        "Temperature_On_Spot",
        "Temperature_On_Web",
        "Land_Cover_Categories"
    ]
].dropna()


# =========================================================
# 6. STANDARDIZE LAND-COVER CATEGORY NAMES
# =========================================================

df_box["Land_Cover_Categories"] = (
    df_box["Land_Cover_Categories"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(category_map)
)


# Remove unmatched categories
df_box = df_box.dropna(
    subset=["Land_Cover_Categories"]
)


# =========================================================
# 7. KEEP ONLY AVAILABLE CATEGORIES
# =========================================================

available_categories = [
    cat
    for cat in category_order
    if cat in df_box["Land_Cover_Categories"].unique()
]


# =========================================================
# 8. PREPARE BOXPLOT DATA
# =========================================================

categories = available_categories


positions = np.arange(
    len(categories)
)


# -----------------------------
# On-Spot Temperature Data
# -----------------------------

temp_spot_data = [

    df_box[
        df_box["Land_Cover_Categories"] == cat
    ]["Temperature_On_Spot"]

    for cat in categories
]


# -----------------------------
# Web Temperature Data
# -----------------------------

temp_web_data = [

    df_box[
        df_box["Land_Cover_Categories"] == cat
    ]["Temperature_On_Web"]

    for cat in categories
]


# =========================================================
# 9. CREATE FIGURE
# =========================================================

fig, ax = plt.subplots(
    figsize=(20, 10)
)


# =========================================================
# 10. BOX PLOT COLORS
# =========================================================

temp_color1 = "#E64B35"
temp_color2 = "#4DBBD5"


# =========================================================
# 11. ON-SPOT TEMPERATURE BOXPLOT
# =========================================================

ax.boxplot(

    temp_spot_data,

    positions=positions - 0.20,

    widths=0.35,

    patch_artist=True,

    boxprops=dict(
        facecolor=temp_color1
    )
)


# =========================================================
# 12. WEB TEMPERATURE BOXPLOT
# =========================================================

ax.boxplot(

    temp_web_data,

    positions=positions + 0.20,

    widths=0.35,

    patch_artist=True,

    boxprops=dict(
        facecolor=temp_color2
    )
)


# =========================================================
# 13. X-AXIS
# =========================================================

ax.set_xticks(
    positions
)


ax.set_xticklabels(

    categories,

    rotation=85,

    fontsize=TICK_SIZE
)


# =========================================================
# 14. X-AXIS LABEL
# =========================================================

ax.set_xlabel(
    "Land Cover Types",
    fontsize=LABEL_SIZE
)


# =========================================================
# 15. Y-AXIS LABEL
# =========================================================

ax.set_ylabel(
    "Temperature (°C)",
    fontsize=LABEL_SIZE
)


# =========================================================
# 16. Y-AXIS TICK SIZE
# =========================================================

ax.tick_params(
    axis="y",
    labelsize=TICK_SIZE
)


# =========================================================
# 17. GRID
# =========================================================

ax.grid(
    axis="y",
    alpha=0.5
)


# =========================================================
# 18. LEGEND
# =========================================================

legend_handles = [

    Patch(
        facecolor=temp_color1,
        label="On Spot"
    ),

    Patch(
        facecolor=temp_color2,
        label="Web"
    )
]


ax.legend(

    handles=legend_handles,

    loc="lower center",

    bbox_to_anchor=(0.5, -0.65),

    ncol=2,

    fontsize=LEGEND_SIZE,

    frameon=True
)


# =========================================================
# 19. FINAL LAYOUT
# =========================================================

plt.tight_layout()


plt.subplots_adjust(
    bottom=0.25
)


# =========================================================
# 20. SHOW FIGURE
# =========================================================

plt.show()
