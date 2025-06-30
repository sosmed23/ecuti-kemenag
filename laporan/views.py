# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cuti.models import PengajuanCuti
from .filters import PengajuanCutiFilter

@login_required
def laporan_cuti(request):
    # Pastikan hanya staf/admin yang bisa mengakses
    if not request.user.is_staff:
        # Redirect atau tampilkan pesan error jika bukan staf
        return redirect('dashboard')

    # Ambil semua data pengajuan cuti
    semua_pengajuan = PengajuanCuti.objects.select_related('pegawai', 'jenis_cuti').all()
    
    # Gunakan filter yang kita buat
    filter_cuti = PengajuanCutiFilter(request.GET, queryset=semua_pengajuan)
    
    context = {
        'filter': filter_cuti
    }
    return render(request, 'laporan_cuti.html', context)