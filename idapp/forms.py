from django.forms import ModelForm
from .models import stud,faculty,SDesign, FDesign

class StudentForm(ModelForm):
     class Meta:
         model = stud
         fields =['name','course','branch','admno','validtill','dateofbirth','bloodgroup','address','contact1','contact2','photo']

class FacultyForm(ModelForm):
     class Meta:
         model = faculty
         fields =['name','designation','dateofbirth','bloodgroup','address','contact','photo']

class SingleStud(ModelForm):
     class Meta:
         model = stud
         fields =['name','course','branch','admno','validtill','dateofbirth','bloodgroup','address','contact1','contact2','photo','clss','rollno']


class Sd(ModelForm):
	class Meta:
		model = SDesign
		fields = [
			"college",
			"cfont",
			"cfontsize",
			"addline1",
			"addline2",
			"addline3",
			"addline4",
			"addline5",
			"addline1to5font",
			"addline1to5fontsize",
			"detfont",
			"detfontsize",
			"clogo",
			"ilogo",
			"psign",
			"bdesign",
		]

class Fd(ModelForm):
	class Meta:
		model = FDesign
		fields = [
			"college",
			"cfont",
			"cfontsize",
			"addline1",
			"addline1font",
			"addline1fontsize",
			"addline2",
			"addline3",
			"addline4",
			"addline5",
			"addline2to5font",
			"addline2to5fontsize",
			"detfont",
			"detfontsize",
			"ilogo",
			"psign",
			"bdesign",
		]

