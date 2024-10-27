import requests
from bs4 import BeautifulSoup
import lxml


def get_weather():
    url = "https://www.tianqi.com/shanghai/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    now_temp = soup.find_all(class_="now")
    temperature:str = now_temp[0].b.string + now_temp[0].i.string

    class_shidu = soup.find_all(class_="shidu")
    wind:str = class_shidu[0].find_all('b')[1].string[3:]
    return temperature,wind
