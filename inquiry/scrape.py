import requests
from bs4 import BeautifulSoup
import chardet


#amazon

def amazon(url):
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
                print(f"product name:{product_name}") 
            
            #img
            div_tag = soup.find('div', id='imgTagWrapperId', class_='imgTagWrapper')
            if div_tag:
                img_tag = div_tag.find('img')
                if img_tag:
                    print(f"img src:{img_tag['src']}")  #img src
            else:
                print('Div tag not found')

            #price
            price_tag = soup.find('span', class_='a-offscreen')
            if price_tag:
                print(f"price:{price_tag.text}")
            else:
                print('price tag not found')   

        else:
            print(f"page.status_code:{page.status_code}")

    except Exception as e:
        print(f"An error occurred while scraping the URL: {url}")
        print(e)

def scrape(url):
    site_name = url[12:]
    if site_name.startswith('amazon'):
        status='amazon'
        print(f"site kind:{status}")
        return amazon(url)