#import library- will clean later

import streamlit as st
from PIL import Image
import os

def search_page(data):
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Found and Search Section
    # st.markdown(f"<div id='linkto_{'Search'}'></div>", unsafe_allow_html=True)
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

       # st.write(os.getcwd())
       # st.write('/sset/img/cluster-wise-photos/' + row['USUAL SPOT'].split(' ')[1] + '/'+ row['NAME'] + '.jpg')
        if os.path.isfile('asset/img/cluster-wise-photos/' + row['USUAL SPOT'].split(' ')[1] + '/'+ row['NAME'] + '.jpg'):
        #    st.write('asset/img/cluster-wise-photos/' + row['USUAL SPOT'].split(' ')[1] + '/' + row['NAME'] + '.jpg')

            st.markdown('Name: ' + row['NAME'] + '-' + row['REMARKS'])
            cat_img = Image.open(('asset/img/cluster-wise-photos/' + row['USUAL SPOT'].split(' ')[1] + '/' + row['NAME'] + '.jpg'))
            st.image(cat_img, caption=row['NAME'] + '-' + row['REMARKS'],
                     use_column_width=True)

