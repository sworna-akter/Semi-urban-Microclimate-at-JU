# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:27:29 2026

@author: Admin
"""



#### Spatial Map: Temperature Only (Zoom View + Reference Map)

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# -----------------------------
# 1. Load Excel data
# -----------------------------
file_path = r"D:/Project_3/JU_shp/Climate data/JU_Survey/Microclimate_Study_SurveyData.xlsx"
sheet_name = "Sheet5"

df = pd.read_excel(file_path, sheet_name=sheet_name)

# -----------------------------
# 2. Create GeoDataFrame for Temperature
# -----------------------------
df_temp = df.dropna(subset=["latitude", "longitude", "Temperature_On_Spot"])

gdf_temp = gpd.GeoDataFrame(
    df_temp,
    geometry=gpd.points_from_xy(df_temp["longitude"], df_temp["latitude"]),
    crs="EPSG:4326"
)

# -----------------------------
# 3. Load shapefiles
# -----------------------------
ju_boundary = gpd.read_file(
    r"D:/Project_3/JU_shp/JU Shape/JU_Boundary.shp"
)

roads = gpd.read_file(
    r"D:/Project_3/JU_shp/JU Shape/Roads.shp"
)

ju_boundary = ju_boundary.to_crs(gdf_temp.crs)
roads = roads.to_crs(gdf_temp.crs)

# -----------------------------
# 4. Create Subplots (1 Row × 2 Columns)
# -----------------------------
fig, axes = plt.subplots(
    1, 2,
    figsize=(18, 8),
    gridspec_kw={'wspace': 0.22}
)

ax1 = axes[0]   # Temperature
ax2 = axes[1]   # Reference Map


# =====================================================
# ZOOM EXTENT
# =====================================================
xmin = gdf_temp.total_bounds[0] - 0.0005
ymin = gdf_temp.total_bounds[1] - 0.0005
xmax = gdf_temp.total_bounds[2] + 0.0005
ymax = gdf_temp.total_bounds[3] + 0.0005


# =====================================================
# LEFT → TEMPERATURE MAP
# =====================================================
ju_boundary.plot(
    ax=ax1,
    color="none",
    edgecolor="black",
    linewidth=1.5
)

roads.plot(
    ax=ax1,
    color="black",
    linewidth=1,
    alpha=0.7
)

scatter1 = gdf_temp.plot(
    ax=ax1,
    column="Temperature_On_Spot",
    cmap="RdYlBu_r",
    markersize=90,
    legend=True,
    edgecolor="black",
    alpha=0.9,
    aspect=None
)

ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)

ax1.grid(False)

ax1.set_xlabel("Longitude", fontsize=18)
ax1.set_ylabel("Latitude", fontsize=18)

ax1.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y',
                labelrotation=90,
                labelsize=16)


# Temperature colorbar
cbar1 = scatter1.get_figure().get_axes()[-1]

cbar1.set_position([0.45, 0.2, 0.01, 0.5])

cbar1.set_ylabel("")
cbar1.tick_params(axis='y', labelsize=16)

cbar1.text(
    2.5, 0.5,
    "Temperature (°C)",
    rotation=90,
    va="center",
    ha="left",
    fontsize=18,
    transform=cbar1.transAxes
)


# =====================================================
# RIGHT → FULL JU REFERENCE MAP
# =====================================================
ju_boundary.plot(
    ax=ax2,
    color="none",
    edgecolor="black",
    linewidth=1.5
)

roads.plot(
    ax=ax2,
    color="black",
    linewidth=1,
    alpha=0.7
)


# Plot survey points
gdf_temp.plot(
    ax=ax2,
    color="black",
    markersize=35,
    edgecolor="black"
)


# Fix longitude display
ax2.set_aspect('equal')

ax2.grid(False)

ax2.set_xlabel("Longitude", fontsize=18)
ax2.set_ylabel("Latitude", fontsize=18)

ax2.tick_params(axis='x', labelsize=16)

ax2.ticklabel_format(style='plain', axis='x')
ax2.get_xaxis().get_major_formatter().set_useOffset(False)

ax2.tick_params(axis='y',
                labelrotation=90,
                labelsize=16)


# =====================================================
# NORTH ARROW
# =====================================================
ax1.annotate(
    'N',
    xy=(0.82, 0.92),
    xytext=(0.82, 0.82),
    xycoords=fig.transFigure,
    textcoords=fig.transFigure,
    arrowprops=dict(
        facecolor='black',
        width=10,
        headwidth=30
    ),
    ha='center',
    va='center',
    fontsize=30
)


# -----------------------------
# CUSTOM LEGEND
# -----------------------------
legend_elements = [
    Patch(
        facecolor='none',
        edgecolor='black',
        label='JU Boundary'
    ),

    Line2D(
        [0], [0],
        color='black',
        lw=2,
        label='Roads'
    ),

    Line2D(
        [0], [0],
        marker='o',
        color='w',
        markerfacecolor='black',
        markeredgecolor='black',
        markersize=10,
        label='Survey Locations'
    )
]

fig.legend(
    handles=legend_elements,
    loc='lower center',
    ncol=3,
    frameon=False,
    fontsize=18
)


# -----------------------------
# FINAL LAYOUT
# -----------------------------
plt.subplots_adjust(
    wspace=0.22,
    top=0.92,
    bottom=0.2
)

plt.show()