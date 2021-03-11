from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from account.forms import AccountUpdateForm, RegistrationForm, AccountAuthenticationForm
from account.models import *
from django.conf import settings
from question.models import Question
from django.conf import settings
# Create your views here.

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exist(request)
            if destination:
                return redirect(destination)
            return redirect('account:home')
        else:
            context['registration_form'] = form
    return render(request, 'account/register.html', context)


def login_view(request, *args, **keargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("account:home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exist(request)
                if destination:
                    return redirect(destination)
                return redirect("account:home")
        else:
            context['login_form'] = form
    return render(request, "account/login.html", context)


def get_redirect_if_exist(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def logout_view(request):
    logout(request)
    return redirect("account:home")


def home_view(request):
    return render(request, 'account/main.html')


def account_view(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get("user_id")
    account_nav = True
    context['account_nav'] = account_nav
    if user.is_authenticated:
        try:
            account = Account.objects.get(pk=user_id)
            questions = Question.objects.filter(auth=account)
        except Account.DoesNotExist:
            return HttpResponse("That user doesn't exist.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image
        context['hide_email'] = account.hide_email
        context['questions'] = questions
        
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        elif questions[0].auth != user and user.is_authenticated:
            is_self = False
        elif not questions:
            return HttpResponse("No question!!")

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

    return render(request, 'account/account.html', context)


def account_search_view(request, *args, **kwargs):
    context = {}
    account_nav = True
    context['account_nav'] = account_nav
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(
                username__icontains=search_query).distinct()
            user = request.user
            accounts = []
            for account in search_results:
                accounts.append((account, False))
            context['accounts'] = accounts
    return render(request, "account/search_results.html", context)


def edit_account_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        return redirect("account:login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("account:view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                                     initial={
                                         "id": account.pk,
                                         "email": account.email,
                                         "username": account.username,
                                         "profile_image": account.profile_image,
                                         "hide_email": account.hide_email,
                                     }
                                     )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                "id": account.pk,
                "email": account.email,
                "username": account.username,
                "profile_image": account.profile_image,
                "hide_email": account.hide_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context)
