
# users = []
# users.append(userDetails)

import bcrypt
def userExists(userData,cursor):
    '''
        @brief:
    '''
    # execute sql_query
    sql_query = f'''
                    select * from users;
                '''
    try:
        cursor.execute(sql_query)

        users = cursor.fetchall()
    except Exception as e:
        print("error: ",e)

    print("Users: ")
    print(users)

    email = userData['email']    # collect users email
    
    for user in users:
        if user[2] == email:
            print("User Found")
            # Email Found
            return {'response':True,'user':user}
    # Email not found
    return {'response':False,'user': {}}


def registerUser(userData,cursor):
    '''
        @brief:
        @param:
        @return:

    '''
    # check whether email id is registered or not
    checkUser = userExists(userData,cursor) 

    if (checkUser['response']):
        # user exists!
        # Return response dictionary
        return {'statusCode': 503, 'messgae': 'already registered'}

    else:
        # store the data
        # users.append(userData)

        sql_query = f'''
                        INSERT INTO users(name,email,password,contact) VALUES ('{userData['name']}','{userData['email']}','{userData['password']}','{userData['contact']}');       
                    '''
        try:
            cursor.execute(sql_query)
        except Exception as e:
            print("Error: ",e)

        # Return response dictionary
        return {'statusCode': 200, 'messgae': 'registered'}


def loginUser(userData,cursor):

    checkUser = userExists(userData,cursor)

    print("User: ")
    print(checkUser)

    if checkUser['response']:
            # User exists and now check form password with the stored password
            
            # form se aaya hua password == database m stored password
            
            db_password = checkUser['user'][3]
            
            print(type(db_password))
            
            if bcrypt.checkpw(userData['password'].encode(), db_password.encode()):
                    # Return response dictionary
                return {'statusCode': 200, 'messgae': 'loggedin'}
            else:
                return {'statusCode': 503, 'messgae': 'password error'}

    else:
        return {'statusCode': 503, 'messgae': 'already registered'}
