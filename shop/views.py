from __future__ import print_function
from __future__ import print_function

import os
import random

import jwt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from city.models import UserCityData
from customs.sms import send_sms
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

# From here the methods are for Shop Admin module

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
                print("full name", full_filename)
                # fout = open(folder+image, 'wb+')
                print("image=", image)
                fout = open(folder + image, 'w')
                file_content = request.FILES.get('image').read()
                # for chunk in file_content.chunks():
                fout.write(file_content)
                fout.close()
            except Exception as e:
                image = 'image'
                print(e)
            image = request.FILES['image']

            # print("Hashed password is:", make_password(password))
            print(name, mobile, type(image), image)

            try:
                category_instance = CategoryData.objects.get(name=category)
                city_instance = CityData.objects.get(name=city)

                if ShopData.objects.filter(mobile=str(mobile)).count() > 0:
                    print("Shop already exist")
                    response_json['success'] = False
                    response_json['message'] = "Shop already exists"
                else:
                    print("New shop")

                    shop_instance = ShopData.objects.create(
                        name=name,
                        mobile=str(mobile),
                        password=str(password),
                        description=description,
                        address=address,
                        category_id=category_instance,
                        city_id=city_instance,
                        image=image
                    )
                    print('User Created')

                    otp = random.randint(1000, 9999)
                    msg = 'Welcome to Discount Store. You One Time Password is ' + str(otp)
                    send_sms(mobile, msg)

                    try:
                        otp_list = ShopOtpData.objects.get(shop_id=shop_instance)

                        if otp_list.count() == 1:
                            setattr(otp_list, 'otp', int(otp))
                            setattr(otp_list, 'flag', False)
                            otp_list.save()
                            print('old user')
                        else:
                            ShopOtpData.objects.create(shop_id=shop_instance, otp=int(otp))

                    except Exception as e:
                        ShopOtpData.objects.create(shop_id=shop_instance, otp=int(otp))
                        print("Otp data does not exist, Creating it")

                    response_json['success'] = True
                    response_json['message'] = "Otp Sent Successfully"

            except Exception as e:
                response_json['success'] = False
                response_json['message'] = 'Unable to send otp at this time'
                print(e)
            print(str(response_json))
        except Exception as e:
            response_json['success'] = False
            response_json['message'] = 'Something went wrong'
            print(e)
    else:
        response_json['success'] = False
        response_json['message'] = "Invalid request"
    return JsonResponse(response_json)


@csrf_exempt
def verify_shop_otp(request):
    response = {}
    if request.method == 'POST':
        try:

            mobile = str(request.POST.get('mobile'))
            otp = str(request.POST.get('otp'))

            print("Mobile" + str(mobile))
            print("otp:" + str(otp))
            shop_instance = ShopData.objects.get(mobile=str(mobile))
            shop_otp_instance = ShopOtpData.objects.get(shop_id=shop_instance)

            access_token = jwt.encode({'mobile': str(mobile)}, '810810', algorithm='HS256')

            print("Required" + str(shop_otp_instance.otp))

            if int(shop_otp_instance.otp) == int(otp):
                response['success'] = True
                response['message'] = "Otp verified successfully"
                response['shop_access_token'] = str(access_token)

            else:
                response['success'] = False
                response['message'] = "Otp doesn't match"
        except Exception as e:
            response['success'] = False
            response['message'] = "Something went wrong " + str(e)
            print(e)
    else:
        response['success'] = False
        response['message'] = "Invalid request"
    print(response)
    return JsonResponse(response)


@csrf_exempt
def verify_shop_login(request):
    response = {}
    if request.method == 'POST':
        try:
            mobile = str(request.POST.get('mobile'))
            password = str(request.POST.get('password'))

            access_token = jwt.encode({'mobile': str(mobile)}, '810810', algorithm='HS256')

            if ShopData.objects.filter(mobile=mobile, password=password).count() == 1:
                response['success'] = True
                response['message'] = "Successful"
                response['shop_access_token'] = str(access_token)
            else:
                response['success'] = False
                response['message'] = "Invalid mobile or password"

        except Exception as e:
            response['success'] = False
            response['message'] = "Something went wrong " + str(e)
    else:
        response['success'] = False
        response['message'] = "Invalid request type"
    # response_data = json.dumps(response)
    print(response)
    return JsonResponse(response)


import json


@csrf_exempt
def my_shop_profile(request):
    response = {}
    if request.method == 'GET':
        try:
            shop_access_token = str(request.GET.get('shop_access_token'))
            json = jwt.decode(str(shop_access_token), '810810', algorithms=['HS256'])
            shop_mobile = str(json['mobile'])
            shop_instance = ShopData.objects.get(mobile=shop_mobile)

            response['name'] = shop_instance.name
            response['mobile'] = shop_instance.mobile
            response['description'] = shop_instance.description
            response['address'] = shop_instance.address
            response['category'] = str(shop_instance.category_id)
            response['city'] = str(shop_instance.city_id)
            response['image'] = request.scheme + '://' + request.get_host() + '/media/shop/' + str(shop_instance.image)
            response['success'] = True
            response['message'] = "Successful"

        except Exception as e:
            response['success'] = False
            response['message'] = "Something went wrong" + str(e)
            print(e)
    else:
        response['success'] = False
        response['message'] = "Illegal request"
    # response_json=json.dumps(response)
    print(response)
    return JsonResponse(response)


@csrf_exempt
def edit_shop_profile(request):
    response = {}
    if request.method == 'POST':
        try:
            for x, y in request.POST.items():
                print(x, ":", y)

            shop_access_token = str(request.POST.get('shop_access_token'))
            json = jwt.decode(str(shop_access_token), '810810', algorithms=['HS256'])
            shop_mobile = str(json['mobile'])
            print("Shop mobile:" + str(shop_mobile))
            name = str(request.POST.get('name'))
            description = str(request.POST.get('description'))
            address = str(request.POST.get('address'))
            category = str(request.POST.get('category'))
            city = str(request.POST.get('city'))

            try:
                image = request.FILES.get('image').name
                folder = 'media/' + 'shop/'
                full_filename = os.path.join(folder, image)
                print("full name", full_filename)
                # fout = open(folder+image, 'wb+')
                print("image=", image)
                fout = open(folder + image, 'w')
                file_content = request.FILES.get('image').read()
                # for chunk in file_content.chunks():
                fout.write(file_content)
                fout.close()
            except Exception as e:
                image = 'image'
                print(e)

            shop_instance = ShopData.objects.get(mobile=shop_mobile)
            shop_instance.name = name
            shop_instance.description = description
            shop_instance.address = address
            shop_instance.category_id = CategoryData.objects.get(name=category)
            shop_instance.city_id = CityData.objects.get(name=city)
            shop_instance.image = image
            shop_instance.save()
            response['success'] = True
            response['message'] = "Successful"

        except Exception as e:
            response['success'] = False
            response['message'] = "Something went wrong " + str(e)
            print(e)
    else:
        response['success'] = False
        response['message'] = "Illegal request"

    print(response)
    return JsonResponse(response)
