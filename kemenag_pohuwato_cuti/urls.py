# File: kemenag_pohuwato_cuti/urls.py
# PERBAIKAN FINAL: Memastikan semua URL terhubung dengan benar

from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <-- Impor baru
from django.conf.urls.static import static # <-- Impor baru

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
    
    # Semua URL yang tidak cocok dengan pola di atas (termasuk halaman utama)
    # akan ditangani oleh aplikasi 'users'.
    # Ini membuat /login, /logout, dan /dashboard bisa diakses dari root.
    # Dan halaman utama http://127.0.0.1:8000/ akan otomatis mengarah ke login.
    path('laporan/', include('laporan.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
