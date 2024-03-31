from rest_framework import serializers
from tickets.models import (Ticket, TicketReply)
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'created_by']
class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = ['id', 'text', 'created_at', 'created_by', 'ticket']

class DetailedTicketSerializer(serializers.ModelSerializer):
    reply = TicketReplySerializer(many=False)
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'created_by', 'reply']