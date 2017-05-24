from __future__ import print_function

import os
import random
import string

import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from customs.sms import send_sms
from register.models import UserData
from .models import *


# Create your views here.
@csrf_exempt
def send_offer(request):
    response_json = {}
    if request.method == "GET":
        try:
            for x, y in request.GET.items():
                print(x, ":", y)
            # category_id= str(request.POST.get("category_id"))
            shop_id = str(request.GET.get("shop_id"))
            shop_row = ShopData.objects.get(id=int(shop_id))
            response_json["success"] = True
            response_json["shop_id"] = int(shop_id)
            response_json["shop_name"] = str(shop_row.name)
            response_json["shop_description"] = str(shop_row.description)
            response_json["shop_image"] = request.scheme + '://' + request.get_host() + '/media/' + str(shop_row.image)
            response_json["shop_address"] = str(shop_row.address)
            response_json["offer_list"] = []

            for o in OfferData.objects.filter(shop_id=int(shop_id)):
                if o.active:
                    temp_json = {"offer_id": int(o.id), "name": str(o.name), "description": str(o.description),
                                 "validity": str(o.validity),
                                 "image": request.scheme + '://' + request.get_host() + '/media/' + str(o.image),
                                 "price": int(o.price)}
                    response_json["offer_list"].append(temp_json)
        except Exception as e:
            print("e@offer", e)
            response_json["success"] = False
            response_json["message"] = " offer_data not  found"
    else:
        response_json['success'] = False
        response_json['message'] = "not get method"
    return JsonResponse(response_json)


# Create your views here.
@csrf_exempt
def buy_offer(request):
    response_json = {}
    if request.method == 'POST':
        try:
            for x, y in request.POST.items():
                print(x, ":", y)
            access_token = request.POST.get('access_token')
            offer_id = request.POST.get('offer_id')
            json = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
            print(json['mobile'])
            mobile = json['mobile']
            response_json["success"] = True
            response_json["message"] = 'Successful'
            user = UserData.objects.get(mobile=str(json['mobile']))
            wallet = user.wallet
            offer_details = OfferData.objects.get(id=int(offer_id))
            price = offer_details.price
            if wallet < price:
                response_json["success"] = False
                response_json[
                    "message"] = 'Transaction Unsuccessful, wallet does not have that amount of money. Please Add ' \
                                 'some Money in your Wallet '
            else:
                offer_code = code_generator()
                OfferBoughtData.objects.create(mobile=str(mobile), price=price, offer_id=offer_id,
                                               offer_code=offer_code, avialable=True)
                user.wallet = wallet - price
                user.save()
                shop_details = ShopData.objects.get(name=offer_details.shop_id)
                try:
                    msg = ' Thank you for using Discount Store. You have successfully bought the Offer " ' + str(
                        offer_details.name) + ' "" for Shop ' + str(shop_details.name) + '. Your Offer Code is  ' + str(
                        offer_code) + '. To Redeem the offer Please show this Message and Code During Billing.%0A ' \
                                      '%0AThanks Team Discount Store '
                    send_sms(mobile, msg)
                    send_sms('8109109457', msg)
                    send_sms('8519072717', msg)
                except Exception as e:
                    print(e)
                response_json["offer_name"] = offer_details.name
                response_json["price"] = offer_details.price
        except Exception as e:
            response_json["success"] = False
            response_json["message"] = "error in buyoffers"
            print(e)

    else:
        response_json['success'] = False
        response_json['message'] = "Get Out From Here"
    return JsonResponse(response_json)


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


####################### Shop Admin Modules #############################
import datetime


@csrf_exempt
def offer_add(request):
    response_json = {}
    if request.method == 'POST':
        try:
            for x, y in request.GET.items():
                print(x, ":", y)

            shop_access_token = str(request.POST.get('shop_access_token'))
            json = jwt.decode(str(shop_access_token), '810810', algorithms=['HS256'])
            shop_mobile = str(json['mobile'])

            offer_title = str(request.POST.get('offer_title'))
            offer_description = str(request.POST.get('offer_description'))
            year = str(request.POST.get('year'))
            month = str(request.POST.get('month'))
            date = str(request.POST.get('date'))

            expiry_date = year + '-' + month + '-' + date
            expiry_date = datetime.datetime.strptime(expiry_date, '%Y-%m-%d')
            print(expiry_date)
            shop_instance = ShopData.objects.get(mobile=shop_mobile)

            try:
                image = request.FILES.get('offer_image').name
                folder = 'media/' + 'offer/'
                full_filename = os.path.join(folder, image)
                print("full name", full_filename)
                # fout = open(folder+image, 'wb+')
                print("image=", image)
                fout = open(folder + image, 'w')
                file_content = request.FILES.get('offer_image').read()
                # for chunk in file_content.chunks():
                fout.write(file_content)
                fout.close()
            except Exception as e:
                image = 'image'
                print(e)

            OfferData.objects.create(
                shop_id=shop_instance,
                name=offer_title,
                description=offer_description,
                image=image,
                expiry_date=expiry_date
            )

            response_json['success'] = True
            response_json['message'] = "Offer created successfully"

        except Exception as e:
            response_json['success'] = False
            response_json['message'] = 'Something went wrong, Unable to create offer - ' + str(e)
            print(e)
    else:
        response_json['success'] = False
        response_json['message'] = "Illegal request"
    print(response_json)
    return JsonResponse(response_json)


@csrf_exempt
def shop_offers(request):
    response = {}
    if request.method == 'GET':
        try:
            shop_access_token = str(request.GET.get('shop_access_token'))
            json = jwt.decode(str(shop_access_token), '810810', algorithms=['HS256'])
            shop_mobile = str(json['mobile'])

            shop_instance = ShopData.objects.get(mobile=shop_mobile)

            offer_data = OfferData.objects.filter(shop_id=shop_instance)
            offer_list = []
            for offer in offer_data:
                today_date = datetime.datetime.today().date()

                print("Today: " + str(today_date))
                print("Expiry: " + str(offer.expiry_date))

                offer_list.append({
                    'offer_id': offer.id,
                    'offer_title': offer.name,
                    'offer_description': offer.description,
                    'offer_image': request.scheme + '://' + request.get_host() + '/media/offer/' + str(offer.image),
                    'offer_validity_days': (offer.expiry_date - today_date).days,
                    'offer_expiry_date': str(offer.expiry_date),
                    'active': offer.active
                })

            response['success'] = True
            response['message'] = "Successful"
            response['shop_name'] = shop_instance.name
            response['subscription_validity'] = 10

            response['shop_offer_list'] = offer_list
        except Exception as e:
            response['success'] = False
            response['message'] = "Something went wrong" + str(e)
    else:
        response['success'] = False
        response['message'] = "Illegal request"
    print(response)
    return JsonResponse(response)


@csrf_exempt
def offer_edit(request):
    response_json = {}
    if request.method == 'POST':
        try:
            for x, y in request.GET.items():
                print(x, ":", y)

            shop_access_token = str(request.POST.get('shop_access_token'))
            json = jwt.decode(str(shop_access_token), '810810', algorithms=['HS256'])
            shop_mobile = str(json['mobile'])

            offer_id = str(request.POST.get('offer_id'))
            offer_title = str(request.POST.get('offer_title'))
            offer_description = str(request.POST.get('offer_description'))
            year = str(request.POST.get('year'))
            month = str(request.POST.get('month'))
            date = str(request.POST.get('date'))

            expiry_date = year + '-' + month + '-' + date
            expiry_date = datetime.datetime.strptime(expiry_date, '%Y-%m-%d')

            try:
                image = request.FILES.get('offer_image').name
                folder = 'media/' + 'offer/'
                full_filename = os.path.join(folder, image)
                print("full name", full_filename)
                # fout = open(folder+image, 'wb+')
                print("image=", image)
                fout = open(folder + image, 'w')
                file_content = request.FILES.get('offer_image').read()
                # for chunk in file_content.chunks():
                fout.write(file_content)
                fout.close()
            except Exception as e:
                image = 'image'
                print(e)

            shop_instance = ShopData.objects.get(mobile=shop_mobile)
            offer_instance = OfferData.objects.get(shop_id=shop_instance, id=offer_id)

            offer_instance.name = offer_title
            offer_instance.description = offer_description,
            offer_instance.image = 'offer/' + image,
            offer_instance.expiry_date = expiry_date
            offer_instance.save()

            response_json['success'] = True
            response_json['message'] = "Offer edited successfully"

        except Exception as e:
            response_json['success'] = False
            response_json['message'] = 'Something went wrong, Unable to edit offer - ' + str(e)
            print(e)
    else:
        response_json['success'] = False
        response_json['message'] = "Illegal request"
    print(response_json)
    return JsonResponse(response_json)
