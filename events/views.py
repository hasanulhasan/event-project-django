from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Category, Participant
import datetime

def home(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    context = {
        'events': events
        }
    return render(request, "home.html", context)

def details(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    
    context = {
        'event': event
        }
    return render(request, "details.html", context)

def dashboard(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()

    total_events = events.count()
    total_participants = Participant.objects.count()
    upcoming_events = events.filter(date__gte=datetime.date.today()).order_by('date').all().count()
    past_events = events.filter(date__lt=datetime.date.today()).order_by('-date').all().count()

    today = datetime.date.today()
    events_by_status = Event.objects.all().order_by('date')

    # Add status property manually
    for event in events_by_status:
        event.status = "Upcoming" if event.date >= today else "Past"

    context = {
        'events': events,
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events_by_status': events_by_status,
    }

    return render(request, "dashboard.html", context)