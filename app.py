import streamlit as st

st.set_page_config(page_title="STAAD Load Generator", layout="wide")

st.title("STAAD Load Generator for RC Design")
st.subheader("NSCP 2015 + 1997 UBC Seismic Parameters")
st.write("Developed by **ENGR. JONAH DAVE T. VEGA**")

st.divider()

# ------------------------------------------------
# UBC 1997 Near Source Tables
# ------------------------------------------------

Na_table = {
"A":[(2,1.5),(5,1.3),(10,1.2),(15,1.1)],
"B":[(2,1.3),(5,1.2),(10,1.1),(15,1.0)]
}

Nv_table = {
"A":[(2,2.0),(5,1.6),(10,1.3),(15,1.1)],
"B":[(2,1.6),(5,1.4),(10,1.2),(15,1.1)]
}

# ------------------------------------------------
# INTERPOLATION FUNCTION
# ------------------------------------------------

def interpolate(distance,data):

    x=[i[0] for i in data]
    y=[i[1] for i in data]

    if distance <= x[0]:
        return y[0]

    if distance >= x[-1]:
        return y[-1]

    for i in range(len(x)-1):

        if x[i] <= distance <= x[i+1]:

            x1=x[i]
            x2=x[i+1]

            y1=y[i]
            y2=y[i+1]

            return y1 + (distance-x1)*(y2-y1)/(x2-x1)

# ------------------------------------------------
# SEISMIC PARAMETERS
# ------------------------------------------------

st.header("Seismic Parameters (1997 UBC)")

col1,col2,col3 = st.columns(3)

with col1:

    zone = st.selectbox(
    "Seismic Zone Factor Z",
    [0.15,0.20,0.30,0.40]
    )

    importance = st.selectbox(
    "Importance Factor I",
    [1.0,1.25]
    )

with col2:

    soil_profile = st.selectbox(
    "Soil Profile Type",
    ["Sa","Sb","Sc","Sd","Se"]
    )

    source_type = st.selectbox(
    "Seismic Source Type",
    ["A","B"]
    )

with col3:

    distance = st.number_input(
    "Distance to Active Fault (km)",
    min_value=0.0,
    value=5.0
    )

    building_height = st.number_input(
    "Building Height (m)",
    value=15.0
    )

Ct = st.number_input(
"Ct Coefficient",
value=0.035
)

# ------------------------------------------------
# COMPUTE Na Nv
# ------------------------------------------------

Na = interpolate(distance,Na_table[source_type])
Nv = interpolate(distance,Nv_table[source_type])

# ------------------------------------------------
# PERIOD
# ------------------------------------------------

T = Ct*(building_height**0.75)

# ------------------------------------------------
# FLOOR DEAD LOADS
# ------------------------------------------------

st.divider()
st.header("Floor Dead Loads (NSCP 2015)")

floor_loads={
"Ceramic Tiles":0.60,
"Marble":0.80,
"Granite":0.90,
"Wood Flooring":0.50
}

ceiling_loads={
"Gypsum Ceiling":0.25,
"Acoustic Ceiling":0.30,
"No Ceiling":0
}

col1,col2,col3 = st.columns(3)

with col1:
    floor_type=st.selectbox("Floor Finish",list(floor_loads.keys()))

with col2:
    ceiling_type=st.selectbox("Ceiling Type",list(ceiling_loads.keys()))

with col3:
    partition=st.number_input("Partition Load (kPa)",value=1.0)

DL = floor_loads[floor_type] + ceiling_loads[ceiling_type] + partition

# ------------------------------------------------
# WALL LOAD TO BEAM
# ------------------------------------------------

st.divider()
st.header("Wall Load to Beam")

col1,col2,col3 = st.columns(3)

with col1:
    wall_height=st.number_input("Wall Height (m)",value=3.0)

with col2:
    wall_thickness=st.number_input("Wall Thickness (m)",value=0.15)

with col3:
    unit_weight=st.number_input("Wall Unit Weight (kN/m³)",value=18.0)

wall_load = wall_height*wall_thickness*unit_weight

# ------------------------------------------------
# ROOF LOAD
# ------------------------------------------------

st.divider()
st.header("Roof Dead Loads")

roof_loads={
"Metal Roof":0.20,
"Waterproofing":0.25,
"Green Roof":2.50
}

roof_type=st.selectbox("Roof Finish",list(roof_loads.keys()))

roof_load=roof_loads[roof_type]

# ------------------------------------------------
# STAAD LOAD SUMMARY
# ------------------------------------------------

st.divider()
st.header("STAAD LOAD SUMMARY")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("Floor Dead Load (kPa)",round(DL,3))

with c2:
    st.metric("Wall Load to Beam (kN/m)",round(wall_load,3))

with c3:
    st.metric("Roof Dead Load (kPa)",round(roof_load,3))

# ------------------------------------------------
# SEISMIC RESULTS
# ------------------------------------------------

st.divider()
st.header("Computed Seismic Factors")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("Na",round(Na,3))

with c2:
    st.metric("Nv",round(Nv,3))

with c3:
    st.metric("Period T (sec)",round(T,3))

st.success(f"""
Use these loads in **STAAD**:

FLOOR LOAD = {round(DL,3)} kPa

WALL LOAD = {round(wall_load,3)} kN/m

ROOF LOAD = {round(roof_load,3)} kPa
""")
