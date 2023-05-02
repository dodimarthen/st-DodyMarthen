import requests
import time

# cityname = input("Input the city: ").lower()
# # Replace YOUR_API_KEY with your actual API key
# url = f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=cac9a33d270ffd14be28239cd38916c8"
# response = requests.get(url).json()
# print(response)


# # weather = response['weather'][0]['main']
# temp_fix= response['main']['temp']
# temp_fixed = temp_fix-273.15
# # tempmin = response['main']['temp_min']
# # tempmax = response['main']['temp_max']
# print(f"temp is: ", int(temp_fixed),"°C")
# print(f"temp min is: ",tempmin)
# print(f"temp max is: ",tempmax)
# # if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("Failed to retrieve data from the API.")

# while True:
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("API is working!")
#         break
#     else:
#         print("API is not responding. Waiting 20 seconds before trying again...")
#         time.sleep(20)

import requests
from time import sleep
from tqdm import tqdm


class Weather:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_temperature(self, cityname):
        url = f"{self.base_url}?q={cityname}&appid={self.api_key}"
        response = requests.get(url).json()
        temperature = response['main']['temp']
        weather = response['weather'][0]['main']
        return temperature, weather
    
    # def ReadJSON(self):
    #     cityname=input("input the city: ").lower()
    #     url = f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=cac9a33d270ffd14be28239cd38916c8"
    #     self.response = requests.get(url).json()

    # def GetTemperature(self):
    #     weather = self.response['weather'][0]['main']
    #     temp = self.response['main']['temp']
    #     print(weather)
    #     print(temp, "° F")
    
    def ConvertTemperature(self):
        temp = self.response['main']['temp']
        temp = temp - 273.15
        print("Your temperature is:",int(temp), "°C")
    



weather = Weather(api_key="cac9a33d270ffd14be28239cd38916c8")
temp1 = weather.get_temperature("Depok")
print(temp1)

# for i in tqdm(range(3600)):
#     sleep(1)

# temp2 = weather.get_temperature("Jakarta")

# delta = temp2-temp1
# print(f"Temperature change: {delta} °C")

# weather.ReadJSON()
# weather.GetTemperature()
# weather.ConvertTemperature()