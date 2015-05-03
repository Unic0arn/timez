from django.contrib import admin

from .models import *
# Register your models here.

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('worker', 'start_time','end_time','length')
    
class ShiftFragmentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'start_time','end_time','oblevel','length')

admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftFragment, ShiftFragmentAdmin)
admin.site.register(ObLevel)
admin.site.register(ObSpecials)
admin.site.register(ObTimes)