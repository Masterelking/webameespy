from django.shortcuts import render

def apropos(request):
    return render(request, 'apropos/apropos.html')

