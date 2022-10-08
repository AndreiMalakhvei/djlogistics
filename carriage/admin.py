from django.contrib import admin

from carriage.models import CustTerritory, Country, City, Coefficient, Way

for x in (CustTerritory, Country, City, Coefficient, Way):
    admin.site.register(x)

