from django.urls import path

from .views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_password_update_view,
    UserCreateView,
    UserListView
)

app_name = "users"
urlpatterns = [
    path("create/", view=UserCreateView.as_view(), name="user-create"),
    path("list/", view=UserListView.as_view(), name="user-list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    path("<str:pk>/update/", view=user_update_view, name="update"),
    path("<str:pk>/update/password", view=user_password_update_view, name="password_update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
