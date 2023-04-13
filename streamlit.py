import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
import plotly.express as px
import pyttsx3
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import folium
import altair as alt
import numpy as np
from streamlit_folium import st_folium

#BACKGROUND-IMAGE
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.pexels.com/photos/11838503/pexels-photo-11838503.jpeg");
background-size: cover;
background-position: center;
}
</style>"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# #WelcomeAnimation
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_url = "https://assets2.lottiefiles.com/packages/lf20_dfvrnyjk.json"
# lottie = load_lottieurl(lottie_url)

# st_lottie(
#     lottie,
#     speed=1,
#     key=None,
#     quality="low",
#     height=250,
#     width=None,
# )


title = st.text_input('Insert your name here : ')
#VoiceWelcome
def VoiceWelcome():
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.say("Hello, welcome"+title+", This simple website was created by Dody Marthen using python and streamlit. This website was created to increase learning about python and add to the portfolio. Some of the information you need about Dody Marthen is below, please scroll down to find out the contact person listed on this website")
    engine.runAndWait()


st.title("Greeting our visitor!")
with st.container():
    result = st.button("Greetings!")
    if result:
        if title:
            with st.spinner('Wait for it...'):
                st.success('Done!')
                VoiceWelcome()
                
            st.write("Halo " +title+ ", Welcome aboard!")
            st.snow()
        else:
            # st.write("Insert your name, please!")
            st.error('Insert your name, please!')


#Displaying image and about me
image = Image.open('me_green.jpg')
# Convert the image to a square by cropping it
width, height = image.size
size = min(width, height)
left = (width - size) / 2
top = (height - size) / 2
right = (width + size) / 2
bottom = (height + size) / 2
image = image.crop((left, top, right, bottom))

# Create a new image with a circular mask
mask = Image.new("L", image.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, size, size), fill=255)
image.putalpha(mask)

# Display the circular image
st.image(image, caption="Me, myself, and i", width=250)



#About
st.subheader('About Me')
with st.expander("_click here!_"):
    st.write("Hi, i'm graduated from Universitas Gunadarma in 2020 majoring in Information System.\nI am currently still working at PT Mindotama Avia Teknik as a system engineer and PMO. \nI was responsible to carry out maintenance of the Indonesian seismograph network 1 (INATEWS). Analyzing and solving problems on hardware components is one of the activities that I like.\n I helped prepare technical report documents and administrative reports when seconded to the PMO division to be submitted to clients. \nI am very happy to be entrusted with traveling on domestic business. I get to know a new environment, new people, new culture. Scroll down to find out the areas I've visited.")

#Domestic Business Trip
# st.subheader('Domestic Business Trip')
# with st.expander("Dataframe"):
#     df = pd.read_excel('test.xlsx')
#     st.table(df)

# with st.expander("Map Visualization"):
#     st.caption("Locations I've visited show blue dots")
#     fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', zoom=3)
#     fig.update_layout(mapbox_style="carto-positron")
#     fig.update_layout(margin={"r":0,"t":1,"l":0,"b":0})
#     st.plotly_chart(fig)

#Badge
st.subheader('Badge')
with st.expander('First badge'):
    image = Image.open('Python_for_Data_Sci_and_AI_Foundational.PNG')
    st.image(image, caption='Python for Data Science, AI', width=290)
    verification_link = "https://www.credly.com/badges/74497ea2-905b-4e72-9286-4d61c9167ac1/public_url"
    markdown_string = f"**[View Verification Link]({verification_link})**"
    st.markdown(markdown_string)
with st.expander('Second badge'):
    image = Image.open('it_support_badge.PNG')
    st.image(image, caption='IT Support', width=340)
    verification_link = "https://www.credly.com/badges/87e060a3-5dbc-4922-953c-a2c35e79a715/public_url "
    markdown_string = f"**[View Verification Link]({verification_link})**"
    st.markdown(markdown_string)

    
#Skills
st.subheader('Skills')
with st.expander("My Skills"):
    col1, col2 = st.columns(2)
    with col1:
        st.write('- Python')
        st.write('- MySQL')
    with col2:
        st.write('- SQL Server Management Studio')
        st.write('- Networking')

#Info Gempa Indonesia

st.subheader('Monitoring Gempa Indonesia')
with st.expander('Live Earthquake'):
    container = st.container()
    url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        event_time = data['Infogempa']['gempa']['Tanggal']
        lokasi = data['Infogempa']['gempa']['Wilayah']
        Magnitudo = data['Infogempa']['gempa']['Magnitude']
        Kedalaman = data['Infogempa']['gempa']['Kedalaman']
        Coordinates = data['Infogempa']['gempa']['Coordinates']
        Potensi = data['Infogempa']['gempa']['Potensi']
        latitude, longitude = Coordinates.split(",")
        Magnitudo = ("{} M".format(Magnitudo))
        st.write('Tanggal kejadian : ', event_time)
        st.write('Lokasi gempa : ', lokasi)
        st.write("Magnitudo Gempa : ", Magnitudo)
        st.write("Kedalaman : ", Kedalaman)
        st.write("Potensi : ",Potensi) 
        st.write("Latitude : ", latitude)
        st.write("Longitude : ", longitude)
        st.write("Data Source : DataterbukaBMKG")
        st.success('JSON is working!', icon="✅")
    else:
        st.error("Failed to get data from the API.")

st.subheader('Earthquake Map')
# Magnitudo = Magnitudo.replace("M",'')

m = folium.Map(location= [latitude, longitude], zoom_start = 7, tiles="OpenStreetMap")
tooltip = "Details"
popup_text = f"Magnitudo: {Magnitudo}<br>Tanggal: {event_time}"
popup = folium.Popup(popup_text, max_width=200)
folium.Marker(
    [latitude, longitude],
    tooltip = tooltip,
    popup = popup,
    icon = folium.Icon(color="red", icon="info-sign")
    
    ).add_to(m)

st_data = st_folium(m, width=725)


st.subheader('15 Earthquakes of Indonesia (Magnitudo >= 5.0 M)')
url = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
response = requests.get(url)
if response.status_code == 200:
    data_json = response.json()
    df = pd.DataFrame.from_records(data_json["Infogempa"]["gempa"])
    df = df[["Tanggal", "Jam", "Lintang", "Bujur", "Magnitude", "Kedalaman", "Wilayah", "Potensi"]]
    st.session_state.df = df
    st.dataframe(df.style.highlight_max(color = 'red', axis=0, subset=["Magnitude"]))
    st.success("Response Status OK")
else:
    st.error("Response Status Error")

st.subheader('Visualization')
if 'df' not in st.session_state:
    st.warning("Load the data first!")
else:
    fig = px.bar(df, x='Magnitude', y='Kedalaman')
    fig.update_layout(title='15 Earthquakes of Indonesia (Magnitude >= 5.0 M)',
                      xaxis_title='Magnitude (M)', yaxis_title='Depth (km)',
                      title_font=dict(size=20),
                      font=dict(size=14),
                      coloraxis_colorbar=dict(title='Magnitude'),
                      yaxis_range=[df['Kedalaman'].min(), df['Kedalaman'].max()])
    st.plotly_chart(fig)

st.subheader('Curriculum Vitae of Dody Marthen')
with open("CV_DodyMarthen.pdf", "rb") as file_pdf:
    PDFbyte = file_pdf.read()
st.download_button(label="Download",
                   data=PDFbyte,
                   file_name="CV_DodyMarthen.pdf",
                   mime='application')

st.subheader('')