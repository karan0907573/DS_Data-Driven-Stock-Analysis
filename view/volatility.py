import streamlit as st
from helper.helper import volatility_view

def show():
    """Display Volatility Analysis Page"""

    st.markdown("---")
    fig=volatility_view()
    st.plotly_chart(fig, width='stretch')
    
    
