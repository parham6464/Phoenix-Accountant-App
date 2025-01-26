from django.shortcuts import render , get_object_or_404 , HttpResponse , redirect 
from django.urls import reverse

import requests
from django.contrib import messages

import json
from .models import Order
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password , check_password
import time
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404

# Create your views here.


def process_payment(request):

    order = get_object_or_404(Order , session = request.session['emailauth'])

    if request.POST['answer'] != order.code_mail:
        messages.warning('کد وارد شده اشتباه است')
        return redirect('confirmation')

    total_price = 5000

    total_price_rial = total_price * 10

    zarinpal_url= "https://api.zarinpal.com/pg/v4/payment/request.json"

    headers = {
        "accept":"application/json",
        "content-type":"application/json",
    }

    request_data ={
        "merchant_id":'6ce23435-9d94-44b3-8de3-b0c9e6a3ed1d',
        "amount":total_price_rial,
        "callback_url":request.build_absolute_uri(reverse('payment_callback')),
        "description":f"خرید اشتراک اپلیکیشن حسابداری ققنوس"

    }

    res = requests.post(zarinpal_url , data=json.dumps(request_data) , headers=headers)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) ==0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error from Zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get("Status")

    if payment_status == 'OK':
    
        order = get_object_or_404(Order , zarinpal_authority=payment_authority)
        total_price = 5000

        total_price_rial = total_price * 10

        headers = {
            "accept":"application/json",
            "content-type":"application/json",
        }

        request_data ={
            "merchant_id":'6ce23435-9d94-44b3-8de3-b0c9e6a3ed1d',
            "amount":total_price_rial,
            "authority":payment_authority

        }

        res=requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json' , data=json.dumps(request_data) , headers=headers)

        data=res.json()['data']

        if 'errors' not in data or len(data['errors']) ==0:
            if len(data) !=0:
                payment_code = data['code']

                if payment_code == 100:
                    order.is_paid = True
                    order.ref_id = data['ref_id']
                    order.zarinpal_data = data
                    order.is_paid = True
                    order.save()

                    timer = int(time.time())
                    timer_30 = 2592000 + timer
                    CustomUser.objects.create(username=order.username , password=make_password(order.password) , email=order.email ,lisence=timer_30)
                

                    return render(request , 'payment-success.html' , context={"username":order.username , "password":order.password})
                elif payment_code ==101:
                    return HttpResponse("پرداخت شما با موفقیت انجام شده است از قبل")
                
                else:
                    return HttpResponse("پرداخت انجام نشد")
                    

            else:
                return HttpResponse("پرداخت انجام نشد")

        else:
            return HttpResponse("پرداخت انجام نشد")
    else:
        return HttpResponse("پرداخت انجام نشد")




def new_account(request):
    if request.method =="POST":
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))

        request.session['emailauth'] = result_str
        all_users = CustomUser.objects.all()
        for i in all_users:
            if i.email == request.POST['email']:
                messages.warning(request , 'این ایمیل قبلا ثبت شده است')
                return redirect('new_account')
            if i.username == request.POST['username']:
                messages.warning(request , 'این آیدی قبلا ثبت شده است')
                return redirect('new_account')

        try:
            order = Order.objects.all().filter(username=request.POST['username'] , is_paid = False)
            order.delete()
            order=Order.objects.create(username=request.POST['username'] , password=request.POST['password'] , email=request.POST['email'] , session=result_str  , is_paid = False)
                
        except:    
            order=Order.objects.create(username=request.POST['username'] , password=request.POST['password'] , email=request.POST['email'] , session=result_str , is_paid = False )

        return redirect('confirmation')
    else:
        return render(request,'payment-form.html')


def emailauth(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        raise Http404

    order = get_object_or_404(Order , session = request.session['emailauth'] , is_paid = False)
    letters = ['1','2','3','4','5','6','7','8','9','0']
    result_str = ''.join(random.choice(letters) for i in range(6))
    order.code_mail = result_str
    order.save()
    send_list = []
    send_list.append(order.email)
    send_mail(subject='تایید حساب کاربری ققنوس' , message=f'لطفا کد تایید را در فرم وارد کنید تا ایمیل شما تایید شود \n کد تایید : {result_str}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=send_list)
    return render(request , 'emailauth.html')

