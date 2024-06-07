from django.urls import path
from .views import BlogView_For_User, BLogDisplay, CommentView
from django.urls.converters import UUIDConverter

urlpatterns = [
    path('user/blog/', BlogView_For_User.as_view(), name='user_blogs' ),
    path('blog/', BLogDisplay.as_view(), name = "blogs"),
    path('blog/<blog_uuid>/comments/', CommentView.as_view(), name = "comments"),    
]