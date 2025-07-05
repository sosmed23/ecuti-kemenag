from django.urls import path
from . import views

urlpatterns = [
    # URL dari langkah sebelumnya
    path('ajukan/', views.ajukan_cuti, name='ajukan_cuti'),
    path('persetujuan/', views.daftar_persetujuan, name='daftar_persetujuan'),
    path('persetujuan/<int:pk>/', views.detail_persetujuan, name='detail_persetujuan'),
    path('persetujuan/<int:pk>/proses/', views.proses_persetujuan, name='proses_persetujuan'),

    # URL baru untuk alur persetujuan Kepala
    path('kepala/persetujuan/', views.daftar_persetujuan_kepala, name='daftar_persetujuan_kepala'),
    path('kepala/persetujuan/<int:pk>/', views.detail_persetujuan_kepala, name='detail_persetujuan_kepala'),
    path('kepala/persetujuan/<int:pk>/proses/', views.proses_persetujuan_kepala, name='proses_persetujuan_kepala'),

    # === URL BARU UNTUK HALAMAN INI ===
    path('riwayat/<int:pk>/', views.riwayat_detail, name='riwayat_detail'),
    path('surat/<int:pk>/cetak/', views.cetak_surat_cuti, name='cetak_surat_cuti'),
    path('ajukan/konfirmasi/', views.konfirmasi_pengajuan, name='konfirmasi_pengajuan'),
    path('ajax/hitung-cuti/', views.hitung_lama_cuti_ajax, name='hitung_cuti_ajax'),
    path('laporan/', views.laporan_cuti, name='laporan_cuti'),
]
