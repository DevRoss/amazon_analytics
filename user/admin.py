from django.contrib import admin
from .models import AmazonUser
# Register your models here.


@admin.register(AmazonUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'member')