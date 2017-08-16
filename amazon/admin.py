from django.contrib import admin
from .models import TopSeller


# Register your models here.

@admin.register(TopSeller)
class TopSellerAdmin(admin.ModelAdmin):
    # id, title, create_time, result_file, origin_file, user_id
    fields = ('title', 'user', 'origin_file')
