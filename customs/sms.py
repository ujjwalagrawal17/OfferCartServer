import requests
from .models import KeysData
def send_sms(mobile,msg,sender="DSTORE"):
	authkey=str(KeysData.objects.get(key="msg91").value)
	url='http://api.msg91.com/api/sendhttp.php?authkey='+authkey+'&mobiles='
	url+=mobile
	url+='&message='+msg
	url+='&sender='+sender+'&route=4'
	print url
	print requests.request('GET', url)