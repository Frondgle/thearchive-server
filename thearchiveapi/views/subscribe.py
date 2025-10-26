from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from thearchiveapi.models import Subscriber
from django.shortcuts import redirect

class SubscribeView(APIView):
    """Handle email subscription requests"""

    def post(self, request):
        try:
            email = request.data.get("email")
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

                # Send CONFIRMATION email
                try:
                    confirm_url = f"{settings.BACKEND_URL}/api/subscribe/confirm/?token={subscriber.subscribe_token}"

                    email_subject = "Confirm Your Subscription to The Sonatore Archive"
                    
                    text_body = f"""
                        Thank you for subscribing to The Sonatore Archive!

                        Please confirm your subscription by clicking the following link:
                        {confirm_url}

                        If you didn't sign up for this, you can safely ignore this email.

                        Best regards,
                        The Sonatore Archive Team
                    """
                    
                    html_body = f"""
                        <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                                <p>Thank you for subscribing to The Sonatore Archive!</p>
                                
                                <p>Please confirm your subscription by clicking the link below:</p>
                                
                                <p><a href="{confirm_url}" style="background-color: #2196F3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Confirm Subscription</a></p>
                                
                                <p style="color: #666; font-size: 14px;">If you didn't sign up for this, you can safely ignore this email.</p>
                                
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
                    
                    print(f"Confirmation email sent to {email}")
                except Exception as e:
                    print(f"Email sending error: {str(e)}")

                return Response(
                    {"success": True, "message": "Please check your email to confirm your subscription!"},
                    status=status.HTTP_201_CREATED
                )
            else:
                # Email already exists - check if confirmed
                if subscriber.is_confirmed:
                    print("Email already confirmed!")
                    return Response(
                        {"success": False, "message": "Email already subscribed"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    print("Email exists but not confirmed - resending confirmation")
                    
                    # Resend confirmation email
                    try:
                        confirm_url = f"{settings.BACKEND_URL}/api/subscribe/confirm/?token={subscriber.subscribe_token}"

                        email_subject = "Confirm Your Subscription to The Sonatore Archive"
                        
                        text_body = f"""
                            Thank you for subscribing to The Sonatore Archive!

                            Please confirm your subscription by clicking the following link:
                            {confirm_url}

                            If you didn't sign up for this, you can safely ignore this email.

                            Best regards,
                            The Sonatore Archive Team
                        """
                        
                        html_body = f"""
                            <html>
                                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                                    <p>Thank you for subscribing to The Sonatore Archive!</p>
                                    
                                    <p>Please confirm your subscription by clicking the link below:</p>
                                    
                                    <p><a href="{confirm_url}" style="background-color: #2196F3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Confirm Subscription</a></p>
                                    
                                    <p style="color: #666; font-size: 14px;">If you didn't sign up for this, you can safely ignore this email.</p>
                                    
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
                        
                        print(f"Confirmation email resent to {email}")
                    except Exception as e:
                        print(f"Email sending error: {str(e)}")
                    
                    return Response(
                        {"success": True, "message": "Confirmation email resent! Please check your inbox."},
                        status=status.HTTP_200_OK
                    )

        except Exception as e:
            print("Error:", str(e))
            return Response(
                {"success": False, "message": "An error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ConfirmSubscriptionView(APIView):
    """Confirm subscription via token and redirect to frontend"""

    def get(self, request):
        token = request.query_params.get("token")
        
        if not token:
            return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=false")

        try:
            subscriber = Subscriber.objects.get(subscribe_token=token)
            
            if subscriber.is_confirmed:
                # Already confirmed
                return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=true&already=true")
            
            # Confirm the subscription
            subscriber.is_confirmed = True
            subscriber.save()
            
            print(f"Subscription confirmed for {subscriber.email}")
            
            return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=true")
            
        except Subscriber.DoesNotExist:
            print("Invalid token")
            return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=false")