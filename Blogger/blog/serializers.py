from rest_framework import serializers
from .models import  Blog, Comment


class BlogSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.username

    class Meta:
        model = Blog
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    comment_user = serializers.PrimaryKeyRelatedField(read_only=True)
    comment_blog = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_user_name(self, obj):
        return obj.comment_user.username

    class Meta:
        model = Comment
        fields = "__all__"

