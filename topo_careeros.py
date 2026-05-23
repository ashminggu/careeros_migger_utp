import streamlit as st
import numpy as np
import plotly.graph_objects as go
from google import genai

# ─── APP CONFIGURATION ───
st.set_page_config(page_title="Career OS - Ecosystem", layout="wide")

# ─── NAVIGATION TABS ───
# This creates two clean tabs at the very top of your webapp interface
tab1, tab2 = st.tabs(["3D Career Navigation & AIMAN.AI Copilot", "Live Internship Marketplace"])

# ==============================================================================
# 🏢 TAB 1: THE TOPO GRAPH & AI COPILOT MODULE
# ==============================================================================
with tab1:
    st.title("Career OS: 3D Path Navigation Engine by Migger3000")
    st.subheader("Visualizing the 40-Year Career Horizon with Data-Driven Geometry")

    # ─── SIDEBAR CONTROL PANEL ───
    st.sidebar.header("Candidate Shape Vector")
    st.sidebar.write("Adjust skill mastery to watch the mathematical terrain morph:")

    k_kinetics = st.sidebar.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8)
    k_math = st.sidebar.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5)
    k_cfd = st.sidebar.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3)

    st.sidebar.divider()
    st.sidebar.info("**note:** Changing the CFD slider instantly lifts the high-yield EV valley on the map (basis on FSUTP)")

    # ─── MATHEMATICAL ENGINE ───
    x_time = np.linspace(0, 40, 50)
    y_paths = np.array([1, 2, 3])
    X, Y = np.meshgrid(x_time, y_paths)
    Z = np.zeros_like(X)

    for i in range(len(y_paths)):
        path_type = y_paths[i]
        if path_type == 1:
            Z[i, :] = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))
        elif path_type == 2:
            Z[i, :] = 1 + (x_time * (k_math * 0.4))
        elif path_type == 3:
            valley_effect = -2 * np.exp(-((x_time - 3)**2) / 4)
            growth_effect = (x_time * (k_cfd * 0.55))
            Z[i, :] = 1.5 + valley_effect + growth_effect

    # ─── PLOTLY 3D SURFACE RENDERING ───
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z, colorscale='Viridis',
        lighting=dict(ambient=0.6, roughness=0.4),
        colorbar=dict(title="Z: Market Yield / Elevation")
    )])

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
            camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=40), height=600
    )

    # ─── DISPLAY APP COLUMNS ───
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### 📋 Navigation Analytics")
        if k_cfd > 0.7:
            st.success("🎯 **Optimal Pathway Detected:** Your high CFD vector has successfully flattened the early friction valley in the EV Automotive sector.")
        else:
            st.warning("⚠️ **Plateau Warning:** Your current profile relies heavily on traditional downstream kinetics. Watch out for the flat structural mesa appearing on Path A around Year 6.")
        st.markdown("""
        **Axis Definitions:**
        * **X-Axis:** Continuous 40-year career arc timeline.
        * **Y-Axis:** Structural industry domain branches.
        * **Z-Axis:** Career height vector (compensation range + regional stability multiplier).
        """)

    # ─── THE LIVE HUMAN AI COPILOT LAYER ───
    st.divider()
    st.subheader("🤖 Career OS: Honest Navigation Copilot")
    st.caption("Ask your co-pilot anything. It dynamically tracks your map configuration to give transparent, authentic advice.")

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Greetings! I'm Aiman Boge- urgh.. I mean AIMAN.AI b-baka! I analyze your profile vector data against market realities. Which pathway's trade-offs or personal concerns would you like me to deconstruct honestly?"}
        ]

    for message in st.session_state.messages:
        avatar_img = "aimanai.jpeg" if message["role"] == "assistant" else "user"
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask about trade-offs, valleys, or if you're feeling stuck..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        system_instruction = f"""
        You are the Career OS Honest Navigation Copilot, a supportive, grounded, and radically candid mentor for a Chemical Engineering student.
        Your tone is empathetic but highly direct—like a helpful peer, not a rigid lecturer. Avoid corporate fluff; speak with data-driven honesty.
        The user is looking at a 3D Career Topology Surface map driven by these EXACT live metrics from their profile sliders:
        - Reactor Kinetics Mastery (Path A Core): {k_kinetics}/1.0
        - Numerical Methods Vector (Path B Core): {k_math}/1.0
        - CFD & Thermal Management Vector (Path C Core): {k_cfd}/1.0
        Keep responses clean and scannable using bolding and short paragraphs.
        """

        formatted_contents = []
        for msg in st.session_state.messages[:-1]:
            formatted_contents.append(f"{msg['role'].upper()}: {msg['content']}")
        formatted_contents.append(f"USER: {user_query}")
        
        with st.chat_message("assistant", avatar="aimanai.jpeg"):
            response_placeholder = st.empty()
            response = client.models.generate_content(
                model='gemini-2.5-flash', contents=formatted_contents, config={"system_instruction": system_instruction}
            )
            ai_text = response.text
            response_placeholder.markdown(ai_text)
        st.session_state.messages.append({"role": "assistant", "content": ai_text})

# ==============================================================================
# 💼 TAB 2: LIVE INTERNSHIP MARKETPLACE MODULE (FOR YOUR FRIEND)
# ==============================================================================
with tab2:
    st.title("💼 Live Internship Marketplace")
    st.subheader("Verifiable Anti-Spam Career Deployment Portals")
    st.write("Unlike traditional job boards, these listings map directly to specific coordinates on your 3D career trajectory.")

    # Mock Data Catalogue for internships
    internships = [
        {
            "company": "PETRONAS Carigali",
            "role": "Downstream Process Operations Intern",
            "course": "Chemical Engineering",
            "duration": "8 Months (May - Dec)",
            "scope": "Assist in daily monitoring of multi-phase separator constraints. Conduct molar mass balances and evaluate catalyst deactivation profiles for production optimization blocks.",
            "impact": "➕ Lifts your [Path A] Reactor Kinetics vector by +0.3 upon verified completion."
        },
        {
            "company": "Proton R&D (NxGV Division)",
            "role": "Battery Thermal Management Simulation Trainee",
            "course": "Mechanical / Chemical Engineering",
            "duration": "6 Months (June - Nov)",
            "scope": "Develop transient thermal fluid simulations for liquid-cooled lithium-ion battery packs. Conduct geometric grid meshing and execute thermal FMEA matrix tracking.",
            "impact": "➕ Lifts your [Path C] CFD & Thermal Management vector by +0.4 upon verified completion."
        },
        {
            "company": "AspenTech Systems",
            "role": "Process Digital Twin Engineer Intern",
            "course": "Chemical / Software Engineering",
            "duration": "6 Months (Jan - June)",
            "scope": "Formulate dynamic numerical simulation models for distillation columns using custom Runge-Kutta convergence blocks. Build localized data-scraping pipelines.",
            "impact": "➕ Lifts your [Path B] Numerical Methods vector by +0.35 upon verified completion."
        },
        {
            "company": "Intel Malaysia",
            "role": "Substrate Thermal Dissipation Intern",
            "course": "Mechanical / Electrical Engineering",
            "duration": "4 Months (May - Aug)",
            "scope": "Analyze micro-component convective heat fluxes on advanced silicon substrates. Run localized finite element analysis (FEA) and testing arrays.",
            "impact": "➕ Lifts your [Path C] CFD & Thermal Management vector by +0.2 upon verified completion."
        }
    ]

    # ─── FILTER UI CONTROLS ───
    st.markdown("### 🔍 Filter Positions")
    course_options = ["All", "Chemical Engineering", "Mechanical / Chemical Engineering", "Chemical / Software Engineering", "Mechanical / Electrical Engineering"]
    selected_course = st.selectbox("Select Your Academic Domain Discipline:", course_options)

    st.divider()

    # ─── DYNAMIC CATALOGUE RENDERING ───
    st.markdown("### 📋 Available Trajectory Placements")
    
    # Loop through data and apply filter logic
    for job in internships:
        if selected_course == "All" or job["course"] == selected_course:
            
            # Using st.expander makes a beautifully clean, clickable drop-down card for each role
            with st.expander(f"🏢 {job['company']} ── {job['role']}"):
                
                # Layout columns inside the card for high scannability
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.markdown(f"**Target Discipline:** `{job['course']}`")
                    st.markdown(f"**Duration:** {job['duration']}")
                    st.markdown("**Core Job Scope & Responsibilities:**")
                    st.write(job["scope"])
                
                with c2:
                    st.info(f"🏆 **Trajectory Vector Impact:**\n\n{job['impact']}")
                    if st.button("Deploy Application", key=f"btn_{job['company']}_{job['role']}"):
                        st.success(f"Application securely deployed to {job['company']}! Your Live Portfolio vector shapes have been transmitted.")
