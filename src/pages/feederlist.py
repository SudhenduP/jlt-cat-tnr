import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

FEEDER_LOG_URL = ('data/JLT_FeederLogs.xlsx')
DATA_LAT_LON_URL = ('data/Cluster-GeoData.csv')
ICON_URL = "https://raw.githubusercontent.com/SudhenduP/temproraryfiles/master/person.png"


st.markdown(
        "<h2 style='text-align: center; color: black;'>Hello! How are you today? This tiny site keeps a log of our JLT community cats 😻</h2>",
        unsafe_allow_html=True)


icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 150,
    "height": 150,
    "anchorY": 150,
}


def load_feeder_data():
    feeder_details = pd.read_excel(FEEDER_LOG_URL)
    data_cluster_geo = pd.read_csv(DATA_LAT_LON_URL)
    # data_cluster_geo.rename({'Cluster': 'USUAL SPOT'})

    # data.dropna(subset=['longitude', 'latitude'], inplace=True)
    # lowercase = lambda x: str(x).lower()
    #  data.rename(lowercase, axis='columns', inplace=True)
    feeder_details = feeder_details.fillna('No')
    feeder_details = pd.merge(left=feeder_details, right=data_cluster_geo, how='left', left_on='Cluster',
                                right_on='Cluster')
    feeder_details = feeder_details.sort_values(by='Cluster', ascending=True)
    #feeder_details = feeder_details.drop(columns=['Telephone No.', 'LAT', 'LON'])
    return feeder_details





def show_feeder_data():
    feeder_details= load_feeder_data()
    feeder_details_plain= feeder_details.drop(columns=['Telephone No.', 'LAT', 'LON'])

    st.subheader("List of feeder in the community with other details")
    cluster_select = st.selectbox(
        'Select the Cluster you want to view?',
        feeder_details_plain['Cluster'].unique())

    selected_cluster = feeder_details_plain[feeder_details_plain['Cluster'] == cluster_select].sort_values(
        by=['Cluster'], ascending=False)
    st.write(selected_cluster)


#For icons


def show_feeder_visual(feeder_visual_data):
    feeder_visual_data = load_feeder_data()
    feeder_visual_data["icon_data"] = None
    for i in feeder_visual_data.index:
        feeder_visual_data["icon_data"][i] = icon_data
    COLOR_RANGE = [
        [1, 152, 189],
        [73, 227, 206],
        [216, 254, 181],
        [254, 237, 177],
        [254, 173, 84],
        [209, 55, 78]
    ];
    LIGHT_SETTINGS = {
        "lightsPosition": [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
        "ambientRatio": 0.4,
        "diffuseRatio": 0.6,
        "specularRatio": 0.2,
        "lightsStrength": [0.8, 0.0, 0.8, 0.0],
        "numberOfLights": 2
    };

    midpoint = (np.average(feeder_visual_data["LAT"]), np.average(feeder_visual_data["LON"]))

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 13,
            "pitch": 60,
            "bearing": -27.36,
            "tooltip": True,

        },
        layers=[
        #    pdk.Layer(
        #    type="IconLayer",
        #    data=feeder_details,
        #    get_icon="icon_data",
        #    get_size=4,
        #    size_scale=15,
        #    get_position=["LON", "LAT"],
        #    pickable=True,
    #),
		pdk.Layer(
			"HexagonLayer",
			data=feeder_visual_data[['LAT', 'LON']],
			get_position=["LON", "LAT"],
			auto_highlight=True,
			radius=100,
			elevation_scale=200,
			pickable=False,
			# scrollZoom=False,
			elevation_range=[0, 10],
			extruded=True,
			coverage=1,
			lightSettings=LIGHT_SETTINGS,
			colorRange=COLOR_RANGE,
			opacity=1,
			tooltip=True,
			hoverinfo='text',
		),
    ],
    ))