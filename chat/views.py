from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from chat.models import Room


@login_required
def chat_room(request, slug):
    return render(request, 'chat/chat.html', {
        'room_slug': slug
    })