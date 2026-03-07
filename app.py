import streamlit as st

st.set_page_config(page_title="STAAD Load Generator", layout="wide")

st.title("STAAD Load Input Generator")
st.write("NSCP 2015 + UBC 1997")
st.write("Created by **ENGR. JONAH DAVE T. VEGA**")

st.divider()

# --------------------------------------------------
# PROJECT DATA
# --------------------------------------------------

st.header("Project Data")

col1,col2,col3 = st.columns(3)

with col1:
    floors = st.number_input("Number of Floors",value=3)

with col2:
    floor_height = st.number_input("Floor Height (m)",value=3.0)

with col3:
    building_height = floors * floor_height
    st.metric("Building Height",f"{building_height} m")

# --------------------------------------------------
# DEAD LOADS
# --------------------------------------------------

st.divider()
st.header("Dead Loads (NSCP)")

floor_finish = {
"Ceramic Tile":0.60,
"Granite":0.90,
"Marble":0.80,
"Wood":0.50
}

ceiling = {
"Gypsum Board":0.25,
"Acoustic":0.30,
"No Ceiling":0
}

roof_finish = {
"Metal Roof":0.20,
"Waterproofing":0.25,
"Green Roof":2.50
}

col1,col2,col3 = st.columns(3)

with col1:
    floor_type = st.selectbox("Floor Finish",floor_finish.keys())

with col2:
    ceiling_type = st.selectbox("Ceiling Type",ceiling.keys())

with col3:
    partition = st.number_input("Partition Load (kPa)",value=1.0)

DL = floor_finish[floor_type] + ceiling[ceiling_type] + partition

# --------------------------------------------------
# WALL LOAD
# --------------------------------------------------

st.header("Wall Load on Beam")

col1,col2,col3 = st.columns(3)

with col1:
    wall_height = st.number_input("Wall Height",value=3.0)

with col2:
    wall_thickness = st.number_input("Wall Thickness",value=0.15)

with col3:
    unit_weight = st.number_input("Wall Unit Weight",value=18.0)

wall_load = wall_height * wall_thickness * unit_weight

# --------------------------------------------------
# LIVE LOAD
# --------------------------------------------------

st.divider()
st.header("Live Loads")

live_load_table = {
"Residential":2.0,
"Office":2.4,
"Corridor":4.8,
"Stairs":4.8,
"Roof Live":0.75
}

occupancy = st.selectbox("Occupancy Type",live_load_table.keys())

LL = live_load_table[occupancy]

# --------------------------------------------------
# STAAD LOAD SUMMARY
# --------------------------------------------------

st.divider()
st.header("STAAD Loads Summary")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Dead Load (Floor)",f"{DL} kPa")

with col2:
    st.metric("Wall Load",f"{wall_load} kN/m")

with col3:
    st.metric("Live Load",f"{LL} kPa")

# --------------------------------------------------
# STAAD COMMAND GENERATOR
# --------------------------------------------------

st.divider()
st.header("STAAD Command Output")

staad_text = f"""
LOAD 1 DEAD LOAD
FLOOR LOAD
YRANGE 0 {floor_height} FLOAD -{DL}

MEMBER LOAD
UNI GY -{wall_load}

LOAD 2 LIVE LOAD
FLOOR LOAD
YRANGE 0 {floor_height} FLOAD -{LL}
"""

st.code(staad_text)
