from django.urls import path

from .views import *

urlpatterns = [
    path('process/' , process_payment , name='order_process'),
    path('payment_callback/' ,payment_callback , name='payment_callback' ),
    path('buy/' , new_account , name="new_account"),
    path('confirmation/' , emailauth , name='confirmation'),
]