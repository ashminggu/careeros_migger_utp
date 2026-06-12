import streamlit as st
import numpy as np
import plotly.graph_objects as go
from google import genai

# ─── APP CONFIGURATION ───
st.set_page_config(page_title="CariKerja.com - Ecosystem", layout="wide", initial_sidebar_state="collapsed")

# Initialize dialogue history session state early
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selamat Sejahtera! I'm AIMAN.AI, your dynamic Career OS Copilot. I analyze your profile vector data against market realities. Which pathway's trade-offs or personal concerns would you like me to deconstruct honestly?"}
    ]

# ─── ADVANCED FIGMA-STYLE CSS UI OVERRIDES ───
st.markdown("""
    <style>
    /* Global Background tech grid layout mesh */
    .stApp {
        background-color: #0b0f17;
        background-image: 
            linear-gradient(rgba(99, 102, 241, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99, 102, 241, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    
    /* Outer layout positioning frame */
    .landing-center-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding-top: 5%;
    }

    /* ─── HERO GLASS PANEL ─── */
    .hero-glass-panel {
        background: rgba(17, 22, 34, 0.65);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 24px;
        padding: 60px 40px;
        max-width: 1200px;
        width: 100%;
        text-align: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        margin-bottom: 60px;
    }
    
    .landing-title {
        font-size: 96px;
        font-weight: 900;
        letter-spacing: -3px;
        line-height: 1.1;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .landing-subtitle {
        font-size: 24px;
        color: #9ca3af;
        margin-bottom: 50px;
        font-weight: 300;
        max-width: 700px;
        line-height: 1.5;
    }
    
    .features-tray {
        display: flex;
        gap: 20px;
        justify-content: center;
        width: 100%;
    }
    
    .feature-card {
        background: rgba(10, 14, 23, 0.6) !important;
        border: 1px solid rgba(240, 246, 252, 0.06) !important;
        border-radius: 16px;
        padding: 24px;
        flex: 1;
        text-align: left;
    }
    
    .icon-box {
        font-size: 32px;
        margin-bottom: 12px;
    }
    
    .feature-title {
        font-size: 19px;
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        font-size: 13.5px;
        color: #8b949e;
        line-height: 1.5;
    }

    /* ─── SCROLLABLE PRODUCT DEEP-DIVE SECTIONS ─── */
    .product-details-container {
        max-width: 1200px;
        width: 100%;
        margin-top: 40px;
        display: flex;
        flex-direction: column;
        gap: 80px;
        padding-bottom: 100px;
    }

    .detail-row {
        display: flex;
        align-items: center;
        gap: 50px;
        width: 100%;
        text-align: left;
    }

    .detail-row.reverse {
        flex-direction: row-reverse;
    }

    .text-block {
        flex: 1;
    }

    .text-block h2 {
        font-size: 36px;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 15px;
        background: linear-gradient(90deg, #ffffff, #9ca3af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .text-block p {
        font-size: 16px;
        color: #8b949e;
        line-height: 1.6;
    }

    .image-placeholder-slot {
        flex: 1;
        height: 320px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
        border: 2px dashed rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #4f46e5;
        font-weight: 500;
        font-size: 14px;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    .image-placeholder-slot:hover {
        border-color: rgba(168, 85, 247, 0.5);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%);
    }
    
    /* ─── STYLED LOGIN BUTTON ─── */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff !important;
        font-size: 20px;
        font-weight: 600;
        padding: 16px 75px;
        border-radius: 35px; 
        border: none;
        box-shadow: 0 4px 25px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #5850ec 0%, #8c46ff 100%);
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.6);
        color: white !important;
    }
    
    /* ─── TIKTOK FEED POST UI ─── */
    .tiktok-card {
        background: #111622;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 16px;
        padding: 0px;
        margin-bottom: 25px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .tiktok-meta {
        padding: 20px;
    }
    
    .tiktok-badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }

    /* ─── VIDEO SIZE CONSTRAINTS OVERRIDE ─── */
    div[data-testid="stVideo"], .stVideo {
        max-width: 440px !important;
        margin: 15px auto !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INITIALIZATION ───
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "active_company_drawer" not in st.session_state:
    st.session_state.active_company_drawer = None
if "selected_marketplace_course" not in st.session_state:
    st.session_state.selected_marketplace_course = "All"

# ==============================================================================
# 🚪 PHASE 1: SCROLLABLE LANDING INTERFACE
# ==============================================================================
if not st.session_state.logged_in:
    
    landing_html = """
    <div class="landing-center-box">
        <div class="hero-glass-panel">
            <h1 class="landing-title">CariKerja.com</h1>
            <p class="landing-subtitle">Networking. Career Projection. Job Finding. All in one app.</p>
            <div class="features-tray">
                <div class="feature-card">
                    <div class="feature-title">User Guide</div>
                    <div class="feature-desc">You are currently on our landing page. To access the actual content of our brainchild, scroll down to login. Once in, allow the UI/UX to guide your journey into our project!
                    P/S Best viewed on desktops (for now).</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">About our Team</div>
                    <div class="feature-desc">Consisting of 1st Year students from Universiti Teknologi PETRONAS, we have developed this project based on our own woes when discussing our future as seeking-to-be-employed post-graduates; all the while being in-line with what we believe CareerOS is about.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title" style="margin-top: 0px;">Thank you for visiting our project!</div>
                    <div class="feature-desc">We hope you enjoy your stay here, and get some beneficial input from us as university students from this project.</div>
                </div>
                <div class="feature-card" style="padding: 0px; overflow: hidden; display: flex; align-items: center; justify-content: center; background: rgba(10, 14, 23, 0.3) !important; border: 1px solid rgba(99, 102, 241, 0.2) !important;">
                    <img src="https://via.placeholder.com/400x500" alt="Team Photo" style="width: 100%; height: 100%; object-fit: cover;">
                    <div class="feature-subtitle-tag" style="font-size: 11px; color: #818cf8; margin-bottom: 4px;">From the left; Umar, Aiman, Imran, Ariq (Aca).</div>
                </div>
            </div>
        </div>

        <div class="product-details-container">
            <div class="detail-row">
                <div class="text-block">
                    <h2>01. Dynamic Trajectory Modeling</h2>
                    <p>Stop looking at flat resumes. Career OS renders professional development as a continuous mathematical landscape. Adjust your domain shape vectors over a 40-year horizon to instantly predict long-term growth vectors, senior leadership plateaus, and sector valleys before making critical career moves.</p>
                </div>
                <div class="image-placeholder-slot">
                    [ 📸 Insert Topology Graph Screenshot Here ]
                </div>
            </div>

            <div class="detail-row reverse">
                <div class="text-block">
                    <h2>02. Background-Running System: Self-updating CV</h2>
                    <p>Long are the days of having to manually update your portfolio! Our system securely integrates with your day-to-day work systems; (be it GitHub, workspace environments, and university modules) that gets parsed as variables into our complex equations. Te result? A constantly updating ready-to-use CV that translates real project accomplishments into objective, verified skill metrics.</p>
                </div>
                <div class="image-placeholder-slot">
                    [ 📸 Insert Living Portfolio Dashboard Image Here ]
                </div>
            </div>

            <div class="detail-row">
                <div class="text-block">
                    <h2>03. "Fair Pay Engine": Is your salary right for you?</h2>
                    <p>Picture this; you accept a posting at a company that offers you X amount starting salary. Later, you end up discovering that X amount is lower than industry standards for the same jobscope. Our "Fair Pay Engine" maps real-time distributed salary benchmarks along your personalized trajectory arc, allowing you to make the right decision, before it becomes too late.</p>
                </div>
                <div class="image-placeholder-slot">
                    [ 📸 Insert Fair Pay Interface Screenshot Here ]
                </div>
            </div>
        </div>
    </div>
    """
    st.html(landing_html)
    
    left_space, center_button_col, right_space = st.columns([2, 1, 2])
    with center_button_col:
        if st.button("Login to Workspace", key="landing_login_btn"):
            st.session_state.logged_in = True
            st.rerun()

# ==============================================================================
# 🌐 PHASE 2: MAIN WORKSPACE ECOSYSTEM (LOADS AFTER LOGIN)
# ==============================================================================
else:
    # Global Sidebar Sliders configuration
    st.sidebar.header("Candidate Shape Vector Configuration")
    k_kinetics = st.sidebar.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8)
    k_math = st.sidebar.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5)
    k_cfd = st.sidebar.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3)
    
    st.sidebar.divider()
    st.sidebar.info("**Note:** Changing the CFD slider instantly lifts the high-yield EV valley on the map (basis on FSUTP)")

    if st.sidebar.button("Log Out Workspace", key="logout_system_btn"):
        st.session_state.logged_in = False
        st.rerun()

    # Shared Mathematics Engine setup
    x_time = np.linspace(0, 40, 50)
    path_a_y = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))
    path_b_y = 1 + (x_time * (k_math * 0.4))
    path_c_y = 1.5 + (-2 * np.exp(-((x_time - 3)**2) / 4)) + (x_time * (k_cfd * 0.55))

    # Master Datastore for listings
    internships_db = [
        {"company": "PETRONAS Carigali", "role": "Downstream Process Operations Intern", "course": "Chemical Engineering", "duration": "8 Months (May - Dec)", "scope": "Assist in daily monitoring of multi-phase separator constraints. Conduct molar mass balances and evaluate catalyst deactivation profiles.", "impact": "➕ Lifts [Path A] Reactor Kinetics by +0.3"},
        {"company": "Proton R&D (NxGV Division)", "role": "Battery Thermal Management Simulation Trainee", "course": "Mechanical / Chemical Engineering", "duration": "6 Months (June - Nov)", "scope": "Develop transient thermal fluid simulations for liquid-cooled lithium-ion battery packs. Conduct geometric grid meshing and execute thermal FMEA matrix tracking.", "impact": "➕ Lifts [Path C] CFD & Thermal Management by +0.4"},
        {"company": "AspenTech Systems", "role": "Process Digital Twin Engineer Intern", "course": "Chemical / Software Engineering", "duration": "6 Months (Jan - June)", "scope": "Formulate dynamic numerical simulation models for distillation columns using custom Runge-Kutta convergence blocks.", "impact": "➕ Lifts [Path B] Numerical Methods by +0.35"},
        {"company": "Intel Malaysia", "role": "Substrate Thermal Dissipation Intern", "course": "Mechanical / Electrical Engineering", "duration": "4 Months (May - Aug)", "scope": "Analyze micro-component convective heat fluxes on advanced silicon substrates. Run localized FEA and testing arrays.", "impact": "➕ Lifts [Path C] CFD & Thermal Management by +0.2"}
    ]

    # Global Navigation Tabs Architecture
    app_tabs = st.tabs([
        "📱 Discover Feed", 
        "📊 Universal Career Graph",
        "⚖️ Fair Pay Engine",
        "💼 Placements Marketplace", 
        "💬 Communications Network"
    ])

    # 📥 TAB 1: SHORT FORM VIDEO DISCOVER FEED (TIKTOK STYLE)
    with app_tabs[0]:
        st.title("Discover Ecosystem")
        st.caption("Verifiable authentic workflows streamed directly by peer talents and corporate engineering leads.")
        
        feed_col, drawer_col = st.columns([2, 1])

        with feed_col:
            # 🎥 Post Vector 1: Proton NxGV Lead
            st.markdown('<div class="tiktok-card">', unsafe_allow_html=True)
            
            raw_github_video_url = "https://raw.githubusercontent.com/ashminggu/careeros_migger_utp/main/WhatsApp%20Video%202026-06-10%20at%2022.24.44.mp4"
            st.video(raw_github_video_url, format="video/mp4", start_time=0)

            st.markdown('<div class="tiktok-meta">', unsafe_allow_html=True)
            st.markdown('<span class="tiktok-badge">🔥 Corporate Engineering Update</span>', unsafe_allow_html=True)
            st.markdown('<h4>"Why mechanical grid meshing limits transient cooling iterations in hybrid powertrains."</h4>', unsafe_allow_html=True)
            st.markdown('<p style="color:#8b949e; font-size:14px;">Published by: Proton R&D (NxGV Division)</p>', unsafe_allow_html=True)
            if st.button("Inspect Corporate Profile & Deploy Roles", key="feed_btn_proton"):
                st.session_state.active_company_drawer = "Proton R&D (NxGV Division)"
            st.markdown('</div></div>', unsafe_allow_html=True)

            # 🎥 Post Vector 2: PETRONAS Carigali Asset Lead
            st.markdown('<div class="tiktok-card">', unsafe_allow_html=True)
            
            st.video(raw_github_video_url, format="video/mp4", start_time=0)

            st.markdown('<div class="tiktok-meta">', unsafe_allow_html=True)
            st.markdown('<span class="tiktok-badge">⚡ Asset Performance Deployment</span>', unsafe_allow_html=True)
            st.markdown('<h4>"Balancing downstream separator constraint margins during unexpected catalyst deactivation cycles."</h4>', unsafe_allow_html=True)
            st.markdown('<p style="color:#8b949e; font-size:14px;">Published by: PETRONAS Carigali</p>', unsafe_allow_html=True)
            if st.button("Inspect Corporate Profile & Deploy Roles", key="feed_btn_petronas"):
                st.session_state.active_company_drawer = "PETRONAS Carigali"
            st.markdown('</div></div>', unsafe_allow_html=True)

        with drawer_col:
            st.markdown("### 🏢 Profile Deep-Dive Drawer")
            if st.session_state.active_company_drawer:
                target_comp = st.session_state.active_company_drawer
                st.success(f"Focused System View: **{target_comp}**")
                st.markdown(f"**Verified Open Trajectory Alignments for {target_comp}:**")
                
                matched_roles = [j for j in internships_db if j["company"] == target_comp]
                for mr in matched_roles:
                    st.markdown(f"**Role:** {mr['role']}")
                    st.caption(f"Requires: {mr['course']} | Vector: {mr['impact']}")
                    if st.button("Instant Apply to Target Pathway", key=f"drawer_apply_{mr['role']}"):
                        st.toast(f"Application safely queued into {target_comp}'s recruitment matrix!")
            else:
                st.info("Click 'Inspect Corporate Profile' on any scrolling video inside your discovery timeline to auto-extract their open operational tracks and metrics here.")

    # 📊 TAB 2: ORIGINAL FULL-PAGE UNIVERSAL CAREER GRAPH
    with app_tabs[1]:
        st.title("Career OS: Path Navigation Engine")
        
        view_mode = st.radio(
            "Select Visualization Framework Layout:",
            ["3D Topography Surface Map", "2D Continuous Line Graph View"],
            horizontal=True,
            key="universal_graph_toggle"
        )
        st.subheader("Visualizing the 40-Year Career Horizon with Data-Driven Geometry")
        
        # ─── CONDITION A: RENDER ORIGINAL 3D TOPOGRAPHY ───
        if view_mode == "3D Topography Surface Map":
            y_paths = np.array([1, 2, 3])
            X, Y = np.meshgrid(x_time, y_paths)
            Z = np.zeros_like(X)
            Z[0, :] = path_a_y
            Z[1, :] = path_b_y
            Z[2, :] = path_c_y

            fig = go.Figure(data=[go.Surface(
                x=X, y=Y, z=Z, colorscale='Viridis',
                lighting=dict(ambient=0.6, roughness=0.4),
                colorbar=dict(title="Z: Market Yield")
            )])

            fig.update_layout(
                scene=dict(
                    xaxis=dict(title='X: Horizon (Years)', range=[0, 40], gridcolor='#23282f'),
                    yaxis=dict(
                        title='Y: Trajectory Choice',
                        tickvals=[1, 2, 3],
                        ticktext=['Path A: Downstream', 'Path B: Numerical', 'Path C: CFD/Thermal'],
                        gridcolor='#23282f'
                    ),
                    zaxis=dict(title='Z: Career Yield', range=[-1, 20], gridcolor='#23282f'),
                    camera=dict(eye=dict(x=1.8, y=-1.8, z=1.2))
                ),
                margin=dict(l=0, r=0, b=0, t=40), height=650,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )

        # ─── CONDITION B: RENDER CLEAN 2D MULTI-LINE VIEW ───
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_time, y=path_a_y, mode='lines', name='Path A: Downstream Operations', line=dict(color='#818cf8', width=4)))
            fig.add_trace(go.Scatter(x=x_time, y=path_b_y, mode='lines', name='Path B: Numerical Simulation', line=dict(color='#c084fc', width=4)))
            fig.add_trace(go.Scatter(x=x_time, y=path_c_y, mode='lines', name='Path C: CFD & Thermal Management', line=dict(color='#f472b6', width=4)))

            fig.update_layout(
                xaxis=dict(title='X: Time / Career Horizon (Years)', range=[0, 40], gridcolor='#23282f', zeroline=False),
                yaxis=dict(title='Y: Career Viability & Yield Metric', range=[-1, 20], gridcolor='#23282f', zeroline=False),
                margin=dict(l=40, r=40, b=40, t=40), height=550,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color="#f0f6fc"), bgcolor="rgba(10,14,23,0.6)", bordercolor="rgba(99,102,241,0.15)", borderwidth=1)
            )
        
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

    # ⚖️ TAB 3: SALARY SPECIFIC GRAPH (FAIR PAY ENGINE)
    with app_tabs[2]:
        st.title("⚖️ Fair Pay Engine: Compensation Trajectory Mapping")
        st.subheader("Combating Information Asymmetry via Distributed Peer Market Quartiles")
        st.caption("This full-page projection charts distributed compensation bands over a 25-year tracking horizon based on active shape metrics.")
        
        salary_fig = go.Figure()
        salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y[:35]*1600, mode='lines', name='Upper Quartile (Top Tier Tier-1 Multinationals)', line=dict(dash='dash', color='#00FF00', width=3)))
        salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y[:35]*1100, mode='lines', name='Median Peer Benchmark Industry Standard', line=dict(color='#818cf8', width=4)))
        salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y[:35]*750, mode='lines', name='Lower Quartile Base Pay Margin', line=dict(color='#FF3333', width=3)))

        salary_fig.update_layout(
            xaxis=dict(title='Career Timeline Horizon (Years)', gridcolor='#23282f'),
            yaxis=dict(title='Estimated Monthly Yield Vector (RM / Local Adjusted)', gridcolor='#23282f'),
            height=550,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color="#f0f6fc"), bgcolor="rgba(10,14,23,0.6)")
        )
        
        s_col1, s_col2 = st.columns([3, 1])
        with s_col1:
            st.plotly_chart(salary_fig, use_container_width=True)
        with s_col2:
            st.markdown("### 🔍 Pay Shadow Audit")
            st.warning("⚠️ **Asymmetry Detected:** Based on default regional baseline weights, entry-level downstream process operations roles reflect a -15% visual trajectory pay shadow compared to advanced computation fields.")
            st.info("💡 **Vector Remedy:** Increasing your [Path B] Numerical Simulation profile tracking slider lifts your early career salary anchor line away from the lower quartile valley boundary.")

    # 💼 TAB 4: PLACEMENTS PLUGINS MARKETPLACE
    with app_tabs[3]:
        st.title("💼 Live Placements & Trajectory Hub")
        st.write("Anti-spam job deployment tunnels mapping real-time professional actions to your specific profile dimension nodes.")
        
        course_options = ["All", "Chemical Engineering", "Mechanical / Chemical Engineering", "Chemical / Software Engineering", "Mechanical / Electrical Engineering"]
        st.session_state.selected_marketplace_course = st.selectbox(
            "Filter Listings by Domain Discipline Parameters:", 
            course_options, 
            index=course_options.index(st.session_state.selected_marketplace_course)
        )
        st.divider()

        for job in internships_db:
            if st.session_state.selected_marketplace_course == "All" or job["course"] == st.session_state.selected_marketplace_course:
                with st.expander(f"🏢 {job['company']} ── {job['role']}"):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.markdown(f"**Target Discipline:** `{job['course']}` | **Duration:** {job['duration']}")
                        st.markdown("**Core Job Scope & Responsibilities:**")
                        st.write(job["scope"])
                    with c2:
                        st.info(f"🏆 **Trajectory Vector Impact:**\n\n{job['impact']}")
                        if st.button("Deploy Application Stack", key=f"market_btn_{job['company']}_{job['role']}"):
                            st.success(f"Application securely deployed to {job['company']} recruitment dashboard!")

    # ─── TAB 5: COMMUNICATIONS NETWORK ───
    with app_tabs[4]:
        st.title("💬 Career OS Communications Matrix")
        st.subheader("Real-Time Network Inbound Tracks & Verification Logs")
        
        net_col1, net_col2 = st.columns([1, 2])
        
        with net_col1:
            st.markdown("### 📭 Channels")
            ch_select = st.radio("Select Thread:", [
                "📬 PETRONAS Talent Acquisition (Inbound System Trigger)", 
                "⚡ Proton NxGV Engineering Group (Follow-up)", 
                "🤝 Safaruddin Raja Ghopal (Acquaintance Peer)"
            ])
        
        with net_col2:
            st.markdown("### 💬 Conversational Wire")
            if "PETRONAS" in ch_select:
                st.markdown("**From: PETRONAS Carigali HR**")
                st.info("『System Alert Match』 Our background semantic parser identified your high downstream vector profile from your university performance module logs. We would love to evaluate your fit for our 8-month Downstream Separator optimization block.")
                st.text_input("Send encrypted corporate transmission response...", key="msg_petronas")
            elif "Proton" in ch_select:
                st.markdown("**From: Proton NxGV Lead Technical Architect**")
                st.warning("Hey candidate, caught your workflow screen-capture video regarding transient thermal dissipation modeling on the system discovery index. Impressive mesh adjustment parameters. Let's schedule a technical panel.")
                st.text_input("Send response to tech architect...", key="msg_proton")
            else:
                st.markdown("**From: Safaruddin Raja Ghopal**")
                st.markdown("*Bro, look at the Fair Pay shadow chart metric. I just verified my engineering logs, and our university project parameters shifted my median track up instantly. Let me know if you want to look over my dashboard code.*")
                st.text_input("Send message to Safaruddin...", key="msg_peer")

    # ─── GLOBAL CHAT INPUT PROCESSING & AI INTEGRATION ───
    st.divider()
    st.subheader("🤖 Career OS: AIMAN.AI Navigation Copilot")
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            avatar_img = "aimanai.jpeg" if message["role"] == "assistant" else "user"
            with st.chat_message(message["role"], avatar=avatar_img):
                st.markdown(message["content"])

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    if user_query := st.chat_input("Ask about structural layout adjustments, pay shadows, or path blockages..."):
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_query)
                
        st.session_state.messages.append({"role": "user", "content": user_query})

        system_instruction = f"""
        You are AIMAN.AI, the Career OS Honest Navigation Copilot. You act as a supportive, grounded, and radically candid mentor for a Chemical Engineering student.
        Your tone is empathetic but highly direct—like a helpful peer, not a rigid lecturer. Avoid corporate fluff; speak with data-driven honesty.
        
        The user is navigating an ecosystem with distinct tabs for short form discover feeds, a full 3D growth topography page, and a full fair pay engine layout:
        - Reactor Kinetics Mastery (Path A Core): {k_kinetics}/1.0
        - Numerical Methods Vector (Path B Core): {k_math}/1.0
        - CFD & Thermal Management Vector (Path C Core): {k_cfd}/1.0
        """

        formatted_contents = []
        for msg in st.session_state.messages[:-1]:
            formatted_contents.append(f"{msg['role'].upper()}: {msg['content']}")
        formatted_contents.append(f"USER: {user_query}")
        
        with chat_container:
            with st.chat_message("assistant", avatar="aimanai.jpeg"):
                response_placeholder = st.empty()
                response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=formatted_contents, config={"system_instruction": system_instruction}
                )
                ai_text = response.text
                response_placeholder.markdown(ai_text)
                
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        st.rerun()
