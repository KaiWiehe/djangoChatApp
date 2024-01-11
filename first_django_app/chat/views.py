from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        print("received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )

    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages})


def loginView(request):
    redirect = request.GET.get("next")
    if request.method == "POST":
        print("login", request.POST["username"], request.POST["password"])
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect_to=request.POST.get("redirect"))
        else:
            return render(
                request,
                "chat/login.html",
                {"wrongPassword": True, "redirect": request.GET.get("next")},
            )
    return render(request, "chat/login.html", {"redirect": request.GET.get("next")})


def registerView(request):
    if request.method == "POST":
        print(
            "login",
            request.POST["username"],
            request.POST["password"],
            request.POST["mail"],
        )
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["mail"],
            password=request.POST["password"],
        )
    return render(request, "chat/register.html")
