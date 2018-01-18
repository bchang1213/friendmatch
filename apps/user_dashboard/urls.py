from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^gosignin$', views.gosignin),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^goregister$', views.goregister),
	url(r'^register$', views.register),
	url(r'^dashboard$', views.dashboard),
	url(r'^addnewuser$', views.addnewuser),
	url(r'^users/(?P<user_id>\d+)/upload_file$', views.upload_file),
	url(r'^users/(?P<user_id>\d+)/post_message$', views.post_message),
	url(r'^users/(?P<user_id>\d+)$', views.show, name = 'show_user'),
	url(r'^users/(?P<user_id>\d+)/comments$', views.comments),
	url(r'^edit/(?P<user_id>\d+)$', views.edit_user),
	url(r'^edit/(?P<user_id>\d+)/save_edits$', views.save_edits),
	url(r'^remove/(?P<user_id>\d+)$', views.removeuser),
	# url(r'^(?P<user_id>\d+)/success$', views.success, name = 'success'),
  ]