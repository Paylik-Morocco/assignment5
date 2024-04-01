"""
URL configuration for ticket_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from users.views import get_profile, signup, CustomTokenObtainPairView
from tickets.views import (all_tickets, get_ticket, create_ticket, update_ticket, create_ticket_reply, tickets_overview)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup, name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', view=get_profile),
    path('api/tickets/', view=all_tickets),
    path('api/tickets/overview/', view=tickets_overview),
    path('api/tickets/<int:id>/', view=get_ticket),
    path('api/tickets/create/', view=create_ticket),
    path('api/tickets/<int:id>/update/', view=update_ticket),
    path('api/tickets/<int:id>/reply/', view=create_ticket_reply),
]

urlpatterns = format_suffix_patterns(urlpatterns)