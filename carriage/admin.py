from django.contrib import admin
from carriage.models import list_of_models

for x in list_of_models:
    admin.site.register(x)

