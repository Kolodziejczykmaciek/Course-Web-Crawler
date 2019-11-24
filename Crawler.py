import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
#url = "http://kt.agh.edu.pl/~matiolanski/website/"
#url = "https://www.ceneo.pl/70283264"


data = {'word1': 'perfumy', 'word2': 'lacoste', 'word3': 'czerwone', 'lowPrice': 50, 'highPrize': 200}


def search(**kwargs):

    ###     PREAERING A SEARCHED URL
    dane = []                   #przechwyt argumentow
    for key in kwargs:
        dane.append(kwargs[key])

    url = "https://www.ceneo.pl/;szukaj-"
    daneSize = len(dane)
    for val in range(daneSize-2):    #budowa linku
        if val==0:
            url += dane[val]
        else:
            url += "+" + dane[val]
    url += ";m" + str(dane[-2] ) + ";n" + str(dane[-1]) + ";basket;0112-0.htm" #gotowy reguest url
    print(url)

    ###     CREATING A REQUEST WITH URL AND PARSING THE RESPONSE
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ID_numbers = re.findall('(?:href="/)(\d{8})(?:###)', str(soup.find_all("a")))
    #ID_numbers containg searched numbers but they are replacing


    new_ID_numbers = []     #new list for not replacing products ID
    try:
        new_ID_numbers.append(ID_numbers[0])
    except IndexError:
        print("Cound not find anything!")       #in case no products were found
        return False

    for i in range(len(ID_numbers)):    #it fills the new_ID_numbers list with individual id products
        if i == len(ID_numbers)-1:
            break
        if (ID_numbers[i] != ID_numbers[i+1]):
            new_ID_numbers.append(ID_numbers[i+1])

    return new_ID_numbers           #fuction returns a ID products list

def get_info(product_ID):
    url = "https://www.ceneo.pl/" + str(product_ID) + ";0284-0;02511.htm" #only status 'dostępny' and sorded from the lowes price
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern_links = r'(?:btn-cta go-to-shop" href=")(.*)(?:"\starget)'
    pattern_opinion = r'(?:">)(.*)(?:\sopini[ie]</span>)'
    pattern_mark = r'(?:class="screen-reader-text">Ocena\s)(.*)(?:\s/\s5</span>)'
    links = re.findall(pattern_links, str(soup))
    mark = re.findall(pattern_mark, str(soup))
    opinion = re.findall(pattern_opinion, str(soup))
    print(len(links))
    print(mark)
    print(len(mark))

    print(opinion)
    print(len(opinion))





print(search(**data))
get_info(71624588)



