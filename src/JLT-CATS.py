import base64
import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import BytesIO


st.beta_set_page_config(page_title='JLT-CAT-A-LOG', page_icon="🧊",
                        layout="centered",
                        initial_sidebar_state="expanded", )
st.sidebar.image('asset/img/leo.jpg')

st.sidebar.markdown(
    """

**This is Leo (also know as Fergus). One of our JLT kitten, now turned into a handsome boy, giving a taking love in a lovely home.**

Welcome! This tiny website keeps a log of our cats buddies 😻 in JLT.** 

JLT has many cats in the communities, big and small, ginger and tabby, fierce and gentle, senior and kittens.

**And we love all of them 😀.**

Some good folks at JLT regularly take care of the community cats. 
Part of their work is to make sure the cats are well fed 🍲, have plenty of water (Dubai summer☀️) and get all necessary medical treatments.

If you would like to help in anyway, please get in touch with: 9715xxxxx

Until then, check our CAT-O-LOG 😄😄😄😄😄

    """
)

fig_1 = make_subplots(
    rows=1, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
    ],
horizontal_spacing = 0, vertical_spacing=0
)

fig_2 = make_subplots(
    rows=1, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
    ],
horizontal_spacing = 0, vertical_spacing=0
)
DATA_URL = ('data/JLT CAT-A-LOG BY CLUSTER.csv')

image = Image.open('asset/img/banner.png')
st.image(image, caption='',
         use_column_width=True)

st.header("Hello! How are you today? This tiny site keeps a log of our JLT communiy tcats 😻")


@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    # data.dropna(subset=['longitude', 'latitude'], inplace=True)
    # lowercase = lambda x: str(x).lower()
    #  data.rename(lowercase, axis='columns', inplace=True)
    data = data.fillna('No')
    data = data.sort_values(by='USUAL SPOT', ascending=True)
    return data


if st.button('Say Meow!!!'):
    st.write('😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽')
    st.balloons()

# Create a text element and let the reader know the data is loading.
# data_load_state = st.sidebar.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
# data_load_state.text("Loading data completed")

original_data = data
show_case_data = data.drop(columns=['LAT', 'LON'])




total_cat_count = len(data)
total_tnr_done = len(data[data['TNR'] == 'Yes'])
total_tnr_pending = len(data[data['TNR'] != 'Yes'])
total_adopted = len(data[data['ADOPTED'] == 'Yes'])


fig_1.add_trace(
    go.Indicator(
        mode="number",
        value=total_cat_count,
        title="Total Cats",

    ),
    row=1, col=1

)

fig_1.add_trace(
    go.Indicator(
        mode="number",
        value=total_adopted,
        title="Adopted",
    ),
    row=1, col=2
)

fig_2.add_trace(
    go.Indicator(
        mode="number",
        value=total_tnr_done,
        title="TNR Done",
    ),
    row=1, col=1
)

fig_2.add_trace(
    go.Indicator(
        mode="number",
        value=total_tnr_pending,
        title="TNR Pending",
    ),
    row=1, col=2
)

fig_1.update_layout(paper_bgcolor="LightSteelBlue", margin=dict(l=20, r=20, t=20, b=20))

#st.write(fig_1)

st.plotly_chart(fig_1,use_container_width=True)
#st.plotly_chart(fig_1)


fig_2.update_layout(paper_bgcolor="LightSteelBlue", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_2,use_container_width=True)

st.subheader('Gender Distribution')

fig_gender = px.pie(original_data,
            # values='GENDER',
            names='GENDER',
            # x='USUAL SPOT',
            # y='Count',
            # title='Gender Distribution',
            # color='GENDER',
            # barmode='stack'
            #    width= 400,
            #    height= 300,
            )

st.plotly_chart(fig_gender,use_container_width=True)

midpoint = (np.average(data["LAT"]), np.average(data["LON"]))

# st.write(pdk.Deck(
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
# ))

LIGHT_SETTINGS = {
    "lightsPosition": [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
    "ambientRatio": 0.4,
    "diffuseRatio": 0.6,
    "specularRatio": 0.2,
    "lightsStrength": [0.8, 0.0, 0.8, 0.0],
    "numberOfLights": 2
};

st.subheader("TNR Status")
tnr_status = st.selectbox('', ['TNR Done', 'TNR Pending', 'Unknown'])

if tnr_status == 'TNR Done':
    tnr_data = original_data.query('TNR == "Yes"').sort_values(
        by=['USUAL SPOT'], ascending=True)

elif tnr_status == 'TNR Pending':
    tnr_data = original_data.query('TNR == "No"').sort_values(
        by=['USUAL SPOT'], ascending=True)

else:
    tnr_data = original_data.query('TNR == "Unknown"').sort_values(
        by=['USUAL SPOT'], ascending=True)

data_cluster = tnr_data.groupby(['USUAL SPOT']).count().sort_values(
    "CATID", ascending=False).head(20).reset_index()
data_cluster = data_cluster.rename(columns={"CATID": "Count"})

st.subheader('Clusterwise distribution for: %s '%tnr_status)

fig_cluster_bar = px.bar(data_cluster,
                  x='Count',
                  y='USUAL SPOT',
                  # title='By Cluster',
                  # color='GENDER',
                  barmode='stack',
                  orientation='h',
             #     height=300, width=400
            )
st.plotly_chart(fig_cluster_bar,use_container_width=True)

COLOR_RANGE = [
    [1, 152, 189],
    [73, 227, 206],
    [216, 254, 181],
    [254, 237, 177],
    [254, 173, 84],
    [209, 55, 78]
];

st.subheader('Map showing the the cluster with: %s '%tnr_status)

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
        pdk.Layer(
            "HexagonLayer",
            data=tnr_data[['LAT', 'LON']],
            get_position=["LON", "LAT"],
            auto_highlight=True,
            radius=100,
            elevation_scale=200,
            pickable=True,
            elevation_range=[0, 10],
            extruded=True,
            coverage=1,
            lightSettings=LIGHT_SETTINGS,
            colorRange=COLOR_RANGE,
            opacity=1,
            tooltip=True,
        ),

    ],


    tooltip={"html": "<b>Color Value:</b> {TNR}", "style": {"color": "white"}},
))

# 'You selected: ', option

st.subheader("List of our cats in the community")
# Feel free to search by Name, Cluster or Gender 😉""")
cluster_select = st.selectbox(
    'Select the Cluster you want to view?',
    data['USUAL SPOT'].unique())

# data.query("injured_persons >= @injured_people")
selected_cluster = show_case_data[show_case_data['USUAL SPOT'] == cluster_select].sort_values(
    by=['USUAL SPOT'], ascending=False)
st.write(selected_cluster)
# ---

st.subheader('****Coming soon!****')
st.text("Search for a particular cat and see their photo")
st.text("Don't see your community or cluster cat in the list? You can add it here")

csv = original_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)