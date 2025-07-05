# File: users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Jabatan
# Jika Anda menggunakan form kustom, pastikan untuk meng-uncomment baris ini
# from .forms import CustomUserCreationForm, CustomUserChangeForm

# --- Inline Profile (Untuk ditampilkan di dalam halaman Edit User) ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Pegawai'
    fk_name = 'user'
    # Field yang akan muncul di form inline
    fields = ('jabatan', 'status_kepegawaian', 'atasan_langsung', 'no_telepon', 'masa_kerja_tahun', 'masa_kerja_bulan')


class CustomUserAdmin(UserAdmin):
    model = User
    
    # Daftarkan ProfileInline untuk muncul di halaman admin User
    inlines = (ProfileInline, )
    
    # Pengaturan untuk tampilan daftar pengguna
    list_display = ('get_full_name_custom', 'nip', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('nip', 'first_name', 'last_name')
    ordering = ('nip',)

    # Field yang akan muncul di halaman 'edit user'
    fieldsets = (
        (None, {'fields': ('nip', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Field yang akan muncul di halaman 'add user'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'first_name', 'last_name', 'password', 'password2'),
        }),
    )
    
    def get_full_name_custom(self, obj):
        return obj.get_full_name()
    get_full_name_custom.short_description = 'Nama Pegawai'

    # === FUNGSI PENTING UNTUK ALUR DUA LANGKAH ===
    
    # 1. Mencegah form Profile muncul saat 'menambah' user baru
    def get_inlines(self, request, obj=None):
        if obj is None: # obj adalah None jika ini halaman 'add'
            return []
        return super().get_inlines(request, obj)

    # 2. Membuat Profile kosong secara otomatis setelah User baru disimpan
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 'change' bernilai False jika ini adalah objek baru
        if not change:
            # Pastikan profile belum ada untuk menghindari error
            if not hasattr(obj, 'profile'):
                Profile.objects.create(user=obj)


# Register User dengan konfigurasi kustom
admin.site.register(User, CustomUserAdmin)

# Register Jabatan seperti biasa
@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    search_fields = ('nama_jabatan',)

# Kita tidak perlu me-register Profile secara terpisah karena sudah menjadi inline
