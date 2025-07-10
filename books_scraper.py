import requests
from bs4 import BeautifulSoup
import csv
import time

baseurl = 'https://books.toscrape.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
 
allbooks = []
currenturl = baseurl
session = requests.Session()
session.headers.update(headers)

while True:
    try:
        print(f'\n Accediendo a: {currenturl}')
        response = session.get(currenturl)
        time.sleep(0)

        if response.status_code != 200:
            print(f'Error {response.status_code} in {currenturl}')
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        print(f'Books found: {len(books)}')
                
        for book in books:
            try:
                partialbookurl = book.find('h3').a['href']
                    
                if '../' in partialbookurl:
                    partialbookurl = partialbookurl.replace('../', '')
                    
                if partialbookurl.startswith('catalogue/'):
                    bookurl = baseurl + '/' + partialbookurl
                else:
                    bookurl = baseurl + '/catalogue/' + partialbookurl
                    
                print(f'Book: {bookurl}')
                responseind = session.get(bookurl)
                time.sleep(0)

                if responseind.status_code != 200:
                    print(f'Error {responseind.status_code} in {bookurl}')
                    continue

                subsoup = BeautifulSoup(responseind.text, 'html.parser')
                title = subsoup.find('h1').text
                table = subsoup.find('table', class_='table table-striped')
                    
                if table:
                    rows = table.find_all('tr')
                    price = rows[3].td.text.replace('Â', '')
                    stock = rows[5].td.text.strip()
                    UPC = rows[0].td.text
                    allbooks.append((title, price, stock, UPC))

            except Exception as e:
                print(f'Error processing {e}')
                continue

        nextbutton = soup.find('li', class_='next')
            
        if nextbutton:
            nextpageurl = nextbutton.a['href']


            if nextpageurl.startswith('catalogue/'):
                urle = '/' + nextpageurl 
            else:
                urle = '/catalogue/' + nextpageurl

            print(f'Next page {nextpageurl}')
            currenturl = baseurl + urle 
        else:
            print('End of scraping')
            break


    except Exception as e:
        print(f'Mistake in the principal loop: {e}')
        break

with open('books_scraped.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('title', 'price with taxes', 'stock', 'UPC'))
    writer.writerows(allbooks)

print(f'The file books_scraped has been saved. Total: {len(allbooks)} books.')