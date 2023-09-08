import streamlit as st
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
import html

if "center" not in st.session_state:
    st.session_state["center"] = None
if "zoom" not in st.session_state:
    st.session_state["zoom"] = 16
if "markers" not in st.session_state:
    st.session_state["markers"] = []

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,  skiprows=1  )
    df = df.drop_duplicates(subset='SSID', keep="last")
    df['SSID'] = df.SSID.str.replace('[^0-9a-zA-Z.,-/ ]', '')
    df['SSID'] = df.SSID.str.replace('\\', '')
    df = df.dropna()
    df = df[:1000]
    st.write(df)
    startIndex = round(len(df)/2)

    if st.session_state["center"] is None:
        st.session_state["center"] = [df.iloc[startIndex]['CurrentLatitude'], df.iloc[startIndex]['CurrentLongitude']]

        for _,row in df.iterrows():
            rowMarker = folium.Marker(
                location=[row['CurrentLatitude'], row['CurrentLongitude']],
                popup = folium.Popup(row['SSID'], parse_html=False)
            )
            st.session_state["markers"].append(rowMarker)

with st.echo(code_location="below"):
    if st.session_state["center"] is not None:
        m = folium.Map(location=st.session_state["center"], zoom_start=16)
        fg = folium.FeatureGroup(name="Markers")
        for marker in st.session_state["markers"]:
            fg.add_child(marker)

        st_folium(
            m,
            center=st.session_state["center"],
            zoom=st.session_state["zoom"],
            key="new",
            feature_group_to_add=fg,
            height=400,
            width=700,
        )