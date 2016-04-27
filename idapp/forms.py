from django import forms
from django.forms import ModelForm
from .models import student,faculty,studentTemplateDesign, facultyTemplateDesign

BIRTH_YEAR_CHOICES = ('1950','1951', '1952', '1953', '1954', '1955','1956', '1957', '1958', '1959',
					  '1960','1961', '1962', '1963', '1964', '1965','1966', '1967', '1968', '1969',
					  '1970','1971', '1972', '1973', '1974', '1975','1976', '1977', '1978', '1979',
					  '1980','1981', '1982', '1983', '1984', '1985','1986', '1987', '1988', '1989',
					  '1990','1991', '1992', '1993', '1994', '1995','1996', '1997', '1998', '1999',
					  '2000','2001', '2002', '2003', '2004', '2005','2006', '2007', '2008', '2009',
					 )
VALID_TILL_CHOICES = ('2015','2016', '2017', '2018', '2019', '2020','2021', '2022', '2023', '2024',
					  '2025','2026', '2027', '2028', '2029', '2030','2031', '2032', '2033', '2034',
					 )

BRANCH_OPTIONS = (  ('Computer Science & Engineering', 'Computer Science & Engineering') ,
                    ('Electronics & Communication Engineering', 'Electronics & Communication Engineering'),
                    ('Electronics & Biomedical Engineering', 'Electronics & Biomedical Engineering') ,
                    ('Electrical & Electronics Engineering', 'Electrical & Electronics Engineering'),
	                ('Signal Processing', 'Signal Processing') , ('Image Processing', 'Image Processing') ,
	                ('VLSI', 'VLSI'), ('OPTO Electronics', 'OPTO Electronics') ,
	                ('Energy Management', 'Energy Management'),
				 )

COURSE_OPTIONS = ( ('B-Tech', 'B-Tech') , ('M-Tech', 'M-Tech'), )

TYPE_OPTIONS = (('Regular', 'Regular') , ('Lateral', 'Lateral'),)

CLASS_OPTIONS = (('None', 'None'),('CSA', 'CSA') , ('CSB', 'CSB'), ('ECA', 'ECA') ,
				('ECB', 'ECB') , ('EBA', 'EBA'), ('EEA', 'EEA') , )
	                
				 

class StudentForm(ModelForm):
	 dateofbirth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	 validtill = forms.DateField(widget=forms.SelectDateWidget(years=VALID_TILL_CHOICES))
	 branch = forms.ChoiceField(choices=BRANCH_OPTIONS)
	 course = forms.ChoiceField(choices=COURSE_OPTIONS)
	 typ = forms.ChoiceField(choices=TYPE_OPTIONS)
	 clss = forms.ChoiceField(choices=CLASS_OPTIONS)
	 class Meta:
	 	model = student
	 	fields =['name','course','branch', 'typ', 'admissionNumber','validtill','dateofbirth','bloodgroup','address','contact1','contact2','photo', 'clss']

class FacultyForm(ModelForm):
	 dateofbirth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	 class Meta:
	 	model = faculty
	 	fields =['name','designation','dateofbirth','bloodgroup','address','contact','photo', 'barcode_serial']

class SingleStudentForm(ModelForm):
	dateofbirth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	validtill = forms.DateField(widget=forms.SelectDateWidget(years=VALID_TILL_CHOICES))
	branch = forms.ChoiceField(choices=BRANCH_OPTIONS)
	course = forms.ChoiceField(choices=COURSE_OPTIONS)
	typ = forms.ChoiceField(choices=TYPE_OPTIONS)
	clss = forms.ChoiceField(choices=CLASS_OPTIONS)
	class Meta:
		model = student
		fields =['name', 'typ' , 'course','branch','admissionNumber','validtill','dateofbirth','bloodgroup','address','contact1','contact2','photo','clss','rollno']


class StudentTemplateForm(ModelForm):
	class Meta:
		model = studentTemplateDesign
		fields = [
			"collegeName",
			"collegeNameFont",
			"collegeNameFontSize",
			"addressLine1",
			"addressLine2",
			"addressLine3",
			"addressLine4",
			"addressLine5",
			"addressLine1To5Font",
			"addressLine1To5FontSize",
			"detailsFont",
			"detailsFontSize",
			"collegeLogo",
			"parentLogo",
			"principalSign",
			"backgroundDesign",
		]

class FacultyTemplateForm(ModelForm):
	class Meta:
		model = facultyTemplateDesign
		fields = [
			"collegeName",
			"collegeNameFont",
			"collegeNameFontSize",
			"addressLine1",
			"addline1font",
			"addline1fontsize",
			"addressLine2",
			"addressLine3",
			"addressLine4",
			"addressLine5",
			"addressLine2To5Font",
			"addressLine2To5FontSize",
			"detailsFont",
			"detailsFontSize",
			"parentLogo",
			"principalSign",
			"backgroundDesign",
		]

