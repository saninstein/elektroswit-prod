from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r'^$', views.general, name='general'),
    url(r'^item/(?P<item>\d+)/$', views.item, name='item_phone'),
    url(r'^phone/(?P<item>\d+)/$', views.item_phone, name='item_phone'),
    url(r'^phones/$', views.phones, name='phones'),
    url(r'^tablets/$', views.tablets, name='tablets'),
    url(r'^notebooks/$', views.notes, name='notes'),
    url(r'^search/(?P<search_str>[\w\-]+)/$', views.all_search),
    url(r'^phones/search/(?P<search_str>[\w\-]+)/$', views.phones_search),
    url(r'^ajax_search/(?P<search_str>[\w\-]+)/$', views.search),
    url(r'^ajax_phone_filter/(?P<filter_str>[\w\-]+)/$', views.phone_filter),
    url(r'^ajax_phone_filter/$', views.phone_filter),
    url(r'^ajax_tablet_filter/(?P<filter_str>[\w\-]+)/$', views.tablet_filter),
    url(r'^ajax_tablet_filter/$', views.tablet_filter),
    url(r'^ajax_notes_filter/(?P<filter_str>[\w\-]+)/$', views.note_filter),
    url(r'^ajax_notes_filter/$', views.note_filter),
    url(r'^ajax_like/(?P<item>\d+)/$', views.like),
    url(r'^ajax_addbasket/$', views.add_basket),
    url(r'^ajax_remove_from_basket/$', views.add_basket, {'remove': True}),
    url(r'^other/(?P<category>[\w\-]+)/(?P<subcategory>\d+)/$', views.other_category, name='other_subcategory'),
    url(r'^other/(?P<category>[\w\-]+)/$', views.other_category, name='other_category'),
    url(r'^show_basket/$', views.show_basket, name='show_basket'),
    url(r'^add_order/$', views.add_order, name='add_order'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^info/(?P<category>[\w\-]+)/$', views.info, name='info'),
]