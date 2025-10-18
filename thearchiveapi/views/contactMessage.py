from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import json
from thearchiveapi.models import ContactMessage


@method_decorator(csrf_exempt, name="dispatch")
class ContactMessageView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            content = data.get("content", "").strip()

            # Validate required fields
            if not name:
                return JsonResponse({"success": False, "message": "Name is required."}, status=400)
            if not content:
                return JsonResponse({"success": False, "message": "Message is required."}, status=400)
            
            # Validate email format
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    return JsonResponse({"success": False, "message": "Invalid email format."}, status=400)

            # Save message
            contact_message = ContactMessage.objects.create(
                name=name, 
                email=email or None, 
                content=content
            )

            # Send notification email
            self._send_notification_email(name, email, content, contact_message.sent_at)

            return JsonResponse({"success": True, "message": "Message sent successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "An error occurred. Please try again later."},
                status=500
            )

    def _send_notification_email(self, name, email, content, sent_at):
        """Send email notification for new contact message"""
        try:
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"""
New contact form submission from The Sonatore Archive:

Name: {name}
Email: {email or 'Not provided'}

Message:
{content}

---
Sent at: {sent_at}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print(f"Email sent successfully for message from {name}")
        except Exception as e:
            print(f"Email sending error: {str(e)}")