
import random
from app_products.models import Product
for prod in Product.objects.all():
    num = random.random()
    prod.limited = False
    print(num)
    if num <= 0.25:
        print('=========>', prod)
        prod.limited = True
    prod.save()
