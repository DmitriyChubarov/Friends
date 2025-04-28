from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^login/',views.login_view, name='login'),
        url(r'^possible/(?P<user_id>\d+)/$',views.send_prop, name='send_prop'),
        url(r'^possible/',views.possible_view, name='possible'),
        url(r'^register/',views.register_view, name='register'),
        url(r'^profile/accept_req/(?P<user_id>\d+)/$',views.accept_req, name='accept_req'),
        url(r'^profile/reject_req/(?P<user_id>\d+)/$',views.reject_req, name='reject_req'),
        url(r'^profile/delete_friend/(?P<user_id>\d+)/$',views.delete_friend, name='delete_friend'),
        url(r'^profile/',views.profile_view, name='profile'),
        url(r'^logout/',views.LogoutView.as_view(), name='logout'),
]
