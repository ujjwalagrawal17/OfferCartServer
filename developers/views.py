from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def developers(request):
	if request.method=='GET':
		response_body={}
		company_data={}
		response_body['success']=True
		response_body['message']="Successful"
		company_data['company']="CodeNicely"
		company_data['address']="Raipur , Chhattisgarh"
		company_data['email']="codenicely@gmail.com"
		company_data['facebook']="http://www.facebook.com/CodeNicely"
		company_data['contact']="+91 8109109457"
		company_data['about']="We Code StartUps \n\n CodeNicely is a Raipur based Startup.\n We provide all types of IT Solutions. We are a team of some geeky geeks from NIT Raipur and we Love Coding."
		company_data['companyImage']=request.scheme+'://'+request.get_host()+"/media/developers/codenicely_full_logo.png"
		company_data['website']="http://www.codenicely.in"
		response_body['companyData']=company_data


		return JsonResponse(response_body)
