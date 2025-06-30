# File: cuti/utils.py
# Berisi fungsi-fungsi bantuan, seperti menghitung hari kerja.

import holidays
from datetime import timedelta
from .models import HariLibur

def hitung_hari_kerja(start_date, end_date):
    """
    Menghitung jumlah hari kerja antara dua tanggal,
    tidak termasuk Sabtu, Minggu, dan hari libur.
    """
    if not start_date or not end_date or start_date > end_date:
        return 0

    # Ambil daftar hari libur dari database
    libur_custom = set(HariLibur.objects.values_list('tanggal', flat=True))
    
    # Ambil daftar hari libur nasional dari library untuk tahun yang relevan
    # Rentang tahun dibuat lebih luas untuk menangani cuti lintas tahun
    libur_nasional = holidays.ID(years=range(start_date.year, end_date.year + 2))

    jumlah_hari_kerja = 0
    current_date = start_date
    while current_date <= end_date:
        # Cek apakah bukan weekend (Senin=0, Minggu=6)
        if current_date.weekday() < 5:
            # Cek apakah bukan hari libur custom atau nasional
            if current_date not in libur_custom and current_date not in libur_nasional:
                jumlah_hari_kerja += 1
        current_date += timedelta(days=1)
        
    return jumlah_hari_kerja
