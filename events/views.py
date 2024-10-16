from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Event, Booking, Attendee, Organizer, CustomUser, Ticket, Order, MpesaTransaction
from .forms import LoginForm, EventForm, BookingForm, RegisterAttendeeForm, RegisterOrganizerForm
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

def register_attendee(request):
    if request.method == 'POST':
        form = RegisterAttendeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'attendee'
            user.save()
            attendee = Attendee.objects.create(
                user=user,
                phone_number=user.phone_number,
            )
            attendee.save()
            return redirect('login')
    else:
        form = RegisterAttendeeForm()
    return render(request, 'register_attendee.html', {'form': form})

def register_organizer(request):
    if request.method == 'POST':
        form = RegisterOrganizerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'organizer'
            user.save()
            organizer = Organizer.objects.create(
                user=user,
                phone_number=user.phone_number,
            )
            organizer.save()
            return redirect('login')
    else:
        form = RegisterOrganizerForm()
    return render(request, 'register_organizer.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'attendee':
                return redirect('attendee_dashboard')
            elif user.user_type == 'organizer':
                return redirect('organizer_dashboard')
        else:
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

@login_required
def create_event(request):
    if request.user.user_type == 'organizer':
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user.organizer
                event.save()
                return redirect('home')
        else:
            form = EventForm()
        return render(request, 'event_form.html', {'form': form})
    else:
        return redirect('home')

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user.organizer)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            ticket_id = request.POST.get('ticket_id')
            print(f"Received ticket_id: {ticket_id}")  # Add this line
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                print(f"Found ticket: {ticket}")  # Add this line
            except Ticket.DoesNotExist:
                print(f"Ticket with id {ticket_id} does not exist")  # Add this line
                # Handle the case when the ticket does not exist
                return render(request, 'booking_form.html', {'form': form, 'event': event, 'error': 'Invalid ticket selected'})
            booking = form.save(commit=False)
            booking.event = event
            booking.attendee = request.user
            booking.save()
            return redirect('booked_events')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'event': event})

@login_required
def booked_events(request):
    if request.user.user_type == 'organizer':
        booked_events = Event.objects.filter(organizer=request.user.organizer)
    else:
        booked_events = Booking.objects.filter(attendee=request.user)
    return render(request, 'booked_events.html', {'booked_events': booked_events})

def organizer_dashboard(request):
    return render(request, 'organizer_dashboard.html')

def attendee_dashboard(request):
    return render(request, 'attendee_dashboard.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def mpesa(request):
    cl = MpesaClient()
    phone_number = '0706680019'  # Use a valid Safaricom phone number
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://mydomain.com/path'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    print(response)
    return HttpResponse(response)

def stk_push_callback(request):
    data = request.body
    # Handle the callback response from M-Pesa
    # ...
    return HttpResponse("STK Push in Django👋")