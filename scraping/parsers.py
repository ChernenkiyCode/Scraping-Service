import requests
from bs4 import BeautifulSoup as BS
from random import randint

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=9,*/*;q=0.8'},
           {
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1',
               "Accept": 'text/html,application/xhtml+xml,application/xml;q=9,*/*;q=0.8'},
           {
               'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
               "Accept": 'text/html,application/xhtml+xml,application/xml;q=9,*/*;q=0.8'},
           {
               'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>',
               "Accept": 'text/html,application/xhtml+xml,application/xml;q=9,*/*;q=0.8'}]


def work(url, language=None, city=None):
    resp = requests.get(url, headers=headers[randint(0, 3)])
    jobs = []
    errors = []

    if url:
        if resp.status_code == 200:
            domain = 'https://www.work.ua'
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'pjax-job-list'})

            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})

                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.p.text
                    company = 'No name'
                    logo = div.find('img')

                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'description': description, 'company': company,
                                 'url': domain + href, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'The div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota(url='https://rabota.ua/zapros/python', language=None, city=None):
    resp = requests.get(url, headers=headers[randint(0, 3)])
    jobs = []
    errors = []

    if url:
        if resp.status_code == 200:
            domain = 'https://rabota.ua'
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            table = soup.find('table', attrs={'id': 'ctl00_content_vacancyList_gridList'})
            if not new_jobs:
                if table:
                    tr_list = table.find_all('tr', attrs={'id': True})

                    for tr in tr_list:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('p', attrs={'class': 'card-title'})
                            description = div.find('div', attrs={'class': 'card-description'})
                            href = title.a['href']
                            p = div.find('p', attrs={'class': 'company-name'})
                            company = 'No name'
                            if p:
                                company = p.a.text
                                jobs.append({'title': title.text, 'description': description.text, 'company': company,
                                             'url': domain + href, 'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'The table does not exist'})
            else:
                errors.append({'url': url, 'title': 'Page is empty'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def dou(url='https://jobs.dou.ua/vacancies/?category=Python&search=%D0%BA%D0%B8%D0%B5%D0%B2', language=None, city=None):
    resp = requests.get(url, headers=headers[randint(0, 3)])
    jobs = []
    errors = []

    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'vacancyListId'})

            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})

                for li in li_list:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    description = li.find('div', attrs={'class': 'sh-info'})
                    company = 'No name'
                    a_comp = title.find('a', attrs={'class': 'company'})

                    if a_comp:
                        company = a_comp.text
                    jobs.append({'title': title.text, 'description': description.text, 'company': company,
                                 'url': href, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'The div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def djinni(url='https://djinni.co/jobs/keyword-python/kyiv/', language=None, city=None):
    resp = requests.get(url, headers=headers[randint(0, 3)])
    jobs = []
    errors = []

    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            domain = 'https://djinni.co'
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})

            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})

                for li in li_list:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    description = li.find('div', attrs={'class': 'list-jobs__description'})
                    company = 'No name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})

                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text, 'description': description.p.text, 'company': company,
                                 'url': domain + href, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'The div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors
