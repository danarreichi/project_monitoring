from decimal import Decimal
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import *
from django.db import connection
from datetime import date, datetime
from .models import *

# Login Function
def login(request):
    if 'id_pengguna_login' in request.session:
        return redirect('/proyek')
    else:
        return render(request, 'login/login_page.html')

def login_auth(request):
    id_pengguna = request.POST['id_pengguna']
    password_pengguna = request.POST['password_pengguna']
    status = MasterPengguna.objects.filter(id_pengguna__icontains=id_pengguna, password_pengguna__icontains=password_pengguna)
    if(status):
        get_user = MasterPengguna.objects.get(id_pengguna=id_pengguna)
        request.session['id_pengguna_login'] = get_user.id_pengguna
        request.session['nama_pengguna'] = get_user.nama_pengguna
        request.session['lokasi_proyek'] = 1
        request.session['carousel'] = 1
        request.session['jabatan_pengguna'] = get_user.jabatan_pengguna
        return redirect('/proyek')
    else:
        messages.add_message(request, messages.INFO, 'User Tidak Ditemukan')
        return redirect('/')

def logout(request):
    del request.session['id_pengguna_login']
    del request.session['nama_pengguna']
    del request.session['jabatan_pengguna']
    request.session.flush()
    return redirect('/')
    

# Main Page
def home(request):
    if 'id_pengguna_login' in request.session:
        context = {"home":"active"}
        return render(request, 'halaman_utama/index.html', context)
    else:
        return redirect('/')

# Pengguna Page
def pengguna(request):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            context = {"pengguna":"active"}
            return render(request, 'pengguna/index.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def tambah_pengguna(request):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            context = {"pengguna":"active"}
            return render(request, 'pengguna/tambah_pengguna.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def tambah_pengguna_save(request):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            id_pengguna = request.POST['id_pengguna']
            nama_pengguna = request.POST['nama_pengguna']
            jabatan_pengguna = request.POST['jabatan_pengguna']
            password_pengguna = request.POST['password_pengguna']
            stat = MasterPengguna.objects.create(id_pengguna=id_pengguna, nama_pengguna=nama_pengguna, jabatan_pengguna=jabatan_pengguna, password_pengguna=password_pengguna)
            if(stat):
                messages.add_message(request, messages.INFO, 'Berhasil Menambah Data')
            else:
                messages.add_message(request, messages.INFO, 'Gagal Menambah Data')
            return redirect('/pengguna')
        else:
            return redirect('/')
    else:
        return redirect('/')

def detail_pengguna(request, id_pengguna):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            pengguna_data = MasterPengguna.objects.get(id_pengguna=id_pengguna)
            context = {"pengguna":"active", "pengguna_data":pengguna_data}
            return render(request, 'pengguna/detail_pengguna.html', context)
        elif request.session['id_pengguna_login'] == id_pengguna:
            pengguna_data = MasterPengguna.objects.get(id_pengguna=id_pengguna)
            context = {"pengguna":"active", "pengguna_data":pengguna_data}
            return render(request, 'pengguna/detail_pengguna.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def pengguna_save(request, id_pengguna):
    nama_pengguna = request.POST['nama_pengguna']
    jabatan_pengguna = request.POST['jabatan_pengguna']
    password_pengguna = request.POST['password_pengguna']
    stat = MasterPengguna.objects.filter(id_pengguna=id_pengguna).update(nama_pengguna=nama_pengguna, jabatan_pengguna=jabatan_pengguna, password_pengguna=password_pengguna)
    if(stat):
        if(id_pengguna == request.session['id_pengguna_login']):
            new_ses = MasterPengguna.objects.get(id_pengguna=id_pengguna)
            del request.session['nama_pengguna']
            request.session['nama_pengguna'] = new_ses.nama_pengguna
        messages.add_message(request, messages.INFO, 'Berhasil Merubah Data')
    else:
        messages.add_message(request, messages.INFO, 'Gagal Merubah Data')
    return redirect('/pengguna/detail_pengguna/'+id_pengguna)

# AJAX Pengguna
def ajax_load_nama_pengguna(request):
    nama_pengguna = request.GET.get('nama_pengguna').lower()
    pengguna_data = MasterPengguna.objects.annotate(
    uname=Lower('nama_pengguna')
    ).filter(uname__icontains=nama_pengguna)
    return render(request, 'pengguna/ajax/search_pengguna.html', {"pengguna_data": pengguna_data})

# Proyek Page
def proyek(request):
    if 'id_pengguna_login' in request.session:
        data_lokasi = MasterLokasi.objects.all()
        periode_tahun = MasterInvestasi.objects.values('tanggal_mulai__year').distinct()
        context = {"proyek":"active", "data_lokasi":data_lokasi, "periode_tahun":periode_tahun}
        return render(request, 'proyek/index.html', context)
    else:
        return redirect('/')

def tambah_proyek(request):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            data_lokasi = MasterLokasi.objects.all()
            data_penanggungjawab = MasterPengguna.objects.filter(jabatan_pengguna=1)
            context = {"proyek":"active", "data_lokasi":data_lokasi, "data_penanggungjawab":data_penanggungjawab}
            return render(request, 'proyek/tambah_proyek.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def detail_proyek_save(request, id_investasi):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            id_manager = request.session['id_pengguna_login']
            id_penanggung_jawab = request.POST['penanggung_jawab']
            id_lokasi = request.POST['kota']
            nama_investasi = request.POST['nama_proyek']
            nilai_investasi = request.POST['budget_proyek']
            uraian = request.POST['uraian']
            tanggal_mulai = request.POST['tanggal_mulai']
            status_master_investasi = request.POST['input_status_investasi']
            stat = MasterInvestasi.objects.filter(id_investasi=id_investasi).update(id_manager=id_manager, id_penanggung_jawab=id_penanggung_jawab, id_lokasi=id_lokasi, nama_investasi=nama_investasi, nilai_investasi=nilai_investasi, uraian=uraian, tanggal_mulai=tanggal_mulai, status_master_investasi=status_master_investasi)
            if(stat):
                messages.add_message(request, messages.INFO, 'Berhasil Merubah Data')
            else:
                messages.add_message(request, messages.INFO, 'Gagal Merubah Data')
            return redirect('/proyek/detail_proyek/'+id_investasi)
        else:
            return redirect('/')
    else:
        return redirect('/')

def ajax_change_lokasi(request):
    lokasi_proyek = request.GET.get('lokasi_proyek')
    request.session['lokasi_proyek'] = lokasi_proyek
    if(request.session['lokasi_proyek'] == lokasi_proyek):
        return HttpResponse('success')
    else:
        return HttpResponse('failed')

def ajax_kunci_status_investasi(request):
    id_investasi = request.GET.get('id_investasi')
    status_kunci_investasi = request.GET.get('status_kunci_investasi')
    try:
        MasterInvestasi.objects.filter(id_investasi=id_investasi).update(status_kunci_investasi=status_kunci_investasi)
        return HttpResponse('success')
    except:
        return HttpResponse('failed')

def tambah_proyek_save(request):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            id_manager = request.session['id_pengguna_login']
            id_penanggung_jawab = request.POST['penanggung_jawab']
            id_lokasi = request.POST['kota']
            nama_investasi = request.POST['nama_proyek']
            nilai_investasi = request.POST['budget_proyek']
            uraian = request.POST['uraian']
            tanggal_mulai = request.POST['tanggal_mulai']
            tanggal_dibuat = datetime.today()
            status_master_investasi = -1
            status_kunci_investasi = 0
            pct_investasi = 0
            stat = MasterInvestasi.objects.create(id_manager_id=id_manager, pct_investasi=pct_investasi, id_penanggung_jawab_id=id_penanggung_jawab, id_lokasi_id=id_lokasi, nama_investasi=nama_investasi, nilai_investasi=nilai_investasi, uraian=uraian, tanggal_mulai=tanggal_mulai, tanggal_dibuat=tanggal_dibuat, status_kunci_investasi=status_kunci_investasi, status_master_investasi=status_master_investasi)
            return redirect('/proyek/detail_proyek/'+str(stat.id_investasi)+'/daftar_pekerjaan')
        else:
            return redirect('/')
    else:
        return redirect('/')

def bukainvestasi(request, id_investasi):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            status_awal = MasterInvestasi.objects.get(id_investasi=id_investasi)
            if(status_awal.status_kunci_investasi == 0 or status_awal.status_kunci_investasi == -1):
                return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')
            else:
                status_kunci_investasi = -1
                MasterInvestasi.objects.filter(id_investasi=id_investasi).update(status_kunci_investasi=status_kunci_investasi)
                return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')
        else:
            return redirect('/')
    else:
        return redirect('/')

def kunciinvestasi(request, id_investasi):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            status_awal = MasterInvestasi.objects.get(id_investasi=id_investasi)
            if(status_awal.status_kunci_investasi == 0 or status_awal.status_kunci_investasi == 1):
                return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')
            else:
                status_kunci_investasi = 1
                MasterInvestasi.objects.filter(id_investasi=id_investasi).update(status_kunci_investasi=status_kunci_investasi)
                return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')
        else:
            return redirect('/')
    else:
        return redirect('/')

def hapuspekerjaan(request, id_detail_investasi):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            try:
                id_pekerjaan = DetailInvestasi.objects.get(id_detail_investasi=id_detail_investasi)
                DetailInvestasi.objects.filter(id_detail_investasi=id_detail_investasi).delete()
                messages.add_message(request, messages.INFO, 'Berhasil Menghapus Data')
                set_pct_id_ivestasi(id_pekerjaan.id_investasi_id)
                return redirect(request.META.get('HTTP_REFERER'))
            except:
                messages.add_message(request, messages.INFO, 'Gagal Menghapus Data (Data sedang digunakan!)')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            stat = MasterInvestasi.objects.filter(id_penanggung_jawab_id=request.session['id_pengguna_login'], detailinvestasi__id_detail_investasi=id_detail_investasi)
            if(stat):
                try:
                    id_pekerjaan = DetailInvestasi.objects.get(id_detail_investasi=id_detail_investasi)
                    DetailInvestasi.objects.filter(id_detail_investasi=id_detail_investasi).delete()
                    messages.add_message(request, messages.INFO, 'Berhasil Menghapus Data')
                    set_pct_id_ivestasi(id_pekerjaan.id_investasi_id)
                    return redirect(request.META.get('HTTP_REFERER'))
                except:
                    messages.add_message(request, messages.INFO, 'Gagal Menghapus Data (Data sedang digunakan!)')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('/')
    else:
        return redirect('/')

def set_pct(id_pekerjaan):
    updated = DaftarPekerjaan.objects.values('id_detail_investasi__id_investasi').filter(id_pekerjaan=id_pekerjaan)
    data_pekerjaan = DetailInvestasi.objects.values('id_investasi').annotate(
                lwr_nama_detail_investasi=Lower('nama_detail_investasi'),
                pct=Avg(Case(When(daftarpekerjaan__status_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__status_pekerjaan__isnull=False, then='daftarpekerjaan__status_pekerjaan'), output_field=DecimalField())) * 100
            ).filter(id_investasi=updated.values('id_detail_investasi__id_investasi')[:1])
    summary_pct = data_pekerjaan.aggregate(Avg('pct'))
    MasterInvestasi.objects.filter(id_investasi=updated.values('id_detail_investasi__id_investasi')[:1]).update(pct_investasi=summary_pct['pct__avg'])

def set_pct_id_ivestasi(id_investasi):
    data_pekerjaan = DetailInvestasi.objects.values('id_investasi').annotate(
                lwr_nama_detail_investasi=Lower('nama_detail_investasi'),
                pct=Avg(Case(When(daftarpekerjaan__status_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__status_pekerjaan__isnull=False, then='daftarpekerjaan__status_pekerjaan'), output_field=DecimalField())) * 100
            ).filter(id_investasi=id_investasi)
    summary_pct = data_pekerjaan.aggregate(Avg('pct'))
    saved = summary_pct['pct__avg']
    if(saved!=None):
        MasterInvestasi.objects.filter(id_investasi=id_investasi).update(pct_investasi=saved)

def set_sisa(id_investasi):
    # data_pekerjaan = MasterInvestasi.objects.raw('SELECT mi.ID_INVESTASI, mi.NILAI_INVESTASI - SUM(dp.NILAI_PEKERJAAN) as sisa FROM master_investasi mi LEFT JOIN detail_investasi di ON di.ID_INVESTASI=mi.ID_INVESTASI LEFT JOIN daftar_pekerjaan dp ON dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI WHERE mi.ID_INVESTASI='+id_investasi+' GROUP BY mi.ID_INVESTASI;')
    data_pekerjaan = MasterInvestasi.objects.raw('SELECT mi.ID_INVESTASI, mi.NILAI_INVESTASI - SUM(di.NILAI_DETAIL_INVESTASI) as sisa FROM master_investasi mi LEFT JOIN detail_investasi di ON di.ID_INVESTASI=mi.ID_INVESTASI WHERE mi.ID_INVESTASI='+id_investasi+' AND di.STATUS_KUNCI_DETAIL_INVESTASI = 0 GROUP BY mi.ID_INVESTASI;')
    return data_pekerjaan[0]

def sisa_real(id_investasi):
    data_sisa = MasterInvestasi.objects.raw('SELECT di.ID_INVESTASI, SUM((SELECT SUM(dp.NILAI_PEKERJAAN) FROM daftar_pekerjaan dp WHERE dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI)) as sisa FROM detail_investasi di WHERE di.ID_INVESTASI='+id_investasi+' GROUP BY di.ID_INVESTASI;')
    return data_sisa[0]

def pemakaian_pekerjaan_berjalan(id_investasi):
    pemakaian = MasterInvestasi.objects.raw('SELECT ID_INVESTASI, SUM(CASE WHEN NILAI_DETAIL_INVESTASI < realisasi THEN realisasi ELSE NILAI_DETAIL_INVESTASI END) AS pemakaian_berjalan FROM (SELECT di.ID_INVESTASI, di.ID_DETAIL_INVESTASI, di.NILAI_DETAIL_INVESTASI, (SELECT CASE WHEN SUM(dp.NILAI_PEKERJAAN) IS NULL THEN 0 ELSE SUM(dp.NILAI_PEKERJAAN) END FROM daftar_pekerjaan dp WHERE dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI) AS realisasi FROM detail_investasi di WHERE di.ID_INVESTASI = '+id_investasi+' AND di.STATUS_KUNCI_DETAIL_INVESTASI=0) AS TBL_BERJALAN GROUP BY ID_INVESTASI;')
    return pemakaian[0]

def pemakaian_realisasi_pekerjaan_berjalan(id_investasi):
    pemakaian = MasterInvestasi.objects.raw('SELECT ID_INVESTASI, SUM(realisasi) AS pemakaian_realisasi_berjalan FROM (SELECT di.ID_INVESTASI, di.ID_DETAIL_INVESTASI, di.NILAI_DETAIL_INVESTASI, (SELECT CASE WHEN SUM(dp.NILAI_PEKERJAAN) IS NULL THEN 0 ELSE SUM(dp.NILAI_PEKERJAAN) END FROM daftar_pekerjaan dp WHERE dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI) AS realisasi FROM detail_investasi di WHERE di.ID_INVESTASI = '+id_investasi+' AND di.STATUS_KUNCI_DETAIL_INVESTASI=0) AS TBL_BERJALAN GROUP BY ID_INVESTASI;')
    return pemakaian[0]

def pemakaian_pekerjaan_selesai(id_investasi):
    pemakaian = MasterInvestasi.objects.raw('SELECT ID_INVESTASI, SUM(pemakaian_selesai) as pemakaian_selesai FROM (SELECT di.ID_INVESTASI, (SELECT SUM(dp.NILAI_PEKERJAAN) FROM daftar_pekerjaan dp WHERE dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI) as pemakaian_selesai FROM detail_investasi di WHERE di.ID_INVESTASI = '+id_investasi+' AND di.STATUS_KUNCI_DETAIL_INVESTASI = 1) AS TBL_SELESAI GROUP BY ID_INVESTASI;')
    return pemakaian[0]

def markdone_kegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        tanggal = datetime.today().strftime('%Y-%m-%d')
        if request.session['jabatan_pengguna'] == 0:
            nilai_pekerjaan = request.GET.get('nilai_pekerjaan')
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(status_pekerjaan=1, tanggal_selesai=tanggal, nilai_pekerjaan=nilai_pekerjaan, kunci_pekerjaan=0, nilai_tawaran_pekerjaan=0)

            #set pct master_investasi
            set_pct(id_pekerjaan)
            #--------------------------------------
            return HttpResponse('done')
        else:
            stat = MasterInvestasi.objects.filter(id_penanggung_jawab_id=request.session['id_pengguna_login'], detailinvestasi__daftarpekerjaan__id_pekerjaan=id_pekerjaan)
            if(stat):
                nilai_pekerjaan = request.GET.get('nilai_pekerjaan')
                DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(status_pekerjaan=1, nilai_pekerjaan=nilai_pekerjaan, kunci_pekerjaan=0, nilai_tawaran_pekerjaan=0, tanggal_selesai=tanggal)
                #set pct master_investasi
                set_pct(id_pekerjaan)
                #--------------------------------------
                return HttpResponse('done')
            else:
                return redirect('/')
    else:
        return redirect('/')

def markundone_kegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(status_pekerjaan=0, tanggal_selesai=None)
            #set pct master_investasi
            set_pct(id_pekerjaan)
            #--------------------------------------
            return HttpResponse('undoned success')
        else:
            stat = MasterInvestasi.objects.filter(id_penanggung_jawab_id=request.session['id_pengguna_login'], detailinvestasi__daftarpekerjaan__id_pekerjaan=id_pekerjaan)
            if(stat):
                DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(status_pekerjaan=0, tanggal_selesai=None)
                #set pct master_investasi
                set_pct(id_pekerjaan)
                #--------------------------------------
                return HttpResponse('undoned success')
            else:
                return redirect('/')
    else:
        return redirect('/')

def pengajuan_kegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        stat = MasterInvestasi.objects.filter(id_penanggung_jawab_id=request.session['id_pengguna_login'], detailinvestasi__daftarpekerjaan__id_pekerjaan=id_pekerjaan)
        #print(stat)
        if(stat):
            kunci_pekerjaan = request.GET.get('kunci_pekerjaan')
            nilai_tawaran_pekerjaan = request.GET.get('nilai_tawaran_pekerjaan')
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(kunci_pekerjaan=kunci_pekerjaan, nilai_tawaran_pekerjaan=nilai_tawaran_pekerjaan)
            return HttpResponse('pengajuan berhasil')
        else:
            return redirect('/')
    else:
        return redirect('/')

def hapuskegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).delete()
            set_pct(id_pekerjaan)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            stat = MasterInvestasi.objects.filter(id_penanggung_jawab_id=request.session['id_pengguna_login'], detailinvestasi__daftarpekerjaan__id_pekerjaan=id_pekerjaan)
            if(stat):
                DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).delete()
                set_pct(id_pekerjaan)
                messages.add_message(request, messages.INFO, 'Berhasil Menghapus Data')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('/')
    else:
        return redirect('/')

def approvekegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            nilai_pekerjaan = DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).get()
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(kunci_pekerjaan=0, nilai_tawaran_pekerjaan=0, nilai_pekerjaan=nilai_pekerjaan.nilai_tawaran_pekerjaan)
            return HttpResponse('approval berhasil')
        else:
            return redirect('/')
    else:
        return redirect('/')

def disapprovekegiatan(request, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        if request.session['jabatan_pengguna'] == 0:
            DaftarPekerjaan.objects.filter(id_pekerjaan=id_pekerjaan).update(kunci_pekerjaan=0, nilai_tawaran_pekerjaan=0)
            return HttpResponse('disapproval berhasil')
        else:
            return redirect('/')
    else:
        return redirect('/')

def ajax_load_proyek(request):
    lokasi_proyek = request.GET.get('lokasi_proyek')
    id_pengguna = request.GET.get('id_pengguna')
    request.session['lokasi_proyek'] = lokasi_proyek
    status_master_investasi = request.GET.get('tab_status')
    nama_investasi = request.GET.get('search').lower()
    periode_tahun = request.GET.get('periode_tahun')
    if periode_tahun == 'null':
        periode_tahun = MasterInvestasi.objects.values('tanggal_mulai__year').distinct()
        try:
            del request.session['periode']
        except:
            print('already deleted')
    else: 
        periode_tahun = MasterInvestasi.objects.values('tanggal_mulai__year').distinct().filter(tanggal_mulai__year=request.GET.get('periode_tahun'))
        request.session['periode'] = request.GET.get('periode_tahun')
    jabatan = MasterPengguna.objects.get(id_pengguna=id_pengguna)
    if(jabatan.jabatan_pengguna == 0):
        investasi_data = MasterInvestasi.objects.values('id_investasi', 'nama_investasi', 'detailinvestasi__daftarpekerjaan', 'pct_investasi').annotate(
            nama_pengguna=F('id_manager__nama_pengguna'),
            jml_pengajuan=Count('detailinvestasi__daftarpekerjaan__kunci_pekerjaan', filter=Q(detailinvestasi__daftarpekerjaan__kunci_pekerjaan=1)),
            lwr_nama_investasi=Lower('nama_investasi'),
            max_date=Max('detailinvestasi__tanggal_selesai_detail_investasi')
        ).filter(id_lokasi=lokasi_proyek, status_master_investasi=status_master_investasi, tanggal_mulai__year__in=periode_tahun, lwr_nama_investasi__icontains=nama_investasi).order_by('max_date')
        #print(investasi_data)
    else:    
        investasi_data = MasterInvestasi.objects.values('id_investasi', 'nama_investasi', 'detailinvestasi__daftarpekerjaan', 'pct_investasi').annotate(
            nama_pengguna=F('id_manager__nama_pengguna'),
            jml_pengajuan=Count('detailinvestasi__daftarpekerjaan__kunci_pekerjaan', filter=Q(detailinvestasi__daftarpekerjaan__kunci_pekerjaan=1)),
            lwr_nama_investasi=Lower('nama_investasi'), 
            max_date=Max('detailinvestasi__tanggal_selesai_detail_investasi'),
            datediff= Min(F('detailinvestasi__tanggal_selesai_detail_investasi'), output_field=DateField()) - date.today()
        ).filter(id_lokasi=lokasi_proyek, status_master_investasi=status_master_investasi, tanggal_mulai__year__in=periode_tahun, id_penanggung_jawab=id_pengguna, lwr_nama_investasi__icontains=nama_investasi).order_by('max_date')
    return render(request, 'proyek/ajax/list_proyek.html', {"investasi_data": investasi_data})

def ajax_detail_proyek(request):
    id_investasi = request.GET.get('id_proyek')
    request.session['selected_item'] = id_investasi
    investasi_data = MasterInvestasi.objects.values('id_investasi', 'nama_investasi', 'nilai_investasi', 'id_penanggung_jawab__nama_pengguna').annotate(
        selesai=Count('detailinvestasi__status_kunci_detail_investasi', filter=Q(detailinvestasi__status_kunci_detail_investasi=1)),
        aktif=Count('detailinvestasi__status_kunci_detail_investasi', filter=Q(detailinvestasi__status_kunci_detail_investasi=0))
    ).get(id_investasi=id_investasi)
    return render(request, 'proyek/ajax/sidebar_detail_proyek.html', {"investasi_data":investasi_data})

def detail_proyek(request, id_investasi):
    data_lokasi = MasterLokasi.objects.all()
    data_penanggungjawab = MasterPengguna.objects.filter(jabatan_pengguna=1)
    if(request.session['jabatan_pengguna'] == 0):
        data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
        context = {"proyek":"active", "data_investasi":data_investasi, "data_lokasi":data_lokasi, "data_penanggungjawab":data_penanggungjawab}
        return render(request, 'proyek/detail_proyek.html', context)
    else:
        try:
            data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi, id_penanggung_jawab=request.session['id_pengguna_login'])
            context = {"proyek":"active", "data_investasi":data_investasi, "data_lokasi":data_lokasi, "data_penanggungjawab":data_penanggungjawab}
            return render(request, 'proyek/detail_proyek.html', context)
        except:
            return redirect('/proyek')

def daftar_pekerjaan(request, id_investasi):
    context = {"proyek":"active", "daftar_pekerjaan":"active", "id_investasi":id_investasi}
    return render(request, 'proyek/daftar_pekerjaan/daftar_pekerjaan.html', context)

def ajax_status_carousel(request):
    carousel_stat = request.GET.get('carousel_stat')
    request.session['carousel'] = carousel_stat
    return HttpResponse(request.session['carousel'])

def daftar_kegiatan(request, id_investasi, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
        data_pekerjaan = DetailInvestasi.objects.get(id_detail_investasi=id_pekerjaan)
        data_detail_investasi_value = DetailInvestasi.objects.values('id_detail_investasi', 'tanggal_selesai_detail_investasi').annotate(
                sisa=F('nilai_detail_investasi') - Sum(Case(When(daftarpekerjaan__nilai_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__nilai_pekerjaan__isnull=False, then='daftarpekerjaan__nilai_pekerjaan'), output_field=DecimalField()))
        ).get(id_detail_investasi=id_pekerjaan)
        context = {"proyek":"active", "daftar_pekerjaan":"active", "data_detail_investasi_value":data_detail_investasi_value, "data_investasi":data_investasi, "id_investasi":id_investasi, "id_pekerjaan":id_pekerjaan, "data_pekerjaan":data_pekerjaan}
        return render(request, 'proyek/daftar_pekerjaan/daftar_kegiatan/daftar_kegiatan.html', context)
    else:
        return redirect('/')

def tambah_kegiatan(request, id_investasi, id_pekerjaan):
    if 'id_pengguna_login' in request.session:
        status_master_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
        if(status_master_investasi.status_master_investasi==-1):
            data_detail_investasi_value = DetailInvestasi.objects.values('id_detail_investasi', 'tanggal_selesai_detail_investasi', 'tanggal_mulai_detail_investasi').annotate(
                sisa=F('nilai_detail_investasi') - Sum(Case(When(daftarpekerjaan__nilai_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__nilai_pekerjaan__isnull=False, then='daftarpekerjaan__nilai_pekerjaan'), output_field=DecimalField()))
            ).get(id_detail_investasi=id_pekerjaan)
            set_pct(id_pekerjaan)
            context = {"proyek":"active", "daftar_pekerjaan":"active", "id_investasi":id_investasi, "status_master_investasi":status_master_investasi, "id_pekerjaan":id_pekerjaan, "data_detail_investasi_value":data_detail_investasi_value}
            return render(request, 'proyek/daftar_pekerjaan/daftar_kegiatan/tambah_kegiatan.html', context)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')

def ajax_sisa_kegiatan(request):
    id_pekerjaan = request.GET.get('id_pekerjaan')
    data_detail_investasi_value = DetailInvestasi.objects.values('id_detail_investasi', 'tanggal_selesai_detail_investasi').annotate(
                sisa=F('nilai_detail_investasi') - Sum(Case(When(daftarpekerjaan__nilai_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__nilai_pekerjaan__isnull=False, then='daftarpekerjaan__nilai_pekerjaan'), output_field=DecimalField()))
            ).get(id_detail_investasi=id_pekerjaan)
    return JsonResponse(list(data_detail_investasi_value.values()), safe=False)


def save_kegiatan(request, id_investasi, id_pekerjaan):
    nama_kegiatan = request.POST['nama_kegiatan']
    budget_kegiatan = request.POST['budget_kegiatan']
    uraian = request.POST['uraian']
    tanggal_mulai = request.POST['tanggal_mulai']
    status_pekerjaan = 0
    kunci_pekerjaan = 0
    nilai_tawaran_pekerjaan = 0
    stat = DaftarPekerjaan.objects.create(id_detail_investasi_id=id_pekerjaan, nama_pekerjaan=nama_kegiatan, uraian_pekerjaan=uraian, nilai_pekerjaan=budget_kegiatan, status_pekerjaan=status_pekerjaan, tanggal_mulai=tanggal_mulai, kunci_pekerjaan=kunci_pekerjaan, nilai_tawaran_pekerjaan=nilai_tawaran_pekerjaan)
    if(stat):
        set_pct_id_ivestasi(id_investasi)
        messages.add_message(request, messages.INFO, 'Berhasil Menambah Data')
    else:
        messages.add_message(request, messages.INFO, 'Gagal Menambah Data')
    return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_kegiatan/'+id_pekerjaan)

def tambah_pekerjaan(request, id_investasi):
    if 'id_pengguna_login' in request.session:
        data_investasi_value = MasterInvestasi.objects.values('id_investasi').values('id_investasi', 'tanggal_mulai', 'nilai_investasi').get(id_investasi=id_investasi)

        data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
        try:
            pemakaian_berjalan = pemakaian_pekerjaan_berjalan(id_investasi).pemakaian_berjalan
        except:
            pemakaian_berjalan = 0

        try:
            pemakaian_selesai = pemakaian_pekerjaan_selesai(id_investasi).pemakaian_selesai
        except:
            pemakaian_selesai = 0
        print(pemakaian_berjalan)
        print(pemakaian_selesai)
        new_sisa = data_investasi.nilai_investasi - (pemakaian_berjalan + pemakaian_selesai)
        if(new_sisa < 0):
            new_sisa = 0

        context = {"proyek":"active", "daftar_pekerjaan":"active", "sisa":new_sisa, "id_investasi":id_investasi, "data_investasi_value":data_investasi_value}
        return render(request, 'proyek/daftar_pekerjaan/tambah_pekerjaan.html', context)
    else:
        return redirect('/')

def ajax_sisa_investasi(request):
    id_investasi = request.GET.get('id_investasi')
    data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
    try:
        pemakaian_berjalan = pemakaian_pekerjaan_berjalan(id_investasi).pemakaian_berjalan
    except:
        pemakaian_berjalan = 0

    try:
        pemakaian_selesai = pemakaian_pekerjaan_selesai(id_investasi).pemakaian_selesai
    except:
        pemakaian_selesai = 0
    # print(pemakaian_berjalan)
    # print(pemakaian_selesai)
    new_sisa = data_investasi.nilai_investasi - (pemakaian_berjalan + pemakaian_selesai)
    if(new_sisa < 0):
        new_sisa = 0
    return JsonResponse(new_sisa, safe=False)

def tambah_pekerjaan_forced(request, id_investasi):
    if 'id_pengguna_login' in request.session:
        data_investasi_value = MasterInvestasi.objects.values('id_investasi').annotate(
            sisa=F('nilai_investasi') - Sum(Case(When(detailinvestasi__nilai_detail_investasi__isnull=True, then=0), When(detailinvestasi__nilai_detail_investasi__isnull=False, then='detailinvestasi__nilai_detail_investasi'), output_field=DecimalField())),
        ).values('id_investasi', 'sisa', 'tanggal_mulai').get(id_investasi=id_investasi)
        context = {"proyek":"active", "daftar_pekerjaan":"active", "data_investasi_value":data_investasi_value}
        return render(request, 'proyek/daftar_pekerjaan/tambah_pekerjaan_forced.html', context)
    else:
        return redirect('/')
    
def save_pekerjaan(request, id_investasi):
    id_investasi = id_investasi
    nama_detail_investasi = request.POST['nama_pekerjaan']
    nilai_detail_investasi = request.POST['budget_pekerjaan']
    uraian = request.POST['uraian']
    tanggal_mulai_detail_investasi = request.POST['tanggal_mulai']
    tanggal_selesai_detail_investasi = request.POST['tanggal_selesai']
    status_kunci_detail_investasi = 0
    stat = DetailInvestasi.objects.create(id_investasi_id=id_investasi, nama_detail_investasi=nama_detail_investasi, nilai_detail_investasi=nilai_detail_investasi, uraian=uraian, tanggal_selesai_detail_investasi=tanggal_selesai_detail_investasi, tanggal_mulai_detail_investasi=tanggal_mulai_detail_investasi, status_kunci_detail_investasi=status_kunci_detail_investasi)
    if(stat):
        set_pct_id_ivestasi(id_investasi)
        messages.add_message(request, messages.INFO, 'Berhasil Menambah Data')
    else:
        messages.add_message(request, messages.INFO, 'Gagal Menambah Data')
    return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')

def save_pekerjaan_forced(request, id_investasi):
    id_investasi = id_investasi
    nama_detail_investasi = request.POST['nama_pekerjaan']
    nilai_detail_investasi = request.POST['budget_pekerjaan']
    uraian = request.POST['uraian']
    tanggal_mulai_detail_investasi = request.POST['tanggal_mulai']
    tanggal_selesai_detail_investasi = request.POST['tanggal_selesai']
    status_kunci_detail_investasi = 0
    stat = DetailInvestasi.objects.create(id_investasi_id=id_investasi, nama_detail_investasi=nama_detail_investasi, nilai_detail_investasi=nilai_detail_investasi, uraian=uraian, tanggal_selesai_detail_investasi=tanggal_selesai_detail_investasi, tanggal_mulai_detail_investasi=tanggal_mulai_detail_investasi, status_kunci_detail_investasi=status_kunci_detail_investasi)
    if(stat):
        set_pct_id_ivestasi(id_investasi)
        messages.add_message(request, messages.INFO, 'Berhasil Menambah Data')
    else:
        messages.add_message(request, messages.INFO, 'Gagal Menambah Data')
    return redirect('/proyek/detail_proyek/'+id_investasi+'/daftar_pekerjaan')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def graph_data(id_investasi):
    query = 'SELECT mi.ID_INVESTASI, di.ID_DETAIL_INVESTASI, di.NAMA_DETAIL_INVESTASI, di.NILAI_DETAIL_INVESTASI, CEILING(DATEDIFF(di.TANGGAL_SELESAI_DETAIL_INVESTASI, di.TANGGAL_MULAI_DETAIL_INVESTASI)/7) AS LAMA_PERIODE, CEILING(DATEDIFF(di.TANGGAL_MULAI_DETAIL_INVESTASI, (SELECT MIN(TANGGAL_MULAI_DETAIL_INVESTASI) FROM `detail_investasi` WHERE ID_INVESTASI = '+id_investasi+'))/7) AS PERIODE_MULAI FROM master_investasi mi JOIN detail_investasi di ON di.ID_INVESTASI = mi.ID_INVESTASI WHERE mi.ID_INVESTASI = '+id_investasi
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = dictfetchall(cursor)
    
    data_json = json.dumps(data, cls=DecimalEncoder)
    return(data_json)

def graph_realisasi(id_investasi):
    query_realisasi = 'SELECT PERIODE_SELESAI, SUM(PCT) AS PCT, SUM(NILAI_PEKERJAAN) AS NILAI_PEKERJAAN FROM (SELECT PERIODE_SELESAI, SUM(STATUS_PEKERJAAN)/(SELECT COUNT(*) FROM daftar_pekerjaan WHERE ID_DETAIL_INVESTASI = TBL2.ID_DETAIL_INVESTASI)/(SELECT COUNT(*) FROM detail_investasi WHERE ID_INVESTASI = '+id_investasi+') * 100 AS PCT, SUM(TBL2.NILAI_PEKERJAAN) AS NILAI_PEKERJAAN FROM (SELECT ID_DETAIL_INVESTASI, PERIODE_SELESAI, STATUS_PEKERJAAN, NILAI_PEKERJAAN FROM (SELECT di.ID_DETAIL_INVESTASI, dp.ID_PEKERJAAN, STATUS_PEKERJAAN, CEILING(DATEDIFF(dp.TANGGAL_SELESAI, (SELECT MIN(TANGGAL_MULAI_DETAIL_INVESTASI) FROM detail_investasi WHERE ID_INVESTASI = di.ID_INVESTASI))/7) AS PERIODE_SELESAI, dp.NILAI_PEKERJAAN FROM daftar_pekerjaan dp RIGHT JOIN detail_investasi di ON dp.ID_DETAIL_INVESTASI=di.ID_DETAIL_INVESTASI JOIN master_investasi mi ON mi.ID_INVESTASI=di.ID_INVESTASI WHERE mi.ID_INVESTASI = '+id_investasi+') AS TBL1 ORDER BY PERIODE_SELESAI, STATUS_PEKERJAAN) AS TBL2 GROUP BY ID_DETAIL_INVESTASI, PERIODE_SELESAI HAVING PERIODE_SELESAI IS NOT NULL) AS TBL3 GROUP BY PERIODE_SELESAI'

    with connection.cursor() as cursor:
        cursor.execute(query_realisasi)
        data = dictfetchall(cursor)

    data_json = json.dumps(data, cls=DecimalEncoder)
    return(data_json)

def ajax_summary_pekerjaan(request):
    id_investasi = request.GET.get('id_investasi')
    set_pct_id_ivestasi(id_investasi)
    data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
    data_investasi_value = MasterInvestasi.objects.values('id_investasi').annotate(
        pct=Avg(Case(When(detailinvestasi__status_kunci_detail_investasi__isnull=True, then=0), When(detailinvestasi__status_kunci_detail_investasi__isnull=False, then='detailinvestasi__status_kunci_detail_investasi'), output_field=DecimalField())) * 100,
        sizsa=Sum(Case(When(detailinvestasi__nilai_detail_investasi__isnull=True, then=0), When(detailinvestasi__nilai_detail_investasi__isnull=False, then='detailinvestasi__nilai_detail_investasi'), output_field=DecimalField()), filter=Q(detailinvestasi__status_kunci_detail_investasi=0)),
        max_date=Max('detailinvestasi__tanggal_selesai_detail_investasi')
    ).get(id_investasi=id_investasi)
    
    data_pekerjaan = DetailInvestasi.objects.values('id_investasi').annotate(
        lwr_nama_detail_investasi=Lower('nama_detail_investasi'),
        pct=Avg(Case(When(daftarpekerjaan__status_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__status_pekerjaan__isnull=False, then='daftarpekerjaan__status_pekerjaan'), output_field=DecimalField())) * 100
    ).filter(id_investasi=id_investasi)

    #data_graphics
    graph_json = graph_data(id_investasi)
    realisasi_json = graph_realisasi(id_investasi)

    summary_pct = data_pekerjaan.aggregate(Avg('pct'))
    
    try:
        pemakaian_berjalan = pemakaian_pekerjaan_berjalan(id_investasi).pemakaian_berjalan
    except:
        pemakaian_berjalan = 0

    try:
        pemakaian_selesai = pemakaian_pekerjaan_selesai(id_investasi).pemakaian_selesai
    except:
        pemakaian_selesai = 0
    
    try:
        pemakaian_realisasi_berjalan = pemakaian_realisasi_pekerjaan_berjalan(id_investasi).pemakaian_realisasi_berjalan
    except:
        pemakaian_realisasi_berjalan = 0
    # print(data_investasi.nilai_investasi)
    # print(pemakaian_berjalan)
    # print(pemakaian_selesai)
    tampilan_sisa = data_investasi.nilai_investasi - (pemakaian_realisasi_berjalan + pemakaian_selesai)
    new_sisa = data_investasi.nilai_investasi - (pemakaian_berjalan + pemakaian_selesai)

    return render(request, 'proyek/daftar_pekerjaan/ajax/summary_pekerjaan.html', {"data_investasi":data_investasi, "realisasi_json":realisasi_json, "graph_json":graph_json, "sisa_real":new_sisa, "tampilan_sisa":tampilan_sisa, "summary_pct":summary_pct, "data_investasi_value":data_investasi_value})

def ajax_daftar_pekerjaan(request):
    id_investasi = request.GET.get('id_investasi')
    search = request.GET.get('search').lower()
    tab_status = request.GET.get('tab_status')
    data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
    data_pekerjaan = DetailInvestasi.objects.annotate(
        lwr_nama_detail_investasi=Lower('nama_detail_investasi'),
        jml_pengajuan=Count('daftarpekerjaan__kunci_pekerjaan', filter=Q(daftarpekerjaan__kunci_pekerjaan=1)),
        pemakaian=Sum('daftarpekerjaan__nilai_pekerjaan'),
        pct=Avg(Case(When(daftarpekerjaan__status_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__status_pekerjaan__isnull=False, then='daftarpekerjaan__status_pekerjaan'), output_field=DecimalField())) * 100
        ).filter(id_investasi=id_investasi, status_kunci_detail_investasi=tab_status, lwr_nama_detail_investasi__icontains=search).values('id_investasi_id__id_penanggung_jawab__nama_pengguna', 'pemakaian', 'id_detail_investasi', 'pct', 'id_investasi', 'id_investasi_id', 'nama_detail_investasi', 'nilai_detail_investasi', 'status_kunci_detail_investasi', 'tanggal_selesai_detail_investasi', 'jml_pengajuan')
    #print(data_pekerjaan)
    return render(request, 'proyek/daftar_pekerjaan/ajax/list_pekerjaan.html', {"data_pekerjaan":data_pekerjaan, "tab_status":tab_status, "data_investasi":data_investasi, "id_investasi":id_investasi})

def ajax_daftar_kegiatan(request):
    id_detail_investasi = request.GET.get('id_detail_investasi')
    nama_pekerjaan = request.GET.get('nama_pekerjaan')
    id_investasi = request.GET.get('id_investasi')
    data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
    data_kegiatan = DaftarPekerjaan.objects.annotate(
        lwr_nama_pekerjaan=Lower('nama_pekerjaan')
    ).filter(lwr_nama_pekerjaan__icontains=nama_pekerjaan, id_detail_investasi_id=id_detail_investasi).order_by('-status_pekerjaan')
    data_pekerjaan = DetailInvestasi.objects.annotate(
        lwr_nama_detail_investasi=Lower('nama_detail_investasi'),
        pct=Avg(Case(When(daftarpekerjaan__status_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__status_pekerjaan__isnull=False, then='daftarpekerjaan__status_pekerjaan'), output_field=DecimalField())) * 100
    ).get(id_detail_investasi=id_detail_investasi)
    if(data_pekerjaan.pct >= 100):
        DetailInvestasi.objects.filter(id_detail_investasi=id_detail_investasi).update(status_kunci_detail_investasi=1, tanggal_aktual_selesai_detail_investasi=datetime.today().strftime('%Y-%m-%d'))
    else:
        DetailInvestasi.objects.filter(id_detail_investasi=id_detail_investasi).update(status_kunci_detail_investasi=0, tanggal_aktual_selesai_detail_investasi=None)
    return render(request, 'proyek/daftar_pekerjaan/daftar_kegiatan/ajax/list_kegiatan.html', {"data_kegiatan":data_kegiatan, "data_investasi":data_investasi})

def ajax_daftar_kegiatan_button(request):
    id_investasi = request.GET.get('id_investasi')
    id_pekerjaan = request.GET.get('id_pekerjaan')
    data_investasi = MasterInvestasi.objects.get(id_investasi=id_investasi)
    data_detail_investasi_value = DetailInvestasi.objects.annotate(
                sisa=F('nilai_detail_investasi') - Sum(Case(When(daftarpekerjaan__nilai_pekerjaan__isnull=True, then=0), When(daftarpekerjaan__nilai_pekerjaan__isnull=False, then='daftarpekerjaan__nilai_pekerjaan'), output_field=DecimalField()))
        ).values('sisa', 'status_kunci_detail_investasi').get(id_detail_investasi=id_pekerjaan)
    #print(data_detail_investasi_value)
    if(data_investasi.status_master_investasi == -1):
        return JsonResponse(list(data_detail_investasi_value.values()), safe=False)
    else:
        return HttpResponse(-1)