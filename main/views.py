from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .utils import registerUser,loginUser
from django.contrib.sessions.backends.db import SessionStore        # for session storage

import psycopg2
import requests
import bcrypt
import json

s = SessionStore()

# connection the database
try:
    connection = psycopg2.connect(
        host = "127.0.0.1",
        port = "5432",
        database = "memestore",
        user = "postgres",
        password = "root"
    )
    print("Database is connected ")
except Exception as e:
    print("Error",e)
    print("Database connection failed")
connection.autocommit = True
cursor = connection.cursor()

# middleware

def checkSession():
    try:
        email = s['email']
        return True
    except Exception as e:
        print("Error: ",e)
        return False

# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome to meme application!</h1>")

def register(request):

    sessionExists = checkSession()

    if sessionExists == False:

        if request.method =='POST':
            form_data = json.loads(request.body.decode("utf-8"))

            # print(request.POST)
            #collect all data from client
            name = form_data.get("name")
            email = form_data.get("email")
            contact = form_data.get("contact")
            password = form_data.get("password")
            

            print(f'Name:{name}')
            print(f'Contact:{contact}')
            print(f'Email:{email}')
            print(f'Password:{password}')

            password = password.encode()

            # hashed aur password
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            
            hashed = hashed.decode('utf-8')

            # create User Dictionary
            userData = {
                # 'id' : user_id,
                'name' : name,
                'contact' : contact,
                'email' : email,
                'password' : hashed,
            }
            # Register user

            response = registerUser(userData,cursor)

            # print user data 
            print("Response:")
            print(response)
        

            if response['statusCode'] == 200:
                # session store
                s['email'] = userData['email']
                s['password'] = userData['password']

                print('session : ')
                print(s)

                return JsonResponse({'status_code':200,'message':'sucess'})

                # return render(request,'register.html',{'message':'Sucessfully recieved'})
                # return redirect('/memes/')
            else:
                return JsonResponse({'status_code':503,'message':'Already registered'})
                # return render(request,'register.html',{'message':'Already Registered'})
        else:
            return render(request,'register.html')
    else:
        return redirect('/memes/')

def login(request):

    sessionExists = checkSession()

    if sessionExists == False:

        if request.method =='POST':
            form_data = json.loads(request.body.decode("utf-8"))

            # print(request.POST)
            #collect all data from client
            password = form_data.get("password")
            email = form_data.get("email")

            print('Email: ')
            print(email)

            print('Password: ')
            print(password)

            userData = {
                'email' : email,
                'password' : password
            }

            response = loginUser(userData,cursor)

            if response['statusCode'] == 200:
                # session store
                s['email'] = userData['email']
                s['password'] = userData['password']

                print('session : ')
                print(s)
                # return render(request,'login.html',{'message':'Sucessfully logged In'})
                # return redirect('/memes/')
                return JsonResponse({'status_code':200,'message':'success'})

            elif response['statusCode'] == 503 and response['message'] == 'passworderror':
                return render(request,'login.html',{'message':'password not matched'})

            else:
                # return render(request,'login.html',{'message':'Not registered'})
                return JsonResponse({'status_code':503,'message':'Authentication_error'})



        else:
            return render(request,'login.html')
    else:
        return redirect('/memes/')

def logout(request):
    try:
        s.clear()
        return redirect("/login/")
    except:
        return redirect("/memes/")

def getmemes(request):
    sessionExists = checkSession()

    # URL:https://api.imgflip.com/get_memes

    r = requests.get('https://api.imgflip.com/get_memes')

    meme_data = r.json()

    if sessionExists == False:
        return redirect("/login/")
    else:
        print(meme_data['data']['memes'])

        context = {
            'memes_metadata' : r.json()['data']['memes']
        }

        return render(request,'memes.html',context=context) 

def editmeme(request):

    sessionStatus = checkSession()

    if sessionStatus:
        # Display update page
        template_id = request.GET['id']

        context = {
            'meme_id' : template_id
        }
        return render(request,'editmeme.html',context=context)

    else:
        return redirect("/login/") 

def memedetails(request):
    sessionStatus = checkSession()

    if sessionStatus:

        if request.method == 'POST':
            template_id = request.POST['id']
            text0 = request.POST['text1']
            text1 = request.POST['text2']

            # POST request Meme API

            payload = {
                'template_id' : template_id,
                'username' : 'Adityachaudhary2',
                'password' : 'qweasd01!@',
                'text0' : text0,
                'text1' : text1,
            }
            response = requests.request('POST','https://api.imgflip.com/caption_image',params=payload).json()
            print("Response : ")
            print(response)

            html_str = f'''
                         <h1>Response</h1>
                         <img style="height: 200px; width: 200px" src="{response['data']['url']}" alt="meme">
                         <a href="{response['data']['url']}">View Image</a>
                        '''
            
            return HttpResponse(html_str)
    else:
        return redirect("/login/")