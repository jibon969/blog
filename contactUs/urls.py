from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('contact-list/', views.contact_list, name='contact-list'),
    path('update-contact/<int:id>/', views.update_contact, name='update-contact'),
    path('delete-contact/<int:id>/', views.delete_contact, name='delete-contact'),
    path('replay-customer/', views.replay_customer, name='replay-customer')
]