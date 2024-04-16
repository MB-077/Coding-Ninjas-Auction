from django.shortcuts import render

# Create your views here.

def leaderboard_view(request):
    return render(request, 'leaderboard.html')