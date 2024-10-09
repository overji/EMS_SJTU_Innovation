import requests
from lxml import etree


def get_weather():
    return "",""
    url = "https://www.tianqishi.com/shanghai.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', }
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    outside_temperature = tree.xpath('//div[@class="ltlTemperature"]//b')[0].text
    datas = tree.xpath('//ul[@class="mt"]//li')
    values = tree.xpath('//ul[@class="mt"]//li//span')
    return outside_temperature,values[2].text