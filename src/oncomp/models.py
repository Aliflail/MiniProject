from __future__ import unicode_literals
from tests import models as tmodels
from django.db import models
from django.conf import settings
from datetime import timedelta
class Compilerquestion(models.Model):
    prog = models.TextField(default="")
    pname = models.CharField(max_length=256)
    mark = models.IntegerField(default=0)
    test_id =models.ForeignKey(tmodels.Apt_Test,on_delete=models.CASCADE)
    time=models.DurationField(default="0:30:00")

    def __str__(self):
        return self.pname
class CompilerTestcases(models.Model):
    testcases=models.TextField(max_length=500)
    test_out = models.TextField(max_length=1000, default='No Output')
    question_id = models.ForeignKey(Compilerquestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_out


class canswer(models.Model):
    uid=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    tid=models.ForeignKey(tmodels.Apt_Test,on_delete=models.CASCADE)
    qid = models.ForeignKey(Compilerquestion,on_delete=models.CASCADE)
    out=models.TextField(default="")
    program=models.CharField(max_length=15000,default="Enter Your Program Here")
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('java', 'Java'),
        ('c_cpp', 'C++'),
        ('javascript', 'Javascript'),
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='python',
    )


    def __str__(self):
        return self.program

class compilertestscore(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    test=models.ForeignKey(tmodels.Apt_Test,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    question=models.ForeignKey(Compilerquestion,models.CASCADE)
    itime=models.DurationField(default=timedelta(hours=1))
    def _str_(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email
