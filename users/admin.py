# File: users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Jabatan

# --- Inline Profile (Untuk ditampilkan di dalam halaman User) ---
# Ini akan memastikan form Profile muncul saat menambah atau mengedit User.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Pegawai'
    fk_name = 'user'
    # Tampilkan semua field yang relevan untuk diisi
    fields = ('jabatan', 'status_kepegawaian', 'atasan_langsung', 'no_telepon', 'masa_kerja_tahun', 'masa_kerja_bulan')


class CustomUserAdmin(UserAdmin):
    model = User
    
    # Menampilkan formulir Profile di dalam halaman User
    inlines = (ProfileInline, )
    
    # Mengatur tampilan daftar pengguna
    list_display = ('get_full_name_custom', 'nip', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('nip', 'first_name', 'last_name')
    ordering = ('nip',)

    # Mengatur field di halaman 'change user'
    fieldsets = (
        (None, {'fields': ('nip', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Mengatur field di halaman 'add user'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'first_name', 'last_name', 'password', 'password2'),
        }),
    )
    
    def get_full_name_custom(self, obj):
        return obj.get_full_name()
    get_full_name_custom.short_description = 'Nama Pegawai'

# --- Admin untuk Jabatan (tetap sama) ---
@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    search_fields = ('nama_jabatan',)

# --- Unregister Profile agar tidak muncul dua kali ---
# Kita tidak perlu mendaftarkan Profile secara terpisah karena sudah inline.
# admin.site.unregister(Profile) 

# --- Register User dengan konfigurasi kustom ---
admin.site.register(User, CustomUserAdmin)

