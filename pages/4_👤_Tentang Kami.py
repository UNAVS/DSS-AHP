import streamlit as st
from streamlit_extras.stylable_container import stylable_container 

st.set_page_config(page_title="Input Alternatif", page_icon="📊", layout="wide")
st.markdown("<h1 style='text-align: center;'>Kelompok 5</h1>", unsafe_allow_html=True)

col = st.columns(4)
with col[0]:
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                background-color: #ecb159
            }
            """,
    ):
        cont0 = st.container(border=True)
        cont0.markdown("<h3 style='text-align: center;'>Giovanny Alberta Tambahjong</h3>", unsafe_allow_html=True)
        cont0.image('images/GIOVANNY.png', caption="162012133012")
with col[1]:
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                background-color: #ecb159
            }
            """,
    ):
        cont1 = st.container(border=True)
        cont1.markdown("<h3 style='text-align: center;'>Michael Albert Theojaya</h3>", unsafe_allow_html=True)
        cont1.image('images/MICHAEL.png', caption="164221011")
with col[2]:
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                background-color: #ecb159
            }
            """,
    ):
        cont2 = st.container(border=True)
        cont2.markdown("<h3 style='text-align: center;'>Muhammad Hanif</h3>", unsafe_allow_html=True)
        cont2.markdown("<h3 style='text-align: center;'> </h3>", unsafe_allow_html=True)
        cont2.image('images/HANIF.png', caption="162112133001")
with col[3]:
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                background-color: #ecb159
            }
            """,
    ):
        cont3 = st.container(border=True)
        cont3.markdown("<h3 style='text-align: center;'>Ziyan Iffatun Nadhira</h3>", unsafe_allow_html=True)
        cont3.image('images/ZIYAN.png', caption="162112133098")
