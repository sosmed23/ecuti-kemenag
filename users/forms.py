# Pembaruan: users/forms.py
# (Ganti seluruh isi file ini)

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User, Profile

# --- FORMULIR UNTUK MEMBUAT USER (DARI ADMIN) ---
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Sandi', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Konfirmasi sandi', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('nip', 'first_name', 'last_name')
    def clean_password2(self):
        cd = self.cleaned_data
        if 'password' in cd and 'password2' in cd:
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Kedua sandi yang Anda masukkan tidak cocok.')
        return cd.get('password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# --- FORMULIR UNTUK MENGUBAH USER (DARI ADMIN) ---
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('nip', 'first_name', 'last_name', 'email')


# ==================== FORMULIR BARU UNTUK HALAMAN PROFIL ====================

# Definisikan atribut CSS yang akan kita gunakan berulang kali
text_input_attrs = {
    'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-600 focus:border-green-600 sm:text-sm'
}

class UserUpdateForm(forms.ModelForm):
    """Formulir untuk user mengedit data pribadinya."""
    first_name = forms.CharField(label="Nama Depan", widget=forms.TextInput(attrs=text_input_attrs))
    last_name = forms.CharField(label="Nama Belakang", widget=forms.TextInput(attrs=text_input_attrs))
    email = forms.EmailField(widget=forms.EmailInput(attrs=text_input_attrs))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Formulir untuk user mengedit data profilnya (seperti no. telp)."""
    no_telepon = forms.CharField(label="No. Telepon", widget=forms.TextInput(attrs=text_input_attrs))

    class Meta:
        model = Profile
        fields = ['no_telepon']
# =========================================================================