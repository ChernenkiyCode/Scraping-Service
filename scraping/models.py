import jsonfield as jsonfield
from django.db import models
from .utils import from_cyrillic_to_eng

def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


class City(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название населенного пункта', unique=True)
    slug = models.CharField(max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Названия населенных пунктов'
        verbose_name = 'Название населенного пункта'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык програмирования', unique=True)
    slug = models.CharField(max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Языки програмирования'
        verbose_name = 'Язык програмирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=80, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=100, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Язык програмирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Вакансии'
        verbose_name = 'Вакансия'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    data = jsonfield.JSONField()
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Язык програмирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
