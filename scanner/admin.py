from django.contrib import admin
from .models import IntakeItem, Asset, CustodyLocation

admin.site.register(IntakeItem)
admin.site.register(Asset)
admin.site.register(CustodyLocation)