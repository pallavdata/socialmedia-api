import numpy
from django.conf import settings
from rest_framework.permissions import BasePermission
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import *
from .serializers import RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# object detection
from tensorflow.keras.models import load_model
import cv2
import os
import numpy as np
# 3
#

# Create your views here.

def home(request):
    return render(request,"home.html")

def temp404(request):
    data = {
        "error 404": "the page you were looking for doesn't exist.",  
    }
    return render(request,"index.html",data,status=404)

class reg_staff_view(APIView):
    def post(self, request):
        first_name = request.data.get("first_name", False)
        last_name = request.data.get("last_name", False)
        username = request.data.get("username", False)
        email = request.data.get("email", False)
        password = request.data.get("password", False)
        password2 = request.data.get("password2", False)
        if not first_name or not last_name or not username or not email or not password or not password2:
            return Response({"errors": "first_name, last_name, username, email, password or password2 is missing"}, status=status.HTTP_404_NOT_FOUND)
        user = request.data
        serializer = RegistrationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_staff = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({"name": f"{first_name} {last_name}", "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)


class reg_view(APIView):
    def post(self, request):
        first_name = request.data.get("first_name", False)
        last_name = request.data.get("last_name", False)
        username = request.data.get("username", False)
        email = request.data.get("email", False)
        password = request.data.get("password", False)
        password2 = request.data.get("password2", False)
        if not first_name or not last_name or not username or not email or not password or not password2:
            return Response({"errors": ["first_name, last_name, username, email, password or password2 is missing"]}, status=status.HTTP_404_NOT_FOUND)
        user = request.data
        serializer = RegistrationSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({"name": f"{first_name} {last_name}", "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)


class follow_id_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if id == request.user.id:
            return Response({"error": "You can't follow yourself"}, status=status.HTTP_404_NOT_FOUND)
        try:
            following = User_access.objects.get(id=id)
        except:
            return Response({"error": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = Following_model.objects.get(
                accid=request.user, following=following)
            return Response({"error": "You are already following the user"}, status=status.HTTP_404_NOT_FOUND)
        except:
            data = Following_model(accid=request.user, following=following)
            data.save()
            return Response({"followed": f"{request.user.first_name} started following {following.first_name}"}, status=status.HTTP_200_OK)


class unfollow_id_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        if id == request.user.id:
            return Response({"error": "You can't follow / unfollow yourself"}, status=status.HTTP_404_NOT_FOUND)
        try:
            following = User_access.objects.get(id=id)
        except:
            return Response({"error": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = Following_model.objects.get(
                accid=request.user, following=following)
            data.delete()
            return Response({"followed": f"{request.user.first_name} unfollowed {following.first_name}"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "The action cannot be performed because you did not follow the user."}, status=status.HTTP_404_NOT_FOUND)


def follow(request):
    followers = Following_model.objects.filter(
        following=request.user).count()
    following = Following_model.objects.filter(accid=request.user).count()
    return {"name": f"{request.user.first_name} {request.user.last_name}"}, {"followers": followers}, {"following": following}


class user_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response([follow(request)], status=status.HTTP_200_OK)


class posts_view(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = (FileUploadParser,)

    def post(self, request):
        data = request.data
        file_path = os.path.join(
            settings.BASE_DIR, 'app', 'static2', 'detect', 'pistol_or_not_third_epoch100.h5')
        model = load_model(file_path)
        title_data = data.get('title', '')
        description_data = data.get('description', '')
        if title_data and description_data:
            file = request.FILES.get('image','')
            datasave = Post_model(accid=request.user, title=title_data, description=description_data)
            if not file == '':
                image = cv2.imdecode(numpy.frombuffer(
                    file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                if image is None:
                    return Response([{"warning - 1": "We can only take the following image formats", "formats": {"JPEG": "(.jpg, .jpeg, .jpe)", "PNG": "(.png)", "BMP": "(.bmp)", "TIFF": "(.tif, .tiff)", "WebP": "(.webp)", "PBM, PGM, PPM": "(.pbm, .pgm, .ppm)"}}, {"warning - 2": "File is corrupted"}], status=status.HTTP_404_NOT_FOUND)
                img_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                image_resize = cv2.resize(img_rgb, (120, 120))
                if not image_resize.shape == (120, 120, 3):
                    return Response({"error": "we cant process it"}, status=status.HTTP_404_NOT_FOUND)
                img_processed = image_resize / 255.0
                prediction = model.predict(np.array([img_processed]))
                if prediction > 0.75:
                    return Response({"error": "gun detected in the image"}, status=status.HTTP_404_NOT_FOUND)
                datasave.image = file
            datasave.save()
            saveresponse = [{"Post-ID": datasave.id}, {"Title": datasave.title}, {"Description": datasave.description},{
                "Created Time(UTC)": datasave.created.strftime("DD-MM-YYYY : " + "%d-%m-%Y"+" HH:MM : "+"%H:%M")}]
            try:
                saveresponse.append({"image": datasave.image.url})
            except:
                pass
            return Response(saveresponse, status=status.HTTP_200_OK)
        return Response({"error": " 'title' or 'description' or both is not specified"}, status=status.HTTP_404_NOT_FOUND)


class IsAuthenticatedOrDeleteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_authenticated
        return True


class posts_id_view(APIView):
    permission_classes = [IsAuthenticatedOrDeleteOnly]

    def delete(self, request, id):
        try:
            data = Post_model.objects.get(accid=request.user, id=id)
            data.delete()
            return Response([{"success": "Post is deleted"}, {"id": id}], status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            data = Post_model.objects.get(id=id)
            likes = Likes_model.objects.filter(postid=data).count()
            comments = Comment.objects.filter(postid=data).count()
            return Response([{"ID": id}, {"Likes": likes}, {"Comments": comments}], status.HTTP_200_OK)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class like_id_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            postdata = Post_model.objects.get(id=id)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = Likes_model.objects.get(
                accid=request.user, postid=postdata)
            if data.liked == False:
                data.liked = True
                data.save()
                return Response({f"You liked the post {id}"}, status=status.HTTP_200_OK)
            return Response({f"The action cannot be performed because you already liked the post."}, status=status.HTTP_200_OK)
        except:
            datasave = Likes_model(
                accid=request.user, postid=Post_model.objects.get(id=id), liked=True)
            datasave.save()
            return Response({f"You liked the post {id}"}, status=status.HTTP_200_OK)


class unlike_id_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            postdata = Post_model.objects.get(id=id)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = Likes_model.objects.get(accid=request.user, postid=postdata)
            data.delete()
            return Response({f"You unliked the post {id}"}, status=status.HTTP_200_OK)
        except:
            return Response({f"The action is not possible because you have not previously liked the post - {id}"}, status=status.HTTP_404_NOT_FOUND)


class comment_id_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            postdata = Post_model.objects.get(id=id)
        except:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        commentsave = request.data.get("comment", False)

        if not commentsave:
            return Response({"error": "Comment is empty"}, status=status.HTTP_404_NOT_FOUND)

        data = Comment(accid=request.user, postid=postdata,
                       comment=commentsave)
        data.save()
        return Response([{f"Comments have been saved for the post - {id}"}, {"Comment": commentsave}], status=status.HTTP_200_OK)


class all_posts_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_post = []
        for i in Post_model.objects.filter(accid=request.user):
            comment_text = i.comments.values_list('comment', flat=True)
            temp_post = {
                "id": i.id,
                "title": i.title,
                "desc": i.description,
                "created_at": i.created.strftime("DD-MM-YYYY : " + "%d-%m-%Y"+" HH:MM : "+"%H:%M"),
                "comments": list(comment_text),
                "likes": Likes_model.objects.filter(postid=i).count()
            }
            all_post.append(temp_post)
        return Response(all_post, status=status.HTTP_200_OK)


class all_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_post = []
        all_post.append(follow(request))
        for i in Post_model.objects.filter(accid=request.user):
            comment_text = i.comments.values_list('comment', flat=True)
            temp_post = {"post":
                         {
                             "id": i.id,
                             "title": i.title,
                             "desc": i.description,
                             "created_at": i.created.strftime("DD-MM-YYYY : " + "%d-%m-%Y"+" HH:MM : "+"%H:%M"),
                             "comments": list(comment_text),
                             "likes": Likes_model.objects.filter(postid=i).count()
                         }
                         }
            all_post.append(temp_post)
        return Response(all_post, status=status.HTTP_200_OK)

# def detect():
#     directory = 'C:/Users/hp/Desktop/tf'
#     filename = 'gun.jpg'
#     file_path = os.path.join(directory, filename)
#     image = cv2.imread('gun.jpg')
#     image_resize = cv2.resize(image, (120,120))
#     img_processed = image_resize / 255.0
#     prediction = model.predict(np.array([img_processed]))
#     print(prediction)

#     if prediction > 0.75:
#         print("The image contains a gun")
#     else:
#         print("others")
