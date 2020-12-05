
# import library- will clean later
import base64
import importlib
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st
from PIL import Image
from plotly.subplots import make_subplots

import search
import helpus
import feederlist
#import reportacat

# set page level setting


st.beta_set_page_config(page_title='JLT-CAT-A-LOG', page_icon="🧊",
                        layout="centered",
                        initial_sidebar_state="auto", )

# hide the hamburger
hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
			#footer {visibility: hidden;}
			</style>
			"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# Found and Search Section


# sidebar configuration- START
#st.markdown(
#    """
#<style>
#.sidebar .sidebar-content {
#    background-image: linear-gradient(#00000,#00000);
#    color: white;
#}
#</style>
#""",
#    unsafe_allow_html=True,
#)


st.sidebar.image('asset/img/logo2.png', width=300)
#st.sidebar.markdown(f"<a href='#linkto_Search'>Found a Cat? Click here to search</a>", unsafe_allow_html=True)
menus = ['Home', 'Search For Cats', 'How can you Help', 'Volunteers']# 'Report A Cat']
# st.sidebar.header('MENU')
menu = st.sidebar.radio('', menus)
st.sidebar.markdown(
    """


**Welcome! This tiny website keeps a log of our cat-buddies 😻 in JLT.**

JLT, DMCC is beautiful community with amazing people and purrfect cats! We have big and small, ginger and tabby, fierce and gentle, senior and kittens.
You ask for it, you got it!

**And we love all of them 😀**

Some good folks 🙋 🙋‍♂️ at JLT regularly take care of the community cats. 
Part of their work is to make sure the cats are well fed 🍲, have plenty of water (Dubai summer☀️) 
and get all medical attention 👨‍⚕️. Oh and most important of all, TNR!

If you would like to help in anyway, please get in touch with: +971 52 6500 102 

Join us on Facebook [CatLoversOfJLT](https://www.facebook.com/groups/CatLoversOfJLT/) 

Until then, check our CAT-O-LOG 😄😄😄😄😄

	"""
)

# sidebar configuration- END

# variables

# DATA_URL = ('data/JLT CAT-A-LOG BY CLUSTER.csv')
banner = Image.open('asset/img/banner2.png')
DATA_LAT_LON_URL = ('data/Cluster-GeoData.csv')
DATA_URL_NEW = ('data/JLT_CatLogs.xlsx')
# Banner
st.image(banner, caption='',
         use_column_width=True)

st.markdown(
        "<h1 style='text-align: center; color: #3269a8;'>Hello! How are you today? ",
        unsafe_allow_html=True)
st.markdown(
        "<h2 style='text-align: center; color: black;'>Over here we keep the log of all our JLT community cats 😻</h2>",
        unsafe_allow_html=True)

if st.button("With more than 300+ cats, we almost have a cat-birthday everyday! Click for party!😻"):
        #st.write('😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽 😹 🙀 😾 😿 😻 😺 😸 😽')
        st.balloons()


# Data load module- START

@st.cache
def load_data():
    data_cat_details = pd.read_excel(DATA_URL_NEW)
    data_cluster_geo = pd.read_csv(DATA_LAT_LON_URL)
    # data_cluster_geo.rename({'Cluster': 'USUAL SPOT'})

    # data.dropna(subset=['longitude', 'latitude'], inplace=True)
    # lowercase = lambda x: str(x).lower()
    #  data.rename(lowercase, axis='columns', inplace=True)
    data_cat_details['GENDER'].fillna('To be confirmed', inplace=True)
    data_cat_details['NAME'].fillna('NA', inplace=True)
    data_cat_details['ALSO SPOTTED IN'].fillna('-', inplace=True)
    data_cat_details['LAST UPDATED'].fillna('-', inplace=True)
    data_cat_details['REMARKS'].fillna('-', inplace=True)
    data_cat_details['MAIN COLOR'].fillna('Unknown', inplace=True)
    data_cat_details.drop(columns=['ALSO SPOTTED IN'], inplace=True)
    data_cat_details = data_cat_details.fillna('No')
    data_cat_details = pd.merge(left=data_cat_details, right=data_cluster_geo, how='left', left_on='USUAL SPOT',
                                right_on='Cluster')
    data_cat_details = data_cat_details.sort_values(by='USUAL SPOT', ascending=True)
    return data_cat_details


cat_details = load_data()

original_data = cat_details
data = cat_details
# Data load module- END


show_case_data = data.drop(columns=['LAT', 'LON'])


# Summary plot for counts - START

def summary_count(data):
    # Main title



    fig_count = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "indicator"}],
        ],
        horizontal_spacing=0, vertical_spacing=0
    )

    total_cat_count = len(data)
    total_tnr_done = len(data[data['TNR'] == 'Yes'])
    total_tnr_pending = len(data[data['TNR'] != 'Yes'])
    total_adopted = len(data[(data['ADOPTED'] == 'ADOPTED') | (data['ADOPTED'] == 'FOSTER HOME') | (data['ADOPTED'] == 'Yes')])

    fig_count.add_trace(
        go.Indicator(
            mode="number",
            value=total_cat_count,
            title="Total Cats",

        ),
        row=1, col=1

    )

    fig_count.add_trace(
        go.Indicator(
            mode="number",
            value=total_adopted,
            title="Adopted",
        ),
        row=1, col=2
    )

    fig_count.add_trace(
        go.Indicator(
            mode="number",
            value=total_tnr_done,
            title="TNR Done",
        ),
        row=2, col=1
    )

    fig_count.add_trace(
        go.Indicator(
            mode="number",
            value=total_tnr_pending,
            title="TNR Pending",
        ),
        row=2, col=2
    )

    fig_count.update_layout(template="plotly_dark", font_family="Arial", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_count, use_container_width=True)


# Summary plot for counts - END

# Gender information-START
def gender_count(data):
    st.subheader("It it a girl? A boy? It's a mystery! 😵")
    st.markdown('Did you know, it is not easy to identify the gender of kitten. '
                'We sometimes have to wait for the vet visit to get an idea')

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

    st.plotly_chart(fig_gender, use_container_width=True)


# Gender information-END


# Show TNR related data on map and hexagon layer-START

def tnr_count(data):
    #st.subheader("TNR Status")
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>TNR Status",
        unsafe_allow_html=True)
    st.markdown('TNR stands for: Trap Neutered Release. Use the dropdown to see the list')
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

    st.subheader('Map showing the the cluster with: %s ' % tnr_status)
    st.markdown('The height of the tower indicate the count of %s ' % tnr_status)

    midpoint = (np.average(data["LAT"]), np.average(data["LON"]))

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

        # tooltip={"html": "<b>Color Value:</b> {TNR}", "style": {"color": "white"}},
        #tooltip={"text": "Elevation: {elevationValue}"},
    ))
    # Show TNR related data on map and hexagon layer-END

    # Bar chart for cluster START
    st.subheader('Clusterwise distribution for: %s ' % tnr_status)

    fig_cluster_bar = px.bar(data_cluster,
                             x='Count',
                             y='USUAL SPOT',
                             # title='By Cluster',
                             barmode='stack',
                             orientation='h',
                             text='Count',

                             )
    st.plotly_chart(fig_cluster_bar, use_container_width=True)
    # Bar chart for cluster END

    # Table for cluster START
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>List of cats in the community with other details",
        unsafe_allow_html=True)

    #st.subheader("List of cats in the community with other details")
    st.markdown('Saw a cat you think is not in the list? You can look for photos here: ')
    # Feel free to search by Name, Cluster or Gender 😉""")
    cluster_select = st.selectbox(
        'Select the Cluster you want to view?',
        data['USUAL SPOT'].unique())

    selected_cluster = show_case_data[show_case_data['USUAL SPOT'] == cluster_select].sort_values(
        by=['USUAL SPOT'], ascending=False)
    st.write(selected_cluster)
    st.subheader("Explore More! Click on the sidebar >>> 👈")
    st.markdown('You can search for cats, adopt one, lookup volunteers, fosters, feed and do so many thing!!!')
    #menus_internal = ['Search For Cats', 'How can you Help', 'Volunteers']  # 'Report A Cat']
    # st.sidebar.header('MENU')
    #menu = st.radio('', menus_internal, key=123)
    # Table for cluster END
    st.markdown("<h2 style='text-align: center; color: #196F3D;'>Site is dedicated to our beloved Cluster G cat George."
                "He left us too soon!</h1>", unsafe_allow_html=True)


# Download the data- START

def download_data(original_data):
    csv = original_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
    st.markdown(href, unsafe_allow_html=True)


# Download the data- END

# Help related info START

def help_section():
    st.subheader("How can you help? Glad you asked")
    st.markdown("""

	- Be nice to them 🧡
	- If you cycle or scooter around 🚴, be mindful of the cats (they are very sneaky)
	- If you can, feed them with cat food (no human food please 🤒)
	- If you can help foster, please get in touch 🐈
	- Looking for adopting 👪? Ask us! We have kittens & cats looking for a lovely home.

	""")


# Help related info END


# Features info START
def future_features():
    st.subheader('**Coming soon features!**')
    st.markdown("Search for a particular cat and see their photo.")
    st.markdown("Don't see your community or cluster cat in the list? You can add it here.")


# Features info END

# Footer collage START
# image = Image.open('asset/img/collage.jpg')
# st.image(image, caption='',
#         use_column_width=True, clamp=True)


# Footer collage END


def cat_list(data):
    st.markdown(f"<div id='linkto_{'Search'}'></div>", unsafe_allow_html=True)
    st.subheader('Found or Find a Cat')
    lost_found_cluster_select = st.selectbox(
        'Which cluster did you find the cat?',
        data['USUAL SPOT'].unique())

    possible_cat = data[(data['USUAL SPOT'] == lost_found_cluster_select)]

    lost_found_color_select = st.selectbox(
        'What is the color of the cat you see? '
        'Dont worry about the detail, just select any of the major color?',
        possible_cat['MAIN COLOR'].unique())

    possible_cat = data[
        (data['USUAL SPOT'] == lost_found_cluster_select) & (
                data['MAIN COLOR'] == lost_found_color_select)].sort_values(
        by=['USUAL SPOT'], ascending=False)

    if len(possible_cat) == 0:
        possible_cat = 'No cat with matching descrpition found. Please check the photos'

    possible_cat = possible_cat.drop(columns=['CATID', 'PHOTO ID', 'LON', 'LAT', 'Cluster'])

    st.write((possible_cat))

    st.subheader('Does the cat look like any of the below?')
    st.markdown('If you are not sure, dont hesitate to post on our facebook group or whatsapp '
                'any of the below contact to get some help')

    for img, row in possible_cat.iterrows():
        if os.path.isfile('asset/img/cats/' + row['NAME'] + '.jpg'):
            st.markdown('Name: ' + row['NAME'] + '-' + row['REMARKS'])
            cat_img = Image.open(('asset/img/cats/' + row['NAME'] + '.jpg'))
            st.image(cat_img, caption=row['NAME'] + '-' + row['REMARKS'],
                     use_column_width=True)


if menu == 'Search For Cats':
    search.search_page(data)
elif menu == 'Info':
    'guide.from_author()'
elif menu == 'Volunteers':
    feederlist.show_feeder_data()
elif menu == 'How can you Help':
    helpus.help_section()
elif menu == 'Home':
    summary_count(data)
    tnr_count(data)
#elif menu =='Report A Cat':
#    reportacat.report_cat()