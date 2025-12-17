# files/forms.py
from django import forms
from .models import Conversation, Message

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title', 'participants']  # participants là ManyToManyField


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
