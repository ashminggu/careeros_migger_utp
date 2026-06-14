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

# ─── ADVANCED FIGMA-STYLE CSS UI OVERRIDES (CREAM & FOREST GREEN) ───
st.markdown("""
    <style>
    /* Global Background - Premium Editorial Cream */
    .stApp {
        background-color: #fcfbf7;
        background-image: 
            linear-gradient(rgba(44, 74, 53, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(44, 74, 53, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #111111 !important;
    }
    
    .block-container {
        max-width: 1300px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: 0 auto !important;
    }
    
    /* UNIVERSAL CONTRAST FORCE - Fixes blending text across ALL components */
    .stApp, p, span, label, li, div, [data-testid="stMarkdownContainer"] p {
        color: #222222 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Typography Headings Force Overrides */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
        color: #1b3b22 !important; /* Deep Forest Green */
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
    }
    
    /* Widget Input Labels, Slider Titles, Selectbox Text Contrast Fix */
    .stSlider label, .stSelectbox label, .stRadio label, .stTextInput label, [data-testid="stWidgetLabel"] p {
        color: #1b3b22 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Expander styling tweaks */
    .data-testid="stExpander" p, .stExpander details summary {
        color: #1b3b22 !important;
    }
    
    /* Native App Bar Branding Header */
    .brand-header-bar {
        width: 100%;
        padding: 15px 0px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e6e4dc;
    }
    .brand-header-title {
        font-size: 32px;
        font-weight: 800;
        color: #1b3b22 !important;
        letter-spacing: -1px;
    }
    
    /* Outer layout positioning frame - CENTERED FOR LANDING */
    .landing-center-box {
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding-top: 2%;
        text-align: center;
    }

    /* ─── HERO CANVAS PANEL ─── */
    .hero-glass-panel {
        background: #ffffff;
        border: 1px solid #e1ded7;
        border-radius: 24px;
        padding: 50px 40px;
        width: 100%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 15px 40px rgba(44, 74, 53, 0.04);
    }
    
    .landing-title {
        font-size: 80px;
        font-weight: 900;
        letter-spacing: -2px;
        line-height: 1.1;
        color: #1b3b22 !important;
        margin-bottom: 15px;
    }
    
    .landing-subtitle {
        font-size: 22px;
        color: #555555 !important;
        margin-bottom: 40px;
        font-weight: 400;
        max-width: 700px;
        line-height: 1.5;
    }
    
    /* ─── FEATURE TRAY & BOXES ─── */
    .features-tray {
        display: flex;
        gap: 20px;
        justify-content: center;
        width: 100%;
        align-items: stretch;
    }
    
    .feature-card {
        background: #ffffff !important;
        border: 1px solid #e6e4dc !important;
        border-radius: 16px;
        padding: 24px;
        flex: 1;
        text-align: left;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 12px rgba(44, 74, 53, 0.02);
    }
    
    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #1b3b22 !important;
        margin-bottom: 12px;
        border-bottom: 1px solid #e6e4dc;
        padding-bottom: 6px;
    }
    
    .feature-desc {
        font-size: 13.5px;
        color: #222222 !important; 
        line-height: 1.6;
        font-weight: 400 !important;
    }

    /* ─── PRODUCT DEEP DIVE ARTIFACTS ─── */
    .product-details-container {
        width: 100%;
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        gap: 60px;
        padding-bottom: 80px;
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
        font-size: 32px;
        font-weight: 700;
        color: #1b3b22 !important;
        margin-bottom: 15px;
    }

    .text-block p {
        font-size: 15px;
        color: #444444 !important;
        line-height: 1.6;
    }

    .image-placeholder-slot {
        flex: 1;
        height: 300px;
        background: #f4f3ec;
        border: 1px solid #e1ded7;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2c4a35;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* ─── HIGH CONTRAST BUTTONS ─── */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    div.stButton > button:first-child {
        background: #1b3b22 !important;
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 600;
        padding: 12px 60px;
        border-radius: 30px; 
        border: 1px solid #142c19;
        box-shadow: 0 4px 15px rgba(27, 59, 34, 0.15);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background: #255230 !important;
        transform: translateY(-1px);
        color: #ffffff !important;
    }
    
    .stSidebar div.stButton > button:first-child {
        background: #cbd5e1 !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1;
        font-size: 14px;
        padding: 8px 20px;
        border-radius: 6px;
    }
    
    /* ─── MAIN APP WORKSPACE FEED OVERRIDES (FIXED REELS MOCKUP) ─── */
    .tiktok-card {
        background: #ffffff;
        border: 1px solid #e6e4dc;
        border-radius: 20px;
        padding: 0px;
        margin: 0 auto 30px auto;
        max-width: 350px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(44,74,53,0.05);
    }
    
    .video-overlay-wrapper {
        position: relative;
        width: 100%;
        height: 520px;
        background-color: #000000;
    }
    
    .immersive-html5-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .video-action-overlay {
        position: absolute;
        right: 14px;
        bottom: 30px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        z-index: 999;
        align-items: center;
        text-align: center;
    }
    
    .overlay-action-btn {
        background: rgba(27, 59, 34, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        width: 44px;
        height: 44px;
        border-radius: 50% !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .overlay-action-btn:hover {
        transform: scale(1.15);
        background: #1b3b22 !important;
    }
    
    .overlay-action-counter {
        font-size: 11px;
        color: #ffffff !important;
        font-weight: 700;
        margin-top: -4px;
        margin-bottom: 4px;
        text-shadow: 0 2px 6px rgba(0,0,0,0.9);
        font-family: 'Inter', sans-serif;
    }
    
    .tiktok-meta {
        padding: 20px;
        background: #ffffff;
        border-top: 1px solid #f4f3ec;
    }
    
    .tiktok-badge {
        background: rgba(44, 74, 53, 0.08);
        color: #1b3b22 !important;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #666666 !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #1b3b22 !important;
        font-weight: 700 !important;
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

# Initialize local variable states safely
k_kinetics, k_math, k_cfd = 0.8, 0.5, 0.3

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
                <div class="feature-desc">You are currently on our landing page. To access the actual content of our brainchild, scroll down to login. Once in, allow the UI/UX to guide your journey into our project!<br><br>P/S Best viewed on desktops (for now).</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">About our Team</div>
                <div class="feature-desc">Consisting of 1st Year students from Universiti Teknologi PETRONAS, we have developed this project based on our own woes when discussing our future as seeking-to-be-employed post-graduates; all the while being in-line with what we believe CareerOS is about.</div>
            </div>
            <div class="feature-card" style="display: flex; flex-direction: column; justify-content: flex-start;">
                <div class="feature-title" style="margin-top: 0px;">Thank you for visiting our project!</div>
                <div class="feature-desc">We hope you enjoy your stay here, and get some beneficial input from us as university students from this project.</div>
            </div>
            <div class="feature-card" style="padding: 0px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; background: #ffffff !important; border: 1px solid #e6e4dc !important;">
                <div style="width: 100%; flex-grow: 1; overflow: hidden; display: flex; align-items: center; justify-content: center; min-height:160px;">
                    <img src="https://raw.githubusercontent.com/ashminggu/careeros_migger_utp/main/teambro.png" alt="Team Photo" style="width: 100%; height: 100%; object-fit: cover; object-position: center 20%;">
                </div>
                <div class="feature-subtitle-tag" style="font-size: 11px; color: #2c4a35; margin-bottom: 6px; text-transform: uppercase; font-weight:700;">From the left; Ariq (ACA), Aiman, Imran, Umar.</div>
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
                <p>Long are the days of having to manually update your portfolio! Our system securely integrates with your day-to-day work systems; (be it GitHub, workspace environments, and university modules) that gets parsed as variables into our complex equations. The result? A constantly updating ready-to-use CV that translates real project accomplishments into objective, verified skill metrics.</p>
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
    # ─── BRAND HEADER NAVIGATION BAR ───
    st.markdown("""
<div class="brand-header-bar">
    <span class="brand-header-title">CariKerja</span>
    <span style="color: #666666; font-size: 14px; margin-left: 15px; font-family: sans-serif;">| Executive Workspace Ecosystem</span>
</div>
""", unsafe_allow_html=True)

    if st.sidebar.button("Log Out Workspace", key="logout_system_btn"):
        st.session_state.logged_in = False
        st.rerun()

    # Shared Mathematics Base Horizontal Tracking Array
    x_time = np.linspace(0, 40, 50)

    # Master Datastore for openings
    internships_db = [
        {"company": "PETRONAS Carigali", "role": "Downstream Process Operations Intern", "course": "Chemical Engineering", "duration": "8 Months (May - Dec)", "scope": "Assist in daily monitoring of multi-phase separator constraints. Conduct molar mass balances and evaluate catalyst deactivation profiles.", "impact": "➕ Lifts [Path A] Reactor Kinetics by +0.3"},
        {"company": "Proton R&D (NxGV Division)", "role": "Battery Thermal Management Simulation Trainee", "course": "Mechanical / Chemical Engineering", "duration": "6 Months (June - Nov)", "scope": "Develop transient thermal fluid simulations for liquid-cooled lithium-ion battery packs. Conduct geometric grid meshing and execute thermal FMEA matrix tracking.", "impact": "➕ Lifts [Path C] CFD & Thermal Management by +0.4"},
        {"company": "AspenTech Systems", "role": "Process Digital Twin Engineer Intern", "course": "Chemical / Software Engineering", "duration": "6 Months (Jan - June)", "scope": "Formulate dynamic numerical simulation models for distillation columns using custom Runge-Kutta convergence blocks.", "impact": "➕ Lifts [Path B] Numerical Methods by +0.35"},
        {"company": "Intel Malaysia", "role": "Substrate Thermal Dissipation Intern", "course": "Mechanical / Electrical Engineering", "duration": "4 Months (May - Aug)", "scope": "Analyze micro-component convective heat fluxes on advanced silicon substrates. Run localized FEA and testing arrays.", "impact": "➕ Lifts [Path C] CFD & Thermal Management by +0.2"}
    ]

    # Global Navigation Tabs Architecture
    app_tabs = st.tabs([
        "📱 FYP Feed", 
        "📊 Universal 3D/2D Career Graph",
        "⚖️ Fair Pay Engine",
        "💼 Intern/Job Marketplace", 
        "💬 Messages"
    ])

    # 📥 TAB 1: SHORT FORM VIDEO DISCOVER FEED
    with app_tabs[0]:
        st.title("For You Page")
        st.caption("Verifiable authentic workflows streamed directly by peer talents and corporate engineering leads.")
        
        feed_col, drawer_col = st.columns([1.8, 1.2])

        with feed_col:
            raw_github_video_url = "https://raw.githubusercontent.com/ashminggu/careeros_migger_utp/main/WhatsApp%20Video%202026-06-10%20at%2022.24.44.mp4"

            # 🎥 Post Vector 1: Proton NxGV Lead
            st.markdown(f"""
<div class="tiktok-card">
    <div class="video-overlay-wrapper">
        <div class="video-action-overlay">
            <div class="overlay-action-btn">❤️</div>
            <div class="overlay-action-counter">14.2k</div>
            <div class="overlay-action-btn">💬</div>
            <div class="overlay-action-counter">382</div>
            <div class="overlay-action-btn">🔖</div>
            <div class="overlay-action-counter">1.8k</div>
            <div class="overlay-action-btn">↩️</div>
            <div class="overlay-action-counter">Share</div>
        </div>
        <video class="immersive-html5-video" controls autoplay muted loop playsinline>
            <source src="{raw_github_video_url}" type="video/mp4">
        </video>
    </div>
    <div class="tiktok-meta">
        <span class="tiktok-badge">🔥 Corporate Engineering Update</span>
        <h4 style="margin-top:0px; line-height:1.3; font-size:16px; color:#1b3b22 !important;">"Why mechanical grid meshing limits transient cooling iterations in hybrid powertrains."</h4>
        <p style="color:#555555; font-size:13px; margin-bottom:15px;">Published by: Proton R&D (NxGV Division)</p>
    </div>
</div>
""", unsafe_allow_html=True)
            
            if st.button("Inspect Corporate Profile & Deploy Roles", key="feed_btn_proton"):
                st.session_state.active_company_drawer = "Proton R&D (NxGV Division)"

            st.markdown("<br><br>", unsafe_allow_html=True)

            # 🎥 Post Vector 2: PETRONAS Carigali Asset Lead
            st.markdown(f"""
<div class="tiktok-card">
    <div class="video-overlay-wrapper">
        <div class="video-action-overlay">
            <div class="overlay-action-btn">❤️</div>
            <div class="overlay-action-counter">9.8k</div>
            <div class="overlay-action-btn">💬</div>
            <div class="overlay-action-counter">214</div>
            <div class="overlay-action-btn">🔖</div>
            <div class="overlay-action-counter">943</div>
            <div class="overlay-action-btn">↩️</div>
            <div class="overlay-action-counter">Share</div>
        </div>
        <video class="immersive-html5-video" controls muted loop playsinline>
            <source src="{raw_github_video_url}" type="video/mp4">
        </video>
    </div>
    <div class="tiktok-meta">
        <span class="tiktok-badge">⚡ Asset Performance Deployment</span>
        <h4 style="margin-top:0px; line-height:1.3; font-size:16px; color:#1b3b22 !important;">"Balancing downstream separator constraint margins during unexpected catalyst deactivation cycles."</h4>
        <p style="color:#555555; font-size:13px; margin-bottom:15px;">Published by: PETRONAS Carigali</p>
    </div>
</div>
""", unsafe_allow_html=True)
            
            if st.button("Inspect Corporate Profile & Deploy Roles", key="feed_btn_petronas"):
                st.session_state.active_company_drawer = "PETRONAS Carigali"

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

    # 📊 TAB 2: UNIVERSAL CAREER GRAPH
    with app_tabs[1]:
        st.title("CariKerja.com: Path Navigation Engine")
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("###Candidate Shape Vector")
            st.write("Adjust parameters to watch the topology surface change:")
            k_kinetics = st.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8, key="graph_sl_k")
            k_math = st.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5, key="graph_sl_m")
            k_cfd = st.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3, key="graph_sl_c")
            st.divider()
            if k_cfd > 0.7:
                st.success("🎯 **Optimal Pathway:** Your high CFD vector has successfully flattened the early friction valley in the EV Automotive sector.")
            else:
                st.warning("""⚠️ **Developer note:** These sliders are here for the sake of observing how the graph will change over the course of the 40 year career with different input values. The actual concept here would be that the
                system will be connected to the user's profile in which it will take into account two main categories of data: 1) details and preferences of the user themselves including the user's current skillset and capabilities (ability to use CAD software, do CFD analysis, etc.), salary over career growth preference (assigned weightage), 
                and 2) the current and projected growth of the specialization pathway for the career. All of these data will be assigned as a variable which will be added into an equation which plots the graph. A higher Z value indicates a better
                'score' for the path. Weightages are applied to each variable depending on the preference of the user (for preference-based variables).""")

        path_a_y = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))
        path_b_y = 1 + (x_time * (k_math * 0.4))
        path_c_y = 1.5 + (-2 * np.exp(-((x_time - 3)**2) / 4)) + (x_time * (k_cfd * 0.55))

        with col1:
            view_mode = st.radio(
                "Select Visualization Framework Layout:",
                ["3D Topography Surface Map", "2D Continuous Line Graph View"],
                horizontal=True,
                key="universal_graph_toggle"
            )
            
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
                    colorbar=dict(title=dict(text="Z: Career Yield", font=dict(color="#1b3b22")))
                )])
                
                fig.update_layout(
                    scene=dict(
                        xaxis=dict(title='X: Horizon (Years)', range=[0, 40], gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                        yaxis=dict(title='Y: Trajectory Choice', tickvals=[1, 2, 3], ticktext=['Path A', 'Path B', 'Path C'], gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                        zaxis=dict(title='Z: Career Yield', range=[-1, 20], gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222'))
                    ),
                    margin=dict(l=0, r=0, b=0, t=40), height=550,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
            else:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_time, y=path_a_y, mode='lines', name='Path A: Downstream Operations', line=dict(color='#1b3b22', width=4)))
                fig.add_trace(go.Scatter(x=x_time, y=path_b_y, mode='lines', name='Path B: Numerical Simulation', line=dict(color='#2c4a35', width=4)))
                fig.add_trace(go.Scatter(x=x_time, y=path_c_y, mode='lines', name='Path C: CFD & Thermal Management', line=dict(color='#d97706', width=4)))
                
                fig.update_layout(
                    xaxis=dict(title='X: Time / Career Horizon (Years)', range=[0, 40], gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                    yaxis=dict(title='Y: Career Viability Metric', range=[-1, 20], gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                    margin=dict(l=40, r=40, b=40, t=40), height=550,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(font=dict(color="#1b3b22"), bgcolor="rgba(255,255,255,0.8)", bordercolor="#e6e4dc", borderwidth=1)
                )
            st.plotly_chart(fig, use_container_width=True)
            
        st.divider()
        st.subheader("🤖 CariKerja: AIMAN.AI Navigation Copilot")
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                avatar_img = "aimanai.jpeg" if message["role"] == "assistant" else "user"
                with st.chat_message(message["role"], avatar=avatar_img):
                    st.markdown(f"<span style='color:#222222 !important;'>{message['content']}</span>", unsafe_allow_html=True)

        api_token = st.secrets.get("GEMINI_API_KEY", "MOCK_KEY_FALLBACK_VAL")
        client = genai.Client(api_key=api_token)

        if user_query := st.chat_input("Ask about structural layout adjustments, pay shadows, or path blockages..."):
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_query)
                    
            st.session_state.messages.append({"role": "user", "content": user_query})

            system_instruction = f"""
            You are AIMAN.AI, the Career OS Honest Navigation Copilot. You act as a supportive, grounded, and radically candid mentor for a Chemical Engineering student.
            Your tone is empathetic but highly direct—like a helpful peer, not a rigid lecturer. Avoid corporate fluff; speak with data-driven honesty.
            """

            formatted_contents = [f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages[:-1]]
            formatted_contents.append(f"USER: {user_query}")
            
            with chat_container:
                with st.chat_message("assistant", avatar="aimanai.jpeg"):
                    response_placeholder = st.empty()
                    if api_token == "MOCK_KEY_FALLBACK_VAL":
                        ai_text = "⚠️ **System Alert:** `GEMINI_API_KEY` is currently missing from your Streamlit Secrets environment."
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash', contents=formatted_contents, config={"system_instruction": system_instruction}
                        )
                        ai_text = response.text
                    response_placeholder.markdown(ai_text)
                    
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            st.rerun()

    # ⚖️ TAB 3: FAIR PAY ENGINE
    with app_tabs[2]:
        st.title("⚖️ Fair Pay Engine: Compensation Trajectory Mapping")
        s_col1, s_col2 = st.columns([3, 1])
        
        with s_col2:
            st.markdown("### 🎛️ Baseline Variable Weighting")
            st.write("Tune variables to shift target benchmarking bands:")
            k_kinetics_p = st.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8, key="pay_sl_k")
            k_math_p = st.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5, key="pay_sl_m")
            k_cfd_p = st.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3, key="pay_sl_c")
            st.divider()
            st.markdown("### 🔍 Pay Shadow Audit")
            st.warning("⚠️ **Asymmetry Detected:** Based on default regional baseline weights, entry-level downstream process operations roles reflect a -15% visual trajectory pay shadow compared to advanced computation fields.")

        path_a_y_p = np.where(x_time <= 6, 2 + (x_time * k_kinetics_p), 2 + (6 * k_kinetics_p))

        with s_col1:
            salary_fig = go.Figure()
            salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y_p[:35]*1600, mode='lines', name='Upper Quartile (Top Tier Multinationals)', line=dict(dash='dash', color='#16a34a', width=3)))
            salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y_p[:35]*1100, mode='lines', name='Median Peer Benchmark Industry Standard', line=dict(color='#1b3b22', width=4)))
            salary_fig.add_trace(go.Scatter(x=x_time[:35], y=path_a_y_p[:35]*750, mode='lines', name='Lower Quartile Base Pay Margin', line=dict(color='#dc2626', width=3)))

            salary_fig.update_layout(
                xaxis=dict(title='Career Timeline Horizon (Years)', gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                yaxis=dict(title='Estimated Monthly Yield Vector (RM / Local Adjusted)', gridcolor='#e6e4dc', title_font=dict(color='#1b3b22'), tickfont=dict(color='#222222')),
                height=550, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color="#1b3b22"), bgcolor="rgba(255,255,255,0.8)", bordercolor="#e6e4dc", borderwidth=1)
            )
            st.plotly_chart(salary_fig, use_container_width=True)

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
        st.title("💬 Communications Matrix")
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
                st.info("『System Alert Match』 Our background semantic parser identified your high downstream vector profile from your university performance module logs.")
                st.text_input("Send encrypted corporate transmission response...", key="msg_petronas")
            elif "Proton" in ch_select:
                st.markdown("**From: Proton NxGV Lead Technical Architect**")
                st.warning("Hey candidate, caught your workflow screen-capture video regarding transient thermal dissipation modeling on the system discovery index.")
                st.text_input("Send response to tech architect...", key="msg_proton")
            else:
                st.markdown("**From: Safaruddin Raja Ghopal**")
                st.markdown("*Bro, look at the Fair Pay shadow chart metric. Let me know if you want to look over my dashboard code.*")
                st.text_input("Send message to Safaruddin...", key="msg_peer")
