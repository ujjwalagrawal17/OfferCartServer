import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from city.models import CityData
from city.models import CityFcmData
from shop.models import ShopData


# Create your views here.
@login_required(login_url='/admin/')
def send_notification(request):
    if request.method == 'GET':
        cities = CityData.objects.values('id', 'name')
        print("yes", cities)
        return render(request, "notification.html", {"cities_data": cities})
    else:

        for x, y in request.POST.items():
            print "key,value", x, ":", y
        message = str(request.POST.get('message'))
        city = request.POST['city']
        shop_id = request.POST.get('shops')
        cities = CityData.objects.values('id', 'name')
        shop_name = str(ShopData.objects.get(id=shop_id).name)
        print shop_name
        for o in CityFcmData.objects.filter(city_id=city):
            notify_users(o.fcm, message, shop_id, shop_name)
        return render(request, "notification.html", {"cities_data": cities})


@csrf_exempt
def notify_users(fcm, body, id, name, title="Discount Store"):
    json = {
        "to": str(fcm),
        # "notification" : {
        #   "body" : str(body)+"",
        #   "title" : str(title),
        #   "sound": "default",
        #   "click_action":"com.codenicely.dicountstore.home.HomePage"
        # },
        "data": {
            "message": str(body),
            "shop_id": str(id),
            "shop_name": str(name),
        }
    }
    print json
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": "key=AAAAf59-gMY:APA91bH47UFR2GGd7RUPbKLYahb6K2IVYRyzzgZpUOYZ9cQak4Zr_6Id4gUdByR48AhLpygmcTqxqzahzCylM_WipAVxlOsEva_drEXE8YJO6yhlLDD0tWPoZyLVJENXlT_ubW1_WRy8LVcwKuC7mNPNU0984hNmxQ"

    }
    # print json
    r = requests.post(url, headers=headers, json=json)
    for o in r:
        print o


@csrf_exempt
def send_shops(request):
    response_json = {}
    if (request.method == 'POST'):
        city_id = request.POST.get('city_id')
        shop_names = ShopData.objects.filter(city_name__id=city_id)
        response_json["shop_data"] = []
        if (shop_names.count() == 0):
            temp_json = {}
            temp_json["shop_id"] = str("")
            temp_json["shop_name"] = "No shop available"
            response_json["shop_data"].append(temp_json)
            print"debugged"
        for o in shop_names:
            print"debugged"
            temp_json = {}
            print o.name
            temp_json["shop_id"] = o.id
            temp_json["shop_name"] = str(o.name)
            response_json["shop_data"].append(temp_json)
        print ("shop_names", shop_names)
        print ("city_id", city_id)
        print str(response_json)
        return JsonResponse(response_json)
