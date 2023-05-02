from main import Weather
import unittest

api_key = "cac9a33d270ffd14be28239cd38916c8"
weather = Weather(api_key)

class TestWeather(unittest.TestCase):
    
    def test_get_temperature(self):
        result = weather.get_temperature("Jogja")
        f'{result}'
    
    def test_get_temperature_upper(self):
        result = weather.get_temperature("JOGJA")
        f'{result}'
    
    def test_get_temperature_intejer(self):
        result = weather.get_temperature("845385")
        f'{result}'

    def test_get_temperature_mixingintestring(self):
        result = weather.get_temperature("sadha8312467")
        f'{result}'

    def test_get_temperature_empty(self):
        result = weather.get_temperature(" ")
        f'{result}'
if __name__ == '__main__':
    unittest.main()

# start_time = time.time()
# result = weather.get_temperature("Lampung")
# print(result)
# end_time = time.time()
# elapsed = end_time - start_time
# print(f"Execution time: {elapsed} seconds")