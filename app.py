import streamlit as st
import math

# =======================
# Page Config
# =======================
st.set_page_config(
    page_title="PH Structural Load Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🇵🇭 Philippine Structural Load Engine")
st.subheader("Developed by ENGR. JONAH DAVE T. VEGA")
st.write("Beam self-weight excluded (Use SELFWEIGHT Y -1 in STAAD)")
st.write("Only WALL loads applied to beams (No slab-to-beam transfer)")

# =======================
# Material Properties
# =======================
st.sidebar.header("Material Unit Weights (kN/m³)")
concrete = st.sidebar.number_input("Concrete", value=24.0)
masonry = st.sidebar.number_input("Masonry / CHB", value=20.0)

# =======================
# Floor Loads (NSCP 2015 Dropdowns)
# =======================
st.header("1️⃣ FLOOR LOADS (kN/m²)")

slab_thk = st.number_input("Slab Thickness (m)", value=0.15)
slab_sw = concrete * slab_thk

# Floor Finish Dropdown
floor_finish_option = st.selectbox("Floor Finish (NSCP 2015)", [
    "Ceramic Tiles (1.0 kN/m²)",
    "Marble / Granite (1.2 kN/m²)",
    "Wood / Laminates (0.8 kN/m²)"
])

floor_finish_dict = {
    "Ceramic Tiles (1.0 kN/m²)": 1.0,
    "Marble / Granite (1.2 kN/m²)": 1.2,
    "Wood / Laminates (0.8 kN/m²)": 0.8
}

finish = floor_finish_dict[floor_finish_option]

# Ceiling Dropdown
ceiling_option = st.selectbox("Ceiling Load (NSCP 2015)", [
    "Light Gypsum Ceiling (0.25 kN/m²)",
    "Heavy Plaster Ceiling (0.5 kN/m²)",
    "None (0.0 kN/m²)"
])

ceiling_dict = {
    "Light Gypsum Ceiling (0.25 kN/m²)": 0.25,
    "Heavy Plaster Ceiling (0.5 kN/m²)": 0.5,
    "None (0.0 kN/m²)": 0.0
}

ceiling = ceiling_dict[ceiling_option]

# Partition / Walls Dropdown
partition_option = st.selectbox("Partition / Wall Load (NSCP 2015)", [
    "Lightweight Partition (1.0 kN/m²)",
    "Heavy Masonry Walls (2.0 kN/m²)",
    "None (0.0 kN/m²)"
])

partition_dict = {
    "Lightweight Partition (1.0 kN/m²)": 1.0,
    "Heavy Masonry Walls (2.0 kN/m²)": 2.0,
    "None (0.0 kN/m²)": 0.0
}

partition = partition_dict[partition_option]

# MEP Allowance Dropdown
mep_option = st.selectbox("MEP Allowance (NSCP 2015)", [
    "Standard (0.25 kN/m²)",
    "Minimal / None (0.0 kN/m²)"
])

mep_dict = {
    "Standard (0.25 kN/m²)": 0.25,
    "Minimal / None (0.0 kN/m²)": 0.0
}

mep = mep_dict[mep_option]

# Total Dead Load
total_dead_floor = slab_sw + finish + ceiling + mep + partition
st.success(f"Total Floor Dead Load D = {total_dead_floor:.2f} kN/m²")

# Live Load
LL = st.number_input("Live Load L (kN/m²)", value=2.0)
st.success(f"Live Load L = {LL:.2f} kN/m²")

# =======================
# Roof Loads (NSCP 2015)
# =======================
st.header("2️⃣ ROOF LOADS (kN/m²)")

roof_type = st.selectbox("Select Roof Type / Finish (NSCP 2015)", [
    "Light Roof / Metal Sheets",
    "RC Roof Slab with Tiles",
    "RC Roof Slab with Concrete Finish",
    "Asphalt / Bituminous Shingles",
    "Clay Tiles",
    "Roof Insulation / Lightweight Concrete Finish"
])

roof_dead_dict = {
    "Light Roof / Metal Sheets": 0.75,
    "RC Roof Slab with Tiles": 1.00,
    "RC Roof Slab with Concrete Finish": 1.25,
    "Asphalt / Bituminous Shingles": 0.80,
    "Clay Tiles": 1.10,
    "Roof Insulation / Lightweight Concrete Finish": 0.50
}

roof_dead = roof_dead_dict[roof_type]

roof_live = st.number_input("Roof Live Load (kN/m²)", value=0.75)

st.success(f"Roof Dead Load based on NSCP 2015 = {roof_dead:.2f} kN/m²")
st.success(f"Roof Live Load = {roof_live:.2f} kN/m²")

# =======================
# Wall Loads to Beams Only
# =======================
st.header("3️⃣ WALL LOAD TO BEAMS (kN/m)")

wall_present = st.checkbox("Beam Supports Wall?")

wall_load = 0

if wall_present:
    wall_height = st.number_input("Wall Height (m)", value=3.0)
    wall_thickness = st.number_input("Wall Thickness (m)", value=0.15)
    wall_load = masonry * wall_height * wall_thickness
    st.success(f"Wall Load on Beam = {wall_load:.2f} kN/m")

# =======================
# Wind Load
# =======================
st.header("4️⃣ WIND LOAD")

V_kph = st.number_input("Basic Wind Speed (kph)", value=250.0)
importance_wind = st.number_input("Wind Importance Factor", value=1.0)
exposure = st.number_input("Exposure Factor", value=1.0)

V = V_kph / 3.6
q = 0.613 * V**2 * importance_wind * exposure / 1000
st.success(f"Velocity Pressure q = {q:.2f} kN/m²")

# =======================
# SEISMIC LOAD - UBC 1997
# =======================
st.header("5️⃣ SEISMIC LOAD (UBC 1997)")

# Zone
zone = st.selectbox("Seismic Zone", [
    "Zone 4 (Z = 0.40)",
    "Zone 3 (Z = 0.30)",
    "Zone 2B (Z = 0.20)"
])

Z_values = {
    "Zone 4 (Z = 0.40)": 0.40,
    "Zone 3 (Z = 0.30)": 0.30,
    "Zone 2B (Z = 0.20)": 0.20
}
Z = Z_values[zone]

I = st.number_input("Seismic Importance Factor (I)", value=1.0)

# Response Modification Factors
st.subheader("Structural System")
system = st.selectbox("Select Structural System", [
    "Special RC Moment Frame (Rx=8.5, Rz=8.5)",
    "Ordinary RC Moment Frame (Rx=5.5, Rz=5.5)",
    "Dual System (Rx=8.5, Rz=8.5)"
])
R_dict = {
    "Special RC Moment Frame (Rx=8.5, Rz=8.5)": (8.5, 8.5),
    "Ordinary RC Moment Frame (Rx=5.5, Rz=5.5)": (5.5, 5.5),
    "Dual System (Rx=8.5, Rz=8.5)": (8.5, 8.5)
}
Rx, Rz = R_dict[system]
st.write(f"Rx = {Rx}")
st.write(f"Rz = {Rz}")

# Near Source Factors
st.subheader("Near Source Factors (Na, Nv) with Interpolation")
distance = st.number_input("Distance to Active Fault (km)", value=10.0)
def interpolate(f1,f2,d1,d2,d):
    return f1 + (f2-f1)*(d-d1)/(d2-d1)

if distance <=2:
    Na,Nv = 1.3,1.6
elif distance <=5:
    Na = interpolate(1.3,1.1,2,5,distance)
    Nv = interpolate(1.6,1.3,2,5,distance)
elif distance <=10:
    Na = interpolate(1.1,1.0,5,10,distance)
    Nv = interpolate(1.3,1.0,5,10,distance)
else:
    Na,Nv = 1.0,1.0
st.write(f"Interpolated Na = {Na:.3f}")
st.write(f"Interpolated Nv = {Nv:.3f}")

# Period
st.subheader("Approximate Period")
height = st.number_input("Total Building Height (m)", value=12.0)
Ct = 0.0731
x = 0.75
T = Ct * (height**x)
st.write(f"Ct = {Ct}")
st.write(f"T = {T:.3f} sec")

# Seismic Coefficient
S = 2.5*Na
Cs_x = (Z*I*S)/Rx
Cs_z = (Z*I*S)/Rz
W = st.number_input("Total Seismic Weight W (kN)", value=10000.0)
Vx = Cs_x*W
Vz = Cs_z*W
Vmin = 0.11*Z*I*W
Vx = max(Vx,Vmin)
Vz = max(Vz,Vmin)
st.success(f"Base Shear Vx = {Vx:.2f} kN")
st.success(f"Base Shear Vz = {Vz:.2f} kN")

# Story Forces
st.header("6️⃣ Vertical Distribution of Seismic Forces")
stories = st.number_input("Number of Stories", value=3)
story_heights=[]
story_weights=[]
for i in range(int(stories)):
    st.subheader(f"Story {i+1}")
    h = st.number_input(f"Height to Story {i+1} (m)", value=(i+1)*3.0)
    w = st.number_input(f"Seismic Weight at Story {i+1} (kN)", value=2000.0)
    story_heights.append(h)
    story_weights.append(w)
k = 1
sum_wh = sum([story_weights[i]*(story_heights[i]**k) for i in range(int(stories))])
st.subheader("Story Forces Fx (Seismic Load Distribution)")
for i in range(int(stories)):
    Fx = (story_weights[i]*(story_heights[i]**k)/sum_wh)*Vx
    st.write(f"Story {i+1} Force Fx = {Fx:.2f} kN")
st.success("Seismic forces distributed per UBC 1997")
st.success("Use SELFWEIGHT Y -1 in STAAD")
