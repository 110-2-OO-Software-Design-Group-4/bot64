import os, math, string
from discord import Message

from libs.flag import MessageFlag

class Scanner:
    def __init__(self) -> None:
        pass

    def remove_punctuation(self, token):
        length = len(token)
        i = length - 1
        while token[i] in string.punctuation and i > 0:
            i -= 1
        return token[:i+1]
    def b_search_link(self, l, r, substring, sen_links, substrlen):
        if l <= r:
            mid = (l+r)//2
            #print(mid, len(sen_links))
            if sen_links[mid] == substring:
                return 100000.
            elif sen_links[mid] > substring:
                return self.b_search_link(l, mid-1, substring, sen_links, substrlen)
            elif sen_links[mid] < substring:
                return self.b_search_link(mid+1, r, substring, sen_links, substrlen)
        else:
            return 0.
        
    def b_search_word(self, l, r, substring, sen_words, substrlen):#二分搜敏感字詞，預設敏感詞已經經過排序
        if l <= r:
            mid = (l+r)//2
            token = substring[:min(substrlen,len(sen_words[mid]))]
            token = self.remove_punctuation(token)
            substring = self.remove_punctuation(substring)
            if sen_words[mid] == token:#如果子字串含有敏感詞則進一步判斷
                if len(substring) != len(token):
                    if not substring[len(token)].isalnum():#此行是避免如hello被誤判(因為hell是敏感詞)
                        return len(token) / 8 + 1. 
                else:
                    return len(token) / 8 + 1.
            if sen_words[mid] > substring:
                return self.b_search_word(l, mid-1, substring, sen_words, substrlen)
            elif sen_words[mid] < substring:
                return self.b_search_word(mid+1, r, substring, sen_words, substrlen)
        else:
            return 0.

    def scan(self, message: Message) -> MessageFlag:    
        # We assume both scanner.py and name.txt are in the same folder.
        # If such assumption does not hold, this would lead to failure. 
        directory = os.path.dirname(__file__)
        blackListFilePath1 = os.path.join(directory, 'name.txt')
        blackListFilePath2 = os.path.join(directory, 'link.txt')
        
        f_word = open(blackListFilePath1, 'r', encoding = 'utf-8')
        f_link = open(blackListFilePath2, 'r', encoding = 'utf-8')
        
        sen_words = f_word.read().split('\n')#切割出各個敏感詞
        sen_links = f_link.read().split('\n')
        
        Num_word = len(sen_words)#敏感詞總數
        Num_link = len(sen_links)
        
        text = message.content#要判斷的文字訊息
        N_char = len(text)#文字訊息長度
        
        judge = 0.
        judge1 = 0.
        
        for i in range(N_char):
            
            if not text[i].isalnum():
                continue
            if i != 0:
                if text[i-1].isalnum():
                    continue
            
            if N_char - i > 32:# 32 為 sensitive中最長的字串+1，如果name.txt有更新要改數字。此部分切出要判斷的子字串。
                substring1 = text[i:i+32].lower()
            else:
                substring1 = text[i:].lower()   
            substrlen1 = len(substring1)

            head = i
            tail = i
            
            while (tail != N_char):
                if text[tail] != ' ' and text[tail] != '\n':#連結為空白或換行符號之間的字串
                    tail += 1
                else:
                    break
                
            substring2 = text[head:tail]
            substrlen2 = len(substring2)

            tail = head
            while (tail != N_char):
                if text[tail].isalnum():
                    tail += 1
                else:
                    break
            substring3 = text[head:tail]
            substrlen3 = len(substring3)#字串三切割標點符號之間的字串

            judge1 = self.b_search_word(0, Num_word - 1, substring1, sen_words, substrlen1)#文字訊息首位，或前一位為空白則以其當字首切割子字串，用二分搜判斷敏感詞
            if(judge1 == 0.):
                judge1 += self.b_search_word(0, Num_word - 1, substring2, sen_words, substrlen2)#敏感字串三種字串切割類型都要檢查
            if(judge1 == 0.):
                judge1 += self.b_search_word(0, Num_word - 1, substring3, sen_words, substrlen3)
                
            judge += judge1
            judge += self.b_search_link(0, Num_link - 1, substring2, sen_links, substrlen2)#以相同訊息判斷釣魚連結

        Score = judge / math.log2(N_char + 6)
        
        Flag =  MessageFlag.Safe
        
        if Score != 0 and Score < 0.5:
            Flag = MessageFlag.Suspicious
            
        elif Score >= 0.5:
            Flag = MessageFlag.Malicious
            
        return Flag
