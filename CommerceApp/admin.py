from django.contrib import admin
from CommerceApp.models import category,Products,Order,OrderItem,Review,Contact,User,visitor


class orderiteminline(admin.TabularInline):
    model=OrderItem
    raw_id_fields=['product']
    
class orderadmin(admin.ModelAdmin):
    inlines=[orderiteminline]
    list_display=['id','status','created_at']
    list_filter=['status','created_at']
    search_fields=['first_name','address']
admin.site.register(category)
admin.site.register(Products)
admin.site.register(OrderItem)
admin.site.register(Order,orderadmin)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(visitor)
