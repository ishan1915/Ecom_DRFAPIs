from django.contrib import admin
from .models import User,Product,Order
# Register your models here.
admin.site.register(User)
#admin.site.register(Product)
#admin.site.register(Order)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'price', 'quantity', 'category', 'created_at', 'image_preview')
    list_filter = ('category', 'created_at', 'seller')
    search_fields = ('name', 'description', 'category', 'seller__username')
    list_per_page = 20

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'quantity', 'ordered_at')
    list_filter = ('ordered_at', 'product__category')
    search_fields = ('product__name', 'buyer__username')
    list_per_page = 20