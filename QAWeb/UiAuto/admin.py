from django.contrib import admin
from UiAuto.models import UIAutoScenario,UIAutoCode

# Register your models here.
class UIAutoSAdmin(admin.ModelAdmin):
    fields =('scenarioId','desc','steps','isAutomated')
    list_display=('desc','createDate','lastUdpateDate','isAutomated')
    actions = ['make_automated']  
    
    def make_automated(self, request, queryset):
        queryset.update(isAutomated=True)
    make_automated.short_description = "Mark selected stories as automated"

class UIAutoCAdmin(admin.ModelAdmin):
    list_display=('sautoId','createDate','lastUdpateDate')

admin.site.register(UIAutoScenario,UIAutoSAdmin)
admin.site.register(UIAutoCode,UIAutoCAdmin)