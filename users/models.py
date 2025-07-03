# File: users/models.py
# PERBAIKAN FINAL: Memastikan method __str__ benar untuk setiap kelas.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Manager kustom untuk model User kita, dimana NIP adalah
    pengenal unik untuk otentikasi, bukan username.
    """
    def create_user(self, nip, password, **extra_fields):
        if not nip:
            raise ValueError('NIP harus diisi')
        user = self.model(nip=nip, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nip, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True.')
        return self.create_user(nip, password, **extra_fields)


class User(AbstractUser):
    username = None 
    nip = models.CharField(max_length=18, unique=True, verbose_name="NIP")

    wajib_ganti_password = models.BooleanField(default=True)

    USERNAME_FIELD = 'nip' 
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    # ==================== KODE __str__ YANG BENAR UNTUK USER ====================
    # 'self' di sini adalah objek User, jadi kita bisa langsung memanggil metodenya.
    def __str__(self):
        return self.get_full_name() or self.nip
    
    class Meta:
        verbose_name = "Pengguna"
        verbose_name_plural = "Daftar Pengguna"
    # =========================================================================


class Jabatan(models.Model):
    nama_jabatan = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_jabatan

    class Meta:
        verbose_name_plural = "Daftar Jabatan"


class Profile(models.Model):
    STATUS_CHOICES = [
        ('PNS', 'PNS'),
        ('PPPK', 'PPPK'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, blank=True)
    status_kepegawaian = models.CharField(
        max_length=4, 
        choices=STATUS_CHOICES, 
        default='PNS', 
        verbose_name="Status Kepegawaian"
    )
    atasan_langsung = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='bawahan')
    masa_kerja_tahun = models.PositiveIntegerField(default=0, verbose_name="Masa Kerja (Tahun)")
    masa_kerja_bulan = models.PositiveIntegerField(default=0, verbose_name="Masa Kerja (Bulan)")
    no_telepon = models.CharField(max_length=15, blank=True)

    # ==================== FIELD BARU DITAMBAHKAN DI SINI ====================
    # Admin bisa mengubah nilai default ini di halaman admin.
    sisa_cuti_sakit = models.PositiveIntegerField(
        default=14, verbose_name="Sisa Cuti Sakit (Hari)"
    )
    sisa_cuti_melahirkan = models.PositiveIntegerField(
        default=90, verbose_name="Sisa Cuti Melahirkan (Hari)"
    )
    sisa_cuti_alasan_penting = models.PositiveIntegerField(
        default=7, verbose_name="Sisa Cuti Alasan Penting (Hari)"
    )
    # =====================================================================

    # ================== KODE __str__ YANG BENAR UNTUK PROFILE ==================
    # 'self' di sini adalah objek Profile, jadi kita perlu akses 'self.user' dulu.
    def __str__(self):
        return self.user.get_full_name() or self.user.nip
    # =========================================================================

