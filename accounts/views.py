import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login

from .models import User



@require_POST
def pick_username(request: HttpRequest) -> JsonResponse:
    request_data = json.loads(request.body)

    username = request_data.get("username")
    password = request_data.get("password")
    user = authenticate(request, username=username, password=password)
    print(username, password)
    if user is not None:
        login(request, user)
        return JsonResponse(
        {"status": True, "message": "Successful! You can now join/create conversations."},
        status=201,
    )
    else:
        return JsonResponse({"status": False, "message": "Invalid username or password"}, status=400)

    # existing_user = User.objects.filter(username=username).exists()
    # if existing_user:
    #     return JsonResponse({"status": False, "message": "Username already taken!"}, status=400)

    # new_user = User.objects.create(username=username)
    # request.session["username"] = new_user.username

    # return JsonResponse(
    #     {"status": True, "message": "Successful! You can now join/create conversations."},
    #     status=201,
    # )
