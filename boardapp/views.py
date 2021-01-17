from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib. auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import BoardModel
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupfunc(request):
    if request.method == "POST":
        username2 = request.POST['username']
        password2 = request.POST['password']
        try:                    #try is a method to test if the error could occur.
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています'})   #here you have to '' both sides, otherwise it'd throw an error. 
        except:
            user = User.objects.create_user(username2,'', password2)
            return render(request, 'signup.html', {'some':100})
    return render(request, 'signup.html', {'some':100})

def loginfunc(request):
    if request.method == "POST":
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            #return render(request, 'signup.html') # render gets the URL, the request and throw the singup.html back. so the URL on the brower may not be /signup.
            return redirect('signup') #redirect gets the name=signup, and gets the path signup/. thats why the URL on the brower is signup/
        else:
            return redirect('login')
    return render(request, 'login.html')
@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request):    
        logout(request)
        return redirect('login')

def detailfunc(request, pk):
    object =BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc (request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()
    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
            return redirect('list')
    else: 
        post.read=post.read + 1
        post.readtext = post.readtext + '' + post2
        post.save()
        return redirect ('list')