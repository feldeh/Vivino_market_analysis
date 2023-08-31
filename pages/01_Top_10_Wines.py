import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import folium
from streamlit_folium import st_folium, folium_static

 
df = pd.read_csv("./data/csv_streamlit/top_10_filtered.csv")

st.set_page_config(page_title="Vivino Analysis", page_icon=":wine_glass:", layout="wide")

st.header('_Quality Wines on a Budget:_ Our Top 10 Recommendations', divider='rainbow')

m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
               zoom_start=3, control_scale=True, tiles='cartodbpositron')
for i, row in df.iterrows():
    # Setup the content of the popup
    iframe = folium.IFrame('<b>Wine:</b> ' + str(row["wines"]) +
                           '<br/> <b>Price:</b> €' + str(row["price"]) +
                           '<br/> <b>Score:</b> ' + str(row["score"]) +
                           '<br/> <b>City:</b> ' + str(row["cities"]) + ' ' + str(row["country_iso"]))
    popup = folium.Popup(iframe, min_width=200, max_width=200)
    folium.Marker(location=[row['latitude'], row['longitude']],
                  popup=popup).add_to(m)

st_data = st_folium(m, width=1250)

