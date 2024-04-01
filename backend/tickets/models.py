from django.db import models
from django.db.models import CheckConstraint, Q, F
from users.models import User
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=(
        # constraint the value of 'status' to (open, resolved, closed)
        ("open", "Open"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ), default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="tickets", on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title
    
class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="replies", on_delete=models.CASCADE)
    text = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    