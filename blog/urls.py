## Create app-specific URL:
# blog/urls.py
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views    ## Authentication Package

urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name='random'), ## new
    path('show_all', ShowAllView.as_view(), name='show_all_articles'), ## refactored
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ##With PK
    path('create_article', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),

    #Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_articles'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
]