from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
from thearchiveapi.models import ContactMessage


@method_decorator(csrf_exempt, name='dispatch')
class ContactMessageView(View):
    
    def post(self, request):
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Extract fields
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            content = data.get('content', '').strip()
            
            # Validate required fields
            if not name:
                return JsonResponse({
                    'success': False,
                    'message': 'Name is required.'
                }, status=400)
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'message': 'Message is required.'
                }, status=400)
            
            # Validate email format if provided
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid email format.'
                    }, status=400)
            
            # Create and save ContactMessage
            contact_message = ContactMessage(
                name=name,
                email=email if email else None,
                content=content
            )
            contact_message.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Message sent successfully!'
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data.'
            }, status=400)
            
        except Exception as e:
            # Log the error for debugging
            print(f"Error saving contact message: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again later.'
            }, status=500)