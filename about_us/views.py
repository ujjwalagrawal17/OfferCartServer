from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def about_us(request):
	if request.method=='GET':
		response_body={}
		response_body['success']=True
		response_body['message']="Successful"
		response_body['title']="About Discount Store"
		response_body['description']="Discount Store is a startup ,\n Discount store sells out Offers from Traditional shops. You will get a offer code in your mobile phone after buying a offer.\n Discount store uses Payumoney for Online Payment.\n\n Have a Nice Day:)"
		response_body['image_url']=request.scheme+'://'+request.get_host()+'/media/about_us/discount_store_logo.png'

		return JsonResponse(response_body)
