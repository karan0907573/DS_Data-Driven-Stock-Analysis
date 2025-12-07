import streamlit as st

from helper.helper import stock_correlation_view

def show():
    """Display Stock Correlation Analysis Page"""
    st.markdown("---")
    fig=stock_correlation_view()
    st.plotly_chart(fig, width='stretch')

