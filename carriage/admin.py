from django.contrib import admin
from carriage.models import list_of_models, ContactRequest


class ContactRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'req_date'
    search_fields = ['fname', 'subject', 'body']
    list_filter = ['req_date', 'fname', 'mail']


for x in list_of_models:
    admin.site.register(x)

admin.site.register(ContactRequest, ContactRequestAdmin)
