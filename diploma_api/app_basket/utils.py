from .models import UserCart


def get_cart(request):
    # print("session=", request.session.__dict__)
    user = request.user
    if not user.is_authenticated:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key
            print('создали session_key=', session_key)
        cart = UserCart.objects.prefetch_related('inside__product').get_or_create(session=session_key)[0]
        request.session['no_user_cart_id'] = cart.id
        request.session['session_key'] = session_key
    else:
        cart_id = request.session.get('no_user_cart_id')
        cart = UserCart.objects.prefetch_related('inside__product').get_or_create(owner=user)[0]
        if cart_id:
            data = UserCart.objects.prefetch_related('inside__product').get(pk=cart_id)
            cart.add_cart(data)
            del request.session['no_user_cart_id']
            request.session.modified = True
    # print('словарь корзины=', request.session.__dict__)
    return cart


def get_data_cart(request):
    return [{
        'id': item.product.id,
        'title': item.product.title,
        'price': item.product.price,
        'description': item.product.description,
        'count': item.quantity,
        'href': item.product.href,
        'images': item.product.images,
    } for item in get_cart(request).inside.all()]
