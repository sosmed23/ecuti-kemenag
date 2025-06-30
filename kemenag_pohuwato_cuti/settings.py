# kemenag_pohuwato_cuti/settings.py

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Muat environment variables dari file .env (berguna saat development lokal)
load_dotenv(os.path.join(BASE_DIR, '.env'))


# ==============================================================================
# PENGATURAN KUNCI UNTUK PRODUKSI & DEVELOPMENT
# ==============================================================================

# Ambil SECRET_KEY dari environment variable. JANGAN TULIS LANGSUNG DI SINI.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG akan 'False' saat di-deploy di Railway, dan 'True' saat di lokal.
# Railway mengatur variabel RAILWAY_ENVIRONMENT menjadi 'production' saat deploy.
DEBUG = os.environ.get('RAILWAY_ENVIRONMENT') != 'production'

# Daftar domain yang diizinkan untuk mengakses aplikasi Anda.
ALLOWED_HOSTS = []
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

# Untuk development, tambahkan host lokal.
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('localhost')


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    # Tambahkan 'whitenoise.runserver_nostatic' di paling atas.
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplikasi Anda (sesuaikan jika namanya berbeda)
    'users.apps.UsersConfig',
    'cuti.apps.CutiConfig',

    # Library pihak ketiga jika ada
    # 'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Tambahkan Middleware Whitenoise setelah SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Ganti 'kemenag_pohuwato_cuti' dengan nama folder proyek utama Anda.
ROOT_URLCONF = 'kemenag_pohuwato_cuti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ganti 'kemenag_pohuwato_cuti' dengan nama folder proyek utama Anda.
WSGI_APPLICATION = 'kemenag_pohuwato_cuti.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

# Konfigurasi ini akan menggunakan DATABASE_URL dari Railway saat online,
# dan SQLite di komputer lokal jika variabel tersebut tidak ditemukan.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Jika Anda menggunakan custom User model:
AUTH_USER_MODEL = 'users.User'


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'id-id'  # Bahasa Indonesia
TIME_ZONE = 'Asia/Makassar' # Waktu Indonesia Tengah (WITA)
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES (PENTING UNTUK PRODUKSI)
# ==============================================================================

# URL untuk mengakses file statis (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# Folder tempat `collectstatic` akan mengumpulkan semua file statis.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Penyimpanan file statis untuk Whitenoise (sangat efisien)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Lokasi tambahan untuk file statis Anda (jika ada)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# URL untuk mengakses file media yang di-upload pengguna (Tanda Tangan, Dokumen)
MEDIA_URL = '/media/'
# Folder tempat file media akan disimpan di lokal.
# PERHATIAN: Di Railway, file lokal ini bersifat sementara. Untuk produksi serius,
# disarankan menggunakan layanan seperti AWS S3 atau Cloudinary.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'