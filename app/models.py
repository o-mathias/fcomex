from django.db import models


class SH2(models.Model):
    co_sh2 = models.IntegerField()
    no_sh2_por = models.TextField()

    class Meta:
        managed = True
        db_table = 'sh2'


class NCM(models.Model):
    co_ncm = models.IntegerField()
    no_ncm_por = models.TextField()
    sh2 = models.ForeignKey(SH2, on_delete=models.PROTECT)
    
    class Meta:
        managed = True
        db_table = 'ncm'


class VIA(models.Model):
    co_via = models.IntegerField()
    no_via = models.CharField(max_length=300)

    class Meta:
        managed = True
        db_table = 'via'


class FComex(models.Model):
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
    movimentacao = models.CharField(max_length=2)

    class Meta:
        managed = True
        db_table = 'fcomex'


