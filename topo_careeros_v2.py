import streamlit as st
import numpy as np
import plotly.graph_objects as go
from google import genai

# ─── APP CONFIGURATION ───
st.set_page_config(page_title="Career OS - Ecosystem", layout="wide")

# Initialize dialogue history session state early
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Greetings! I'm AIMAN.AI, your dynamic Career OS Copilot. I analyze your profile vector data against market realities. Which pathway's trade-offs or personal concerns would you like me to deconstruct honestly?"}
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

    /* Styled Image Placeholder Boxes */
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
        margin-top: 40px;
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
    </style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INITIALIZATION ───
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==============================================================================
# 🚪 PHASE 1: SCROLLABLE LANDING INTERFACE
# ==============================================================================
if not st.session_state.logged_in:
    
    landing_html = """
    <div class="landing-center-box">
        <div class="hero-glass-panel">
            <h1 class="landing-title">Career OS</h1>
            <p class="landing-subtitle">Your personal data-driven life-long career coach.</p>
            <div class="features-tray">
                <div class="feature-card">
                    <div class="icon-box">📊</div>
                    <div class="feature-title">Career Topology</div>
                    <div class="feature-desc">Interactive 3D mathematical terrain surfaces structural career peaks and valleys.</div>
                </div>
                <div class="feature-card">
                    <div class="icon-box">📂</div>
                    <div class="feature-title">Living Portfolio</div>
                    <div class="feature-desc">Automated system tracking that compiles verifiable workflows quietly in the background.</div>
                </div>
                <div class="feature-card">
                    <div class="icon-box">⚖️</div>
                    <div class="feature-title">Fair Pay Engine</div>
                    <div class="feature-desc">Combats asymmetry by casting direct visual shadows across underpaid peer timelines.</div>
                </div>
                <div class="feature-card">
                    <div class="icon-box">💼</div>
                    <div class="feature-title">Market Deployment</div>
                    <div class="feature-desc">Placements tied to explicit vector actions that physically alter your map variables.</div>
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
                    <h2>02. The Passive Verification Layer</h2>
                    <p>Eradicate manual resume updating and employer cynicism. Our system securely integrates with your day-to-day work systems (GitHub, workspace environments, and university modules) to parse actual code, models, and execution frameworks. It quietly translates real project accomplishments into objective, verified skill metrics.</p>
                </div>
                <div class="image-placeholder-slot">
                    [ 📸 Insert Living Portfolio Dashboard Image Here ]
                </div>
            </div>

            <div class="detail-row">
                <div class="text-block">
                    <h2>03. Data-Driven Salary Accountability</h2>
                    <p>Wage gaps thrive in information silos. The Fair Pay Engine maps real-time distributed salary benchmarks along your personalized trajectory arc. If your compensation drops behind market trends, the dashboard flags the exact financial delta and uses generative AI architectures to draft direct corporate talking points for review cycles.</p>
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
        if st.button("Login to Workspace"):
            st.session_state.logged_in = True
            st.rerun()

# ==============================================================================
# 🌐 PHASE 2: MAIN WORKSPACE ECOSYSTEM (LOADS AFTER LOGIN)
# ==============================================================================
else:
    # Sidebar Setup
    st.sidebar.header("Candidate Shape Vector")
    st.sidebar.write("Adjust skill mastery to watch the mathematical terrain morph:")

    k_kinetics = st.sidebar.slider("[PATH A] Downstream Operations: Reactor Kinetics Mastery", 0.1, 1.0, 0.8)
    k_math = st.sidebar.slider("[PATH B] Numerical Methods in ChemE", 0.1, 1.0, 0.5)
    k_cfd = st.sidebar.slider("[PATH C] CFD & Thermal Management", 0.1, 1.0, 0.3)

    st.sidebar.divider()
    if st.sidebar.button("Log Out Workspace"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2 = st.tabs(["3D Career Navigation & AIMAN.AI Copilot", "Live Internship Marketplace"])

    # TAB 1: GRAPH & CHAT RUNTIME ENVIRONMENT
    with tab1:
        st.title("Career OS: 3D Path Navigation Engine")
        
        # Mathematical Grid Topology
        x_time = np.linspace(0, 40, 50)
        y_paths = np.array([1, 2, 3])
        X, Y = np.meshgrid(x_time, y_paths)
        Z = np.zeros_like(X)

        for i in range(len(y_paths)):
            if y_paths[i] == 1:
                Z[i, :] = np.where(x_time <= 6, 2 + (x_time * k_kinetics), 2 + (6 * k_kinetics))
            elif y_paths[i] == 2:
                Z[i, :] = 1 + (x_time * (k_math * 0.4))
            elif y_paths[i] == 3:
                Z[i, :] = 1.5 + (-2 * np.exp(-((x_time - 3)**2) / 4)) + (x_time * (k_cfd * 0.55))

        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X: Years', range=[0, 40], gridcolor='#23282f'),
                yaxis=dict(title='Y: Paths', tickvals=[1, 2, 3], ticktext=['Path A', 'Path B', 'Path C'], gridcolor='#23282f'),
                zaxis=dict(title='Z: Yield', range=[-1, 20], gridcolor='#23282f')
            ),
            margin=dict(l=0, r=0, b=0, t=0), height=550, paper_bgcolor='rgba(0,0,0,0)'
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("### 📋 Navigation Analytics")
            st.info("Adjust sliders on the left panel to dynamically shift terrain dimensions.")

        st.divider()
        st.subheader("🤖 Career OS: AIMAN.AI Navigation Copilot")
        
        # Container representing active dialogue history loop
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                # FIX 1: Linked assistant image pfp definition inside active loop
                avatar_img = "aimanai.jpeg" if message["role"] == "assistant" else "user"
                with st.chat_message(message["role"], avatar=avatar_img):
                    st.markdown(message["content"])

    # TAB 2: MARKETPLACE
    with tab2:
        st.title("💼 Live Internship Marketplace")
        with st.expander("🏢 PETRONAS Carigali ── Downstream Operations Intern"):
            st.write("Conduct molar mass balances and evaluate catalyst deactivation profiles.")
            if st.button("Deploy Application"):
                st.success("Application securely sent!")

    # ─── GLOBAL AI CHAT PIPELINE EXECUTION ENGINE ───
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    if user_query := st.chat_input("Ask about trade-offs..."):
        with chat_container:
            st.chat_message("user").markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Format the sliding values context parameters
        system_instruction = f"""
        You are AIMAN.AI, the Career OS Navigation Copilot. Speak directly and authentically.
        Current Vector States: Path A={k_kinetics}, Path B={k_math}, Path C={k_cfd}.
        """
        
        formatted_contents = [f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages]
        
        with chat_container:
            # FIX 2: Linked assistant image pfp definition during generation phase
            with st.chat_message("assistant", avatar="aimanai.jpeg"):
                response_placeholder = st.empty()
                response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=formatted_contents, config={"system_instruction": system_instruction}
                )
                ai_text = response.text
                response_placeholder.markdown(ai_text)
                
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        st.rerun()
