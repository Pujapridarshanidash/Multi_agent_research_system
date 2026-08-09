import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import sys
from pathlib import Path
from datetime import datetime

# Add the project directory to the path so we can import from pipeline.py
# Adjust this path based on where your project is located
# sys.path.insert(0, "/path/to/your/project")

from pipeline import run_research_pipeline

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1.5rem;
        border-radius: 0.5rem;
    }
    
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        color: #0c5460;
    }
    
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    
    h1 {
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔍 Multi-Agent Research System")
    st.markdown(
        "**Automated research pipeline** using AI agents to search, read, write, and critique research reports"
    )

with col2:
    st.markdown("")
    st.markdown("")
    if st.button("🔄 Reset", key="reset_button"):
        st.session_state.clear()
        st.rerun()

st.divider()

# ============================================================
# SIDEBAR CONFIGURATION
# ============================================================

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.markdown("### Research Configuration")
    
    show_details = st.toggle(
        "Show detailed output",
        value=True,
        help="Display detailed information from each agent"
    )
    
    auto_scroll = st.toggle(
        "Auto-scroll to results",
        value=True,
        help="Automatically scroll to results after research completes"
    )
    
    st.markdown("---")
    st.markdown("### About This System")
    st.info(
        """
        This multi-agent research system performs the following steps:
        
        1. **Search Agent** 🔎 - Searches for relevant information
        2. **Reader Agent** 📖 - Scrapes and reads top resources
        3. **Writer Chain** ✍️ - Drafts a comprehensive report
        4. **Critic Chain** 👁️ - Reviews and critiques the report
        """
    )

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "research_state" not in st.session_state:
    st.session_state.research_state = None
if "is_researching" not in st.session_state:
    st.session_state.is_researching = False
if "research_history" not in st.session_state:
    st.session_state.research_history = []

# ============================================================
# MAIN CONTENT - INPUT SECTION
# ============================================================

st.markdown("### 🎯 Enter Your Research Topic")

col1, col2 = st.columns([4, 1])

with col1:
    research_topic = st.text_input(
        "Research Topic",
        placeholder="e.g., 'Latest developments in quantum computing'",
        label_visibility="collapsed",
        key="topic_input"
    )

with col2:
    submit_button = st.button(
        "🚀 Start Research",
        key="submit_button",
        use_container_width=True,
        disabled=not research_topic or st.session_state.is_researching,
        type="primary"
    )

# ============================================================
# RESEARCH EXECUTION
# ============================================================

if submit_button:
    st.session_state.is_researching = True
    
    # Create a container for progress tracking
    progress_container = st.container()
    results_container = st.container()
    
    with progress_container:
        st.divider()
        st.markdown("### 📊 Research Progress")
        
        # Create columns for step indicators
        col1, col2, col3, col4 = st.columns(4)
        
        step_placeholders = {
            "search": col1.empty(),
            "reader": col2.empty(),
            "writer": col3.empty(),
            "critic": col4.empty()
        }
        
        # Status messages container
        status_placeholder = st.empty()
        
        try:
            # Step 1 - Search Agent
            with step_placeholders["search"]:
                st.markdown(
                    '<div class="info-box">🔎 <b>Search Agent</b><br/>Running...</div>',
                    unsafe_allow_html=True
                )
            
            with status_placeholder.container():
                st.info("🔎 Search Agent is searching for information...")
            
            # Step 2 - Reader Agent
            with step_placeholders["reader"]:
                st.markdown(
                    '<div class="info-box">📖 <b>Reader Agent</b><br/>Pending...</div>',
                    unsafe_allow_html=True
                )
            
            # Step 3 - Writer Chain
            with step_placeholders["writer"]:
                st.markdown(
                    '<div class="info-box">✍️ <b>Writer Chain</b><br/>Pending...</div>',
                    unsafe_allow_html=True
                )
            
            # Step 4 - Critic Chain
            with step_placeholders["critic"]:
                st.markdown(
                    '<div class="info-box">👁️ <b>Critic Chain</b><br/>Pending...</div>',
                    unsafe_allow_html=True
                )
            
            # Run the research pipeline
            state = run_research_pipeline(research_topic)
            st.session_state.research_state = state
            
            # Update all steps to completed
            with step_placeholders["search"]:
                st.markdown(
                    '<div class="success-box">🔎 <b>Search Agent</b><br/>✓ Completed</div>',
                    unsafe_allow_html=True
                )
            
            with step_placeholders["reader"]:
                st.markdown(
                    '<div class="success-box">📖 <b>Reader Agent</b><br/>✓ Completed</div>',
                    unsafe_allow_html=True
                )
            
            with step_placeholders["writer"]:
                st.markdown(
                    '<div class="success-box">✍️ <b>Writer Chain</b><br/>✓ Completed</div>',
                    unsafe_allow_html=True
                )
            
            with step_placeholders["critic"]:
                st.markdown(
                    '<div class="success-box">👁️ <b>Critic Chain</b><br/>✓ Completed</div>',
                    unsafe_allow_html=True
                )
            
            with status_placeholder.container():
                st.success("✅ Research completed successfully!")
            
            # Add to history
            st.session_state.research_history.append({
                "topic": research_topic,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "completed"
            })
            
        except Exception as e:
            st.error(f"❌ An error occurred during research: {str(e)}")
            with status_placeholder.container():
                st.error(f"Error details: {str(e)}")
            
            st.session_state.research_history.append({
                "topic": research_topic,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "failed"
            })
        
        finally:
            st.session_state.is_researching = False

# ============================================================
# RESULTS DISPLAY
# ============================================================

if st.session_state.research_state:
    st.divider()
    st.markdown("### 📋 Research Results")
    
    state = st.session_state.research_state
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📝 Report", "👁️ Critic Feedback", "🔎 Search Results", "📖 Scraped Content", "📊 Summary"]
    )
    
    # TAB 1 - FINAL REPORT
    with tab1:
        st.markdown("#### Final Research Report")
        if "report" in state and state["report"]:
            st.markdown(state["report"])
            
            # Download button for report
            col1, col2 = st.columns([3, 1])
            with col2:
                st.download_button(
                    label="📥 Download Report",
                    data=state["report"],
                    file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        else:
            st.warning("No report generated yet.")
    
    # TAB 2 - CRITIC FEEDBACK
    with tab2:
        st.markdown("#### Critic Review & Feedback")
        if "critic_report" in state and state["critic_report"]:
            st.markdown(state["critic_report"])
        else:
            st.warning("No critic feedback available yet.")
    
    # TAB 3 - SEARCH RESULTS
    with tab3:
        st.markdown("#### Search Agent Results")
        if show_details:
            if "search_results" in state and state["search_results"]:
                with st.expander("🔎 Search Results Details", expanded=True):
                    st.text(state["search_results"])
            else:
                st.warning("No search results available.")
        else:
            st.info("Enable 'Show detailed output' in settings to view search results.")
    
    # TAB 4 - SCRAPED CONTENT
    with tab4:
        st.markdown("#### Reader Agent - Scraped Content")
        if show_details:
            if "scraped_content" in state and state["scraped_content"]:
                with st.expander("📖 Scraped Content Details", expanded=False):
                    st.text(state["scraped_content"])
            else:
                st.warning("No scraped content available.")
        else:
            st.info("Enable 'Show detailed output' in settings to view scraped content.")
    
    # TAB 5 - SUMMARY
    with tab5:
        st.markdown("#### Research Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Topic", state.get("topic", "N/A")[:30] + "...")
        
        with col2:
            report_words = len(state.get("report", "").split()) if state.get("report") else 0
            st.metric("Report Length", f"{report_words} words")
        
        with col3:
            search_length = len(state.get("search_results", ""))
            st.metric("Search Results", f"{search_length} chars")
        
        with col4:
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.metric("Completed At", timestamp)
        
        st.divider()
        
        # Topic details
        st.markdown("**Research Topic:**")
        st.write(state.get("topic", "Not specified"))

# ============================================================
# RESEARCH HISTORY
# ============================================================

if st.session_state.research_history:
    with st.expander("📚 Research History", expanded=False):
        st.markdown("#### Previous Searches")
        
        for i, item in enumerate(reversed(st.session_state.research_history), 1):
            status_emoji = "✅" if item["status"] == "completed" else "❌"
            st.markdown(
                f"{status_emoji} **{item['topic']}** - {item['timestamp']}"
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.9rem; margin-top: 2rem;'>
    <p>🤖 Multi-Agent Research System | Powered by AI Agents</p>
    <p>For best results, provide detailed and specific research topics.</p>
    </div>
    """,
    unsafe_allow_html=True
)
