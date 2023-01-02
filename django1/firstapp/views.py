from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib import messages
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# generate PDF file venue list
def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.phone)
        lines.append(venue.email_address)
        lines.append("=============================")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# generate Text file venue list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.email_address}\n')

    response.writelines(lines)
    return response

# generate csv file venue list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    writer = csv.writer(response)

    venues = Venue.objects.all()

    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email Address'])

    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])

    return response

# Create your views here.
def all_events(request):
    event_list = Event.objects.all().order_by('name')
    return render(request, 'firstapp/eventslist.html', {'event_list': event_list})

def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    return render(request, 'firstapp/venues.html', {'venue_list': venue_list})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'firstapp/venuedetails.html', {'venue': venue, 'venue_owner': venue_owner})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'firstapp/addvenue.html', {'form': form, 'submitted': submitted})

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request, 'firstapp/updatevenue.html', {'venue': venue, 'form': form})

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()

    return redirect('list-venues')

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'firstapp/searchvenues.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'firstapp/searchvenues.html', {})

def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/firstapp/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                #form.save()
                return HttpResponseRedirect('add_event?submitted=True')

    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'firstapp/addevent.html', {'form': form, 'submitted': submitted})

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('events')

    return render(request, 'firstapp/updateevent.html', {'event': event, 'form': form})

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted Successfully!"))
        return redirect('events')
    else:
        messages.success(request, ("You Aren't Authorized to Delete this Event!"))
        return redirect('events')

def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):

    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    #get current time
    time = now.strftime('%Y-%m-%d-%I:%M %p')

    return render(request, 'firstapp/index.html', {"year": year, "month": month, "month_number": month_number, "cal": cal, "current_year": current_year, "time": time,})