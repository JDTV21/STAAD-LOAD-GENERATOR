import streamlit as st

st.set_page_config(page_title="STAAD Load Generator", layout="wide")

st.title("STAAD Load Generator")
st.subheader("NSCP 2015 + 1997 UBC Seismic Parameters")
st.write("Developed by **ENGR. JONAH DAVE T. VEGA**")

st.divider()

# ==========================================
# UBC 1997 NEAR SOURCE TABLE VALUES
# ==========================================

Na_table = {
"A":[(2,1.5),(5,1.3),(10,1.2),(15,1.1)],
"B":[(2,1.3),(5,1.2),(10,1.1),(15,1.0)]
}

Nv_table = {
"A":[(2,2.0),(5,1.6),(10,1.3),(15,1.1)],
"B":[(2,1.6),(5,1.4),(10,1.2),(15,1.1)]
}

def interpolate(distance,data):

    x=[d[0] for d in data]
    y=[d[1] for d in data]

    if distance<=x[0]:
        return y[0]

    if distance>=x[-1]:
        return y[-1]

    for i in range(len(x)-1):

        if x[i]<=distance<=x[i+1]:

            x1=x[i]
            x2=x[i+1]

            y1=y[i]
            y2=y[i+1]

            return y1+(distance-x1)*(y2-y1)/(x2-x1)

# ==========================================
# SEISMIC INPUT PARAMETERS
# ==========================================

st.sidebar.header("Seismic Parameters")

zone = st.sidebar.selectbox(
"Seismic Zone Factor Z",
[0.15,0.20,0.30,0.40]
)

importance = st.sidebar.selectbox(
"Importance Factor I",
[1.0,1.25]
)

soil_profile = st.sidebar.selectbox(
"Soil Profile",
["Sa","Sb","Sc","Sd","Se"]
)

source_type = st.sidebar.selectbox(
"Seismic Source Type",
["A","B"]
)

distance = st.sidebar.number_input(
"Distance to Active Fault (km)",
value=5.0,
min_value=0.0
)

building_height = st.sidebar.number_input(
"Building Height (m)",
value=15.0
)

Ct = st.sidebar.number_input(
"Ct Coefficient",
value=0.035
)

# ==========================================
# COMPUTE Na Nv
# ==========================================

Na = interpolate(distance,Na_table[source_type])
Nv = interpolate(distance,Nv_table[source_type])

# ==========================================
# PERIOD
# ==========================================

T = Ct*(building_height**0.75)

# ==========================================
# DEAD LOAD SECTION
# ==========================================

st.header("Floor Dead Loads (NSCP 2015)")

floor_options={
"Ceramic Tiles":0.60,
"Marble":0.80,
"Granite":0.90,
"Wood Flooring":0.50
}

ceiling_options={
"Gypsum Ceiling":0.25,
"Acoustic Ceiling":0.30,
"No Ceiling":0
}

floor_type=st.selectbox("Floor Finish",list(floor_options.keys()))
ceiling_type=st.selectbox("Ceiling Type",list(ceiling_options.keys()))

partition=st.number_input(
"Partition Load (kPa)",
value=1.0
)

floor_load=floor_options[floor_type]
ceiling_load=ceiling_options[ceiling_type]

DL=floor_load+ceiling_load+partition

# ==========================================
# WALL LOAD TO BEAMS
# ==========================================

st.header("Wall Load to Beam")

wall_height=st.number_input(
"Wall Height (m)",
value=3.0
)

wall_thickness=st.number_input(
"Wall Thickness (m)",
value=0.15
)

unit_weight=st.number_input(
"Wall Unit Weight (kN/m³)",
value=18.0
)

wall_load=wall_height*wall_thickness*unit_weight

# ==========================================
# ROOF LOADS
# ==========================================

st.header("Roof Dead Loads")

roof_options={
"Metal Roof":0.20,
"Waterproofing":0.25,
"Green Roof":2.50
}

roof_type=st.selectbox("Roof Finish",list(roof_options.keys()))
roof_load=roof_options[roof_type]

# ==========================================
# STAAD SUMMARY (TOP RESULT)
# ==========================================

st.divider()
st.header("STAAD LOAD SUMMARY")

col1,col2,col3=st.columns(3)

with col1:
    st.metric("Floor Dead Load (kPa)",round(DL,3))

with col2:
    st.metric("Wall Load to Beam (kN/m)",round(wall_load,3))

with col3:
    st.metric("Roof Load (kPa)",round(roof_load,3))

# ==========================================
# SEISMIC RESULTS
# ==========================================

st.divider()
st.header("Seismic Results (1997 UBC)")

c1,c2,c3=st.columns(3)

with c1:
    st.metric("Na",round(Na,3))

with c2:
    st.metric("Nv",round(Nv,3))

with c3:
    st.metric("Period T (sec)",round(T,3))

st.info(f"""
Use these loads in **STAAD**:

FLOOR LOAD = {round(DL,3)} kPa  

WALL LOAD = {round(wall_load,3)} kN/m  

ROOF LOAD = {round(roof_load,3)} kPa
""")
