import os
from db import db
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from multiprocessing import Process
from  threading import Thread
from time import sleep as sl
import urllib

path = "/home/demir/Desktop/BitirmeProjesi/getData/data/"

cursor, conn = db()

web_sites = ["https://www.hepsiburada.com/erkek-giyim-urunleri-c-60004641?sayfa=","https://www.hepsiburada.com/bayan-giyim-urunleri-c-60004640?sayfa="]

def productThread(productLink):

    try:

        request = Request(productLink, headers={"User-Agent":"XYZ/3.0"})
        webpage = urlopen(request).read()

        soup = BeautifulSoup(webpage,"html.parser")

        price = soup.find("span", { "id" : "offering-price" }).text.split(" ")
        price = price[0].split("\n")[1]+" TL"

        productName = soup.find("span", { "class" : "product-name" }).text


        # add product database
        cursor.execute('INSERT INTO tbl_product(pr_name, pr_url, pr_store, pr_price) VALUES(%s, %s, %s, %s) returning pr_id',(productName,productLink,2,price,))
        conn.commit()
        data = cursor.fetchone()

        print("Pr Id: ", data[0])

        images = soup.findAll("img", {"class":"product-image"})

    except:

        return

    for i in images:

        try:
            imageLink = i["data-src"]

        except:

            continue

        try:

            # add image database
            cursor.execute('INSERT INTO tbl_product_images(pr_id, img_url) VALUES(%s, %s) returning img_id',(data[0],imageLink,))
            dataImg = cursor.fetchone()
        
            urllib.request.urlretrieve(imageLink, path+str(dataImg[0])+".png")

            print(path+str(dataImg[0])+".png")

        except:

            pass

def pageProcess(soup):

    productDiv = soup.findAll("div", { "class" : "moria-ProductCard-joawUM" })

    for i in productDiv:

        productHref = i.find('a', href=True)

        productLink = "https://www.hepsiburada.com"+productHref['href']

        productThread(productLink)
        
def main():

    for web in web_sites:

        for i in range(1,60):

            web_site = web+str(i)

            request = Request(web_site, headers={"User-Agent":"XYZ/3.0"})
            webpage = urlopen(request).read()

            soup = BeautifulSoup(webpage,"html.parser")

            pageProcess(soup)



if __name__=="__main__":

    main()