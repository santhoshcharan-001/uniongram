from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
# Create your views here.
from .models import posts,comments,likes,follows

from rest_framework.views import APIView
from .serializers import postSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
# import override_action
from .submit_code import startAutomate

class PostViewSet(viewsets.ModelViewSet):
    queryset = posts.objects.all()
    serializer_class = postSerializer
    permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            serializer = postSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["user"] = request.user
                serializer.save()
                # Post-ID, Title, Description, Created Time(UTC)
                # print(serializer.data['id'])
                return JsonResponse({"Response":{"Post-ID":serializer.data['id'],"Title":serializer.data["title"],"Description":serializer.data["content"],"Created Time(UTC)":serializer.data["time_stamp"]}})
        except:
            return Response("Error creating the post")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response("You are not authorized to delete this post")
        # print(instance.user)
        self.perform_destroy(instance)
        return JsonResponse({"Response":"Post deleted successfully"})

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        try:
            postes= posts.objects.filter(user=request.user)
            serializer = postSerializer(postes, many=True)
            return Response(serializer.data)
        except:
            return Response("Error listing the posts")
            
class addLike(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,post_id):
        user = User.objects.get(username=request.user.username)
        post = posts.objects.get(id=post_id)
        if post is None:
            return JsonResponse({"Response":"Post not found"})
        l=likes.objects.filter(post_id=post,user=user)
        if len(l) ==0:
            post.like_count += 1
            post.save()
            like = likes.objects.create(post_id=post, user=user,time_stamp=datetime.now())
            like.save()
            return JsonResponse({"Response":"Liked it"})
        else:
            return JsonResponse({"Response":"User has already liked it"})

    def get(self,request,post_id):
        return JsonResponse({"Response":"Get type is not allowed"})


class UnLike(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,post_id):
        user = User.objects.get(username=request.user.username)
        post = posts.objects.get(id=post_id)
        if post is None:
            return JsonResponse({"Response":"Post not found"})
        l=likes.objects.filter(post_id=post,user=user)
        if len(l) != 0:
            post.like_count -= 1
            post.save()
            # like = likes.objects.create(post_id=post, user=user,time_stamp=datetime.now())
            l.delete()
            return JsonResponse({"Response":"Unliked it"})
        else:
            return JsonResponse({"Response":"User haven't liked it till now."})

    def get(self,request,post_id):
        return JsonResponse({"Response":"Get type is not allowed"})


class follow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        follow_user = User.objects.get(id=user_id)
        if follow_user is None:
            return JsonResponse({"Response":"User you want to follow not found"})
        user = User.objects.get(username=request.user.username)
        if user == follow_user:
            return JsonResponse({"Response":"You can't follow yourself"})
        f=follows.objects.filter(followee=follow_user,follower=user)
        if len(f) == 0:
            follow = follows.objects.create(followee=follow_user, follower=user,time_stamp=datetime.now())
            follow.save()
            return JsonResponse({"Response":"Followed"})
        else:
            return JsonResponse({"Response":"User has already followed it"})

    def get(self,request,username):
        return JsonResponse({"Response":"Get type is not allowed"})


class unfollow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        follow_user = User.objects.get(id=user_id)
        user = User.objects.get(username=request.user.username)
        if follow_user is None:
            return JsonResponse({"Response":"User you want to unfollow not found"})
        f=follows.objects.filter(followee=follow_user,follower=user)
        if len(f) != 0:
            f.delete()
            return JsonResponse({"Response":"Unfollowed"})
        else:
            return JsonResponse({"Response":"User haven't followed that user till now."})

    def get(self,request,username):
        return JsonResponse({"Response":"Get type is not allowed"})


class user_details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        followers = len(follows.objects.filter(followee=user))
        following = len(follows.objects.filter(follower=user))
        return Response({"Response":{"username":user.username,"email":user.email,"followers":followers,"following":following}})
    def post(self,request):
        return JsonResponse({"Response":"Post type is not allowed"})

class addComment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,post_id):
        try:
            user = User.objects.get(username=request.user.username)
            post = posts.objects.get(id=post_id)
            if post is None:
                return JsonResponse({"Response":"Post not found"})
            post.comment_count += 1
            post.save()
            comment = comments.objects.create(post=post, user=user,content=request.data["comment"],time_stamp=datetime.now())
            comment.save()
            return Response({"Response":"Commented","Comment-id":comment.id})
        except:
            return Response("Error creating the comment")
    def get(self,request,post_id):
        return JsonResponse({"Response":"Get type is not allowed"})

class deleteComment(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,comment_id):
        try:
            user = User.objects.get(username=request.user.username)
            comment = comments.objects.get(id=comment_id)
            if comment is None:
                return JsonResponse({"Response":"Comment not found"})
            if comment.user == user:
                comment.delete()
                comment.post.comment_count -= 1
                comment.post.save()
                return Response({"Response":"Comment Deleted"})
            else:
                return Response({"Response":"You are not authorized to delete this comment"})
        except:
            return Response("Error deleting the comment")
    def get(self,request,comment_id):
        return JsonResponse({"Response":"Get type is not allowed"})

class user_posts(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = User.objects.get(username=request.user.username)
        dic={}
        postes = posts.objects.filter(user=user).order_by('-time_stamp', '-id')
        for post in postes:
            commentes=[]
            comms = comments.objects.filter(post=post, user=user)
            for com in comms:
                commentes.append({"content":com.content,"time_stamp":com.time_stamp})
            dic[post.id] = {"title":post.title,"content":post.content,"like_count":post.like_count,"comment_count":post.comment_count,"created_at":post.time_stamp,"comments":commentes}
        # serializer = postSerializer(posts,many=True)
        return Response({"Response":dic})

    def post(self,request):
        return JsonResponse({"Response":"Post type is not allowed"})


def submitCode(request):
    startAutomate()
    logs=""
    x=open("./profileapp/logs.txt","r")
        # logs=files.read()
    return JsonResponse({"logs":x.read()})