from django.conf.urls import url
from adminpanel import views

urlpatterns = [
    url(r'^$', views.general, name='admingeneral'),
    url(r'^new/(?P<category>[\w\-]+)/item=(?P<inv>\d+)/$', views.new_item, name='new_item'),
    url(r'^new/(?P<category>[\w\-]+)/$', views.new_item, name='add_item'),
    url(r'^edit/(?P<inv>\d+)/$', views.new_item, name='edit_item'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'edit_slide/(?P<num>\d+)/$', views.slide_edit, name='slide_edit'),
    url(r'^show/(?P<category>[\w\-]+)/$', views.show_items, name='show'),
    url(r'^show/order/(?P<client>\d+)/$', views.show_items, {'category': 'order'}, name='show_client_orders'),
    url(r'^ajax_delete/$', views.delete_item),
    url(r'^add_share/$', views.add_share, name='add_share'),
    url(r'^ajax_adm_search/(?P<search_str>[\w\-]+)/$', views.ajax_search),
    url(r'^info/(?P<page>[\w\-]+)/$', views.info_edit, name='info_edit'),
    url(r'^discount/(?P<client_id>\d+)/$', views.client_edit, name='client_edit'),
]