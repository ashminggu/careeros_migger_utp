import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─── APP CONFIGURATION ───
st.set_page_config(page_title="Career OS - Path Engine", layout="wide")
st.title("🌐 Career OS: 3D Path Navigation Engine")
st.subheader("Isolating Discrete Trajectories Across a 40-Year Horizon")

# ─── SIDEBAR CONTROL PANEL ───
st.sidebar.header("🛠️ Candidate Shape Vector")
st.sidebar.write("Adjust your skill mastery to watch the paths morph dynamically:")

k_kinetics = st.sidebar.slider("Reactor Kinetics Mastery (Path A Core)", 0.1, 1.0, 0.8)
k_math = st.sidebar.slider("Numerical Methods / Runge-Kutta (Path B Core)", 0.1, 1.0, 0.5)
k_cfd = st.sidebar.slider("CFD & Thermal Management (Path C Core)", 0.1, 1.0, 0.3)

st.sidebar.divider()
st.sidebar.info("💡 **UX Improvement:** By plotting separate lines instead of a massive surface, the user can easily see where the paths diverge from 'The Launchpad'.")

# ─── MATHEMATICAL ENGINE (INDEPENDENT PATH LINES) ───
# X-Axis: Time / Timeline (0 to 40 Years)
x_time = np.linspace(0, 40, 100)

# --- Path A: Downstream Plant Operations ---
y_path_a = np.full_like(x_time, 1) # Holds constant on Y-axis coordinate 1
# Steady incline that hits a harsh plateau capping at Year 6
z_path_a = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))

# --- Path B: Process Simulation & Optimization ---
y_path_b = np.full_like(x_time, 2) # Holds constant on Y-axis coordinate 2
# Scaled growth driven directly by numerical methods skill vector
z_path_b = 1 + (x_time * (k_math * 0.4))

# --- Path C: Next-Gen EV Thermal Management ---
y_path_c = np.full_like(x_time, 3) # Holds constant on Y-axis coordinate 3
# Learning valley early on, followed by high-yield exponential spike
valley_effect = -2 * np.exp(-((x_time - 3)**2) / 4)
growth_effect = (x_time * (k_cfd * 0.55))
z_path_c = 1.5 + valley_effect + growth_effect


# ─── PLOTLY 3D LINE RENDERING ───
fig = go.Figure()

# Add Path A Line
fig.add_trace(go.Scatter3d(
    x=x_time, y=y_path_a, z=z_path_a,
    mode='lines',
    name='Path A: Plant Ops',
    line=dict(color='#2ecc71', width=8), # Solid green
    hovertemplate='<b>Plant Ops</b><br>Year: %{x:.1f}<br>Yield: %{z:.2f}<extra></extra>'
))

# Add Path B Line
fig.add_trace(go.Scatter3d(
    x=x_time, y=y_path_b, z=z_path_b,
    mode='lines',
    name='Path B: Simulation',
    line=dict(color='#3498db', width=8), # Solid blue
    hovertemplate='<b>Simulation</b><br>Year: %{x:.1f}<br>Yield: %{z:.2f}<extra></extra>'
))

# Add Path C Line
fig.add_trace(go.Scatter3d(
    x=x_time, y=y_path_c, z=z_path_c,
    mode='lines',
    name='Path C: EV Thermal',
    line=dict(color='#e67e22', width=8), # Solid orange
    hovertemplate='<b>EV Thermal</b><br>Year: %{x:.1f}<br>Yield: %{z:.2f}<extra></extra>'
))

# Add a pulsing highlight for "The Launchpad" initialization point
fig.add_trace(go.Scatter3d(
    x=[0], y=[2], z=[1.5],
    mode='markers',
    name='The Launchpad (t=0)',
    marker=dict(size=10, color='#ffffff', symbol='diamond', line=dict(color='#9b59b6', width=2))
))

# Axis Customization and Labels
# Axis Customization and Labels
fig.update_layout(
    scene=dict(
        xaxis=dict(
            title='X: Time / Horizon (Years)', 
            range=[0, 40], 
            gridcolor="rgba(255, 255, 255, 0.1)"  # Moved inside xaxis
        ),
        yaxis=dict(
            title='Y: Trajectory Choice',
            tickvals=[1, 2, 3],
            ticktext=['Path A: Plant Ops', 'Path B: Simulation', 'Path C: EV Thermal'],
            range=[0.5, 3.5],
            gridcolor="rgba(255, 255, 255, 0.1)"  # Moved inside yaxis
        ),
        zaxis=dict(
            title='Z: Career Viability & Yield', 
            range=[-1, 20],
            gridcolor="rgba(255, 255, 255, 0.1)"  # Moved inside zaxis
        ),
        camera=dict(eye=dict(x=1.5, y=-1.5, z=1.0))
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=700,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# ─── DISPLAY APP COLUMNS ───
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📋 Navigation Analytics")
    
    if k_cfd > 0.7:
        st.success("🎯 **Optimal Pathway Detected:** Your high CFD vector has successfully flattened the early friction valley in the EV Automotive sector. Your 10-year yield looks highly optimized.")
    else:
        st.warning("⚠️ **Plateau Warning:** Your current profile relies heavily on traditional downstream kinetics. Watch out for the flat structural mesa appearing on Path A around Year 6.")
        
    st.markdown("""
    **Visual Paradigm Shift:**
    By unlinking the mesh, the system now displays **highways of potential**. This clarifies the *agency* aspect of the brief—the user can visibly pick a lane to track, analyze the independent elevation curves, and understand where paths structurally diverge.
    """)