from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(Watchlist)