from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Sum
from Teams.models import Team
from Players.models import Group

# Create your views here.

def leaderboard_view(request):
    return render(request, 'leaderboard.html')

def group_list(request):
    # Fetch all teams and groups
    teams = Team.objects.all()
    groups = Group.objects.all()

    # Fetch existing assignments from session first
    previous_assignment = request.session.get('existing_assignments', [])

    # Check for new group assignments and update purse value accordingly
    existing_assignments = set(group.group_id for group in groups if group.alloted_team_id is not None)
    print(f"Existing Assignments: {existing_assignments}")

    for group in groups:
        # Check if the group was previously assigned to any team
        if group.group_id in existing_assignments and group.group_id not in previous_assignment:
            team = Team.objects.get(team_id=group.alloted_team_id)
            team.purse_value -= group.group_price
            team.save()
            print(f"Deducted group price from purse value for Group ID - {group.group_id}")

    # Store existing assignments in session
    request.session['existing_assignments'] = list(existing_assignments)

    # Pass the data to the template
    context = {
        'teams': teams,
        'groups': groups,
    }

    return render(request, 'group_list.html', context)