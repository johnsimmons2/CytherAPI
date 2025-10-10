from django.http import JsonResponse


def health_check(request) -> JsonResponse:
    return JsonResponse({'status': 'OK', 'message': 'API is running'}, status=200)
