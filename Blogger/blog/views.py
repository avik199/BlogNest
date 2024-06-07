import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializers, CommentSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog, Comment
from django.db.models import Q  
from django.core.exceptions import ObjectDoesNotExist


class BlogView_For_User(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #####################  post comment ########################
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id  # Include the authenticated user's ID in the data
            serializer = BlogSerializers(data=data)
            if not serializer.is_valid():
                return Response({'data': serializer.errors, 'message': 'Something went wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Blog created successfully!!!'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data': '', 'message': 'Something went wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)


    #################### retrive comment for each user ############### 
    def get(self, request):
        try:
            blog = Blog.objects.filter(user = request.user)
            
            #search feature to search for particular blog of a user
            if request.GET.get('search'):    
                search = request.GET.get('search')
                blog = blog.filter(Q(title__icontains = search) | Q(content__icontains = search))
            #####################################


            serializer = BlogSerializers(blog, many=True)
            return Response({'data': serializer.data, 'message': 'Blog fetched!!!'},  status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data': '', 'message': 'something went wrong!!!'},status=status.HTTP_400_BAD_REQUEST)
    

    ###########################  delete comment #####################
    '''def delete(self, request, blog_uuid):
        if not blog_uuid:
            return Response({'data': '', 'message': 'Blog ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert blog_uuid to a UUID object
            blog_id = uuid.UUID(blog_uuid)
            blog = Blog.objects.get(uid=blog_id)
            if request.user != blog.user:
                return Response({'data': '', 'message': 'Not authorised'}, status=status.HTTP_400_BAD_REQUEST)
            blog.delete()
            return Response({'data': '', 'message': 'Blog deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except (ValueError, ObjectDoesNotExist):
            return Response({'data': '', 'message': 'Blog does not exist'}, status=status.HTTP_400_BAD_REQUEST)'''

    def delete(self, request):
        data = request.data
        uid = data.get('uid')
        if uid is None:
            return Response({'data': '', 'message': 'Invalid uid!'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            blog = Blog.objects.get(uid=uid)
            if request.user == blog.user:
                blog.delete()
                return Response({'data': {}, 'message': 'Blog deleted successfully!!!'}, status=status.HTTP_200_OK)
            else:
                return Response ({'data': '', 'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Blog.DoesNotExist:
            return Response({'data': '', 'message': 'Invalid blog!!!'},status=status.HTTP_400_BAD_REQUEST)



        
    #############################  update blog ##########################
    def patch(self, request):
        try:
            data=request.data
            blog = Blog.objects.get(uid=data.get('uid'))

            if request.user == blog.user:
                serializer = BlogSerializers(blog,data = data, partial = True)
            else:
                return Response ({'data': '', 'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'message': 'Blog updated successfully!!!'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': '', 'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
            return Response({'data': '', 'message': 'something went wrong!!!'},status=status.HTTP_400_BAD_REQUEST)
        

        
####################  display blog for all ##########################3
class BLogDisplay(APIView):
    def get(self, request):
        try:
            blog = Blog.objects.all()
            
            #search feature to search for particular blog of a user
            if request.GET.get('search'):    
                search = request.GET.get('search')
                blog = blog.filter(Q(title__icontains = search) | Q(content__icontains = search))
            #####################################


            serializer = BlogSerializers(blog, many=True)
            return Response({'data': serializer.data, 'message': 'Blog fetched!!!'},  status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'data': '', 'message': 'something went wrong!!!'},status=status.HTTP_400_BAD_REQUEST)
        

######################################################   comment section   ##############        

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, blog_uuid=None):
        # Check for blog_uuid
        if not blog_uuid:
            return Response({'data': '', 'message': 'Blog ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert blog_uuid to a UUID object
            blog_id = uuid.UUID(blog_uuid)
            blog = Blog.objects.get(uid=blog_id)
        except (ValueError, ObjectDoesNotExist):
            return Response({'data': '', 'message': 'Blog does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'data': serializer.errors, 'message': 'Something went wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(comment_user=request.user, comment_blog=blog)
        return Response({'data': serializer.data, 'message': 'Comment created successfully!!!'}, status=status.HTTP_201_CREATED)
