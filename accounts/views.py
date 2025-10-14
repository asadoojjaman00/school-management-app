from django.shortcuts import render



# register view function : 
def register_view(request):
    return render(request, 'register.html')


# login view function : 
def login_view(request):
    return render(request, 'login.html')

