from ..Database import DatabaseCommands as dbc
from mysql.connector import Error
from PyQt5.QtCore import pyqtSignal, Qt, QByteArray, QBuffer, QIODevice, QDate, QResource
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtWidgets import ( QLineEdit,QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QCompleter, QTreeWidget, QTreeWidgetItem,
                             QLabel, QListWidgetItem, QListWidget, QHBoxLayout,QDateEdit,   QTreeWidget, QCalendarWidget,
                             QTreeWidgetItem, QHeaderView, QPlainTextEdit, QComboBox,   QDateEdit, QTreeWidgetItemIterator,QFileDialog, )
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import base64
import datetime
from tkinter import Tk, filedialog


             


class SearchBox(QWidget):
    user_selected = pyqtSignal(int)
        
    def search(self, LineEdit, user_info):
        text_search = LineEdit.text()
        try:
                
           # Retrieve matching rows from the database
            search = text_search.split(" ")
            if len(search) == 1:
                query = f"SELECT user_id, FirstName, MidName, LastName, Department FROM user WHERE FirstName LIKE '%{search[0]}%' OR MidName LIKE '%{search[0]}%' OR LastName LIKE '%{search[0]}%'"
            elif len(search) == 2:
                query = f"SELECT user_id, FirstName, MidName, LastName, Department  FROM user WHERE FirstName LIKE '%{search[0]}%' AND MidName LIKE '%{search[1]}%'"
            else:
                query = f"SELECT user_id, FirstName, MidName, LastName, Department  FROM user WHERE FirstName LIKE '%{search[0]}%' AND MidName LIKE '%{search[1]}%' AND LastName LIKE '%{' '.join(search[2:])}%'"

                
            data = lambda: dbc.User().execute_query(query)

            # Create a list of search results
            search_results = []
            for row in data():
                id, first_name, middle_name, last_name, department = row.values()
                if user_info["Privileges"] == "admin":
                    full_name = f"{first_name} {middle_name} {last_name}"
                    search_results.append(full_name)
                else:
                    if user_info["Department"] ==  department:
                        full_name = f"{first_name} {middle_name} {last_name}"
                        search_results.append(full_name)
                        

            # Use a QCompleter widget to show the search results
            completer = QCompleter(search_results, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            LineEdit.setCompleter(completer)

        except Exception as e:
            print("Error while connecting to MySQL", e)





class Profile:
    
    def __init__(self, profile_data):
      self.user = profile_data
      
    
    def employeeData (self, prev):
        user = self.user
        # Assume we have fetched data from the database and stored it in a dictionary
        employee_data = {
            "Name": {
                        "FirstName": user["FirstName"],
                        "MidName": user["MidName"],
                        "LastName": user["LastName"]
            },
            "Identification": {
                        "IDCard": user["IDCard"],
                        "DOB": str(user["DOB"])
            },
            "Employment": {
                        "Jop": user["Jop"],
                        "Address": user["Address"],
                        "Role": user["Role"],
                        "Department": user["Department"],
                        "Rate":user["Rate"]
            },
            "Contact": {
                        "email": user["email"]
            },
            "Account": {
                        "UserName": user["UserName"],
                        "Password": user["Password"],
                        "Privileges": user["Privileges"],
                        "RegisterDate":user["RegisterDate"]
            },
        }

        return employee_data
    


    def generate_profile_html(self, limit, pic_width:int = 160, pic_hight:int = 160):
        profile_dict = self.user
        # Retrieve values from the dictionary
        firstname = profile_dict.get('FirstName', '')
        midname = profile_dict.get('MidName', '')
        jop = profile_dict.get('Jop', '')
        department = profile_dict.get('Department', '')
        rate = int(profile_dict.get('Rate', ''))
        rate = "☆" if rate == 0 else rate * "⭐"

        idcard = profile_dict.get('IDCard', '')
        dob = profile_dict.get('DOB', '')
        address = profile_dict.get('Address', '')

        username = profile_dict.get('UserName', '')
        password = profile_dict.get('Password', '')
        registerdate = profile_dict.get('RegisterDate', '')

        email = profile_dict.get('email', '')

        # Load the pixmap image
        pixmap = QPixmap()
        pixmap = EditWidgate().pixmap2Pic(pixmap, profile_dict.get('Picture', ''),pic_hight, pic_width,pic_type="Circule")
        #pixmap.scaled(10, 10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap_data = QByteArray()
        buffer = QBuffer(pixmap_data)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        pixmap_str = str(base64.b64encode(pixmap_data.data()), 'utf-8')

        # Generate the HTML code
        css = f"""<!DOCTYPE html>
            <html dir="rtl">
            <head>
            <style>
                body {{
                    font-family:Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    color: #000000;
                    background-radius: 50px;
                }}

                .circle {{
                    overflow: hidden;
                    display: inline-block;
                }}

                .account-info {{
                    text-align: left;
                    font-size: 15px;
                    background-color: #f2f2f2;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 10px;
                    display: inline-block;
                    width: 300px;
                }}
            </style>
            </head>
           """
        html = ""
        if limit == "user_list_chat":
            html+=f"""<body>
                        <div >
                            <table style="width: 300px; height: 120px;text-align: right;">
                                <tr>
                                    <td>
                                        <div style="font-size: 20px; font-weight: bold; text-align: left;">
                                            {firstname} {midname}
                                        </dv>
                                        
                                        <div style="font-size: 16px; font-color: gray; text-align: left;">                                        
                                            {jop}
                                        </dv>
                                    </td>
                                    <td><img src="data:image/png;base64,{pixmap_str}" alt="Profile picture" class="profile-image"></td>
                                </tr>
                            </table>
                        </div>
                    """
        
        if limit == "star":
            html+=f"""<body>
                    <div style="text-align: right;">
                        <table style="width: 300px; height: 50px;text-align: right;">
                            <tr>
                                <td style="width: 250px; padding-right: 40px;"><h1>{rate}</h1></td>
                                <td style="width: 200px; padding-right: 20px;"><h1>{firstname} {midname}</h1></td>
                                <td style="width: 50px; padding-right: 50px;"><img src="data:image/png;base64,{pixmap_str}" alt="Profile picture" class="profile-image" width="50px"></td>
                            </tr>
                        </table>
                    </div>
                    """
        if limit in ["card", "over_view","total_data"]: 
            html=f"""<body>
                    <div class="circle">
                        <img src="data:image/png;base64,{pixmap_str}" alt="Profile picture">
                    </div>
                    <div style="font-size: 25px; font-weight: bold;">
                        {firstname} {midname}
                    </div>
                    <div style="font-size: 15px; font-weight: bold;">
                        {jop}
                    </div>
                    <div style="font-size: 14px;">
                        {department}
                    </div>
                    <div style="font-size: 16px;">
                        {rate}
                    </div>
                    """
                    
        if limit in ["card","total_data"]:
            html += f"""
                    <div class="account-info">
                        <div style="font-weight: bold;">المعلومات الشخصية</div>
                        <div>الرقم القومي: {idcard}</div>
                        <div>تاريخ الميلاد : {dob}</div>
                        <div>العنوان: {address}</div>
                    </div>
                    <div class="account-info">
                        <div style="font-weight: bold;">معلومات التواصل</div>
                        <div> الإيميل: {email}</div>
                        <div></div>
                    </div>
                    """
    
        if limit == "total_data":
            html += f"""
                    <div class="account-info">
                        <div style="font-weight: bold;">معلومات الحساب</div>
                        <div> اسم المستخدم: {username}</div>
                        <div> رمز المرور: {password}</div>
                        <div> تاريخ التسجيل: {registerdate}</div>
                    </div>
                    """ 
        
        html+=f"""
            </body>
            </html>"""
        
        user_info = css+html
        return user_info


         
class EditWidgate:
    parent_aren = {"Name":"الأسـم","Identification":"المعلومات الشخصية","Employment":"الوظيفة","Account":"الحساب","Contact":"التواصل"}
    chiled_aren = {"FirstName": "الأول", "MidName": "الأوسط", "LastName": "العائلة", "IDCard": "بطاقة الهوية", "DOB": "ت الميلاد", "Jop": "الوظيفة", "Address": "العنوان", "Role": "الدور", "Department": "القسم", "Rate": "التقييم", "email": "البريد الإلكتروني", "UserName": "اسم مستخدم", "Password": "كلمة السر", "Privileges": "الامتيازات", "RegisterDate": "ت التسجيل"}
    chiled_enar= {'الأول': 'FirstName', 'الأوسط': 'MidName', 'العائلة': 'LastName', 'بطاقة الهوية': 'IDCard', 'ت الميلاد': 'DOB', 'الوظيفة': 'Jop', 'العنوان': 'Address', 'الدور': 'Role', 'القسم': 'Department', 'التقييم': 'Rate', 'البريد الإلكتروني': 'email', 'اسم مستخدم': 'UserName', 'كلمة السر': 'Password', 'الامتيازات': 'Privileges', 'ت التسجيل': 'RegisterDate'}

    
    def addData_Tree(self, tree: QTreeWidget, profile_data:dict, prev:str=["user-edit,user-add,admin-edit,admin-add"]):
        # Clear any prevouse tree
        tree.clear()
        # Create the tree widget
        tree.setColumnCount(2)
        employee_data = Profile(profile_data).employeeData(prev[:5])
        tree.setHeaderHidden(True)
       
        # Iterate on top-level item for each category
        for iteam in ["Name", "Identification","Employment","Account", "Contact" ]:
            name_item = QTreeWidgetItem(tree, [self.parent_aren[iteam]])
            
            # Add child items for each attribute in the category
            for attribute, value in employee_data[iteam].items():
                
                # ADD NEW USER (-add)
                if prev[-3:] == "add": 
                    if attribute in ["DOB","RegisterDate"]: value =  datetime.date.today()
                    elif  attribute == "Rate": value = 0
                    elif  attribute == "RegisterDate" : value =  datetime.date.today()
                    else:  value = ""
                
                # EDIT USER (edit)
                else: 
                    if    attribute in ["DOB"]: value =  datetime.datetime.strptime(value, '%Y-%m-%d').date()


                
                child = QTreeWidgetItem(name_item, [self.chiled_aren[attribute], str(value)])
                print(attribute)
                # ADMIN WILL ADD-EDIT (admin)
                if prev[:5] == "admin":
                        
                    if attribute in ["RegisterDate", "Rate"]:
                        label = QLabel(str(value))
                        tree.setItemWidget(child, 1, label)

                    elif attribute == "DOB":
                        # Add a QDateEdit widget for the value column
                        date_edit = QDateEdit(value)
                        date_edit.setDisplayFormat("dd-MM-yyyy")
                        tree.setItemWidget(child, 1, date_edit)

                    elif attribute == "Privileges":
                        privileges = QComboBox()
                        privileges.addItems(["admin", "sub_admin", "employee"])
                        privileges.setCurrentText(value)
                        tree.setItemWidget(child, 1, privileges)

                    elif attribute == "Department":
                        dept = QComboBox()
                        dept.addItems(["أخصائى حاسبات آلية", "أمن", "اخصائي رياضي","ادارة عامة","الارشيف",
                                            "الشئون الماليه","المخازن","المعامل","توثيق","حاسبات الكترونية",
                                            "خدمات معاونة","رعاية الشباب","شئون إداريه","شئون افراد","شئون الخريجين",
                                            "شئون العاملين","شئون تعليم","شئون طلاب","شئون مالية"])
                        
                        dept.setCurrentText(value)
                        tree.setItemWidget(child, 1, dept)

                    else:
                        line_edit = QLineEdit(value)
                        line_edit.setStyleSheet("border:none; border-bottom: 2px solid rgba(105,118,132,50); padding-bottom:7px;font-size = 13px;")
                        tree.setItemWidget(child, 1, line_edit)
                        
                # USER WILL EDIT  (user)
                else:
                    if attribute in ["UserName","Password"]:
                        line_edit = QLineEdit(value)
                        tree.setItemWidget(child, 1, line_edit)
                        
                    else:
                        label = QLabel(str(value))
                        label.setStyleSheet("border:none; border-bottom: 2px solid rgba(105,118,132,50); padding-bottom:7px;font-size = 13px;")
                        tree.setItemWidget(child, 1, label)
                

 
# 19457


    
    def getData_tree(self, tree: QTreeWidget) -> dict:
        data = {}
        for category_index in range(tree.topLevelItemCount()):
            category_item = tree.topLevelItem(category_index)
            for attribute_index in range(category_item.childCount()):
                attribute_item = category_item.child(attribute_index)
                attribute_name = attribute_item.text(0)
                value_widget = tree.itemWidget(attribute_item, 1)
                if isinstance(value_widget, QDateEdit):
                    value = value_widget.date().toString("yyyy-MM-dd")
                elif isinstance(value_widget, QComboBox):
                    value = value_widget.currentText()
                else:
                    value = value_widget.text().strip()
                data[self.chiled_enar[attribute_name]] = value
        return data



        
    

    
    def addListWidget(self, list_widget: QListWidget, text: str, item_width: int, item_height: int, use_case: str, text_alignment=Qt.AlignLeft):
        """
        Adds a QListWidgetItem to the given QListWidget based on the given useage.
        If useage is 'normal', the item text will be added as is.
        If useage is 'star' or 'card', the item text will be wrapped in a QLabel with a specific stylesheet.
        If useage is 'chat', the item text will be wrapped in a QLabel with a specific stylesheet and alignment.
        Args:
            listWidget (QListWidget): The QListWidget to add the item to.
            text (str): The text to display in the item.
            item_width (int): The fixed width of the item.
            item_height (int): The fixed height of the item.
            useage (str): The useage of the item. Can be 'normal', 'star', 'card', or 'chat'.
            text_alignment (Qt.AlignmentFlag, optional): The text alignment of the item. Defaults to Qt.AlignLeft.
        """

        if use_case == "normal":
            list_widget.addItem(text)
            
        else:
            # Create a label to display the text
            label = QLabel(" "+text)
            label.setFixedSize(item_width, item_height)
            label.setWordWrap(True)
            label.setContentsMargins(10, 0, 10, 0)
            
            # Apply style sheet based on use case
            if use_case in ["star", "card"]:
                label.setAlignment(Qt.AlignLeft)

                
            elif use_case == "chat":
                bg_color  = "#FFFFFF" if text_alignment == Qt.AlignLeft else "#5EAAA8"
                text_color= "#000000" if text_alignment == Qt.AlignLeft else "#FFFFFF"
                label.setStyleSheet(f"background-color: {bg_color}; color: {text_color}; padding: 15px; border-radius: 10px; font-size: 17px;white-space: pre-wrap;")

                
            
            # Add the label to a widget container
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(label, 0, text_alignment)

            # Create a list widget item and set its properties
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())

            # Add the item to the list widget
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)


    def showListItm(self, list_widget: QListWidget, text: list, item_width: int, item_height: int, use_case: str, text_alignment=Qt.AlignLeft):
                list_widget.clear()
                for item in text:
                        EditWidgate().addListWidget(list_widget, item,item_width,item_height,use_case,text_alignment )
        
        
    def pixmap2Pic(self, pixmap: QPixmap, Picture: bytearray, hight:int=160, width:int=160, pic_type:str=["Circule","Squaire"]): 
        
        # Create a new pixmap with the desired dimensions
        pixmap = pixmap
        pixmap.loadFromData(Picture)
        pixmap =  pixmap.scaled(width, hight,aspectRatioMode=Qt.KeepAspectRatio)
        if pic_type == "Squaire":
            return pixmap
        rounded_pixmap = QPixmap(width, hight)
        rounded_pixmap = rounded_pixmap.scaled(hight, width,)

        # Create a QPainter object to draw on the new pixmap
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create a brush to fill the new pixmap with white color
        brush = QBrush(QColor(Qt.white))
        painter.fillRect(0, 0, width, hight, brush)

        # Create a circular path to clip the image
        path = QPainterPath()
        path.addEllipse(0, 0, width, hight)
        painter.setClipPath(path)

        # Draw the original pixmap image on the new pixmap
        painter.drawPixmap(0, 0, pixmap)

        # Clean up the painter object
        painter.end()

        return rounded_pixmap

    def selectPic(self, path=None):
        if path == None:
            # Open a Tkinter file dialog to select an image file
            root = Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                # Open the selected image file and convert it to a binary string
                with open(file_path, "rb") as f:
                    image_data = f.read()
                f.close()

            else: 
                image_data = QResource(path).data()
        else: 
            image_data = QResource(path).data()

        return image_data
    

    
    