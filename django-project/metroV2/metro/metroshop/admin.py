from django.contrib import admin
from django.contrib.admin.models import LogEntry
LogEntry.objects.all().delete()
# Register your models here.
from metroshop.models import Master_config
#admin.site.register(Master_config)

from metroshop.models import Product
#admin.site.register(Product)



