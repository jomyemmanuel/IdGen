from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# imports for reportlab pdfgeneration
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from .forms import StudentForm,FacultyForm,StudentTemplateForm, FacultyTemplateForm,SingleStudentForm
from .models import student,faculty,studentTemplateDesign, facultyTemplateDesign
import os
import re
import zipfile

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def login1(request):
  next=request.GET.get('next','/')
  if request.method=="POST":
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
      if user.is_active:
        login(request,user)
        return HttpResponseRedirect('/')
      else:
        HttpResponse("Inactive user!")
    else:
      return HttpResponseRedirect('/login/')
  return render(request,"login.html",{'redirect_to':next})


def logout1(request):
  logout(request)
  return HttpResponseRedirect('/')


def mainpage(request):
   return render(request,'home.html')

@login_required(login_url='/login/')
def studentHome(request):
   return render(request,'studentHome.html')

@login_required(login_url='/login/')
def facultyHome(request):
   return render(request,'facultyHome.html')

@login_required(login_url='/login/')
def studentRegistration(request):
	if request.method=='POST':
		try:
			a=student.objects.get(admissionNumber=request.POST.get("admissionNumber"))
		except:
			form=StudentForm(request.POST,request.FILES)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.save()
				messages.success(request, 'Student Registered Succesfully.')
				return HttpResponseRedirect('/studentRegistration')
			else:
				form=StudentForm()
				context={"form":form}
				messages.error(request, 'Form Not Valid.')
				return render(request,'studentRegistration.html',context)
		else:
			form=StudentForm()
			context={"form":form}
			messages.error(request, 'Student Exists.')
			return render(request,'studentRegistration.html',context)
	else:
		form=StudentForm()
		context={"form":form}
		return render(request,'studentRegistration.html',context)

@login_required(login_url='/login/')
def facultyRegistration(request):
   if request.method=='POST':
    try:
      a=faculty.objects.get(barcode_serial=request.POST.get("barcode_serial"))
    except:
     form=FacultyForm(request.POST,request.FILES)
     if form.is_valid():
       instance=form.save(commit=False)
       instance.save()
       messages.success(request, 'Faculty Registered Succesfully.')
       return HttpResponseRedirect('/facultyRegistration') 
     else:
       form=FacultyForm()
       context={"form":form}
       messages.error(request, 'Form Not Valid.')
       return render(request,'facultyRegistration.html',context)
    else:
    	form=FacultyForm()
    	context={"form":form}
    	messages.error(request, 'Faculty Exists.')
    	return render(request,'facultyRegistration.html',context)
   else:
     #errormsg="Method not POST"
     form=FacultyForm()
     context={"form":form}
     return render(request,'facultyRegistration.html',context)


@login_required(login_url='/login/')
def studentEdit(request, id=None):
  instance = get_object_or_404(student, id=id)
  form=StudentForm(request.POST or None,request.FILES or None, instance=instance)
  if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
  context = {
  	"instance":instance,
  	"form":form,
  	"name":instance.name,
  }
  return render(request,'studentEditForm.html',context)

@login_required(login_url='/login/')
def facultyEdit(request, id=None):
	instance = get_object_or_404(faculty, id=id)
	form=FacultyForm(request.POST or None,request.FILES or None, instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
	context = {
		"instance":instance,
		"form":form,
		"name":instance.name,
	}
	return render(request,'facultyEditForm.html',context)

@login_required(login_url='/login/')
def studentPdfHome(request):
	return render(request,'studentPdfHome.html')

@login_required(login_url='/login/')
def studentPdf(request):
	details=studentTemplateDesign.objects.all()
	if not len(details):
		return HttpResponseRedirect('/studentTemplateInput')
	details=studentTemplateDesign.objects.get()
	if request.method=="POST":
		try:
			smallest=100000000
			largest=0
			for i in student.objects.all():
			    a=int(i.admissionNumber.split('/')[0])
			    if a<smallest:
			    	smallest=a
			    	#print smallest
			    elif a>largest:
		      		largest=a
		      		#print largest
			a=int(request.POST['range'].split('-')[0])
			b=int(request.POST['range'].split('-')[1])
			q=[]
			if(a<smallest):
				a=smallest
				#print smallest
			elif(b>largest):
				b=largest
				#print largest
			for i in student.objects.all():
				if((int(i.admissionNumber.split('/')[0])>=a)and(int(i.admissionNumber.split('/')[0])<=b)):
					q.append(i)

			if q.__len__()==0:
			  	return render(request,'home.html')
			details=studentTemplateDesign.objects.get()
			back = root + '/media/'+ str(details.backgroundDesign)
			princi = root + '/media/'+ str(details.principalSign)
			logoright = root + '/media/'+ str(details.parentLogo)
			logoleft = root + '/media/'+ str(details.collegeLogo)
			width = 540*mm
			height = 860*mm
			c = canvas.Canvas("pdf/"+'rangefront.pdf')
			for i in q:
			  pic = root + i.photo.url
			  c.setPageSize((width, height))
			  if details.backgroundDesign:
			    c.drawImage(back, 0, 0, height=height, width=width)
			#c.saveState()
			  if details.collegeLogo:
			    c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
			  if details.parentLogo:
			    c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
			  c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
			  c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
			  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
			  c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
			  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
			  c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
			  #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
			  c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
			  c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
			  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
			  c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
			  if i.photo.url:
			  	c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
			  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
			  c.drawString(30*mm, 430*mm, "Name :")
			  c.drawString(165*mm, 430*mm,i.name)
			  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
			  c.drawString(30*mm, 340*mm, "Course :")
			  c.drawString(165*mm, 340*mm,i.course)
			  c.drawString(30*mm, 280*mm, "Branch :")
			  c.drawString(165*mm, 280*mm, i.branch)
			  c.drawString(30*mm, 180*mm, "ADMN No :")
			  c.drawString(165*mm, 180*mm, i.admissionNumber)
			  c.drawString(30*mm, 120*mm, "Valid Till :")
			  c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
			  c.drawString(30*mm, 60*mm, "Date Of Birth:")
			  c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
			  c.setFont('Times-Bold', 60)
			  c.drawString(420*mm, 20*mm, "Principal")
			  if details.principalSign:
			    c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
			  c.showPage()
			c.save()
			c = canvas.Canvas("pdf/"+'rangeback.pdf')
			for i in q:
			  barcode128 = code128.Code128(i.barcode_serial, barHeight=50*mm, barWidth=1.5*mm)
			  c.setPageSize((width, height))
			  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
			  barcode128.drawOn(c, 130*mm, 750*mm)
			  c.drawString(190*mm, 720*mm, i.barcode_serial)
			  c.drawString(30*mm, 630*mm, "Blood Group :")
			  c.drawString(210*mm, 630*mm,i.bloodgroup)
			  c.drawString(30*mm, 550*mm, "Address :")
			  le=i.address.__len__()
			  n=0
			      #x=2
			  ht=550
			  y=re.split(',',i.address)
			  y=re.split(',',i.address)
			  for x in y:
			    c.drawString(210*mm, ht*mm,x)
			    ht=ht-40

			  c.drawString(30*mm, 170*mm, "Contact No. :")
			  c.drawString(210*mm, 170*mm,i.contact1)
			  c.drawString(210*mm, 140*mm,i.contact2)
			  c.drawString(30*mm, 60*mm, "Signature     :")
			  c.rect(160*mm,30*mm,320*mm,70*mm)
			  c.showPage()
			c.save()

			arch=zipfile.ZipFile("pdf/"+"range.zip","w")
			arch.write("pdf/"+'rangefront.pdf')
			arch.write("pdf/"+'rangeback.pdf')
			arch.close()
			response = HttpResponse(open(root+"/pdf"+'/range.zip', 'rb').read(), content_type='application/zip')
			response['Content-Disposition'] = 'attachment; filename=range.zip'
			return response
			return render(request,'home.html')				
		except:
			messages.error(request, 'Please Fill Details of' + i.name)
			return HttpResponseRedirect('/studentList')
	else:
		try:
			q=student.objects.all()
			if q.__len__()==0:
				return render(request,'home.html')
			details=studentTemplateDesign.objects.get()
			back = root + '/media/'+ str(details.backgroundDesign)
			princi = root + '/media/'+ str(details.principalSign)
			logoright = root + '/media/'+ str(details.parentLogo)
			logoleft = root + '/media/'+ str(details.collegeLogo)
			width = 540*mm
			height = 860*mm
			c = canvas.Canvas("pdf/"+'front.pdf')
			for i in q:
				pic = root + i.photo.url
				c.setPageSize((width, height))
				if details.backgroundDesign:
					c.drawImage(back, 0, 0, height=height, width=width)
				if details.collegeLogo:
					c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
				if details.parentLogo:
					c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
				c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
				c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
				c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
				c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
				c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
				c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
				c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
				c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
				c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
				c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
				if i.photo.url:
					c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
				c.setFont(str(details.detailsFont), int(details.detailsFontSize))
				c.drawString(30*mm, 430*mm, "Name :")
				c.drawString(165*mm, 430*mm,i.name)
				c.setFont(str(details.detailsFont), int(details.detailsFontSize))
				c.drawString(30*mm, 340*mm, "Course :")
				c.drawString(165*mm, 340*mm,i.course)
				c.drawString(30*mm, 280*mm, "Branch :")
				c.drawString(165*mm, 280*mm, i.branch)
				c.drawString(30*mm, 180*mm, "ADMN No :")
				c.drawString(165*mm, 180*mm, i.admissionNumber)
				c.drawString(30*mm, 120*mm, "Valid Till:")
				c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
				c.drawString(30*mm, 60*mm, "Date Of Birth:")
				c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
				c.setFont('Times-Bold', 60)
				c.drawString(420*mm, 20*mm, "Principal")
				if details.principalSign:
					c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
				c.showPage()
			c.save()
			c = canvas.Canvas("pdf/"+'back.pdf')
			for i in q:
				barcode128 = code128.Code128(i.barcode_serial, barHeight=50*mm, barWidth=1.5*mm)
				c.setPageSize((width, height))
				c.setFont(str(details.detailsFont), int(details.detailsFontSize))
				barcode128.drawOn(c, 130*mm, 750*mm)
				c.drawString(190*mm, 720*mm, i.barcode_serial)
				c.drawString(30*mm, 630*mm, "Blood Group :")
				c.drawString(210*mm, 630*mm,i.bloodgroup)
				c.drawString(30*mm, 550*mm, "Address :")
				le=i.address.__len__()
				n=0
				ht=550
				y=re.split(',',i.address)
				y=re.split(',',i.address)
				for x in y:
					c.drawString(210*mm, ht*mm,x)
					ht=ht-40
				c.drawString(30*mm, 170*mm, "Contact No. :")
				c.drawString(210*mm, 170*mm,i.contact1)
				c.drawString(210*mm, 140*mm,i.contact2)
				c.drawString(30*mm, 60*mm, "Signature     :")
				c.rect(160*mm,30*mm,320*mm,70*mm)
				c.showPage()
			c.save()

			arch=zipfile.ZipFile("pdf/"+"id.zip","w")
			arch.write("pdf/"+'front.pdf')
			arch.write("pdf/"+'back.pdf')
			arch.close()
			response = HttpResponse(open(root+"/pdf"+'/id.zip', 'rb').read(), content_type='application/zip')
			response['Content-Disposition'] = 'attachment; filename=student.zip'
			return response
			return render(request,'home.html')
		except:
			messages.error(request, 'Please Fill Entire Details.(' + i.name + ')' )
			return HttpResponseRedirect('/studentList')


@login_required(login_url='/login/')
def studentPdfPreview(request):
  details = studentTemplateDesign.objects.get()
        #print str(details.backgroundDesign.url)[2:]
  back = root + '/media/'+ str(details.backgroundDesign)
  pic = root + '/static/img/do_not_delete.jpg'
  princi = root + '/media/' + str(details.principalSign)
  logoright = root+ '/media/' +  str(details.parentLogo)
  logoleft = root + '/media/' +  str(details.collegeLogo)
  barcode_value = "U617513CSB99"
  barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
  width = 540*mm
  height = 860*mm
        #print str(details.collegeName)
  c = canvas.Canvas("pdf/"+'student.pdf')
  c.setPageSize((width, height))
  if details.backgroundDesign:
    c.drawImage(back, 0, 0, height=height, width=width)
  #c.saveState()
  if details.collegeLogo:
    c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
  if details.parentLogo:
    c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
  c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
  c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
  c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
  c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
  #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
  c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
  c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
  c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
  c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
  c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
  c.drawString(30*mm, 430*mm, "Name ")
  c.drawString(165*mm, 430*mm, ": JOMY EMMANUEL")
  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
  c.drawString(30*mm, 340*mm, "Course ")
  c.drawString(165*mm, 340*mm, ": BTech")
  c.drawString(30*mm, 280*mm, "Branch ")
  c.drawString(165*mm, 280*mm, ": Computer Science And Engineering")
  c.drawString(30*mm, 180*mm, "ADMN No ")
  c.drawString(165*mm, 180*mm, ": 6175/13")
  c.drawString(30*mm, 120*mm, "Valid Till ")
  c.drawString(165*mm, 120*mm, ": 30-06-2017")
  c.drawString(30*mm, 60*mm, "Date Of Birth ")
  c.drawString(165*mm, 60*mm, ": 06/05/1995")
  c.setFont('Times-Bold', 60)
  c.drawString(420*mm, 20*mm, "Principal")
  if details.principalSign:
    c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
  c.showPage()

  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
  barcode128.drawOn(c, 130*mm, 750*mm)
  c.drawString(190*mm, 720*mm, "U617513CSB27")
  c.drawString(30*mm, 630*mm, "Blood Group ")
  c.drawString(210*mm, 630*mm, ": A+")
  c.drawString(30*mm, 550*mm, "Address ")
  c.drawString(210*mm, 550*mm, ": FLAT 2A")
  c.drawString(210*mm, 500*mm, "  SLYLINE BUILDERS")
  c.drawString(210*mm, 450*mm, "  APJ ROAD")
  c.drawString(210*mm, 400*mm, "  EDAPPALLY TOLL,")
  c.drawString(210*mm, 350*mm, "  EDAPPALLY P.O.")
  c.drawString(210*mm, 300*mm, "  682024")
  c.drawString(30*mm, 170*mm, "Contact No. ")
  c.drawString(210*mm, 170*mm, ": 0484-2657856")
  c.drawString(210*mm, 140*mm, "  9895462865")
  c.drawString(30*mm, 60*mm, "Signature     :")
  c.rect(160*mm,30*mm,320*mm,70*mm)
  
  c.save()

  with open("pdf/"+'student.pdf', 'rb') as pdf:
    response = HttpResponse(pdf.read(),content_type='application/pdf')
    response['Content-Disposition'] = 'filename=some_file.pdf'
    return response
  pdf.closed

@login_required(login_url='/login/')
def studentListSave(request):
	if request.method=='POST':
		for i in student.objects.all():
			i.clss=request.POST['clss'+str(i.pk)]
			i.rollno=request.POST['rollno'+str(i.pk)]
			if i.barcode_serial is None:
				if i.clss != "None" and i.rollno != "None":
					i.barcode_serial=""
					if(i.course[0]=="B"):
						i.barcode_serial+="U"
					else:
						i.barcode_serial+="P"
					i.barcode_serial+=i.admissionNumber.split('/')[0]+i.admissionNumber.split('/')[1]
					i.barcode_serial+=str(i.clss) + str(i.rollno)
			i.save()
		messages.success(request, 'Details Updated.')
		return HttpResponseRedirect('/studentList')
	else:
		return render(request,'home.html')        
   
    
@login_required(login_url='/login/')
def studentSave(request):
   if request.method=='POST':
	   q=student.objects.get(pk=request.POST['stu'])
	   q.name=request.POST.get('name')
	   q.course=request.POST.get('course')
	   q.branch=request.POST.get('branch')
	   q.admissionNumber=request.POST.get('admissionNumber')
	   q.validtill=request.POST.get('validtill_year')+ "-" + request.POST.get('validtill_month') + "-" + request.POST.get('validtill_day')
	   q.dateofbirth=request.POST.get('dateofbirth_year')+ "-" + request.POST.get('dateofbirth_month') + "-" + request.POST.get('dateofbirth_day')
	   q.bloodgroup=request.POST.get('bloodgroup')
	   q.address=request.POST.get('address')
	   q.contact1=request.POST.get('contact1')
	   q.contact2=request.POST.get('contact2')  
	   q.clss=request.POST.get('clss')
	   q.rollno=request.POST.get('rollno')
	   if not q.barcode_serial:
	   	if q.clss != "None" and q.rollno != "None":
	   		q.barcode_serial=""
	   		if(q.course[0]=="B"):
	   			q.barcode_serial+="U"
	   		else:
	   			q.barcode_serial+="P"
	   		q.barcode_serial+=q.admissionNumber.split('/')[0]+q.admissionNumber.split('/')[1]
	   		q.barcode_serial+=str(q.clss) + str(q.rollno)
	   else:
	   	q.barcode_serial=request.POST.get('barcode_serial')
	   if(request.FILES.get('photo')):
	   	if q.photo:
	   		os.system('rm '+ root + q.photo.url)
	   	else:
	   		q.photo=request.FILES.get('photo')
	   q.save()
	   messages.success(request, 'Student Details Updated.')
	   return HttpResponseRedirect('/studentList')
   else:
	   return render(request,'home.html')
   
@login_required(login_url='/login/')
def facultySave(request):
   if request.method=='POST':
       q=faculty.objects.get(pk=request.POST['fac'])
       q.name=request.POST.get('name')
       q.designation=request.POST.get('designation')
       q.dateofbirth=request.POST.get('dateofbirth_year')+ "-" + request.POST.get('dateofbirth_month') + "-" + request.POST.get('dateofbirth_day')
       q.bloodgroup=request.POST.get('bloodgroup')
       q.address=request.POST.get('address')
       q.contact=request.POST.get('contact')
       if(request.FILES.get('photo')):
       	if q.photo:
       		os.system('rm '+ root + q.photo.url)
       	else:
       		q.photo=request.FILES.get('photo')
       q.save()
       messages.success(request, 'Faculty Details Updated.')
       return HttpResponseRedirect('/facultyList')
   else:
	   return render(request,'home.html')
   
@login_required(login_url='/login/')
def studentDelete(request):
   if request.method=='POST':
      try:
         q=student.objects.get(admissionNumber=request.POST.get('adm'))
         exist = ""
         if q.photo:
         	exist = root + q.photo.url
         q.delete()
         if exist:
         	os.system('rm '+exist)
      except ObjectDoesNotExist:
      	 messages.error(request, 'No match found!')
      	 return HttpResponseRedirect('/studentList')
      else:
      	 messages.success(request, 'Deleted Succesfully.')
      	 return HttpResponseRedirect('/studentList')
   else:
      return render(request,'studentList.html')          

@login_required(login_url='/login/')
def facultyDelete(request):
	if request.method=='POST':
		try:
			q=faculty.objects.get(name=request.POST.get('name'))
			exist = ""
			if q.photo:
				exist = root + q.photo.url
			q.delete()
			if exist:
				os.system('rm '+exist)
		except ObjectDoesNotExist:
			messages.error(request, 'No match found!')
			return HttpResponseRedirect('/facultyList')
		else:
			messages.success(request, 'Deleted Succesfully.')
			return HttpResponseRedirect('/facultyList')
	else:
		return render(request,'facultyList.html')          


@login_required(login_url='/login/')
def studentTemplateInput(request):
  try:
    instance = studentTemplateDesign.objects.get()
    return HttpResponseRedirect('/studentTemplate')
  except studentTemplateDesign.DoesNotExist:
    form = StudentTemplateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      return HttpResponseRedirect('/studentTemplate')
    context = {
      "form": form,
    }
    return render(request, "studentTemplateInput.html", context)


@login_required(login_url='/login/')
def studentTemplate(request):
  try:
    instance = studentTemplateDesign.objects.get()
    form = StudentTemplateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
    return render(request, "studentTemplate.html", {"form": form, "i":instance})
  except studentTemplateDesign.DoesNotExist:
    return HttpResponseRedirect('/studentTemplateInput')


@login_required(login_url='/login/')
def facultyTemplateInput(request):
  try:
    instance = facultyTemplateDesign.objects.get()
    return HttpResponseRedirect('/facultyTemplate')
  except facultyTemplateDesign.DoesNotExist:
    form = FacultyTemplateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      return HttpResponseRedirect('/facultyTemplate')
    context = {
      "form": form,
    }
    return render(request, "facultyTemplateInput.html", context)

@login_required(login_url='/login/')
def facultyTemplate(request):
  try:
    instance = facultyTemplateDesign.objects.get()
    form = FacultyTemplateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
    return render(request, "facultyTemplate.html", {"form": form, "i":instance})
  except facultyTemplateDesign.DoesNotExist:
    return HttpResponseRedirect('/facultyTemplateInput')

@login_required(login_url='/login/')
def facultyPdfPreview(request):
  details = facultyTemplateDesign.objects.get()
        #print str(details.backgroundDesign.url)[2:]
  back = root + '/media/' + str(details.backgroundDesign)
  pic = root + '/static/img/do_not_delete.jpg'
  princi = root + '/media/' + str(details.principalSign)
  logocentre = root + '/media/' + str(details.parentLogo)
  barcode_value = "U617513CSB99"
  barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
  width = 540*mm
  height = 860*mm
        #print str(details.collegeName)
  c = canvas.Canvas("pdf/"+'faculty.pdf')
  c.setPageSize((width, height))
  if details.backgroundDesign:
    c.drawImage(back, 0, 0, height=height, width=width)
  #c.saveState()
  if details.parentLogo:
    c.drawImage(logocentre, 210*mm, 750*mm, height=100*mm, width=100*mm)
  c.drawImage(pic, 170*mm, height-(540*mm), height=280*mm, width=200*mm)
  c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
  c.drawCentredString(width/2, 730*mm, str(details.collegeName))
  c.setFont(str(details.addline1font), int(details.addline1fontsize))
  c.drawCentredString(width/2, 710*mm, str(details.addressLine1))
  c.setFont(str(details.addressLine2To5Font), int(details.addressLine2To5FontSize))
  c.drawCentredString(width/2, 690*mm,str(details.addressLine2))
  #c.drawCentredString(width/2, height-(120*mm), "")
  c.drawCentredString(width/2, 670*mm, str(details.addressLine3))
  c.drawCentredString(width/2, 650*mm, str(details.addressLine4))
  c.drawCentredString(width/2, 630*mm, str(details.addressLine5))
  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
  c.drawString(50*mm, 250*mm, "Name ")
  c.drawString(190*mm, 250*mm, ": JOMY EMMANUEL")
  c.drawString(50*mm, 150*mm, "Designation ")
  c.drawString(190*mm, 150*mm, ": Assistant Professor")
  c.setFont('Times-Bold', 60)
  c.drawString(420*mm, 20*mm, "Principal")
  if details.principalSign:
  	c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
  c.showPage()

  c.setFont(str(details.detailsFont), int(details.detailsFontSize))
  c.drawString(30*mm, 760*mm, "Address ")
  c.drawString(210*mm, 760*mm, ": FLAT 2A")
  c.drawString(210*mm, 720*mm, "  SLYLINE BUILDERS")
  c.drawString(210*mm, 680*mm, "  APJ ROAD")
  c.drawString(210*mm, 640*mm, "  EDAPPALLY TOLL,")
  c.drawString(210*mm, 600*mm, "  EDAPPALLY P.O.")
  c.drawString(210*mm, 560*mm, "  682024")
  c.drawString(30*mm, 360*mm, "Contact No. ")
  c.drawString(210*mm, 360*mm, ": 0484-2657856")
  c.drawString(210*mm, 330*mm, "  9895462865")
  c.drawString(30*mm, 280*mm, "Blood Group ")
  c.drawString(210*mm, 280*mm, ": A+")
  c.drawString(30*mm, 220*mm, "Date Of Birth ")
  c.drawString(210*mm, 220*mm, ": 06/05/1995")
  barcode128.drawOn(c, 130*mm, 60*mm)
  c.drawCentredString(width/2, 30*mm, "MECF0000")
  c.save()

  with open("pdf/"+'faculty.pdf', 'rb') as pdf:
    response = HttpResponse(pdf.read(),content_type='application/pdf')
    response['Content-Disposition'] = 'filename=some_file.pdf'
    return response
  pdf.closed

@login_required(login_url='/login/')
def facultyPdf(request):
  details = facultyTemplateDesign.objects.all()
  if not len(details):
  	return HttpResponseRedirect('/facultyTemplateInput')
  details = facultyTemplateDesign.objects.get()
  q=faculty.objects.all()
  if q.__len__()==0:
  	return render(request,'home.html')
  #print str(details.backgroundDesign.url)[2:]
  back = root +'/media/'+str(details.backgroundDesign)
  princi = root + '/media/'+str(details.principalSign)
  logocentre = root+'/media/'+ str(details.parentLogo)
  width = 540*mm
  height = 860*mm
        #print str(details.collegeName)
  c = canvas.Canvas("pdf/"+'front1.pdf')
  for i in q:
    pic = root + i.photo.url
    c.setPageSize((width, height))
    if details.backgroundDesign:
      c.drawImage(back, 0, 0, height=height, width=width)
    #c.saveState()
    if details.parentLogo:
      c.drawImage(logocentre, 210*mm, 750*mm, height=100*mm, width=100*mm)
    if i.photo.url:
    	c.drawImage(pic, 170*mm, height-(540*mm), height=280*mm, width=200*mm)
    c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
    c.drawCentredString(width/2, 730*mm, str(details.collegeName))
    c.setFont(str(details.addline1font), int(details.addline1fontsize))
    c.drawCentredString(width/2, 710*mm, str(details.addressLine1))
    c.setFont(str(details.addressLine2To5Font), int(details.addressLine2To5FontSize))
    c.drawCentredString(width/2, 690*mm,str(details.addressLine2))
    #c.drawCentredString(width/2, height-(120*mm), "")
    c.drawCentredString(width/2, 670*mm, str(details.addressLine3))
    c.drawCentredString(width/2, 650*mm, str(details.addressLine4))
    c.drawCentredString(width/2, 630*mm, str(details.addressLine5))
    c.setFont(str(details.detailsFont), int(details.detailsFontSize))
    c.drawString(50*mm, 250*mm, "Name :")
    c.drawString(190*mm, 250*mm,i.name)
    c.drawString(50*mm, 150*mm, "Designation :")
    c.drawString(190*mm, 150*mm,i.designation)
    c.setFont('Times-Bold', 60)
    c.drawString(420*mm, 20*mm, "Principal")
    if details.principalSign:
    	c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
    c.showPage()
  c.save()
  c = canvas.Canvas("pdf/"+'back1.pdf')
  for i in q:
    c.setPageSize((width, height))
    c.setFont(str(details.detailsFont), int(details.detailsFontSize))
    c.drawString(30*mm, 760*mm, "Address ")
    #le=i.address.__len__()
    n=0
        #x=2
    ht=760
    y=re.split(',',i.address)
    for x in y:
	  c.drawString(210*mm, ht*mm,x)
	  ht=ht-40
    c.drawString(30*mm, 360*mm, "Contact No. :")
    c.drawString(210*mm, 360*mm,i.contact)
    c.drawString(30*mm, 280*mm, "Blood Group :")
    c.drawString(210*mm, 280*mm, i.bloodgroup)
    c.drawString(30*mm, 220*mm, "Date Of Birth :")
    c.drawString(210*mm, 220*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
    barcode128 = code128.Code128(i.barcode_serial, barHeight=50*mm, barWidth=1.5*mm)
    barcode128.drawOn(c, 130*mm, 60*mm)
    c.drawCentredString(width/2, 30*mm, i.barcode_serial)
    c.showPage()
  c.save()
  arch=zipfile.ZipFile("pdf/"+"id1.zip","w")
  arch.write("pdf/"+'front1.pdf')
  arch.write("pdf/"+'back1.pdf')
  arch.close()
  response = HttpResponse(open(root+"/pdf"+'/id1.zip', 'rb').read(), content_type='application/zip')
  response['Content-Disposition'] = 'attachment; filename=faculty.zip'
  return response
  return render(request,'home.html')

@login_required(login_url='/login/')
def studentList(request):
  queryset_list = student.objects.all()
  if queryset_list.__len__()==0:
   	messages.error(request, 'List is Empty!')
	return render(request,'studentList.html')

  paginator = Paginator(queryset_list, 50) # Show 50 contacts per page
  page = request.GET.get('page')
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    queryset = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    queryset = paginator.page(paginator.num_pages)


  context = {
    "object_list" : queryset
  }
  return render(request,'studentList.html', context)

@login_required(login_url='/login/')
def facultyList(request):
	queryset_list = faculty.objects.all()
	if queryset_list.__len__()==0:
		messages.error(request, 'List is Empty!')
		return render(request,'facultyList.html')

	context = {
		"object_list" : queryset_list
	}
	return render(request,'facultyList.html', context)


@login_required(login_url='/login/')
def singleStudent(request):
  if request.method=="POST":
    details=studentTemplateDesign.objects.all()
    if not len(details):
      return HttpResponseRedirect('/studentTemplateInput')
    else:
      details=studentTemplateDesign.objects.get()
      form=SingleStudentForm(request.POST,request.FILES)
      if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
      else:
        form=SingleStudentForm()
        error_message="Either "+request.POST['admissionNumber']+" exists or Form syntax is invalid"
        context={"form":form}
        messages.error(request, error_message)
        return render(request,'singleStudent.html',context)
      i=student.objects.get(admissionNumber=request.POST['admissionNumber'])
      back = root +'/media/'+str(details.backgroundDesign)
      princi = root + '/media/'+str(details.principalSign)
      logoright = root+'/media/'+ str(details.parentLogo)
      logoleft = root +'/media/'+ str(details.collegeLogo)
      width = 540*mm
      height = 860*mm
      c = canvas.Canvas("pdf/"+str(i.admissionNumber).split('/')[0]+'front.pdf')
      pic = root + i.photo.url
      c.setPageSize((width, height))
      if details.backgroundDesign:
        c.drawImage(back, 0, 0, height=height, width=width)
    #c.saveState()
      if details.collegeLogo:
        c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
      if details.parentLogo:
        c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
      c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
      c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
      #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
      c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
      c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
      if i.photo.url:
      	c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
      c.setFont(str(details.detailsFont), int(details.detailsFontSize))
      c.drawString(30*mm, 430*mm, "Name :")
      c.drawString(165*mm, 430*mm,i.name)
      c.setFont(str(details.detailsFont), int(details.detailsFontSize))
      c.drawString(30*mm, 340*mm, "Course :")
      c.drawString(165*mm, 340*mm,i.course)
      c.drawString(30*mm, 280*mm, "Branch :")
      c.drawString(165*mm, 280*mm, i.branch)
      c.drawString(30*mm, 180*mm, "ADMN No :")
      c.drawString(165*mm, 180*mm, i.admissionNumber)
      c.drawString(30*mm, 120*mm, "Valid Till:")
      c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
      c.drawString(30*mm, 60*mm, "Date Of Birth:")
      c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
      c.setFont('Times-Bold', 60)
      c.drawString(420*mm, 20*mm, "Principal")
      if details.principalSign:
        c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
      c.showPage()
      c.save()
      c = canvas.Canvas("pdf/"+str(i.admissionNumber).split('/')[0]+'back.pdf')
      barcode_value = ""
      if(i.course[0]=="B"):
        barcode_value+="U"
      else:
        barcode_value+="P"
      barcode_value+=i.admissionNumber.split('/')[0]+i.admissionNumber.split('/')[1]
      barcode_value+=str(i.clss)
      barcode_value+=str(i.rollno)
      barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
      c.setPageSize((width, height))
      c.setFont(str(details.detailsFont), int(details.detailsFontSize))
      barcode128.drawOn(c, 130*mm, 750*mm)
      c.drawString(190*mm, 720*mm, barcode_value)
      c.drawString(30*mm, 630*mm, "Blood Group :")
      c.drawString(210*mm, 630*mm,i.bloodgroup)
      c.drawString(30*mm, 550*mm, "Address :")
      #le=i.address.__len__()
      n=0
          #x=2
      ht=550
      y=re.split(',',i.address)
      for x in y:
        c.drawString(210*mm, ht*mm,x)
        ht=ht-40

      c.drawString(30*mm, 170*mm, "Contact No. :")
      c.drawString(210*mm, 170*mm,i.contact1)
      c.drawString(210*mm, 140*mm,i.contact2)
      c.drawString(30*mm, 60*mm, "Signature     :")
      c.rect(160*mm,30*mm,320*mm,70*mm)
      c.showPage()
      c.save()

      arch=zipfile.ZipFile("pdf/"+"i.zip","w")
      arch.write("pdf/"+str(i.admissionNumber).split('/')[0]+'front.pdf')
      arch.write("pdf/"+str(i.admissionNumber).split('/')[0]+'back.pdf')
      arch.close()
      adf="pdf/"+i.admissionNumber.split('/')[0]+'front.pdf'
      adb="pdf/"+i.admissionNumber.split('/')[0]+'back.pdf'
      pho= root + i.photo.url
      i.delete()
      os.system('rm '+pho)
      os.system('rm '+adb)
      os.system('rm '+adf)
      response = HttpResponse(open(root+"/pdf"+'/i.zip', 'rb').read(), content_type='application/zip')
      response['Content-Disposition'] = 'attachment; filename=single.zip'
      return response
  else:
    form=SingleStudentForm()
    return render(request,'singleStudent.html',{'form':form})

@login_required(login_url='/login/')
def report(request):
  if request.method=="POST":
    details=studentTemplateDesign.objects.all()
    if not len(details):
      return HttpResponseRedirect('/studentTemplateInput')
    else:
      details=studentTemplateDesign.objects.get()
      form=StudentForm(request.POST,request.FILES)
      if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
      else:
        form=StudentForm()
        error_message="Either "+request.POST['admissionNumber']+" exists or Form syntax is invalid"
        context={"form":form}
        messages.error(request, error_message)
        return render(request,'studentform.html',context)
      i=student.objects.get(admissionNumber=request.POST['admissionNumber'])
      back = root +'/media/'+str(details.backgroundDesign)
      princi = root + '/media/'+str(details.principalSign)
      logoright = root+'/media/'+ str(details.parentLogo)
      logoleft = root +'/media/'+ str(details.collegeLogo)
      width = 540*mm
      height = 860*mm
      c = canvas.Canvas("pdf/"+str(i.admissionNumber).split('/')[0]+'front.pdf')
      c.setPageSize((width, height))
      if details.backgroundDesign:
        c.drawImage(back, 0, 0, height=height, width=width)
    #c.saveState()
      if details.collegeLogo:
        c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
      if details.parentLogo:
        c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
      c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
      c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
      #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
      c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
      c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
      c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
      c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
      c.setFont(str(details.detailsFont), int(details.detailsFontSize))
      c.drawString(30*mm, 630*mm, "Name :")
      c.drawString(165*mm, 630*mm,i.name)
      c.setFont(str(details.detailsFont), int(details.detailsFontSize))
      c.drawString(30*mm, 560*mm, "Course :")
      c.drawString(165*mm, 560*mm,i.course)
      c.drawString(30*mm, 500*mm, "Type :")
      c.drawString(165*mm, 500*mm,i.typ)
      c.drawString(30*mm, 440*mm, "Branch :")
      c.drawString(165*mm, 440*mm, i.branch)
      c.drawString(30*mm, 370*mm, "ADMN No :")
      c.drawString(165*mm, 370*mm, i.admissionNumber)
      c.drawString(30*mm, 320*mm, "Valid Till:")
      c.drawString(165*mm, 320*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
      c.drawString(30*mm, 260*mm, "Date Of Birth:")
      c.drawString(165*mm, 260*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
      c.drawString(30*mm, 200*mm, "Address :")
      #le=i.address.__len__()
      n=0
          #x=2
      ht=200
      y=re.split(',',i.address)
      for x in y:
        c.drawString(165*mm, ht*mm,x)
        ht=ht-30

      c.drawString(30*mm, 70*mm, "Contact No. :")
      c.drawString(165*mm, 70*mm,i.contact1)

      c.showPage()
      c.save()
      
      arch=zipfile.ZipFile("pdf/"+"t.zip","w")
      arch.write("pdf/"+str(i.admissionNumber).split('/')[0]+'front.pdf')
     
      arch.close()
      response = HttpResponse(open(root+"/pdf"+'/t.zip', 'rb').read(), content_type='application/zip')
      response['Content-Disposition'] = 'attachment; filename=report.zip'
      return response
  else:
    form=StudentForm()
    context={"form":form}
    return render(request,'studentform.html',context)




  