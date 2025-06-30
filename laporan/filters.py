# File: laporan/filters.py
# Berisi definisi filter untuk halaman laporan cuti.

import django_filters
from cuti.models import PengajuanCuti, JenisCuti
from users.models import User
from django import forms

class PengajuanCutiFilter(django_filters.FilterSet):
    """
    FilterSet untuk memfilter data PengajuanCuti.
    """
    # Filter berdasarkan rentang tanggal pengajuan
    start_date = django_filters.DateFilter(
        field_name='tanggal_mulai', 
        lookup_expr='gte',
        label='Dari Tanggal',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
    )
    end_date = django_filters.DateFilter(
        field_name='tanggal_mulai', 
        lookup_expr='lte',
        label='Sampai Tanggal',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
    )

    # Filter berdasarkan nama pegawai
    pegawai = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Nama Pegawai',
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
    )

    # Filter berdasarkan jenis cuti
    jenis_cuti = django_filters.ModelChoiceFilter(
        queryset=JenisCuti.objects.all(),
        label='Jenis Cuti',
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
    )

    class Meta:
        model = PengajuanCuti
        fields = ['pegawai', 'jenis_cuti', 'start_date', 'end_date']