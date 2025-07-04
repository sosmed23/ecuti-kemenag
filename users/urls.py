from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Jadikan halaman login sebagai halaman utama (root) dengan path kosong ''
    # Nama 'login' tetap sama agar semua link yang ada tetap berfungsi.
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # URL untuk proses logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # URL untuk dashboard pegawai
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # URL untuk profil pengguna
    path('profile/', views.edit_profile, name='edit_profile'),
    
    # URL untuk halaman ganti password
    # path('ganti-password/', views.ganti_password_pertama_kali, name='ganti_password'),
]