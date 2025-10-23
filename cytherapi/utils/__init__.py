from django.http import HttpResponse, JsonResponse
from typing import Any


def RESPONSE(status: int, msg: str | None = None, err: Any = None, **extra) -> JsonResponse:
    """
    Generic JSON response.
    :param status: HTTP status code
    :param msg: message to return
    :param err: if truthy, include an 'error' field (bool or stringified object)
    """
    # No body for 204/304
    if status in (204, 304):
        return HttpResponse(status=status)

    body: dict[str, Any] = {}
    if msg is not None:
        body["message"] = msg

    if err:  # only include when truthy
        body["error"] = err if isinstance(err, bool) else str(err)

    if extra is not None:
        extra_data: dict[str, Any] = {}
        extra_data.update(extra)
        body["data"] = extra_data
    return JsonResponse(body, status=status)

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