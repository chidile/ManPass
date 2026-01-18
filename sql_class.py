from mysql import connector 


class ConnectMySQL:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "passman"
        self.password = "21222333"
        self.port = 3306
        self.database = "password_db"
        self.my_connector = None
        self.my_cursor = None

    def connect(self):
        """Establish a connection to the MySQL database."""
        self.my_connector = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password, 
            database=self.database
        )

        self.my_cursor = self.my_connector.cursor(dictionary=True, buffered=True)


    def get_data(self, sql):
        """Common function to get data from the database."""
        self.connect()
        try:
            self.my_cursor.execute(sql)
            result = self.my_cursor.fetchall()

            return result
        except Exception as E:
            print(f"Error executing query: {E}")
            return
        finally:
            if self.my_connector:
                self.my_cursor.close()
              


    def  update_data(self, sql):
        """Common function  to update data in the database"""
        self.connect()

        try:
            self.my_cursor.execute(sql)
            # commit on the connection, not the cursor
            self.my_connector.commit()
        except Exception as E:
            self.my_connector.rollback()
            print(f"Error executing update: {E}")
            return E
        finally:
            if self.my_connector:
                self.my_cursor.close()
            


    ## Function for login window
    def create_login_account(self, user_name, password):
        """Function to create a new login data ."""
        sql = f"INSERT INTO user_tb (user_name, password) VALUES ('{user_name}', '{password}')"
        result = self.update_data(sql=sql)
        return result
    
    def check_username(self, username):
        """ Check the username when creating a new account."""
        sql = f"SELECT * FROM user_tb WHERE user_name = '{username}'"
        result = self.get_data(sql=sql)
        return result
    
    ## Function for show data window
    def get_password_list(self, user_id, search_username, search_website):
        """Search and list password data."""
        sql = f"""
            SELECT * FROM password_tb 
            WHERE user_id={user_id} 
                AND user_name LIKE '%{search_username}%'
                AND website LIKE '%{search_website}%';
        """
        result = self.get_data(sql=sql)
        return result
    
    def delete_password_data(self, id):
        """Function to delete selected password data."""
        sql = f"DELETE FROM password_tb WHERE id = {id}"
        result = self.update_data(sql=sql)
        return result
    
    ## Function to generate password window
    def save_generated_password(self, user_id, user_name, website,password):
        """ Save generated password data to the database."""
        sql = f"""
            INSERT INTO password_tb (user_id, user_name, website, password)
                VALUES ({user_id}, '{user_name}', '{website}', '{password}')
        """
        result = self.update_data(sql=sql)
        return result
    
    ## Function for configuration window
    def create_config_data(self, user_id, 
                           lowercase = "abcdefghijklmnopqrstuvwxyz",
                           uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                           number = "1234567890",
                           special_character = "!@#$%^&*()-+"
                           ):
        """Function to create configuration data for the user."""
        sql = f"""
            INSERT INTO configuration_tb (user_id, lowercase, uppercase, number, special_character)
                VALUES ({user_id}, '{lowercase}', '{uppercase}', '{number}', '{special_character}')
        """
        
        result = self.update_data(sql=sql)
        return result
    
    def check_config_data(self, user_id):
        """ Check if the configuration data for the user is in the database. """
        sql = f"SELECT * FROM configuration_tb WHERE user_id={user_id}"

        result = self.get_data(sql=sql)
        return result
    

    def update_config_data(self, user_id, lowercase, uppercase, number, special_character):
        """ Update configuration data"""
        sql = f"""
            UPDATE configuration_tb
                SET lowercase='{lowercase}', uppercase='{uppercase}',
                    number='{number}', special_character='{special_character}'
                WHERE user_id={user_id}

        """
        result = self.update_data(sql=sql)
        return result


# print("SQL Class Loaded")
# print("----------------")

# print(f"checking the username function: {ConnectMySQL().check_username('test1')}")
# # print(f"Add a user account by calling the create_login_account function.", ConnectMySQL().create_login_account('test1', 'pass1234'))