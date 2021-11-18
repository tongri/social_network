from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from posts.views import CreateAuth, PostCreateAPIView, LikeViewSet, JWTTokenObtain, UserActivityRetrieveListViewSet

router = routers.SimpleRouter()
router.register(r'like', LikeViewSet)
router.register(r'users_activity', UserActivityRetrieveListViewSet)

urlpatterns = [
    path('signup/', CreateAuth.as_view()),
    path('token/', JWTTokenObtain.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('post/', PostCreateAPIView.as_view()),
    *router.urls
]
