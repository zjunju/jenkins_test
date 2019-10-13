from django.http import JsonResponse


def jsonSuccess(msg=None, data={}):
    context = {
        'code': 200,
        'msg': msg,
        'data': data,
    }

    return JsonResponse(context)


def jsonFailed(code,msg=None, data={}):
    context = {
        'code': code,
        'msg': msg,
        'data': data,
    }

    return JsonResponse(context)
