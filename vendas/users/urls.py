from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from rest_framework import routers
from django.conf import settings


from . import views

urlpatterns = [
	# view de login
	path('login/',auth_views.LoginView.as_view(),name='login'),
	path('logout/',auth_views.LogoutView.as_view(),name='logout'),
	path('',views.dashboard,name='dashboard'),
	# urls para alteração de senha
	path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
	path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
	# urls para reiniciar a senha
	path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
	path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
	path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
	# url de cadastro de usuários
	path('register/',views.register,name='register'),
	path('list_user/',views.list,name='seguranca'),
	path('<int:pk>/',views.detalhe_usuario,name='detalhe de usuario'),
	path('detalhe/<int:pk>/',views.detalhe_usuario,name='detalhe de usuario'),
	path('registrar/',views.criacao_conta,name="nova conta"),
#	path('register/done',views.register_done,name='register_done'),
	path('camera',views.camera,name='camera'),
	path('login_camera',views.login_camera,name='login_camera'),
	# url de alteração de cadastro
	path('edit/',views.edit,name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
