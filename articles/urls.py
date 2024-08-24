from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('category/<str:category_name>/', views.category_page, name='category_page'),
    path('chatbox/', views.chat_with_bot, name='chat_with_bot'),
    path('sse-updates/', views.sse_view, name='sse_view'),
    path('search/', views.search_articles, name='search_articles'),
    path('category/<str:category_name>/', views.category_page, name='category_page'),
    path('website/<str:website_name>/', views.website_page, name='website_page'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('bookmark/', views.bookmark_article, name='bookmark_article'),


    
]
