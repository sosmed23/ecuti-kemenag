# File: users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Jabatan
# Pastikan Anda mengimpor form kustom jika menggunakannya
# from .forms import CustomUserCreationForm, CustomUserChangeForm

# --- Admin untuk Profile (Akan muncul sebagai menu terpisah) ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'jabatan', 'status_kepegawaian')
    search_fields = ('user__nip', 'user__first_name', 'user__last_name')
    list_select_related = ('user', 'jabatan')
    list_filter = ('status_kepegawaian', 'jabatan')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nama Pegawai'

# --- Inline Profile (Untuk ditampilkan di dalam halaman edit User) ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Pegawai'
    fk_name = 'user'
    # Mengatur field yang akan ditampilkan di inline form
    fields = ('jabatan', 'status_kepegawaian', 'atasan_langsung', 'no_telepon', 'masa_kerja_tahun', 'masa_kerja_bulan')


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    
    ordering = ('nip',)
    # Menampilkan formulir Profile di dalam halaman User
    inlines = (ProfileInline, )
    
    list_display = ('get_full_name_custom', 'nip', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('nip', 'first_name', 'last_name')

    # Mengatur tampilan field di halaman 'change user'
    fieldsets = (
        (None, {'fields': ('nip', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Mengatur tampilan field di halaman 'add user'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'first_name', 'last_name', 'password', 'password2'),
        }),
    )
    
    def get_full_name_custom(self, obj):
        return obj.get_full_name()
    get_full_name_custom.short_description = 'Nama Pegawai'

    # === FUNGSI get_inlines DIHAPUS DARI SINI ===
    # Dengan menghapusnya, ProfileInline akan muncul di halaman 'add user' dan 'change user'


# Register model lainnya
admin.site.register(User, CustomUserAdmin)
admin.site.register(Jabatan)

