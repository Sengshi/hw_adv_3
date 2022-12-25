import json
from time import sleep
import requests
from bs4 import BeautifulSoup
from re import search
from fake_headers import Headers


def generate_json(vacs, filename):
    with open(filename, 'w') as write_file:
        json.dump(vacs, write_file)


def req_hh(letters):
    vac_parsed = []
    head = Headers(browser="firefox", os="win").generate()
    vac_list = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=head)
    soup1 = BeautifulSoup(vac_list.text, 'html.parser')
    posts = soup1.find_all('div', class_='serp-item')
    # основное задание
    for post in posts:
        sleep(0.2)
        vac_full = requests.get(post.find('a')['href'], headers=head)
        soup2 = BeautifulSoup(vac_full.text, 'html.parser')
        vac_about = str(soup2.find('div', attrs={'data-qa': 'vacancy-description'}))
        for letter in letters:
            if search(letter, vac_about):
                wages = post.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                company = post.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                city = post.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(', ')
                if not wages:
                    wages = 'ЗП не указана'
                else:
                    wages = wages.text.replace('\u202f', '')
                # print(post.find('a')['href'])
                vac_parsed.append({
                    'link': post.find('a')['href'],
                    'wages': wages,
                    'company': company,
                    'city': city[0],
                })
                break
    generate_json(vac_parsed, 'vac_file.json')

    # дополнительное задание
    vac_parsed_dop = []
    for post in posts:
        if post.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}):
            wages = post.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            if search('USD', wages):
                company = post.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                city = post.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(', ')
                vac_parsed_dop.append({
                    'link': post.find('a')['href'],
                    'wages': wages.replace('\u202f', ''),
                    'company': company,
                    'city': city[0],
                })
    generate_json(vac_parsed_dop, 'vac_file_dop.json')


if __name__ == '__main__':
    letters = ['Django', 'Flask']
    req_hh(letters)
