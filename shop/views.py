import pickle, hashlib, datetime, random
from django.template.loader import get_template
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404, redirect, RequestContext, render
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.db.models import Q, Max, Min
from shop.models import *
from shop.forms import OrderForm, RegistrationForm
from django.contrib.auth.models import User


def get_item(item_inv):
        l = [list(x.objects.filter(pk=item_inv)) for x in (Phone, Tablet, Notebook, Accessories, ForMaster,
                                                            ForHome, Share)]
        item = list()
        for x in l:
            item += x
        if item:
            return item[0]
        return False


def item(req, item=''):
    args = dict(item=get_item(item))
    if args['item']:
        shares = Share.objects.filter(gen_item__exact=args['item'].inv).only('sec_item', 'discount').values()
        if shares:
            args['shares'] = list()
            for obj in shares:
                args['shares'].append(dict(sec_item=get_item(str(obj['sec_item'])), discount=obj['discount'],
                                      inv=obj['inv'], price=obj['price']))
        return render_to_response('item_phone/index.html', args, context_instance=RequestContext(req))
    else:
        return redirect('general')


def tablet_filter(req, filter_str=""):
    if filter_str == "":
        args = dict()
        args["items"] = Tablet.objects.all()
        return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))
    filter_str = filter_str.split('-')
    filter_str.sort()
    filters = {
        "d1": lambda: (Q(diagonal__gte=6) & Q(diagonal__lte=7.7)),
        "d2": lambda: (Q(diagonal__gte=7.85) & Q(diagonal__lte=9.5)),
        "d3": lambda: (Q(diagonal__gte=9.6) & Q(diagonal__lte=10.1)),
        "d4": lambda: Q(diagonal__gt=10.1),

        "r1": lambda: Q(resolution__iexact="2560х1440"),
        "r2": lambda: Q(resolution__iexact="1920x1080"),
        "r3": lambda: Q(resolution__iexact="800х400"),
        "r4": lambda: Q(resolution__iexact="1280x720"),
        "r5": lambda: Q(resolution__iexact="1136x640"),
        "r6": lambda: Q(resolution__iexact="960x540"),
        "r7": lambda: Q(resolution__iexact="854х480"),
        "r8": lambda: Q(resolution__iexact="3840x2160"),

        "n1": lambda: Q(count_core__exact=1),
        "n2": lambda: Q(count_core__exact=2),
        "n3": lambda: Q(count_core__exact=4),
        "n4": lambda: Q(count_core__exact=8),
        "n5": lambda: Q(count_core__gt=8),

        "m1": lambda: Q(ram__lt=1024),
        "m2": lambda: (Q(ram__gte=1024) & Q(ram__lt=2048)),
        "m3": lambda: Q(ram__exact=2048),
        "m4": lambda: Q(ram__exact=3072),
        "m5": lambda: Q(ram__exact=4096),
        "m6": lambda: Q(ram__gt=4096),

        "c1": lambda: Q(camera__lte=2),
        "c2": lambda: (Q(camera__gt=2) & Q(camera__lte=7)),
        "c3": lambda: (Q(camera__gte=8) & Q(camera__lte=12)),
        "c4": lambda: Q(camera__gte=13),

        "f1": lambda: Q(availability__exact="is"),
        "f2": lambda: Q(availability__exact="c"),

        "p": lambda min_p, max_p: (Q(price__gte=min_p) & Q(price__lte=max_p)),
    }

    q_objs_d = Q()
    q_objs_r = Q()
    q_objs_n = Q()
    q_objs_m = Q()
    q_objs_c = Q()
    q_objs_f = Q()
    q_objs_p = Q()
    filters_keys = list(filters.keys())

    for f in filter_str:
        if f[0] == 'p':
            s = f[1:]
            s = s.split('p')
            q_objs_p.add(filters['p'](int(s[0]), int(s[1]) + 1), Q.OR)
        if f in filters_keys:
            if f[0] == 'd':
                q_objs_d.add(filters[f](), Q.OR)
            elif f[0] == 'r':
                q_objs_r.add(filters[f](), Q.OR)
            elif f[0] == 'n':
                q_objs_n.add(filters[f](), Q.OR)
            elif f[0] == 'm':
                q_objs_m.add(filters[f](), Q.OR)
            elif f[0] == 'c':
                q_objs_c.add(filters[f](), Q.OR)
            elif f[0] == 'f':
                q_objs_f.add(filters[f](), Q.OR)
    q_l = [q_objs_d, q_objs_r, q_objs_n, q_objs_m, q_objs_c, q_objs_f, q_objs_p]
    q = Q()
    for f in q_l:
        q.add(f, Q.AND)
    args = dict()
    args["items"] = Tablet.objects.filter(q)
    return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))


def note_filter(req, filter_str=""):
    if filter_str == "":
        args = dict()
        args["items"] = Notebook.objects.all()
        return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))
    filter_str = filter_str.split('-')
    filter_str.sort()
    filters = {
        "d1": lambda: (Q(diagonal__gte=9) & Q(diagonal__lte=12.5)),
        "d2": lambda: Q(diagonal=13),
        "d3": lambda: (Q(diagonal__gte=14) & Q(diagonal__lte=15.6)),
        "d4": lambda: (Q(diagonal__gte=16) & Q(diagonal__lte=17)),

        "r1": lambda: Q(resolution__iexact="1900x1080"),
        "r2": lambda: Q(resolution__iexact="1366x768"),
        "r3": lambda: Q(resolution__iexact="1600x900"),

        "n1": lambda: Q(count_core__exact=1),
        "n2": lambda: Q(count_core__exact=2),
        "n3": lambda: Q(count_core__exact=4),
        "n4": lambda: Q(count_core__exact=8),
        "n5": lambda: Q(count_core__gt=8),

        "m1": lambda: Q(ram__lt=4096),
        "m2": lambda: (Q(ram__gte=4096) & Q(ram__lte=6144)),
        "m3": lambda: (Q(ram__gte=8192) & Q(ram__lte=10240)),
        "m4": lambda: Q(ram__gte=12288),

        "c1": lambda: Q(gpu__icontains='amd'),
        "c2": lambda: Q(gpu__icontains='nvidia'),

        "w1": lambda: Q(core_other__icontains='amd'),
        "w2": lambda: Q(core_other__icontains='intel'),

        "f1": lambda: Q(availability__exact="is"),
        "f2": lambda: Q(availability__exact="c"),

        "p": lambda min_p, max_p: (Q(price__gte=min_p) & Q(price__lte=max_p)),
    }

    q_objs_d = Q()
    q_objs_r = Q()
    q_objs_n = Q()
    q_objs_m = Q()
    q_objs_c = Q()
    q_objs_f = Q()
    q_objs_p = Q()
    q_objs_w = Q()
    filters_keys = list(filters.keys())

    for f in filter_str:
        if f[0] == 'p':
            s = f[1:]
            s = s.split('p')
            q_objs_p.add(filters['p'](int(s[0]), int(s[1]) + 1), Q.OR)
        if f in filters_keys:
            if f[0] == 'd':
                q_objs_d.add(filters[f](), Q.OR)
            elif f[0] == 'r':
                q_objs_r.add(filters[f](), Q.OR)
            elif f[0] == 'n':
                q_objs_n.add(filters[f](), Q.OR)
            elif f[0] == 'm':
                q_objs_m.add(filters[f](), Q.OR)
            elif f[0] == 'c':
                q_objs_c.add(filters[f](), Q.OR)
            elif f[0] == 'f':
                q_objs_f.add(filters[f](), Q.OR)
            elif f[0] == 'w':
                q_objs_w.add(filters[f](), Q.OR)
    q_l = [q_objs_d, q_objs_r, q_objs_n, q_objs_m, q_objs_c, q_objs_f, q_objs_p, q_objs_w]
    q = Q()
    for f in q_l:
        q.add(f, Q.AND)
    args = dict()
    args["items"] = Notebook.objects.filter(q)
    return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))


def phone_filter(req, filter_str=""):
    if filter_str == "":
        args = dict()
        args["items"] = Phone.objects.all()
        return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))
    filter_str = filter_str.split('-')
    filter_str.sort()
    filters = {
        "d1": lambda: (Q(diagonal__gte=6) & Q(diagonal__lte=7.7)),
        "d2": lambda: (Q(diagonal__gte=7.85) & Q(diagonal__lte=9.5)),
        "d3": lambda: (Q(diagonal__gte=9.6) & Q(diagonal__lte=10.1)),
        "d4": lambda: Q(diagonal__gt=10.1),

        "r1": lambda: Q(resolution__iexact="2560х1440"),
        "r2": lambda: Q(resolution__iexact="1920x1080"),
        "r3": lambda: Q(resolution__iexact="800х400"),
        "r4": lambda: Q(resolution__iexact="1280x720"),
        "r5": lambda: Q(resolution__iexact="1136x640"),
        "r6": lambda: Q(resolution__iexact="960x540"),
        "r7": lambda: Q(resolution__iexact="854х480"),
        "r8": lambda: Q(resolution__iexact="3840x2160"),

        "n1": lambda: Q(count_core__exact=1),
        "n2": lambda: Q(count_core__exact=2),
        "n3": lambda: Q(count_core__exact=4),
        "n4": lambda: Q(count_core__exact=8),
        "n5": lambda: Q(count_core__gt=8),

        "m1": lambda: Q(ram__lt=1024),
        "m2": lambda: (Q(ram__gte=1024) & Q(ram__lt=2048)),
        "m3": lambda: Q(ram__exact=2048),
        "m4": lambda: Q(ram__exact=3072),
        "m5": lambda: Q(ram__exact=4096),
        "m6": lambda: Q(ram__gt=4096),

        "c1": lambda: Q(camera__lte=2),
        "c2": lambda: (Q(camera__gt=2) & Q(camera__lte=7)),
        "c3": lambda: (Q(camera__gte=8) & Q(camera__lte=12)),
        "c4": lambda: Q(camera__gte=13),

        "f1": lambda: Q(availability__exact="is"),
        "f2": lambda: Q(availability__exact="c"),

        "p": lambda min_p, max_p: (Q(price__gte=min_p) & Q(price__lte=max_p)),
    }

    q_objs_d = Q()
    q_objs_r = Q()
    q_objs_n = Q()
    q_objs_m = Q()
    q_objs_c = Q()
    q_objs_f = Q()
    q_objs_p = Q()
    filters_keys = list(filters.keys())

    for f in filter_str:
        if f[0] == 'p':
            s = f[1:]
            s = s.split('p')
            q_objs_p.add(filters['p'](int(s[0]), int(s[1]) + 1), Q.OR)
        if f in filters_keys:
            if f[0] == 'd':
                q_objs_d.add(filters[f](), Q.OR)
            elif f[0] == 'r':
                q_objs_r.add(filters[f](), Q.OR)
            elif f[0] == 'n':
                q_objs_n.add(filters[f](), Q.OR)
            elif f[0] == 'm':
                q_objs_m.add(filters[f](), Q.OR)
            elif f[0] == 'c':
                q_objs_c.add(filters[f](), Q.OR)
            elif f[0] == 'f':
                q_objs_f.add(filters[f](), Q.OR)
    q_l = [q_objs_d, q_objs_r, q_objs_n, q_objs_m, q_objs_c, q_objs_f, q_objs_p]
    q = Q()
    for f in q_l:
        q.add(f, Q.AND)
    args = dict()
    args["items"] = Phone.objects.filter(q)
    return render_to_response("filter_items/index.html", args, context_instance=RequestContext(req))


def search(req, search_str=""):
    args = dict()
    args['phones'] = Phone.objects.filter(name__icontains=search_str).only('name', 'inv')
    args['tablets'] = Tablet.objects.filter(name__icontains=search_str).only('name', 'inv')
    args['note'] = Notebook.objects.filter(name__icontains=search_str).only('name', 'inv')
    args['acs'] = Accessories.objects.filter(name__icontains=search_str).only('name', 'inv')
    args['home'] = ForHome.objects.filter(name__icontains=search_str).only('name', 'inv')
    args['master'] = ForMaster.objects.filter(name__icontains=search_str).only('name', 'inv')
    return render_to_response("search/index.html", args, context_instance=RequestContext(req))


def all_search(req, search_str=""):
    args = dict()
    l = [list(x.objects.filter(name__icontains=search_str)) for x in (Phone, Tablet, Notebook, Accessories, ForMaster, ForHome, Accessories)]
    res = list()
    for x in l:
        res += x
    del l
    args["items"] = res
    args["search_str"] = search_str
    return render_to_response("items/index.html", args, context_instance=RequestContext(req))


def other_category(req, category='', subcategory=''):
    args = dict()
    if category:
        if category == 'appliances':
            if subcategory:
                try:
                    args['items'] = ForHome.objects.filter(link_category_id=subcategory)
                    args['category'] = Category.objects.get(pk=subcategory)
                except (ForHome.DoesNotExist, Category.DoesNotExist):
                    args['items'] = ForHome.objects.all()
                    args['category'] = 'Бытовая техника'
            else:
                args['items'] = ForHome.objects.all()
                args['category'] = 'Бытовая техника'
            args['cat'] = 'appliances'
            args['subcategory'] = Category.objects.filter(variant=3)
        elif category == 'master-tools':
            if subcategory:
                try:
                    args['items'] = ForMaster.objects.filter(link_category_id=subcategory)
                    args['category'] = Category.objects.get(pk=subcategory)
                except (ForMaster.DoesNotExist, Category.DoesNotExist):
                    args['items'] = ForMaster.objects.all()
                    args['category'] = 'Всё для мастера'
            else:
                args['items'] = ForMaster.objects.all()
                args['category'] = 'Всё для мастера'
            args['subcategory'] = Category.objects.filter(variant=2)
            args['cat'] = 'master-tools'
        elif category == 'accessories':
            if subcategory:
                try:
                    args['items'] = Accessories.objects.filter(link_category_id=subcategory)
                    args['category'] = Category.objects.get(pk=subcategory)
                except (ForMaster.DoesNotExist, Category.DoesNotExist):
                    args['items'] = ForMaster.objects.all()
                    args['category'] = 'Акссесуары и Комплектующие'
            else:
                args['items'] = Accessories.objects.all()
                args['category'] = 'Акссесуары и Комплектующие'
            args['subcategory'] = Category.objects.filter(variant=1)
            args['cat'] = 'accessories'
        return render_to_response('items/index.html', args, context_instance=RequestContext(req))
    else:
        return redirect('general')


def phones_search(req, search_str=""):
    args = dict()
    args['items'] = Phone.objects.filter(name__icontains=search_str)
    return render_to_response("phones/index.html", args, context_instance=RequestContext(req))


def general(req):
    args = dict()
    args['about'] = Info.objects.get(pk=1)
    args['slides'] = Slide.objects.all()
    l = [list(x.objects.order_by('-date')[:4]) for x in (Phone, Tablet, Notebook, Accessories, ForHome, ForMaster)]
    news = list()
    for x in l:
        news += x
    del l
    news.sort(key=lambda i: i.date, reverse=True)
    args['new_items'] = news
    del news
    l = [list(x.objects.order_by('-likes')[:4]) for x in (Phone, Tablet, Notebook)]
    populars = list()
    for x in l:
        populars += x
    populars.sort(key=lambda i: i.likes, reverse=True)
    args["pop_items"] = populars
    return render_to_response('general/index.html', args, context_instance=RequestContext(req))


def phones(req):
    args = dict()
    a = Phone.objects.aggregate(Max('price'), Min('price'))
    args['items'] = Phone.objects.all()
    try:
        args['price_max'] = int(a['price__max'])
        args['price_min'] = int(a['price__min'])
    except TypeError:
        args['price_max'] = 0
        args['price_min'] = 0
    return render_to_response("phones/index.html", args, context_instance=RequestContext(req))


def tablets(req):
    args = dict()
    a = Tablet.objects.aggregate(Max('price'), Min('price'))
    args['items'] = Tablet.objects.all()
    try:
        args['price_max'] = int(a['price__max'])
        args['price_min'] = int(a['price__min'])
    except TypeError:
        args['price_max'] = 0
        args['price_min'] = 0
    return render_to_response("tablets/index.html", args, context_instance=RequestContext(req))


def notes(req):
    args = dict()
    a = Notebook.objects.aggregate(Max('price'), Min('price'))
    args['items'] = Notebook.objects.all()
    try:
        args['price_max'] = int(a['price__max'])
        args['price_min'] = int(a['price__min'])
    except TypeError:
        args['price_max'] = 0
        args['price_min'] = 0
    return render_to_response("notes/index.html", args, context_instance=RequestContext(req))


def item_phone(req, item='1'):
    args = dict()
    args["item"] = get_object_or_404(Phone, pk=item)
    return render_to_response("item_phone/index.html", args, context_instance=RequestContext(req))


def like(req, item=''):
    if 'like' not in req.session:
        item = get_item(item)
        item.likes += 1
        item.save()
        req.session.set_expiry(8640000)
        req.session['like'] = True
        return HttpResponse(True)
    return HttpResponse(False)


@csrf_exempt
def add_basket(req, remove=''):
    if req.method == 'POST':
        if remove:
            item = int(req.POST.get('item', ''))
            if 'basket' in req.session:
                basket = req.session['basket']
                basket = list(basket)
                try:
                    pos = basket.index(item)
                    basket.pop(pos)
                    req.session['basket'] = tuple(basket)
                    count = req.session['item_count']
                    count = list(count)
                    count.pop(pos)
                    req.session['item_count'] = tuple(count)
                    if not len(req.session.get('basket')):
                        del req.session['basket']
                        del req.session['item_count']
                except ValueError:
                    pass
            return HttpResponse()
        new_item = req.POST.get('item')
        item_count = req.POST.get('count')
        if new_item.isdigit() and item_count.isdigit():
            new_item = int(new_item)
            item_count = int(item_count)
        else:
            return HttpResponse()
        if not ('basket' in req.session):
            req.session['basket'] = ()
            req.session.set_expiry(0)
            req.session['item_count'] = ()
            req.session.set_expiry(0)
        if new_item not in req.session.get('basket'):
            req.session['basket'] += (new_item,)
            req.session.set_expiry(0)
            req.session['item_count'] += (item_count,)
            req.session.set_expiry(0)
        else:
            pos = req.session['basket'].index(new_item)
            a = req.session['item_count']
            req.session.set_expiry(0)
            a = list(a)
            a[pos] = item_count
            req.session['item_count'] = tuple(a)
            req.session.set_expiry(0)
    return HttpResponse()


def show_basket(req, form=''):
    args = dict()
    args.update(csrf(req))
    if 'basket' in req.session:
        items = req.session.get('basket', '')
        counts = req.session.get('item_count', '')
        args['items'] = list()
        for sale_item, count in zip(items, counts):
            args['items'].append([get_item(str(sale_item)), count])
        if form:
            args['form'] = form
        else:
            args['form'] = OrderForm()
        return render_to_response('show_basket/index.html', args, context_instance=RequestContext(req))
    else:
        return redirect('general')


def add_order(req):
    if req.method == 'POST':
        if 'basket' not in req.session:
            return redirect('general')
        form = OrderForm(req.POST)
        if form.is_valid():
            items_inv = req.session.get('basket')
            counts = req.session.get('item_count')
            l = []
            s = 0
            items = [x for x in zip(items_inv, counts)]
            for item, count in items:
                i = get_item(str(item))
                l.append([i, count])
                if type(i) == Share:
                    s += i.price * count
                elif i.price_opt and count > 1:
                    s += i.price_opt * count
                else:
                    s += i.price * count
            items = pickle.dumps(items)
            context = dict()
            context['items'] = l
            order = form.save(commit=False)
            try:
                client = Client.objects.get(email=order.email)
            except Client.DoesNotExist:
                client = Client(email=order.email)
                client.save()
            finally:
                order.link_client = client
            context['pay'] = s
            tmp = None
            if client.discount > 0:
                tmp = client.discount
                tmp = s * tmp / 100
                context['pay'] = str(s) + '- {0}% = '.format(client.discount) + str(round(s - tmp, 2))
            order.items = items
            order.save()
            context['payment'] = Info.objects.get(pk=4)
            del req.session['basket']
            del req.session['item_count']
            send_mail(
                'ELEKTROSWIT: Спасибо за покупку!',
                ' ',
                'elekto-swit@yandex.ru',
                [order.email],
                fail_silently=True,
                html_message=get_template('mail_order_usr/index.html').render(context)
            )
            context['to_admin'] = True
            context['email'] = order.email
            context['message'] = order.message
            context['phone'] = order.phone
            send_mail(
                'ELEKTROSWIT: Поступил новый заказ!',
                ' ',
                'elekto-swit@yandex.ru',
                ['saninstein@yandex.ua'],
                fail_silently=True,
                html_message=get_template('mail_order_usr/index.html').render(context)
            )
            return redirect('general')
        else:
            return show_basket(req, form)


def info_basket(req):
    if 'basket' in req.session:
        return HttpResponse('OK')
    else:
        return HttpResponse()


def register_user(req):
    args = dict()
    args.update(csrf(req))
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        args['form'] = form
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user = User.objects.get(username=username)

            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            send_mail(
                'Подтверждение регистрации',
                'Спасибо за регистрацию. Активируйте свой аккаунт в течении 48 часов http://127.0.0.1:8000/confirm_mail/%s' % (activation_key),
                'elekto-swit@yandex.ru',
                [email],
                fail_silently=True
            )
            return render_to_response()
    else:
        args['form'] = RegistrationForm()
    return render_to_response('register/index.html', args, content_type=RequestContext(req))


def info(req, category=""):
    args = dict()
    if category == 'payment':
        args['info'] = Info.objects.get(pk=2)
        args['title'] = "Оплата"
    elif category == 'delivery':
        args['info'] = Info.objects.get(pk=3)
        args['title'] = "Доставка"
    elif category == 'guarantee':
        args['info'] = Info.objects.get(pk=4)
        args['title'] = "Гарантия"
    return render_to_response('info/index.html', args, context_instance=RequestContext(req))