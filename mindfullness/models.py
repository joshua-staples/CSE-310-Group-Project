from django.db import models
import json
from mindfullness.static import static
# Create your models here.
class rand_quotes(models.Model):
    f = open(static.relax.json)
    json_object = json.load(f)
