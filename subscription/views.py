from __future__ import print_function
from django.shortcuts import render
import os
import random

import jwt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from city.models import UserCityData
from customs.sms import send_sms
from .models import *


# Create your views here.
@csrf_exempt
def add_subscription(request):
    response={}
    if request.method=='GET':
        try:
            subscription_list=[]
            for subscription in SubscriptionData.objects.all():
                subscription_list.append(
                    {
                    }
                )

        except Exception as e:
            print(e)
