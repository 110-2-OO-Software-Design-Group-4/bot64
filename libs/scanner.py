from discord import Message
from typing import Literal
import os

from libs.message_flag import MessageFlag

def binarysearch(l, r, substring, sen_words, substrlen):#二分搜敏感字詞，預設敏感詞已經經過排序
    if l <= r:
        mid = (l+r)//2
        token = substring[:min(substrlen,len(sen_words[mid]))]
        if sen_words[mid] == token:#如果子字串含有敏感詞則進一步判斷
            if len(substring) != len(token):
                if not substring[len(token)].isalnum():#此行是避免如hello被誤判(因為hell是敏感詞)
                    return True
            else:
                return True
        if sen_words[mid] > substring:
            return binarysearch(l, mid-1, substring, sen_words, substrlen)
        elif sen_words[mid] < substring:
            return binarysearch(mid+1, r, substring, sen_words, substrlen)
    else:
        return False

async def scanner(message: Message) -> Literal[MessageFlag.Safe, MessageFlag.Suspicious, MessageFlag.Malicious]:
    
    # We assume both scanner.py and name.txt are in the same folder.
    # If such assumption does not hold, this would lead to failure. 
    directory = os.path.dirname(__file__)
    blackListFilePath = os.path.join(directory, 'name.txt')
    f_sen = open(blackListFilePath, 'r')
    
    sen_words = f_sen.read().split('\n')#切割出各個敏感詞
    Num = len(sen_words)#敏感詞總數
    string = message.content#要判斷的文字訊息
    N_char = len(string)#文字訊息長度
    judge = False
    for i in range(N_char):
        substring = ''
        if(N_char - i > 28):# 28 為 sensitive中最長的字串+1，如果name.txt有更新或有加網址要改數字。此部分切出要判斷的子字串。
            substring = string[i:i+28].lower()
        else:
            substring = string[i:].lower()
        substrlen = len(substring)
        if i == 0:
            judge = binarysearch(0, Num - 1, substring, sen_words, substrlen)#文字訊息首位，或前一位為空白則以其當字首切割子字串，用二分搜判斷敏感詞
            
        elif string[i-1] == ' ' or string[i-1] == '\n':
            judge = binarysearch(0, Num - 1, substring, sen_words, substrlen)
            
        if judge:
            break
    Flag =  MessageFlag.Safe
    if judge:#如果有敏感詞則為惡意訊息,反之則為安全訊息
        Flag = MessageFlag.Malicious
    return Flag