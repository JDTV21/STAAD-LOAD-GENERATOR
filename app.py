import streamlit as st
import math

st.set_page_config(page_title="PH Structural Load Engine", layout="centered")

st.title("🏗️ PH Structural Load Engine")
st.subheader("STAAD Load Generator")
st.caption("Developed by ENGR. JONAH DAVE T. VEGA")

st.markdown("---")

# ==========================
# MATERIAL PROPERTIES
# ==========================

st.header("Material Properties")

concrete = st.number_input("Concrete Unit Weight (kN/m³)", value=24.0)
masonry = st.number_input("Masonry / CHB Unit Weight (kN/m³)", value=20.0)

# ==========================
# FLOOR LOAD
# ==========================

st.header("Floor Loads (NSCP 2015)")

slab_thickness = st.number_input("Slab Thickness (m)", value=0.15)

finish = st.selectbox(
"Floor Finish",
[
"Ceramic Tile (1.0)",
"Granite (1.2)",
"Wood (0.8)"
]
)

ceiling = st.selectbox(
"Ceiling Load",
[
"Gypsum (0.25)",
"Plaster (0.5)",
"None (0)"
]
)

partition = st.selectbox(
"Partition Load",
[
"Light (1.0)",
"Heavy (2.0)",
"None (0)"
]
)

LL = st.number_input("Live Load (kN/m²)", value=2.0)

finish_dict = {
"Ceramic Tile (1.0)":1.0,
"Granite (1.2)":1.2,
"Wood (0.8)":0.8
}

ceiling_dict = {
"Gypsum (0.25)":0.25,
"Plaster (0.5)":0.5,
"None (0)":0
}

partition_dict = {
"Light (1.0)":1.0,
"Heavy (2.0)":2.0,
"None (0)":0
}

slab_sw = concrete * slab_thickness

floor_dead = slab_sw + finish_dict[finish] + ceiling_dict[ceiling] + partition_dict[partition]

# ==========================
# ROOF LOAD
# ==========================

st.header("Roof Loads")

roof_finish = st.selectbox(
"Roof Type",
[
"Metal Roof (0.75)",
"RC Roof w/ Tiles (1.0)",
"RC Roof w/ Waterproofing (1.25)"
]
)

roof_live = st.number_input("Roof Live Load (kN/m²)", value=0.75)

roof_dict = {
"Metal Roof (0.75)":0.75,
"RC Roof w/ Tiles (1.0)":1.0,
"RC Roof w/ Waterproofing (1.25)":1.25
}

roof_dead = roof_dict[roof_finish]

# ==========================
# WALL LOAD
# ==========================

st.header("Wall Load to Beam")

wall_height = st.number_input("Wall Height (m)", value=3.0)
wall_thickness = st.number_input("Wall Thickness (m)", value=0.15)

wall_load = masonry * wall_height * wall_thickness

# ==========================
# WIND LOAD
# ==========================

st.header("Wind Load")

wind_speed = st.number_input("Basic Wind Speed (kph)", value=250.0)

V = wind_speed / 3.6

wind_pressure = 0.613 * V**2 / 1000

# ==========================
# SEISMIC LOAD (UBC 1997)
# ==========================

st.header("Seismic Load (UBC 1997)")

zone = st.selectbox(
"Seismic Zone",
[
"Zone 4 (0.40)",
"Zone 3 (0.30)",
"Zone 2B (0.20)"
]
)

zone_dict = {
"Zone 4 (0.40)":0.40,
"Zone 3 (0.30)":0.30,
"Zone 2B (0.20)":0.20
}

Z = zone_dict[zone]

importance = st.number_input("Importance Factor I", value=1.0)

R = st.number_input("Response Modification Factor R", value=8.5)

# ==========================
# SOIL PROFILE TYPE
# ==========================

soil = st.selectbox(
"Soil Profile Type",
["SA","SB","SC","SD","SE"]
)

Ca_dict = {
"SA":0.32,
"SB":0.40,
"SC":0.44,
"SD":0.50,
"SE":0.60
}

Cv_dict = {
"SA":0.32,
"SB":0.50,
"SC":0.64,
"SD":0.84,
"SE":0.96
}

Ca = Ca_dict[soil]
Cv = Cv_dict[soil]

# ==========================
# NEAR SOURCE FACTORS
# ==========================

st.subheader("Near Source Factors")

distance = st.number_input("Distance to Active Fault (km)", value=10.0)

def interpolate(x1,x2,y1,y2,x):
    return y1 + (y2-y1)*(x-x1)/(x2-x1)

if distance <= 2:
    Na = 1.3
    Nv = 1.6

elif distance <= 5:
    Na = interpolate(2,5,1.3,1.1,distance)
    Nv = interpolate(2,5,1.6,1.3,distance)

elif distance <= 10:
    Na = interpolate(5,10,1.1,1.0,distance)
    Nv = interpolate(5,10,1.3,1.0,distance)

else:
    Na = 1.0
    Nv = 1.0

st.write("Na =", round(Na,3))
st.write("Nv =", round(Nv,3))

# ==========================
# BUILDING PERIOD
# ==========================

st.subheader("Building Period")

height = st.number_input("Building Height (m)", value=12.0)

Ct = 0.0731
x = 0.75

T = Ct * height**x

st.write("Approximate Period T =", round(T,3), "sec")

# ==========================
# SEISMIC WEIGHT
# ==========================

W = st.number_input("Total Seismic Weight W (kN)", value=10000.0)

# ==========================
# BASE SHEAR
# ==========================

Cs = Z * I * Ca * Na / R

V = Cs * W

# ==========================
# SUMMARY
# ==========================

st.markdown("---")
st.header("STAAD Load Summary")

st.write("Floor Dead Load:", round(floor_dead,2),"kN/m²")
st.write("Floor Live Load:", round(LL,2),"kN/m²")

st.write("Roof Dead Load:", round(roof_dead,2),"kN/m²")
st.write("Roof Live Load:", round(roof_live,2),"kN/m²")

st.write("Wall Load:", round(wall_load,2),"kN/m")

st.write("Wind Pressure:", round(wind_pressure,3),"kN/m²")

st.write("Na:", round(Na,3))
st.write("Nv:", round(Nv,3))

st.write("Base Shear V:", round(V,2),"kN")
