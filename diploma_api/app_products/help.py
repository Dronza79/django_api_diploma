
import random
import re

import transliterate

from app_products.models import Product, Tag

for prod in Product.objects.all():
    num = random.random()
    prod.limited = False
    print(num)
    if num <= 0.25:
        print('=========>', prod)
        prod.limited = True
    prod.save()

c = 100
while c < 140:
    c += 1
    na = f'Tag Product {c}'
    Tag.objects.get_or_create(name=na)
    # Tag.objects.get_or_create(name=f'Таг_Прод_1')

from transliterate import translit, slugify, detect_language
import re
name = 'product'
if not re.fullmatch(r'[а-яА-ЯёЁ]+', name):
    string = slugify(translit(name, 'ru'))
else:
    string = slugify(name)

for prod in Product.objects.all():
    num = [tag for tag in Tag.objects.all()]
    print(num)
    prod.tags.set(num)

    prod.save()
