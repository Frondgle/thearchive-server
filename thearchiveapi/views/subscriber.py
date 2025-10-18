from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
from thearchiveapi.models import Subscriber


@method_decorator(csrf_exempt, name="dispatch")
class SubscriberView(View):

    def post(self, request):
        try:
            print("Request body:", request.body)  # See raw data
            data = json.loads(request.body)
            print("Parsed data:", data)  # See parsed JSON
            email = data.get("email")
            print("Email:", email)  # See email value

            if not email:
                print("No email provided!")
                return JsonResponse(
                    {"success": False, "message": "Email is required"}, status=400
                )

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                print("Invalid email format!")
                return JsonResponse(
                    {"success": False, "message": "Invalid email format"}, status=400
                )

            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if created:
                print("New subscriber created!")

                # Send welcome email to new subscriber
                try:
                    email_subject = "Welcome to The Sonatore Archive!"
                    email_body = f"""
                        Thank you for subscribing to The Sonatore Archive!

                        You'll now receive updates about new content, features, and announcements.

                        If you didn't sign up for this, please ignore this email.

                        Best regards,
                        The Sonatore Archive Team
                    """
                    
                    send_mail(
                        subject=email_subject,
                        message=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],  # Send to the subscriber
                        fail_silently=False,
                    )
                    print(f"Welcome email sent to {email}")
                except Exception as e:
                    # Log email error but don't fail the subscription
                    print(f"Email sending error: {str(e)}")

                return JsonResponse(
                    {"success": True, "message": "Successfully subscribed!"}
                )
            else:
                print("Email already exists!")
                return JsonResponse(
                    {"success": False, "message": "Email already subscribed"},
                    status=400,
                )

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"success": False, "message": str(e)}, status=500)
