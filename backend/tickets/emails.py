from postmarker.core import PostmarkClient
import os
import asyncio
from tickets.models import Ticket
from users.models import User
import time
from django.core.exceptions import ObjectDoesNotExist

postmark = PostmarkClient(server_token=os.environ['POSTMARK_SERVER_TOKEN'])

async def send_email(From, To, Subject, HtmlBody):
    return postmark.emails.send(From=From, To=To, Subject=Subject, HtmlBody=HtmlBody)


def send_ticket_created_emails(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except ObjectDoesNotExist:
        raise Exception('ticket does not exist.')
    ticket_owner = User.objects.get(id=ticket.created_by.id)
    admins = User.objects.filter(is_staff=True)

    emails = []
    APP_URL = os.environ['APP_URL']
    emails.append({
        'From': 'noreply@paylik.ma',
        'To': ticket_owner.email,
        'Subject': 'Your ticket has been created',
        'HtmlBody': f'<html><body>Your ticket has been created. <strong>Ticket#{ticket.id} </strong> <br/> <a href="{APP_URL}/ticket/{ticket.id}">View ticket</a>.</body></html>',
    })

    for admin in admins:
        emails.append({
            'From': 'noreply@paylik.ma',
            'To': admin.email,
            'Subject': 'A ticket has been created',
            'HtmlBody': f'<html><body>A ticket has been created. with the title {ticket.title} by the user {ticket_owner.username} ({ticket_owner.email}) <br /> <strong>Ticket#{ticket.id} </strong> <br/> <a href="{APP_URL}/ticket/{ticket.id}">View ticket</a>.</body></html>',
        })
    postmark.emails.send_batch(*emails)
    return

def send_ticket_updated_email(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except ObjectDoesNotExist:
        raise Exception('ticket does not exist.')
    ticket_owner = User.objects.get(id=ticket.created_by.id)

    emails = []
    # APP_URL = os.environ['APP_URL']
    APP_URL = "http://localhost:5173/"
    emails.append({
        'From': 'noreply@paylik.ma',
        'To': ticket_owner.email,
        'Subject': 'Your ticket has been updated!',
        'HtmlBody': f'<html><body>Your ticket has been updated. <strong>Ticket#{ticket.id} </strong> <br/> <a href="{APP_URL}/ticket/{ticket.id}">View ticket</a>.</body></html>',
    })
   
    postmark.emails.send_batch(*emails)
    return 

def send_ticket_reply_email(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except ObjectDoesNotExist:
        raise Exception('ticket does not exist.')
    ticket_owner = User.objects.get(id=ticket.created_by.id)

    emails = []
    # APP_URL = os.environ['APP_URL']
    APP_URL = "http://localhost:5173/"
    emails.append({
        'From': 'noreply@paylik.ma',
        'To': ticket_owner.email,
        'Subject': 'An admin replied to your ticket!',
        'HtmlBody': f'<html><body>An admin replied to your ticket. <strong>Ticket#{ticket.id} </strong> <br/> <a href="{APP_URL}/ticket/{ticket.id}">View ticket</a>.</body></html>',
    })
   
    postmark.emails.send_batch(*emails)
    return 