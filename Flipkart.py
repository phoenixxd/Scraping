import requests
from bs4 import BeautifulSoup
import re 
import json

def Flipkart_Crawl(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get('https://www.flipkart.com/search?q=' + query, headers = headers).content
    print(data)
    soup = BeautifulSoup(data, "html.parser")
    collection = soup.find_all("div", {"class": "col _2-gKeQ"})
    out = {}

    for c in collection:
        a = c.find("a")['href']
        prod = re.sub(r"(?s)^/(.*?)/.*$",r"\1", a)
        pid = re.sub(r"(?s)^.*pid=(.*?)&.*$",r"\1", a)
        out[prod] = pid

    return out

def Flipkart_Scrape(productID, product):
    data = {"productId": productID, # end of url pid=MOBEG4XWJG7F9A6Z
            "count": "15000",
            "ratings": "ALL",
            "reviewerType:ALL"
            "sortOrder": "MOST_HELPFUL"}

    headers = ({"x-user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36 FKUA/website/41/website/Desktop"})
    data = requests.get("https://www.flipkart.com/api/3/product/reviews", params=data, headers=headers).json()
    if data is None or data['RESPONSE'] is None: return 
    reviews = data['RESPONSE']['data']
    
    output = []
    for reviewdict in reviews:
        review = reviewdict['value']
        author, certBuyer = review['author'], review['certifiedBuyer']
        title, text = review['title'] , review['text']
        rating, helpful = review['rating'], review['helpfulCount']
        output.append([{'title': title, 'text': text, 'rating':rating,'helpful': helpful, 'author':author,'certBuyer': certBuyer}])

    with open(re.sub("[^a-zA-Z0-9]", " " ,product) + ".json", 'w') as f:
        json.dump(output, f, indent=4)


products = Flipkart_Crawl("redmi")
print(products)
for product in products:
    Flipkart_Scrape(products[product], product)
