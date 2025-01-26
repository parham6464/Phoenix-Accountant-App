from django.urls import path

from .views import *

urlpatterns = [
    path('login1/' , login1 , name='login1'),
    path('allhesab/' , test2 , name='hesab'),
    path('showall/' , showall , name='showallhesab'),
    path('addmoein/' , sabtemoein , name='sabtemoein'),
    path('showmoein/' , showmoein , name='showmoein'),
    path('addtafsili/' , sabtetafsili , name='sabtetafsili'),
    path('showtafsili/' , showtafsili , name='showtafsili'),
    path('moeinrecord/' , moeinrecord , name='moeinrecord'),
    path('tafsilirecord/' , tafsilirecord , name='tafsilirecord'),
    path('sabtesanad/' , sabtesanad , name='sabtesanad'),
    path('deletesnad/' , deletesnad , name='deletesnad'),
    path('predeletesanad/' , pre_delete_sanad , name='pre_delete_sanad'),
    path('savesandfinal/' , savesandfinal , name='savesandfinal'),
    path('showallsanads/' , showallsanads , name='showallsanads'),
    path('showeditedsanad/' , showeditedsanad , name='showeditedsanad'),
    path('deleteverified/' , deleteverified , name='deleteverified'),
    path('getuserinfo/' , getuserinfo , name='getuserinfo'),
    path('exporter/' , exporter , name='exporter'),
    path('deletespecific/' , deletespecialrecord , name='deletespecialrecord'),
    path('deletehesab/' , deletespecifichesab , name='deletespecifichesab'),
    path ('deletemoeinspecific/' , deletemoeinspecific , name='deletemoeinspecific'),
    path('deletetafsspecific/' , deletetafsspecific , name='deletetafsspecific'),
    # path('downloaddocs/' , downloaddocs , name='downloaddocs'),
    path('forgetpassword/' , forgetpassword , name='forgetpassword'),
    path('checkshomaresanad/' , checkshomaresanad , name='checkshomaresanad'),
    path('savefinalai/' , save_ai_sanad , name='save_ai_sanad'),
    path('checkaisanad/' , checkaisanad , name='checkaisanad'),

]