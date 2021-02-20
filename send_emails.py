import os
import sys
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = 'scraping_service.settings'

import django

django.setup()

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER

today = datetime.date.today()
User = get_user_model()
empty = '<h2>К сожалению сегодня для вас данных нет.</h2>'
subject = f'Рассылка вакансий с сервиса за {today}'
text_content = f'Рассылка вакансий с сервиса {today}'
from_email = EMAIL_HOST_USER

qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for q in qs:
    users_dict.setdefault((q['city'], q['language']), [])
    users_dict[(q['city'], q['language'])].append(q['email'])

if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pairs in users_dict.keys():
        params['city_id__in'].append(pairs[0])
        params['language_id__in'].append(pairs[1])
    qs = Vacancy.objects.filter(**params).values()  # for correct work should add 'timestamp=today' to the filter func
    vacancies = {}
    for q in qs:
        vacancies.setdefault((q['city_id'], q['language_id']), [])
        vacancies[(q['city_id'], q['language_id'])].append(q)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html, "text/html")
            msg.send()

err_qs = Error.objects.filter(timestamp=today)
to = EMAIL_HOST_USER
subject = ''
text_content = f'Errors {today}'
content = ''
if err_qs.exists():
    error = err_qs.first()
    subject += f'Errors for {today}'
    errs = error.data.get('Errors', False)
    if errs:
        for i in errs:
            content += f'<h5><a href="{i["url"]}">Error: {i["title"]}</a></h5>'
    reqs = error.data.get('Users_requests', False)
    if reqs:
        subject += 'Users requests'
        for i in reqs:
            content += f'<h5>{i["city"]} {i["language"]} {i["user_email"]} {i.get("message", "")}</h5>'

urls_qs = Url.objects.all().values('city', 'language')
urls_dict = {((i['city'], i['language']) for i in urls_qs)}
urls_err = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        urls_err += f'There are no urls for pair ({keys[0]}, {keys[1]})'
if urls_err:
    subject += "Отсутствующие url адреса"
    content += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()
