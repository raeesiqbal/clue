from django.contrib import admin
from .models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "active",
        "clue_count",
        "publish_date",
    )

    search_fields = [
        "title",
        "active",
        "clue_count",
        "publish_date",
    ]


class BlogClueAdmin(admin.ModelAdmin):
    list_display = (
        "blog",
        "clue",
        "publish_date",
    )

    search_fields = [
        "blog__title",
        "clue__clue",
        "publish_date",
    ]


class WorkerResultAdmin(admin.ModelAdmin):
    list_display = (
        "clue_added",
        "blog_created",
    )

    search_fields = [
        "clue_added",
        "blog_created",
    ]


class ClueMainAdmin(admin.ModelAdmin):
    list_display = (
        "clue",
        "answer",
    )

    search_fields = [
        "clue",
        "answer",
    ]


admin.site.register(subscribe)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogClue, BlogClueAdmin)
admin.site.register(WorkerResult)
admin.site.register(ClueMain, ClueMainAdmin)
