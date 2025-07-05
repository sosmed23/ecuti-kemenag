# File: cuti/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from django.db.models import Subquery, OuterRef

from .forms import PengajuanCutiForm
from .models import PengajuanCuti, SaldoCutiTahunan, HariLibur, JenisCuti
from users.models import Profile, User 
from .utils import hitung_hari_kerja

# ==================== FUNGSI BANTUAN ====================

def potong_saldo_cuti_tahunan(pegawai, lama_cuti_diminta):
    """Mengurangi saldo cuti tahunan dari tahun-tahun sebelumnya terlebih dahulu."""
    sisa_cuti_untuk_dipotong = lama_cuti_diminta
    tahun_sekarang = timezone.now().year
    tahun_prioritas = [tahun_sekarang - 2, tahun_sekarang - 1, tahun_sekarang]
    pesan_log = []
    for tahun in tahun_prioritas:
        if sisa_cuti_untuk_dipotong <= 0:
            break
        try:
            saldo = SaldoCutiTahunan.objects.get(pegawai=pegawai, tahun=tahun)
            if saldo.sisa_hari > 0:
                cuti_yang_bisa_diambil = min(saldo.sisa_hari, sisa_cuti_untuk_dipotong)
                saldo.sisa_hari -= cuti_yang_bisa_diambil
                saldo.save()
                sisa_cuti_untuk_dipotong -= cuti_yang_bisa_diambil
                pesan_log.append(f"{cuti_yang_bisa_diambil} hari dari saldo tahun {tahun}")
        except SaldoCutiTahunan.DoesNotExist:
            continue
    if sisa_cuti_untuk_dipotong > 0:
        return False, "Total sisa cuti tidak mencukupi."
    else:
        return True, "Pengurangan berhasil: " + ", ".join(pesan_log) + "."

def kepala_kantor_required(function):
    """Decorator untuk memastikan hanya user dalam grup 'Kepala Kantor' yang bisa mengakses view."""
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Kepala Kantor').exists():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
            return redirect('dashboard')
    return wrap

# ==================== VIEW UTAMA ====================

@login_required
def dashboard(request):
    """Menampilkan halaman utama setelah login."""
    tahun_sekarang = timezone.now().year
    
    # Mengambil data sisa cuti tahunan
    sisa_cuti_2025 = SaldoCutiTahunan.objects.filter(pegawai=request.user, tahun=2025).first()
    sisa_cuti_2024 = SaldoCutiTahunan.objects.filter(pegawai=request.user, tahun=2024).first()
    
    # Mengambil data profil untuk cuti lainnya
    profil_pegawai, created = Profile.objects.get_or_create(user=request.user)

    # Mengambil riwayat pengajuan terakhir
    riwayat_pengajuan = PengajuanCuti.objects.filter(pegawai=request.user).order_by('-created_at')[:5]

    context = {
        'sisa_cuti_2025': sisa_cuti_2025.sisa_hari if sisa_cuti_2025 else 0,
        'sisa_cuti_2024': sisa_cuti_2024.sisa_hari if sisa_cuti_2024 else 0,
        'profil': profil_pegawai,
        'riwayat_pengajuan': riwayat_pengajuan,
        'active_page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)

# ==================== ALUR PENGAJUAN CUTI OLEH PEGAWAI ====================

@login_required
def ajukan_cuti(request):
    """Langkah 1: Menampilkan dan memproses form pengajuan cuti awal."""
    if request.method == 'POST':
        form = PengajuanCutiForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            request.session['pengajuan_data'] = {
                'jenis_cuti_id': form.cleaned_data['jenis_cuti'].id,
                'tanggal_mulai': form.cleaned_data['tanggal_mulai'].isoformat(),
                'tanggal_selesai': form.cleaned_data['tanggal_selesai'].isoformat(),
                'alasan': form.cleaned_data['alasan'],
                'alamat_selama_cuti': form.cleaned_data['alamat_selama_cuti'],
                'telepon_selama_cuti': form.cleaned_data['telepon_selama_cuti'],
            }
            return redirect('konfirmasi_pengajuan')
    else:
        form = PengajuanCutiForm(request=request)

    context = {'form': form, 'active_page': 'ajukan_cuti'}
    return render(request, 'pengajuan_cuti.html', context)

@login_required
def konfirmasi_pengajuan(request):
    """Langkah 2: Menampilkan ringkasan data dan memproses konfirmasi dengan tanda tangan."""
    pengajuan_data = request.session.get('pengajuan_data')
    if not pengajuan_data:
        messages.error(request, "Sesi pengajuan tidak ditemukan. Silakan isi formulir kembali.")
        return redirect('ajukan_cuti')

    jenis_cuti = get_object_or_404(JenisCuti, id=pengajuan_data['jenis_cuti_id'])
    pengajuan_data['jenis_cuti_nama'] = jenis_cuti.nama
    pengajuan_data['lama_cuti'] = hitung_hari_kerja(
        datetime.fromisoformat(pengajuan_data['tanggal_mulai']).date(),
        datetime.fromisoformat(pengajuan_data['tanggal_selesai']).date()
    )

    if request.method == 'POST':
        tanda_tangan_data_url = request.POST.get('tanda_tangan_pemohon_data')
        if not tanda_tangan_data_url:
            messages.error(request, "Tanda tangan wajib dibubuhkan untuk konfirmasi.")
            return render(request, 'konfirmasi_pengajuan.html', {'data': pengajuan_data})

        pengajuan = PengajuanCuti(
            pegawai=request.user,
            jenis_cuti=jenis_cuti,
            tanggal_mulai=pengajuan_data['tanggal_mulai'],
            tanggal_selesai=pengajuan_data['tanggal_selesai'],
            alasan=pengajuan_data['alasan'],
            alamat_selama_cuti=pengajuan_data['alamat_selama_cuti'],
            telepon_selama_cuti=pengajuan_data['telepon_selama_cuti'],
            lama_cuti=pengajuan_data['lama_cuti']
        )
        
        try:
            format, imgstr = tanda_tangan_data_url.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"tt_pemohon_{request.user.nip}_{int(timezone.now().timestamp())}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            pengajuan.tanda_tangan_pemohon = data
        except (ValueError, TypeError):
            messages.error(request, 'Data tanda tangan tidak valid.')
            return render(request, 'konfirmasi_pengajuan.html', {'data': pengajuan_data})

        try:
            profile_pegawai = Profile.objects.get(user=request.user)
            if profile_pegawai.atasan_langsung:
                pengajuan.status = 'PENDING_ATASAN'
                # === PERBAIKAN: Ambil objek .user dari atasan_langsung ===
                pengajuan.atasan_penyetuju = profile_pegawai.atasan_langsung.user
                # ==========================================================
            else:
                pengajuan.status = 'PENDING_KEPALA'
        except Profile.DoesNotExist:
             pengajuan.status = 'PENDING_KEPALA'

        pengajuan.save()
        
        if 'pengajuan_data' in request.session:
            del request.session['pengajuan_data']

        messages.success(request, 'Pengajuan cuti Anda telah berhasil dikirim dan ditandatangani!')
        return redirect('dashboard')

    context = {'data': pengajuan_data, 'active_page': 'ajukan_cuti'}
    return render(request, 'konfirmasi_pengajuan.html', context)

# ==================== ALUR PERSETUJUAN ATASAN ====================

@login_required
def daftar_persetujuan(request):
    daftar_tugas = PengajuanCuti.objects.filter(atasan_penyetuju=request.user, status='PENDING_ATASAN').order_by('created_at')
    context = {'daftar_tugas': daftar_tugas, 'judul_halaman': 'Persetujuan Atasan Langsung'}
    return render(request, 'daftar_persetujuan.html', context)

@login_required
def detail_persetujuan(request, pk):
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk, atasan_penyetuju=request.user)
    context = {'pengajuan': pengajuan}
    return render(request, 'detail_persetujuan.html', context)

@login_required
def proses_persetujuan(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk, atasan_penyetuju=request.user)
    aksi = request.POST.get('aksi')
    catatan = request.POST.get('catatan_atasan', '')
    pengajuan.catatan_atasan = catatan
    pengajuan.tanggal_pertimbangan_atasan = timezone.now()

    if aksi == 'setujui':
        pengajuan.status = 'PENDING_KEPALA'
        messages.success(request, f"Pengajuan cuti a.n. {pengajuan.pegawai.get_full_name()} telah disetujui dan diteruskan ke Kepala Kantor.")
    elif aksi == 'tolak':
        pengajuan.status = 'DITOLAK_ATASAN'
        messages.error(request, f"Pengajuan cuti a.n. {pengajuan.pegawai.get_full_name()} telah ditolak.")
        
    pengajuan.save()
    return redirect('daftar_persetujuan')

# ==================== ALUR PERSETUJUAN KEPALA KANTOR ====================

@login_required
@kepala_kantor_required
def daftar_persetujuan_kepala(request):
    daftar_tugas = PengajuanCuti.objects.filter(status='PENDING_KEPALA').order_by('created_at')
    
    if not daftar_tugas.exists():
        messages.info(request, "Saat ini tidak ada pengajuan cuti yang menunggu keputusan Kepala Kantor.")
    
    context = {'daftar_tugas': daftar_tugas, 'judul_halaman': 'Persetujuan Kepala Kantor', 'peran': 'Kepala'}
    return render(request, 'daftar_persetujuan.html', context)

@login_required
@kepala_kantor_required
def detail_persetujuan_kepala(request, pk):
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk, status__in=['PENDING_KEPALA', 'DISETUJUI', 'DITOLAK_KEPALA'])
    context = {'pengajuan': pengajuan, 'peran': 'Kepala'}
    return render(request, 'detail_persetujuan.html', context)

@login_required
@kepala_kantor_required
def proses_persetujuan_kepala(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
        
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk)
    aksi = request.POST.get('aksi')
    catatan = request.POST.get('catatan_kepala', '')
    
    pengajuan.catatan_kepala = catatan
    pengajuan.tanggal_keputusan_kepala = timezone.now()
    pengajuan.kepala_penyetuju = request.user

    if aksi == 'setujui':
        pengajuan.status = 'DISETUJUI'
        
        pegawai = pengajuan.pegawai
        lama_cuti = pengajuan.lama_cuti
        jenis_cuti_kode = pengajuan.jenis_cuti.kode

        try:
            if jenis_cuti_kode == 'CT':
                sukses, pesan = potong_saldo_cuti_tahunan(pegawai, lama_cuti)
                if sukses:
                    messages.success(request, f"Pengajuan Cuti Tahunan disetujui. {pesan}")
                else:
                    messages.warning(request, f"Pengajuan disetujui, namun saldo bermasalah: {pesan}")
            else:
                profil_pegawai = pegawai.profile
                pesan = f"Pengajuan cuti untuk {pegawai.get_full_name()} telah DISETUJUI."
                if jenis_cuti_kode == 'CS':
                    profil_pegawai.sisa_cuti_sakit -= lama_cuti
                    pesan = f"Jatah Cuti Sakit a.n. {pegawai.get_full_name()} dikurangi {lama_cuti} hari."
                elif jenis_cuti_kode == 'CM':
                    profil_pegawai.sisa_cuti_melahirkan -= lama_cuti
                    pesan = f"Jatah Cuti Melahirkan a.n. {pegawai.get_full_name()} dikurangi {lama_cuti} hari."
                elif jenis_cuti_kode == 'CAP':
                    profil_pegawai.sisa_cuti_alasan_penting -= lama_cuti
                    pesan = f"Jatah Cuti Alasan Penting a.n. {pegawai.get_full_name()} dikurangi {lama_cuti} hari."
                
                profil_pegawai.save()
                messages.success(request, pesan)

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat memotong saldo cuti: {e}")
            
    elif aksi == 'tolak':
        pengajuan.status = 'DITOLAK_KEPALA'
        messages.error(request, f"Pengajuan cuti untuk {pengajuan.pegawai.get_full_name()} telah DITOLAK.")
        
    pengajuan.save()
    return redirect('daftar_persetujuan_kepala')

# ==================== VIEW LAINNYA ====================

@login_required
def riwayat_detail(request, pk):
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk, pegawai=request.user)
    context = {'pengajuan': pengajuan}
    return render(request, 'riwayat_detail.html', context)

@login_required
def cetak_surat_cuti(request, pk):
    pengajuan = get_object_or_404(PengajuanCuti, pk=pk, status='DISETUJUI')
    is_pemilik = pengajuan.pegawai == request.user
    is_atasan = pengajuan.atasan_penyetuju == request.user if pengajuan.atasan_penyetuju else False
    is_kepala = request.user.groups.filter(name='Kepala Kantor').exists()

    if not (is_pemilik or is_atasan or is_kepala):
        messages.error(request, "Anda tidak memiliki izin untuk mengakses dokumen ini.")
        return redirect('dashboard')
        
    tahun_sekarang = timezone.now().year
    sisa_cuti = {
        'n': SaldoCutiTahunan.objects.filter(pegawai=pengajuan.pegawai, tahun=tahun_sekarang).first(),
        'n_1': SaldoCutiTahunan.objects.filter(pegawai=pengajuan.pegawai, tahun=tahun_sekarang - 1).first(),
        'n_2': SaldoCutiTahunan.objects.filter(pegawai=pengajuan.pegawai, tahun=tahun_sekarang - 2).first(),
    }
    context = {
        'pengajuan': pengajuan, 
        'sisa_cuti': sisa_cuti, 
        'tahun_sekarang': tahun_sekarang
    }
    
    return render(request, 'cetak_surat_cuti.html', context)

def hitung_lama_cuti_ajax(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            lama_cuti = hitung_hari_kerja(start_date, end_date)
            return JsonResponse({'lama_cuti': lama_cuti})
        except (ValueError, TypeError):
            return JsonResponse({'lama_cuti': 0})
    return JsonResponse({'lama_cuti': 0})

@login_required
def laporan_cuti(request):
    pengajuan_list = PengajuanCuti.objects.all().select_related('pegawai', 'jenis_cuti')

    pegawai_id = request.GET.get('pegawai', '')
    jenis_cuti_id = request.GET.get('jenis_cuti', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if pegawai_id:
        pengajuan_list = pengajuan_list.filter(pegawai_id=pegawai_id)
    if jenis_cuti_id:
        pengajuan_list = pengajuan_list.filter(jenis_cuti_id=jenis_cuti_id)
    if start_date:
        pengajuan_list = pengajuan_list.filter(tanggal_mulai__gte=start_date)
    if end_date:
        pengajuan_list = pengajuan_list.filter(tanggal_selesai__lte=end_date)
    
    tahun_sekarang = timezone.now().year
    sisa_cuti_subquery = SaldoCutiTahunan.objects.filter(
        pegawai=OuterRef('pegawai'),
        tahun=tahun_sekarang
    ).values('sisa_hari')[:1]

    pengajuan_list = pengajuan_list.annotate(
        sisa_cuti_tahunan=Subquery(sisa_cuti_subquery)
    )

    context = {
        'semua_pengajuan': pengajuan_list,
        'semua_pegawai': User.objects.all(),
        'semua_jenis_cuti': JenisCuti.objects.all(),
        'active_page': 'laporan'
    }
    return render(request, 'laporan_cuti.html', context)
