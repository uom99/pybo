from django.db import models
from django.contrib.auth.models import User

class question(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') #추천인
    def __str__(self):
        return self.subject

class answer(models.Model):
  modify_date = models.DateTimeField(null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
  question = models.ForeignKey(question, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField()
  modify_date= models.DateTimeField(null=True, blank=True)
  voter = models.ManyToManyField(User, related_name='voter_answer')

  def __str__(self):
    return self.content
