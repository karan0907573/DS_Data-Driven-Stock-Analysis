import streamlit as st
from view import volatility, cumulative_return, monthly_gainers_losers, stock_correlation, stock_return

# Page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Title
st.title("📊 Data Driven Stock Analysis Dashboard")

# Initialize session state for page tracking
if "current_page" not in st.session_state:
    st.session_state.current_page = "volatility"

# Custom CSS for active button highlighting
st.markdown(f"""
<style>
    .stMain .stMainBlockContainer {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    .stMain .stMainBlockContainer > div {{
        gap: unset !important;
    }}
    [data-testid="stButton"] button {{
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stButton"] button:hover {{
        background-color: #f0f2f6 !important;
        transform: translateX(5px);
    }}

    .st-key-btn_{st.session_state.current_page} button {{
        background-color: #0D6EFD !important;
        color: white !important;
        font-weight: bold !important;
        border: 2px solid #0D6EFD !important;
    }}
    
    .st-key-btn_{st.session_state.current_page} button:hover {{
        background-color: #0A58CA !important;
    }}
</style>
""", unsafe_allow_html=True)

# Define pages
pages = {
    "📈 Volatility": "volatility",
    "💹 Cumulative Return": "cumulative_return",
    "🏆 Gainers & Losers": "monthly_gainers_losers",
    "🔗 Correlation": "stock_correlation",
    "📊 Sector Return": "stock_return"
}

# Navigation buttons in sidebar
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("---")

for display_name, page_key in pages.items():
    # Highlight active tab with visual indicator
    
        if st.sidebar.button(display_name, key=f"btn_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()

st.sidebar.markdown("---")

# Route to appropriate page
if st.session_state.current_page == "volatility":
    volatility.show()
elif st.session_state.current_page == "cumulative_return":
    cumulative_return.show()
elif st.session_state.current_page == "monthly_gainers_losers":
    monthly_gainers_losers.show()
elif st.session_state.current_page == "stock_correlation":
    stock_correlation.show()
elif st.session_state.current_page == "stock_return":
    stock_return.show()

if __name__ == "__main__":
    pass
