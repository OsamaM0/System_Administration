from  .DatabaseQuire import DatabaseQuery as  dbq 
from datetime import date

class DatabaseCommands: 

        def __init__(self) -> None:


                self.dbq = dbq("localhost","root","12345","UniversityDB")
                if not self.dbq.connection:
                        self.dbq.connect()

                self.isConnect = lambda :  self.dbq.connection.is_connected()
                self.disconnect = lambda : self.dbq.connection.disconnect()
                
        def select(self, table:str, where:str = "user_id <> -1" ):
                """
                Retrieves data from the specified table based on the given condition.

                Args:
                table (str): The name of the table to retrieve data from.
                where (str): The condition to filter data by has defulte value  .

                Returns:
                A list of dictionaries representing rows in the table that match the condition.
                """
                
                return self.dbq.select(table, where)
        
        
        def execute_query(self, query:str):
                """
                Executes a SQL query and returns a list of dictionaries representing the rows returned by the query.

                Parameters:
                -----------
                query : str
                The SQL query to execute.

                Returns:
                --------
                A list of dictionaries representing the rows returned by the query.
                """
                return self.dbq.execute_query(query)


class User(DatabaseCommands) : 
        
        def insert(self,FirstName: str, MidName: str, LastName: str, IDCard: str,
                        DOB: str, Jop: str, Address: str, Role: str, Department: str, Privileges: str,
                        UserName: str, Password: str,RegisterDate: date, Rate:float, email: str, Picture: bytes) -> None:
                
                """
                Inserts a new user into the user table.

                Parameters:
                ------------
                
                - firstname (str): The user's first name.
                - midname (str): The user's middle name.
                - lastname (str): The user's last name.
                - idcard (str): The user's ID card number.
                - dob (str): The user's date of birth (in YYYY-MM-DD format).
                - jop (str): The user's job title.
                - address (str): The user's address.
                - role (str): The user's role in the organization.
                - department (str): The user's department.
                - privileges (str): The user's access privileges.
                - username (str): The user's login username.
                - password (str): The user's login password.
                - registerdate (str): The date the user registered (in YYYY-MM-DD format).
                - rate (float): The user's rating (default 0).
                - email (str): The user's email address (default None).
                - picture (bytes): The user's profile picture (default None).

                Raises:
                -------
                mysql.connector.Error: If there is an error executing the query.
                """


                data = {
                        'FirstName': FirstName,
                        'MidName': MidName,
                        'LastName': LastName,
                        'IDCard': IDCard,
                        'DOB': DOB,
                        'Jop': Jop,
                        'Address': Address,
                        'Role': Role,
                        'Department': Department,
                        'Privileges': Privileges,
                        'UserName': UserName,
                        'Password': Password,
                        'RegisterDate': RegisterDate,
                        'Rate': Rate,
                        'email': email,
                        "Picture":Picture
                        }
                
                try: 
                        self.dbq.insert('User', data)
                except Exception as e: 
                        print("Exception When Insert Values in User Table : ", e)
                        
        
        


        def update(self,user_id: int, user_data: dict) -> None:
                
                """
                Updates a row in the User table with the specified user_id using the provided data.

                Parameters:
                ------------
                - user_data: dict
                        user data that you want to update

                Raises:
                -------
                mysql.connector.Error: If there is an error executing the query.
                """

                
                where = f"user_id = {user_id}"
                try: 
                        self.dbq.update('User',user_data, where)
                except Exception as e: 
                        print("Exception When Update Values in User Table : ", e)     
                

        def delete(self, user_id): 
                """
                Deletes a row from the 'User' table with the specified 'user_id'.
                
                Parameters:
                -----------
                user_id: int
                        The unique identifier of the user to be deleted.
                
                Returns:
                --------
                None
                """
                ides = Report().select("report", f"sender_id = {user_id} OR recever_id = {user_id} ")
                where_user = f"user_id = {user_id}"
                try: 
                        for id in ides:
                                Report().delete(id["report_id"])
                        self.dbq.delete('User', where_user)
                except Exception as e: 
                        print("Exception When Delete Values in User Table : ", e)     
        

class Report(DatabaseCommands) : 
        
        def insert(self, sender_id:int, recever_id:int, reportStartDate:str, reportEndtDate:str, state:str,Importance:str, reportHeadText:str): 
                """
                Inserts a new row into the Report table with the specified data.

                Parameters:
                ------------
                
                - sender_id (int): The ID of the sender of the report.
                - recever_id (int): The ID of the receiver of the report.
                - reportStartDate (str): The start date of the report in the format YYYY-MM-DD.
                - reportEndtDate (str): The end date of the report in the format YYYY-MM-DD.
                - state (str): The state of the report it one of this values [Accepted, Refused, Waitting]

                - reportHeadText (str): The text content of the report.

                Returns:
                - None: This function doesn't return anything.
                """

                # insert a row into the Report table
                report_data = {
                                'sender_id': sender_id,
                                'recever_id': recever_id,
                                'ReportStartDate': reportStartDate,
                                'ReportEndDate': reportEndtDate,
                                'State': state,
                                'Importance':Importance,
                                'ReportHeadText': reportHeadText,
                                }
                
                try:
                        self.dbq.insert('Report', report_data)
                except Exception as e: 
                        print("Exception When Insert Values in Report Table : ", e)
                        

        def update(self, report_id:int,sender_id:int, recever_id:int, reportStartDate:str, reportEndtDate:str, state:str,importance:str, reportHeadText:str): 
                """
                update a Excitnace row into the Report table with the specified data.

                Parameters:
                ------------
                
                - sender_id (int): The ID of the sender of the report.
                - recever_id (int): The ID of the receiver of the report.
                - reportStartDate (str): The start date of the report in the format YYYY-MM-DD.
                - reportEndtDate (str): The end date of the report in the format YYYY-MM-DD.
                - state (str): The state of the report it one of this values [Accepted, Refused, Waitting]

                - reportHeadText (str): The text content of the report.

                Returns:
                - None: This function doesn't return anything.
                """

                # update a row into the Report table
                report_data = {
                                'sender_id': sender_id,
                                'recever_id': recever_id,
                                'ReportStartDate': reportStartDate,
                                'ReportEndDate': reportEndtDate,
                                'State': state,
                                'Importance':importance,
                                'ReportHeadText': reportHeadText,
                                }
                
                try:
                        self.dbq.update('Report', report_data,f"report_id = {report_id}")
                except Exception as e: 
                        print("Exception When update Values in Report Table : ", e)    
        
        
        def delete(self, report_id): 
                """
                Deletes a row from the 'Report' table with the specified 'report_id'.
                
                Parameters:
                -----------
                report_id: int
                        The unique identifier of the report to be deleted.
                
                Returns:
                --------
                None
                """
                where_message = f"message_report_id = {report_id}"
                where_report = f"report_id = {report_id}"
                try: 
                        self.dbq.delete('Message', where_message)
                        self.dbq.delete('Report', where_report)
                except Exception as e: 
                        print("Exception When Delete Values in Report Table : ", e)   



        def getUserReports(self, user_info, recever_info, state, type):
                user_id = user_info["user_id"]               
                recever_id = recever_info["user_id"]
                if (user_info["Privileges"] == "sub_admin") and ( user_info["Department"] != recever_info["Department"])  : type = "مشتركة"
                # if you admin you can see any report the recever receved or common report between you 
                if type == "كلها":
                        where = f"(recever_id = {recever_id} OR sender_id = {recever_id} OR ((sender_id = {user_id } AND recever_id = {recever_id}) OR (sender_id = {recever_id} AND recever_id = {user_id })))  AND  State {state}"
                elif type == "مشتركة":
                        where = f"((sender_id = {user_id } AND recever_id = {recever_id}) OR (sender_id = {recever_id} AND recever_id = {user_id }))  AND  State {state}"
                elif type == "مستلمة":
                        where = f" recever_id = {recever_id}  AND  State {state}"
                elif type == "مرسلة":
                        where = f" sender_id = {recever_id }  AND  State {state}"    


                return self.select("Report", where)
        


class Message(DatabaseCommands) : 
        
        def insert(self, sender_id:int, recever_id:int, message_report_id:int, MessageDate:str, MessageHeadText:str, MessageBodyText:bytes) -> None:
                """
                Inserts a row into the Message table with the given data.
                
                Parameters:
                - sender_id (int): the ID of the user who sent the message.
                - recever_id (int): the ID of the user who received the message.
                - message_report_id (int): the ID of the report related to the message (optional).
                - MessageDate (str): the date and time when the message was sent (in the format 'YYYY-MM-DD HH:MM:SS').
                - MessageHeadText (str): the message header text.
                - MessageBodyText (bytes): the message body text (as bytes).
                """
                
                data = {
                        "sender_id": sender_id,
                        "recever_id": recever_id,
                        "message_report_id": message_report_id,
                        "MessageDate": MessageDate,
                        "MessageHeadText":MessageHeadText,
                        "MessageBodyText": MessageBodyText
                        }
                
                try:
                        self.dbq.insert("Message", data)
                except Exception as e: 
                        print("Exception When Insert Values in Message Table : ", e)
                
        
        def update(self, message_id:int ,MessageHeadText:str): 
                """
                update a Excitnace message into the Message table with the specified message text.

                Parameters:
                ------------
                - message_id (int): The ID of the message related to the report.
                - reportHeadText (str): The text content of the report.

                Returns:
                - None: This function doesn't return anything.
                """
                
                # Test update method
                data = {'MessageHeadText': MessageHeadText}
                
                try:
                        self.dbq.update("Message", data, f"message_id = {message_id}")   
                except Exception as e: 
                        print("Exception When update Values in Message Table : ", e)    
                
        
        def delete(self, message_id:int): 
                """
                Deletes a row from the 'Message' table with the specified 'message_id'.
                
                Parameters:
                -----------
                message_id: int
                        The unique identifier of the message to be deleted.
                
                Returns:
                --------
                None
                """

                self.dbq.delete("Message", f"message_id = {message_id}")


