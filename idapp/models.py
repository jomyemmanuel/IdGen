from __future__ import unicode_literals

from django.db import models

class stud(models.Model):
  name=models.CharField(max_length=200)
  course=models.CharField(max_length=200)
  branch=models.CharField(max_length=200)
  admno=models.CharField(max_length=200,unique=True)
  validtill=models.DateField()
  dateofbirth=models.DateField()
  bloodgroup=models.CharField(max_length=200)
  address=models.CharField(max_length=200)
  contact1=models.CharField(max_length=10)
  contact2=models.CharField(max_length=10,blank=True,null=True)
  photo=models.ImageField(upload_to="student")
  clss=models.CharField(max_length=5,blank=True,null=True)
  rollno=models.CharField(max_length=5,blank=True,null=True)
  def __str__(self):
    return self.name

class faculty(models.Model):
  name=models.CharField(max_length=200)
  designation=models.CharField(max_length=200)
  dateofbirth=models.DateField()
  bloodgroup=models.CharField(max_length=200)
  address=models.CharField(max_length=200)
  contact=models.CharField(max_length=10)
  photo=models.ImageField(upload_to="faculty")
  
  def __str__(self):
     return self.name

class SDesign(models.Model):
  college = models.CharField(max_length=120)
  cfont = models.CharField(max_length=120)
  cfontsize = models.IntegerField()
  addline1 = models.CharField(max_length=120)
  addline2 = models.CharField(max_length=120)
  addline3 = models.CharField(max_length=120)
  addline4 = models.CharField(max_length=120)
  addline5 = models.CharField(max_length=120)
  addline1to5font = models.CharField(max_length=120)
  addline1to5fontsize = models.IntegerField()
  detfont = models.CharField(max_length=120)
  detfontsize = models.IntegerField()
  clogo = models.ImageField(upload_to="template_student", null=True, blank=True)
  ilogo = models.ImageField(upload_to="template_student", null=True, blank=True)
  psign = models.ImageField(upload_to="template_student", null=True, blank=True)
  bdesign = models.ImageField(upload_to="template_student", null=True, blank=True)
  
  def __unicode__(self):
    return self.college
  def __str__(self):
    return self.college

class FDesign(models.Model):
  college = models.CharField(max_length=120)
  cfont = models.CharField(max_length=120)
  cfontsize = models.IntegerField()
  addline1 = models.CharField(max_length=120)
  addline1font = models.CharField(max_length=120)
  addline1fontsize = models.IntegerField()
  addline2 = models.CharField(max_length=120)
  addline3 = models.CharField(max_length=120)
  addline4 = models.CharField(max_length=120)
  addline5 = models.CharField(max_length=120)
  addline2to5font = models.CharField(max_length=120)
  addline2to5fontsize = models.IntegerField()
  detfont = models.CharField(max_length=120)
  detfontsize = models.IntegerField()
  ilogo = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  psign = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  bdesign = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  
  def __unicode__(self):
    return self.college
  def __str__(self):
    return self.college


