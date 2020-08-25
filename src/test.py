import streamlit as st

link_number = st.selectbox('Select appropiate section',( '10', '30'))

#link_number = st.number_input("What subheading do you want to go to?", value=50)

st.markdown(f"<a href='#linkto_{link_number}'>Link to {link_number}</a>", unsafe_allow_html=True)
st.markdown(f"<a href='#linkto_{link_number}'>Link to {link_number}</a>", unsafe_allow_html=True)

for i in range(100):
    st.markdown(f"<div id='linkto_{i}'></div>", unsafe_allow_html=True)
    st.subheader(f"Subtitle {i}")
    st.write(f"I am a thing {i}")