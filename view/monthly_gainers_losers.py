import streamlit as st

from helper.helper import monthly_gainers_losers_view

def show():
    """Display Monthly Gainers & Losers Page"""
    st.markdown("---")
    fig=monthly_gainers_losers_view()
    st.plotly_chart(fig, width='stretch')

