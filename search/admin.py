from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Article)
admin.site.register(Word)
admin.site.register(Stoplist)
admin.site.register(Postingfile)
