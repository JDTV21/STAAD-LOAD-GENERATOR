import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# =======================
# Page Config
# =======================
st.set_page_config(
    page_title="PH Structural Load Engine",
    layout="wide",
    page_icon="🏗️"
)

# =======================
# Theme Toggle
# =======================
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        .reportview-container {background-color: #1e1e1e; color: #f0f0f0;}
        .stButton>button {background-color:#00FFFF; color:#000000;}
        </style>
    """, unsafe_allow_html=True)

# =======================
# Title
# =======================
st.markdown(
    "<h1 style='text-align: center; color: #00FFFF;'>🏗️ PH Structural Load Engine</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; color: #FFD700;'>Developed by ENGR. JONAH DAVE T. VEGA</h3>",
    unsafe_allow_html=True
)
st.markdown("---")

# =======================
# Sidebar: Material Properties
# =======================
st.sidebar.header("🧱 Material Unit Weights (kN/m³)")
concrete = st.sidebar.number_input("Concrete", value=24.0)
masonry = st.sidebar.number_input("Masonry / CHB", value=20.0)

# =======================
# Floor Loads
# =======================
st.markdown("### 🏢 Floor Loads (NSCP 2015)")
col1, col2 = st.columns(2)
with col1:
    slab_thk = st.number_input("Slab Thickness (m)", value=0.15)
    floor_finish_option = st.selectbox("Floor Finish", [
        "Ceramic Tiles (1.0 kN/m²)",
        "Marble / Granite (1.2 kN/m²)",
        "Wood / Laminates (0.8 kN/m²)"
    ])
    ceiling_option = st.selectbox("Ceiling Load", [
        "Light Gypsum (0.25 kN/m²)",
        "Heavy Plaster (0.5 kN/m²)",
        "None (0.0 kN/m²)"
    ])
with col2:
    partition_option = st.selectbox("Partition / Wall Load", [
        "Lightweight (1.0 kN/m²)",
        "Heavy Masonry (2.0 kN/m²)",
        "None (0.0 kN/m²)"
    ])
    mep_option = st.selectbox("MEP Allowance", [
        "Standard (0.25 kN/m²)",
        "Minimal / None (0.0 kN/m²)"
    ])
    LL = st.number_input("Live Load (kN/m²)", value=2.0)

# Dictionaries
floor_dict = {"Ceramic Tiles (1.0 kN/m²)":1.0,"Marble / Granite (1.2 kN/m²)":1.2,"Wood / Laminates (0.8 kN/m²)":0.8}
ceiling_dict = {"Light Gypsum (0.25 kN/m²)":0.25,"Heavy Plaster (0.5 kN/m²)":0.5,"None (0.0 kN/m²)":0.0}
partition_dict = {"Lightweight (1.0 kN/m²)":1.0,"Heavy Masonry (2.0 kN/m²)":2.0,"None (0.0 kN/m²)":0.0}
mep_dict = {"Standard (0.25 kN/m²)":0.25,"Minimal / None (0.0 kN/m²)":0.0}

slab_sw = concrete*slab_thk
D_total = slab_sw + floor_dict[floor_finish_option] + ceiling_dict[ceiling_option] + partition_dict[partition_option] + mep_dict[mep_option]

# =======================
# Roof Loads
# =======================
st.markdown("### 🏠 Roof Loads (NSCP 2015)")
col1, col2 = st.columns(2)
with col1:
    roof_type = st.selectbox("Roof Finish", [
        "Light Roof / Metal Sheets",
        "RC Slab w/ Tiles",
        "RC Slab w/ Concrete Finish",
        "Asphalt / Bituminous Shingles",
        "Clay Tiles",
        "Roof Insulation / Lightweight Concrete Finish"
    ])
with col2:
    roof_live = st.number_input("Roof Live Load (kN/m²)", value=0.75)

roof_dead_dict = {
    "Light Roof / Metal Sheets":0.75,
    "RC Slab w/ Tiles":1.00,
    "RC Slab w/ Concrete Finish":1.25,
    "Asphalt / Bituminous Shingles":0.80,
    "Clay Tiles":1.10,
    "Roof Insulation / Lightweight Concrete Finish":0.50
}

# =======================
# Wall Loads
# =======================
st.markdown("### 🧱 Wall Loads to Beams")
wall_present = st.checkbox("Beam Supports Wall?")
if wall_present:
    wall_height = st.number_input("Wall Height (m)", value=3.0)
    wall_thick = st.number_input("Wall Thickness (m)", value=0.15)
    wall_load = masonry*wall_height*wall_thick
else:
    wall_load = 0.0

# =======================
# Wind Load
# =======================
st.markdown("### 🌬️ Wind Load")
V_kph = st.number_input("Basic Wind Speed (kph)", value=250.0)
imp_wind = st.number_input("Importance Factor", value=1.0)
exposure = st.number_input("Exposure Factor", value=1.0)
V = V_kph/3.6
q = 0.613*V**2*imp_wind*exposure/1000

# =======================
# Seismic Loads
# =======================
st.markdown("### 🌐 Seismic Load (UBC 1997)")
zone = st.selectbox("Seismic Zone", ["Zone 4 (Z=0.40)","Zone 3 (Z=0.30)","Zone 2B (Z=0.20)"])
Z_dict={"Zone 4 (Z=0.40)":0.40,"Zone 3 (Z=0.30)":0.30,"Zone 2B (Z=0.20)":0.20}
Z = Z_dict[zone]
I = st.number_input("Importance Factor I", value=1.0)
system = st.selectbox("Structural System", ["Special RC MF","Ordinary RC MF","Dual System"])
R_dict={"Special RC MF":8.5,"Ordinary RC MF":5.5,"Dual System":8.5}
Rx = Rz = R_dict[system]

distance = st.number_input("Distance to Active Fault (km)", value=10.0)
def interp(f1,f2,d1,d2,d): return f1+(f2-f1)*(d-d1)/(d2-d1)
if distance<=2: Na,Nv=1.3,1.6
elif distance<=5: Na=interp(1.3,1.1,2,5,distance); Nv=interp(1.6,1.3,2,5,distance)
elif distance<=10: Na=interp(1.1,1.0,5,10,distance); Nv=interp(1.3,1.0,5,10,distance)
else: Na,Nv=1.0,1.0

height = st.number_input("Total Building Height (m)", value=12.0)
Ct = 0.0731; x=0.75; T=Ct*height**x
W = st.number_input("Total Seismic Weight W (kN)", value=10000.0)
S = 2.5*Na
Cs_x = Z*I*S/Rx; Cs_z = Z*I*S/Rz
Vx = max(Cs_x*W,0.11*Z*I*W)
Vz = max(Cs_z*W,0.11*Z*I*W)

# =======================
# 🔹 Summary Section
# =======================
st.markdown("## 📝 Summary of Loads (STAAD Input)")
summary_data = {
    "Load Type": [
        "Floor Dead Load (kN/m²)",
        "Floor Live Load (kN/m²)",
        "Roof Dead Load (kN/m²)",
        "Roof Live Load (kN/m²)",
        "Wall Load on Beams (kN/m)",
        "Wind Pressure q (kN/m²)",
        "Seismic Base Shear Vx (kN)",
        "Seismic Base Shear Vz (kN)"
    ],
    "Value": [
        round(D_total,2),
        round(LL,2),
        round(roof_dead_dict[roof_type],2),
        round(roof_live,2),
        round(wall_load,2),
        round(q,2),
        round(Vx,2),
        round(Vz,2)
    ]
}
summary_df = pd.DataFrame(summary_data)
st.table(summary_df)

# =======================
# Story Forces Chart (Matplotlib)
# =======================
st.markdown("### 📊 Vertical Distribution of Seismic Forces")
stories = st.number_input("Number of Stories", value=3)
heights=[]; weights=[]
for i in range(int(stories)):
    h = st.number_input(f"Height Story {i+1} (m)", value=(i+1)*3.0)
    w = st.number_input(f"Weight Story {i+1} (kN)", value=2000.0)
    heights.append(h); weights.append(w)

# Calculate Fx
k=1
sum_wh=sum([weights[i]*(heights[i]**k) for i in range(int(stories))])
Fx_list=[(weights[i]*(heights[i]**k)/sum_wh)*Vx for i in range(int(stories))]
df = pd.DataFrame({"Story":[f"Story {i+1}" for i in range(int(stories))], "Fx (kN)": Fx_list})
st.table(df)

# Bar chart with Matplotlib
fig, ax = plt.subplots()
ax.bar(df["Story"], df["Fx (kN)"], color='teal')
ax.set_ylabel("Fx (kN)")
ax.set_xlabel("Story")
ax.set_title("Story Forces Distribution")
for i, v in enumerate(df["Fx (kN)"]):
    ax.text(i, v + 50, f"{v:.1f}", ha='center')
st.pyplot(fig)

# =======================
# Export Option
# =======================
st.markdown("### 💾 Export Results")
if st.button("Export to Excel"):
    df.to_excel("Story_Forces.xlsx", index=False)
    summary_df.to_excel("STAAD_Load_Summary.xlsx", index=False)
    st.success("Exported Story Forces and Summary to Excel")
