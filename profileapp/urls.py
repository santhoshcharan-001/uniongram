from django.urls import path
from .views import PostViewSet
from .views import addLike,UnLike
from .views import unfollow,follow,user_details
from .views import addComment,deleteComment
from .views import user_posts
from rest_framework_simplejwt import views as jwt_views

# from .views import UnlikeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='posts')
# router.register(r'api/like', addLike.as_view(), basename='like')
# router.register(r'api/unlike', UnlikeViewSet, basename='unlike')
# router.register(r'posts/<str:text>', PostViewSet, basename='posts')


urlpatterns = [
    path('api/like/<str:post_id>',addLike.as_view()),
    path('api/unlike/<str:post_id>',UnLike.as_view()),
    path('api/follow/<str:user_id>',follow.as_view()),
    path('api/unfollow/<str:user_id>',unfollow.as_view()),
    path('api/authenticate',jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/user',user_details.as_view()),
    path('api/comment/<str:post_id>',addComment.as_view()),
    path('api/all_posts',user_posts.as_view()),
    # additional endpoint
    path('api/deletecomment/<str:comment_id>',deleteComment.as_view()),
    # path('api/posts/',PostViewSet.as_view({"post":"create"})),
    # path('api/posts/<str:text>',PostViewSet.as_view({"delete":"destroy"}))
    # path('/api/authenticate',user_authenticate, name='authenticate'),
] + router.urls