from matplotlib.pyplot import text
import requests
from os import getcwd

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
        ##print(Phishing.tiananmenSquareList[-1])

