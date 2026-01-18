from sql_class import ConnectMySQL


mysql = ConnectMySQL()

username = "staff33"
password = "wrongpass33"

def login(username, password):
    """Function for login app."""
    if not username or not password:
        print("Username or password is empty. Please provide both.")
        
            
        ## Check username and password from database
    result = mysql.check_username(username=username)
    if result and len(result) == 1:
        if result[0]["password"] == password:
            user_id = result[0]["user_id"]

            print(f"Login successful. User ID: {user_id}")
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Username does not exist. Please try again.")





def register(username, password):
    """ Create a Login account """
    if username and password:
        ## Check if username exist on the database.
        
        result = mysql.check_username(username=username)
        if result:
            print(f"The username {username} is already in database. Please try another one.")

        else:
            print("Username is available. Creating account...")
            ## Create login account
            result = mysql.create_login_account(user_name=username, password=password)

            if result: # if there is an error
                print(f"Error creating login account: {result}")
                
            else:
                ## Successfully create login account
                print("Successfully create login account.")

                result_1 = mysql.check_username(username=username)
                user_id =result_1[0]["user_id"]
                result_2 = mysql.check_config_data(user_id=user_id)
                if not result_2:
                    result3 = mysql.create_config_data(user_id=user_id)
                    if result3:
                        print(f"Error creating default configuration data: {result3}")
                        content = f"Something is wrong: {result3}. Please try again."
                        print(content)
                
    else:
        print("Please enter both username and password.")



result = register(username, password)
print("-----")
print(result)