from django.contrib import admin
from ApiAuto.models import ApiAutoCode,ApiAutoScenario

# Register your models here.
class ApiAutoSAdmin(admin.ModelAdmin):
    fields =('scenarioId','desc','steps','isAutomated')
    list_display=('desc','createDate','lastUdpateDate','isAutomated')
    actions = ['make_automated']  
    
    def make_automated(self, request, queryset):
        queryset.update(isAutomated=True)
    make_automated.short_description = "Mark selected stories as automated"

class ApiAutoCAdmin(admin.ModelAdmin):
    list_display=('sautoId','createDate','lastUdpateDate')

admin.site.register(ApiAutoScenario,ApiAutoSAdmin)
admin.site.register(ApiAutoCode,ApiAutoCAdmin)