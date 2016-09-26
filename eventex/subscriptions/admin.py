from django.contrib import admin
from django.utils.timezone import now
from eventex.subscriptions.models import Subscription


# TODO: Test this somehow
class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf', 'email', 'phone', 'created_at', 'subscribed_today', 'paid']
    date_hierarchy = 'created_at'
    search_fields = ['name', 'cpf', 'email', 'phone', 'created_at', 'paid']
    list_filter = ['paid', 'created_at']

    actions = ['mark_as_paid']

    def subscribed_today(self, obj):
        return obj.created_at.date() == now().date()

    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True

    def mark_as_paid(self, request, queryset):
        rows_updated = queryset.update(paid=True)
        if rows_updated == 1:
            message_bit = '1 incrição foi marcada'
        else:
            message_bit = '{} inscrições foram marcadas'.format(rows_updated)
        self.message_user(request, '{} como paga com sucesso.'.format(message_bit))

    mark_as_paid.short_description = 'Marcar como pago'

admin.site.register(Subscription, SubscriptionModelAdmin)
