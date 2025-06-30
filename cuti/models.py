# Pembaruan: cuti/models.py
# PERBAIKAN FINAL: Memastikan semua class terdefinisi dengan benar

from django.db import models
from users.models import User

class JenisCuti(models.Model):
    # Definisikan pilihan peruntukan
    BERLAKU_UNTUK_CHOICES = [
        ('SEMUA', 'Semua (PNS & PPPK)'),
        ('PNS', 'Hanya PNS'),
        ('PPPK', 'Hanya PPPK'),
    ]

    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=10, unique=True)

    berlaku_untuk = models.CharField(
        max_length=5, 
        choices=BERLAKU_UNTUK_CHOICES, 
        default='SEMUA', 
        verbose_name="Berlaku Untuk"
    )
    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural = "Daftar Jenis Cuti"

class SaldoCutiTahunan(models.Model):
    pegawai = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saldo_cuti")
    tahun = models.PositiveIntegerField()
    sisa_hari = models.PositiveIntegerField(default=12)
    class Meta:
        unique_together = ('pegawai', 'tahun')
        verbose_name_plural = "Data Saldo Cuti Tahunan"
    def __str__(self):
        return f"Saldo Cuti {self.pegawai.get_full_name()} ({self.tahun}): {self.sisa_hari} hari"

class PengajuanCuti(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING_ATASAN', 'Menunggu Persetujuan Atasan'),
        ('PENDING_KEPALA', 'Menunggu Keputusan Kepala'),
        ('DISETUJUI', 'Disetujui'),
        ('DITOLAK_ATASAN', 'Ditolak oleh Atasan'),
        ('DITOLAK_KEPALA', 'Ditolak oleh Kepala'),
        ('PERUBAHAN', 'Disarankan Perubahan'),
        ('DITANGGUHKAN', 'Ditangguhkan'),
    ]
    pegawai = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pengajuan')
    jenis_cuti = models.ForeignKey(JenisCuti, on_delete=models.PROTECT)
    alasan = models.TextField()
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    lama_cuti = models.PositiveIntegerField(help_text="Jumlah hari kerja")
    alamat_selama_cuti = models.TextField()
    telepon_selama_cuti = models.CharField(max_length=15)

    dokumen_pendukung = models.FileField(
        upload_to='dokumen_cuti/', 
        null=True, 
        blank=True, 
        verbose_name="Dokumen Pendukung (jika ada)"        
    )
    tanda_tangan_pegawai = models.TextField(
        null=True, blank=True, verbose_name="Tanda Tangan Pegawai (Data URL)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_ATASAN')
    created_at = models.DateTimeField(auto_now_add=True)
    atasan_penyetuju = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='persetujuan_atasan')
    catatan_atasan = models.TextField(blank=True, null=True)
    tanggal_pertimbangan_atasan = models.DateTimeField(null=True, blank=True)
    kepala_penyetuju = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='persetujuan_kepala')
    catatan_kepala = models.TextField(blank=True, null=True)
    tanggal_keputusan_kepala = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Cuti ({self.jenis_cuti.kode}) a.n. {self.pegawai.get_full_name()}"
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Data Pengajuan Cuti"

# === KODE YANG DIPERBAIKI ===
class HariLibur(models.Model):
    """
    Model untuk menyimpan tanggal hari libur nasional atau cuti bersama
    yang bisa diatur oleh Admin.
    """
    # Indentasi yang benar
    tanggal = models.DateField(unique=True)
    keterangan = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tanggal.strftime('%d %B %Y')} - {self.keterangan}"
        
    class Meta:
        verbose_name_plural = "Daftar Hari Libur"
        ordering = ['tanggal']