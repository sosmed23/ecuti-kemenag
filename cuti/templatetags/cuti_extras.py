# File: cuti/templatetags/cuti_extras.py
# Berisi fungsi kustom untuk digunakan di dalam template.

from django import template

register = template.Library()

@register.filter(name='terbilang')
def terbilang(n):
    """
    Mengubah angka integer menjadi teks terbilang dalam Bahasa Indonesia.
    Contoh: 12 menjadi "Dua Belas".
    """
    if n is None or not isinstance(n, int):
        return ""
    
    satuan = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]
    
    if n < 12:
        return satuan[n]
    elif n < 20:
        return terbilang(n - 10) + " Belas"
    elif n < 100:
        return terbilang(n // 10) + " Puluh " + terbilang(n % 10)
    elif n < 200:
        return "Seratus " + terbilang(n - 100)
    elif n < 1000:
        return terbilang(n // 100) + " Ratus " + terbilang(n % 100)
    # Anda bisa melanjutkan logika ini untuk ribuan, jutaan, dst. jika diperlukan.
    else:
        return str(n) # Fallback jika angka terlalu besar
