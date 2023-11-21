from django.urls import path
from .views import Home,UserSignIn,LoginUser,Profile,NewPost,ReadMore,ViewProfile,EditPost,EditProfile
from . import views
urlpatterns= [
path('',Home.as_view(),name = 'home'),
path('auth/signin',UserSignIn.as_view(),name ='user_signin'),
path('user/logout',views.logut_user,name= 'logout'),
path('auth/login',LoginUser.as_view(),name ='login'),
path('user/profile',Profile.as_view(),name = 'profile'),
path('user/newpost',NewPost.as_view(),name ='newpost'),
path('post/readmore/<int:id>',ReadMore.as_view(),name='readmore'),
path('viewprofile/',ViewProfile.as_view(),name = 'viewprofile'),
path('posts/delete/<int:id>',views.delete_post,name = 'deleteposts'),
path('posts/edit/<int:id>',EditPost.as_view(),name = 'editpost'),
path('user/profile/edit/<int:id>',EditProfile.as_view(),name = 'editprofile')
] 
