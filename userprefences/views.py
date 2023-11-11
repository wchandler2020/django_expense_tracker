from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import Userprefences
from django.contrib import messages

# Create your views here.
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currency.json')
    userprefences = None
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'key':k, 'value': v})
            
    exists = Userprefences.objects.filter(user=request.user).exists()
    if exists:
        userprefences = Userprefences.objects.get(user=request.user)
    if request.method == 'GET':        
        return render(request, 'preferences/index.html', context = {
            'currencies': currency_data,
            'userprefences': userprefences
        })
    else:
        currency = request.POST['currency']
        if exists:
            userprefences.currency = currency
            userprefences.save()
        else: 
            Userprefences.objects.create(user=request.user, currency = currency)
        messages.success(request, 'Currency Preference Updated')
        return render(request, 'preferences/index.html', context = {
            'currencies': currency_data,
            'userprefences': userprefences
        })
        

