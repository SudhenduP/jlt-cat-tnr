import streamlit as st
import pandas as pd
from PIL import Image
import smtplib
from email.mime.text import MIMEText



def report_cat():
     st.set_option('deprecation.showfileUploaderEncoding', False)

     st.header('Note: This page is only to report a cat which is not part of our list. Please check the Search for Cat page before adding details here')

     st.subheader('Please enter Cluster')
     clustername = st.selectbox('', ['', 'A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z'])
     st.success(('You have entered Cluster : ' + clustername))


     st.subheader('Please select gender')
     gender = st.selectbox('', ['', 'Male', 'Female', 'Dont Know'])
     st.success(('You have entered : ' + gender))

     st.subheader('Please enter your mobile number (format: 0551234567)')
     mobile = st.text_input('')
     st.success(('You have entered: ' + mobile))

     st.subheader('Please upload an image of the cat')
     uploaded_file = st.file_uploader("", type=["jpg", "png"])
     if uploaded_file is not None:
          cat_image = Image.open(uploaded_file)
          #st.image(img_PIL)
          cat_image.save(r'test.1.png')
          st.success('File uploaded successfully')


     cat_input_data = [clustername, gender, mobile]
     cat_df = pd.DataFrame(cat_input_data)
     cat_df.to_csv('cat.csv')

report_cat()


# Import smtplib for the actual sending function


# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
