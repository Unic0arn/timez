from django.contrib import admin

from .models import *
# Register your models here.

class ShiftAdmin(admin.ModelAdmin):
    readonly_fields = ('length',)
    list_display = ('start_time','end_time','length')
    
class ShiftFragmentAdmin(admin.ModelAdmin):
    readonly_fields = ('length',)
    list_display = ('start_time','end_time','oblevel','length')

class ShiftDefaultAdmin(admin.ModelAdmin):
    readonly_fields = ('length',)
    list_display = ('name','start_time','length')
    
    
admin.site.register(ShiftDefault,ShiftDefaultAdmin)    
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftFragment, ShiftFragmentAdmin)
admin.site.register(ObLevel)
admin.site.register(ObSpecials)
admin.site.register(ObTimes)
admin.site.register(Day)
admin.site.register(MonthlyReport)