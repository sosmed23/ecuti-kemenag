# File: users/admin.py
# PERBARUAN: Menambahkan halaman admin khusus untuk Profile

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Jabatan
from .forms import CustomUserCreationForm, CustomUserChangeForm

# --- Admin untuk Profile (Akan muncul sebagai menu terpisah) ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'jabatan', 'status_kepegawaian', 'sisa_cuti_sakit', 'sisa_cuti_melahirkan', 'sisa_cuti_alasan_penting')
    search_fields = ('user__nip', 'user__first_name', 'user__last_name')
    list_select_related = ('user', 'jabatan')
    list_editable = ('sisa_cuti_sakit', 'sisa_cuti_melahirkan', 'sisa_cuti_alasan_penting')
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
    fieldsets = (
        (None, {
            'fields': ('jabatan', 'status_kepegawaian', 'atasan_langsung', 'no_telepon')
        }),
        ('Informasi Kepegawaian', {
            'fields': ('masa_kerja_tahun', 'masa_kerja_bulan')
        }),
        ('Saldo Cuti Tambahan', {
            'fields': ('sisa_cuti_sakit', 'sisa_cuti_melahirkan', 'sisa_cuti_alasan_penting')
        }),
    )

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    ordering = ('nip',)
    inlines = (ProfileInline, )
    list_display = ('get_full_name', 'nip', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('nip', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'first_name', 'last_name', 'password', 'password2'),
        }),
    )
    search_fields = ('nip', 'first_name', 'last_name')

    def get_inlines(self, request, obj=None):
        if not obj:
            return []
        return (ProfileInline,)

# Register model lainnya
admin.site.register(User, CustomUserAdmin)
admin.site.register(Jabatan)

