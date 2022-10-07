import os
from db import db
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep as sl
import urllib

cursor, conn = db()

web_site = "https://www.trendyol.com/sr?wg=1,2,3&wb=38,859,37,41,43,33,101990,44,160,136,430,257,230,124,263,108455,108412,111572&wc=82&pi="
path = "/home/demir/Desktop/BitirmeProjesi/getData/data/"

def productThread(productLink):

    try:

        request = Request(productLink, headers={"User-Agent":"XYZ/3.0"})
        webpage = urlopen(request).read()

        soup = BeautifulSoup(webpage,"html.parser")

        price = soup.find("span", { "class" : "prc-dsc" }).text

        productName = soup.find("h1", { "class" : "pr-new-br" })
        brand = productName.find('a', href=True).text
        productName = productName.find('span')
        productName = brand + productName.text

        # add product database
        cursor.execute('INSERT INTO tbl_product(pr_name, pr_url, pr_store, pr_price) VALUES(%s, %s, %s, %s) returning pr_id',(productName,productLink,1,price,))
        conn.commit()
        data = cursor.fetchone()

        images = soup.find("div", { "class" : "styles-module_slider__o0fqa" })
        images = images.find_all("img")

        print("Pr Id: ", data[0])

    except:

        return

    for i in images:

        try:

            imageLink = i["src"].replace("mnresize/128/192/","")

            # add image database
            cursor.execute('INSERT INTO tbl_product_images(pr_id, img_url) VALUES(%s, %s) returning img_id',(data[0],imageLink,))
            dataImg = cursor.fetchone()                
            urllib.request.urlretrieve(imageLink, path+str(dataImg[0])+".png")

            print(path+str(dataImg[0])+".png")

        except:

            pass
            
def pageProcess(soup):
    
    productDiv = soup.findAll("div", { "class" : "p-card-chldrn-cntnr card-border" })

    for i in productDiv:

        productHref = i.find('a', href=True)

        productLink = "https://www.trendyol.com"+productHref['href']
        
        productThread(productLink)

def main():

    for i in range(1,150):

        web_site_temp = web_site+str(i)

        request = Request(web_site_temp, headers={"User-Agent":"XYZ/3.0"})
        webpage = urlopen(request).read()

        soup = BeautifulSoup(webpage,"html.parser")

        pageProcess(soup)

if __name__=="__main__":

    main()