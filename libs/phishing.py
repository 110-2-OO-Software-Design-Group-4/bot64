import requests

# clean ..\list.txt before running program

class Phishing:
    tiananmenSquareList = []

    def __init__(self):
        if len(Phishing.tiananmenSquareList) == 0:
            Phishing.fetch()
        
    @staticmethod
    def fetch():
        url = 'https://raw.githubusercontent.com/Dogino/Discord-Phishing-URLs/main/scam-urls.txt'
        r = requests.get(url)
        Phishing.tiananmenSquareList = r.text.split('\n')
        print('Successfully fetched latest phishing links at ' + url)

