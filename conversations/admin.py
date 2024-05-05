from django.contrib import admin
from .models import Conversation, Message


class MessageAdmin(admin.ModelAdmin):
	list_display = ('conversation', 'sender', 'content', 'timestamp')


class ConversationAdmin(admin.ModelAdmin):
	list_display = ('id', 'creator', 'invitee', 'created_at')


admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)
