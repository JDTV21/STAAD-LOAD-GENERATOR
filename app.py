import streamlit as st

st.set_page_config(page_title="STAAD Structural Load Generator",layout="wide")

st.title("STAAD Structural Load Generator")
st.write("NSCP 2015 + UBC 1997")
st.write("Developed by **ENGR. JONAH DAVE T. VEGA**")

st.divider()

# ------------------------------------------------
# PROJECT DATA
# ------------------------------------------------

st.header("Project Geometry")

c1,c2,c3 = st.columns(3)

with c1:
    floors = st.number_input("Number of Floors",value=3)

with c2:
    floor_height = st.number_input("Floor Height (m)",value=3.0)

with c3:
    building_height = floors * floor_height
    st.metric("Building Height",building_height)

# ------------------------------------------------
# DEAD LOADS
# ------------------------------------------------

st.divider()
st.header("Dead Loads")

floor_finish = {
"Ceramic Tile":0.60,
"Granite":0.90,
"Marble":0.80,
"Wood":0.50
}

ceiling = {
"Gypsum":0.25,
"Acoustic":0.30,
"No Ceiling":0
}

c1,c2,c3 = st.columns(3)

with c1:
    floor_type = st.selectbox("Floor Finish",floor_finish.keys())

with c2:
    ceiling_type = st.selectbox("Ceiling",ceiling.keys())

with c3:
    partition = st.number_input("Partition Load kPa",value=1.0)

DL = floor_finish[floor_type] + ceiling[ceiling_type] + partition

# ------------------------------------------------
# WALL LOAD
# ------------------------------------------------

st.header("Wall Load to Beam")

c1,c2,c3 = st.columns(3)

with c1:
    wall_height = st.number_input("Wall Height",value=3.0)

with c2:
    wall_thickness = st.number_input("Wall Thickness",value=0.15)

with c3:
    unit_weight = st.number_input("Wall Unit Weight",value=18.0)

wall_load = wall_height * wall_thickness * unit_weight

# ------------------------------------------------
# LIVE LOAD
# ------------------------------------------------

st.divider()
st.header("Live Load")

live_load = {
"Residential":2.0,
"Office":2.4,
"Corridor":4.8,
"Stairs":4.8,
"Roof":0.75
}

occupancy = st.selectbox("Occupancy",live_load.keys())

LL = live_load[occupancy]

# ------------------------------------------------
# SEISMIC PARAMETERS
# ------------------------------------------------

st.divider()
st.header("Seismic Parameters UBC 1997")

c1,c2,c3 = st.columns(3)

with c1:

    Z = st.selectbox("Zone Factor Z",[0.15,0.20,0.30,0.40])

    I = st.selectbox("Importance Factor",[1.0,1.25])

with c2:

    soil = st.selectbox("Soil Profile",["Sa","Sb","Sc","Sd","Se"])

    source = st.selectbox("Seismic Source Type",["A","B"])

with c3:

    distance = st.number_input("Distance to Fault km",value=5.0)

# ------------------------------------------------
# Na Nv TABLES
# ------------------------------------------------

Na_table = {
"A":[(2,1.5),(5,1.3),(10,1.2),(15,1.1)],
"B":[(2,1.3),(5,1.2),(10,1.1),(15,1.0)]
}

Nv_table = {
"A":[(2,2.0),(5,1.6),(10,1.3),(15,1.1)],
"B":[(2,1.6),(5,1.4),(10,1.2),(15,1.1)]
}

def interpolate(d,data):

    x=[i[0] for i in data]
    y=[i[1] for i in data]

    if d<=x[0]: return y[0]
    if d>=x[-1]: return y[-1]

    for i in range(len(x)-1):

        if x[i]<=d<=x[i+1]:

            x1=x[i]
            x2=x[i+1]

            y1=y[i]
            y2=y[i+1]

            return y1+(d-x1)*(y2-y1)/(x2-x1)

Na = interpolate(distance,Na_table[source])
Nv = interpolate(distance,Nv_table[source])

# ------------------------------------------------
# STRUCTURAL SYSTEM
# ------------------------------------------------

st.subheader("Structural System")

system = st.selectbox("System",
["RC Moment Frame",
"Steel Moment Frame",
"Braced Frame",
"Shear Wall"])

if system=="RC Moment Frame":
    R=8.5
    Ct=0.035

elif system=="Steel Moment Frame":
    R=8
    Ct=0.028

elif system=="Braced Frame":
    R=6
    Ct=0.03

elif system=="Shear Wall":
    R=5.5
    Ct=0.02

# ------------------------------------------------
# PERIOD
# ------------------------------------------------

T = Ct * (building_height ** 0.75)

# ------------------------------------------------
# SEISMIC COEFFICIENT
# ------------------------------------------------

Cs = (Z*I)/R

# ------------------------------------------------
# BASE SHEAR
# ------------------------------------------------

W = DL * floors

V = Cs * W

# ------------------------------------------------
# RESULTS
# ------------------------------------------------

st.divider()
st.header("Seismic Results")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("Na",round(Na,3))

with c2:
    st.metric("Nv",round(Nv,3))

with c3:
    st.metric("Period T",round(T,3))

with c4:
    st.metric("Base Shear V",round(V,3))

# ------------------------------------------------
# STAAD OUTPUT
# ------------------------------------------------

st.divider()
st.header("STAAD Load Commands")

staad = f"""
DEFINE UBC LOAD
ZONE {Z}
I {I}
NA {round(Na,3)}
NV {round(Nv,3)}
RX {R}
RZ {R}

LOAD 1 DEAD LOAD
FLOOR LOAD
YRANGE 0 {floor_height} FLOAD -{DL}

MEMBER LOAD
UNI GY -{wall_load}

LOAD 2 LIVE LOAD
FLOOR LOAD
YRANGE 0 {floor_height} FLOAD -{LL}
"""

st.code(staad)
