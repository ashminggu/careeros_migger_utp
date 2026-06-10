import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="InternMatch Prototype", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# This keeps track of our "swipes" so the profiles actually change when you click buttons
if 'student_idx' not in st.session_state:
    st.session_state.student_idx = 0
if 'company_idx' not in st.session_state:
    st.session_state.company_idx = 0
if 'matches' not in st.session_state:
    st.session_state.matches = []

# --- MOCK DATA ---
companies = [
    {"name": "Volt Dynamics", "role": "Hardware Intern", "promise": "You'll design actual PCBs, not fetch coffee.", "video_desc": "🎬 Video: Engineer giving a lab tour and showing the testing equipment."},
    {"name": "CodeCore Systems", "role": "C Programming Intern", "promise": "Mentorship from senior devs on embedded systems.", "video_desc": "🎬 Video: Team lunch and a quick look at the open-concept coding floor."},
    {"name": "Nexus Energy", "role": "Power Systems Trainee", "promise": "Hands-on experience with grid optimization projects.", "video_desc": "🎬 Video: Manager explaining the day-to-day tasks on site."}
]

students = [
    {"name": "Jordan", "major": "Electrical & Electronics Engineering", "skills": "Circuit Theory, MATLAB", "video_desc": "🎬 Video: Jordan showing a breadboard circuit they built for a lab project."},
    {"name": "Sam", "major": "Software Engineering", "skills": "C++, Python", "video_desc": "🎬 Video: Sam doing a quick 30-second screen record of a working script."},
    {"name": "Alex", "major": "Mechanical Engineering", "skills": "AutoCAD, SolidWorks", "video_desc": "🎬 Video: Alex presenting a 3D printed prototype."}
]

# --- APP NAVIGATION ---
st.title("🤝 InternMatch Marketplace")
view = st.sidebar.radio("Log in as:", [
    "🎓 Student (Find Internships)", 
    "🏢 Employer (Find Talent)", 
    "💬 Messages & Matches"
])

# --- 1. STUDENT VIEW (Swiping on Companies) ---
if view == "🎓 Student (Find Internships)":
    st.subheader("Swipe on Company 'Day in the Life' Pitches")
    
    if st.session_state.company_idx < len(companies):
        current_company = companies[st.session_state.company_idx]
        
        # Profile Card
        with st.container(border=True):
            st.header(f"🏢 {current_company['name']}")
            st.subheader(f"Role: {current_company['role']}")
            st.info(current_company['video_desc'])
            st.write(f"*Our Promise to You:* {current_company['promise']}")
            
            # Swipe Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ Pass", key="pass_comp", use_container_width=True):
                    st.session_state.company_idx += 1
                    st.rerun()
            with col2:
                if st.button("✅ Match", key="match_comp", use_container_width=True):
                    st.success(f"You swiped right on {current_company['name']}!")
                    st.session_state.matches.append(current_company['name'])
                    st.session_state.company_idx += 1
                    st.rerun()
    else:
        st.warning("You've seen all the companies for today! Check back later.")

# --- 2. EMPLOYER VIEW (Swiping on Students) ---
elif view == "🏢 Employer (Find Talent)":
    st.subheader("Swipe on Student Video Portfolios")
    
    if st.session_state.student_idx < len(students):
        current_student = students[st.session_state.student_idx]
        
        # Profile Card
        with st.container(border=True):
            st.header(f"🎓 {current_student['name']}")
            st.write(f"*Major:* {current_student['major']}")
            st.write(f"*Core Skills:* {current_student['skills']}")
            st.info(current_student['video_desc'])
            
            # Swipe Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ Pass", key="pass_stud", use_container_width=True):
                    st.session_state.student_idx += 1
                    st.rerun()
            with col2:
                if st.button("✅ Connect", key="match_stud", use_container_width=True):
                    st.success(f"You invited {current_student['name']} to connect!")
                    st.session_state.student_idx += 1
                    st.rerun()
    else:
        st.warning("No more student profiles in your queue.")

# --- 3. IN-APP CHAT VIEW ---
elif view == "💬 Messages & Matches":
    st.subheader("Your Direct Connections")
    
    if len(st.session_state.matches) == 0:
        st.write("You don't have any matches yet. Go swipe!")
    else:
        # Create a tab for each match to simulate a chat interface
        tabs = st.tabs(st.session_state.matches)
        
        for i, tab in enumerate(tabs):
            with tab:
                company_name = st.session_state.matches[i]
                st.write(f"### Chatting with {company_name}")
                
                # Mock Chat History
                with st.chat_message("assistant"):
                    st.write(f"Hi! We saw your video portfolio and loved your circuit project. Are you available for a quick call this Thursday?")
                
                # Chat Input Box
                prompt = st.chat_input("Say something back...")
                if prompt:
                    with st.chat_message("user"):
                        st.write(prompt)
                    with st.chat_message("assistant"):
                        st.write("Awesome, I'll send over a calendar invite!")
                
                # Quick Action Buttons
                st.divider()
                st.write("*Quick Actions:*")
                col1, col2 = st.columns(2)
                col1.button("📅 Schedule Interview", key=f"sched_{i}")
                col2.button("📎 Attach Lab Project PDF", key=f"attach_{i}")
