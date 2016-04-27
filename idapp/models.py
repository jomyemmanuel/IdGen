from __future__ import unicode_literals

from django.db import models

class student(models.Model):
  name=models.CharField(max_length=200)
  course=models.CharField(max_length=200)
  branch=models.CharField(max_length=200)
  typ = models.CharField(max_length=10)
  admissionNumber=models.CharField(max_length=200,unique=True)
  validtill=models.DateField()
  dateofbirth=models.DateField()
  bloodgroup=models.CharField(max_length=200,blank=True,null=True)
  address=models.CharField(max_length=200)
  contact1=models.CharField(max_length=10)
  contact2=models.CharField(max_length=10,blank=True,null=True)
  photo=models.ImageField(upload_to="student",blank=True,null=True)
  clss=models.CharField(max_length=5,blank=True,null=True)
  rollno=models.CharField(max_length=5,blank=True,null=True)
  barcode_serial=models.CharField(max_length=200,unique=True,null=True)
  
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
  barcode_serial=models.CharField(max_length=200,unique=True)
  
  def __str__(self):
     return self.name

class studentTemplateDesign(models.Model):
  collegeName = models.CharField(max_length=120)
  collegeNameFont = models.CharField(max_length=120)
  collegeNameFontSize = models.IntegerField()
  addressLine1 = models.CharField(max_length=120)
  addressLine2 = models.CharField(max_length=120)
  addressLine3 = models.CharField(max_length=120)
  addressLine4 = models.CharField(max_length=120)
  addressLine5 = models.CharField(max_length=120)
  addressLine1To5Font = models.CharField(max_length=120)
  addressLine1To5FontSize = models.IntegerField()
  detailsFont = models.CharField(max_length=120)
  detailsFontSize = models.IntegerField()
  collegeLogo = models.ImageField(upload_to="template_student", null=True, blank=True)
  parentLogo = models.ImageField(upload_to="template_student", null=True, blank=True)
  principalSign = models.ImageField(upload_to="template_student", null=True, blank=True)
  backgroundDesign = models.ImageField(upload_to="template_student", null=True, blank=True)
  
  def __unicode__(self):
    return self.collegeName
  def __str__(self):
    return self.collegeName

class facultyTemplateDesign(models.Model):
  collegeName = models.CharField(max_length=120)
  collegeNameFont = models.CharField(max_length=120)
  collegeNameFontSize = models.IntegerField()
  addressLine1 = models.CharField(max_length=120)
  addline1font = models.CharField(max_length=120)
  addline1fontsize = models.IntegerField()
  addressLine2 = models.CharField(max_length=120)
  addressLine3 = models.CharField(max_length=120)
  addressLine4 = models.CharField(max_length=120)
  addressLine5 = models.CharField(max_length=120)
  addressLine2To5Font = models.CharField(max_length=120)
  addressLine2To5FontSize = models.IntegerField()
  detailsFont = models.CharField(max_length=120)
  detailsFontSize = models.IntegerField()
  parentLogo = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  principalSign = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  backgroundDesign = models.ImageField(upload_to="template_faculty", null=True, blank=True)
  
  def __unicode__(self):
    return self.collegeName
  def __str__(self):
    return self.collegeName


