# File: kemenag_pohuwato_cuti/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL untuk Halaman Admin Django
    path('admin/', admin.site.urls),
    
    # Semua URL yang berawalan 'cuti/' akan ditangani oleh aplikasi 'cuti'
    # Contoh: /cuti/ajukan/, /cuti/persetujuan/
    path('cuti/', include('cuti.urls')),
    
    # Semua URL yang tidak cocok dengan pola di atas (termasuk halaman utama)
    # akan ditangani oleh aplikasi 'users'.
    # Ini membuat /login, /logout, dan /dashboard bisa diakses dari root.
    path('', include('users.urls')),
]

# Konfigurasi untuk menampilkan file media saat development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)