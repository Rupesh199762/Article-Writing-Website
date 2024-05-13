from django.contrib import admin
from .models import BondModel

class BondAdmin(admin.ModelAdmin):
    list_display = ("bond_id","date_of_purchase","name_of_purchaser","date_of_expiry","name_of_political_party","date_of_encashment","denomination","status","short_name")


admin.site.register(BondModel,BondAdmin)



# Register your models here.
