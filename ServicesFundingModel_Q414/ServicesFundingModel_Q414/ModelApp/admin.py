from django.contrib import admin
from ModelApp.models import *

class RolePropertiesInline(admin.StackedInline):
	model = RoleProperties
	extra = 1
	
class RoleAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	inlines = [RolePropertiesInline]

class PlatformProductPropertiesInline(admin.StackedInline):
	model = PlatformProductProperties

class PlatformProductWorkingValue(admin.TabularInline):
	model = PlatformProductWorkingValue
	extra = 2

class PlatformProductAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	inlines = [PlatformProductPropertiesInline, PlatformProductWorkingValue]
	
class GSSProductPropertiesInline(admin.StackedInline):
	model = GSSProductProperties

class GSSProductWorkingValue(admin.TabularInline):
	model = GSSProductWorkingValue
	extra = 3

class GSSProductAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	inlines = [GSSProductPropertiesInline, GSSProductWorkingValue]
	
class TimeAndMaterialsPropertiesInline(admin.StackedInline):
	model = TimeAndMaterialsProperties

class TimeAndMaterialsWorkingValue(admin.TabularInline):
	model = TimeAndMaterialsWorkingValue
	extra = 2

class TimeAndMaterialsAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	inlines = [TimeAndMaterialsPropertiesInline, TimeAndMaterialsWorkingValue]

class PlatformProductForecastAdmin(admin.ModelAdmin):
	search_fields = ('product__name',)
	
admin.site.register(Role, RoleAdmin)
admin.site.register(PlatformProduct, PlatformProductAdmin)
admin.site.register(GSSProduct, GSSProductAdmin)
admin.site.register(TimeAndMaterials, TimeAndMaterialsAdmin)
admin.site.register(GDRAT)
admin.site.register(PlatformProductForecast, PlatformProductForecastAdmin)
admin.site.register(Year)
