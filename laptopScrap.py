import pandas as pd
import requests 
from bs4 import BeautifulSoup
import time
import re
import warnings

warnings.filterwarnings("ignore")
print("setup complete")
def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "close",
    }
    url=f"https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=9ce5bcac-ccf4-418d-a536-fee70f0ce240&as-searchtext=laptop"
    response=requests.get(url,headers=headers)
    # print(response.content)
    if response.status_code!=200:
        print(f"failed to retrive page status code: {response.status_code}")
        return []

    soup=BeautifulSoup(response.content,"html.parser")
    # print(f"soap content",soup)
    # identify book blocks
    cards=soup.find_all('div',attrs={'class':'tUxRFH'})
    # print(cards)
    print(f"found {len(cards)} items in laptop")
    alls=[]
    for d in cards:
        all1=[]
        product_name=d.find('div',attrs={'class':'KzDlHZ'})
        # print(product_name.text)
        if product_name:
            all1.append(product_name.text)
        else:
            all1.append("Name not Avl")
        rating=d.find('div',attrs={'class':'XQDdHH'})
        all1.append(rating.text.strip() if rating else "No Rating")
        # processor
        processor=d.find('li', attrs={'class':'J+igdf'})
        # print(processor.text)
        all1.append(processor.text.strip() if processor else "Not Available")
        #storage
        storage=d.findAll('li',attrs={'class':"J+igdf"})
        # print(storage[3])
        all1.append(storage[3].text.strip() if storage[3] else "Not Available")
        #storage
        warranty=d.findAll('li',attrs={'class':"J+igdf"})
        # print(warranty[-1].text)
        all1.append(warranty[-1].text.strip() if warranty[-1] else "Not Available")
        #prize of product
        prize=d.find('div',attrs={'class':'Nx9bqj _4b5DiR'})
        # print(prize.text)
        all1.append(prize.text.strip() if prize else "$$Not Available$$")
        alls.append(all1)
    return alls
#main section 
result=[]
data=get_data("https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=9ce5bcac-ccf4-418d-a536-fee70f0ce240&as-searchtext=laptop")
result.extend(data)
df=pd.DataFrame(result,columns=['Product Name','Rating','Processor','Storage','Warranty','Price'])
# save to csv
df.to_csv('laptop_Products.csv',index=False, encoding='utf-8')
print("Data Saved to 'laptop_product.csv'")
df=pd.read_csv('laptop_Products.csv')
print(df.head(18))