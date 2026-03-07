import streamlit as st

st.set_page_config(page_title="STAAD RC Designer", layout="wide")

st.title("STAAD RC Designer Load Generator")
st.subheader("NSCP 2015 + 1997 UBC Seismic Tool")
st.write("Created by **ENGR. JONAH DAVE T. VEGA**")

st.divider()

# =========================================================
# NEAR SOURCE TABLES (1997 UBC)
# =========================================================

Na_table = {
    "A": [(2,1.5),(5,1.3),(10,1.2),(15,1.1)],
    "B": [(2,1.3),(5,1.2),(10,1.1),(15,1.0)]
}

Nv_table = {
    "A": [(2,2.0),(5,1.6),(10,1.3),(15,1.1)],
    "B": [(2,1.6),(5,1.4),(10,1.2),(15,1.1)]
}

def interpolate(distance, table):

    distances=[x[0] for x in table]
    values=[x[1] for x in table]

    if distance<=distances[0]:
        return values[0]

    if distance>=distances[-1]:
        return values[-1]

    for i in range(len(distances)-1):

        if distances[i] <= distance <= distances[i+1]:

            x1=distances[i]
            x2=distances[i+1]

            y1=values[i]
            y2=values[i+1]

            return y1 + (distance-x1)*(y2-y1)/(x2-x1)

# =========================================================
# SIDEBAR INPUT
# =========================================================

st.sidebar.header("Project Parameters")

zone = st.sidebar.selectbox(
"Seismic Zone",
[0.15,0.20,0.30,0.40]
)

importance = st.sidebar.selectbox(
"Importance Factor (I)",
[1.0,1.25]
)

soil = st.sidebar.selectbox(
"Soil Profile",
["Sa","Sb","Sc","Sd","Se"]
)

source_type = st.sidebar.selectbox(
"Seismic Source Type",
["A","B"]
)

distance = st.sidebar.slider(
"Distance to Active Fault (km)",
0.0,20.0,5.0
)

height = st.sidebar.number_input(
"Building Height (m)",
value=15.0
)

Ct = st.sidebar.number_input(
"Ct Coefficient",
value=0.035
)

# =========================================================
# COMPUTE Na Nv
# =========================================================

Na = interpolate(distance, Na_table[source_type])
Nv = interpolate(distance, Nv_table[source_type])

# =========================================================
# PERIOD
# =========================================================

T = Ct * (height**0.75)

# =========================================================
# LOAD INPUTS
# =========================================================

st.header("Dead Loads (NSCP 2015)")

floor_finish = st.selectbox(
"Floor Finish",
{
"Ceramic Tiles":0.60,
"Marble":0.80,
"Granite":0.90,
"Wood Flooring":0.50
}
)

ceiling = st.selectbox(
"Ceiling Load",
{
"Gypsum Board":0.25,
"Acoustic Ceiling":0.30,
"None":0.0
}
)

partition = st.number_input(
"Partition Load (kPa)",
value=1.0
)

# values
floor_load={
"Ceramic Tiles":0.60,
"Marble":0.80,
"Granite":0.90,
"Wood Flooring":0.50
}[floor_finish]

ceiling_load={
"Gypsum Board":0.25,
"Acoustic Ceiling":0.30,
"None":0.0
}[ceiling]

DL = floor_load + ceiling_load + partition

# =========================================================
# WALL LOAD
# =========================================================

st.header("Wall Load to Beam")

wall_height = st.number_input(
"Wall Height (m)",
value=3.0
)

wall_thickness = st.number_input(
"Wall Thickness (m)",
value=0.15
)

unit_weight = st.number_input(
"Wall Unit Weight (kN/m³)",
value=18.0
)

wall_load = wall_height * wall_thickness * unit_weight

# =========================================================
# ROOF LOADS
# =========================================================

st.header("Roof Dead Loads")

roof_finish = st.selectbox(
"Roof Finish",
{
"Metal Roofing":0.20,
"Waterproofing":0.25,
"Roof Garden":2.50
}
)

roof_load={
"Metal Roofing":0.20,
"Waterproofing":0.25,
"Roof Garden":2.50
}[roof_finish]

# =========================================================
# SUMMARY (TOP SECTION FOR STAAD)
# =========================================================

st.divider()
st.header("STAAD INPUT SUMMARY")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Floor Dead Load (kPa)",round(DL,3))

with col2:
    st.metric("Wall Load to Beam (kN/m)",round(wall_load,3))

with col3:
    st.metric("Roof Load (kPa)",round(roof_load,3))

# =========================================================
# SEISMIC RESULTS
# =========================================================

st.divider()
st.header("Seismic Parameters (1997 UBC)")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("Na",round(Na,3))

with c2:
    st.metric("Nv",round(Nv,3))

with c3:
    st.metric("Period T (sec)",round(T,3))

st.info("""
Use the loads above directly in **STAAD load definitions**.

Example:

FLOOR LOAD  
`{}` kPa  

WALL LOAD ON BEAM  
`{}` kN/m  

ROOF LOAD  
`{}` kPa
""".format(round(DL,3),round(wall_load,3),round(roof_load,3)))
