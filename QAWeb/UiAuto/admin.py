from django.contrib import admin
from UiAuto.models import UIAutoScenario,UIAutoCode

# Register your models here.
class UIAutoSAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    fields =('scenarioId','desc','steps')
class UIAutoCAdmin(admin.ModelAdmin):
    actions_on_bottom = True

admin.site.register(UIAutoScenario,UIAutoSAdmin)
admin.site.register(UIAutoCode,UIAutoCAdmin)