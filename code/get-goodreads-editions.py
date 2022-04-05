import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
import time
import re

'''
Code taken and changed by Timos Zacharatos (https://github.com/rkeytech),
 https://github.com/rkeytech/goodreads-editions
'''

def get_isbn():
    isbns = [] #insert isbns
    return isbns


def get_page(base_url, data):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        r = requests.get(base_url, headers=headers, params=data)
    except:
        r = None
    return r


def get_editions_details(isbn):
    data = {'q': isbn}
    book_url = get_page("https://www.goodreads.com/search", data)
    soup = bs(book_url.text, 'html.parser')

    ed_item = soup.find("div", class_="otherEditionsLink").find("a")
    ed_link = f"https://www.goodreads.com{ed_item['href']}"
    ed_num = ed_item.text.strip().split(' ')[-1].strip('()')

    return ((ed_link, int(ed_num), isbn))


def get_editions_urls(ed_details):
    rows = []

    # Unpack the tuple with the informations about the editions
    url, ed_num, isbn = ed_details

    # Navigate to all pages for books with more than 100 editions

    end_of_list = False
    page = 0
    while end_of_list == False:
        print('Page: ', page + 1)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        r = requests.get(url, headers=headers, params={
            'page': str(page + 1),
            'per_page': '100',
            'filter_by_format': '',
            # if you want all editions change above line to 'filter_by_format': '',
            'utf8': "%E2%9C%93"})

        soup = bs(r.text, 'html.parser')

        editions = soup.find_all("div", class_="editionData")

        print(len(editions))
        if len(editions) < 100:
            end_of_list = True


        for book in editions:
            item = book.find("a", class_="bookTitle")
            rating = book.find_all("div", class_="dataValue")[-1].text
            rating = ' '.join(rating.split())
            row = {'item': f"https://www.goodreads.com{item['href']}",
                   'rating': f'{rating}'}

            rows.append(row)

        time.sleep(2)
        page += 1
    return rows


if __name__ == "__main__":
    try:
        os.mkdir('./urls_files')
    except Exception:
        pass

    isbns = get_isbn()

    for isbn in isbns:
        ed_details = get_editions_details(isbn)
        rows = get_editions_urls(ed_details)
        df = pd.DataFrame(rows)
        df.to_csv(f"urls_files/{isbn}_urls.csv", index=False)