import os
from db import db
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Process
from  threading import Thread
from time import sleep as sl

cursor, conn = db()

web_site = "https://www.trendyol.com/sr?wg=1,2,3&wb=38,859,37,41,43,33,101990,44,160,136,430,257,230,124,263,108455,108412,111572&wc=82&pi="


def productThread(productLink):

    request = Request(productLink, headers={"User-Agent":"XYZ/3.0"})
    webpage = urlopen(request).read()

    soup = BeautifulSoup(webpage,"html.parser")

    price = soup.find("span", { "class" : "prc-dsc" }).text

    productName = soup.find("h1", { "class" : "pr-new-br" })
    brand = productName.find('a', href=True).text
    productName = productName.find('span')
    productName = brand + productName.text

    images = soup.find("div", { "class" : "styles-module_slider__o0fqa" })

    images = images.find_all("img")

    imagesLink = []

    for i in images:

        imagesLink.append(i["src"].replace("mnresize/128/192/",""))

    category = productName.split(" ")
    category = category[len(category)-2]

    print(productName)
    

def pageProcess(soup):
    
    productDiv = soup.findAll("div", { "class" : "p-card-chldrn-cntnr card-border" })

    for i in productDiv:

        productHref = i.find('a', href=True)


        productLink = "https://www.trendyol.com"+productHref['href']
        
        t = Thread(target=productThread, args=(productLink,))
        t.start()
        t.join(0.01)


def main():

    for i in range(1,209):

        web_site_temp = web_site+str(i)

        request = Request(web_site_temp, headers={"User-Agent":"XYZ/3.0"})
        webpage = urlopen(request).read()

        soup = BeautifulSoup(webpage,"html.parser")

        p = Process(target=pageProcess, args=(soup,))
        p.start()
        p.join(0.01)



if __name__=="__main__":

    main()