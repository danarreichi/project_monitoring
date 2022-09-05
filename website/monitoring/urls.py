from django.urls import path
from . import views

urlpatterns = [
    # login routing
    path('', views.login, name='login'),
    path('login/auth', views.login_auth, name='login_auth'),
    path('logout', views.logout, name='logout'),

    # Home routing
    path('home', views.home, name='home'),

    # Pengguna routing
    path('pengguna', views.pengguna, name='pengguna'),
    path('pengguna/tambah_pengguna', views.tambah_pengguna, name='tambah_pengguna'),
    path('pengguna/tambah_pengguna/save', views.tambah_pengguna_save, name='tambah_pengguna_save'),
    path('pengguna/detail_pengguna/<id_pengguna>', views.detail_pengguna, name='detail_pengguna'),
    path('pengguna/detail_pengguna/<id_pengguna>/save', views.pengguna_save, name='pengguna_save'),
    path('ajax_load_nama_pengguna', views.ajax_load_nama_pengguna, name='ajax_load_nama_pengguna'),

    # Proyek routing
    path('proyek', views.proyek, name='proyek'),
    path('proyek/detail_proyek/<id_investasi>', views.detail_proyek, name='detail_proyek'),
    path('proyek/detail_proyek/<id_investasi>/daftar_pekerjaan', views.daftar_pekerjaan, name='daftar_pekerjaan'),
    path('proyek/detail_proyek/<id_investasi>/daftar_kegiatan/<id_pekerjaan>', views.daftar_kegiatan, name='daftar_kegiatan'),
    path('proyek/detail_proyek/<id_investasi>/daftar_kegiatan/<id_pekerjaan>/tambah_kegiatan', views.tambah_kegiatan, name='tambah_kegiatan'),
    path('proyek/detail_proyek/<id_investasi>/daftar_kegiatan/<id_pekerjaan>/save_kegiatan', views.save_kegiatan, name='save_kegiatan'),
    path('proyek/detail_proyek/<id_investasi>/tambah_pekerjaan', views.tambah_pekerjaan, name='tambah_pekerjaan'),
    path('proyek/detail_proyek/<id_investasi>/tambah_pekerjaan_forced', views.tambah_pekerjaan_forced, name='tambah_pekerjaan_forced'),
    path('proyek/detail_proyek/<id_investasi>/save_pekerjaan', views.save_pekerjaan, name='save_pekerjaan'),
    path('proyek/detail_proyek/<id_investasi>/save_pekerjaan_forced', views.save_pekerjaan_forced, name='save_pekerjaan_forced'),
    path('proyek/detail_proyek/<id_investasi>/save', views.detail_proyek_save, name='detail_proyek_save'),
    path('proyek/tambah_proyek', views.tambah_proyek, name='tambah_proyek'),
    path('proyek/tambah_proyek/save', views.tambah_proyek_save, name='tambah_proyek_save'),
    path('bukainvestasi/<id_investasi>', views.bukainvestasi, name='bukainvestasi'),
    path('kunciinvestasi/<id_investasi>', views.kunciinvestasi, name='kunciinvestasi'),
    path('hapuspekerjaan/<id_detail_investasi>', views.hapuspekerjaan, name='hapuspekerjaan'),
    path('hapuskegiatan/<id_pekerjaan>', views.hapuskegiatan, name='hapuskegiatan'),
    path('approvekegiatan/<id_pekerjaan>', views.approvekegiatan, name='approvekegiatan'),
    path('disapprovekegiatan/<id_pekerjaan>', views.disapprovekegiatan, name='disapprovekegiatan'),
    path('markdone_kegiatan/<id_pekerjaan>', views.markdone_kegiatan, name='markdone_kegiatan'),
    path('markundone_kegiatan/<id_pekerjaan>', views.markundone_kegiatan, name='markundone_kegiatan'),
    path('pengajuan_kegiatan/<id_pekerjaan>', views.pengajuan_kegiatan, name='pengajuan_kegiatan'),
    path('ajax_change_lokasi', views.ajax_change_lokasi, name='ajax_change_lokasi'),
    path('ajax_kunci_status_investasi', views.ajax_kunci_status_investasi, name='ajax_kunci_status_investasi'),
    path('ajax_load_proyek', views.ajax_load_proyek, name='ajax_load_proyek'),
    path('ajax_detail_proyek', views.ajax_detail_proyek, name='ajax_detail_proyek'),
    path('ajax_daftar_pekerjaan', views.ajax_daftar_pekerjaan, name='ajax_daftar_pekerjaan'),
    path('ajax_daftar_kegiatan', views.ajax_daftar_kegiatan, name='ajax_daftar_kegiatan'),
    path('ajax_daftar_kegiatan_button', views.ajax_daftar_kegiatan_button, name='ajax_daftar_kegiatan_button'),
    path('ajax_summary_pekerjaan', views.ajax_summary_pekerjaan, name='ajax_summary_pekerjaan'),
    path('ajax_status_carousel', views.ajax_status_carousel, name='ajax_status_carousel'),
    path('ajax_sisa_investasi', views.ajax_sisa_investasi, name='ajax_sisa_investasi'),
    path('ajax_sisa_kegiatan', views.ajax_sisa_kegiatan, name='ajax_sisa_kegiatan'),
]