from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name="home-page"),
    path("post/<slug:slug>/", views.post_detail, name="blog-post-detail"),
]