from django.shortcuts import render


# функция обработки шаблона ошибки 404.
def page_not_found(request, exception):
    return render (request, 'pages/404.html', status=404)


# функция обработки шаблона ошибки 500.
def server_error(request):
    return render (request, 'pages/500.html', status=500)


# функция обработки шаблона ошибки 403.
def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

