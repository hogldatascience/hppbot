from django.db import models

# Create your models here.

class P_kW(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_p_kw"


class U1_P_kW(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_u1_p_kw"

class U2_P_kW(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_u2_p_kw"

class U1_Y(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_u1_y"

class U2_Y(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_u2_y"

class H_m(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_h_m"

class Uab_kV(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_uab_kv"

class Ubc_kV(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_ubc_kv"

class Uca_kV(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Minimum = models.FloatField(null=True)
    Maximum = models.FloatField(null=True)
    Average = models.FloatField(null=True)

    Minimum_Shaped = models.FloatField(null=True)
    Maximum_Shaped = models.FloatField(null=True)
    Average_Shaped = models.FloatField(null=True)

    Minimum_Code = models.BigIntegerField(null=True)
    Maximum_Code = models.BigIntegerField(null=True)
    Average_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "scada_uca_kv"

class intake_data(models.Model):

    Date = models.DateField(primary_key=True)
    Time = models.TimeField(null=True)
    Bridge = models.FloatField(null=True)
    Upstream = models.FloatField(null=True)
    Downstream = models.FloatField(null=True)

    Bridge_Shaped = models.FloatField(null=True)
    Upstream_Shaped = models.FloatField(null=True)
    Downstream_Shaped = models.FloatField(null=True)

    Bridge_Code = models.BigIntegerField(null=True)
    Upstream_Code = models.BigIntegerField(null=True)
    Downstream_Code = models.BigIntegerField(null=True)

    class Meta:
        db_table = "box_intake_data"

# class ExcelFile(models.Model):
#     file = models.FileField()
