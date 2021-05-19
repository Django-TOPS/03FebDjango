from django.shortcuts import render,redirect
from .forms import signupForm,notesForm
from .models import signup
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import random
import os
from twilio.rest import Client
import requests
import json

# Create your views here.

def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            signupfrm=signupForm(request.POST)
            if signupfrm.is_valid():
                signupfrm.save()
                print("Signup Sucessfully!")
                
                #Email Send
                otp=random.randint(11111,99999)
                mail_sub='Re:Testing Mail'
                mail_message=f'Hello User, Your account has been activated after using this OTP:{otp}'
                mail_from=settings.EMAIL_HOST_USER
                #mail_to=['varajay51@gmail.com','keyurdasani@gmail.com','bharmalluvay@gmail.com']
                mail_to=[request.POST['username']]
                send_mail(mail_sub,mail_message,mail_from,mail_to)

                return redirect('notes')
            else:
                print(signupfrm.errors)
        elif request.POST.get("login")=='login':
            email=request.POST['username']
            password=request.POST['password']

            userid=signup.objects.get(username=email)
            #print("Current UserID:",userid.id)
            userdata=signup.objects.filter(username=email,password=password)
            if userdata:
                print("Login Successfully!")

                # Send SMS using Twilio
            
                """ 
                client = Client('AC6f36f9d4cd12fabb2e4adbed1c77e4b4', '85515455ae22277ea943103e7a43c4fc')

                message = client.messages.create(
                              body='Hello User, This is testimg SMS Service by Django.',
                              from_='+14243532027',
                              to='+917777998452'
                          )

                print(message.sid)
                """

                # Send SMS using Fast2sms
                # mention url
                url = "https://www.fast2sms.com/dev/bulk"
                # create a dictionary
                otp=random.randint(11111,99999)

                my_data = {
                # Your default Sender ID
                    'sender_id': 'FSTSMS', 
    
                # Put your message here!
                    'message': f'Your one time password is {otp}', 
    
                    'language': 'english',
                    'route': 'p',
    
                # You can send sms to multiple number, separated by comma.
                    'numbers': '7777998452,8460382280,9714765534,9601800090'    
                }
  
                # create a dictionary
                headers = {
                    'authorization': 'DGcl96vNtzarXWuZgkfUV1opqjs3bmiR27QOCJMY4w8AdT50EyqBaNMVki0uz8TYI26oZb5hXGDWRyLJ',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }
                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
                #load json data from source
                returned_msg = json.loads(response.text)
                
                # print the send message
                print(returned_msg['message'])

                request.session["user"]=email
                request.session['uid']=userid.id
                return redirect('notes')
                
            else:
                print("Error...Username or Password is invalid!")
    else:
        signupfrm=signupForm()
    return render(request,'index.html')


def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        mynotes=notesForm(request.POST, request.FILES)
        if mynotes.is_valid():
            mynotes.save()
            print("Your notes has been uploaded!")
        else:
            print(mynotes.errors)
    else:
        mynotes=notesForm()
    return render(request,'notes.html',{'user':user})

def userlogout(request):
    logout(request)
    return redirect('/')

def updateprofile(request):
    user=request.session.get('user')
    uid=request.session.get('uid')
    if request.method=='POST':
        signupfrm=signupForm(request.POST)
        id=signup.objects.get(id=uid)
        if signupfrm.is_valid():
            signupfrm=signupForm(request.POST,instance=id)
            signupfrm.save()
            print("Your profile has been updated!")
            return redirect('notes')
        else:
            print(signupfrm.errors)
    else:
        signupfrm=signupForm()
    return render(request,'updateprofile.html',{'user':user,'uid':signup.objects.get(id=uid)})