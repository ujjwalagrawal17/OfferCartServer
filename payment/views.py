from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import hashlib
import random

import jwt
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from register.models import UserData
from .models import *

# Create your views here.
transaction_type = {}
transaction_type['credit'] = "credit"
transaction_type['debit'] = "debit"


@csrf_exempt
def request_payment_hash(request):
    if (request.method == 'POST'):
        for x, y in request.POST.items():
            print(x, ":", y)
        access_token = request.POST.get('access_token')
        response_json = {}

        json = {}

        try:
            json = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
            user_details = UserData.objects.get(mobile=str(json['mobile']))
            amount = request.POST.get("amount")
            name = str(user_details.name)
            email = str(user_details.email)
            mobile = str(user_details.mobile)
            product_name = 'Wallet'

            key = 't1iq81Kx'
            merchant_id = '5669435'
            merchant_salt = 'RZHvaXdcuR'

            # key='OPnqOtgp'
            # merchant_id='4943078'
            # merchant_salt='uIBWzo2PAt'



            transaction_id = str(random.randint(10, 99)) + mobile + str(random.randint(10, 99))

            try:
                response_json['name'] = name
                response_json['email'] = email
                response_json['mobile'] = mobile
                response_json['product_name'] = product_name
                response_json['key'] = key
                response_json['merchant_id'] = merchant_id
                response_json['amount'] = amount
                response_json['transaction_id'] = transaction_id

                server_hash_to_encode = key + '|' + transaction_id + '|' + amount + '|' + product_name + '|' + name + '|' + email + '||||||' + merchant_salt
                print(server_hash_to_encode)
                hash_encoded = hashlib.sha512(server_hash_to_encode).hexdigest().lower()
                print(hash_encoded)
                response_json['server_hash'] = hash_encoded
                response_json['success'] = True
                response_json['message'] = 'Successfully Sent Hash'

                PaymentData.objects.create(transaction_id=transaction_id, amount=amount, mobile=mobile)

            except Exception as e:

                response_json['success'] = False
                response_json['message'] = str(e)

                print(e)

        except Exception as e:
            response_json['success'] = False
            response_json['message'] = str(e)
            print(e)

        return JsonResponse(response_json)


    else:
        response_json['success'] = False
        response_json['message'] = "This api is not made for GET Requests"

        return JsonResponse(response_json)


import json


@csrf_exempt
def update_payment_status(request):
    response_json = {}
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        json_mobile = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
        mobile = str(json_mobile['mobile'])
        for x, y in request.POST.items():
            print(x, ":", y)
        # transaction_id='8223003905122'
        transaction_id = request.POST.get('transaction_id')
        key = 't1iq81Kx'
        head = {"Authorization": "bCskEw6nzrPSSN8W+XMy6QZaAV4aFr1+srsGBk1hmp8="}
        url = 'https://www.payumoney.com/payment/op/getPaymentResponse'
        resp = requests.post(url, data={'merchantKey': key, 'merchantTransactionIds': transaction_id}, headers=head)
        payu_payment_details = json.loads(resp.text)
        print("..\n", payu_payment_details)
        for o in payu_payment_details['result']:
            payment = {}
            payment['txnid'] = o['merchantTransactionId']
            if payment['txnid'] == transaction_id:
                tmp = o['postBackParam']
                payment['status'] = tmp['status']
                payment['amount'] = tmp['net_amount_debit']
                if payment['status'] == "success":
                    try:
                        obj = PaymentData.objects.get(transaction_id=transaction_id)
                        obj.status = True
                        obj.transaction_type = transaction_type['credit']
                        obj.save()
                        try:
                            user = UserData.objects.get(mobile=mobile)
                            user.wallet = user.wallet + int(payment['amount'])
                            user.save()
                            response_json['success'] = True
                            response_json['payment'] = payment
                            response_json['message'] = 'Payment Successful'
                        except Exception as e:
                            print("error at 126 ", e)
                            response_json['success'] = False
                            response_json['payment'] = "payment succesful but could not add to wallet"

                    except:
                        response_json['success'] = False
                        response_json['message'] = 'Payment Failed'
                else:
                    response_json['success'] = False
                    response_json['message'] = 'Payment Failed'
            else:
                response_json['success'] = False
                response_json['message'] = 'Tansaction id not found'
                # Do nothing

        return JsonResponse(response_json, safe=False)
    else:
        response_json['success'] = False
        response_json['message'] = 'This api is not made for GET Requests'


def wallet(request):
    response_json = {}
    access_token = request.GET.get('access_token')
    json_mobile = jwt.decode(str(access_token), '999123', algorithms=['HS256'])
    mobile = str(json_mobile['mobile'])
    try:
        user = UserData.objects.get(mobile=mobile)
        response_json['balance'] = user.wallet
        response_json['success'] = True
        response_json['message'] = "succesfull"
    except Exception as e:
        print("error at 163 ", e)
        response_json['success'] = False
        response_json['message'] = "some error occoured"
    print(response_json)
    return JsonResponse(response_json)
