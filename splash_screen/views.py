from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from customs.models import KeysData


@csrf_exempt
def splash_screen(request):
    # version_row = VersionData.objects.get(version_type='production')
    if request.method == 'GET':

        try:

            version = int(KeysData.objects.get(key='version').value)
            compulsory_update = int(KeysData.objects.get(key='compulsory_update').value)
            # version = version_row.version
            # compulsory_update = version_row.compulsory_update
            response_json = dict(
                version_code=version,
                compulsory_update=compulsory_update,
                success=True,
                message="Version data successful"
            )

        except Exception, e:
            print e
            response_json = dict(
                success=False,
                message='Unable to get version data'
            )
    else:
        response_json = dict(
            success=False,
            message='Invalid server request'
        )
    print str(response_json)
    return JsonResponse(response_json)


def initial():
    return HttpResponse("<a href=./login>admin_login</a>")
