import requests
from os import getcwd

# clean ..\list.txt before running program

class Phishing:
    tiananmenSquareList = []

    def __init__(self):
        url = 'https://raw.githubusercontent.com/Dogino/Discord-Phishing-URLs/main/scam-urls.txt'
        r = requests.get(url)
        directory = getcwd()
        filename = directory + '\List.txt'
        f = open(filename, 'wb')
        f.write(r.content)
        f.close()

    def IsPhishingLink(self, msg):
        '''
        if message.author == bot.user:
            return
        content = message.content.split()
        print(content)
        for word in content:
            print("Loop iteration")
            if word.upper() in keywords:
                global keywords_met
                keywords_met += 1
        if keywords_met >= 3:
            channel = bot.get_channel(ID of a mod channel)
            await channel.send("<@ID of a role> nitro scam detected")
            keywords_met = 0
        '''
        directory = getcwd()
        filename = directory + '\List.txt'
        f = open(filename, 'r')

        if 'https://' in msg:
            for line in f.readlines():
                line = line.strip()
                if line in msg:
                    print("74147414")
                    return True

fish = Phishing()
fish.IsPhishingLink('https://1tvv.ru46546')
