from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

def send_election_notifications(request, election, recipients):
    """Send email notifications about a new election to all eligible voters."""
    subject = f'New Election: {election.title}'
    
    context = {
        'election': election,
        'request': request,
    }
    
    html_message = render_to_string('election/email/election_notification.html', context)
    plain_message = strip_tags(html_message)
    
    messages = []
    for recipient in recipients:
        messages.append((
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [recipient.email]
        ))
    
    try:
        send_mass_mail(messages, fail_silently=False)
        election.notification_sent = True
        election.save()
        return True
    except Exception as e:
        print(f"Error sending election notifications: {e}")
        return False

def send_vote_confirmation(request, user, election):
    """Send a confirmation email to a user after they vote."""
    subject = f'Vote Confirmation - {election.title}'
    
    context = {
        'user': user,
        'election': election,
        'request': request,
    }
    
    html_message = render_to_string('election/email/vote_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False
        )
        return True
    except Exception as e:
        print(f"Error sending vote confirmation: {e}")
        return False 