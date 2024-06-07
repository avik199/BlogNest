import uuid
from django.db import models
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4)
    class Meta:
        abstract = True

class Blog(BaseModel):    
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    images  = models.ImageField(upload_to="blogs")

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title

class Comment(BaseModel):
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="comments")
    comment_blog = models.ForeignKey(Blog, on_delete = models.CASCADE, related_name="comments")
    comment_content = models.TextField()
    comment_date_created = models.DateTimeField(auto_now_add=True)
    comment_date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['comment_date_created']

    def __str__(self):
        return f"Comment by {self.comment_user.username} on {self.comment_blog.title}"
    

