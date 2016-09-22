from django.conf.urls import url
from eventex.subscriptions.views import new_subscription, detail

urlpatterns = [
    url(r'^$', new_subscription, name='new'),
    url(r'^(\d+)/$', detail, name='detail')
]