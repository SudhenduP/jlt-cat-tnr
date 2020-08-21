import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots


fig = make_subplots(
    rows = 1, cols = 4,
    specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
    ]
)
DATA_URL = (r'data\JLT CAT-A-LOG BY CLUSTER.csv')

image = Image.open('asset/img/banner.png')
st.image(image, caption='',
                 use_column_width=True)

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    #data.dropna(subset=['longitude', 'latitude'], inplace=True)
    #lowercase = lambda x: str(x).lower()
    #  data.rename(lowercase, axis='columns', inplace=True)
    data  = data.fillna('No')
    return data

if st.button('Say Meow!!!'):
    st.write('😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽')
    st.balloons()




# Create a text element and let the reader know the data is loading.
data_load_state = st.sidebar.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading data completed")

original_data = data
show_case_data = data.drop(columns=['LAT','LON'])

st.header("A look the numbers")

total_cat_count= len(data)
total_tnr_done= len(data[data['TNR'] == 'Yes'])
total_tnr_pending= len(data[data['TNR'] != 'Yes'])
total_adopted = len(data[data['ADOPTED'] == 'Yes'])
print(total_tnr_done)
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_cat_count ,
        title="Total Cats",
    ),
    row=1, col=1
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_tnr_done,
        title="TNR Done ",
    ),
    row=1, col=2
)

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_tnr_pending,
        title="TNR Pending",
    ),
    row=1, col=3
)


fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_adopted ,
        title="Adopted",
    ),
    row=1, col=4
)


fig.update_layout(paper_bgcolor = "LightSteelBlue", autosize=True, height=300)

st.write(fig)



ax = fig = px.pie(original_data,
             #values='GENDER',
             names='GENDER',
             #x='USUAL SPOT',
             #y='Count',
             title='Gender Distribution',
             #color='GENDER',
             #barmode='stack'
                  )
st.write(ax)


midpoint = (np.average(data["LAT"]), np.average(data["LON"]))

#st.write(pdk.Deck(
#    map_style="mapbox://styles/mapbox/dark-v10",
#    initial_view_state={
#        "latitude": midpoint[0],
#        "longitude": midpoint[1],
#        "zoom": 14,
#        "pitch": 50,
#    },
#    layers=[
#        pdk.Layer(
#            "ScatterplotLayer",
#            data=data[['LAT', 'LON']],
#            get_position=["LON", "LAT"],
#            pickable=True,
#            opacity=0.8,
#            stroked=True,
#            filled=True,
#            radius_scale=6,
#            #radius_min_pixels=8,
#            #radius_max_pixels=100,
#            line_width_min_pixels=1,
#            get_radius=5,
#            get_fill_color=[255, 200, 0],
#            get_line_color=[0, 0, 0],
#       ),
#    ],
#))

LIGHT_SETTINGS = {
    "lightsPosition": [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
    "ambientRatio": 0.4,
    "diffuseRatio": 0.6,
    "specularRatio": 0.2,
    "lightsStrength": [0.8, 0.0, 0.8, 0.0],
    "numberOfLights": 2
};


st.header("TNR Status")
tnr_status = st.selectbox('',['TNR Done', 'TNR Pending', 'Unknown'])


if tnr_status == 'TNR Done':
    tnr_data = original_data.query('TNR == "Yes"').sort_values(
        by=['USUAL SPOT'], ascending=False)

elif tnr_status == 'TNR Pending':
    tnr_data = original_data.query('TNR == "No"').sort_values(
        by=['USUAL SPOT'], ascending=False)

else:
    tnr_data = original_data.query('TNR == "Unknown"').sort_values(
        by=['USUAL SPOT'], ascending=False)

data_cluster = tnr_data.groupby(['USUAL SPOT']).count().sort_values(
    "CATID", ascending=False).head(20).reset_index()
data_cluster=data_cluster.rename(columns={"CATID": "Count"})


ax = fig = px.bar(data_cluster,
             x='USUAL SPOT',
             y='Count',
             title='By Cluster',
             #color='GENDER',
             barmode='stack')
st.write(ax)


COLOR_RANGE = [
    [1, 152, 189],
    [73, 227, 206],
    [216, 254, 181],
    [254, 237, 177],
    [254, 173, 84],
    [209, 55, 78]
];
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 14,
        "pitch": 50,
        "bearing" :-27.36,

    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=tnr_data[['LAT', 'LON']],
            get_position=["LON", "LAT"],
            auto_highlight=True,
            radius= 25,
            elevation_scale=200,
            pickable=True,
            elevation_range=[0, 10],
            extruded=True,
            coverage=1,
            lightSettings= LIGHT_SETTINGS,
            #colorRange = '00000',
            opacity=1,
            tooltip= True
        ),
    ],
))


st.header("Log of all cats in and around JLT Clusters")
st.write(show_case_data)
#---



