# Pembaruan: users/views.py
# Memperbaiki FieldError saat mengambil data profil

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.db.models import Sum
import json
import datetime

# Impor dari aplikasi lain
from cuti.models import SaldoCutiTahunan, PengajuanCuti
from .models import Profile # <<<--- IMPOR PENTING
from .forms import UserUpdateForm, ProfileUpdateForm

# --- FUNGSI-FUNGSI VIEW ---

@login_required
def dashboard(request):
    pegawai = request.user
    
    # Menggunakan get_or_create untuk keamanan
    profile, created = Profile.objects.get_or_create(user=pegawai)

    tahun_sekarang = timezone.now().year
    
    # Ambil data sisa cuti
    sisa_cuti_list = SaldoCutiTahunan.objects.filter(
        pegawai=pegawai,
        tahun__in=[tahun_sekarang, tahun_sekarang - 1, tahun_sekarang - 2]
    ).order_by('-tahun')
    
    # Ambil riwayat pengajuan
    riwayat_pengajuan = PengajuanCuti.objects.filter(pegawai=pegawai).order_by('-created_at')[:5]
    
    # Cek tugas persetujuan sebagai Atasan Langsung
    tugas_persetujuan_count = PengajuanCuti.objects.filter(
        atasan_penyetuju=pegawai,
        status='PENDING_ATASAN'
    ).count()
    
    # Cek tugas persetujuan sebagai Kepala Kantor
    tugas_kepala_count = 0
    if pegawai.groups.filter(name='Kepala Kantor').exists():
        tugas_kepala_count = PengajuanCuti.objects.filter(status='PENDING_KEPALA').count()

    # Logika untuk data grafik
    pengajuan_disetujui = PengajuanCuti.objects.filter(
        pegawai=pegawai,
        status='DISETUJUI'
    ).values(
        'jenis_cuti__nama'
    ).annotate(
        total_hari=Sum('lama_cuti')
    ).order_by('-total_hari')

    chart_labels = [item['jenis_cuti__nama'] for item in pengajuan_disetujui]
    chart_data = [item['total_hari'] for item in pengajuan_disetujui]

    context = {
        'sisa_cuti_list': sisa_cuti_list,
        'riwayat_pengajuan': riwayat_pengajuan,
        'tugas_persetujuan_count': tugas_persetujuan_count,
        'tugas_kepala_count': tugas_kepala_count,
        'profile': profile,
        'chart_labels': chart_labels, # <-- Kirim sebagai list Python
        'chart_data': chart_data,     # <-- Kirim sebagai list Python
        'tanggal_hari_ini': datetime.date.today(),
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def edit_profile(request):
    # PERBAIKAN: Gunakan juga get_or_create di sini untuk konsistensi
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Profil Anda telah berhasil diperbarui!')
                return redirect('edit_profile')
        
        elif 'change_password' in request.POST:
            pass_form = PasswordChangeForm(request.user, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Anda telah berhasil diubah!')
                return redirect('edit_profile')
            else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=profile)
                messages.error(request, 'Gagal mengubah password. Silakan periksa error di bawah.')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        pass_form = PasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pass_form': pass_form,
    }
    return render(request, 'profile.html', context)

