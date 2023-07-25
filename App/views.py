from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from App.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def registration(request):
    d={'UFO':UserForm(),'PFO':ProfileForm()}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            NSUFO=UFD.save(commit=False)
            submittedPW=UFD.cleaned_data['password']
            NSUFO.set_password(submittedPW)
            NSUFO.save()
            NSPO=PFD.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()
            send_mail('Registration',
                    'Registration is Successfull',
                      'jacksparrow.7828.007@gmail.com',
                      [NSUFO.email],
                      fail_silently=True
                      )
            return HttpResponse('<center><h1><b>REGISTRATION Mail Sending is Succeffully Done</b></h1></center>')
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('<center><h1><b>Not a Active User</b></h1></center>')
        else:
            return HttpResponse('<center><h1><b>INVALID DETAILS</b></h1></center>')
    return render(request,'signin.html')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def details(request):
        username=request.session['username']
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO,'PO':PO}
        return render(request,'details.html',d)


@login_required
def change(request):
    if request.method=='POST':
        pswd=request.POST['password']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(pswd)
        UO.save()
        return HttpResponse('<center><h1><b>Password CHANGED Successfully</b></h1></center>')
    return render(request,'change.html')

def reset(request):
    if request.method=='POST':
        un=request.POST['username']
        pw=request.POST['password']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('<center><h1><b>Password RESET Done Successfully</b></h1></center>')
        else:
            return HttpResponse('<center><h1><b>PLease Enter a Valid USERNAME</b></h1></center>')
    return render(request,'reset.html')