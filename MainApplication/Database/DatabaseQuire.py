import mysql.connector
from typing import List, Dict, Any

class DatabaseQuery:
    """
    A class representing a database connection and query methods.

    Attributes:
    -----------
    host : str
        The hostname or IP address of the MySQL server.
    user : str
        The username to use when connecting to the MySQL server.
    password : str
        The password to use when connecting to the MySQL server.
    database : str
        The name of the database to connect to.

    Methods:
    --------
    execute_query(query:str) -> List:
        Executes a SQL query and returns a list of dictionaries representing the rows returned by the query.
    insert(table:str, data:dict) -> None:
        Inserts a row into the specified table with the given data.
    update(table:str, data:dict, where:str) -> None:
        Updates rows in the specified table with the given data that match the specified condition.
    delete(table:str, where:str) -> None:
        Deletes rows from the specified table that match the specified condition.
    """

    def __init__(self, host:str, username:str, password:str, database:str) -> None:
        """
        Initializes a new instance of the DatabaseQuery class.

        Parameters:
        -----------
        host : str
            The hostname or IP address of the MySQL server.
        user : str
            The username to use when connecting to the MySQL server.
        password : str
            The password to use when connecting to the MySQL server.
        database : str
            The name of the database to connect to.
        """

        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None


    def connect(self):
        """
        Creates a connection to the MySQL database with the specified credentials.
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )



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
        
        if not self.connection:
            self.connect()
            
        # execute the query and get the results
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        self.connection.commit()

        # close the database connection
        cursor.close()

        # return the results
        return results



    def insert(self, table:str, data:dict) -> None:
        """
        Inserts a row into the specified table with the given data.

        Parameters:
        -----------
        table : str
            The name of the table to insert the row into.
        data : dict
            A dictionary representing the data to insert into the table. The keys of the dictionary should correspond to the names of the columns in the table.
        """

        if not self.connection:
            self.connect()
            
        # build the SQL query
        columns = ', '.join(list(data.keys()))
        values = list(data.values())
        values_sym = ', '.join([ "%s" for value in values])
        query = "INSERT INTO " + table + " (" + columns + ") VALUES (" + values_sym + ")"


        # execute the query
        cursor = self.connection.cursor()
        cursor.execute(query, values)

        # commit the changes and close the database connection
        self.connection.commit()
        cursor.close()
        
        
    def update(self, table:str, set_values:dict, where_clause:str):
        """
        Updates the specified table in the database.

        Parameters:
        -----------
        table: 
                The name of the table to update.
        set_values: 
                A dictionary of column names and their new values.
        where_clause: 
                The WHERE clause to use in the UPDATE statement.
                
        Returns:
        --------
        None
        """
        if not self.connection:
            self.connect()
    
        # Construct SET clause dynamically based on non-null fields in data dictionary
        set_clause = ', '.join([f"{column} = %s" for column, value in set_values.items() if value is not None])
        if not set_clause:
            # No non-null fields found in data dictionary
            return
        
        # Construct parameters list for SQL query
        params = [value for value in set_values.values() if value is not None]
        
        # Construct and execute SQL query
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
    
    
    
    def delete(self, table: str, where: str) -> None:
        """
        Deletes rows from the specified table that match the specified condition.

        Parameters:
        -----------
        table : str
            The name of the table to delete rows from.
        where : str
            The condition that specifies which rows to delete.

        Returns:
        None.
        """
        if not self.connection:
            self.connect()
                   
        try:
            sql = f"DELETE FROM {table} WHERE {where}"
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            print(f"{cursor.rowcount} rows deleted from {table} where {where}.")
        except mysql.connector.Error as error:
            print(f"Error while deleting rows from {table}: {error}")
        finally:
            cursor.close()
    
    def select(self, table:str, where:str) -> List[Dict[str, Any]]:
        """
        Retrieves data from the specified table based on the given condition.

        Args:
            table (str): The name of the table to retrieve data from.
            where (str): The condition to filter data by.

        Returns:
            A list of dictionaries representing rows in the table that match the condition.
        """
        if not self.connection:
            self.connect()    
        cursor = self.connection.cursor()
        
        # Form the SQL query
        sql_query = f"SELECT * FROM {table} WHERE {where}"

        # Execute the query and fetch the results
        cursor.execute(sql_query)
        result = cursor.fetchall()

        # Convert the result into a list of dictionaries
        rows = [dict(zip([column[0] for column in cursor.description], row)) for row in result]

        return rows