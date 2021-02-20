import os
import sys
import asyncio
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = 'scraping_service.settings'

import django

django.setup()

from django.db import DatabaseError
from django.contrib.auth import get_user_model
from scraping.parsers import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()
jobs, errors = [], []


def get_filters():
    qs = User.objects.filter(send_email=True).values()
    return set((q['city_id'], q['language_id']) for q in qs)


def get_urls(_filters):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _filters:
        if pair in url_dict:
            tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
            urls.append(tmp)
    return urls


async def task(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


parsers = ((work, 'work'), (rabota, 'rabota'), (dou, 'dou'), (djinni, 'djinni'))

filters = get_filters()
url_list = get_urls(filters)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['language'], data['city'])
             for data in url_list
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(task(f)) for f in tmp_tasks])

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=datetime.date.today())
    if qs.exists():
        err = qs.first()
        err.data['Errors'].update(errors)
        err.save()
    else:
        Error.objects.create(data={'Errors': errors})
