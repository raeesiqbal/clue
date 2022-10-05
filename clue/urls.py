from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("blog/", views.myblog),
    path("blog-detail/<int:id>", views.blog_detail, name="blog_detail"),
    path("clue-word/<str:clue>", views.clue_word, name="clue_words"),
    path("subscribe/", views.subscribeview),
    path("add-clue", views.addClue, name="add_clue"),
]
