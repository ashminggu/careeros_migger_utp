import streamlit as st
import numpy as np
import plotly.graph_objects as go
from google import genai

# ─── APP CONFIGURATION ───
st.set_page_config(page_title="Career OS - Topology Engine", layout="wide")
st.title("Career OS: 3D Path Navigation Engine Nigger 3000 [Topography]")
st.subheader("Visualizing the 40-Year Career Horizon with Data-Driven Geometry")

# ─── SIDEBAR CONTROL PANEL (THE COMPULSORY INPUTS) ───
st.sidebar.header("Candidate Shape Vector")
st.sidebar.write("Adjust skill mastery to watch the mathematical terrain morph (or boleh input variables in terms of salary, career growth, dll.):")

# Interactive sliders that act as inputs to our Z equation
k_kinetics = st.sidebar.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8)
k_math = st.sidebar.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5)
k_cfd = st.sidebar.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3)

st.sidebar.divider()
st.sidebar.info("**note:** Changing the CFD slider instantly lifts the high-yield EV valley on the map (basis on FSUTP)")

# ─── MATHEMATICAL ENGINE ───
# X-Axis: Time (0 to 40 Years)
x_time = np.linspace(0, 40, 50)
# Y-Axis: Categorical Career Pathways (1: Plant Ops, 2: Simulation, 3: EV Tech)
y_paths = np.array([1, 2, 3])

# Create a meshgrid grid coordinate system
X, Y = np.meshgrid(x_time, y_paths)

# Matrix initialization for Elevation (Z)
Z = np.zeros_like(X)

# Calculate Z coordinates based on multi-variable trajectories
for i in range(len(y_paths)):
    path_type = y_paths[i]
    if path_type == 1:  # Path A: Downstream Plant Operations
        # Steady incline that hitting a harsh plateau capping at Year 6
        Z[i, :] = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))
    
    elif path_type == 2:  # Path B: Process Simulation & Optimization
        # Scaled growth driven directly by numerical methods skill vector
        Z[i, :] = 1 + (x_time * (k_math * 0.4))
        
    elif path_type == 3:  # Path C: Next-Gen EV Thermal Management
        # Learning valley early on, followed by high-yield exponential spike
        valley_effect = -2 * np.exp(-((x_time - 3)**2) / 4)  # Dips near year 3
        growth_effect = (x_time * (k_cfd * 0.55))
        Z[i, :] = 1.5 + valley_effect + growth_effect

# ─── PLOTLY 3D SURFACE RENDERING ───
fig = go.Figure(data=[go.Surface(
    x=X, 
    y=Y, 
    z=Z, 
    colorscale='Viridis',
    lighting=dict(ambient=0.6, roughness=0.4),
    colorbar=dict(title="Z: Market Yield / Elevation")
)])

# Axis Customization and Labels
fig.update_layout(
    title='Interactive Career Topology Surface',
    scene=dict(
        xaxis=dict(title='X: Time / Career Horizon (Years)', range=[0, 40]),
        yaxis=dict(
            title='Y: Trajectory Choice',
            tickvals=[1, 2, 3],
            ticktext=['Path A: Downstream Operations', 'Path B: Numerical Simulation', 'Path C: CFD & Thermal Management']
        ),
        zaxis=dict(title='Z: Career Viability & Yield', range=[-1, 20]),
        camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2)) # Sets initial 3D viewing angle
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=700
)

# ─── DISPLAY APP COLUMNS ───
col1, col2 = st.columns([3, 1])

with col1:
    # Render the interactive 3D map
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📋 Navigation Analytics")
    
    # Simple dynamic textual copilot based on state variables
    if k_cfd > 0.7:
        st.success("🎯 **Optimal Pathway Detected:** Your high CFD vector has successfully flattened the early friction valley in the EV Automotive sector. Your 10-year yield looks highly optimized.")
    else:
        st.warning("⚠️ **Plateau Warning:** Your current profile relies heavily on traditional downstream kinetics. Watch out for the flat structural mesa appearing on Path A around Year 6.")
        
    st.markdown("""
    **Axis Definitions:**
    * **X-Axis:** Continuous 40-year career arc timeline.
    * **Y-Axis:** Structural industry domain branches.
    * **Z-Axis:** Career height vector (compensation range + regional stability multiplier).
    """)

# AI Copilot (Google GenAI)
st.divider()
st.subheader("AIMAN.AI: Honest Navigation Copilot")
st.caption("Ask your co-pilot anything. It dynamically tracks your map configuration to give transparent, authentic advice.")

# Securely pull the Gemini API Key from Streamlit's secrets manager
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize dialogue history session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Greetings! I'm Aiman Boge- urgh.. I mean AIMAN.AI b-baka! I analyze your profile vector data against market realities. Which pathway's trade-offs or personal concerns would you like me to deconstruct honestly?"}
    ]

# Render continuous chat elements
for message in st.session_state.messages:
    # If the message is from the assistant, use your custom PNG file
    avatar_img = "aimanai.jpeg" if message["role"] == "assistant" else "user"
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# Process active user interactions
if user_query := st.chat_input("Ask about trade-offs, valleys, or if you're feeling stuck..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # System prompt feeding real-time landscape topology values into the engine's instructions
    system_instruction = f"""
    You are the Career OS Honest Navigation Copilot, a supportive, grounded, and radically candid mentor for a Chemical Engineering student.
    Your tone is empathetic but highly direct—like a helpful peer, not a rigid lecturer. Avoid corporate fluff; speak with data-driven honesty.
    
    The user is looking at a 3D Career Topology Surface map driven by these EXACT live metrics from their profile sliders:
    - Reactor Kinetics Mastery (Path A Core): {k_kinetics}/1.0
    - Numerical Methods Vector (Path B Core): {k_math}/1.0
    - CFD & Thermal Management Vector (Path C Core): {k_cfd}/1.0
    
    The topology surface models 3 interconnected tracks across a 40-year landscape:
    - Path A (Downstream Operations): Stable climb early on, but hits a structural 'Mesa Plateau' at Year 6 due to industry seniority bottlenecks.
    - Path B (Numerical Simulation): High-elevation digital ridge peaking around Year 15. Scales globally but requires strong math optimization.
    - Path C (CFD & Thermal Management): Features a deep 'Learning Valley' from Year 0-3 due to core mechanical engineering entry barriers, but rises exponentially by Year 10 because EV battery thermal systems are fundamentally a thermodynamics/chemical phase-change challenge.
    
    Respond to the user's query naturally. If they express existential dread (e.g., 'Am I suited for this course?'), look at their metrics, validate their feelings authentically, and show them alternative routes on the topology map. If they ask about a path, break down the brutal trade-offs using their metrics. Keep responses clean and scannable using bolding and short paragraphs.
    """

    # Format the chat history logs for context retention
    formatted_contents = []
    for msg in st.session_state.messages[:-1]:
        formatted_contents.append(f"{msg['role'].upper()}: {msg['content']}")
    formatted_contents.append(f"USER: {user_query}")

    # Generate streaming/live inference text output
    with st.chat_message("assistant", avatar="aimanai.jpeg"):
        response_placeholder = st.empty()
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=formatted_contents,
            config={"system_instruction": system_instruction}
        )
        
        ai_text = response.text
        response_placeholder.markdown(ai_text)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_text})
