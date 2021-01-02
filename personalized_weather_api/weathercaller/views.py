from django.http import JsonResponse
from weathercaller.models import Day
import json
import requests
from datetime import date

def retrieveWeather(req):
    reqtoken = req.GET.get('token')
    if not reqtoken:
        return JsonResponse({'Error':'Token not provided'},status=400)
    data = requests.get("http://api.weatherapi.com/v1/current.json?key=8b1a4a9509a64577a89155041210101&q={}".format(req.GET.get('ip'))) #Use req.META['REMOTE_ADDR']
    data = json.loads(data.text) 
    weather = data['current']
    if Day.objects.filter(token=reqtoken,date=str(date.today())):
        CurrentDay = Day.objects.get(token=reqtoken,date=date.today())
        CurrentDay.data = json.dumps(weather)
        CurrentDay.save()
    else:
        CurrentDay = Day(token=reqtoken,date=date.today(),data=json.dumps(weather))
        CurrentDay.save()
    return JsonResponse({"date":str(date.today()),"weather":weather})

def retrieveData(req):
    reqtoken = req.GET.get('token')
    if not reqtoken:
        return JsonResponse({'Error':'Token not provided'},status=400)
    ListOfDays = Day.objects.filter(token=reqtoken)
    if not ListOfDays:
        return JsonResponse({'Error':'Token not found'},status=400)
    data = dict()
    for i in ListOfDays:
        data.update({str(i.date):json.loads(i.data)}) 
    return JsonResponse(data)
