import streamlit as st

from helper.helper import stock_return_view

def show():
    """Display Stock Return by Sector Page"""

    st.markdown("---")
    fig=stock_return_view()  
    st.plotly_chart(fig, width='stretch')

