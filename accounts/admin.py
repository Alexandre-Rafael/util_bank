from django.contrib import admin

from .models import User, UserBankAccount


admin.site.register(User)
admin.site.register(UserBankAccount)
