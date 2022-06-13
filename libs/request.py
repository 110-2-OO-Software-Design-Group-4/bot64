import requests
from os import getcwd

url = 'https://raw.githubusercontent.com/Dogino/Discord-Phishing-URLs/main/scam-urls.txt'
r = requests.get(url)
directory = getcwd()
filename = directory + '\list.txt'
f = open(filename, 'wb')
f.write(r.content)
f.close()
