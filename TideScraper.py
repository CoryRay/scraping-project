import requests
import re

class TideScraper():

    def get_url_data(city_url: str):
        html = requests.get(city_url)
        data = html.text

        pattern = re.compile(r"window\.FCGON = (.+);")
        # the line with window.FCGON has all the data!
        return pattern.findall(data)
