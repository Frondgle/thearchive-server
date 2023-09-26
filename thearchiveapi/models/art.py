from django.db import models


class Art(models.Model):
    pic = models.ImageField(upload_to='pics/', null=True, blank=True)
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    color = models.BooleanField(default=True)
    frame_type = models.CharField(max_length=50)
    mods = models.BooleanField(default=False)
    date_created = models.IntegerField()
    film_type = models.CharField(max_length=50)
    malfunction = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        'Tag', through='ArtTag', related_name='art', blank=True)

    # @property
    # def circle_image(self):
    #     return CloudinaryImage(self.image.name).build_url(width=256, height=256, radius="max", gravity="faces", crop="fill", cloud_name=os.environ.get("CLOUD_NAME"))

    # @property
    # def is_complete(self):
    #     has_projects = self.projects.count()
    #     return bool(self.bio and has_projects and self.image)
