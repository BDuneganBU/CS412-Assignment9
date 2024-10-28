## Create app-specific URL:
# mini_fb/urls.py
from django.urls import path
from . import views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.ShowAllProfilesView.as_view(), name='show_all'), # generic class-based view
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('createProfile', views.CreateProfileView.as_view(), name='createProfile'),
    path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='create_friend'),
    path('profile/<int:pk>/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
]