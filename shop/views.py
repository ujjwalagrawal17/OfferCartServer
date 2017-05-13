from __future__ import print_function
from __future__ import print_function
import json
import os
import random

import jwt
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from city.models import UserCityData
from customs.sms import send_sms
from shop_otp.models import ShopOtpData
from .models import *


@csrf_exempt
def shop(request):
    response_json = {}
    if request.method == 'GET':
        try:
            for x, y in request.GET.items():
                print(x, ":", y)
            access_token = request.GET.get('access_token')
            json = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
            user_id = str(json['mobile'])
            category_id = str(request.GET.get("category_id"))

            city_id = UserCityData.objects.get(user_id=user_id).city_id

            # print "City id",city_id

            response_json["success"] = True
            response_json["message"] = 'Successful'
            response_json["shopDatas"] = []
            fields = ["name", "address"]
            for o in ShopData.objects.filter(city_id=city_id, category_id=category_id):

                temp_json = {}
                for f in fields:
                    print("f=", f)
                    temp_json[f] = str(getattr(o, str(f)))
                temp_json['shop_id'] = int(o.id)
                temp_json['category_id'] = int(o.category_id.id)
                temp_json['city_id'] = int(o.city_id.id)

                temp_json['image'] = request.scheme + '://' + request.get_host() + '/media/' + str(o.image)
                response_json["shopDatas"].append(temp_json)

        except Exception as e:
            response_json = {"success": False, "message": "shop_data not found"}

            print("e@shop=", e)

        print(str(response_json))
    else:
        response_json['success'] = False
        response_json['message'] = "Invalid request"

    return HttpResponse(str(response_json))


# Create your views here.
# noinspection PyUnreachableCode
@csrf_exempt
def create_shop(request):
    response_json = {}
    if request.method == 'POST':
        try:
            for x, y in request.GET.items():
                print(x, ":", y)
            name = str(request.POST.get('name'))
            mobile = str(request.POST.get('mobile'))
            password = str(request.POST.get('password'))
            description = str(request.POST.get('description'))
            address = str(request.POST.get('address'))
            category = str(request.POST.get('category'))
            city = str(request.POST.get('city'))

            try:
                image = request.FILES.get('image').name
                folder = 'media/' + 'shop/'
                full_filename = os.path.join(folder, image)
                print ("full name", full_filename)
                # fout = open(folder+image, 'wb+')
                print ("image=", image)
                fout = open(folder + image, 'w')
                file_content = request.FILES.get('image').read()
                # for chunk in file_content.chunks():
                fout.write(file_content)
                fout.close()
            except Exception as e:
                image = 'image'
                print (e)
            #image = request.FILES['image']

            print("Hashed password is:", make_password(password))
            print(name, mobile, type(image), image)

            otp = random.randint(100000, 999999)
            msg = 'Welcome to Discount-Store. You One Time Password is ' + str(otp)
            send_sms(mobile, msg)

            try:
                otp_list = ShopOtpData.objects.get(mobile=str(mobile))
                setattr(otp_list, 'otp', int(otp))
                setattr(otp_list, 'flag', False)
                otp_list.save()
                print('old user')
                shop_list = ShopData.objects.get(mobile=str(mobile))
                setattr(shop_list, 'name', name)
                setattr(shop_list, 'description', description)
                setattr(shop_list, 'address', address)
                setattr(shop_list, 'category', category)
                setattr(shop_list, 'city', city)
                shop_list.save()
                print('Shop Details Updated')
            except Exception as e:
                category_instance = CategoryData.objects.get(name=category)
                city_instance = CityData.objects.get(name=city)

                ShopOtpData.objects.create(mobile=str(mobile), otp=int(otp))
                ShopData.objects.create(
                    name=name,
                    mobile=str(mobile),
                    password=make_password(password),
                    description=description,
                    address=address,
                    category_id=category_instance,
                    city_id=city_instance,
                    image=image
                )
                print('User Created')
                print(e)
            response_json['success'] = True
            response_json['message'] = "Otp Sent Successfully"
            pass
        except Exception as e:
            response_json['success'] = False
            response_json['message'] = 'Unable to send otp at this time'
            print(e)
        print(str(response_json))
    else:
        response_json['success'] = False
        response_json['message'] = "Invalid request"
    return JsonResponse(response_json)


@csrf_exempt
def city_category(request):
    response_json = {}
    if request.method == 'GET':
        try:
            response_json['city_list'] = []
            for i in CityData.objects.all():
                temp_json = {}
                temp_json['id'] = int(i.id)
                temp_json['name'] = str(i.name)
                response_json['city_list'].append(temp_json)
            response_json['category_list'] = []
            for i in CategoryData.objects.all():
                temp_json = {}
                temp_json['id'] = int(i.id)
                temp_json['name'] = str(i.name)
                response_json['category_list'].append(temp_json)
            response_json['success'] = True
            response_json['message'] = "Succesful"
            # response_json['city_list'] = [(i.id, i.name) for i in CityData.objects.all()]
            # response_json['category_list'] = [(i.id, i.name) for i in CategoryData.objects.all()]
            print(response_json)
        except Exception as e:
            response_json = {'success': True, 'message': "city/category not found"}
            print(e)
    else:
        response_json['success'] = False
        response_json['message'] = "Invalid request"
    return HttpResponse(str(json.dumps(response_json)))
