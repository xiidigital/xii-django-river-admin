from django.contrib import admin

from xii.django_river_admin import RiverAdmin, site
from examples.shipping_example.models import Shipping


class ShippingRiverAdmin(RiverAdmin):
    name = "Shipping Flow"
    icon = "mdi-truck"
    list_displays = ['pk', 'product', 'customer', 'shipping_status']


site.register(Shipping, "shipping_status", ShippingRiverAdmin)


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'customer', 'shipping_status',)
    readonly_fields = ('shipping_status',)


admin.site.register(Shipping, ShippingAdmin)
