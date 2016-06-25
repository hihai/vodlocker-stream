from bs4 import BeautifulSoup
import requests
from time import sleep
import sys
import re
import os


def get_server(link):
    """get form into a dict, post it and parse the server afterwards"""
    link += "?imhuman=Proceed+to+video"
    header = {"Referer": link,
                      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    post_values = {}
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "html.parser")

    for i in soup.find_all("form"):
        for text in i.find_all("input"):
            post_values[str(text.get("name"))] = text.get("value")
        try:
            del post_values["k"]
        except KeyError:
            print (post_values)

    sleep(5)

    new = requests.post(link, data=post_values, headers=header)
    soup = BeautifulSoup(new.text, "html.parser")
    html= soup.find(id="player_code")

    for i in html.find_all("script"):
        for text in i:
            asd = text

    asd = asd.split("\n")
    server = asd[2].strip()

    server = "".join(re.findall(r'\"(.*?)\"', server))

    open_vlc(server)


def search():
    """parse the first 20 results of titles and links into 2 lists"""
    name = " ".join(sys.argv[1:])
    print (name)
    html = requests.get("http://vodlocker.com/?op=search&k=%s&user=" %(name))
    soup = BeautifulSoup(html.text, "html.parser")
    link_list = []
    name_list = []
    for i in soup.find_all("table", class_="vlist"):
        for text in i.find_all("div", class_="link"):
            link_list.append(text.find("a").get("href"))
            name_list.append(text.text.strip())

    choose(name_list, link_list)


def choose(name_list, link_list):
    """print list of the avaible 20 streams"""
    for l, k in enumerate(name_list):
        print (l, k)
    number = int(input("choose stream by number: "))

    get_server(link_list[number])


def open_vlc(server):
    """start vlc stream"""
    stream = "vlc " + server
    os.system(stream)

search()
