from PIL import Image
from django.db import models
from .utils import get_filtered_image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.

ACTION_CHOICES = (
    ('NO_FILETER', 'no_filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert')
)

class Upload(models.Model):
    image = models.ImageField(upload_to = 'images',)
    action = models.CharField(max_length = 60, choices = ACTION_CHOICES)
    update = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        #open image
        pil_image = Image.open(self.image)

        #convert the image to array and do some processing

        cv_image = np.array(pil_image)
        image_filtered = get_filtered_image(cv_image, self.action)

        #convert back to pill
        im_pil = Image.fromarray(image_filtered)

        #save
        buffer = BytesIO()
        im_pil.save(buffer, format= 'png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), ContentFile(image_png),save = False)
        super().save(*args, **kwargs)