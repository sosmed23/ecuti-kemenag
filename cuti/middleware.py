# cuti/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Hanya jalankan jika pengguna sudah login dan bukan superuser
        if request.user.is_authenticated and not request.user.is_superuser:
            # Jika pengguna wajib ganti password
            if request.user.wajib_ganti_password:
                # Dapatkan URL halaman ganti password dan logout
                change_password_url = reverse('ganti_password')
                logout_url = reverse('logout')

                # Izinkan akses hanya ke halaman ganti password atau logout
                if request.path not in [change_password_url, logout_url]:
                    return redirect(change_password_url)
        
        return response