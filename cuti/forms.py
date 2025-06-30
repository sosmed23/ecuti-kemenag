from django import forms
from .models import PengajuanCuti, JenisCuti
from django.utils import timezone
from datetime import date
from django.db.models import Q

class PengajuanCutiForm(forms.ModelForm):
    """
    Formulir pengajuan cuti yang pilihan jenis cutinya dinamis.
    """
    class Meta:
        model = PengajuanCuti
        # PASTIKAN 'dokumen_pendukung' ada di dalam daftar ini
        fields = [
            'jenis_cuti', 
            'tanggal_mulai', 
            'tanggal_selesai', 
            'alasan', 
            'dokumen_pendukung', # <<<--- FIELD PENTING
            'alamat_selama_cuti', 
            'telepon_selama_cuti',
            
        ]
        labels = {
            'jenis_cuti': 'Jenis Cuti yang Diambil',
            'tanggal_mulai': 'Mulai Tanggal',
            'tanggal_selesai': 'Sampai Dengan Tanggal',
            'alasan': 'Alasan Cuti',
            'dokumen_pendukung': 'Unggah Dokumen Pendukung (opsional)',
            'alamat_selama_cuti': 'Alamat Selama Menjalankan Cuti',
            'telepon_selama_cuti': 'No. Telepon/HP yang bisa dihubungi',
        }
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
            'alasan': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
            'alamat_selama_cuti': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
            'telepon_selama_cuti': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
            # Widget untuk input file
            'dokumen_pendukung': forms.ClearableFileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100'}),
            'tanda_tangan_pegawai': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PengajuanCutiForm, self).__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
            user_status = None
            try:
                user_status = user.profile.status_kepegawaian
            except user._meta.model.profile.RelatedObjectDoesNotExist:
                pass
            valid_jenis_cuti = JenisCuti.objects.filter(Q(berlaku_untuk='SEMUA') | Q(berlaku_untuk=user_status))
            self.fields['jenis_cuti'] = forms.ModelChoiceField(
                queryset=valid_jenis_cuti,
                widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'}),
                label="Jenis Cuti yang Diambil"
            )

    def clean(self):
        cleaned_data = super().clean()
        tanggal_mulai = cleaned_data.get("tanggal_mulai")
        tanggal_selesai = cleaned_data.get("tanggal_selesai")
        if tanggal_mulai and tanggal_mulai < date.today():
            self.add_error('tanggal_mulai', "Tanggal mulai tidak boleh kurang dari hari ini.")
        if tanggal_mulai and tanggal_selesai:
            if tanggal_selesai < tanggal_mulai:
                self.add_error('tanggal_selesai', "Tanggal selesai tidak boleh sebelum tanggal mulai.")
        return cleaned_data