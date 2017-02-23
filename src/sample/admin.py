from django.contrib import admin
from sample import models
# Register your models here.
admin.site.register(models.Tests)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.Correct)
admin.site.register(models.compilerquestion)

