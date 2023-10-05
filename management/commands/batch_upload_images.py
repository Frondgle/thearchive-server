import os
from django.core.management.base import BaseCommand
import cloudinary
from cloudinary import api
from thearchiveapi.models import Art

class Command(BaseCommand):
    # python manage.py batch_upload_images
    help = 'Batch upload images from Cloudinary'

    def handle(self, *args, **options):
        # Initialize Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )

        # Fetch images from Cloudinary (e.g., using tags)
        cloudinary_images = api.resources(
            type='upload',
            tags='your_tag',  # Specify your criteria
            max_results=100  # Adjust as needed
        )

        # Iterate through Cloudinary images and create Art objects
        for cloudinary_image in cloudinary_images['resources']:
            # Create an Art object and populate its fields
            art = Art(
                title=cloudinary_image['public_id'],  # Use a relevant identifier
                description=cloudinary_image.get('context', {}).get('description', ''),
                pic=cloudinary_image[os.environ.get('CLOUDINARY_URL')]  # Use the Cloudinary URL
            )

            # Save the Art object to the Django database
            art.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {art.title}'))

        self.stdout.write(self.style.SUCCESS('Batch image upload complete'))
