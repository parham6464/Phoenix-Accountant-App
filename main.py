from datetime import timedelta
from optparse import Values
import flet as ft 
import random
import dns.resolver
import mysql.connector
import requests
import json
import time

global my_token
my_token = ''

class ExportRecords(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/export" , scroll='ALWAYS' , padding=60)

        self.my_docs = ''
        ############################# API EXPORT DOCS #############
        def exporter(e):
            if self.name_sherkat.value == '':
                self.notif3.open=True
                return 
            token_url= "http://127.0.0.1:8000/accounts/exporter/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":exp_id,
                "name":self.name_sherkat.value,

            }

            res = requests.post(token_url , data=request_data)
            linker=f"http://127.0.0.1:8000{res.json()['link']}"
            resulter=page.launch_url(linker)

            # open('document.docx', 'wb').write(resulter.content)
            # return res.json()

        ############################################################


        ############################# API EXPORT DOCS #############
        def downloader(e=None):
            token_url= "http://127.0.0.1:8000/accounts/downloaddocs/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",

            }

            res = requests.post(token_url , data=request_data)
            return res

        ############################################################
        # result_link=downloader()
        # print(result_link)
        
        self.name_sherkat = ft.TextField(hint_text='اسم شرکت' , border_radius=10 , border_color='white')
        self.submit_butt = ft.Row(controls=[ft.ElevatedButton(text='دانلود خروجی word' , on_click=exporter , width=page.width/3)] , alignment=ft.MainAxisAlignment.START)
        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('اسم شرکت را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.but_back = ft.Row(controls=[ft.ElevatedButton(text='بازگشت' ,on_click=lambda e : page.go('/history') , width=page.width/2)],alignment=ft.MainAxisAlignment.CENTER)


        self.controls = [ft.SafeArea(self.name_sherkat) , ft.SafeArea(self.submit_butt) , ft.SafeArea(self.but_back),ft.SafeArea(self.notif3) ]

        self.page=page


class EditRecord(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/editrecord" , scroll='AUTO')

        self.my_docs = ''

        ############################# API Save SANAD #############
        def restoreedit():
            token_url= "http://127.0.0.1:8000/accounts/showeditedsanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ############################################################
        restore_edit = restoreedit()
        ############################# API Save SANAD #############
        def SaveSanadFinal( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/savesandfinal/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        ############################################################

        ############################# API DELETE SANAD #############
        def DeleteSanad( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/deletesnad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        ############################# API ADD HESAB ################
        def GetAllHesab( sanadid , kol , moein , tafs , sharhe_hesab , bedehkar , bestankar ):
            token_url= "http://127.0.0.1:8000/accounts/sabtesanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "kol":f"{kol}",
                "moein":f"{moein}",
                "tafs":f"{tafs}",
                "sharhe_hesab":f"{sharhe_hesab}",
                "bedehkar":f"{bedehkar}",
                "bestankar":f"{bestankar}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        #########################API DELETE KARDANE RECORD######################
        def DeleteRecord(sanadid,sharhe_hesab , tafs , moein , kol , bestankar , bedehkar):
            token_url= "http://127.0.0.1:8000/accounts/deletespecific/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id,
                "sharhe_hesab":sharhe_hesab,
                "tafs":tafs,
                "moein":moein,
                "kol":kol,
                "bestankar":bestankar,
                "bedehkar":bedehkar

            }

            res = requests.post(token_url , data=request_data)
            return "ok"

        ##################################################################

        ##################################################################
        def ShowAllHesab(token):
            token_url= "http://127.0.0.1:8000/accounts/showall/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{token}",
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################
        self.my_docs = ShowAllHesab(my_token['token'])
        ##################################################################

        def moeinshow(e):
            token_url= "http://127.0.0.1:8000/accounts/moeinrecord/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'name_hesab':f'{self.kol.value}'
            }

            res = requests.post(token_url , data=request_data)
            my_moeins=res.json()
            self.dd.options = []
            self.tafsili.options = []

            if len(my_moeins) != 0:
                for i in my_moeins:
                    self.dd.options.append(ft.dropdown.Option(i['name_hesab']))    
            self.update()        
        ##################################################################

        def tafsilishow(e):
            token_url= "http://127.0.0.1:8000/accounts/tafsilirecord/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'name_hesab':f'{self.dd.value}'
            }

            res = requests.post(token_url , data=request_data)
            my_tafsili=res.json()
            self.tafsili.options = []
            if len(my_tafsili) != 0:
                for i in my_tafsili:
                    self.tafsili.options.append(ft.dropdown.Option(i['name_hesab']))    
            self.update()        
        ##################################################################

        self.page = page 
        self.moein_label=ft.Text(value='معین:')
        self.dd = ft.Dropdown(
            width=page.width-10,
            on_change=tafsilishow,
            options=[
            ],
            border_color='white'
        )
        self.tafsili_label=ft.Text(value='تفصیلی:')
        self.tafsili = ft.Dropdown(
            width=page.width-10,
            options=[
            ],
            border_color='white'
        )
        self.kol_label=ft.Text(value='کل:')
        self.kol = ft.Dropdown(
            width=page.width-10,
            on_change=moeinshow,
            options=[
            ],
            border_color='white'
        )
        if len(self.my_docs) != 0:
            for i in self.my_docs:
                self.kol.options.append(ft.dropdown.Option(i['name_hesab']))

        self.point_delete = ft.SafeArea(ft.Text(value='برای حذف ستون های اضافه شده بر روی آن در جدول بزنید تا حذف شود' , color='blue' , weight=3))
        self.hesabha_section = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='انتخاب حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=130 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))],alignment=ft.MainAxisAlignment.CENTER))

        self.my_row = ft.SafeArea(ft.Container(ft.Column(controls=[self.point_delete,self.hesabha_section,self.kol_label,self.kol,self.moein_label,self.dd]) ,padding=ft.Padding(top=0 , right=0, bottom=0 , left=0 )))
        self.my_row1 = ft.SafeArea(ft.Container(ft.Column(controls=[self.tafsili_label,self.tafsili]) ,padding=ft.Padding(top=0 , right=0, bottom=10 , left=0 )))
        
        self.table=ft.DataTable(
            vertical_lines=ft.border.BorderSide(3, "grey"),
            # border=ft.border.all(2, "grey"),
            border=ft.border.only(bottom=ft.border.BorderSide(2, "grey")),
            width=self.page.window.max_width-60,



            columns=[  
                ft.DataColumn(ft.Text("نام حساب")),
                ft.DataColumn(ft.Text("بدهکار"),numeric=True),
                ft.DataColumn(ft.Text("بستانکار"),numeric=True),
            ],
            )
        def deleter():
            if self.shomare_sanad !='':
                DeleteSanad(self.shomare_sanad )
        
        def remove_table(e , r , s):
            row_num = 0
            for i in self.my_sanads: 
                # print(type(i.values()[5])) 
                tmp_checker = f"{i['tafsili']}\n{i['sharhe_hesab']}"
                if str(s.value) in i.values() and str(r.value) in i.values() and e.value in tmp_checker: 
                    self.table.rows.remove(self.table.rows[row_num])
                    if str(i['bedehkar']) !="0":
                        print('1')
                        self.bed_kol -= int(i['bedehkar'])
                        if self.taraze_kol <0:
                            print('negative')
                            self.taraze_kol += int(i['bedehkar'])
                        elif self.taraze_kol >=0:
                            print('positive')
                            self.taraze_kol += int(i['bedehkar'])
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'
                        self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'
                        del self.my_sanads[row_num]

                    if str(i['bestankar']) !="0":
                        self.bes_kol -= int(i['bestankar'])
                        if self.taraze_kol <0:
                            print('negative')
                            self.taraze_kol -= int(i['bestankar'])
                        elif self.taraze_kol >=0:
                            print('positive')
                            self.taraze_kol -= int(i['bestankar'])
                            print(self.taraze_kol)

                        self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'
                        del self.my_sanads[row_num]

                    self.update()
                    obj=DeleteRecord(self.shomare_sanad , i['sharhe_hesab'] , i['tafsili'] , i['moein'] , i['kol'] ,i['bestankar'] , i['bedehkar'] )
                    return
                else:
                    row_num+=1
        self.my_sanads = []
        self.taraze_kol = 0
        self.bed_kol = 0
        self.bes_kol = 0
        self.shomare_sanad = final_id
        def addsanad(e):
            tmp = {}
            if self.bestankar.value !='' or self.bedehkar.value !='':
                if not (self.bestankar.value!='' and self.bedehkar.value !=''):
                    if self.kol.value !=None and self.dd.value !=None and self.tafsili.value !=None:
                        if self.sanadID.value !='':
                            if self.sharh.value !='':
                                self.sanadID.read_only=True
                                if self.bestankar.value !='':
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bestankar":self.bestankar.value , 'bedehkar':"0" , "sharhe_hesab":self.sharh.value , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value}
                                    self.my_sanads.append(tmp)
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , 0 , self.bestankar.value)
                                    self.bes_kol += int(self.bestankar.value)
                                    self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                                    self.taraze_kol += int(self.bestankar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1
                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text("0" , color='red')), ft.DataCell(ft.Text(self.bestankar.value , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''

                                    self.update()
                                elif self.bedehkar.value !='':
                                    print('2')
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bedehkar":self.bedehkar.value , 'bestankar':"0" , "sharhe_hesab":self.sharh.value , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value}
                                    self.my_sanads.append(tmp)
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , self.bedehkar.value , 0 )
                                    self.bed_kol += int(self.bedehkar.value)
                                    self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'
                                    self.taraze_kol -= int(self.bedehkar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1

                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text(self.bedehkar.value , color='red')), ft.DataCell(ft.Text("0" , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''
                                    
                                    self.update()

                            else:
                                self.notif4.open=True
                                self.update()
                        else:
                            self.notif2.open=True
                            self.update()

                    else:
                        self.notif.open=True
                        self.update()
                
                else:
                    self.notif3.open=True
                    self.update()
            else:
                self.notif1.open=True
                self.update()      

        def savasanad(e):
            if self.shomare_sanad !='':
                if self.taraze_kol == 0:
                    SaveSanadFinal(self.shomare_sanad)
                    self.notif6.open=True
                    self.update()
                else:
                    self.notif5.open=True
                    self.update()
            else:
                self.notif2.open=True
                self.update()


        
        self.my_col=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS , vertical_alignment='center')], scroll= ft.ScrollMode.ALWAYS , horizontal_alignment='center',) , height=220 , width=self.page.window.width , border_radius=10 , shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))]))

        self.bestankar_label = ft.Text(value='تراز بستانکار:')
        self.bedehkar_label = ft.Text(value='تزار بدهکار:')
        self.ban_bas_label = ft.Text(value='تزار بن-بس:')

        if len(restore_edit) !=0:
            for i in restore_edit:
                if str(i['bedehkar']) =="0":
                    tmp = {"bestankar":str(i['bestankar']) , "sharhe_hesab":i['sharhe_hesab'] , "kol":i['kol'] , "moein":i['moein'] , "tafsili":i['tafs'] , 'deleter':f"{i['tafs']}\n{i['sharhe_hesab']}" , 'bedehkar':"0"}
                if str(i['bestankar'])=="0":
                    tmp = {"bedehkar":str(i['bedehkar']) , "sharhe_hesab":i['sharhe_hesab'] , "kol":i['kol'] , "moein":i['moein'] , "tafsili":i['tafs'] , 'deleter':f"{i['tafs']}\n{i['sharhe_hesab']}" , 'bestankar':"0"}

                self.my_sanads.append(tmp)
                text_add = f"{i['tafs']}\n{i['sharhe_hesab']}"
                self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text(i['bedehkar'] , color='red')), ft.DataCell(ft.Text(i['bestankar'] , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                self.bed_kol += int(i['bedehkar'])
                self.bes_kol += int(i['bestankar'])
                self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'
                
                
            self.taraze_kol -= self.bed_kol
            self.taraze_kol += self.bes_kol
            self.ban_bas_label.value = f'تراز بن-بس: {self.taraze_kol}'
            self.update()

        self.my_row2 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.bestankar_label,self.bedehkar_label,self.ban_bas_label] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=30 ,right=0 ,left=0 , bottom=0))]))

        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('اضافه کردن' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=addsanad,
            width=self.page.width-10 
        )

        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ذخیره سند' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=savasanad,
            width=self.page.width-10 
        )

        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=lambda e: [deleter(),page.go('/landing22')],
            width=self.page.width-10 
        )


        self.info_sanad = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='اطلاعات حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=140 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600) )],alignment=ft.MainAxisAlignment.CENTER))

        self.bestankar = ft.TextField(label='بستانکار' , width=self.page.width/2-25 , color='green', border_color='white')
        self.bedehkar = ft.TextField(label='بدهکار' , width=self.page.width/2-25 , color='red', border_color='white')
        self.sharh = ft.TextField(label='شرح حساب' , width=self.page.width-10  , border_color='white')


        self.my_row7 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Row(controls=[self.bestankar,self.bedehkar] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=10 ,right=0 ,left=0 , bottom=0))]))

        self.ssabt = ft.ElevatedButton(text='اضافه کردن' , width=self.page.width-10 , height=45 , on_click=addsanad)
        self.my_row8 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[ self.sharh  ] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=5 ,right=0 ,left=0 , bottom=0))]))


        self.sanadID = ft.TextField(label='شماره سند' , width=self.page.width-10 , border_color='white')
        self.sanadID.value = f'{final_id}'
        self.sanadID.read_only=True

        self.my_row3 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.sanadID] , alignment='center' , width=self.page.window_width),padding=ft.Padding(top=30 ,right=0 ,left=0 , bottom=0))]))

        self.save_sanad = ft.ElevatedButton(text='ذخیره سند' , width=page.width-10 , height=45 ,on_click=savasanad)
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=45 , width=page.width-10 , on_click=lambda e: [deleter(),page.go('/landing22')])

        self.my_row4 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.save_sanad ] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=15 ,right=0 ,left=0 , bottom=0))]))
        self.my_row5 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.back_button] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=0 ,right=0 ,left=0 , bottom=0))]))


        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حساب های کل و تفصیلی و معین را انتخاب کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('شماره سند را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('در هر بار فقط یا بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif4 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار شرح حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif5 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('تراز بن بس باید صفر باشد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif6 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('ذخیره شد'),
            ft.Icon(name=ft.icons.DONE, color=ft.colors.PINK),
        ]) , duration=2000)



        self.controls=[self.my_col,self.my_row,self.my_row1,self.info_sanad,self.my_row7,self.my_row8,ft.SafeArea(ft.Row(controls=[self.button0])),self.my_row3,self.my_row2,ft.SafeArea(ft.Row(controls=[self.button1])),ft.SafeArea(ft.Row(controls=[self.button2])) , ft.SafeArea(self.notif),ft.SafeArea(self.notif1),ft.SafeArea(self.notif2),ft.SafeArea(self.notif3),ft.SafeArea(self.notif4),ft.SafeArea(self.notif5) , ft.SafeArea(self.notif6)]




class History(ft.View):
    def __init__(self , page:ft.Page ):
        super().__init__(route="/history" , scroll='ALWAYS' , padding=20)

        ############################# check AI sanad #############
        def checkAISanad(sanadid):
            token_url= "http://127.0.0.1:8000/accounts/checkaisanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanadid
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ############################################################


        ############################# delete sanad #############
        def deletechoosen(sanadid):
            token_url= "http://127.0.0.1:8000/accounts/deleteverified/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanadid
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ############################################################


        ############################# API Save SANAD #############
        def ShowHistory():
            token_url= "http://127.0.0.1:8000/accounts/showallsanads/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ############################################################
        allsanads=ShowHistory()
        self.page=page
        self.controls = []

        def editsanad(e):
            txt=e.control.text
            allow_numbers = ['0' ,'1','2','3','4','5','6','7','8','9']
            global final_id
            final_id = ''
            for i in txt:
                if i in allow_numbers:
                    final_id+=i
            
            resulter = checkAISanad(final_id)
            if resulter['answer'] != 'None':
                if resulter['answer'] == 'yes':
                    page.go('/editrecord22')
                else:
                    page.go('/editrecord')


        def exportsanad(e):
            txt=e.control.text
            allow_numbers = ['0' ,'1','2','3','4','5','6','7','8','9']
            global exp_id
            exp_id = ''
            for i in txt:
                if i in allow_numbers:
                    exp_id+=i


        def deletesanad(e):
            txt=e.control.text
            allow_numbers = ['0' ,'1','2','3','4','5','6','7','8','9']
            final_id1 = ''
            for i in txt:
                if i in allow_numbers:
                    final_id1+=i

            deletechoosen(final_id1)

            page.go('/landing22')
            page.go('/history')
            self.update()

        
        self.labal_page = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Text(value='لیست اسناد ثبت شده' , text_align=ft.TextAlign.CENTER) , border_radius=10 , height=30 , width=self.page.window.width )]))
        self.controls.append(self.labal_page)
        if len(allsanads)!=0 and 'None' not in allsanads:
            for i in allsanads:
                self.my_con=ft.SafeArea(ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.EDIT_DOCUMENT),
                                    title=ft.Text(f"سند شماره {i['shomare_sanad']}"),
                                    subtitle=ft.Text(
                                        "می توانید با استفاده از گزینه های زیر سند را ادیت کنید یا حذف کنید و یا خروجی ورد بگیرید"
                                    ),
                                ),
                                ft.Row(
                                    [ft.TextButton(f"خروجی گرفتن سند {i['shomare_sanad']}" ,on_click=lambda e :[exportsanad(e) , page.go('/export')]), ft.TextButton(f"ویرایش سند {i['shomare_sanad']}" , on_click=lambda e:[editsanad(e)]) , ],
                                    
                                    alignment=ft.MainAxisAlignment.END,
                                ),ft.Row([ft.TextButton(f'حذف سند {i["shomare_sanad"]}' , on_click=lambda e: [deletesanad(e)])] , alignment=ft.MainAxisAlignment.END,),
                            ]
                        ),
                        width=self.page.window.width-60,
                        padding=10,
                    )
                )
                )
                self.controls.append(self.my_con)
        
        self.back_button= ft.SafeArea(ft.ResponsiveRow([ft.ElevatedButton(text='بازگشت'  , height=50 , width=self.page.window.width-30 , on_click=lambda e: page.go('/landing22'))]))
        self.controls.append(self.back_button)


class Tafsili(ft.View):
    def __init__(self , page:ft.Page ):
        super().__init__(route="/tafsili" , scroll='ALWAYS' , padding=20)

        self.my_docs = ''

        ############################# API ADD HESAB ################
        def GetAllHesab(token , code , name):
            token_url= "http://127.0.0.1:8000/accounts/addtafsili/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{token}",
                'code_hesab':f'{code}',
                "name_hesab":f'{name}',
                'idhesab':f'{id_temp_moein}'
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        
        #########################API DELETE KARDANE HESAB######################
        def DeleteTafs(code_tafs):
            token_url= "http://127.0.0.1:8000/accounts/deletetafsspecific/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'code_tafs':code_tafs,
                "code_hesab":id_temp_hesab.value,
                "code_moein":str(id_temp_moein.value)
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################


        ##################################################################
        def ShowAllHesab(token):
            token_url= "http://127.0.0.1:8000/accounts/showtafsili/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{token}",
                'hesab_id':f"{id_temp_moein}"
            }

            res = requests.post(token_url , data=request_data)
            self.my_docs = res.json()

        ##################################################################
        ShowAllHesab(my_token['token'])


        self.page=page

        self.labal_page = ft.Text(value='لیست حساب های تفصیلی:')

        def on_submit(c):
            if self.code_hesab.value !='':
                if self.name_hesab.value !='':
                    result=GetAllHesab(my_token['token'] , self.code_hesab.value , self.name_hesab.value)
                    if result['token'] == 'ok':
                        self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(self.code_hesab.value)), ft.DataCell(ft.Text(self.name_hesab.value)),]))
                        self.code_hesab.value = ''
                        self.name_hesab.value = ''
                        self.update()
                    else:
                        self.notif2.open=True
                        self.update()
                else:
                    self.notif1.open=True
                    self.update()
            else:
                self.notif.open=True
                self.update()

        self.table=ft.DataTable(
            # bgcolor="blue",
            vertical_lines=ft.border.BorderSide(3, "grey"),
            border=ft.border.all(2, "grey"),
            border_radius=10,
            width=self.page.window.width-60,
            

            columns=[  
                ft.DataColumn(ft.Text("کد حساب")),
                ft.DataColumn(ft.Text("نام حساب"),numeric=True),
            ],

            )
        if len(self.my_docs)!=0:
            for i in self.my_docs:
                self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(i['code_hesab'])), ft.DataCell(ft.Text(i['name_hesab'])),]))

        ss=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS)], scroll= ft.ScrollMode.ALWAYS) , height=220 , width=self.page.window.width)]))

        def remove_table(e):
            if self.code_hesab1.value !='':
                result = DeleteTafs(self.code_hesab1.value)
                if result['status'] == 'ok':
                    page.go('/moein')
                    page.go('/tafsili')
                else:
                    self.notif3.open=True
                    self.update()

        self.hazf_label = ft.Text(value='حذف حساب:')
        self.code_hesab1 = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30 , border_color='white')
        self.submit1_button= ft.ElevatedButton(text='حذف'  , height=50 , width=self.page.window.width/2-30 , on_click=remove_table )
        self.my_col1_5 = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab1  ,self.submit1_button ])]))


        self.code_hesab = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30 , border_color='white')
        self.name_hesab = ft.TextField(label='اسم حساب',hint_text='اسم حساب' , width=self.page.window.width/2-30 , border_color='white')
        self.submit_button= ft.ElevatedButton(text='ثبت'  , height=50 , width=self.page.window.width-30 , on_click=on_submit )
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=50 , width=self.page.window.width-30 , on_click=lambda e: page.go('/moein'))
        
        self.my_col = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab ,self.name_hesab ])]))
        self.my_col2 = ft.SafeArea(ft.ResponsiveRow([ft.Column(controls=[self.submit_button ,self.back_button])]))




        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('کد حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('اسم حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حسابی با این نام یا کد وجود دارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        
        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حسابی با این کد وجود ندارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)


        self.controls = [self.labal_page,ss,self.my_col,self.hazf_label,self.my_col1_5 , self.my_col2, ft.SafeArea(self.notif) , ft.SafeArea(self.notif1) , ft.SafeArea(self.notif2) , ft.SafeArea(self.notif3)]


class Moein(ft.View):
    def __init__(self , page:ft.Page ):
        super().__init__(route="/moein" , scroll='ALWAYS' , padding=20)

        self.my_docs = ''

        ##############################func zakhire hesabe entekhabi#######
        def entekhabi(c):
            global id_temp_moein
            id_temp_moein=c.control.cells[0].content
        ############################# API ADD HESAB ################
        def GetAllHesab(token , code , name):
            token_url= "http://127.0.0.1:8000/accounts/addmoein/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{token}",
                'code_hesab':f'{code}',
                "name_hesab":f'{name}',
                'idhesab':f'{id_temp_hesab}'
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        #########################API DELETE KARDANE HESAB######################
        def DeleteMoein(code_moein):
            token_url= "http://127.0.0.1:8000/accounts/deletemoeinspecific/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'code_moein':code_moein,
                "code_hesab":str(id_temp_hesab.value)
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################

        ##################################################################
        def ShowAllHesab(token):
            token_url= "http://127.0.0.1:8000/accounts/showmoein/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            

            request_data ={
                "token":f"{token}",
                'hesab_id':id_temp_hesab
            }

            res = requests.post(token_url , data=request_data)
            self.my_docs = res.json()

        ##################################################################
        ShowAllHesab(my_token['token'])


        self.page=page

        self.labal_page = ft.Text(value='لیست حساب های معین:')

        def on_submit(c):
            if self.code_hesab.value !='':
                if self.name_hesab.value !='':
                    result=GetAllHesab(my_token['token'] , self.code_hesab.value , self.name_hesab.value)
                    if result['token'] == 'ok':
                        self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(self.code_hesab.value)), ft.DataCell(ft.Text(self.name_hesab.value)),],on_select_changed=lambda e: [entekhabi(e) , page.go('/tafsili')] ))
                        self.code_hesab.value = ''
                        self.name_hesab.value = ''
                        self.update()
                    else:
                        self.notif2.open=True
                        self.update()
                else:
                    self.notif1.open=True
                    self.update()
            else:
                self.notif.open=True
                self.update()

        self.table=ft.DataTable(
            # bgcolor="blue",
            vertical_lines=ft.border.BorderSide(3, "grey"),
            border=ft.border.all(2, "grey"),
            border_radius=10,
            width=self.page.window.width-60,
            

            columns=[  
                ft.DataColumn(ft.Text("کد حساب")),
                ft.DataColumn(ft.Text("نام حساب"),numeric=True),
            ],
            )
        if len(self.my_docs)!=0:
            for i in self.my_docs:
                self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(i['code_hesab'])), ft.DataCell(ft.Text(i['name_hesab'])),],on_select_changed=lambda e: [entekhabi(e) , page.go('/tafsili')]))

        ss=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS)], scroll= ft.ScrollMode.ALWAYS) , height=220 , width=self.page.window.width)]))

        def remove_table(e):
            if self.code_hesab1.value !='':
                result = DeleteMoein(self.code_hesab1.value)
                if result['status'] == 'ok':
                    page.go('/hesabha')
                    page.go('/moein')
                else:
                    self.notif3.open=True
                    self.update()

        self.hazf_label = ft.Text(value='حذف حساب:')
        self.code_hesab1 = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30 , border_color='white')
        self.submit1_button= ft.ElevatedButton(text='حذف'  , height=50 , width=self.page.window.width/2-30 , on_click=remove_table )
        self.my_col1_5 = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab1  ,self.submit1_button ])]))


        self.code_hesab = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30, border_color='white')
        self.name_hesab = ft.TextField(label='اسم حساب',hint_text='اسم حساب' , width=self.page.window.width/2-30, border_color='white')
        self.submit_button= ft.ElevatedButton(text='ثبت'  , height=50 , width=self.page.window.width-30 , on_click=on_submit )
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=50 , width=self.page.window.width-30 , on_click=lambda e: page.go('/hesabha'))
        
        self.tozihat = ft.Text(value='با کلیک بر روی هر حساب به صفحه اضافه کردن حساب تفصیلی آن حساب کل معین می شوید.')
        self.my_col = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab ,self.name_hesab ])]))
        self.my_col2 = ft.SafeArea(ft.ResponsiveRow([ft.Column(controls=[self.submit_button,self.back_button , self.tozihat])]))


        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('کد حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('اسم حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حسابی با این نام یا کد وجود دارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حسابی با این کد وجود ندارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        


        self.controls = [self.labal_page,ss,self.my_col ,self.hazf_label,self.my_col1_5, self.my_col2 , ft.SafeArea(self.notif) , ft.SafeArea(self.notif1) , ft.SafeArea(self.notif2) , ft.SafeArea(self.notif3)]

class Hesabha(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/hesabha" , scroll='ALWAYS' , padding=20)
        self.my_docs = ''

        ##############################func zakhire hesabe entekhabi#######
        def entekhabi(c):
            global id_temp_hesab 
            id_temp_hesab=c.control.cells[0].content
        ############################# API ADD HESAB ################
        def GetAllHesab(token , code , name):
            token_url= "http://127.0.0.1:8000/accounts/allhesab/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{token}",
                'code_hesab':f'{code}',
                "name_hesab":f'{name}'
            }

            res = requests.post(token_url , data=request_data)
            return res.json()
        
        #########################API DELETE KARDANE HESAB######################
        def DeleteHesab(code_hesab):
            token_url= "http://127.0.0.1:8000/accounts/deletehesab/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                "code_hesab":code_hesab,
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################

        ##################################################################
        def ShowAllHesab(token):
            token_url= "http://127.0.0.1:8000/accounts/showall/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{token}",
            }

            res = requests.post(token_url , data=request_data)
            self.my_docs = res.json()

        ##################################################################
        ShowAllHesab(my_token['token'])
        self.page=page
        self.labal_page = ft.Text(value='لیست حساب های کل:')

        def on_submit(c):
            if self.code_hesab.value !='':
                if self.name_hesab.value !='':
                    rresult=GetAllHesab(my_token['token'] , self.code_hesab.value , self.name_hesab.value)
                    if rresult['token'] == 'ok':
                        self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(self.code_hesab.value)), ft.DataCell(ft.Text(self.name_hesab.value)),],on_select_changed=lambda e: [entekhabi(e) , page.go('/moein')] ))

                        self.code_hesab.value = ''
                        self.name_hesab.value = ''
                        self.update()
                    else:
                        self.notif2.open=True
                        self.update()
                else:
                    self.notif1.open=True
                    self.update()
            else:
                self.notif.open=True
                self.update()

        self.table=ft.DataTable(
            # bgcolor="blue",
            vertical_lines=ft.border.BorderSide(3, "grey"),
            border=ft.border.all(2, "grey"),
            border_radius=10,
            width=self.page.window.width-60,
            

            columns=[  
                ft.DataColumn(ft.Text("کد حساب")),
                ft.DataColumn(ft.Text("نام حساب"),numeric=True),
            ],
            )
        if len(self.my_docs)!=0:
            for i in self.my_docs:
                self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(i['code_hesab'])), ft.DataCell(ft.Text(i['name_hesab'])),],on_select_changed=lambda e: [entekhabi(e) , page.go('/moein')]))

        def remove_table(e):
            if self.code_hesab1.value !='':
                result = DeleteHesab(self.code_hesab1.value)
                if result['status'] == 'ok':
                    page.go('/landing22')
                    page.go('/hesabha')
                else:
                    self.notif3.open=True
                    self.update()


        ss=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS)], scroll= ft.ScrollMode.ALWAYS) , height=220 , width=self.page.window.width)]))
        self.hazf_label = ft.Text(value='حذف حساب:')
        self.code_hesab1 = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30, border_color='white')
        self.submit1_button= ft.ElevatedButton(text='حذف'  , height=50 , width=self.page.window.width/2-30 , on_click=remove_table )

        self.code_hesab = ft.TextField(label='کد حساب',hint_text='کد حساب' , width=self.page.window.width/2-30, border_color='white')
        self.name_hesab = ft.TextField(label='اسم حساب',hint_text='اسم حساب' , width=self.page.window.width/2-30, border_color='white')
        self.submit_button= ft.ElevatedButton(text='ثبت'  , height=50 , width=self.page.window.width-30 , on_click=on_submit )
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=50 , width=self.page.window.width-30 , on_click=lambda e: page.go('/landing22'))
        
        self.tozihat = ft.Text(value='با کلیک بر روی هر حساب به صفحه اضافه کردن حساب معین آن حساب کل منتقل می شوید.')
        self.my_col1_5 = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab1  ,self.submit1_button ])]))

        self.my_col = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[self.code_hesab ,self.name_hesab ])]))
        self.my_col2 = ft.SafeArea(ft.ResponsiveRow([ft.Column(controls=[self.submit_button , self.back_button,self.tozihat])]))


        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('کد حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('اسم حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('قبلا حسابی به این نام یا کد وارد کرده اید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حسابی با این کد وجود ندارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)


        


        self.controls = [self.labal_page,ss,self.my_col ,self.hazf_label,self.my_col1_5, self.my_col2 , ft.SafeArea(self.notif) , ft.SafeArea(self.notif1) , ft.SafeArea(self.notif2) , ft.SafeArea(self.notif3)]

class Accounts(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/records" , scroll='AUTO')

        self.my_docs = ''
        
        ############################# API Save SANAD #############
        def SaveSanadFinal( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/savesandfinal/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanadid
            }

            res = requests.post(token_url , data=request_data)

        ############################################################

        ############################# API DELETE SANAD #############
        def DeleteSanad( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/deletesnad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanadid
            }

            res = requests.post(token_url , data=request_data)

        ############################# API ADD HESAB ################
        def GetAllHesab( sanadid , kol , moein , tafs , sharhe_hesab , bedehkar , bestankar ):
            token_url= "http://127.0.0.1:8000/accounts/sabtesanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "kol":f"{kol}",
                "moein":f"{moein}",
                "tafs":f"{tafs}",
                "sharhe_hesab":f"{sharhe_hesab}",
                "bedehkar":f"{bedehkar}",
                "bestankar":f"{bestankar}",
                "sanadid":sanadid
            }

            res = requests.post(token_url , data=request_data)

        #########################API DELETE KARDANE RECORD######################
        def DeleteRecord(sanadid,sharhe_hesab , tafs , moein , kol , bestankar , bedehkar):
            token_url= "http://127.0.0.1:8000/accounts/deletespecific/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanadid,
                "sharhe_hesab":sharhe_hesab,
                "tafs":tafs,
                "moein":moein,
                "kol":kol,
                "bestankar":bestankar,
                "bedehkar":bedehkar

            }

            res = requests.post(token_url , data=request_data)
            return "ok"

        ##################################################################
        ##################################################################
        def checkshomaresanad(sanaid):
            token_url= "http://127.0.0.1:8000/accounts/checkshomaresanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":sanaid
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################
        
        ##################################################################
        def ShowAllHesab(token):
            token_url= "http://127.0.0.1:8000/accounts/showall/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{token}",
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ##################################################################
        self.my_docs = ShowAllHesab(my_token['token'])

        def moeinshow(e):
            token_url= "http://127.0.0.1:8000/accounts/moeinrecord/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'name_hesab':f'{self.kol.value}'
            }

            res = requests.post(token_url , data=request_data)
            my_moeins=res.json()
            self.dd.options = []
            self.tafsili.options = []
            if len(my_moeins) != 0:
                for i in my_moeins:
                    self.dd.options.append(ft.dropdown.Option(i['name_hesab']))    
            self.update()        

        def tafsilishow(e):
            token_url= "http://127.0.0.1:8000/accounts/tafsilirecord/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                'name_hesab':f'{self.dd.value}'
            }

            res = requests.post(token_url , data=request_data)
            my_tafsili=res.json()
            self.tafsili.options = []
            if len(my_tafsili) != 0:
                for i in my_tafsili:
                    self.tafsili.options.append(ft.dropdown.Option(i['name_hesab']))    
            self.update()        

        self.page = page 
        self.moein_label=ft.Text(value='معین:')
        self.dd = ft.Dropdown(
            width=page.width-10,
            on_change=tafsilishow,
            options=[
            ],
            border_color='white'
        )
        self.tafsili_label=ft.Text(value='تفصیلی:')
        self.tafsili = ft.Dropdown(
            width=page.width-10,
            options=[
            ],
            border_color='white'
        )
        self.kol_label=ft.Text(value='کل:')
        self.kol = ft.Dropdown(
            width=page.width-10,
            on_change=moeinshow,
            options=[
            ],
            border_color='white'
        )
        if len(self.my_docs) != 0:
            for i in self.my_docs:
                self.kol.options.append(ft.dropdown.Option(i['name_hesab']))

        self.point_delete = ft.SafeArea(ft.Text(value='برای حذف ستون های اضافه شده بر روی آن در جدول بزنید تا حذف شود' , color='blue' , weight=3))
        self.hesabha_section = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='انتخاب حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=130 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))],alignment=ft.MainAxisAlignment.CENTER))
        self.my_row = ft.SafeArea(ft.Container(ft.Column(controls=[self.point_delete ,self.hesabha_section,self.kol_label,self.kol,self.moein_label,self.dd]) ,padding=ft.Padding(top=0 , right=0, bottom=0 , left=0 )))
        self.my_row1 = ft.SafeArea(ft.Container(ft.Column(controls=[self.tafsili_label,self.tafsili]) ,padding=ft.Padding(top=0 , right=0, bottom=10 , left=0 )))
        
        self.table=ft.DataTable(
            vertical_lines=ft.border.BorderSide(3, "grey"),
            # border=ft.border.all(2, "grey"),
            border=ft.border.only(bottom=ft.border.BorderSide(2, "grey")),
            width=self.page.window.width-60,



            columns=[  
                ft.DataColumn(ft.Text("نام حساب")),
                ft.DataColumn(ft.Text("بدهکار"),numeric=True),
                ft.DataColumn(ft.Text("بستانکار"),numeric=True),
            ],
            )
        def deleter():
            if self.shomare_sanad !='':
                DeleteSanad(self.shomare_sanad )

        def remove_table(e , r , s):
            row_num = 0
            for i in self.my_sanads:  
                if str(s.value) in i.values() and str(r.value) in i.values() and str(e.value) in i.values():   
                    self.table.rows.remove(self.table.rows[row_num])
                    if str(i['bedehkar']) !="0":
                        self.bed_kol -= int(i['bedehkar'])
                        self.taraze_kol =self.bes_kol - self.bed_kol
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'
                        self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'

                    if str(i['bestankar']) !="0":
                        self.bes_kol -= int(i['bestankar'])
                        self.taraze_kol = self.bes_kol - self.bed_kol
                        self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'


                    self.update()
                    obj=DeleteRecord(self.shomare_sanad , i['sharhe_hesab'] , i['tafsili'] , i['moein'] , i['kol'] ,i['bestankar'] , i['bedehkar'] )
                    return
                else:
                    row_num+=1
            


        self.my_sanads = []
        self.taraze_kol = 0
        self.bed_kol = 0
        self.bes_kol = 0
        self.shomare_sanad = ''
        def addsanad(e):
            tmp = {}
            if self.bestankar.value !='' or self.bedehkar.value !='':
                if not (self.bestankar.value!='' and self.bedehkar.value !=''):
                    if self.kol.value !=None and self.dd.value !=None and self.tafsili.value !=None:
                        if self.sanadID.value !='':
                            check_sanad=checkshomaresanad(self.sanadID.value)
                            if check_sanad['answer'] == "yes":
                                self.notif7.open=True
                                self.update()
                                return
                            if self.sharh.value !='':
                                self.sanadID.read_only=True
                                if self.bestankar.value !='':
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bestankar":self.bestankar.value , "sharhe_hesab":self.sharh.value , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value , 'deleter':f'{self.tafsili.value}\n{self.sharh.value}' , 'bedehkar':"0"}
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , 0 , self.bestankar.value)
                                    self.my_sanads.append(tmp)
                                    self.bes_kol += int(self.bestankar.value)
                                    self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                                    self.taraze_kol += int(self.bestankar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1
                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text("0" , color='red')), ft.DataCell(ft.Text(self.bestankar.value , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''

                                    self.update()
                                elif self.bedehkar.value !='':
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bedehkar":self.bedehkar.value , "sharhe_hesab":self.sharh.value, 'deleter':f'{self.tafsili.value}\n{self.sharh.value}' , 'bestankar':"0" , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value}
                                    self.my_sanads.append(tmp)
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , self.bedehkar.value , 0 )
                                    self.bed_kol += int(self.bedehkar.value)
                                    self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'
                                    self.taraze_kol -= int(self.bedehkar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1

                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text(self.bedehkar.value , color='red')), ft.DataCell(ft.Text("0" , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''
                                    
                                    self.update()

                            else:
                                self.notif4.open=True
                                self.update()
                        else:
                            self.notif2.open=True
                            self.update()

                    else:
                        self.notif.open=True
                        self.update()
                
                else:
                    self.notif3.open=True
                    self.update()
            else:
                self.notif1.open=True
                self.update()      

        def savasanad(e):
            if self.shomare_sanad !='':
                if self.taraze_kol == 0:
                    SaveSanadFinal(self.shomare_sanad)
                    self.notif6.open=True
                    self.update()
                else:
                    self.notif5.open=True
                    self.update()
            else:
                self.notif2.open=True
                self.update()



        self.my_col=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS , vertical_alignment='center')], scroll= ft.ScrollMode.ALWAYS , horizontal_alignment='center',) , height=220 , width=self.page.window.width , border_radius=10 , shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))]))

        self.bestankar_label = ft.Text(value='تراز بستانکار:')
        self.bedehkar_label = ft.Text(value='تزار بدهکار:')
        self.ban_bas_label = ft.Text(value='تزار بن-بس:')

        self.my_row2 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.bestankar_label,self.bedehkar_label,self.ban_bas_label] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=30 ,right=0 ,left=0 , bottom=0))]))

        self.info_sanad = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='اطلاعات حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=140 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600) )],alignment=ft.MainAxisAlignment.CENTER))

        self.bestankar = ft.TextField(label='بستانکار' , width=self.page.width/2-25 , color='green', border_color='white')
        self.bedehkar = ft.TextField(label='بدهکار' , width=self.page.width/2-25 , color='red', border_color='white')
        self.sharh = ft.TextField(label='شرح حساب' , width=self.page.width-10  , border_color='white')


        self.my_row7 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Row(controls=[self.bestankar,self.bedehkar] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=10 ,right=0 ,left=0 , bottom=0))]))

        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('اضافه کردن' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=addsanad,
            width=self.page.width-10 
        )

        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ذخیره سند' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=savasanad,
            width=self.page.width-10 
        )

        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=lambda e: [deleter(),page.go('/landing22')],
            width=self.page.width-10 
        )

        self.ssabt = ft.ElevatedButton(text='اضافه کردن' , width=self.page.width-10 , height=45 , on_click=addsanad)
        self.my_row8 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[ self.sharh] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=5 ,right=0 ,left=0 , bottom=0))]))


        self.sanadID = ft.TextField(label='شماره سند' , width=self.page.width-10 , border_color='white')

        self.my_row3 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.sanadID] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=10 ,right=0 ,left=0 , bottom=0))]))

        self.save_sanad = ft.ElevatedButton(text='ذخیره سند' , width=page.width-10 , height=45 ,on_click=savasanad)
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=45 , width=page.width-10 , on_click=lambda e: [deleter(),page.go('/landing22')])

        self.my_row4 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.save_sanad ] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=15 ,right=0 ,left=0 , bottom=0))]))
        self.my_row5 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.back_button] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=0 ,right=0 ,left=0 , bottom=0))]))

        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حساب های کل و تفصیلی و معین را انتخاب کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('شماره سند را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('در هر بار فقط یا بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif4 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار شرح حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif5 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('تراز بن بس باید صفر باشد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif6 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('ذخیره شد'),
            ft.Icon(name=ft.icons.DONE, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif7 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('شماره سند قبلا ثبت شده است'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.controls=[self.my_col,self.my_row,self.my_row1,self.info_sanad,self.my_row7,self.my_row8,ft.SafeArea(ft.Row(controls=[self.button0])),self.my_row3,self.my_row2,ft.SafeArea(ft.Row(controls=[self.button1])),ft.SafeArea(ft.Row(controls=[self.button2])), ft.SafeArea(self.notif),ft.SafeArea(self.notif1),ft.SafeArea(self.notif2),ft.SafeArea(self.notif3),ft.SafeArea(self.notif4),ft.SafeArea(self.notif5) , ft.SafeArea(self.notif6) , ft.SafeArea(self.notif7)]



class Profile(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/landing" )

        ####################### delete all unverified records ########################
        def DeleteSanad( ):
            token_url= "http://127.0.0.1:8000/accounts/predeletesanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
            }

            res = requests.post(token_url , data=request_data)

        ####################### delete all unverified records ########################

        ####################### gerefrane etelaat user ########################
        def getuserinfo( ):
            token_url= "http://127.0.0.1:8000/accounts/getuserinfo/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ####################### gerefrane etelaat user ########################
        getuser = getuserinfo()

        self.page = page 

        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('ورود موفقیت آمیز'),
            ft.Icon(name=ft.icons.DONE, color=ft.colors.PINK),
        ]) , duration=2000)
        
        timer = my_token['timer']
        
        total_seconds = int(timer) - int(time.time())
        total_days = int(total_seconds/86400)
        
        self.container_main = ft.SafeArea(ft.Container(
            height=self.page.window.height,
            width=self.page.window.width,
            border_radius=35,
            bgcolor='#041955',
            content=ft.Stack(
                controls=[
                    ft.Container(height=self.page.window.height,width=self.page.window.width,bgcolor='#3450a1',border_radius=35),
                    ft.Container(height=200,
                    width=self.page.window.width-50
                    ,bgcolor='#041955'
                    ,border_radius=35
                     , alignment=ft.alignment.center 
                     , margin=15 , 
                     ),
                     ft.Container(width=200 , height=30,bgcolor='#041955' ,border_radius=35 , alignment=ft.alignment.center_right , margin=ft.margin.only(top=45 , right=32) , content=ft.Text(f"نام کاربری:{getuser['username']}") ),
                     ft.Container(width=200 , height=30,bgcolor='#041955' ,border_radius=35 , alignment=ft.alignment.center_right , margin=ft.margin.only(top=75 , right=45) , content=ft.Text(f'مدت زمان اعتبار:{total_days}روز') ),
                     ft.Container(width=150 , height=30,bgcolor='#3450a1' ,border_radius=35 , alignment=ft.alignment.center , margin=ft.margin.only(top=145 , right=45) , content=ft.Text('وضعیت : فعال') ),
                     ft.Container(width=self.page.window_width-50 , height=100,bgcolor='#3450a1' ,border_radius=35 , alignment=ft.alignment.top_left , margin=ft.margin.only(top=40 , right=200) ,shape = ft.BoxShape('circle'), image_src='/accountant.jpg' , image_fit='cover' , shadow = ft.BoxShadow(spread_radius=6,blur_radius=20,color = ft.colors.with_opacity(0.71,'black'))),
                     ft.Column(controls=[ft.Container(width=self.page.window.width-70 , height=47,bgcolor='#041955' ,border_radius=35 , alignment=ft.alignment.center , margin=ft.margin.only(top=230 , right=20) , content=ft.Text('ثبت سند' , text_align=ft.TextAlign.LEFT , size=22 , font_family='b yekan+') ,on_click=lambda _: [DeleteSanad(), page.go('/records')]), ft.Container(width=self.page.window.width-70 , height=47,bgcolor='#041955' ,border_radius=35 , alignment=ft.alignment.center , margin=ft.margin.only(top=20 , right=20) , content=ft.Text('مدیریت حساب ها' , text_align=ft.TextAlign.LEFT , size=22 , font_family='b yekan+'),on_click=lambda _: page.go('/hesabha')),ft.Container(width=self.page.window.width-70 , height=47,bgcolor='#041955' ,border_radius=35 , alignment=ft.alignment.center , margin=ft.margin.only(top=20 , right=20) , content=ft.Text('اسناد ثبت شده' , text_align=ft.TextAlign.LEFT , size=22 , font_family='b yekan+') , on_click=lambda _:  page.go('/history')),],spacing=0),
                     
                     
                     

                ]

            )

        )
        )
        # self.container_header = ft.Container(
        #         height=200,
        #         width=self.page.window_width,
        #         bgcolor='blue',
        #         border_radius=35)
        self.controls=[self.container_main]

        # self.container1=ft.SafeArea(ft.Container(
        #     bgcolor='white10',
        #     width=128,
        #     height=128,
        #     shape = ft.BoxShape('circle'),
        #     image_src='/main.jpg',
        #     image_fit='cover',
        #     shadow = ft.BoxShadow(
        #         spread_radius=6,
        #         blur_radius=20,
        #         color = ft.colors.with_opacity(0.71,'black')
        #     )
        # ))

        # self.container2=ft.SafeArea(ft.Container(
        #     bgcolor='white10',
        #     width=128,
        #     height=100,
        #     shape = ft.BoxShape('rectangle'),
        #     content = ft.Text(f'مدیریت \n حساب ها' , color='purple',size=18 , text_align='center' , font_family='b yekan+'),
        #     on_click=lambda _: page.go('/hesabha'),
        #     shadow = ft.BoxShadow(
        #         spread_radius=6,
        #         blur_radius=20,
        #         color = ft.colors.with_opacity(0.71,'black')
        #     )
        # ))

        # self.container3=ft.SafeArea(ft.Container(
        #     bgcolor='white10',
        #     width=128,
        #     height=100,
        #     shape = ft.BoxShape('rectangle'),
        #     content = ft.Text(f'ثبت سند' , color='purple',size=18 , text_align='center' , font_family='b yekan+'),
        #     on_click=lambda _: [DeleteSanad(), page.go('/records')],
        #     shadow = ft.BoxShadow(
        #         spread_radius=6,
        #         blur_radius=20,
        #         color = ft.colors.with_opacity(0.71,'black')
        #     )
        # ))

        # self.container4=ft.SafeArea(ft.Container(
        #     bgcolor='white10',
        #     width=128,
        #     height=100,
        #     shape = ft.BoxShape('rectangle'),
        #     content = ft.Text(f'اسناد' , color='purple',size=18 , text_align='center' , font_family='b yekan+'),
        #     on_click=lambda _:  page.go('/history'),
        #     shadow = ft.BoxShadow(
        #         spread_radius=6,
        #         blur_radius=20,
        #         color = ft.colors.with_opacity(0.71,'black')
        #     )
        # ))



        # self.controls=[ft.SafeArea(ft.ResponsiveRow([ft.Column(
        #     alignment=ft.MainAxisAlignment.START,
        #     horizontal_alignment='center',
        #     controls=[ft.SafeArea(self.container1) ,ft.SafeArea(ft.Row(controls=[self.container2 , self.container3 ],width=self.page.window_width )), ft.SafeArea(ft.Row(controls=[self.container4],width=self.page.window_width , alignment=ft.MainAxisAlignment.CENTER)),ft.SafeArea(self.notif)],
        #     spacing=40
        #     ),

        # ]))
        # ]

        # self.notif.open=True


##########################################################Edit AI Sanad




class EditRecord22(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/editrecord22" , scroll='AUTO')

        self.my_docs = ''


        ############################# API Save SANAD #############
        def restoreedit():
            token_url= "http://127.0.0.1:8000/accounts/showeditedsanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ############################################################
        restore_edit = restoreedit()
        ############################# API Save SANAD #############
        def SaveSanadFinal( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/savesandfinal/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        ############################################################

        ############################# API DELETE SANAD #############
        def DeleteSanad( sanadid  ):
            token_url= "http://127.0.0.1:8000/accounts/deletesnad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        ############################# API ADD HESAB ################
        def GetAllHesab( sanadid , kol , moein , tafs , sharhe_hesab , bedehkar , bestankar ):
            token_url= "http://127.0.0.1:8000/accounts/sabtesanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
                "kol":f"{kol}",
                "moein":f"{moein}",
                "tafs":f"{tafs}",
                "sharhe_hesab":f"{sharhe_hesab}",
                "bedehkar":f"{bedehkar}",
                "bestankar":f"{bestankar}",
                "sanadid":final_id
            }

            res = requests.post(token_url , data=request_data)

        #########################API DELETE KARDANE RECORD######################
        def DeleteRecord(sanadid,sharhe_hesab , tafs , moein , kol , bestankar , bedehkar):
            token_url= "http://127.0.0.1:8000/accounts/deletespecific/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }
            request_data ={
                "token":f"{my_token['token']}",
                "sanadid":final_id,
                "sharhe_hesab":sharhe_hesab,
                "tafs":tafs,
                "moein":moein,
                "kol":kol,
                "bestankar":bestankar,
                "bedehkar":bedehkar

            }

            res = requests.post(token_url , data=request_data)
            return "ok"

        ##################################################################


        self.page = page 
        self.moein_label=ft.Text(value='معین:')
        self.dd = ft.TextField(
            width=page.width-10,
            border_color='white'
        )
        self.tafsili_label=ft.Text(value='تفصیلی:')
        self.tafsili = ft.TextField(
            width=page.width-10,
            border_color='white'
        )
        self.kol_label=ft.Text(value='کل:')
        self.kol = ft.TextField(
            width=page.width-10,
            border_color='white'
        )

        self.point_delete = ft.SafeArea(ft.Text(value='برای حذف ستون های اضافه شده بر روی آن در جدول بزنید تا حذف شود' , color='blue' , weight=3))
        self.hesabha_section = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='انتخاب حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=130 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))],alignment=ft.MainAxisAlignment.CENTER))

        self.my_row = ft.SafeArea(ft.Container(ft.Column(controls=[self.point_delete,self.hesabha_section,self.kol_label,self.kol,self.moein_label,self.dd]) ,padding=ft.Padding(top=0 , right=0, bottom=0 , left=0 )))
        self.my_row1 = ft.SafeArea(ft.Container(ft.Column(controls=[self.tafsili_label,self.tafsili]) ,padding=ft.Padding(top=0 , right=0, bottom=10 , left=0 )))
        
        self.table=ft.DataTable(
            vertical_lines=ft.border.BorderSide(3, "grey"),
            # border=ft.border.all(2, "grey"),
            border=ft.border.only(bottom=ft.border.BorderSide(2, "grey")),
            width=self.page.window.width-60,



            columns=[  
                ft.DataColumn(ft.Text("نام حساب")),
                ft.DataColumn(ft.Text("بدهکار"),numeric=True),
                ft.DataColumn(ft.Text("بستانکار"),numeric=True),
            ],
            )
        def deleter():
            if self.shomare_sanad !='':
                DeleteSanad(self.shomare_sanad )
        
        def remove_table(e , r , s):
            row_num = 0
            for i in self.my_sanads: 
                # print(type(i.values()[5])) 
                tmp_checker = f"{i['tafsili']}\n{i['sharhe_hesab']}"
                if str(s.value) in i.values() and str(r.value) in i.values() and e.value in tmp_checker: 
                    self.table.rows.remove(self.table.rows[row_num])
                    if str(i['bedehkar']) !="0":
                        print('1')
                        self.bed_kol -= int(i['bedehkar'])
                        if self.taraze_kol <0:
                            print('negative')
                            self.taraze_kol += int(i['bedehkar'])
                        elif self.taraze_kol >=0:
                            print('positive')
                            self.taraze_kol += int(i['bedehkar'])
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'
                        self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'
                        del self.my_sanads[row_num]

                    if str(i['bestankar']) !="0":
                        self.bes_kol -= int(i['bestankar'])
                        if self.taraze_kol <0:
                            print('negative')
                            self.taraze_kol -= int(i['bestankar'])
                        elif self.taraze_kol >=0:
                            print('positive')
                            self.taraze_kol -= int(i['bestankar'])
                            print(self.taraze_kol)

                        self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                        self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'
                        del self.my_sanads[row_num]

                    self.update()
                    obj=DeleteRecord(self.shomare_sanad , i['sharhe_hesab'] , i['tafsili'] , i['moein'] , i['kol'] ,i['bestankar'] , i['bedehkar'] )
                    return
                else:
                    row_num+=1

        self.my_sanads = []
        self.taraze_kol = 0
        self.bed_kol = 0
        self.bes_kol = 0
        self.shomare_sanad = final_id
        def addsanad(e):
            tmp = {}
            if self.bestankar.value !='' or self.bedehkar.value !='':
                if not (self.bestankar.value!='' and self.bedehkar.value !=''):
                    if self.kol.value !=None and self.dd.value !=None and self.tafsili.value !=None:
                        if self.sanadID.value !='':
                            if self.sharh.value !='':
                                self.sanadID.read_only=True
                                if self.bestankar.value !='':
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bestankar":self.bestankar.value,"bedehkar":"0" , "sharhe_hesab":self.sharh.value , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value}
                                    self.my_sanads.append(tmp)
                                    # tmp=json.dumps(tmp)
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , 0 , self.bestankar.value)
                                    self.bes_kol += int(self.bestankar.value)
                                    self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                                    self.taraze_kol += int(self.bestankar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1
                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text("0" , color='red')), ft.DataCell(ft.Text(self.bestankar.value , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''

                                    self.update()
                                elif self.bedehkar.value !='':
                                    self.shomare_sanad = self.sanadID.value
                                    tmp = {"bedehkar":self.bedehkar.value, "bestankar":"0" , "sharhe_hesab":self.sharh.value , "kol":self.kol.value , "moein":self.dd.value , "tafsili":self.tafsili.value}
                                    self.my_sanads.append(tmp)
                                    GetAllHesab(self.sanadID.value,self.kol.value , self.dd.value , self.tafsili.value , self.sharh.value , self.bedehkar.value , 0 )
                                    self.bed_kol += int(self.bedehkar.value)
                                    self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'

                                    self.taraze_kol -= int(self.bedehkar.value)

                                    self.ban_bas_label.value = f'تراز بن-بس : {self.taraze_kol}'

                                    final_sharh = ''
                                    counter = 1
                                    for i in self.sharh.value:
                                        if (counter)/10 == 0:
                                            final_sharh+=f'{i}\n'
                                            counter+=1
                                        else:
                                            final_sharh +=i
                                            counter +=1

                                    text_add = f'{self.tafsili.value}\n{final_sharh}'
                                    self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text(self.bedehkar.value , color='red')), ft.DataCell(ft.Text("0" , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                                    self.sharh.value = ''
                                    self.bestankar.value = ''
                                    self.bedehkar.value = ''
                                    self.tafsili.value = ''
                                    self.dd.value = ''
                                    self.kol.value = ''
                                    
                                    self.update()

                            else:
                                self.notif4.open=True
                                self.update()
                        else:
                            self.notif2.open=True
                            self.update()

                    else:
                        self.notif.open=True
                        self.update()
                
                else:
                    self.notif3.open=True
                    self.update()
            else:
                self.notif1.open=True
                self.update()      

        def savasanad(e):
            if self.shomare_sanad !='':
                if self.taraze_kol == 0:
                    SaveSanadFinal(self.shomare_sanad)
                    self.notif6.open=True
                    self.update()
                else:
                    self.notif5.open=True
                    self.update()
            else:
                self.notif2.open=True
                self.update()


        
        self.my_col=ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column([ft.Row([self.table], scroll= ft.ScrollMode.ALWAYS , vertical_alignment='center')], scroll= ft.ScrollMode.ALWAYS , horizontal_alignment='center',) , height=220 , width=self.page.window.width , border_radius=10 , shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600))]))

        self.bestankar_label = ft.Text(value='تراز بستانکار:')
        self.bedehkar_label = ft.Text(value='تزار بدهکار:')
        self.ban_bas_label = ft.Text(value='تزار بن-بس:')

        if len(restore_edit) !=0:
            for i in restore_edit:
                if str(i['bedehkar']) =="0":
                    tmp = {"bestankar":str(i['bestankar']) , "sharhe_hesab":i['sharhe_hesab'] , "kol":i['kol'] , "moein":i['moein'] , "tafsili":i['tafs'] , 'deleter':f"{i['tafs']}\n{i['sharhe_hesab']}" , 'bedehkar':"0"}
                if str(i['bestankar'])=="0":
                    tmp = {"bedehkar":str(i['bedehkar']) , "sharhe_hesab":i['sharhe_hesab'] , "kol":i['kol'] , "moein":i['moein'] , "tafsili":i['tafs'] , 'deleter':f"{i['tafs']}\n{i['sharhe_hesab']}" , 'bestankar':"0"}

                self.my_sanads.append(tmp)
                text_add = f"{i['tafs']}\n{i['sharhe_hesab']}"
                self.table.rows.insert(len(self.table.rows), ft.DataRow([ft.DataCell(ft.Text(text_add)), ft.DataCell(ft.Text(i['bedehkar'] , color='red')), ft.DataCell(ft.Text(i['bestankar'] , color='green')),],on_select_changed=lambda e:remove_table(e.control.cells[0].content,e.control.cells[1].content,e.control.cells[2].content)))
                self.bed_kol += int(i['bedehkar'])
                self.bes_kol += int(i['bestankar'])
                self.bestankar_label.value = f'تراز بستانکار : {self.bes_kol}'
                self.bedehkar_label.value = f'تراز بدهکار : {self.bed_kol}'

            self.taraze_kol -= self.bed_kol
            self.taraze_kol += self.bes_kol
            self.ban_bas_label.value = f'تراز بن-بس: {self.taraze_kol}'
            self.update()

        print(self.my_sanads)
        self.my_row2 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.bestankar_label,self.bedehkar_label,self.ban_bas_label] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=30 ,right=0 ,left=0 , bottom=0))]))



        self.info_sanad = ft.SafeArea(ft.Row(controls=[ft.Container(content=ft.Text(value='اطلاعات حساب' , size=20 , font_family='b yekan+' , text_align=ft.TextAlign.CENTER) , border_radius=10 , width=140 , bgcolor='purple' ,shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),border=ft.border.all(5, ft.colors.GREY_600) )],alignment=ft.MainAxisAlignment.CENTER))

        self.bestankar = ft.TextField(label='بستانکار' , width=self.page.width/2-25 , color='green', border_color='white')
        self.bedehkar = ft.TextField(label='بدهکار' , width=self.page.width/2-25 , color='red', border_color='white')
        self.sharh = ft.TextField(label='شرح حساب' , width=self.page.width-10  , border_color='white')


        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('اضافه کردن' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=addsanad,
            width=self.page.width-10 
        )

        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ذخیره سند' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=savasanad,
            width=self.page.width-10 
        )

        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=45,
            on_click=lambda e: [deleter(),page.go('/landing22')],
            width=self.page.width-10 
        )


        self.my_row7 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Row(controls=[self.bestankar,self.bedehkar] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=10 ,right=0 ,left=0 , bottom=0))]))

        self.ssabt = ft.ElevatedButton(text='اضافه کردن' , width=self.page.width-10 , height=45 , on_click=addsanad)
        self.my_row8 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[ self.sharh  ] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=5 ,right=0 ,left=0 , bottom=0))]))


        self.sanadID = ft.TextField(label='شماره سند' , width=self.page.width-10 , border_color='white')
        self.sanadID.value = f'{final_id}'
        self.sanadID.read_only=True

        self.my_row3 = ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.sanadID] , alignment='center' , width=self.page.window.width),padding=ft.Padding(top=30 ,right=0 ,left=0 , bottom=0))]))

        self.save_sanad = ft.ElevatedButton(text='ذخیره سند' , width=page.width-10 , height=45 ,on_click=savasanad)
        self.back_button= ft.ElevatedButton(text='بازگشت'  , height=45 , width=page.width-10 , on_click=lambda e: [deleter(),page.go('/landing22')])

        self.my_row4 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.save_sanad ] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=15 ,right=0 ,left=0 , bottom=0))]))
        self.my_row5 =ft.SafeArea(ft.ResponsiveRow([ft.Container(ft.Column(controls=[self.back_button] , alignment=ft.MainAxisAlignment.CENTER , width=self.page.window.width),padding=ft.Padding(top=0 ,right=0 ,left=0 , bottom=0))]))


        self.notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('حساب های کل و تفصیلی و معین را انتخاب کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif1 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif2 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('شماره سند را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif3 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('در هر بار فقط یا بستانکار یا بدهکار را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif4 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('مقدار شرح حساب را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.notif5 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('تراز بن بس باید صفر باشد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)
        self.notif6 = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('ذخیره شد'),
            ft.Icon(name=ft.icons.DONE, color=ft.colors.PINK),
        ]) , duration=2000)



        self.controls=[self.my_col,self.my_row,self.my_row1,self.info_sanad,self.my_row7,self.my_row8,ft.SafeArea(ft.Row(controls=[self.button0])),self.my_row3,self.my_row2,ft.SafeArea(ft.Row(controls=[self.button1])),ft.SafeArea(ft.Row(controls=[self.button2])), ft.SafeArea(self.notif),ft.SafeArea(self.notif1),ft.SafeArea(self.notif2),ft.SafeArea(self.notif3),ft.SafeArea(self.notif4),ft.SafeArea(self.notif5) , ft.SafeArea(self.notif6)]











################################### sand zane hoshmand


global temp_ai_list
global temp_ai_sanad
temp_ai_sanad = {"kind":None , 'price':None,"tozihat":None , "kol":None , 'tafsili':None , 'moein':None }
temp_ai_list = []
global price_kol
price_kol = 0
class Ai_hesab_sanad(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/page5ai")
        self.page = page

        ####################### gerefrane etelaat user ########################
        def savefinal(allasnad):
            token_url= "http://127.0.0.1:8000/accounts/savefinalai/"

            headers = {
                "accept":"application/json",
                "Content-Type":"application/json",
            }
            # request_data ={
            #     "token":f"{my_token['token']}",

            # }
            tmp = {'token':my_token['token']}
            allasnad.append(tmp)

            res = requests.post(token_url ,json=allasnad)
            return res.json()

        ####################### gerefrane etelaat user ########################


        def on_press_continue(c):
            if textField_kol.value == '' or textField_moein.value == "" or textField_tafsili.value =="":
                alert_user.open=True
                self.page.update()
                return

            global temp_ai_sanad
            temp_ai_sanad['kol'] = textField_kol.value
            temp_ai_sanad['moein'] = textField_moein.value
            temp_ai_sanad['tafsili'] = textField_tafsili.value
            temp_ai_list.append(temp_ai_sanad)
            self.page.go('/page1ai')
            self.page.update()
            
            
        
        def on_press_finish(c):
            if int(price_kol) != 0 :
                alert_taraz.open=True
                self.page.update()
                return

            if textField_kol.value == '' or textField_moein.value == "" or textField_tafsili.value =="":
                alert_user.open=True
                self.page.update()
                return

            global temp_ai_sanad
            temp_ai_sanad['kol'] = textField_kol.value
            temp_ai_sanad['moein'] = textField_moein.value
            temp_ai_sanad['tafsili'] = textField_tafsili.value
            temp_ai_list.append(temp_ai_sanad)
            checker = savefinal(allasnad=temp_ai_list)
            self.page.go('/landing22')
            self.page.update()

        # nameBox =  ft.Text('' , color='white',size=18 , font_family="b yekan+",)
        textField_kol = ft.TextField(width=self.page.window.width , password=False , hint_text='توضیحات خود را بنویسید' , border_radius=10 , border_color='white' , label='کل' )
        textField_moein = ft.TextField(width=self.page.window.width , password=False , hint_text='توضیحات خود را بنویسید' , border_radius=10 , border_color='white' , label='معین' )
        textField_tafsili = ft.TextField(width=self.page.window.width , password=False , hint_text='توضیحات خود را بنویسید' , border_radius=10 , border_color='white' , label='تفصیلی' )
        global price_kol
        if len(temp_ai_list)!=0:
            for i in temp_ai_list:
                if "price" in i.keys():
                    if i['kind'] == "buy":
                        
                        price_kol -= float(i['price'])
                    else:
                        price_kol += float(i['price'])
        else:
            if "price" in temp_ai_sanad.keys():
                if temp_ai_sanad['kind'] == "buy":
                    price_kol -= float(temp_ai_sanad['price'])
                else:
                    price_kol += float(temp_ai_sanad['price'])
            

        taraz = ft.Text(f'تراز بن-بس : {price_kol}' , color='white',size=18 , font_family="b yekan+",)
        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت و ادامه ی سفارشات' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press_continue(_)
        )

        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت و اتمام فرآیند' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press_finish(_)
        )
        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/page4ai')
        )

        alert_user = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('همه ی فیلدهارا پر کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        alert_taraz = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('تراز بن-بس باید صفر شود'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)



        self.controls=[ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        # nameBox,
                        textField_kol,
                        ft.Divider(height=3 , color='transparent'),
                        textField_moein,
                        ft.Divider(height=3 , color='transparent'),
                        textField_tafsili,
                        ft.Divider(height=3 , color='transparent'),
                        taraz,
                        ft.Divider(height=5 , color='yellow'),
                        ft.Row(
                            controls = [self.button0],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button1],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button2],
                            alignment='center',
                            height=45
                        ),
                        alert_user,
                        alert_taraz

            ])
        )]





class AI_tozihat_sanad(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/page4ai")
        self.page = page

        def on_press(c):
            if textField.value == "":
                alert_user.open=True
                self.page.update()
                return
            
            temp_ai_sanad['tozihat'] = textField.value
            self.page.go('/page5ai')
            self.page.update()

        nameBox =  ft.Text('توضیحاتی راجب آن بنویسید' , color='white',size=18 , font_family="b yekan+",)
        textField = ft.TextField(width=self.page.window.width , password=False , hint_text='توضیحات خود را بنویسید\n\n\n' , border_radius=10 , border_color='white' , multiline=True)


        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press(_)
        )

        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/page3ai')
        )
        alert_user = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('همه ی فیلدهارا پر کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)


        self.controls=[ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        nameBox,
                        textField,
                        ft.Row(
                            controls = [self.button1],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button0],
                            alignment='center',
                            height=45
                        ),
                        alert_user

            ])
        )]



class AI_kind_sanad(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/page1ai")
        self.page = page

                                                                                                                                                                                                        
        
        def on_press_buy(c):
            temp_ai_sanad['kind'] = "buy"
            self.page.go('/page3ai')
            self.page.update()
        
        def on_press_sell(c):
            temp_ai_sanad['kind'] = "sell"
            self.page.go('/page3ai')
            self.page.update()

        nameBox =  ft.Text('نوع سند را انتخاب کنید' , color='white',size=18 , font_family="b yekan+",)
        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('خرید' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press_buy(_)
        )
        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('فروش' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press_sell(_)
        )
        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/landing22')
        )
        alert_user = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('همه ی فیلدهارا پر کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.controls=[ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        nameBox,
                        ft.Row(
                            controls = [self.button0 , self.button1],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button2],
                            alignment='center',
                            height=45
                        ),
                        alert_user

            ])
        )]




class AI_price_sanad(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/page3ai")
        self.page = page

        def on_press(c):
            if inputBox.value == '':
                alert_user.open=True
                self.page.update()
                return
            temp_ai_sanad['price'] = inputBox.value
            self.page.go('/page4ai')
            self.page.update()

        _filter = ft.InputFilter('^[0-9]*')
        nameBox =  ft.Text('قیمت آن را وارد کنید' , color='white',size=18 , font_family="b yekan+",)
        inputBox = ft.TextField(width=self.page.window.width ,input_filter=_filter, password=False , hint_text='قیمت خرید یا فروش را وارد کنید' , border_radius=10 , border_color='white')
        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:on_press(_)
        )
        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/page1ai')
        )

        alert_user = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('همه ی فیلدهارا پر کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.controls=[ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        nameBox,
                        inputBox,
                        ft.Row(
                            controls = [self.button0],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button1],
                            alignment='center',
                            height=45
                        ),
                        alert_user

            ])
        )]
        



class AI_name_sanad(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/page2ai")
        self.page = page

        nameBox =  ft.Text('چه خریده اید یا فروخته اید ؟' , color='white',size=18 , font_family="b yekan+",)
        inputBox = ft.TextField(width=self.page.window.width , password=False , hint_text='اسم چیزی که خریده اید یه فروخته اید را وارد کنید' , border_radius=10 , border_color='white')
        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/page3ai')
        )
        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('بازگشت' , color='black',size=22 , font_family="b yekan+",),
            # padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            height=200,
            on_click=lambda _:page.go('/page1ai')
        )

        self.controls=[ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        nameBox,
                        inputBox,
                        ft.Row(
                            controls = [self.button0],
                            alignment='center',
                            height=45
                        ),
                        ft.Row(
                            controls = [self.button1],
                            alignment='center',
                            height=45
                        ),

            ])
        )]
        


#################################### End -> sanad zane hoshmand

################################### Profile jadid


link_style = {
    'height':50,
    "focused_border_color": "#F4CE14",
    "border_radius":5,
    "cursor_height":16,
    "cursor_color":"white",
    "content_padding":10,
    "border_width":1.5,
    "text_size":14,
    "label_style": ft.TextStyle(color='#F4CE14')
}
class Link(ft.TextField):
    def __init__(self , label:str , value:str , page:ft.Page):
        super().__init__(
            value=value,
            read_only=True,
            label=label,
            on_focus=self.selected,
            **link_style
        )

        self.page=page
    
    def selected(self,event:ft.TapEvent = None):
        
        
        self.page.snack_bar = ft.SnackBar(
            ft.Text(f'Copied {self.label}!'),
            show_close_icon=True,
            duration=2000
        )

        self.page.snack_bar.open=True
        self.page.update()


class Profile22(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/landing22" )

        ####################### delete all unverified records ########################
        def DeleteSanad( ):
            token_url= "http://127.0.0.1:8000/accounts/predeletesanad/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
            }

            res = requests.post(token_url , data=request_data)

        ####################### delete all unverified records ########################

        ####################### gerefrane etelaat user ########################
        def getuserinfo( ):
            token_url= "http://127.0.0.1:8000/accounts/getuserinfo/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "token":f"{my_token['token']}",
            }

            res = requests.post(token_url , data=request_data)
            return res.json()

        ####################### gerefrane etelaat user ########################
        getuser = getuserinfo()
        
        self.lock = ft.Icon(

            name= "lock" , scale=ft.Scale(4)
        )
        timer = my_token['timer']
        
        total_seconds = int(timer) - int(time.time())
        total_days = int(total_seconds/86400)

        #Define a button to route to profile
        self.button0 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('سند زن هوشمند' , color='black',size=18 , font_family="b yekan+",),
            padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            on_click=lambda _:page.go('/page1ai')
        )

        self.button = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('ثبت سند' , color='black',size=18 , font_family="b yekan+",),
            padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            on_click=lambda _:page.go('/records')
        )
        self.button1 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('مدیریت حساب ها' , color='black',size=18 , font_family="b yekan+"),
            padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            on_click=lambda _:page.go('/hesabha')
        )
        self.button2 = ft.Container(
            border_radius=5,
            expand=True , 
            bgcolor='#F4CE14',
            content = ft.Text('اسناد ثبت شده' , color='black',size=18 , font_family="b yekan+") ,
            padding=ft.padding.only(left=25,right=25,top=10 , bottom=10),
            alignment=ft.alignment.center,
            on_click=lambda _:page.go('/history')
        )


        self.page =page

        self.controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment='center',
                    controls=[
                        ft.Divider(height=20 , color='transparent'),
                        ft.Container(
                            bgcolor='white10',
                            width=128,
                            height=128,
                            shape = ft.BoxShape('circle'),
                            image_src='./assets/accountant.jpg',
                            image_fit='cover',
                            shadow = ft.BoxShadow(spread_radius=6, blur_radius=20,color = ft.colors.with_opacity(0.71,'black')),

                        ),
                        ft.Divider(height=10 , color='transparent'),
                        ft.Text('پنل کاربری' , size=32 , font_family="b yekan+"),
                        ft.Text(
                            f'نام کاربری : {getuser["username"]} | مدت زمان اعتبار : {total_days} روز',
                            weight='w400',
                            text_align='center', font_family="b yekan+"
                        ),
                        ft.Divider(height=50 , color='transparent'),
                        ft.Column(
                            spacing=20,
                            controls=[
                                ft.Row(
                                    controls = [self.button0],
                                    alignment='center'
                                ),
                                ft.Row(
                                    controls = [self.button],
                                    alignment='center'
                                ),
                                ft.Row(
                                    controls = [self.button1],
                                    alignment='center'
                                ),
                                ft.Row(
                                    controls = [self.button2],
                                    alignment='center'
                                )

                            ]
                        )

                    ]
                )
            )
        ]


        self.page.update()
#####################################

class MailSend(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/mailsend"  , padding=60)

        self.text1 = ft.Row(controls=[ft.Text(value='ایمیل برای شما ارسال شد')],alignment=ft.MainAxisAlignment.CENTER)
        self.back_but = ft.Row(controls=[ft.ElevatedButton(text='برگشت به صفحه ورود' , on_click=lambda _ : page.go('/loginpage') , width=page.width/2)] , alignment=ft.MainAxisAlignment.CENTER)

        self.controls=[ft.SafeArea(self.text1) , ft.SafeArea(self.back_but)]


class ForgetPW(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/forgetpw"  , padding=60)

        def submit(e):
            token_url= "http://127.0.0.1:8000/accounts/forgetpassword/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "email":self.enter_mail.value

            }
            
            res = requests.post(token_url , data=request_data)
            if res.json()['answer'] == 'yes':
                page.go('/mailsend')
            elif res.json()['answer'] == 'no':
                self.alert_notif.open = True
                self.update()


        self.text1 = ft.Text(value='ایمیلی که با آن ثبت نام کردید را در کادر زیر وارد کنید تا نام کاربری و رمز عبور برایتان ارسال شود')
        self.enter_mail = ft.TextField(hint_text='ایمیل خود را وارد کنید' , border_color='white')
        self.submit_but = ft.SafeArea(ft.Row(controls=[ft.ElevatedButton(text='ثبت' , on_click=submit , width=page.width/2 )] , alignment=ft.MainAxisAlignment.CENTER , width=page.width))
        self.back_but =ft.SafeArea(ft.Row(controls=[ft.ElevatedButton(text='بازگشت' , on_click= lambda _:page.go('/loginpage' ) , width=page.width/2)] , alignment=ft.MainAxisAlignment.CENTER  , width=page.width))
        self.alert_notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('ایمیل شما وجود ندارد'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        self.controls = [ft.SafeArea(self.text1) , ft.SafeArea(self.enter_mail) , self.submit_but , self.back_but , ft.SafeArea(self.alert_notif)]


class LoginPage(ft.View):
    def __init__(self , page:ft.Page):
        super().__init__(route="/loginpage"  , padding=60)
        self.theme_mode = ft.ThemeMode.DARK
        self.window_bgcolor = "#041955"
        self.window_resizable=False
        self.rtl=True
        self.window.height = page.height
        self.window.width =page.width
        self.window_max_height = page.height
        self.window_min_height = page.height
        self.window_min_width = page.width
        self.window_max_width = page.width

        def get_token(user , password):
            token_url= "http://127.0.0.1:8000/accounts/login1/"

            headers = {
                "accept":"application/json",
                "content-type":"application/json",
            }

            request_data ={
                "username":f"{user}",
                "password":f"{password}",
            }

            res = requests.post(token_url , data=request_data)
            global my_token
            my_token = res.json()
            return my_token

        def on_press(c):



            if user_field.value =='':
                alert_user.open=True
                self.update()
                return 
            if pass_field.value =='':
                alert_pass.open=True
                self.update()
                return 

            checker=get_token(user_field.value , pass_field.value)
            if checker['token'] != '':
                page.go('/landing22')
                self.update()

                
            else:
                alert_notif.open=True
                self.update()
                
                




        onvan = ft.Text('برنامه حسابداری ققنوس' ,text_align=ft.TextAlign.CENTER , size=25 , font_family='b yekan+' )

        user_field = ft.TextField(width=page.window.width , password=False , hint_text='شناسه کاربری خود را وارد کنید' , border_radius=10 , border_color='white')
        pass_field = ft.TextField(width=page.window.width , password=True , hint_text=' رمز عبور خود را وارد کنید' , border_radius=10 , border_color='white',can_reveal_password=True)


        gen_but= ft.ElevatedButton(text='ورود به حساب کاربری' , width=page.window.width  , height=40 , on_click=on_press )

        def buywebpage(e):
            page.launch_url("http://127.0.0.1:8000/accounts/buy/")

        forget_but = ft.TextButton(text="فراموشی اطلاعات کاربری" , on_click=lambda _:page.go('/forgetpw'))
        buy_but = ft.TextButton(text="خرید اشتراک" , on_click=buywebpage)

        alert_notif = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('یوزر یا پسورد اشتباه است'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        alert_user = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('شناسه کاربری را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)

        alert_pass = ft.SnackBar(content=ft.Row(controls=[
            ft.Text('رمز عبور را وارد کنید'),
            ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
        ]) , duration=2000)


        mu_row = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[onvan] , alignment=ft.MainAxisAlignment.CENTER  )]))
        my_col =ft.SafeArea(ft.ResponsiveRow([ft.Column(controls=[ft.Row(controls=[onvan] , alignment=ft.MainAxisAlignment.CENTER  ),user_field,pass_field ,gen_but,ft.Row(controls=[forget_but,buy_but] , alignment=ft.MainAxisAlignment.CENTER) ,  alert_notif , alert_user , alert_pass] ,horizontal_alignment='center',alignment=ft.MainAxisAlignment.CENTER , height=page.window.height-70 , width=page.window.width , spacing=20)]))

        self.controls.append(my_col)




def main(page:ft.Page):

    def router(route):
        page.views.clear()

        if page.route =='/loginpage':
            loginer = LoginPage(page)
            page.views.append(loginer)

        if page.route =='/landing':
            profile = Profile(page)
            page.views.append(profile)
        
        if page.route == '/records':
            account = Accounts(page)
            page.views.append(account)
        
        if page.route == '/hesabha':
            hesabha = Hesabha(page)
            page.views.append(hesabha)
        
        if page.route == '/moein':
            moein = Moein(page)
            page.views.append(moein)
        
        if page.route =='/tafsili':
            tafsili1 = Tafsili(page)
            page.views.append(tafsili1)
        
        if page.route == '/history':
            history = History(page)
            page.views.append(history)
        
        if page.route == '/editrecord':
            editter = EditRecord(page)
            page.views.append(editter)
            
        if page.route == '/export':
            export = ExportRecords(page)
            page.views.append(export)
        
        if page.route == '/forgetpw':
            pw = ForgetPW(page)
            page.views.append(pw)
        
        if page.route =='/mailsend':
            mailsend = MailSend(page)
            page.views.append(mailsend)

        if page.route =='/landing22':
            landing22 = Profile22(page)
            page.views.append(landing22)

        if page.route =='/page1ai':
            page1ai = AI_kind_sanad(page)
            page.views.append(page1ai)

        if page.route =='/page2ai':
            page2ai = AI_name_sanad(page)
            page.views.append(page2ai)

        if page.route =='/page3ai':
            page3ai = AI_price_sanad(page)
            page.views.append(page3ai)

        if page.route =='/page4ai':
            page4ai = AI_tozihat_sanad(page)
            page.views.append(page4ai)

        if page.route =='/page5ai':
            page5ai = Ai_hesab_sanad(page)
            page.views.append(page5ai)
            
        if page.route =='/editrecord22':
            accounts22 = EditRecord22(page)
            page.views.append(accounts22)


        page.update()
    # page.on_route_change = router
    # page.go('/mailsend')

    # page.theme_mode = ft.ThemeMode.DARK
    # page.window_bgcolor = "#041955"
    page.on_route_change = router
    # page.go('/mailsend')

    page.theme_mode = ft.ThemeMode.DARK
    page.platform = ft.PagePlatform.ANDROID
    # page.window_bgcolor = "#041955"
    page.window.resizable=True
    page.rtl=True
    page.window.height = page.height
    page.window.width =page.width
    page.update()

    def get_token(user , password):
        token_url= "http://127.0.0.1:8000/accounts/login1/"

        headers = {
            "accept":"application/json",
            "content-type":"application/json",
        }

        request_data ={
            "username":f"{user}",
            "password":f"{password}",
        }

        res = requests.post(token_url , data=request_data)
        global my_token
        my_token = res.json()
        return my_token

    def on_press(c):

  

        if user_field.value =='':
            alert_user.open=True
            page.update()
            return 
        if pass_field.value =='':
            alert_pass.open=True
            page.update()
            return 

        checker=get_token(user_field.value , pass_field.value)
        if checker['token'] != '':
            page.go('/landing22')
            page.update()

            
        else:
            alert_notif.open=True
            page.update()
            
            




    onvan = ft.Text('برنامه حسابداری ققنوس' ,text_align=ft.TextAlign.CENTER , size=25 , font_family='b yekan+' )

    user_field = ft.TextField(width=page.window.width , password=False , hint_text='شناسه کاربری خود را وارد کنید' , border_radius=10 , border_color='white')
    pass_field = ft.TextField(width=page.window.width , password=True , hint_text=' رمز عبور خود را وارد کنید' , border_radius=10 ,border_color='white' ,can_reveal_password=True)


    gen_but= ft.ElevatedButton(text='ورود به حساب کاربری' , width=page.window.width  , height=40 , on_click=on_press )

    def buywebpage(e):
        page.launch_url("http://127.0.0.1:8000/accounts/buy/")

    forget_but = ft.TextButton(text="فراموشی اطلاعات کاربری" , on_click=lambda _:page.go('/forgetpw'))
    buy_but = ft.TextButton(text="خرید اشتراک" , on_click=buywebpage)

    alert_notif = ft.SnackBar(content=ft.Row(controls=[
        ft.Text('یوزر یا پسورد اشتباه است'),
        ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
    ]) , duration=2000)

    alert_user = ft.SnackBar(content=ft.Row(controls=[
        ft.Text('شناسه کاربری را وارد کنید'),
        ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
    ]) , duration=2000)

    alert_pass = ft.SnackBar(content=ft.Row(controls=[
        ft.Text('رمز عبور را وارد کنید'),
        ft.Icon(name=ft.icons.WARNING, color=ft.colors.PINK),
    ]) , duration=2000)


    mu_row = ft.SafeArea(ft.ResponsiveRow([ft.Row(controls=[onvan] , alignment=ft.MainAxisAlignment.CENTER  )]))
    my_col =ft.SafeArea(ft.ResponsiveRow([ft.Column(controls=[ft.Row(controls=[onvan] , alignment=ft.MainAxisAlignment.CENTER  ),user_field,pass_field ,gen_but,ft.Row(controls=[forget_but,buy_but] , alignment=ft.MainAxisAlignment.CENTER) ,  alert_notif , alert_user , alert_pass] ,horizontal_alignment='center',alignment=ft.MainAxisAlignment.CENTER , height=page.window.height-70 , width=page.window.width , spacing=20)]))

    page.add(my_col)

    page.update()

ft.app(target=main  , assets_dir='assets')

##########################################################


