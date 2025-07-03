# File: kemenag_pohuwato_cuti/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ==================== KODE KUSTOMISASI ADMIN ====================
admin.site.site_header = "Admin E-Cuti Kemenag Pohuwato"
admin.site.site_title = "Portal Admin E-Cuti"
admin.site.index_title = "Selamat Datang di Portal Admin E-Cuti"
# =============================================================

urlpatterns = [
    # URL untuk Halaman Admin Django
    path('admin/', admin.site.urls),
    
    # Semua URL yang berawalan 'cuti/' akan ditangani oleh aplikasi 'cuti'
    # Contoh: /cuti/ajukan/, /cuti/persetujuan/
    path('cuti/', include('cuti.urls')),
    
    # (Opsional) Jika Anda punya aplikasi laporan terpisah
    # path('laporan/', include('laporan.urls')),
    
    # Semua URL yang tidak cocok dengan pola di atas (termasuk halaman utama)
    # akan ditangani oleh aplikasi 'users'.
    # Ini membuat /login, /logout, dan /dashboard bisa diakses dari root.
    path('', include('users.urls')),
]

# Konfigurasi untuk menampilkan file media saat development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)