import requests
from bs4 import BeautifulSoup

URL = 'https://fora.kz'

def get_soup(URL):
    r = requests.get(URL, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    categories = [
        (item['href'], item.find('span', class_='catalog-item-name').text) 
        for item 
        in soup.find_all('a', class_='catalog-item')
        ]
    return categories

res_list = []

for parent_category_link, parent_category_name in get_soup(URL + '/catalog'):
    for subcategory_link, subcategory_name in get_soup(URL + parent_category_link):
        # getting prod details
        i = 1
        while True:
            r = requests.get(URL + subcategory_link + f'?page={i}', verify=False)
            print(URL + subcategory_link + f'?page={i}')
            soup = BeautifulSoup(r.text, 'html.parser')
            products = soup.find_all('div', class_='catalog-list-item')
            if products:
                for product in products:
                    product_card = product.find('div', class_='item-content')
                    name_tab = product_card.find('a')
                    name = name_tab.text
                    link = URL + name_tab['href']

                    price = product_card.find('p', class_='price').text
                    price = price \
                        .replace(' ', '') \
                        .replace('m', '')

                    res = {
                        'name': name,
                        'link': link,
                        'price': price,
                        'parent_category_name': parent_category_name,
                        'subcategory_name': subcategory_name
                        }
                        
                    res_list.append(res)
                i += 1
            else:
                break
