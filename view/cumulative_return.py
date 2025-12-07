import streamlit as st
import mpld3
import streamlit.components.v1 as components
from helper.helper import cumulative_return_view,cumulative_return_plotly_view

def show():
    """Display Cumulative Return Analysis Page"""
    st.markdown("---")
    fig=cumulative_return_plotly_view()
    st.plotly_chart(fig, width='stretch')
    # fig=cumulative_return_view()
    # fig_html = mpld3.fig_to_html(fig)
    # components.html(fig_html, height=600, scrolling=True)
    # st.pyplot(fig)
    

