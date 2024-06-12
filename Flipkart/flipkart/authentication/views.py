from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


from .models import Signup
# Create your views here.

def user_signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        age = request.POST.get('age')
        username = request.POST.get('username')
        password = request.POST.get('password')
        u = User(first_name=first_name, last_name=last_name, email=email, username=username)
        u.set_password(password)
        u.save()
        d = Signup(phone=phone, address=address,age=age,user=u)
        d.save()
        return HttpResponse("SignedUP")

    return HttpResponse("Make a Post Request")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        authentication = authenticate(username=username, password=password)

        if authentication:
            if authentication.is_active:
                login(request, authentication)
                user = get_object_or_404(User,pk=authentication.pk)
                s = get_object_or_404(Signup,user=user)
                data = {
                    "id":user.id,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email,
                    "phone":s.phone,
                    "address":s.address,
                    "username":user.username,
                    "password":password,
                }
                return JsonResponse(data)
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse({"error":"no user found"})

    return HttpResponse("Make Post Request")

def user_logout(request):
    logout(request)
    return HttpResponse("Logged Out")


