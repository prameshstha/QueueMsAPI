from .views import RegistrationView, Login, Logout, UserListUpdateDelete, AllUsersList, GetAvailableDoc

from django.urls import path


urlpatterns = [
    path('login/', Login.as_view(), name='login-token'),  # post request only - login
    path('logout/', Logout.as_view(), name='logout-token'),  # post request only
    path('register/', RegistrationView.as_view(), name='register-token'),  # post request only
    path('user-list/', AllUsersList.as_view(), name='user-list'),  # get request only
    path('doc-list/', GetAvailableDoc.as_view(), name='doc-list'),  # get request only
    # patch and delete request only -(all edit of users and delete)
    path('user-edit-delete/<str:email>/', UserListUpdateDelete.as_view(), name='user-edit-delete'),

]