import pydeck as pdk
import pandas as pd
import streamlit as st
import numpy as np
import streamlit.components.v1 as components


def github_gist(gist_creator, gist_id, height=600, scrolling=True):
    components.html(
        f"""
	  <script src="https://gist.github.com/{gist_creator}/{gist_id}.js">
	  </script>
	""",
        height=height,
        scrolling=scrolling,
    )


# Data from OpenStreetMap, accessed via osmpy
DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/biergartens.json"
DATA_LAT_LON_URL = (r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\data\Cluster-GeoData.csv')
DATA_URL_NEW = (r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\data\JLT_CatLogs.xlsx')
#ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"
ICON_URL = "https://raw.githubusercontent.com/SudhenduP/temproraryfiles/master/person.png"
icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 150,
    "height": 150,
    "anchorY": 150,
}

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

    data_cat_details = data_cat_details.fillna('No')
    data_cat_details = pd.merge(left=data_cat_details, right=data_cluster_geo, how='left', left_on='USUAL SPOT',
                                right_on='Cluster')
    data_cat_details = data_cat_details.sort_values(by='USUAL SPOT', ascending=True)
    return data_cat_details


data = load_data()

data["icon_data"] = None
for i in data.index:
    data["icon_data"][i] = icon_data

view_state = pdk.data_utils.compute_view(data[["LON", "LAT"]], 0.1)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=data,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["LON", "LAT"],
    pickable=True,
)

r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{tags}"})
r.to_html("1icon_layer.html")


st.markdown('The height of the tower indicate the count')

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
            type="IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position=["LON", "LAT"],
            pickable=True,
        ),

    ],

    # tooltip={"html": "<b>Color Value:</b> {TNR}", "style": {"color": "white"}},
    tooltip={"text": "Elevation: {elevationValue}"},
))


st.markdown("""
	Be nice to the communty cats 🧡

	If you cycle or scooter around 🚴, be mindful of the cats (they are very sneaky)

	If you can, feed them with cat food (no human food please 🤒)

	If you can help foster, please get in touch 🐈

	Looking for adopting 👪? Ask us! We have kittens & cats looking for a lovely home. Please click here: [whatsapp](https://api.whatsapp.com/send?phone=971551283234)

	Found a cat? Please check on our 'Search Our Cats' page. Still think you found a new cat? Great!! Please fill this [form](https://pandeysudhendu.typeform.com/to/ybosfUSt)
	""")