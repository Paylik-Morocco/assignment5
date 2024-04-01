from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication

from tickets.models import Ticket, TicketReply

from tickets.serializers import TicketSerializer, TicketReplySerializer, DetailedTicketSerializer

from django.shortcuts import get_object_or_404
import datetime

from tickets.emails import send_ticket_created_emails, send_ticket_updated_email, send_ticket_reply_email

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def all_tickets(request):
    tickets = []
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = request.user.tickets
    if request.GET.get('status') != None:
        tickets = tickets.filter(status=request.GET.get('status'))
    if 'start_datetime' in request.GET:
        tickets = tickets.filter(created_at__gte=datetime.datetime.fromisoformat(request.GET['start_datetime']))
    if 'end_datetime' in request.GET:
        tickets = tickets.filter(created_at__lte=datetime.datetime.fromisoformat(request.GET['end_datetime']))
    if 'search' in request.GET:
        tickets = tickets.filter(title__icontains=request.GET['search'])
        tickets = tickets.filter(description__icontains=request.GET['search'])

    serializer = TicketSerializer(instance=tickets, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def tickets_overview(request):
    tickets = []
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = request.user.tickets
    all = tickets.count()
    open = tickets.filter(status='open').count()
    closed = tickets.filter(status='closed').count()
    resolved = tickets.filter(status='resolved').count()

    return Response({
        'all': all,
        'open': open,
        'closed': closed,
        'resolved': resolved
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ticket(request, id):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, id=id)
    else:
        ticket = get_object_or_404(Ticket, id=id, created_by=request.user)

    serializer = DetailedTicketSerializer(instance=ticket)
    return Response(data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    if request.user.is_staff:
        # staff can't create tickets
        return Response({"detail": "You cannot create a ticket as an admin."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TicketSerializer(data={**request.data, "created_by": request.user.id})

    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    send_ticket_created_emails(ticket_id=serializer.data['id'])
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.status != 'open':
        return Response({"detail": f"You cannot change the status of a {ticket.status} ticket"}, status=status.HTTP_403_FORBIDDEN)
    if request.data['status'] not in ('closed', 'resolved'):
        return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    
    ticket.status = request.data['status']
    ticket.save()

    serializer = TicketSerializer(instance=ticket)
    send_ticket_updated_email(ticket_id=ticket.id)
    return Response(serializer.data, status=status.HTTP_200_OK)
 
@api_view(['POST'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_ticket_reply(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if TicketReply.objects.filter(ticket=ticket, created_by=request.user).exists():
        return Response({"detail": "You have already replied to this ticket."}, status=status.HTTP_403_FORBIDDEN)
    serializer = TicketReplySerializer(data={**request.data, "created_by": request.user.id, "ticket":ticket.id})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    send_ticket_reply_email(ticket_id=ticket.id)
    return Response(serializer.data, status=status.HTTP_201_CREATED)