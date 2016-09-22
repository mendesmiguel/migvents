from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from django.http import Http404


def new_subscription(request):
    if request.method == 'POST':
        return create(request)
    return empty_form(request)


def empty_form(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_mail('Confirmação de Inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscriptions/subscription_mail.txt',
               {'subscription': subscription})

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404()
    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})


def _send_mail(subject, from_email, to, template_name, context):
    body = render_to_string(template_name, context)

    mail.send_mail(subject, body, from_email, [from_email, to])
