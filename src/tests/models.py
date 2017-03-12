from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from datetime import timedelta,datetime
# Create your models here.
class Apt_Test(models.Model):
   time = models.DurationField(default="1:00:00")
   name = models.CharField(max_length=100)
   startDate = models.DateTimeField(default=(datetime.now()+timedelta(days=1)))
   endDate=models.DateTimeField(default=datetime.now)

   def __str__(self):
       return self.name

class Apt_Qns(models.Model):
    question = models.TextField()
    test_id = models.ForeignKey(Apt_Test,on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answers(models.Model):
    answer = models.CharField(max_length=300)
    qn_id = models.ForeignKey(Apt_Qns,on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

class Correct(models.Model):
    ans_id = models.ForeignKey(Answers, on_delete=models.CASCADE)
    qn_id = models.ForeignKey(Apt_Qns, on_delete=models.CASCADE)


class Testscore(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    test=models.ForeignKey(Apt_Test,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    question=models.IntegerField(default=1)
    itime=models.DurationField(default=timedelta(hours=1))
    def _str_(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email


def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Testscore.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_reciever, sender=settings.AUTH_USER_MODEL)