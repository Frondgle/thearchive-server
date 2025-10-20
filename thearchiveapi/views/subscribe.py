from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from thearchiveapi.models import Subscriber

class SubscribeView(APIView):
    """Handle email subscription requests"""

    def post(self, request):
        try:
            email = request.data.get("email")  # ← DRF auto-parses JSON
            print("Email:", email)

            if not email:
                print("No email provided!")
                return Response(
                    {"success": False, "message": "Email is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                print("Invalid email format!")
                return Response(
                    {"success": False, "message": "Invalid email format"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if created:
                print("New subscriber created!")

                # Send welcome email to new subscriber
                try:
                    unsubscribe_url = f"{settings.SITE_URL}/unsubscribe/unsubscribe/?token={subscriber.unsubscribe_token}"

                    email_subject = "Welcome to The Sonatore Archive!"
                    
                    text_body = f"""
                        Thank you for subscribing to The Sonatore Archive!

                        You'll now receive updates about new content, features, and announcements.

                        If you didn't sign up for this, or if you wish to unsubscribe, click the following link: {unsubscribe_url}

                        Best regards,
                        The Sonatore Archive Team
                    """
                    
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
                    print(f"Email sending error: {str(e)}")

                return Response(
                    {"success": True, "message": "Successfully subscribed!"},
                    status=status.HTTP_201_CREATED  # ← 201 for resource creation
                )
            else:
                print("Email already exists!")
                return Response(
                    {"success": False, "message": "Email already subscribed"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print("Error:", str(e))
            return Response(
                {"success": False, "message": "An error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )