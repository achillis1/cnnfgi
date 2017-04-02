from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.
from cnnfgiapp.models import Fgi

@admin.register(Fgi)
class FgiAdmin(VersionAdmin):
    fieldsets = [
        ('Information', {'fields': ['index',
                                    ]}),
    ]
    list_display = ('id', 'index')
    search_fields = ['id', 'index']
    list_filter = ['index']
