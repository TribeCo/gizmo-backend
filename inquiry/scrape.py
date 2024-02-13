import requests
from bs4 import BeautifulSoup
import chardet

#You can use the commented codes to test the code

#amazon

def amazon(url):
    out_put={}
    try:
        page=requests.get(url)
        # print(page.text)
        if page.status_code == 200:
            encoding = chardet.detect(page.content)["encoding"]
            html = page.content.decode(encoding)
            soup = BeautifulSoup(html, 'html.parser')   

            #product name
            title=soup.find('title')
            if title:
                product_name=title.text[12:]
                out_put["product name"] = product_name
                # print(f"product name:{product_name}") 
            else:
                print('title tag not found')
            
            #img
            div_tag = soup.find('div', id='imgTagWrapperId', class_='imgTagWrapper')
            if div_tag:
                img_tag = div_tag.find('img')
                if img_tag:
                    out_put["img src"] = img_tag['src']
                    # print(f"img src:{img_tag['src']}")  #img src
            else:
                print('Div tag not found')

            #price
            price_tag = soup.find('span', class_='a-offscreen')
            if price_tag:
                out_put["price"] = price_tag.text
                # print(f"price:{price_tag.text}")
            else:
                print('price tag not found')   

        else:
            print(f"page.status_code:{page.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping the URL: {url}")
        print(e)
    return out_put

def scrape(url):
    site_name = url[12:]
    if site_name.startswith('amazon'):
        status='amazon'
        out_put["site kind"] = status
        # print(f"site kind:{status}")
        out_put=amazon(url)
        return out_put