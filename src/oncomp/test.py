from django.test import testcases
from . import models
from django.conf import settings
class compilertestcase(testcases):
   def delete(self):
        models.compilertestscore.objects.delete()

   def insert(self):
       self.delete()
       models.canswer.objects.create("")