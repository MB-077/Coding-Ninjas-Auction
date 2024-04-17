from django.urls import path
from .views import leaderboard_view, group_list

urlpatterns = [
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('groups/', group_list, name='group_list'),
    # other URL patterns
]