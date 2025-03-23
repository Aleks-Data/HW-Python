# Напишите программу, которая запрашивает у пользователя URL-адрес веб-страницы,
# спользует библиотеку Beautiful Soup для парсинга HTML и выводит список всех ссылок
# на странице.

import requests
from bs4 import BeautifulSoup


def get_links(url):
    html = requests.get("https://"+url).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    for i in links:
        print(i["href"])


address = input("Введите адрес страницы: ")
get_links(address)
