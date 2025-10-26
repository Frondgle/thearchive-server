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

            else:
                # Email already exists - check if confirmed
                if subscriber.is_confirmed:
                    print("Email already confirmed!")
                    # Don't send another email, they're already subscribed
                    
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

            # SAME MESSAGE FOR ALL SCENARIOS - prevents user enumeration
            return Response(
                {"success": True, "message": "Please check your email for confirmation instructions."},
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

            # Send welcome email with unsubscribe option
            try:
                unsubscribe_url = f"{settings.SITE_URL}/unsubscribe/unsubscribe/?token={subscriber.unsubscribe_token}"

                email_subject = "Welcome to The Sonatore Archive!"
                
                text_body = f"""
                    Welcome to The Sonatore Archive!

                    Your subscription has been confirmed. You'll now receive updates about new content, features, and announcements.

                    We're excited to have you as part of our community!

                    If you wish to unsubscribe at any time, click the following link: {unsubscribe_url}

                    Best regards,
                    The Sonatore Archive Team
                """
                
                html_body = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <h2 style="color: #2196F3;">Welcome to The Sonatore Archive!</h2>
                            
                            <p>Your subscription has been confirmed. You'll now receive updates about new content, features, and announcements.</p>
                            
                            <p>We're excited to have you as part of our community!</p>
                            
                            <p style="margin-top: 30px;">
                                <a href="{unsubscribe_url}" 
                                   style="background-color: #666; color: white; padding: 10px 20px; 
                                          text-decoration: none; border-radius: 4px; display: inline-block; font-size: 14px;">
                                    Unsubscribe
                                </a>
                            </p>
                            
                            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                                You can unsubscribe at any time by clicking the button above.
                            </p>
                            
                            <p>Best regards,<br>
                            The Sonatore Archive Team</p>
                        </body>
                    </html>
                """
                
                email_message = EmailMultiAlternatives(
                    subject=email_subject,
                    body=text_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email]
                )
                email_message.attach_alternative(html_body, "text/html")
                email_message.send(fail_silently=False)
                
                print(f"Welcome email sent to {subscriber.email}")
            except Exception as e:
                print(f"Welcome email error: {str(e)}")
            
            return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=true")
            
        except Subscriber.DoesNotExist:
            print("Invalid token")
            return redirect(f"{settings.SITE_URL}/subscriptionConfirmed/subscriptionConfirmed?success=false")