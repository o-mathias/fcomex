from django.db import models


class SH2(models.Model):
    id_sh2 = models.PositiveIntegerField(primary_key=True)
    no_sh2_por = models.CharField(max_length=300, unique=True)

    class Meta:
        managed = True
        db_table = 'sh2'


class NCM(models.Model):
    id_ncm = models.PositiveIntegerField(primary_key=True)
    no_ncm_por = models.CharField(max_length=300, unique=False)
    sh2 = models.ForeignKey(SH2, on_delete=models.PROTECT)
    
    class Meta:
        managed = True
        db_table = 'ncm'


class VIA(models.Model):
    id_via = models.PositiveIntegerField(primary_key=True)
    no_via = models.CharField(max_length=300, unique=True)

    class Meta:
        managed = True
        db_table = 'via'


class FComex(models.Model):
    id_fcomex = models.AutoField(primary_key=True)
    ano = models.IntegerField()
    mes = models.IntegerField()
    ncm = models.ForeignKey(NCM, on_delete=models.PROTECT)
    cod_unidade = models.IntegerField()
    cod_pais = models.IntegerField()
    sg_uf = models.CharField(max_length=2)
    via = models.ForeignKey(VIA, on_delete=models.PROTECT)
    cod_urf = models.IntegerField()
    vl_quantidade = models.IntegerField()
    vl_peso_kg = models.IntegerField()
    vl_fob = models.IntegerField()
    movimentacao = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'fcomex'

