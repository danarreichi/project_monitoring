from django.db import models


class MasterPengguna(models.Model):
    id_pengguna = models.CharField(db_column='ID_PENGGUNA', primary_key=True, max_length=50)  # Field name made lowercase.
    nama_pengguna = models.CharField(db_column='NAMA_PENGGUNA', max_length=255)  # Field name made lowercase.
    password_pengguna = models.CharField(db_column='PASSWORD_PENGGUNA', max_length=16)  # Field name made lowercase.
    jabatan_pengguna = models.IntegerField(db_column='JABATAN_PENGGUNA')  # Field name made lowercase.

    class Meta:
        db_table = 'master_pengguna'


class MasterLokasi(models.Model):
    id_lokasi = models.AutoField(db_column='ID_LOKASI', primary_key=True)  # Field name made lowercase.
    nama_lokasi = models.CharField(db_column='NAMA_LOKASI', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'master_lokasi'


class MasterInvestasi(models.Model):
    id_investasi = models.AutoField(db_column='ID_INVESTASI', primary_key=True)  # Field name made lowercase.
    id_manager = models.ForeignKey('MasterPengguna', models.DO_NOTHING, related_name='ID_MANAGER')  # Field name made lowercase.
    id_penanggung_jawab = models.ForeignKey('MasterPengguna', models.DO_NOTHING, related_name='ID_PENANGGUNG_JAWAB')  # Field name made lowercase.
    id_lokasi = models.ForeignKey('MasterLokasi', models.DO_NOTHING, db_column='ID_LOKASI')  # Field name made lowercase.
    nama_investasi = models.CharField(db_column='NAMA_INVESTASI', max_length=255)  # Field name made lowercase.
    nilai_investasi = models.DecimalField(db_column='NILAI_INVESTASI', max_digits=50, decimal_places=2)  # Field name made lowercase.
    pct_investasi = models.DecimalField(db_column='PCT_INVESTASI', max_digits=50, decimal_places=2)  # Field name made lowercase.
    uraian = models.CharField(db_column='URAIAN', max_length=255)  # Field name made lowercase.
    tanggal_mulai = models.DateField(db_column='TANGGAL_MULAI')  # Field name made lowercase.
    tanggal_dibuat = models.DateField(db_column='TANGGAL_DIBUAT')  # Field name made lowercase.
    status_master_investasi = models.IntegerField(db_column='STATUS_MASTER_INVESTASI')  # Field name made lowercase.
    status_kunci_investasi = models.IntegerField(db_column='STATUS_KUNCI_INVESTASI')  # Field name made lowercase.

    class Meta:
        db_table = 'master_investasi'


class DetailInvestasi(models.Model):
    id_detail_investasi = models.AutoField(db_column='ID_DETAIL_INVESTASI', primary_key=True)  # Field name made lowercase.
    id_investasi = models.ForeignKey('MasterInvestasi', models.DO_NOTHING, db_column='ID_INVESTASI')  # Field name made lowercase.
    nama_detail_investasi = models.CharField(db_column='NAMA_DETAIL_INVESTASI', max_length=255)  # Field name made lowercase.
    nilai_detail_investasi = models.DecimalField(db_column='NILAI_DETAIL_INVESTASI', max_digits=50, decimal_places=2)  # Field name made lowercase.
    uraian = models.CharField(db_column='URAIAN', max_length=255, blank=True, null=True) # Field name made lowercase.# Field name made lowercase.
    tanggal_mulai_detail_investasi = models.DateField(db_column='TANGGAL_MULAI_DETAIL_INVESTASI')  # Field name made lowercase.
    tanggal_selesai_detail_investasi = models.DateField(db_column='TANGGAL_SELESAI_DETAIL_INVESTASI')  # Field name made lowercase.
    tanggal_aktual_selesai_detail_investasi = models.DateField(db_column='TANGGAL_AKTUAL_SELESAI_DETAIL_INVESTASI', blank=True, null=True)  # Field name made lowercase.
    status_kunci_detail_investasi = models.IntegerField(db_column='STATUS_KUNCI_DETAIL_INVESTASI')  # Field name made lowercase.

    class Meta:
        db_table = 'detail_investasi'


class DaftarPekerjaan(models.Model):
    id_pekerjaan = models.AutoField(db_column='ID_PEKERJAAN', primary_key=True)  # Field name made lowercase.
    id_detail_investasi = models.ForeignKey('DetailInvestasi', models.DO_NOTHING, db_column='ID_DETAIL_INVESTASI')  # Field name made lowercase.
    nama_pekerjaan = models.CharField(db_column='NAMA_PEKERJAAN', max_length=255)  # Field name made lowercase.
    uraian_pekerjaan = models.CharField(db_column='URAIAN_PEKERJAAN', max_length=255)  # Field name made lowercase.
    nilai_pekerjaan = models.DecimalField(db_column='NILAI_PEKERJAAN', max_digits=50, decimal_places=2)  # Field name made lowercase.
    status_pekerjaan = models.IntegerField(db_column='STATUS_PEKERJAAN')  # Field name made lowercase.
    kunci_pekerjaan = models.IntegerField(db_column='KUNCI_PEKERJAAN')  # Field name made lowercase.
    nilai_tawaran_pekerjaan = models.DecimalField(db_column='NILAI_TAWARAN_PEKERJAAN', max_digits=50, decimal_places=2)  # Field name made lowercase.
    tanggal_mulai = models.DateField(db_column='TANGGAL_MULAI')  # Field name made lowercase.
    tanggal_selesai = models.DateField(db_column='TANGGAL_SELESAI', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'daftar_pekerjaan'