from django.conf.urls import url
from lunches import views


api_url = 'api_v1/'

urlpatterns = [
    url(r'^{}menu/$'.format(api_url), views.MenuToday.as_view()),
    url(r'^{}orders/$'.format(api_url), views.OrdersListCreate.as_view()),
    url(r'^{}orders/(?P<pk>[0-9]+)/$'.format(api_url), views.OrdersDetail.as_view()),
    url(r'^{}items/(?P<pk>[0-9]+)/$'.format(api_url), views.Item.as_view())
]
