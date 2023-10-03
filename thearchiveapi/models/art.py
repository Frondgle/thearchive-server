from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy
from .tag import Tag


class Art(models.Model):
    # pic = models.ImageField(upload_to='pics/', null=True, blank=True)
    pic = CloudinaryField('pic', folder='the-archive/')
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    color = models.BooleanField(default=True)
    frame_type = models.CharField(max_length=50)
    mods = models.BooleanField(default=False)
    date_created = models.DateField()
    film_type = models.CharField(max_length=50)
    malfunction = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        Tag, through='ArtTag', related_name='art', blank=True)


    def delete(self, *args, **kwargs):
        # Delete the Cloudinary image associated with this Art object
        if self.pic:
            # include folder name in the public_id
            open_id = f'the-archive/{self.pic.public_id}'
            destroy(open_id)
            #destroy(self.pic.public_id)
        super(Art, self).delete(*args, **kwargs)

    # @property
    # def circle_image(self):
    #     return CloudinaryImage(self.image.name).build_url(width=256,
    #               height=256, radius="max", gravity="faces",
    #               crop="fill", cloud_name=os.environ.get("CLOUD_NAME"))

    # @property
    # def is_complete(self):
    #     has_projects = self.projects.count()
    #     return bool(self.bio and has_projects and self.image)
