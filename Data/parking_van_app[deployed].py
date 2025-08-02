#Import libraries 
import pandas as pd
import numpy as np 
import datetime as dt
import streamlit as st
from branca.element import Element
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from streamlit.components.v1 import html as st_html
from st_aggrid import AgGrid, GridOptionsBuilder
from geopy.distance import geodesic
from pathlib import Path

#Preprocessing previous data 

BASE_DIR = Path(__file__).resolve().parent  # folder containing this script, e.g., Data/
data_path = BASE_DIR / "parking-meters.xlsx"
logo_path = BASE_DIR / "logo.png"

@st.cache_data
def load_parking():
    return pd.read_excel(data_path)

park = load_parking()
park_clean = park.dropna(subset='CREDITCARD')

st.session_state.setdefault("geo_placeholder", None)

if "request_location" not in st.session_state:
    st.session_state.request_location = False
if "user_coords" not in st.session_state:
    st.session_state.user_coords = None



#Title
st.markdown("<h1 style='text-align:center; margin:0;'>Vancouver Parking Price Finder</h1>", unsafe_allow_html=True)

#Sidebar 
with st.sidebar:
    st.sidebar.image(logo_path)
    date = st.sidebar.selectbox("Which Day Will You Park?", ['Mon - Fri', 'Sat', 'Sun']) 
    time = st.sidebar.selectbox("What Time Will You Park?", ['9:00AM - 6:00PM', '6:00PM - 10:00PM'])
    credit = st.sidebar.selectbox("Paying By Credit Card?", ['', 'Yes', 'No'])
    location_button = st.button("Use Location")

    if location_button or (st.session_state.request_location and st.session_state.user_coords is None):
        st.session_state.request_location = True
        loca = streamlit_geolocation()
        lat = loca.get("latitude")
        lon = loca.get("longitude")
        if lat is not None and lon is not None:
            st.session_state.user_coords = (lat, lon)
            st.session_state.request_location = False
            st.success("Location shared successfully!")
        else:
            st.warning("Please allow location access in your browser.")
     



#Filters For Data
if date == 'Mon - Fri' :
    if time == '9:00AM - 6:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_MF_9A_6P',
                   'T_MF_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '9:00AM - 6:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_MF_9A_6P',
                    'T_MF_9A_6P','CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No'] 
    elif time == '9:00AM - 6:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_MF_9A_6P',
                    'T_MF_9A_6P','CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
    elif time == '6:00PM - 10:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD','R_MF_6P_10', 
                    'T_MF_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '6:00PM - 10:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD','R_MF_6P_10', 
                    'T_MF_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No'] 
    elif time == '6:00PM - 10:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD','R_MF_6P_10', 
                    'T_MF_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]


if date == 'Sat' :
    if time == '9:00AM - 6:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_9A_6P',
                   'T_SA_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '9:00AM - 6:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_9A_6P',
                   'T_SA_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No']
    elif time == '9:00AM - 6:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_9A_6P',
                   'T_SA_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
    elif time == '6:00PM - 10:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_6P_10',
                   'T_SA_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '6:00PM - 10:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_6P_10',
                   'T_SA_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No']
    elif time == '6:00PM - 10:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SA_6P_10',
                   'T_SA_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']] 


if date == 'Sun':
    if time == '9:00AM - 6:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_9A_6P',
                   'T_SU_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '9:00AM - 6:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_9A_6P',
                   'T_SU_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No']
    elif time == '9:00AM - 6:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_9A_6P',
                   'T_SU_9A_6P', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
    elif time == '6:00PM - 10:00PM' and credit == 'Yes':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_6P_10',
                   'T_SU_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'Yes']
    elif time == '6:00PM - 10:00PM' and credit == 'No':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_6P_10',
                   'T_SU_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']]
        park_list = park_list.loc[park_list['CREDITCARD'] == 'No']
    elif time == '6:00PM - 10:00PM' and credit == '':
        park_list = park_clean[['METERID', 'METERHEAD', 'R_SU_6P_10',
                   'T_SU_6P_10', 'CREDITCARD', 'Geo Local Area', 'geo_point_2d']] 
        
cols = list(park_list.columns)
cols[2] = 'Rate'
cols[3] = 'Time_Limit'
park_list2 = park_list
park_list2.columns = cols


meter_id = park_list2[['METERID']]
gb = GridOptionsBuilder.from_dataframe(meter_id) 
gb.configure_selection('single')
gb.configure_column('METERID', width = 300, autowidth = False, resizable = True)
gb.configure_grid_options(
    suppressHorizontalScroll=True,
    domLayout='normal')
grid_options = gb.build()
grid_response = None


col1, col2, col3, col4, col5 = st.columns([1, 1, 4, 1, 0.2])  
user_coords = st.session_state["user_coords"] 
park_list2[['lat', 'lon']] = (
    park_list2['geo_point_2d']
    .str.split(',', expand=True)
    .apply(lambda col: col.str.strip())
    .astype(float))

if user_coords:
    park_list2['distance_km'] = park_list2.apply(
        lambda row: geodesic(user_coords, (row['lat'], row['lon'])).km,
        axis=1
    )
    meter_id["Distance_From"] = park_list2['distance_km'].round(2)
    meter_id = meter_id.sort_values('Distance_From').reset_index(drop=True)
if user_coords: 
    with col2:
        grid_response = AgGrid(meter_id, gridOptions = grid_options, height = 300,
                        fit_columns_on_grid_load= False, 
                        use_container_width= True) 

with col3:
    if grid_response:
        if grid_response.selected_data is not None and not grid_response.selected_data.empty: 
            selected_row = grid_response.selected_data.iloc[0]
            target_coords_str2 = park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'geo_point_2d'].iloc[0]
            lat2, lon2 = map(float, target_coords_str2.split(','))
            target_coords2 = (lat2, lon2)
            distance_km = round(geodesic(user_coords, target_coords2).km, 2)
            st.markdown(
            f"""
            <div style="background-color:#2E2E2E; border-radius:5px">
            <div style='font-size:32px; font-weight:700;'> &nbspRate (CAD/Hour): {park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'Rate'].values[0]}</div>
            <div style='font-size:32px; font-weight:700; margin-top:-13px;'> &nbspTime Limit: {park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'Time_Limit'].values[0]}</div>
            <div style='font-size:32px; font-weight:700; margin-top:-13px;'> &nbspDistance: {distance_km}km</div>
            <div style='font-size:32px; font-weight:700; margin-top:-13px;'> &nbspWalking Time: {round((distance_km * 10))} min</div>
            <div style="height:28px;"></div>
            <div style='font-size:18px; font-weight:400; margin-top:-0px;'> <strong>&nbsp&nbsp;Parking Meter ID:</strong> {selected_row['METERID']}</div>
            <div style='font-size:18px; font-weight:400; margin-top:-3px;'> <strong>&nbsp&nbsp;Local Area:</strong> {park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'Geo Local Area'].values[0]}</div>
            <div style='font-size:18px; font-weight:400; margin-top:-3px;'> <strong>&nbsp&nbsp;Type of Meter:</strong> {park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'METERHEAD'].values[0]}</div>         
            <div style='font-size:18px; font-weight:400; margin-top:-3px;'> <strong>&nbsp&nbsp;Credit Card:</strong> {park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'CREDITCARD'].values[0]}</div>
            <div style='height:5px;'></div>
        </div>
        """,
        unsafe_allow_html=True)

if grid_response:
        if grid_response.selected_data is not None and not grid_response.selected_data.empty: 
            selected_row = grid_response.selected_data.iloc[0]
            target_coords_str2 = park_list2.loc[park_list2['METERID'] == selected_row['METERID'], 'geo_point_2d'].iloc[0]
            lat2, lon2 = map(float, target_coords_str2.split(','))
            target_coords2 = (lat2, lon2)
            distance_km = round(geodesic(user_coords, target_coords2).km, 2)
            #Making Map          
            mid_lat = (user_coords[0] + target_coords2[0]) / 2 
            mid_lon = (user_coords[1] + target_coords2[1]) / 2
            m = folium.Map(location=[mid_lat, mid_lon], zoom_start=14, tiles= "OpenStreetMap")
            # user marker
            folium.Marker(
                    location=user_coords,
                    tooltip="You are here",
                    popup="You",
                    icon=folium.Icon(color="red", prefix= "fa", icon="user")
                    ).add_to(m)

            # meter marker with info
            folium.Marker(
                    location=target_coords2,
                    tooltip= 'Parking meter is here',
                    popup= "Parking meter",
                    icon= folium.Icon(color="black",prefix= "fa", icon = "parking" )
            ).add_to(m)

            # line connecting them
            folium.PolyLine(locations=[user_coords, target_coords2], weight=3, dash_array="5").add_to(m)

            # ensure both points are visible
            m.fit_bounds([user_coords, target_coords2]) 
            
            inner_css = """
            <style>
            html, body {
                margin: 0;
                padding: 0;
                background: transparent;
                height: 100%;
            }
            .leaflet-container {
                width: 100% !important;
                height: 100% !important;
                border-radius: 0px; /* optional if you want internal rounding */
                overflow: hidden;
            }
            </style>
            """
            m.get_root().html.add_child(Element(inner_css))


            map_html = m.get_root().render()
            escaped = map_html.replace('"', "&quot;").replace("\n", " ")
            iframe = f"""
            <iframe
            srcdoc="{escaped}"
            width="675"
            height="495"
            style="
                display:block;
                box-sizing:border-box;
                border:6px solid white;
                border-radius:12px;
                box-shadow:0 4px 14px rgba(0,0,0,0.25);
                overflow:hidden;
            "
            loading="lazy"
            sandbox="allow-scripts allow-same-origin"
            ></iframe>
            """
            st_html(iframe, height=520)   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            