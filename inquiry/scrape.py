import requests
from bs4 import BeautifulSoup
import chardet

out_put={}

#You can use the commented codes to test the code

#amazon

def amazon(url,soup):
    out_put={}
    try:  
            #product name
            title=soup.find('title')
            if title:
                product_name=title.text[12:]
                out_put["product name"] = product_name.strip()
                # print(f"product name:{product_name}") 
            else:
                print('product name tag not found')
            
            #img
            div_tag = soup.find('div', id='imgTagWrapperId', class_='imgTagWrapper')
            if div_tag:
                img_tag = div_tag.find('img')
                if img_tag:
                    out_put["img src"] = img_tag['src']
                    # print(f"img src:{img_tag['src']}")  #img src
            else:
                print('img tag not found')

            #price
            price_tag = soup.find('span', class_='a-offscreen')
            if price_tag:
                out_put["price"] = price_tag.text.strip()
                # print(f"price:{price_tag.text}")
            else:
                print('price tag not found')   

        

    except Exception as e:
        print(f"An error occurred while scraping the URL: {url}")
        print(e)
    


def nike(url,soup):
    try:

        #product name
        name=soup.find('span',class_='b-pdp__product-name js-gtm-product-name')
        if name:
            product_name=name.text
            out_put["product name"] = product_name.strip()
                
        else:
            print('product name tag not found')
        
        #img
        img_tag = soup.find('img', class_='b-picture__img b-pdpimages__carousel-img js-zoomed-img js-lazy-disabled')
        if img_tag:
            out_put["img src"] = img_tag['src']
        else:
            print('img tag not found')

        #price
        div_tag = soup.find('span', class_='price__regular')
        if div_tag:
            span_tag=div_tag.find('span',class_='value')
            out_put["price"] = div_tag.text.strip()
        else:
            print('price tag not found')
                    
            
    except Exception as e:
                print(f"An error occurred while scraping the URL: {url}")
                print(e)


def adidas(url,soup):
    try:
        
        #product name
        name=soup.find('h1',class_='product-name')
        if name:
            product_name=name.text
            out_put["product name"] = product_name.strip()
        else:
            print('product name tag not found')

        #img
        div_tag=soup.find('div',class_='main_image sub_img')
        if div_tag:
            img_tag = div_tag.find('img', class_='img-fluid')
            if img_tag:
                out_put["img src"] = img_tag['src']
            else:
                print('img tag not found')
        else:
                    print('img tag not found')

        #price
        div_tag = soup.find('div', class_='price')
        if div_tag:
            span_tag=div_tag.find('span',class_='value')
            out_put["price"] = span_tag.text.strip()
        else:
            print('price tag not found')

    
    except Exception as e:
        print(f"An error occurred while scraping the URL: {url}")
        print(e)


def scrape(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    }
    page=requests.get(url,headers=headers)
    # print(page.text)
    if page.status_code == 200:
        encoding = chardet.detect(page.content)["encoding"]
        html = page.content.decode(encoding)
        soup = BeautifulSoup(html, 'html.parser') 
    else:
            print(f"page.status_code:{page.status_code}")


    site_name = url[12:]
    if site_name.startswith('amazon'):
        status='amazon'
        amazon(url,soup)
        
    elif site_name.startswith('nike'):
        status='nike'
        nike(url,soup)
    elif site_name.startswith('adidas'):
        status='adidas'
        adidas(url,soup)
            
    out_put["site kind"] = status      
    # print(f"site kind:{status}")
        
    return out_put