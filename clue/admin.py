from django.contrib import admin
from .models import *


# class ClueAdmin(admin.ModelAdmin):
#     search_fields = ("clue",)


# class WordAdmin(admin.ModelAdmin):
#     list_display = (
#         "clue",
#         "word",
#         "year",
#         "publish_date",
#     )

#     search_fields = [
#         "clue__clue",
#         "word",
#         "year",
#         "publish_date",
#     ]


# class BlogAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "active",
#         "clue_count",
#         "publish_date",
#     )

#     search_fields = [
#         "title",
#         "active",
#         "clue_count",
#         "publish_date",
#     ]


# class BlogClueAdmin(admin.ModelAdmin):
#     list_display = (
#         "blog",
#         "clue",
#         "publish_date",
#     )

#     search_fields = [
#         "blog__title",
#         "clue__clue",
#         "publish_date",
#     ]


# class WorkerResultAdmin(admin.ModelAdmin):
#     list_display = (
#         "clue_added",
#         "blog_created",
#     )

#     search_fields = [
#         "clue_added",
#         "blog_created",
#     ]


# admin.site.register(subscribe)
# admin.site.register(Clue, ClueAdmin)
# admin.site.register(Blog, BlogAdmin)
# admin.site.register(BlogClue, BlogClueAdmin)
# admin.site.register(Word, WordAdmin)
# admin.site.register(WorkerResult)
admin.site.register(ClueMain)
