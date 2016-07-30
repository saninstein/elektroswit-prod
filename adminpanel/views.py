from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from adminpanel.form import PhoneForm, TabletForm, NotebookForm, SlideForm, AccessoriesForm, ForHomeForm, ForMasterForm, \
    InfoForm, ClientForm
from shop.models import *
from shop.views import get_item
import pickle


def is_su(user):
    return user.is_superuser


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def general(req):
    args = dict()
    return render_to_response('admin_general/index.html', args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def new_item(req, category='', inv=''):
    args = dict()
    args.update(csrf(req))
    if inv:
        item = get_item(inv)
        item_inv = item.inv
    else:
        item = None
        item_inv = False
    if req.method == 'POST':
        if category == 'phone':
            args['category'] = 'Смартфон'
            form = PhoneForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'phone', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'phone'})
        elif category == 'notebook':
            args['category'] = 'Ноутбук'
            form = NotebookForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'notebook', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'notebook'})
        elif category == 'tablet':
            args['category'] = 'Планшет'
            form = TabletForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'tablet', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'tablet'})
        elif category == 'accessories':
            args['category'] = 'Аксессуар/Комплектующие'
            form = AccessoriesForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'accessories', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'accessories'})
        elif category == 'appliances':
            args['category'] = 'Бытовая Техника'
            form = ForHomeForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'appliances', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'appliances'})
        elif category == 'master-tools':
            args['category'] = 'Для Мастера'
            form = ForMasterForm(req.POST, req.FILES, instance=item or None)
            if form.is_valid():
                item = form.save(commit=False)
                form.save()
                return redirect(item.get_item())
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'master-tools', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'master-tools'})
        args['form'] = form
        return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))
    else:
        if item:
            catg = item.link_category_id
        else:
            catg = False
        if category == 'phone' or catg == 1:
            args['category'] = 'Смартфон'
            args['form'] = PhoneForm(instance=item or None)
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'phone', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'phone'})
        elif category == 'notebook' or catg == 3:
            args['category'] = 'Ноутбук'
            args['form'] = NotebookForm(instance=item or None)
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'notebook', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'notebook'})
        elif category == 'tablet' or catg == 2:
            args['form'] = TabletForm(instance=item or None)
            args['category'] = 'Планшет'
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'tablet', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'tablet'})
        elif category == 'accessories' or catg in [4, 5, 6]:
            args['form'] = AccessoriesForm(instance=item or None)
            args['category'] = 'Аксессуар/Комплектующие'
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'accessories', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'accessories'})
        elif category == 'master-tools' or catg in [7, 8, 9]:
            args['form'] = ForMasterForm(instance=item or None)
            args['category'] = 'Для Мастера'
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'master-tools', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'master-tools'})
        elif category == 'appliances' or catg in [10, 11, 12, 13]:
            args['form'] = ForHomeForm(instance=item or None)
            args['category'] = 'Бытовая Техника'
            if item_inv:
                args['url'] = reverse('new_item', kwargs={'category': 'appliances', 'inv': item_inv})
            else:
                args['url'] = reverse('add_item', kwargs={'category': 'appliances'})
    return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def slide_edit(req, num=''):
    args = dict()
    args.update(csrf(req))
    slides = ['1', '2', '3', '4']
    if num in slides:
        try:
            slide = Slide.objects.get(pk=num)
        except Slide.DoesNotExist:
            return redirect('general')
        if req.method == 'POST':
            form = SlideForm(req.POST, req.FILES, instance=slide)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                args['category'] = 'Слайд ' + str(slide.id)
                args['form'] = form
                args['url'] = reverse('slide_edit', kwargs={'num': num})
                return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))
        else:
            args['category'] = 'Слайд ' + str(slide.id)
            args['form'] = SlideForm(instance=slide)
            args['url'] = reverse('slide_edit', kwargs={'num': num})
            return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))
    else:
        return redirect('general')


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def show_items(req, category='', client=''):
    args = dict()
    args.update(csrf(req))
    if category == 'phone':
        args['items'] = Phone.objects.all()
    elif category == 'tablet':
        args['items'] = Tablet.objects.all()
    elif category == 'notebook':
        args['items'] = Notebook.objects.all()
    elif category == 'accessories':
        args['items'] = Accessories.objects.all()
    elif category == 'appliances':
        args['items'] = ForHome.objects.all()
    elif category == 'master-tools':
        args['items'] = ForMaster.objects.all()
    elif category == 'share':
        args['share'] = True
        objs = Share.objects.all().values()
        args['items'] = list()
        for obj in objs:
            args['items'].append(dict(gen_item=get_item(str(obj['gen_item'])).name, sec_item=get_item(str(obj['sec_item'])).name,
                                      inv=obj['inv'], discount=obj['discount']))
    elif category == 'order':
        if client:
            orders = Order.objects.filter(link_client=client).values()
        else:
            orders = Order.objects.values()
        for order in orders:
            items = pickle.loads(order['items'])
            order['items'] = ''
            for item, count in items:
                item = get_item(str(item))
                if item:
                    order['items'] += '{1}x<a href="{2}">{0}</a><br>'.format(item.name, count, item.get_item())
                    if item.price_opt and count > 1:
                        order.update(price=item.price_opt * count)
                    else:
                        order.update(price=item.price * count)
                else:
                    order['items'] += 'Данный товар отсутсвует<br>'
        args['orders'] = orders
        return render_to_response('show_orders/index.html', args, context_instance=RequestContext(req))
    elif category == 'clients':
        args = dict()
        args['clients'] = Client.objects.all()
        return render_to_response('show_clients/index.html', args, context_instance=RequestContext(req))
    else:
        return redirect('admingeneral')

    if not args['items']:
        return redirect('admingeneral')
    else:
        if 'share' in args:
            args['category'] = 'Акции'
        else:
            args['category'] = args['items'][0].link_category.name
    return render_to_response('show_all/index.html', args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def delete_item(req):
    if req.method == 'POST':
        try:
            item = get_item(req.POST.get('item', ''))
            if not item:
                raise Share.DoesNotExist
            item.delete()
        except Share.DoesNotExist:
            return HttpResponse()
        else:
            return HttpResponse('OK')
    return HttpResponse()


def login(req):
    args = dict()
    args.update(csrf(req))
    if req.POST:
        username = req.POST.get('username', '')
        password = req.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            if user.is_superuser:
                return redirect('/adminpanel/')
            else:
                return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login/index.html', args, context_instance=RequestContext(req))
    else:
        return render_to_response('login/index.html', args, context_instance=RequestContext(req))


def logout(req):
    auth.logout(req)
    return redirect('/')


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def add_share(req):
    args = dict()
    args.update(csrf(req))
    if req.method == 'POST':
        item = Share(gen_item=req.POST['first'], sec_item=req.POST['second'], discount=req.POST['discount'])
        try:
            item.full_clean()
        except ValidationError:
            return HttpResponse()
        else:
            item.save()
            return HttpResponse('OK')

    else:
        return render_to_response('share_form/index.html', args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def ajax_search(req, search_str=""):
    args = dict()
    l = [list(x.objects.filter(name__icontains=search_str).only('name', 'inv')) for x in
         (Phone, Tablet, Notebook, Accessories, ForMaster, ForHome, Accessories)]
    res = list()
    for x in l:
        res += x
    del l
    args["items"] = res
    return render_to_response("adm_search/index.html", args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def info_edit(req, page=''):
    args = dict()
    if req.method == 'POST':
        if page == 'payment':
            args['category'] = "Оплата"
            form = InfoForm(req.POST, instance=Info.objects.get(pk=2))
        elif page == 'delivery':
            args['category'] = "Доставка"
            form = InfoForm(req.POST, instance=Info.objects.get(pk=3))
        elif page == 'about':
            form = InfoForm(req.POST, instance=Info.objects.get(pk=1))
            args['category'] = "О магазине"
        elif page == 'rmail':
            form = InfoForm(req.POST, instance=Info.objects.get(pk=4))
            args['category'] = "Реквизиты(для сообщений)"
        else:
            return redirect('admingeneral')
        if form.is_valid():
            form.save()
            return redirect('admingeneral')
        else:
            args['form'] = form
            args['url'] = reverse('info_edit', kwargs={'page': page})
            return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))
    else:
        if page == 'payment':
            args['category'] = "Оплата"
            form = InfoForm(instance=Info.objects.get(pk=2))
        elif page == 'delivery':
            args['category'] = "Доставка"
            form = InfoForm(instance=Info.objects.get(pk=3))
        elif page == 'about':
            form = InfoForm(instance=Info.objects.get(pk=1))
            args['category'] = "О магазине"
        elif page == 'rmail':
            form = InfoForm(instance=Info.objects.get(pk=4))
            args['category'] = "Реквизиты(для сообщений)"
        else:
            return redirect('admingeneral')
        args['form'] = form
        args['url'] = reverse('info_edit', kwargs={'page': page})
        return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))


@user_passes_test(is_su, login_url='/adminpanel/login/', redirect_field_name='')
def client_edit(req, client_id=''):
    args = dict()
    args.update(csrf(req))
    if client_id:
        try:
            client = Client.objects.get(id=client_id)
            args['category'] = 'Клиент ' + client.email
        except Client.DoesNotExist:
            return redirect('admingeneral')
        if req.method == 'POST':
            form = ClientForm(req.POST, instance=client)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                if obj.discount > 0:
                    send_mail(
                        'ELEKTROSWIT: Вам предоставляется скидка!',
                        'Поздравляем! При оформлении заказа по вашему e-mail вам будет предоставлена {0}% скидка!'.format(
                            obj.discount
                        ),
                        'elekto-swit@yandex.ru',
                        [obj.email],
                        fail_silently=True,
                    )
                return redirect('show', 'clients')
            else:
                args['form'] = form
        else:
            args['form'] = ClientForm(instance=client)
        return render_to_response('new_item/index.html', args, context_instance=RequestContext(req))
    return redirect('admingeneral')

