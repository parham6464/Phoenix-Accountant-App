from tkinter import E
from unicodedata import category, name
from django.shortcuts import render , get_object_or_404
from django.views.generic import TemplateView , CreateView

from .forms import CustomCreationForm
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate , login , logout 

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 
from django.contrib.auth.decorators import login_required
from json import JSONDecoder, JSONEncoder ,dumps , loads
from django.http import JsonResponse
from .models import *
from .forms import *
import string
import random
from .serializers import AsnadSerializer, HesabhaSerializer , CategorySerializer
import re
import ast
from .doc import docx_generator
import time
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from payment.models import Order
import json
# Create your views here.


# class SignUp(CreateView):
#     form_class = CustomCreationForm
#     template_name = 'registration/signup.html'
#     success_url = reverse_lazy('home')

@csrf_exempt
@require_POST
def login1(request):
    form = UserRegistrationForm(request.POST , )
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user1 = authenticate(request,username=username , password=password)
        if user1 is not None:
            if user1.lisence is not None:
                timer = user1.lisence
                if time.time() < timer:
                    pass
                else:
                    return JsonResponse({"token":''})
            else:
                return JsonResponse({"token":''})
            login(request,user1)
            #########################################

            hesabhaye_kol={
            10: 'صندوق',
            11: 'بانک ها',
            12: 'بدهکاران',
            13: 'اسناد دریافتی',
            14: 'اسناد در جریان وصول',
            15: 'موجودی مواد و کالا',
            16: 'پیش پرداخت ها',
            17: 'دارایی های غیر جاری',
            22: 'اسناد پرداختی',
            23: 'بستانکاران (حساب‌های پرداختی )',
            24: 'پیش دریافت ها',
            25: 'ذخیره مالیات',
            26: 'تسهیلات مالی کوتاه مدت',
            30: 'حقوق صاحبان سهام',
            40: 'درآمدها',
            50: 'هزینه ها',
            51: 'قیمت تمام شده ی کالای فروش رفته',
            60: 'فروش',
            61: 'برگشت از فروش و تخفیفات',
            62: 'خرید',
            63: 'برگشت از خرید و تخفیفات',
            64: 'حساب‌های انتظامی',
            65: 'طرف حساب های انتظامی',
            66: 'تراز افتتاحیه',
            }
            riz_joziat = [{"1":"صندوق" , "2": "تنخواه گردانها"} , {}, {"1":" اشخاص متفرقه" , "2":" مشتریان"}, {"1":" اسناد دریافتنی"}, {"1":"اسناد در جریان وصول"}, {"1":" موجودی مواد اولیه" , "2":" موجودی مواد و کالا"}, {"1":" پیش پرداخت مالیات" , "2":" پیش پرداخت اجاره" , "3":" پیش پرداخت هزینه های جاری"},{"1":" اموال،ماشین آلات و تجهیزات" , "2":" استهلاک انباشته اموال،ماشین آلات و تجهیزات" , "3":" زمین" , "4":" سرمایه گذاری های بلند مدت" , "5":" سپرده ها و مطالبات بلند مدت" , "6":" سایر دارائیها"}, {"1":" اسناد پرداختنی"}, {},{"1":" پیش دریافت فروش محصولات" , "2":" سایر پیش دریافتها"}, {"1":" مالیات بر ارزش افزوده فروش" , "2":" مالیات بر ارزش افزوده خرید" , "3":" عوارض فروش" , "4":" عوارض خرید"}, {"1":" تسهیلات مالی کوتاه مدت" , "2":" بهره تحقق نیافته"}, {"1":" سرمایه" , "2":" اندوخته قانونی" , "3":" سود (زیان) انباشته" , "4":" سود (زیان) جاری" , "5":" تقسیم سود"}, {"1":" درآمد اقساط"}, {"1":" بازاریاب" , "2":" هزینه حقوق و دستمزد" , "3":" هزینه استهلاک" , "4":" هزینه آب و برق مصرفی" , "5":" هزینه پست و تلفن" , "6":" هزینه اجاره محل" , "7":" هزینه ملزومات و نوشت افزار" , "8":" هزینه های متفرقه" , "9":" هزینه حمل" , "200":" هزینه بهره بانکی" , "300":" هزینه کارمزد بانک"}, {"1":" قیمت تمام شده‌ی کالای فروش رفته"}, {"1":" فروش"}, {"1":" تخفیفات فروش" , "2":" برگشت از فروش"}, {"1":" خرید"}, {"1":" برگشت از خرید" , "2":" تخفیف خرید"}, {"1":" حساب‌های انتظامی به نفع شرکت" , "2":" حساب های انتظامی به عهده شرکت"}, {"1":" طرف حساب انتظامی به نفع شرکت" , "2":" طرف حساب انتظامی به عهده شرکت"}, {"1":"تراز افتتاحیه" }]

            if user1.first_login == False:
                counter = 0
                for key , value in hesabhaye_kol.items():
                    tmp_obj_hesab=Hesabha.objects.create(code_hesab = key , name_hesab = value , user = user1)
                    tmp_obj_riz_joziat = riz_joziat[counter]
                    if len(tmp_obj_riz_joziat) != 0:
                        for key1,value1 in tmp_obj_riz_joziat.items():
                            Moein.objects.create(code_hesab = int(key1) , name_hesab = value1 ,user = user1 , hesabha = tmp_obj_hesab )
                    counter +=1

            user1.first_login = True
            user1.save()
 
            #########################################

            randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=48))

            check_user_token = GetToken.objects.get(user=user1)
            if check_user_token is not None:
                check_user_token.TOKEN = randomstr
                check_user_token.save()
                return JsonResponse({"token":randomstr , "timer":timer})
            else:
                mytk = GetToken.objects.create(TOKEN = randomstr , user=user1)
                mytk.save()
                return JsonResponse({"token":randomstr , "timer":timer})
        else:
            return JsonResponse({"token":''})



@csrf_exempt
@require_POST
def test2(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        form = AddHesab(request.POST, )
        if form.is_valid():
            hesab_name = form.cleaned_data.get('name_hesab')
            code_name = form.cleaned_data.get('code_hesab') 
            try:   
                obj1=Hesabha.objects.get(code_hesab=code_name , user=user1)
                return JsonResponse({"token":'no'})
            except:
                try:
                    obj1=Hesabha.objects.get(name_hesab = hesab_name , user=user1)
                    return JsonResponse({"token":'no'})
                except:
                    obj_hesab = Hesabha.objects.create(name_hesab = hesab_name , code_hesab=code_name , user=user1)
            
            # obj_hesab = Hesabha.objects.create(name_hesab = hesab_name , code_hesab=code_name , user=user1)


            return JsonResponse({"token":'ok'})


@api_view(['GET' , 'POST'])
def showall(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        hesab = Hesabha.objects.all().filter(user=user1)
        # product.select_related('')
        serializer = HesabhaSerializer(hesab , many=True)
        return Response(serializer.data)


@csrf_exempt
@require_POST
def sabtemoein(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        form = AddHesab(request.POST, )
        if form.is_valid():
            hesab_name = form.cleaned_data.get('name_hesab')
            code_name = form.cleaned_data.get('code_hesab') 
            id_hesab = request.POST['idhesab']
            id_final =''
            allow_numbers = ['0','1','2','3','4','5','6','7','8','9']
            for i in id_hesab:
                if i in allow_numbers:
                    id_final+=i

            hesab_obj = Hesabha.objects.get(code_hesab = int(id_final))


            try:   
                obj1=Moein.objects.get(code_hesab=code_name , user=user1 , hesabha=hesab_obj)
                return JsonResponse({"token":'no'})
            except:
                try:
                    obj1=Moein.objects.get(name_hesab = hesab_name , user=user1 , hesabha=hesab_obj)
                    return JsonResponse({"token":'no'})
                except:
                    obj_hesab = Moein.objects.create(name_hesab = hesab_name , code_hesab=code_name , user=user1 , hesabha=hesab_obj)

            return JsonResponse({"token":'ok'})


@api_view(['GET' , 'POST'])
def showmoein(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        id_hesab = request.POST['hesab_id']
        id_final =''
        allow_numbers = ['0','1','2','3','4','5','6','7','8','9']
        for i in id_hesab:
            if i in allow_numbers:
                id_final+=i
        
        hesab_obj = Hesabha.objects.get(code_hesab = int(id_final))
        
        hesab = Moein.objects.all().filter(user=user1 , hesabha=hesab_obj)
        # product.select_related('')
        serializer = HesabhaSerializer(hesab , many=True)
        return Response(serializer.data)


@api_view(['GET' , 'POST'])
def moeinrecord(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        hesab_obj = Hesabha.objects.get(name_hesab = request.POST['name_hesab'])
        
        hesab = Moein.objects.all().filter(user=user1 , hesabha=hesab_obj)
        # product.select_related('')
        serializer = HesabhaSerializer(hesab , many=True)
        return Response(serializer.data)

@api_view(['GET' , 'POST'])
def tafsilirecord(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        hesab_obj = Moein.objects.get(name_hesab = request.POST['name_hesab'])
        
        hesab = tafsili.objects.all().filter(user=user1 , moein=hesab_obj)
        # product.select_related('')
        serializer = HesabhaSerializer(hesab , many=True)
        return Response(serializer.data)


@csrf_exempt
@require_POST
def sabtetafsili(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        form = AddHesab(request.POST, )
        if form.is_valid():
            hesab_name = form.cleaned_data.get('name_hesab')
            code_name = form.cleaned_data.get('code_hesab') 
            id_hesab = request.POST['idhesab']
            id_final =''
            allow_numbers = ['0','1','2','3','4','5','6','7','8','9']
            for i in id_hesab:
                if i in allow_numbers:
                    id_final+=i

            moein_obj = Moein.objects.get(code_hesab = int(id_final))


            try:   
                obj1=tafsili.objects.get(code_hesab=code_name , user=user1 , moein=moein_obj)
                return JsonResponse({"token":'no'})
            except:
                try:
                    obj1=tafsili.objects.get(name_hesab = hesab_name , user=user1 , moein=moein_obj)
                    return JsonResponse({"token":'no'})
                except:
                    obj_hesab = tafsili.objects.create(name_hesab = hesab_name , code_hesab=code_name , user=user1 , moein=moein_obj)

            return JsonResponse({"token":'ok'})



@api_view(['GET' , 'POST'])
def showtafsili(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        id_hesab = request.POST['hesab_id']
        id_final =''
        allow_numbers = ['0','1','2','3','4','5','6','7','8','9']
        for i in id_hesab:
            if i in allow_numbers:
                id_final+=i
        
        moein_obj = Moein.objects.get(code_hesab = int(id_final))
        
        hesab = tafsili.objects.all().filter(user=user1 , moein=moein_obj)
        # product.select_related('')
        serializer = HesabhaSerializer(hesab , many=True)
        return Response(serializer.data)


@csrf_exempt
@require_POST
def sabtesanad(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1)
        except:
            category_obj=Category.objects.create(shomare_sanad = request.POST['sanadid'] , user=user1)
        

        obj_hesab = Asnad.objects.create(kol=request.POST['kol'] , moein=request.POST['moein'] , tafs = request.POST['tafs'] , sharhe_hesab = request.POST['sharhe_hesab'] , bedehkar = request.POST['bedehkar'] , bestankar =request.POST['bestankar'] , user=user1,category=category_obj)


        return JsonResponse({"status":'ok'})


@csrf_exempt
@require_POST
def deletesnad(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1)
        except:
            return JsonResponse({"status":'None'})
        
        all_asnad=category_obj.asnad.all()

        for i in all_asnad:
            if i.verified == False:
                try:
                    obj_deleter=Asnad.objects.all().filter( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=category_obj , verified=False)
                    obj_deleter.delete()
                except:
                     return JsonResponse({"status":'ok'})



        return JsonResponse({"status":'ok'})



@csrf_exempt
@require_POST
def pre_delete_sanad(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.all()
        except:
            return JsonResponse({"status":'ok'})
        
        for j in category_obj:

            all_asnad=j.asnad.all()

            for i in all_asnad:
                if i.verified == False:
                    try:
                        obj_deleter=Asnad.objects.all().filter( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=j , verified=False)
                        obj_deleter.delete()
                    except:
                        return JsonResponse({"status":'ok'})


        return JsonResponse({"status":'ok'})


@csrf_exempt
@require_POST
def savesandfinal(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1)
        except:
            return JsonResponse({"status":'None'})
        category_obj.verified = True
        category_obj.save()
        all_asnad=category_obj.asnad.all()

        for i in all_asnad:
            if i.verified == False:
                try:
                    obj_deleter=Asnad.objects.all().filter( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=category_obj , verified=False)
                    for jj in obj_deleter:
                        jj.verified = True
                        jj.save()
                except:
                     return JsonResponse({"status":'ok'})



        return JsonResponse({"status":'ok'})




@api_view(['GET' , 'POST'])
def showallsanads(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.all().filter( user=user1 , verified=True)
        except:
            return JsonResponse({"status":'None'})
        
        
        obj=CategorySerializer(category_obj , many=True)


        return Response(obj.data)


@api_view(['GET' , 'POST'])
def showeditedsanad(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            asnad_obj = Category.objects.get(verified = True , shomare_sanad = request.POST['sanadid'])
        except:
            return JsonResponse({"status":'None'})


        try:
            asnad_obj = Asnad.objects.all().filter( verified=True , user=user1 , category=asnad_obj)
        except:
            return JsonResponse({"status":'None'})
        
        
        obj=AsnadSerializer(asnad_obj , many=True)


        return Response(obj.data)


@csrf_exempt
@require_POST
def deleteverified(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1 , verified=True)
        except:
            return JsonResponse({"status":'ok'})
        
        all_asnad=category_obj.asnad.all()

        for i in all_asnad:
            if i.verified == True:
                try:
                    obj_deleter=Asnad.objects.all().filter( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=category_obj , verified=True)
                    obj_deleter.delete()
                    
                except:
                     return JsonResponse({"status":'ok'})


        category_obj.delete()
        
        return JsonResponse({"status":'ok'})


@csrf_exempt
@require_POST
def getuserinfo(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user

        return JsonResponse({"username":user1.username})


@csrf_exempt
@require_POST
def exporter(request):
    token = request.POST['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
       
        
        user1=check_user_token.user

        obj1=Docs.objects.all().filter(user=user1)

        obj1.delete()

        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1 , verified=True)
        except:
            return JsonResponse({"status":'ok'})
        
        all_asnad=category_obj.asnad.all()

        resulter = docx_generator(all_asnad , request.POST['sanadid'] , request.POST['name'] , category_obj.date_create , category_obj , user1)
        # for i in all_asnad:
        #     if i.verified == False:
        #         try:
        #             obj_sanad=Asnad.objects.get( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=category_obj , verified=False)
                    
        #         except:
        #              return JsonResponse({"status":'ok'})


        
        with open("gfg.docx" , 'rb') as existing_file:
            file_save = File(file=existing_file , name='test.docx')
            post = Docs(doc_file=file_save , user=user1)
            post.full_clean()
            post.save()
    
        obj=Docs.objects.get(user=user1)
        return JsonResponse({"link":obj.doc_file.url})


@csrf_exempt
@require_POST
def deletespecialrecord(request):
    token = request.POST['token']
    print('6')
    check_user_token = GetToken.objects.get(TOKEN=token)
    print('7')
    if check_user_token is not None:
        user1=check_user_token.user
        print(request.POST['sanadid'])
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1)
        except:
            return JsonResponse({"status":'ok'})
        print(5)
        all_asnad=category_obj.asnad.all()

        for i in all_asnad:
            if i.kol==request.POST['kol'] and i.tafs == request.POST['tafs'] and i.moein == request.POST['moein'] and str(i.bestankar) == request.POST['bestankar'] and str(i.bedehkar)==request.POST['bedehkar'] and i.sharhe_hesab == request.POST['sharhe_hesab']  :
                try:
                    print('2')
                    obj_deleter=Asnad.objects.all().filter( kol=i.kol , moein=i.moein , tafs = i.tafs , sharhe_hesab = i.sharhe_hesab , bedehkar = i.bedehkar , bestankar =i.bestankar , user=user1,category=category_obj)
                    obj_deleter.delete()
                    print('3')
                    
                except:
                     return JsonResponse({"status":'ok'})


        
        return JsonResponse({"status":'ok'})


@csrf_exempt
@require_POST
def deletespecifichesab(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            hesab = Hesabha.objects.get(user=user1 ,code_hesab = request.POST['code_hesab'])
            # product.select_related('')
            hesab.delete()
            return JsonResponse({"status":'ok'})
        except:
            return JsonResponse({"status":'no'})



@csrf_exempt
@require_POST
def deletemoeinspecific(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            hesab = Hesabha.objects.all().filter(user=user1 ,code_hesab = int(request.POST['code_hesab']))
            # product.select_related('')
            moein = Moein.objects.get(user=user1 , hesabha__in = hesab  , code_hesab = request.POST['code_moein'])
            moein.delete()
            return JsonResponse({"status":'ok'})
        except:
            return JsonResponse({"status":'no'})
            
    else:
        pass



@csrf_exempt
@require_POST
def deletetafsspecific(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            hesab = Hesabha.objects.all().filter(user=user1 ,code_hesab = int(request.POST['code_hesab']))
            # product.select_related('')
            moein = Moein.objects.all().filter(user=user1 , hesabha__in = hesab  , code_hesab = request.POST['code_moein'])
            tafs = tafsili.objects.get(user=user1 , moein__in=moein , code_hesab = request.POST['code_tafs'])
            tafs.delete()
            return JsonResponse({"status":'ok'})

        except:
            return JsonResponse({"status":'no'})
            
    else:
        pass



@csrf_exempt
@require_POST
def downloaddocs(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        with open("gfg.docx" , 'rb') as existing_file:
            file_save = File(file=existing_file , name='test.docx')
            post = Docs(doc_file=file_save , user=user1)
            post.full_clean()
            post.save()
    
        obj=Docs.objects.get(user=user1)
        return JsonResponse({"link":obj.doc_file.url})

@csrf_exempt
@require_POST
def forgetpassword(request):
    try:
        email = request.POST['email']
        obj = Order.objects.get(email = email , is_paid=False)    
        send_list = []
        send_list.append(obj.email)
        send_mail(subject='اطلاعات حساب کاربری ققنوس' , message=f'اطلاعات حساب کاربری شما در اپلیکیشن حسابداری ققنوس \n نام کاربری : {obj.username} \n رمز عبور : {obj.password}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=send_list)
        return JsonResponse({"answer":'yes'})
    except:
        return JsonResponse({"answer":'no'})


@csrf_exempt
@require_POST
def checkshomaresanad(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1 , verified=True)
            return JsonResponse({"answer":'yes'})
        except:
            return JsonResponse({"answer":'no'})


######################## sand zan hoshmand back-end


@csrf_exempt
@require_POST
def save_ai_sanad(request):
    # print(request.POST)
    json_string = request.body.decode('utf-8')
    all_asnad = json.loads(json_string)
    token = ''
    for i in all_asnad:
        if "token" in i.keys():
            token=i['token']
            del i['token']
    
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            counter = Category.objects.count()
            category_obj = Category.objects.create(shomare_sanad = counter+1 , user=user1)
        except:
            return JsonResponse({"status":'None'})
        category_obj.verified = True
        category_obj.ai_sanad = True
        category_obj.save()
        for i in all_asnad:
            try:
                
                if i['kind'] == 'buy':
                    Asnad.objects.create( kol=i['kol'] , moein=i['moein'] , tafs = i['tafsili'] , sharhe_hesab = i['tozihat'] , bedehkar = i['price'] , bestankar =0, user=user1,category=category_obj , verified=True)
                else:
                    Asnad.objects.create( kol=i['kol'] , moein=i['moein'] , tafs = i['tafsili'] , sharhe_hesab = i['tozihat'] , bedehkar = 0 , bestankar =i['bestankar'], user=user1,category=category_obj , verified=True)

            except:
                    return JsonResponse({"status":'ok'})



        # return JsonResponse({"status":'ok'})


################################################ check AI Sanad 

@csrf_exempt
@require_POST
def checkaisanad(request):
    token = request.POST['token']
    check_user_token = GetToken.objects.get(TOKEN=token)
    if check_user_token is not None:
        user1=check_user_token.user
        try:
            category_obj = Category.objects.get(shomare_sanad = request.POST['sanadid'] , user=user1 , verified=True)
            if category_obj.ai_sanad == True:
                return JsonResponse({"answer":'yes'})
            else:
                return JsonResponse({"answer":'no'})
        except:
            return JsonResponse({"answer":'None'})
