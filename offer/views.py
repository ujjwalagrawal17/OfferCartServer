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
                print x, ":", y
            # category_id= str(request.POST.get("category_id"))
            shop_id = str(request.GET.get("shop_id"))
            print"............................shopid", shop_id
            shop_row = ShopData.objects.get(id=int(shop_id))
            response_json["success"] = True
            response_json["shop_id"] = int(shop_id)
            response_json["shop_name"] = str(shop_row.name)
            response_json["shop_description"] = str(shop_row.description)
            response_json["shop_image"] = request.scheme + '://' + request.get_host() + '/media/' + str(shop_row.image)
            response_json["shop_address"] = str(shop_row.address)
            response_json["offer_list"] = []
            print "debuuged 25"
            for o in OfferData.objects.filter(shop_id=int(shop_id)):
                if o.active == True:
                    temp_json = {}
                    temp_json["offer_id"] = int(o.id)
                    temp_json["name"] = str(o.name)
                    temp_json["description"] = str(o.description)
                    temp_json["validity"] = str(o.validity)
                    temp_json["image"] = request.scheme + '://' + request.get_host() + '/media/' + str(o.image)
                    temp_json["price"] = int(o.price)
                    response_json["offer_list"].append(temp_json)
        except Exception, e:
            print "e@offer", e
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
                print x, ":", y
            access_token = request.POST.get('access_token')
            offer_id = request.POST.get('offer_id')
            json = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
            print json['mobile']
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
                user_id = str(mobile)
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
                except Exception, e:
                    print e
                response_json["offer_name"] = offer_details.name
                response_json["price"] = offer_details.price
        except Exception, e:
            response_json["success"] = False
            response_json["message"] = "error in buyoffers"
            print"e@buyoffer=", e


    else:
        response_json['success'] = False
        response_json['message'] = "Get Out From Here"
    return JsonResponse(response_json)


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
