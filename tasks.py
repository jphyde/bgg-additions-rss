from celery import Celery

import requests
from bs4 import BeautifulSoup
import json

app = Celery("tasks")  # defining the app name to be used in our flag


@app.task
def save_function(boardgame_list):
    with open("boardgames.txt", "w") as outfile:
        json.dump(boardgame_list, outfile)


@app.task
def bggadditions_rss():
    boardgame_list = []

    try:
        r = requests.get(
            "https://boardgamegeek.com/recentadditions/rss?subdomain=&infilters%5B0%5D=thing&domain=boardgame"
        )
        soup = BeautifulSoup(r.content, features="xml")

        boardgames = soup.findAll("item")

        for bg in boardgames:
            link = bg.find("link").text
            guid = bg.find("guid").text
            published = bg.find("pubDate").text

            boardgame = {"link": link, "guid": guid, "published": published}
            boardgame_list.append(boardgame)

        return save_function(boardgame_list)
    except Exception as e:
        print("The scraping job failed. See exception: ")
        print(e)
