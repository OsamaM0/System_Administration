from MainApplication.Database.DatabaseCommands  import User, Report, Message
from MainApplication.GUI.MainGUI  import Ui_MainWindow
from MainApplication.GUI.GlobalClasses import Profile , EditWidgate,SearchBox
from Custom_Widgets.Widgets import *
from PyQt5.QtCore import QThread
from PyQt5 import QtChart
import pytz, langdetect, datetime 
import numpy as np
import tkinter as tk
import time
from tkinter import simpledialog, messagebox, filedialog
from plyer import notification


class DashBoard(QMainWindow):
    def __init__(self,ui, Department, time,user_info,importance = "<>'0'"):
            
        self.ui = ui
        self.date = lambda: (datetime.datetime.now(tz=pytz.utc )+ datetime.timedelta(hours=2)).strftime('%Y-%m-%d')
        self.user_dbc = User()
        self.report_dbc = Report()
        
        if user_info["Privileges"] == "admin":
                user_id = "<>0"
        else:
                user_id = f'={user_info["user_id"]}'
        # ARABIC TO ENGLISH 
        time_dict = {"سنة":"Year","شهر":"Month", "أسبوع":"Week", "يوم":"Day"}
        
        # CIRCULE CHART
        self.circuleProgressBar(Department=Department, time=time_dict[time], user_id=user_id)
        # BAR CHART 
        self.createPercentageBarChart(Department=Department, user_id=user_id)
        
        # USER RATE
        r = f"<> '{Department}'" if Department == "كل الأقسام" else f"= '{Department}'"
        user = self.user_dbc.execute_query(f'SELECT * FROM user WHERE Department {r} AND user_id {user_id} ORDER BY rate DESC;')
        self.ui.lw_user_rating.clear()
        for user in user: EditWidgate().addListWidget(self.ui.lw_user_rating, Profile(user).generate_profile_html("star", 40,40), 1000,60,"star", Qt.AlignRight )
        
        
        
        # REPORT PROGRESS BARS
        
        # Get All Receved Reports
        get_reports = lambda send_recev : Report().execute_query(f' SELECT * FROM Report JOIN User ON Report.recever_id = user.user_id  WHERE State = "Waiting" AND Department {r} AND report.{send_recev} {user_id} AND Importance {importance} ORDER BY ReportStartDate DESC ;')
        print(user_info["FirstName"])
        # Get Send or Receved Reports according to Privileges
        reports = get_reports("recever_id") if user_info["Privileges"] == "employee" else get_reports("sender_id")
        
        self.ui.lw_task_progress_bar.clear()
        if len(reports) != 0:
                for report in reports : 
                        progress_bar = QProgressBar()
                        list_item = QListWidgetItem()

                        # Get the Percentage of number Day Left from the Report 
                        report_day_left_percentage = ((report["ReportEndDate"]- datetime.datetime.strptime( str(self.date()),'%Y-%m-%d').date() ).days + 1) / ((report["ReportEndDate"]- report["ReportStartDate"]).days + 1)
                        # Change Value of Prograss Bar
                        progress_bar.setValue(min(100,int((1-round(report_day_left_percentage,2)) * 100)))
                        
                        # Change Sytle shape of progress par 
                        IMPORTANCE_LEVELS = {"VeryHigh": "#b30000", "High": "#ea5545", "Medium": "#df8879", "Low": "#8bd3c7", "VeryLow": "#5eaaa8"}
                        progress_bar.setStyleSheet(f"""QProgressBar {{background-color: rgba(102, 102, 102,40);border-radius: 8px;text-align: center; color:rgb(177, 177, 177)}} 
                                                       QProgressBar::chunk  {{background-color:{IMPORTANCE_LEVELS[report.get("Importance","VeryLow")]};border-radius : 8px;}}""")
                        progress_bar.setToolTip(f'{str(report["ReportStartDate"])} - {str(report["ReportEndDate"])}' )
                        list_item.setSizeHint(progress_bar.sizeHint() )

                        if user_info["Privileges"] == "admin":
                                self.ui.lw_task_progress_bar.addItem(f' {report["FirstName"] }  {report["MidName"] }  :  {report["ReportHeadText"]} ')
                                self.ui.lw_task_progress_bar.addItem(f'يبدأ: {report["ReportStartDate"]}       ينتهي: {report["ReportEndDate"]}')                         
                        else:
                                user = User().execute_query(f'select FirstName, MidName  from user where user_id={report["sender_id"]}')[0]
                                self.ui.lw_task_progress_bar.addItem(f'{user["FirstName"] }  {user["MidName"] } : {report["ReportHeadText"]}')                         
                                self.ui.lw_task_progress_bar.addItem(f'بدأ: {report["ReportStartDate"]}       ينتهي: {report["ReportEndDate"]}')                         
                        
                        self.ui.lw_task_progress_bar.addItem(list_item)
                        self.ui.lw_task_progress_bar.setItemWidget(list_item, progress_bar)
                        self.ui.lw_task_progress_bar.addItem(" ")

                        
                
                
                
    def createPercentageBarChart(self, Department, user_id="<>0"):
                
                temp_layout = self.ui.bar_chart_frame
                
                x_axis_title = "Week"
                r = f"<> '{Department}'" if Department == "كل الأقسام" else f"= '{Department}'"
                print(r)
                
                # Get the Reports
                Accepted, Refused, Waiting, total = self.getReportState(time= x_axis_title, Department= r, user_id=user_id)       
                x_axis_ticks = []
                if x_axis_title == "Week": x_axis_ticks = ['Saturday', 'Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


                #function to convert from datatime type 2023-03-01 to the name of this day
                day_name = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%A')
                day_state = []
                for state in [Accepted, Refused, Waiting ]:
                        try:
                                # Apply the lambda function to the ReportStartDate column
                                day_column = [day_name(str(start_day["ReportStartDate"])) for start_day in state ]
                                # Count the frequency of each day name
                                day_counts = dict(zip(*np.unique(day_column, return_counts=True)))
                                day_state.append(day_counts)
                        except:
                                day_state.append({})
                print(day_state)
                # Create the QPercentBarSeries
                series = QtChart.QPercentBarSeries()
                
                # ONE BAR CHART 

                set0 = QtChart.QBarSet(" ")
                set1 = QtChart.QBarSet(" ")
                set2 = QtChart.QBarSet(" ")
                
                set0 = QtChart.QBarSet("مقبول")
                set1 = QtChart.QBarSet("مرفوض")
                set2 = QtChart.QBarSet("منتظر")        
                n = True
                test = []
                for tick in x_axis_ticks :
                        
                        if n:
                                set0.append(day_state[0].get(tick,0))
                                set1.append(day_state[1].get(tick,0))
                                set2.append(day_state[2].get(tick,0))
                   
                        if tick == day_name(str(self.date())[:10]): n = False
                        if not n:
                                set0.append(0)
                                set1.append(0)
                                set2.append(0)


                series.append(set0)
                series.append(set1)
                series.append(set2)
                # Create the chart view
                chart = QtChart.QChart()
                chart.addSeries(series)

                # Set the chart title
                chart.setTitle("نسبة التقارير لهذا الاسبوع")
                x_axis_ticks = ['السـبـت', 'الأحــد','الأثنين', 'الثلاثاء', 'الاربعاء', 'الخميس', 'الجمعة','']
                # Set the axis labels
                axis_x = QtChart.QBarCategoryAxis()
                axis_x.append(x_axis_ticks)
                chart.addAxis(axis_x, Qt.AlignBottom)

                axis_y = QtChart.QValueAxis()
                chart.addAxis(axis_y, Qt.AlignLeft)

                # Set the bar color
                brush = QBrush(QColor('#5EAAA8'))
                set0.setBrush(brush)                
                brush = QBrush(QColor('#F05945'))
                set1.setBrush(brush)                
                brush = QBrush(QColor('#C8C8C8'))
                set2.setBrush(brush)

                # Create the chart view
                chart_view = QtChart.QChartView(chart)


                # Create the layout
                layout = QVBoxLayout()
                layout.addWidget(chart_view)
                
                self.ui.bar_chart_frame.deleteLater()
                self.ui.bar_chart_frame = QtWidgets.QFrame(self.ui.spendingFrame_2)
                self.ui.bar_chart_frame.setMinimumSize(QtCore.QSize(0, 250))
                self.ui.bar_chart_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
                self.ui.bar_chart_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
                self.ui.bar_chart_frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.ui.bar_chart_frame.setObjectName("bar_chart_frame")
                self.ui.horizontalLayout_36.addWidget(self.ui.bar_chart_frame)
                
                # Set the layout for the frame
                self.ui.bar_chart_frame.setLayout(layout)  
                
                
                
        
    def circuleProgressBar(self, Department, time, user_id="<>0" ):
                
                r = f"<> '{Department}'" if Department == "كل الأقسام" else f"= '{Department}'"
                
                # CIRCULE PROGRESS BAR
                Accepted, Refused, Waitting, total = self.getReportState(Department = r, time = time, user_id=user_id)
                Accepted, Refused, Waitting, total = len(Accepted), len(Refused), len(Waitting), len(total)+0.0001
                
                # Main Circule Progress Bar 
                self.ui.Task_percentage_coloer.setStyleSheet(f"""
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop: {(Accepted/total)} rgb(94, 170, 168), stop: {(Accepted/total)+0.0001}  rgba(200, 200, 203,100),stop: {((Accepted+Waitting)/total)-.11}  rgba(200, 200, 203,100),stop: {((Accepted+Waitting)/total)}  rgb(240, 89, 69), stop:{min(1,total)}  rgb(247, 243, 233)  );
                        border: none;
                        border-radius: 100px;
                """)

                # Accepted Circule Progress Bar 
                self.ui.Task_Complet_percentage_coloer.setStyleSheet(f"""
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop:{(Accepted/total)} rgb(94, 170, 168), stop:{(Accepted/total)+0.1} rgb(247, 243, 233));
                        border: none;
                        border-radius: 80px;                 
                """)               
        
                 # Waitting Circule Progress Bar 
                self.ui.Task_Watting_percentage_coloer_3.setStyleSheet(f"""
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop:{(Waitting/total)} rgba(200, 200, 203,100), stop:{(Waitting/total)+0.1} rgb(247, 243, 233));
                        border: none;
                        border-radius: 80px;                
                """)      
                # Refused Circule Progress Bar 
                self.ui.Task_Refuesd_percentage_coloer_4.setStyleSheet(f"""
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,stop:{(Refused/total)} rgb(240, 89, 69), stop:{(Refused/total)+0.1} rgb(247, 243, 233));
                        border: none;
                        border-radius: 80px;
                """)      
                        #background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.4 rgb(94, 170, 168), stop:0.5 rgb(247, 243, 233));                
                
                # Change Lables
                self.ui.lbl_total_task_percntage.setText(f"{int(total)}")
                self.ui.lbl_complet_task.setText(f"{int(round((Accepted/total) * 100))} %")
                self.ui.lbl_notcomplet_task.setText(f"{int(round((Waitting/total) * 100))} %")
                self.ui.lbl_restrected_task.setText(f"{int(round((Refused/total) * 100))} %")
                
                self.ui.lbl_total_Complet_task_percntage.setText(f"{Accepted}")
                self.ui.lbl_total_watting_task_percntage.setText(f"{Waitting}")
                self.ui.lbl_total_refused_task_percntage.setText(f"{Refused}" )
                
    
    def getReportState(self, time='2000-01-01', Department = "", user_id = "<>0"):
        start_time = time
        if time == "Year"       :start_time = f"{str(self.date())[:4]}-01-01"
        if time == "Month"      :start_time = f"{str(self.date())[:7]}-01"
        if time == "Week"       :start_time = f"{datetime.datetime.strptime( str(self.date())[:10],'%Y-%m-%d')- datetime.timedelta(days=7)}"
        if time == "Day"        :start_time = f"{str(self.date())[:10]}"
        

        quire = lambda state: f"SELECT * FROM Report JOIN User ON Report.recever_id = user.user_id  WHERE report.ReportStartDate >= '{start_time}' AND user.Department  {Department} AND Report.State = '{state}' AND user.user_id {user_id};"
        Accepted = (Report().execute_query(quire('Accepted')))
        Refused  = (Report().execute_query(quire('Refused')))
        Waiting  = (Report().execute_query(quire('Waiting')))
        
        total = Accepted + Refused + Waiting
        
        return [Accepted, Refused, Waiting, total]







class UserPage(QMainWindow):
        def __init__(self,ui, parent=None):  
                super().__init__(parent)  
                self.ui = ui
                self.showUserProfileCard()
                
        def showUserProfileCard(self, department:str='="كل الأقسام"', FirstName:str="<>'0'", MidName:str="<>'0'",LastName:str="<>'0'"):
                try:
                        department = "<>'0'" if department == '="كل الأقسام"' else department       
                        self.users_data = lambda: User().select("user", where=f"Department {department} AND FirstName {FirstName} AND MidName {MidName} AND LastName {LastName}  ")   
                        # Clear Old Cards    
                        self.ui.lw_users_profiles.clear()
                        # Add Cards to the list widget
                        self.ui.lw_users_profiles.setSpacing(20) 

                        for user in self.users_data() :
                                label = Profile(user).generate_profile_html(limit="card")
                                EditWidgate().addListWidget(self.ui.lw_users_profiles, label, 300,400,"card")
                except Exception as e:
                        print(e)
        
        def addUser(self):
                try:
                        user_info_empty = self.users_data()[0]
                        EditWidgate().addData_Tree(self.ui.add_profile_info, user_info_empty, "admin-add" )
                        # SHOW USER PIC
                        self.img_date = EditWidgate().selectPic(path=":/image/image/MainApplicaton/none_profile.jpg")
                        user_photo = QPixmap()
                        user_photo = EditWidgate().pixmap2Pic(user_photo,self.img_date,width=200, hight=200, pic_type="Circule")
                        self.ui.lbl_add_profile_menu_pic.setPixmap(user_photo)    
                except:
                        messagebox.showerror("لم يتم اختيار مستخدم", f"برجاء اختيار مستخدم  ") 
           
        
        def editUser(self, prev,user_info="" ):
                try:
                        if prev == "admin-edit":
                                # GET USER DATA
                                self.user_info = self.users_data()[self.ui.lw_users_profiles.currentRow()]
                        else:
                                self.user_info = user_info
                                
                        # SHOW USER DATA
                        EditWidgate().addData_Tree(self.ui.edit_profile_info, self.user_info, prev)
                        # SHOW USER PIC
                        user_photo = QPixmap()
                        self.img_date = self.user_info["Picture"]
                        EditWidgate().pixmap2Pic(user_photo,self.img_date, pic_type="Circule")
                        self.ui.lbl_edit_profile_menu_pic.setPixmap(user_photo)
                except Exception as e:
                        messagebox.showerror("لم يتم اختيار مستخدم", f"برجاء اختيار مستخدم  ") 
                        print("error at Edit user", e)
                
                

                
        def removeUser(self):
                try:
                        self.user_info = self.users_data()[self.ui.lw_users_profiles.currentRow()]
                        if messagebox.askyesno("حذف مستخدم",f'هل تريد حذف مستخدم {self.user_info["FirstName"]} {self.user_info["MidName"]}') :
                                if messagebox.askyesno("حذف مستخدم",f'سوف يتم حذف جميع البيانات وال تقارير المتعلقة بهذا المتستخدم نهائياً ولن تستطيع ان تسترجعها مره اخري، هل تريد ان تكمل ؟ ') :
                                        user_info = self.users_data()[self.ui.lw_users_profiles.currentRow()]
                                        user_id = user_info["user_id"]
                                        User().delete(user_id)
                                        messagebox.showinfo("تم الحذف بنجاح",f'لقد تم حذف المستخدم  {self.user_info["FirstName"]} {self.user_info["MidName"]} بنجاح')
                except Exception as e:
                        messagebox.showerror("لم يتم اختيار مستخدم", f"برجاء اختيار مستخدم  ") 
                        print(e)
        
        def submitUserData(self, state:str=["add","edit"]):
                try: 
                        if state == "add":
                                # GET USER DATE
                                user_new_data =  EditWidgate().getData_tree(self.ui.add_profile_info)
                                # GET USER PIC
                                user_new_data["Picture"] = self.img_date
                                if "" in user_new_data.values(): messagebox.showerror("لم تقم إدخال جميع القيم", f"برجاء أدخل جميع القيم") 
                                else: 
                                        User().insert(**user_new_data)
                                        messagebox.showinfo("تم إضافة مستدم جديد بنجاح",f' لقد قمت بإضافة المستخدم {user_new_data["MidName"] +" " +user_new_data["FirstName"]}وتم ترقيته إلي {user_new_data["Privileges"]} ') 
                                        self.ui.rightMenuContainer.collapseMenu()
        
                        if state == "edit":
                                # GET USER DATE
                                user_new_data =  EditWidgate().getData_tree(self.ui.edit_profile_info)
                                # GET USER PIC
                                user_new_data["Picture"] = self.img_date
                                if "" in user_new_data.values(): 
                                        messagebox.showwarning("لم تقم إدخال جميع القيم", f"لم تقم بإدخال جميع القيم المطلوبة منك ") 
                                        User().update(user_id=self.user_info["user_id"],user_data= user_new_data )      
                                        messagebox.showinfo("تم تحديث بيانات المستخدم بنجاح",f'لقد قمت بتحديث بيانات المستخدم {user_new_data["MidName"] +" " + user_new_data["FirstName"]}') 
                                        self.ui.rightMenuContainer.collapseMenu()
                except Exception as e:
                        messagebox.showwarning("لم تقم إدخال جميع القيم", f"لم تقم بإدخال جميع القيم المطلوبة منك ") 
                        print(e)
                        
        def changePic(self):
                try:
                        # SELECT USER PIC
                        self.img_date = EditWidgate().selectPic()
                        user_photo = QPixmap()
                        user_photo = EditWidgate().pixmap2Pic(user_photo,self.img_date,width=2000, hight=200, pic_type="Circule")      
                        self.ui.lbl_add_profile_menu_pic.setPixmap(user_photo)    
                except Exception as e:
                        print(e)
        
        def searchUserCard(self):
                user_name = self.ui.le_user_search.text().split(" ")
                if len(user_name) == 1:
                        self.showUserProfileCard(FirstName=f"='{user_name[0]}'")
                elif len(user_name) == 2:
                        self.showUserProfileCard(FirstName=f"='{user_name[0]}'", MidName=f"='{user_name[1]}'" )
                else:
                        self.showUserProfileCard(FirstName=f"='{user_name[0]}'", MidName=f"='{user_name[1]}'",LastName= f'="{" ".join(user_name[2:])}"' )             
                        
                
                
                
                        

        
        












class Chat(QMainWindow):
        
        def __init__(self,ui, user_info, parent=None):    
                super().__init__(parent)
                self.ui = ui
                self.user_info = user_info
                self.user_id = self.user_info["user_id"]
                self.recever_id = 0
                self.report_id =  0
                dt =  lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")
                d = lambda: datetime.datetime.now().strftime('%Y-%m-%d')
                self.date_time =datetime.datetime.strptime( dt(), "%Y-%m-%d %H:%M%S")
                self.date = datetime.datetime.strptime( d(), '%Y-%m-%d') 
                self.client = None
                self.receiver_thread = None
                

        #####################################################################################
        ###################################### SHOW METHODS #################################
        #####################################################################################
        
        def showUserListChat(self, department:str='="كل الأقسام"', FirstName:str="<>'0'", MidName:str="<>'0'",LastName:str="<>'0'"):
                try:
                        # Extract ALL User Data Profiles 
                        department = "<>'0'" if department == '="كل الأقسام"' else department       
                        self.users_data = lambda: User().select("user", where=f"Department {department} AND FirstName {FirstName} AND MidName {MidName} AND LastName {LastName}  ")   
                        # Convert All users data to HTML      
                        temp_users = lambda : [Profile(user_data).generate_profile_html("user_list_chat", 50,50) for user_data in self.users_data() ]
                        # Show ALL user
                        EditWidgate().showListItm(self.ui.lw_user_chat, temp_users(),300,80,"" )
                except Exception as e:
                        print(e)
                
        def showReportListChat(self,state:str, type:str ):
                try:
                        # Get Selected User ID 
                        self.recever_info = self.users_data()[self.ui.lw_user_chat.currentRow()]
                        self.recever_id =  self.recever_info["user_id"]
                        # Get All Report for spacific User
                        
                        self.report_data = Report().getUserReports(self.user_info, self.recever_info, state, type)
                        temp_report = lambda : [ report["ReportHeadText"] for report in self.report_data]
                        # Show All Report
                        EditWidgate().showListItm(self.ui.lw_report_chat, temp_report(),300,40,"normal" )
                        # Show Selected User
                        self.ui.lbl_user_chat_info.setText(Profile(User().select("user", f"user_id = {self.recever_id}")[0]).generate_profile_html("over_view", 200,200))
                        
                        # incase choice another user clear old user chat that you was open 
                        self.ui.chat_history.clear()
                        self.ui.report_control_continer.collapseMenu()                                                    
                        self.report_id = None
                        self.report_info = None
                except Exception as e:
                        print(e)

        def showMessageListChat(self, message_text:str=""):
                try:
                        # Get Selected Report ID
                        self.report_info = self.report_data[self.ui.lw_report_chat.currentRow()]
                        self.report_id  = self.report_info ["report_id"]
                        # Get All Messages for Spacific Report 
                        self.message_data = Message().select("message", f"message_report_id = {self.report_id} AND MessageHeadText LIKE '%{message_text}%'")
                        # Show ALL Message 
                        self.ui.chat_history.clear()
                        for message in self.message_data: self.chat_box(self.ui.chat_history, message) 
                        self.ui.chat_history.scrollToBottom()
                        # Show Selected Report Head & State
                        self.ui.chat_report_name.setText(self.report_info["ReportHeadText"])
                        report_state_ae = {"Accepted":"مُكتمل", "Waiting":"مُنتظر","Refused":"مرفوض"}
                        self.ui.chat_report_state.setText(report_state_ae[self.report_info ["State"]])

                except Exception as e:
                        messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")    
                        print(e)  
        


        ###################################################################
        ###################### REPORT CONTROL FUNCTION ####################
        ###################################################################
        report_importnacey_ae = {"مهم جداً":"VeryHigh", "مهم":"High","متوسط":"Medium","أقل أهمية":"Low","غير مهم":"VeryLow"}
                                                                      
        def add_editReport(self, edit_or_add):
                try:
                        # Change Where Page Get Data From 
                        if edit_or_add == "add": 
                                report_name = self.ui.le_add_report_name.text()
                                report_importnacey = self.report_importnacey_ae[self.ui.cb_edit_report_imp.currentText()]
                                report_end_date = self.ui.de_add_report_enddate.date().toPyDate() 
                                
                        elif edit_or_add == "edit": 
                                report_name = self.ui.le_edit_report_name.text()                        
                                report_importnacey = self.report_importnacey_ae[self.ui.cb_edit_report_imp.currentText()]
                                report_end_date = self.ui.de_edit_report_enddate.date().toPyDate() 
                        
                        if self.user_id == 0: 
                                messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")                       
                        else: 
                                if report_name == "": 
                                        messagebox.showerror("لم تقم بأدخال اسم التقرير", f"برجاء إدخال اسم التقرير")   
                                else: 
                                        if report_importnacey == "": 
                                                messagebox.showerror("لم تقم بأدخال درجة أهمية التقرير", f"برجاء إدخال درحة أهمية التقرير")   
                                        else: 
                                                print(datetime.datetime.combine(report_end_date, datetime.time.min) , self.date_time)
                                                if( report_end_date == None )or (datetime.datetime.combine(report_end_date, datetime.time.min) < self.date_time): 
                                                        messagebox.showerror("التاريخ الذي أدخلته غير صالح", f"برجاء إدخال تاريخ صالح علي الأقل غداً")   
                                                else: 
                                                        
                                                        if edit_or_add == "add":
                                                                Report().insert(self.user_id, self.recever_id,self.date,report_end_date, "Waiting",report_importnacey, report_name  )
                                                                messagebox.showinfo("تم إضافة تقرير جديد بنجاح",f"لقد قمت بإضافة تقرير جديد بأسم  {report_name}   موعد تسليم التقرير سيكون  {report_end_date}") 
                                                                self.ui.report_control_continer.collapseMenu() 
                                                        elif edit_or_add == "edit":
                                                                Report().update(self.report_id, self.user_id, self.recever_id,self.date,report_end_date, "Waiting",report_importnacey, report_name  )
                                                                messagebox.showinfo("تم حفط تعديلاتك بنجاح",f"تم حفط تعديلاتك بنجاح")  
                                                                self.ui.report_control_continer.collapseMenu()                                                    
                except Exception as e:
                        print(e)

                                                                                                          
        
        def addReport(self):
                try: 
                        self.ui.le_add_report_name.clear()
                        self.ui.de_add_report_enddate.setDate(QDate.currentDate()) 
                        self.ui.cb_add_report_imp.setCurrentText("HighLevel")
                        self.ui.report_control_continer.collapseMenu() 
                        self.ui.report_control_continer.collapseMenu() 
                        self.ui.report_control_continer.expandMenu()
                        self.ui.report_control_continer.expandMenu()
                except Exception as e:
                        print(e)

                

                
        def editReport(self):        
                try:
                        if self.user_id == self.report_info["sender_id"]:
                                self.ui.le_edit_report_name.setText(self.report_info["ReportHeadText"])
                                self.ui.de_edit_report_enddate.setDate(self.report_info["ReportEndDate"]) 
                                report_importnacey_ae = {"VeryHigh":"مهم جداً", "High":"مهم","Medium":"متوسط","Low":"أقل أهمية","VeryLow":"غير مهم"}
                                self.ui.cb_edit_report_imp.setCurrentText(report_importnacey_ae[self.report_info["Importance"]] )
                                self.ui.report_control_continer.collapseMenu() 
                                self.ui.report_control_continer.collapseMenu() 
                                self.ui.report_control_continer.expandMenu()
                                self.ui.report_control_continer.expandMenu()
                                
                        else:
                                self.ui.report_control_continer.collapseMenu()
                                messagebox.showerror("لا يمكنك التعديل في هذا التقرير", f"لا يمكنك التعديل في هذا التقرير لأنك لم تنشئة") 
                except:
                        messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")    
                        self.ui.report_control_continer.collapseMenu()
                                            

        def removeReport(self):
                try: 
                        if self.user_id == self.report_info["sender_id"]:
                                if messagebox.askyesno("حذف تقرير",f'هل تريد حذف تقرير : {self.report_info["ReportHeadText"]} ان قمت بحذفة ستحذف جميع الرسائل ولم تتمكن من استرجاعها') :
                                        Report().delete(self.report_id)
                                        messagebox.showinfo("تم حذف التقرير بنجاح",f'لقد قمت بحذف التقرير {self.report_info["ReportHeadText"]} بنجاح ')
                        else:
                                messagebox.showerror("لا يمكنك التعديل في هذا التقرير", f"لا يمكنك التعديل في هذا التقرير لأنك لم تنشئة") 

                except: 
                        messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")                         
                

        def changeReportState(self, state: str = ["Accepted", "Refused"]):
                try:
                        if self.user_id == self.report_info["sender_id"]:
                                root = tk.Tk()
                                root.withdraw()

                                if self.report_id == 0 : 
                                        messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")       
                                else: 
                                        rate = simpledialog.askfloat(title=f"ادخل تقيمك لصاحب التقرير", prompt="من فضلط ادخل رقم يمثل تقيمك")
                                        if rate is not None :
                                                if  (rate <= 5) and (rate >= 0):

                                                                Report().execute_query(f"UPDATE Report SET State= '{state}'  WHERE report_id = {self.report_id}")
                                                                self.giveUserRate(rate)
                                                                root.destroy()
                                                else:
                                                        messagebox.showerror("لم تقم بإدخال اي شئ", f"من فضلك ادخل رقم من 0 إلي 5 ")  
                except :
                        messagebox.showerror("لم تقم باختيار اي تقرير", f"برجاء اختيار تقرير")        

        ###################################################################
        ########################### MESSAGES FUNCTION #####################
        ###################################################################
        # Send Message to Database
        def addMessage(self, message_head,message_body=b""):
                senderid  = int(self.user_id )
                receverId = self.recever_id
                reportId = self.report_id
                messageDate = self.date_time
                messageHeadText= message_head 
                messageData = message_body 
                 
                if not ((messageHeadText.strip() == "")  and (messageHeadText.strip() == "") ):
                        try : 
                                # Send to database
                                Message().insert(senderid,receverId,reportId,messageDate,message_head,messageData)
                                # Update Chat Box 
                                self.chat_box(ListWiegat= self.ui.chat_history, message={"sender_id":senderid,"MessageHeadText":messageHeadText,"MessageDate":messageDate})
                                self.ui.txt_space_chat.clear()
                        except Exception as e:
                                print(e)
                                
                else:
                        print("Enter Message")

        
        def sendMessage(self ):
                # Get Message
                try:
                        msg_txt = self.ui.txt_space_chat.text()
                        self.addMessage(msg_txt)
                        msg_txt = self.ui.txt_space_chat.clear()
                except:
                        print("Message Not Sent")

        

                        
        def sendFile(self):
                file_path = filedialog.askopenfilename()
                print(file_path)
                try:
                        file_body = open(file_path,'rb' )
                        file_name = os.path.basename(file_path)
                        data = file_body.read()              
                        # Send file to the database 
                        self.addMessage(file_name,data)
                except Exception as e:
                        print("please Choose File ",e)

        def download_file(self,file_path,file_name, file_btyes):
                try:
                        print(file_name)
                        print(type(file_btyes))
                        file = open(file_path +"\\"+file_name,'wb' )
                        file.write(file_btyes)
                        file.close()
                except Exception as e:
                        print(f"Download field cause: {e}")
                        
                        
        ########################## EXTRA METHODS ##################################### 
        
        def update_chat_box(self, sender_id):
                print("senderID", sender_id)
                message = Message().execute_query(f"SELECT * FROM Message WHERE sender_id = {sender_id} AND recever_id = {self.user_id } ORDER BY message_id DESC LIMIT 1")[0]

                
                if message["message_report_id"] == self.report_id:
                        self.chat_box(self.ui.chat_history,message )
                else:
                        try: 
                                sender_data = User().select('user',f"user_id={sender_id}")[0]
                                report_data = Report().select("report", f'report_id = {message["message_report_id"]}')[0]
                                head_noti = sender_data["FirstName"] + " " + sender_data["MidName"] + " : " + report_data["ReportHeadText"]
                                print(head_noti)
                                
                                # Program Notification 
                                self.ui.lbl_notification_sender.setText( head_noti )
                                self.ui.lbl_notification_msg.setText(message["MessageHeadText"])
                                self.ui.PopupNotificationContainer.expandMenu()  
                                
                                # System Notification 
                                # Create a notification
                                notification.notify(
                                title=head_noti,
                                message=message["MessageHeadText"],
                                app_name="المدير العام",
                                timeout=1  # Time in seconds the notification should stay visible
                                )
                        except Exception as e: 
                                print(e)
                 
        def chat_box(self,ListWiegat, message):
                
                # Determined message from Who
                txte = ""
                if message["sender_id"] == self.user_id:
                        txte = Qt.AlignRight
                else:
                        txte = Qt.AlignLeft
                        
                #Create a label with styled text
                message_text = message["MessageHeadText"]
                try:
                        language = langdetect.detect(message_text)
                except:
                        language = "ar"
                        print("Can't Detect the Enterd Language")
                                              
                if language == 'ar':
                        # Set the direction and alignment of the label for Arabic text
                        text = f'<html dir="rtl" ><head/><body><p style="line-height:130%; ">'
                        text += f'<span style=" font-weight: bold; bfont-size = 16px;">{message_text}</span><br>'
                else:
                        # Set the direction and alignment of the label for non-Arabic text
                        text = f'<html dir="ltr"    ><head/><body><p style="line-height:130%; ">'
                        text += f'<span style="  font-weight: bold; bfont-size = 16px; ">{message_text}</span><br>'

                text += f"<span style=\"font-size:14px; color:#808080;\">{message['MessageDate']}</span>"
                text += "</p></body></html>"
                
                EditWidgate().addListWidget(ListWiegat,text, 600, 80, "chat",txte  )

                        

        def giveUserRate(self, rate: float):
                if self.user_info["Privileges"] == "admin":
                        old_rate = self.recever_info["Rate"]
                        if old_rate == 0 : old_rate = 5
                        new_rate =  (old_rate + rate)/2
                        User().execute_query(f"UPDATE User SET Rate = {new_rate}  WHERE user_id = {self.recever_id}")
                
        def searchUserName(self):
                try:
                        user_name = self.ui.le_chat_user_search.text().split(" ")
                        if len(user_name) == 1:
                                self.showUserListChat(FirstName=f"='{user_name[0]}'")
                        elif len(user_name) == 2:
                                self.showUserListChat(FirstName=f"='{user_name[0]}'", MidName=f"='{user_name[1]}'" )
                        else:
                                self.showUserListChat(FirstName=f"='{user_name[0]}'", MidName=f"='{user_name[1]}'",LastName= f'="{" ".join(user_name[2:])}"' )   
                except Exception as e:
                        print(e)             

        
        
        
        
        def contextMenuEvent(self,event):
                if self.ui.chat_history.currentItem() != None :
                        try:
                                # Get Selected Message ID
                                self.message_info = lambda: self.message_data[self.ui.chat_history.currentRow()]  
                                self.message_id = self.message_info()["message_id"]
                                
                                # Create a menu and add some actions
                                menu = QMenu(self.ui.chat_history)
                                try: 
                                        if self.message_info()["sender_id"] == self.user_id:
                                                action_edit = menu.addAction("Edit")
                                                action_delete = menu.addAction("Delete")
                                        if len(self.message_info()["MessageBodyText"] )>1:
                                                action_download= menu.addAction("Download")

                                        # Show the menu and get the selected action
                                        global_pos = self.ui.chat_history.mapToGlobal(event.pos())
                                        menu_pos = QPoint(global_pos.x()  -350, global_pos.y()  -230)
                                        
                                        action = menu.exec_(menu_pos)
                                except Exception as e: 
                                        print(e)

                                        

                                item = self.ui.chat_history.currentItem()
                                try:
                                        if item is not None :
                                                # Handle the selected action
                                                if action == action_edit:
                                                        # Get the selected Message and edit it
                                                        new_text, ok = QInputDialog.getText(self.ui.chat_history, "Edit Item", "Enter new text:", text=self.message_info()['MessageHeadText'])
                                                        if ok:
                                                                Message().update(self.message_id, new_text)

                                                
                                                elif action == action_delete:
                                                        # Get the selected Message and delete it
                                                        Message().delete(self.message_id)
                                                        self.ui.chat_history.takeItem(self.ui.chat_history.row(item))
                                                
                                                elif action == action_download:
                                                        # Get Selected Message to Download
                                                        path = "Download\\"+self.user_info["FirstName"]+"_"+ self.user_info["MidName"]+"\\"+self.report_info["ReportHeadText"].replace(" ", "_")
                                                        os.makedirs(path, exist_ok=True)
                                                        self.download_file(path,self.message_info()["MessageHeadText"], self.message_info()["MessageBodyText"])
                                                        messagebox.showinfo("تم تنزيل الملف",f" تم تنزيل الملف {self.message_info()['MessageHeadText']} بنجاح")
                                except Exception as e:
                                        print("select message",e)
                        except Exception as e:
                                print(e)


        def search_message(self):
                self.showMessageListChat(message_text= self.ui.le_message_search.text() )
                

        class ReceiverThread(QThread):
                received  = Signal(str)

                def __init__(self,user_id, parent=None):
                        super().__init__(parent)
                        self.message_count = len(Message().select("message", "message_id > 0"))
                        self.user_id = user_id

                def run(self):
                        try:
                                
                                while True:
                                        # Detect Any Database Change
                                        current_message_count = Message().select("message", "message_id > 0")
                                        if  len(current_message_count) > self.message_count :  
                                                if  current_message_count[-1]["recever_id"]  == self.user_id :                       
                                                        # Emit received signal with the message data
                                                        self.received.emit(str(current_message_count[-1]["sender_id"]))
                                                        self.message_count = len(current_message_count)
                                        time.sleep(1)

                        except Exception as e :
                                print(e)