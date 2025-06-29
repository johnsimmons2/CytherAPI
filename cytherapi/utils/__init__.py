from django.http import JsonResponse
from typing import Any


def RESPONSE(status: int, msg: str = None, err: bool | Any = False, **additional_data) -> JsonResponse:
    '''
    generic response function.
    :param status: HTTP status code
    :param msg: message to return
    :param err: defaults to "True", can override with object or detail message.
    '''
    response = {'status': status, 'message': msg}
    if err is not False:
        response['error'] = err if isinstance(err, bool) else str(err)
        
    if additional_data:
        for key, value in additional_data.items():
            response[key] = value
    return JsonResponse(response, status=status)

def OK(msg='OK', **kwargs):
    return RESPONSE(200, msg, **kwargs)

def CREATED(msg='Created', **kwargs):
    return RESPONSE(201, msg, **kwargs)

def ACCEPTED(msg='Accepted', **kwargs):
    return RESPONSE(202, msg, **kwargs)

def NO_CONTENT(msg='No Content', **kwargs):
    return RESPONSE(204, msg, **kwargs)

def NOT_MODIFIED(msg='Not Modified', **kwargs):
    return RESPONSE(304, msg, **kwargs)

def BAD_REQUEST(msg='Bad Request', err=True, **kwargs):
    return RESPONSE(400, msg, err, **kwargs)

def UNAUTHORIZED(msg='Unauthorized', err=True, **kwargs):
    return RESPONSE(401, msg, err, **kwargs)

def FORBIDDEN(msg='Forbidden', err=True):
    return JsonResponse({'status': 403, 'message': msg, 'error': err})

def NOT_FOUND(msg='Not Found', err=True, **kwargs):
    return RESPONSE(404, msg, err, **kwargs)

def INTERNAL_SERVER_ERROR(msg='Internal Server Error', err=True, **kwargs):
    import logging
    logger = logging.getLogger('cytherapi-fatal')
    server_response = {'status': 500, 'message': msg, 'error': err}
    if kwargs:
        for key, value in kwargs.items():
            server_response[key] = value
    logger.error(server_response)
    return JsonResponse(server_response)