from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from urllib.parse import quote
import json
from thearchiveapi.models import Subscriber

@method_decorator(csrf_exempt, name="dispatch")
class SubscriberView(View):

    def post(self, request):
        try:
            print("Request body:", request.body)
            data = json.loads(request.body)
            print("Parsed data:", data)
            email = data.get("email")
            print("Email:", email)

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
                    # URL encode the email for the unsubscribe link
                    encoded_email = quote(email)
                    unsubscribe_url = f"{settings.SITE_URL}/unsubscribe/unsubscribe/?email={encoded_email}"

                    email_subject = "Welcome to The Sonatore Archive!"
                    
                    # Plain text version (fallback)
                    text_body = f"""
                        Thank you for subscribing to The Sonatore Archive!

                        You'll now receive updates about new content, features, and announcements.

                        If you didn't sign up for this, or if you wish to unsubscribe, click the following link: {unsubscribe_url}

                        Best regards,
                        The Sonatore Archive Team
                    """
                    
                    # HTML version (with clickable link)
                    html_body = f"""
                        <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                                <p>Thank you for subscribing to The Sonatore Archive!</p>
                                
                                <p>You'll now receive updates about new content, features, and announcements.</p>
                                
                                <p>If you didn't sign up for this, or if you wish to unsubscribe, 
                                click <a href="{unsubscribe_url}" style="color: #2196F3;">HERE</a>.</p>
                                
                                <p>Best regards,<br>
                                The Sonatore Archive Team</p>
                            </body>
                        </html>
                    """
                    
                    # Create email with both text and HTML versions
                    email_message = EmailMultiAlternatives(
                        subject=email_subject,
                        body=text_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email]
                    )
                    email_message.attach_alternative(html_body, "text/html")
                    email_message.send(fail_silently=False)
                    
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