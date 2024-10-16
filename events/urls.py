# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerattendee/', views.register_attendee, name='register_attendee'),
    path('registerorganizer/', views.register_organizer, name='register_organizer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    path('events/<int:event_id>/book/', views.book_event, name='book_event'),
    path('booked_events/', views.booked_events, name='booked_events'),
    path('organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('attendee/', views.attendee_dashboard, name='attendee_dashboard'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('mpesa/', views.mpesa, name='mpesa'),
    path('stk_push_callback/', views.stk_push_callback, name='stk_push_callback'),
]