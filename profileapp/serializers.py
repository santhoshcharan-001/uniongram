from rest_framework import serializers
from .models import posts,likes

class userSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

# class postdestroySerializer(serializers.Serializer):
#     post_id = serializers.CharField(max_length=200)

class postSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = ['user','title','content','time_stamp','like_count','comment_count']
        read_only_fields = ['user','time_stamp','like_count','comment_count']

# class likeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = likes
#         fields = '__all__'
#         read_only_fields = ['user']