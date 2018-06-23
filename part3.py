# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py
most_read = None
url = "http://www.michigandaily.com"
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
divs = soup.findAll('div')
for div in divs:
    if div.get("class") is not None and "view-most-read" in div.get("class"):
        most_read = div
        break
most_read_li = most_read.findAll('li')

print("Michigan Daily -- MOST READ")
for item in most_read_li:
    print(item.string)
    byline = None
    try:
        author_soup = BeautifulSoup(requests.get(url + item.a.get('href')).text, 'html.parser')
        divs = author_soup.findAll('div')
        for div in divs:
            if div.get("class") is not None and "byline" in div.get("class"):
                byline = div
                break
        print("  by " + byline.div.a.string)
    except:
        print("  by unknown author")

