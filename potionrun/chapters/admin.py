from django.contrib import admin
from .models import Chapter, Act, Scene

class SceneInline(admin.TabularInline):
    model = Scene
    extra = 3  # 3 scènes par acte

class ActInline(admin.TabularInline):
    model = Act
    extra = 7  # 7 actes par chapitre
    inlines = [SceneInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    inlines = [ActInline]
    list_display = ('name', 'description', 'completed_sessions', 'associated_routes')
    search_fields = ('name', 'description')

@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'number', 'cr_duration')
    list_filter = ('chapter',)
    search_fields = ('chapter__name', 'description')

@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('act', 'number', 'cl_duration', 'cr_duration')
    list_filter = ('act__chapter', 'act')
    search_fields = ('act__chapter__name', 'instructions')
