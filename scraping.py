import requests
from bs4 import BeautifulSoup

def bggadditions_rss():
    boardgame_list = []

    try:
        r = requests.get('https://boardgamegeek.com/recentadditions/rss?subdomain=&infilters%5B0%5D=thing&domain=boardgame')
        soup = BeautifulSoup(r.content, features='xml')
        
        boardgames = soup.findAll('item')

        for bg in boardgames:
            link = bg.find('link').text
            guid = bg.find('guid').text
            published = bg.find('pubDate').text

            boardgame = {
                'link': link,
                'guid': guid,
                'published': published
            }
            boardgame_list.append(boardgame)

        return print(boardgame_list)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)

print('Starting scraping')
bggadditions_rss()
print('Finished scraping')