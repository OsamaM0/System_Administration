import sys, os
import socket
import threading
import tqdm
from tkinter import filedialog
import numpy as np
# Get Current Data And Time
import datetime, pytz, langdetect

from PyQt5 import QtCore , QtGui , QtWidgets , uic
from MainApplication.GUI.MainGUI  import Ui_MainWindow
from MainApplication.GUI.MainGUI_Control import DashBoard, UserPage, Chat
from MainApplication.GUI.GlobalClasses import  SearchBox, Profile, EditWidgate

from Custom_Widgets.Widgets import *
from MainApplication.Database.DatabaseCommands  import User, Report, Message
import pickle
from PyQt5.QtGui import QBrush, QColor
from PyQt5 import QtChart
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout


class MainWindow(QMainWindow):
        
        
        def __init__(self, user_id ):
                QMainWindow.__init__(self)
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                try: 
                        ####################################################### ATTRIBUTES #########################################
                        
                        # Database Attributes 
                        self.user_dbc    = User()
                        self.report_dbc  = Report()
                        self.message_dbc = Message()
                        
                        # User Info
                        self.user_info = self.user_dbc.select('User',f"UserName ='{user_id }'" )[0]
                        self.user_id  = self.user_info["user_id"]
                        self.prev = self.user_info["Privileges"]

                        
                        ########################################## Privileges ##########################################
                        
                        get_dept = self.user_dbc.execute_query("SELECT DISTINCT `Department` FROM `UniversityDB`.`User` ORDER BY `Department`  COLLATE `utf8mb4_general_ci` LIMIT 0, 1000;")
                        self.dept =["كل الأقسام"]+[row["Department"] for row in get_dept]
                        if self.prev == "admin":
                                self.all_dept  = self.dept
                                self.ui.cb_chat_report_filter_type.addItems(["كلها","مشتركة","مرسلة","مستلمة"])
                                
                        else:
                                self.all_dept  = [self.user_info["Department"]]
                                if self.prev == "sub_admin":
                                        self.ui.cb_chat_report_filter_type.addItems(["كلها","مشتركة","مرسلة","مستلمة"]) 
                                
                                elif self.prev == "employee":
                                        self.ui.cb_chat_report_filter_type.addItems(["مشتركة"]) 
                                        self.ui.btn_users.setVisible(False)




                        ########################################## Message & Reports Attributes  ########################################## 
                        self.recever_id = 0
                        self.report_id = 0 
                        self.message_id = 0 
                        self.date_time = lambda: (datetime.datetime.now(tz=pytz.utc )+ datetime .timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
                        self.date = lambda: (datetime.datetime.now(tz=pytz.utc )+ datetime .timedelta(hours=2)).strftime('%Y-%m-%d')
                        self.client = None
                        self.receiver_thread = None
                        
                        # APPLY JSON STYLESHEET
                        loadJsonStyle(self, self.ui)


                        ########################################################################       
                        ########################################################################
                        ############################## BUTTON ##################################
                        ########################################################################
                        ######################################################################## 
                        

                        ########################################################################
                        # BUTTONS EXPAND AND COLLAPSE
                        ########################################################################

                        # EXPAND CENTER MENU WIDGET SIZE       
                        self.ui.btn_settings.clicked.connect(lambda:self.ui.centerMenuContainer.expandMenu())
                        self.ui.btn_info.clicked.connect(lambda:self.ui.centerMenuContainer.expandMenu())
                        self.ui.btn_help.clicked.connect(lambda:self.ui.centerMenuContainer.expandMenu())
                        # CLOSE CENTER MENU WIDGET SIZE       
                        self.ui.btn_closeCenterMenu.clicked.connect(lambda:self.ui.centerMenuContainer.collapseMenu())   
                                
                        # EXPAND RIGHT MENU WIDGET SIZE       
                        self.ui.btn_profile.clicked.connect(lambda:self.ui.rightMenuContainer.expandMenu())
                        # CLOSE RIGHT MENU WIDGET SIZE       
                        self.ui.btn_closeRightMenu.clicked.connect(lambda:self.ui.rightMenuContainer.collapseMenu())      
                        # CLOSE NOTIFICATION WIDGET SIZE       
                        self.ui.btn_closeNotification.clicked.connect(lambda:self.ui.PopupNotificationContainer.collapseMenu())   

                        ########################################################################
                        ######################### BUTTONS HOME PAGE ############################
                        ########################################################################

                        ########################################## CONTROL DASHBOARD #####################################################
                        #BUTTON TO HOME DASHBOARD
                        self.ui.btn_home.clicked.connect(lambda: DashBoard(ui= self.ui, Department = self.ui.cb_dashboard_role.currentText(), time =self.ui.cb_dashboard_time.currentText(),user_info=self.user_info ))
                        # COMBO BOX SELEC USER ROLE
                        self.ui.cb_dashboard_role.addItems(self.all_dept)
                        self.ui.cb_dashboard_role.setCurrentText(self.all_dept[0])
                        self.ui.cb_dashboard_role.currentIndexChanged.connect(lambda: DashBoard(ui= self.ui, Department = self.ui.cb_dashboard_role.currentText(), time =self.ui.cb_dashboard_time.currentText(),user_info=self.user_info ))
                        # COMBO BOX SELEC REPORT TIME
                        self.ui.cb_dashboard_time.currentIndexChanged.connect(lambda: DashBoard(ui= self.ui, Department = self.ui.cb_dashboard_role.currentText(), time =self.ui.cb_dashboard_time.currentText(),user_info=self.user_info))

                        # RADIO BUTTONS
                        report_wait_list = lambda imp: DashBoard(ui= self.ui, Department = self.ui.cb_dashboard_role.currentText(), time =self.ui.cb_dashboard_time.currentText(),user_info=self.user_info, importance= imp)
                        self.ui.rd_vi.toggled.connect(lambda:report_wait_list("='VeryHigh'"))
                        self.ui.rd_i.toggled.connect(lambda:report_wait_list("='High'"))
                        self.ui.rd_m.toggled.connect(lambda:report_wait_list("='Medium'"))
                        self.ui.rd_li.toggled.connect(lambda:report_wait_list("='Low'"))
                        self.ui.rd_ni.toggled.connect(lambda:report_wait_list("='VeryLow'"))
                        ########################################## USER PROFLIE #####################################################
                        # SET USER PROFLIE IMAGE
                        pixmap = QPixmap()
                        pixmap= EditWidgate().pixmap2Pic(pixmap,self.user_info["Picture"], 70,70, "Circule") 
                        self.ui.lbl_home_profile_pic.setPixmap(pixmap)

                        # SET USER PROFILE INFO
                        self.ui.lbl_user_info.setText(Profile(self.user_info).generate_profile_html(limit="total_data",pic_width=200, pic_hight=200))
                        self.ui.lbl_home_profile_Name.setText(f'أهلاً بيك يا {self.user_info["FirstName"]}')
                
                        ########################################################################
                        ######################## BUTTONS CHAT PAGE #############################
                        ########################################################################
                        
                        chat = Chat(ui=self.ui, user_info= self.user_info)
                        
                        ########################################## SHOW LIST #####################################################
                        # SHOW USER LIST
                        self.ui.btn_user_chat.clicked.connect(lambda: chat.showUserListChat("<>1"))
                        # SHOW USER'S REPORTS
                        self.ui.lw_user_chat.itemClicked.connect(lambda:chat.showReportListChat("<>1","مشتركة"))
                        self.ui.lw_user_chat.itemClicked.connect(lambda:self.ui.chat_report_container.expandMenu())
                        self.ui.btn_close_report_continer.clicked.connect(lambda:self.ui.chat_report_container.collapseMenu())
                        # SHOW CHAT FOR SELECTED USER'S REPORTS
                        self.ui.lw_report_chat.itemClicked.connect(lambda:chat.showMessageListChat())
                        # CHANGE REPORT STATE
                        # Accepted report
                        self.ui.btn_accept_report.clicked.connect(lambda:chat.changeReportState("Accepted"))
                        # Refused report
                        self.ui.btn_reject_report.clicked.connect(lambda:chat.changeReportState("Refused"))
                        
                        ########################################## REPORT CONTROL #####################################################                                       
                        # ADD NEW REPORT 
                        self.ui.btn_add_report.clicked.connect(lambda:chat.addReport())
                        # EDIT  REPORT
                        self.ui.btn_edit_report.clicked.connect(lambda:chat.editReport())
                        # REMOVE REPORT
                        self.ui.btn_remove_report.clicked.connect(lambda:chat.removeReport())
                        # SAVE NEW REPORTS
                        self.ui.btn_save_add_report.clicked.connect(lambda: chat.add_editReport("add"))
                        # SAVE EDITED REPORTS
                        self.ui.btn_save_edit_report.clicked.connect(lambda: chat.add_editReport("edit"))
                        # FILTER REPORTS 
                        #Report Arabic English
                        report_state_ae = {"مُكتمل":"Accepted", "مُنتظر":"Waiting","مرفوض":"Refused"}
                        filter_report = lambda: chat.showReportListChat(f'="{report_state_ae[self.ui.cb_chat_report_filter_state.currentText()]}"', self.ui.cb_chat_report_filter_type.currentText())
                        self.ui.cb_chat_report_filter_state.currentIndexChanged.connect(lambda:filter_report())
                        self.ui.cb_chat_report_filter_type.currentIndexChanged.connect(lambda:filter_report())
                        
                        ########################################## CHAT CONTROL #####################################################               
                        # BUTTON SEND MESSAGE
                        self.ui.btn_send_text.clicked.connect(lambda:chat.sendMessage())
                        # BUTTON SEND FILE
                        self.ui.btn_send_file.clicked.connect(lambda:chat.sendFile())
                        # MESSAGE OPTION 
                        self.cme = lambda event:chat.contextMenuEvent(event )
                        # FILTER USER NAMES
                        self.ui.cb_chat_user_filter.addItems(self.dept)
                        self.ui.cb_chat_user_filter.setCurrentText(self.dept[0])
                        self.ui.cb_chat_user_filter.currentIndexChanged.connect(lambda: chat.showUserListChat(f'="{self.ui.cb_chat_user_filter.currentText()}"'))
                        # MESSAGE SEARCH HINT
                        self.ui.btn_message_search.clicked.connect(lambda:chat.search_message()) 
                        # SEARCH USER NAMES
                        sb = SearchBox()
                        self.ui.le_chat_user_search.textChanged.connect(lambda:sb.search(self.ui.le_chat_user_search, self.user_info))
                        self.ui.btn_chat_user_search.clicked.connect(lambda:chat.searchUserName() )      
                        
                        
                        
                        #############################################################################################################
                        ####################################### BUTTONS PROFILES PAGE ###############################################
                        #############################################################################################################
                        user = UserPage(self.ui)
                        
                        ########################################## CONTROL USERS #####################################################               
                        # ADD USER BUTTON
                        self.ui.btn_add_user.clicked.connect(lambda:user.addUser())
                        self.ui.btn_add_user.clicked.connect(lambda:self.ui.rightMenuContainer.expandMenu())
                        # EDIT USER BUTTON                
                        self.ui.btn_edit_user.clicked.connect(lambda:user.editUser(prev="admin-edit"))
                        self.ui.btn_edit_user.clicked.connect(lambda:self.ui.rightMenuContainer.expandMenu())
                        # EDIT USER PROFILE BUTTON 
                        self.ui.btn_edit_user_profile.clicked.connect(lambda:user.editUser(prev="user-edit", user_info= self.user_info))
                        # REMOVE USER BUTTON
                        self.ui.btn_remove_user.clicked.connect(lambda:user.removeUser())
                        # SUBMIT ADD USER BUTTON
                        self.ui.btn_submit_add_profile_change.clicked.connect(lambda: user.submitUserData("add") )
                        # SUBMIT EDIT USER BUTTON
                        self.ui.btn_submit_edit_profile_change.clicked.connect(lambda: user.submitUserData("edit") )
                        # ADD USER PHOTO
                        self.ui.btn_changePhoto_add.clicked.connect(lambda: user.changePic())
                        # CHANGE USER PHOTO
                        self.ui.btn_changePhoto_edit.clicked.connect(lambda: user.changePic())
                        
                        ########################################## SHOW CARDS #####################################################
                        # FILTER USER CARDS
                        self.ui.cb_user_card_filter.addItems(self.all_dept)
                        self.ui.cb_user_card_filter.setCurrentText(self.all_dept[0])
                        self.ui.cb_user_card_filter.currentIndexChanged.connect(lambda: user.showUserProfileCard(f'="{self.ui.cb_user_card_filter.currentText()}"'))
                        # SEARCH USER CARD
                        sb = SearchBox()
                        self.ui.le_user_search.textChanged.connect(lambda:sb.search(self.ui.le_user_search, self.user_info))
                        self.ui.btn_search_user.clicked.connect(lambda:user.searchUserCard())       
                        ########################################## INIT USER PAGE #####################################################          
                        self.ui.btn_users.clicked.connect(lambda: user.showUserProfileCard(f'="{self.ui.cb_user_card_filter.currentText()}"') )

                except Exception as e:
                        print(e)
                
                
                self.show()
                # Instantiate receiver thread and connect its received signal

                try: 
                        print("Exception in Thread: ",e)
                        self.receiver_thread = chat.ReceiverThread(self.user_id, self)
                        self.receiver_thread.received.connect(chat.update_chat_box)
                        self.receiver_thread.start()
                except Exception as e:
                        print(e)
                #Update Dashboard page
                DashBoard(ui = self.ui, Department = self.ui.cb_dashboard_role.currentText(), time =self.ui.cb_dashboard_time.currentText(),user_info=self.user_info )


        # MESSAGE OPTION 
        def contextMenuEvent(self,event):
                self.cme(event)

  

  
        





                        
class MainApplicationRun :
        def __init__(self,user_id):
                window = MainWindow( user_id )

                
                


