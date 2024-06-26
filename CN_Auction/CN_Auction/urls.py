"""
URL configuration for CN_Auction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Teams.views import leaderboard_view, group_list, question_view, allot_data


urlpatterns = [
    path('admin/', admin.site.urls),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('groups/', group_list, name='group_list'),
    path('', question_view, name='questions'),
    path('allot_data/', allot_data, name='allot_data'),
]
