import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
import plotly.express as px
import pyttsx3
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
from time import sleep
from tqdm import tqdm
import folium
import altair as alt
import numpy as np
from streamlit_folium import st_folium
import streamlit_ace
import re

#BACKGROUND-IMAGE
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.pexels.com/photos/4862892/pexels-photo-4862892.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
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
st.title("Greeting our visitor!")
with st.container():
    result = st.button("Greetings!")
    if result:
        if title:
            with st.spinner('Wait for it...'):
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


#Badge
st.subheader('Badge')
with st.expander('First badge'):
    image = Image.open('Python_for_Data_Sci_and_AI_Foundational.png')
    st.image(image, caption='Python for Data Science, AI', width=290)
    verification_link = "https://www.credly.com/badges/74497ea2-905b-4e72-9286-4d61c9167ac1/public_url"
    markdown_string = f"**[View Verification Link]({verification_link})**"
    st.markdown(markdown_string)
with st.expander('Second badge'):
    image = Image.open('it_support_badge.png')
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
        Shakemap = data['Infogempa']['gempa']['Shakemap']
        latitude, longitude = Coordinates.split(",")
        Magnitudo = ("{} M".format(Magnitudo))
        st.write('Tanggal kejadian : ', event_time)
        st.write('Lokasi gempa : ', lokasi)
        st.write("Magnitudo Gempa : ", Magnitudo)
        st.write("Kedalaman : ", Kedalaman)
        st.write("Potensi : ",Potensi) 
        st.write("Latitude : ", latitude)
        st.write("Longitude : ", longitude)
        
    else:
        st.error("Failed to get Shakemap from the API.")
        st.write("Data Source : DataterbukaBMKG")
        st.success('JSON is working!', icon="✅")


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

#Barchart
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

#WeatherChecker
st.subheader("Check the Temperature on your city: ")


#CallingWeatherResponseFromAPI
class Weather:
    def __init__(self, api_key):
        self.api_key=api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_temperature(self, cityname):
        url = f"{self.base_url}?q={cityname}&appid={self.api_key}"
        try:
            response = requests.get(url).json()
            temperature = response['main']['temp']
            weather = response['weather'][0]['main']
            humidity = response['main']['humidity']
            windspeed = response['wind']['speed']
            return temperature, weather, humidity, windspeed
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
        except KeyError:
            st.error(f"City '{cityname}' not found.")
            return None
        except:
            st.error("An error occurred. Please try again later.")
            return None
    def get_icon(self, response):
        icon_id = response['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/{icon_id}.png'.format(icon=icon_id)
        return url
        
api_key="cac9a33d270ffd14be28239cd38916c8"

#WeatherIcon
Thunderstorm = "https://cdn.iconscout.com/icon/free/png-512/free-rain-3617452-3023677.png?f=avif&w=512"
Drizzle = "https://cdn.iconscout.com/icon/free/png-512/free-drizzle-19-445596.png?f=avif&w=512"
Rain = "https://cdn.iconscout.com/icon/premium/png-512-thumb/rain-323-532294.png?f=avif&w=512"
Snow = "https://cdn.iconscout.com/icon/free/png-512/free-snow-414-445591.png?f=avif&w=512"
Clouds = "https://cdn.iconscout.com/icon/free/png-512/free-cloudy-2739825-2271155.png?f=avif&w=512"
Clear_sky = "https://cdn.iconscout.com/icon/free/png-512/free-weather-1656157-1407896.png?f=avif&w=512"
Mist = "https://img.icons8.com/?size=512&id=5JFKFoWQfT74&format=png"
Fog = "https://cdn.iconscout.com/icon/premium/png-512-thumb/foggy-weather-532284.png?f=avif&w=512"
Tornado = "https://cdn.iconscout.com/icon/free/png-512/free-tornado-2363202-1972081.png?f=avif&w=512"
#----- Source : https://iconscout.com/ -----#
#DisplayWeather
cityname= st.text_input("Insert your City below: ")
if cityname:
    if re.match("^[a-zA-Z ]*$", cityname):
        weather = Weather(api_key)
        temperature, weather_type, humidity, windspeed = weather.get_temperature(cityname)
        if temperature is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Temperature ({weather_type})", f"{int(temperature-273.15):.2f}°C")
            if weather_type == "Clouds":
                col1.image(Clouds, width=90)
            elif weather_type == "Thunderstorm":
                col1.image(Thunderstorm, width=80)
            elif weather_type == "Drizzle":
                col1.image(Drizzle, width=80)
            elif weather_type == "Rain":
                col1.image(Rain, width=80)
            elif weather_type == "Snow":
                col1.image(Snow, width=110)
            elif weather_type == "Clear":
                col1.image(Clear_sky, width=80)
            elif weather_type == "Mist" or "Smoke" or "Haze" or "Dust" or "Fog":
                col1.image(Fog, width=70)
            
            col2.metric("Humidity",f"{humidity}%")
            col3.metric("Wind",f"{windspeed} Mph")
            # col3.text({weather_type})
            
        else:
            st.error(f"City '{cityname}' not found.")
    else:
        st.error("Please insert a valid city name (letters and spaces only)")
else:
    st.warning("Please insert your city")



#QUIZ GAME
st.subheader('Quiz Game')
with st.expander("Quiz 1"):
    st.write("1. What does RAM stand for?\n")
    st.write("\n")
    a = st.checkbox("A . Random Access Memory")
    b = st.checkbox("B.  Ransom Access Memory")
    if a:
        st.success("Good job!")
    elif b:
        st.error("Wrong Answer!")
with st.expander("Quiz 2"):
    st.write("2. Who is the president of Russia?")
    st.write("\n")
    a = st.checkbox("A. Donald Trumph")
    b = st.checkbox("B. John F. Kennedy")
    c = st.checkbox("C. Vladimir Putin")
    if a:
        st.error("Incorrect!")
    elif b:
        st.error("Almost Correct!")
    elif c:
        st.success("Correct!")
    else:
        st.warning("This question only contain one answer")


#Curriculum Vitae
st.subheader('Curriculum Vitae of Dody Marthen')
with open("CV_DodyMarthen.pdf", "rb") as file_pdf:
    PDFbyte = file_pdf.read()
st.download_button(label="Download",
                   data=PDFbyte,
                   file_name="CV_DodyMarthen.pdf",
                   mime='application')

