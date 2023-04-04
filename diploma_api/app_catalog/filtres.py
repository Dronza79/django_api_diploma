from app_catalog.models import Category


def sort_filter(request, qs, **kwargs):
    print('request=', request.query_params)
    print(f'qs={qs}')
    print(f'count={qs.count()}')
    print('kwargs=', kwargs)
    data = request.query_params
    category = Category.objects.filter(id=kwargs.get('id')).first()
    if category:
        fst_filter = tuple(str(category.id))
        if not category.parent:
            fst_filter = tuple(cat.id for cat in category.subcategories.all())
        print("fst_filter=", fst_filter)
        qs = qs.filter(category_id__in=fst_filter)

    snd_filter = data.get('filter[name]')
    if snd_filter:
        print('snd_filter=', snd_filter)
        qs = qs.filter(title__icontains=snd_filter)

    thd_filter = data.get('filter[available]')
    if thd_filter:
        print('thd_filter=', thd_filter)
        qs = qs.filter(count__gt=0)

    four_filter = data.getlist('tags[]')
    if four_filter:
        print('four_filter=', four_filter)
        qs = qs.filter(tags__in=four_filter)

    price_from = data.get('filter[minPrice]')
    price_to = data.get('filter[maxPrice]')
    qs = qs.filter(price__gte=price_from, price__lte=price_to)

    sort = data.get('sort')
    if sort == 'reviews':
        sort = 'rev'
    if data.get('sortType') == 'inc':
        qs = qs.order_by(f'-{sort}')
    else:
        qs = qs.order_by(f'{sort}')

    print(f'окончательный qs={qs}\n count={qs.count()}')
    return qs
