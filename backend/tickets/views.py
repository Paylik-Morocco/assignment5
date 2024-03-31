from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication

from tickets.models import Ticket, TicketReply

from tickets.serializers import TicketSerializer, TicketReplySerializer, DetailedTicketSerializer

from django.shortcuts import get_object_or_404

@api_view(['GET'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def all_tickets(request):
    tickets = []
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = request.user.tickets
    
    serializer = TicketSerializer(instance=tickets, many=True)

    return Response(serializer.data)
    """ 
    if user not is_staff
    get own tickets paginated

if user is_staff
    get all tickets paginated

    filter:
    status
    date
    search by keyword

    sort by date asc desc
    
    """
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
    return Response(serializer.data, status=status.HTTP_200_OK)
    """
        if user not is_staff: prevent

        else if user is_staff:
        update ticket
        send email to user
    """
@api_view(['POST'])
@authentication_classes([TokenAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_ticket_reply(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if TicketReply.objects.filter(ticket=ticket).exists():
        return Response({"detail": "This ticket already has a reply."}, status=status.HTTP_403_FORBIDDEN)
    serializer = TicketReplySerializer(data={**request.data, "created_by": request.user.id, "ticket":ticket.id})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    """
    if user not is_staff: prevent
    else if user is_staff:
    create ticket reply
    send email to user
    """