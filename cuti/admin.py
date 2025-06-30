from django.contrib import admin
from .models import JenisCuti, SaldoCutiTahunan, PengajuanCuti, HariLibur

@admin.register(JenisCuti)
class JenisCutiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode', 'berlaku_untuk')
    list_filter = ('berlaku_untuk',)
@admin.register(SaldoCutiTahunan)
class SaldoCutiTahunanAdmin(admin.ModelAdmin):
    list_display = ('pegawai', 'tahun', 'sisa_hari')
    list_filter = ('tahun', 'pegawai')
    search_fields = ('pegawai__first_name', 'pegawai__last_name', 'pegawai__nip')

@admin.register(PengajuanCuti)
class PengajuanCutiAdmin(admin.ModelAdmin):
    list_display = ('pegawai', 'jenis_cuti', 'tanggal_mulai', 'status')
    list_filter = ('status', 'jenis_cuti', 'created_at')
    search_fields = ('pegawai__first_name', 'pegawai__last_name', 'pegawai__nip')
    readonly_fields = ('created_at',)

@admin.register(HariLibur)
class HariLiburAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'keterangan')
    search_fields = ('keterangan',)