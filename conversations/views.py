import json

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import Conversation, User


@require_POST
def create_conversation(request: HttpRequest) -> JsonResponse:
    user = request.user
    # session_username = request.session.get("username")
    # if not session_username:
    #     return JsonResponse(
    #         {"status": False, "message": "No username found in session!"}, status=422
    #     )

    # try:
    #     user: User = User.objects.get(username=session_username)
    # except User.DoesNotExist:
    #     return JsonResponse({"status": False, "message": "User does not exist!"}, status=400)

    new_conversation: Conversation = Conversation.objects.create(creator=user)

    return JsonResponse(
        {
            "status": True,
            "message": "Conversation created successfully!",
            "data": {"conversation_id": new_conversation.id},
        },
        status=201,
    )


@require_POST
def join_conversation(request: HttpRequest) -> JsonResponse:
    user = request.user
    # session_username = request.session.get("username")

    # if not session_username:
    #     return JsonResponse(
    #         {"status": False, "message": "No username found in session!"}, status=422
    #     )

    # try:
    #     user: User = User.objects.get(username=session_username)
    # except User.DoesNotExist:
    #     return JsonResponse({"status": False, "message": "User does not exist!"}, status=400)

    request_data = json.loads(request.body)
    conversation_id = request_data.get("conversation_id")

    try:
        conversation: Conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return JsonResponse(
            {"status": False, "message": "Conversation does not exist!"}, status=400
        )

    # checks if conversation has an invitee already
    if conversation.invitee:
        if conversation.invitee == user:
            return JsonResponse(
                {
                    "status": True,
                    "message": "Conversation joined successfully!",
                    "data": {"conversation_id": conversation.id},
                },
                status=200,
            )

        return JsonResponse({"status": False, "message": "Conversation full already!"}, status=400)

    # checks if the creator is same as the user in session
    if conversation.creator == user:
        return JsonResponse(
            {
                "status": True,
                "message": "Conversation joined successfully!",
                "data": {"conversation_id": conversation.id},
            },
            status=200,
        )

    # if the conversation does not have an invitee
    conversation.invitee = user
    conversation.save()

    return JsonResponse(
        {
            "status": True,
            "message": "Conversation joined successfully!",
            "data": {"conversation_id": conversation.id},
        },
        status=200,
    )


# TODO: make username check a decorator
@require_GET
def view_conversation(request: HttpRequest, id: str) -> HttpResponse:
    user = request.user
    # username = request.session.get("username")
    # if not username:
    #     messages.error(request, "You need to pick username to join a conversation!")
    #     return redirect(reverse("core:index"))

    # try:
    #     user = User.objects.get(username=username)
    # except User.DoesNotExist:
    #     messages.error(request, "Conversation does not exist!")
    #     return redirect(reverse("core:index"))

    try:
        conversation = Conversation.objects.get(id=id)
    except Conversation.DoesNotExist:
        messages.error(request, "Conversation does not exist!")
        return redirect(reverse("core:index"))

    # checks if the user is either a creator or an invitee
    if conversation.creator == user or conversation.invitee == user:
        return render(
            request,
            "conversations/view_conversation.html",
            {
                "title": f"Conversation {conversation.id}",
                "conversation": conversation,
                "convo_messages": conversation.messages.all(),
                "username": user.username,
            },
        )

    # if the user is neither
    messages.error(request, "Sorry, you cannot join this conversation!")
    return redirect(reverse("core:index"))


@require_GET
def get_conversation_history(request):
    current_user = request.user
    conversations = Conversation.objects.filter(creator=current_user) | Conversation.objects.filter(invitee=current_user)
    return render(request, 'calls_history.html', {'conversations': conversations})


@require_POST
def find_conversation(request):
    # Get the current user
    current_user = request.user

    # Query to find an existing conversation with an empty invitee field
    existing_conversation = Conversation.objects.filter(invitee__isnull=True).order_by('-created_at').first()

    # If an existing conversation with empty invitee exists, update it and redirect
    if existing_conversation:
        existing_conversation.invitee = current_user
        existing_conversation.save()
        return JsonResponse(
        {
            "status": True,
            "message": "Conversation joined successfully!",
            "data": {"conversation_id": existing_conversation.id},
        },
        status=200,
    )

    # If no empty conversation exists, create a new one and redirect
    new_conversation = Conversation.objects.create(creator=current_user)
    return JsonResponse(
        {
            "status": True,
            "message": "Conversation joined successfully!",
            "data": {"conversation_id": new_conversation.id},
        },
        status=200,
    )