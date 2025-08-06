from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from events.models import Event, Category, Participant
import datetime
from django.db.models import Q
from events.forms import EventForm, AddParticipantForm, CategoryForm
from django.contrib import messages

def home(request):
    query = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participants').all()

    if query:
        events = events.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

    context = {
        'events': events,
        'query': query,
    }
    return render(request, "home.html", context)

def details(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    
    context = {
        'event': event
    }
    return render(request, "details.html", context)

def dashboard(request):
    type = request.GET.get('type', 'all')

    events = Event.objects.select_related('category').prefetch_related('participants').all()
    total_events = events.count()
    total_participants = Participant.objects.count()
    upcoming_events = events.filter(date__gte=datetime.date.today()).order_by('date').all().count()
    past_events = events.filter(date__lt=datetime.date.today()).order_by('-date').all().count()
    today_events = events.filter(date=datetime.date.today()).all()

    today = datetime.date.today()
    events_by_status = Event.objects.all().order_by('date')

    base_query = events

    if type == 'upcoming':
        events = base_query.filter(date__gte=datetime.date.today()).order_by('date')
    elif type == 'past':
        events = base_query.filter(date__lt=datetime.date.today()).order_by('-date')
    else:
        events = base_query.order_by('date')

    # Add status property manually
    for event in events_by_status:
        event.status = "Upcoming" if event.date >= today else "Past"

    context = {
        'events': events,
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'today_events': today_events,
        'events_by_status': events_by_status,
    }

    return render(request, "dashboard.html", context)

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you want to redirect
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

def update_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully")
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)

    return render(request, 'update_event.html', {'form': form, 'event': event})

def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('dashboard')
    else:
        messages.error(request, "Something went wrong, please try again.")
        return redirect('dashboard')
    
def add_participant(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            participant.events.add(event)
            return redirect('details', id=event.id)
    else:
        form = AddParticipantForm()

    return render(request, 'add_participant.html', {'form': form, 'event': event})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you want to redirect
    else:
        form = CategoryForm()
    return render(request, 'create-category.html', {'form': form})