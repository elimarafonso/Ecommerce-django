from django.contrib import admin


from .models import Payment, OrderProduct, Order


@admin.register(Payment)
class Payment(admin.ModelAdmin):
    pass
    # fields = ('__all__',)

@admin.register(OrderProduct)
class OrderProduct(admin.ModelAdmin):
    pass
    # fields = ('__all__',)

@admin.register(Order)
class Order(admin.ModelAdmin):
    pass
    # fields = ('__all__',)
