from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_str
# imports for reportlab pdfgeneration
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .forms import StudentForm,FacultyForm,Sd, Fd,SingleStud
from .models import stud,faculty,SDesign, FDesign
import os
import re
import urllib2
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
def mainstu(request):
   return render(request,'homestu.html')

@login_required(login_url='/login/')
def mainfac(request):
   return render(request,'homefac.html')

@login_required(login_url='/login/')
def student(request):
   if request.method=='POST':
     try:
      a=stud.objects.get(admno=request.POST.get("admno"))
     except:
      form=StudentForm(request.POST,request.FILES)
      if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request, 'Student Registered Succesfully.')
        return HttpResponseRedirect('/student') 
      else:
         form=StudentForm()
         context={"form":form}
         messages.error(request, 'Form Not Valid.')
         return render(request,'studentform.html',context)
     form=StudentForm()
     context={"form":form}
     messages.error(request, 'Student Exists.')
     return render(request,'studentform.html',context)
   else:
    form=StudentForm()
    context={"form":form}
    return render(request,'studentform.html',context)

@login_required(login_url='/login/')
def faculty1(request):
   if request.method=='POST':
    try:
      a=faculty.objects.get(name=request.POST.get("name"))
    except:
     form=FacultyForm(request.POST,request.FILES)
     if form.is_valid():
       instance=form.save(commit=False)
       instance.save()
       messages.success(request, 'Faculty Registered Succesfully.')
       return HttpResponseRedirect('/faculty') 
     else:
       form=FacultyForm()
       context={"form":form}
       messages.error(request, 'Form Not Valid.')
       return render(request,'facultyform.html',context)
    form=FacultyForm()
    context={"form":form}
    messages.error(request, 'Faculty Exists.')
    return render(request,'facultyform.html',context)
   else:
     #errormsg="Method not POST"
     form=FacultyForm()
     context={"form":form}
     return render(request,'facultyform.html',context)


@login_required(login_url='/login/')
def studentEdit(request, id=None):
  q = get_object_or_404(stud, id=id)
  return render(request,'studeditform.html',{'i':q})

@login_required(login_url='/login/')
def facultyEdit(request, id=None):
  q = get_object_or_404(faculty, id=id)
  return render(request,'faceditform.html',{'i':q})

@login_required(login_url='/login/')
def studentpdfhome(request):
	return render(request,'genpdf.html')

@login_required(login_url='/login/')
def generatepdf(request):
	details=SDesign.objects.get()
	if details is None:
		return HttpResponseRedirect('/siddesign')
	if request.method=="POST":
		try:
			smallest=100000000
			largest=0
			for i in stud.objects.all():
			    a=int(i.admno.split('/')[0])
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
			for i in stud.objects.all():
				if((int(i.admno.split('/')[0])>=a)and(int(i.admno.split('/')[0])<=b)):
					q.append(i)

			if q.__len__()==0:
			  	return render(request,'home.html')
			details=SDesign.objects.get()
			back = root + '/media/'+ str(details.bdesign)
			princi = root + '/media/'+ str(details.psign)
			logoright = root + '/media/'+ str(details.ilogo)
			logoleft = root + '/media/'+ str(details.clogo)
			width = 540*mm
			height = 860*mm
			c = canvas.Canvas("pdf/"+'rangefront.pdf')
			for i in q:
			  pic = root + i.photo.url
			  c.setPageSize((width, height))
			  if back:
			    c.drawImage(back, 0, 0, height=height, width=width)
			#c.saveState()
			  if logoleft:
			    c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
			  if logoright:
			    c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
			  c.setFont(str(details.cfont), int(details.cfontsize))
			  c.drawCentredString(width/2, height-(60*mm),str(details.college))
			  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
			  c.drawCentredString(width/2, height-(80*mm),str(details.addline1))
			  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
			  c.drawCentredString(width/2, height-(100*mm), str(details.addline2))
			  #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
			  c.drawCentredString(width/2, height-(120*mm),str(details.addline3))
			  c.drawCentredString(width/2, height-(140*mm),str(details.addline4))
			  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
			  c.drawCentredString(width/2, height-(160*mm), str(details.addline5))
			  c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
			  c.setFont(str(details.detfont), int(details.detfontsize))
			  c.drawString(30*mm, 430*mm, "Name ")
			  c.drawString(165*mm, 430*mm,i.name)
			  c.setFont(str(details.detfont), int(details.detfontsize))
			  c.drawString(30*mm, 340*mm, "Course :")
			  c.drawString(165*mm, 340*mm,i.course)
			  c.drawString(30*mm, 280*mm, "Branch :")
			  c.drawString(165*mm, 280*mm, i.branch)
			  c.drawString(30*mm, 180*mm, "ADMN No :")
			  c.drawString(165*mm, 180*mm, i.admno)
			  c.drawString(30*mm, 120*mm, "Valid Till:")
			  c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
			  c.drawString(30*mm, 60*mm, "Date Of Birth:")
			  c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
			  c.setFont('Times-Bold', 60)
			  c.drawString(420*mm, 20*mm, "Principal")
			  if princi:
			    c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
			  c.showPage()
			c.save()
			c = canvas.Canvas("pdf/"+'rangeback.pdf')
			for i in q:
			  barcode_value = ""
			  if(i.course[0]=="B"):
			    barcode_value+="U"
			  else:
			    barcode_value+="P"
			  barcode_value+=i.admno.split('/')[0]+i.admno.split('/')[1]
			  barcode_value+=str(i.clss)
			  barcode_value+=str(i.rollno)
			  barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
			  c.setPageSize((width, height))
			  c.setFont(str(details.detfont), int(details.detfontsize))
			  barcode128.drawOn(c, 130*mm, 750*mm)
			  c.drawString(190*mm, 720*mm, barcode_value)
			  c.drawString(30*mm, 630*mm, "Blood Group ")
			  c.drawString(210*mm, 630*mm,i.bloodgroup)
			  c.drawString(30*mm, 550*mm, "Address ")
			  le=i.address.__len__()
			  n=0
			      #x=2
			  ht=550
			  y=re.split(',',i.address)
			  y=re.split(',',i.address)
			  for x in y:
			    c.drawString(210*mm, ht*mm,x)
			    ht=ht-40
			  #c.drawString(210*mm, 550*mm, ": FLAT 2A")
			  #c.drawString(210*mm, 500*mm, "  SLYLINE BUILDERS")
			  #c.drawString(210*mm, 450*mm, "  APJ ROAD")
			  #c.drawString(210*mm, 400*mm, "  EDAPPALLY TOLL,")
			  #c.drawString(210*mm, 350*mm, "  EDAPPALLY P.O.")
			  #c.drawString(210*mm, 300*mm, "  682024")
			  c.drawString(30*mm, 170*mm, "Contact No. ")
			  c.drawString(210*mm, 170*mm,i.contact1)
			  c.drawString(210*mm, 140*mm,i.contact2)
			  c.drawString(30*mm, 60*mm, "Signature     :")
			  c.rect(160*mm,30*mm,320*mm,70*mm)
			  c.showPage()
			c.save()
			     ###### TO DISPLAY PDF VIA BROWSER  ###
			     #with open('amal.pdf', 'rb') as pdf:
			     #   response = HttpResponse(pdf.read(),content_type='application/pdf')
			     #   response['Content-Disposition'] = 'filename=some_file.pdf'
			     #   return response
			     #pdf.closed
			arch=zipfile.ZipFile("pdf/"+"range.zip","w")
			arch.write("pdf/"+'rangefront.pdf')
			arch.write("pdf/"+'rangeback.pdf')
			arch.close()
			response = HttpResponse(open(root+"/pdf"+'/range.zip', 'rb').read(), content_type='application/zip')
			response['Content-Disposition'] = 'attachment; filename=range.zip'
			return response
			return render(request,'home.html')				
		except:
		    return HttpResponseRedirect('/')
	else:
	  q=stud.objects.all()
	  if q.__len__()==0:
	  	return render(request,'home.html')
	  details=SDesign.objects.get()
	  back = root + '/media/'+ str(details.bdesign)
	  princi = root + '/media/'+ str(details.psign)
	  logoright = root + '/media/'+ str(details.ilogo)
	  logoleft = root + '/media/'+ str(details.clogo)
	  width = 540*mm
	  height = 860*mm
	  c = canvas.Canvas("pdf/"+'front.pdf')
	  for i in q:
	    pic = root + i.photo.url
	    c.setPageSize((width, height))
	    if back:
	      c.drawImage(back, 0, 0, height=height, width=width)
	  #c.saveState()
	    if logoleft:
	      c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
	    if logoright:
	      c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
	    c.setFont(str(details.cfont), int(details.cfontsize))
	    c.drawCentredString(width/2, height-(60*mm),str(details.college))
	    c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
	    c.drawCentredString(width/2, height-(80*mm),str(details.addline1))
	    c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
	    c.drawCentredString(width/2, height-(100*mm), str(details.addline2))
	    #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
	    c.drawCentredString(width/2, height-(120*mm),str(details.addline3))
	    c.drawCentredString(width/2, height-(140*mm),str(details.addline4))
	    c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
	    c.drawCentredString(width/2, height-(160*mm), str(details.addline5))
	    c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
	    c.setFont(str(details.detfont), int(details.detfontsize))
	    c.drawString(30*mm, 430*mm, "Name ")
	    c.drawString(165*mm, 430*mm,i.name)
	    c.setFont(str(details.detfont), int(details.detfontsize))
	    c.drawString(30*mm, 340*mm, "Course :")
	    c.drawString(165*mm, 340*mm,i.course)
	    c.drawString(30*mm, 280*mm, "Branch :")
	    c.drawString(165*mm, 280*mm, i.branch)
	    c.drawString(30*mm, 180*mm, "ADMN No :")
	    c.drawString(165*mm, 180*mm, i.admno)
	    c.drawString(30*mm, 120*mm, "Valid Till:")
	    c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
	    c.drawString(30*mm, 60*mm, "Date Of Birth:")
	    c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
	    c.setFont('Times-Bold', 60)
	    c.drawString(420*mm, 20*mm, "Principal")
	    if princi:
	      c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
	    c.showPage()
	  c.save()
	  c = canvas.Canvas("pdf/"+'back.pdf')
	  for i in q:
	    barcode_value = ""
	    if(i.course[0]=="B"):
	      barcode_value+="U"
	    else:
	      barcode_value+="P"
	    barcode_value+=i.admno.split('/')[0]+i.admno.split('/')[1]
	    barcode_value+=str(i.clss)
	    barcode_value+=str(i.rollno)
	    barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
	    c.setPageSize((width, height))
	    c.setFont(str(details.detfont), int(details.detfontsize))
	    barcode128.drawOn(c, 130*mm, 750*mm)
	    c.drawString(190*mm, 720*mm, barcode_value)
	    c.drawString(30*mm, 630*mm, "Blood Group ")
	    c.drawString(210*mm, 630*mm,i.bloodgroup)
	    c.drawString(30*mm, 550*mm, "Address ")
	    le=i.address.__len__()
	    n=0
	        #x=2
	    ht=550
	    y=re.split(',',i.address)
	    y=re.split(',',i.address)
	    for x in y:
	      c.drawString(210*mm, ht*mm,x)
	      ht=ht-40
	    #c.drawString(210*mm, 550*mm, ": FLAT 2A")
	    #c.drawString(210*mm, 500*mm, "  SLYLINE BUILDERS")
	    #c.drawString(210*mm, 450*mm, "  APJ ROAD")
	    #c.drawString(210*mm, 400*mm, "  EDAPPALLY TOLL,")
	    #c.drawString(210*mm, 350*mm, "  EDAPPALLY P.O.")
	    #c.drawString(210*mm, 300*mm, "  682024")
	    c.drawString(30*mm, 170*mm, "Contact No. ")
	    c.drawString(210*mm, 170*mm,i.contact1)
	    c.drawString(210*mm, 140*mm,i.contact2)
	    c.drawString(30*mm, 60*mm, "Signature     :")
	    c.rect(160*mm,30*mm,320*mm,70*mm)
	    c.showPage()
	  c.save()
	       ###### TO DISPLAY PDF VIA BROWSER  ###
	       #with open('amal.pdf', 'rb') as pdf:
	       #   response = HttpResponse(pdf.read(),content_type='application/pdf')
	       #   response['Content-Disposition'] = 'filename=some_file.pdf'
	       #   return response
	       #pdf.closed
	  arch=zipfile.ZipFile("pdf/"+"id.zip","w")
	  arch.write("pdf/"+'front.pdf')
	  arch.write("pdf/"+'back.pdf')
	  arch.close()
	  response = HttpResponse(open(root+"/pdf"+'/id.zip', 'rb').read(), content_type='application/zip')
	  response['Content-Disposition'] = 'attachment; filename=student.zip'
	  return response
	  return render(request,'home.html')

@login_required(login_url='/login/')
def rlab(request):
  details = SDesign.objects.get()
        #print str(details.bdesign.url)[2:]
  back = root + '/media/'+ str(details.bdesign)
  pic = root + '/static/img/do_not_delete.jpg'
  princi = root + '/media/' + str(details.psign)
  logoright = root+ '/media/' +  str(details.ilogo)
  logoleft = root + '/media/' +  str(details.clogo)
  barcode_value = "U617513CSB99"
  barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
  width = 540*mm
  height = 860*mm
        #print str(details.college)
  c = canvas.Canvas("pdf/"+'student.pdf')
  c.setPageSize((width, height))
  if back:
    c.drawImage(back, 0, 0, height=height, width=width)
  #c.saveState()
  if logoleft:
    c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
  if logoright:
    c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
  c.setFont(str(details.cfont), int(details.cfontsize))
  c.drawCentredString(width/2, height-(60*mm),str(details.college))
  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
  c.drawCentredString(width/2, height-(80*mm),str(details.addline1))
  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
  c.drawCentredString(width/2, height-(100*mm), str(details.addline2))
  #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
  c.drawCentredString(width/2, height-(120*mm),str(details.addline3))
  c.drawCentredString(width/2, height-(140*mm),str(details.addline4))
  c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
  c.drawCentredString(width/2, height-(160*mm), str(details.addline5))
  c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
  c.setFont(str(details.detfont), int(details.detfontsize))
  c.drawString(30*mm, 430*mm, "Name ")
  c.drawString(165*mm, 430*mm, ": JOMY EMMANUEL")
  c.setFont(str(details.detfont), int(details.detfontsize))
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
  if princi:
    c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
  c.showPage()

  c.setFont(str(details.detfont), int(details.detfontsize))
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
def editstud(request):
	if request.method=='POST':
		for i in stud.objects.all():
			i.clss=request.POST['clss'+str(i.pk)]
			i.branch=request.POST['branch'+str(i.pk)]
			i.rollno=request.POST['rollno'+str(i.pk)]
			i.save()
		messages.success(request, 'Details Updated.')
		return HttpResponseRedirect('/liststud')
	else:
		return render(request,'home.html')        
   
@login_required(login_url='/login/')
def editfac(request):
	if request.method=='POST':
		return render(request,'faceditform.html',{'i':q}) 	
	else:
		return render(request,'home.html')

	    
      
@login_required(login_url='/login/')
def studsave(request):
   if request.method=='POST':
	   q=stud.objects.get(pk=request.POST['stu'])
	   q.name=request.POST.get('name')
	   q.course=request.POST.get('course')
	   q.branch=request.POST.get('branch')
	   q.admno=request.POST.get('admno')
	   q.validtill=request.POST.get('validtill')
	   q.dateofbirth=request.POST.get('dateofbirth')
	   q.bloodgroup=request.POST.get('bloodgroup')
	   q.address=request.POST.get('address')
	   q.contact1=request.POST.get('contact1')
	   q.contact2=request.POST.get('contact2')  
	   q.clss=request.POST.get('clss')
	   q.rollno=request.POST.get('rollno')
	   if(request.FILES.get('photo')):
	       os.system('rm '+ root + q.photo.url)
	       q.photo=request.FILES.get('photo')
	   q.save()
	   messages.success(request, 'Student Details Updated.')
	   return HttpResponseRedirect('/liststud')
   else:
	   return render(request,'home.html')
   
@login_required(login_url='/login/')
def facsave(request):
   if request.method=='POST':
       q=faculty.objects.get(pk=request.POST['fac'])
       q.name=request.POST.get('name')
       q.designation=request.POST.get('designation')
       q.dateofbirth=request.POST.get('dateofbirth')
       q.bloodgroup=request.POST.get('bloodgroup')
       q.address=request.POST.get('address')
       q.contact=request.POST.get('contact')
       if(request.FILES.get('photo')):
           os.system('rm '+ root + q.photo.url)
           q.photo=request.FILES.get('photo')
       q.save()
       messages.success(request, 'Faculty Details Updated.')
       return HttpResponseRedirect('/listfac')
   else:
	   return render(request,'home.html')
   
@login_required(login_url='/login/')
def delstud(request):
   if request.method=='POST':
      try:
         q=stud.objects.get(admno=request.POST['adm'])
         pho= root + q.photo.url
         q.delete()
         os.system('rm '+pho)
      except ObjectDoesNotExist:
      	 messages.error(request, 'No match found!')
      	 return render(request,'studel.html')
      else:
      	 messages.success(request, 'Deleted Succesfully.')
      	 return HttpResponseRedirect('/studel')
   else:
      return render(request,'studel.html')          

@login_required(login_url='/login/')
def delfac(request):
   if request.method=='POST':
      try:
         q=faculty.objects.get(name=request.POST['name'])
         pho= root + q.photo.url
         q.delete()
         os.system('rm '+pho)
      except ObjectDoesNotExist:
         messages.error(request, 'No match found!')
      	 return render(request,'facdel.html')
      else:
      	 messages.success(request, 'Deleted Succesfully.')
      	 return HttpResponseRedirect('/facdel')
   else:
      return render(request,'facdel.html')          


@login_required(login_url='/login/')
def siddesign(request):
  try:
    instance = SDesign.objects.get()
    return HttpResponseRedirect('/pdfsdesign')
  except SDesign.DoesNotExist:
    form = Sd(request.POST or None, request.FILES or None)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      return HttpResponseRedirect('/pdfsdesign')
    context = {
      "form": form,
    }
    return render(request, "siddesign.html", context)
    #return HttpResponseRedirect('/pdfsdesign')


@login_required(login_url='/login/')
def pdfsdesign(request):
  try:
    instance = SDesign.objects.get()
    form = Sd(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
    return render(request, "pdfsdesign.html", {"form": form, "i":instance})
  except SDesign.DoesNotExist:
    return HttpResponseRedirect('/siddesign')


@login_required(login_url='/login/')
def fiddesign(request):
  try:
    instance = FDesign.objects.get()
    return HttpResponseRedirect('/pdffdesign')
  except FDesign.DoesNotExist:
    form = Fd(request.POST or None, request.FILES or None)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
      return HttpResponseRedirect('/pdffdesign')
    context = {
      "form": form,
    }
    return render(request, "fiddesign.html", context)
    #return HttpResponseRedirect('/pdfsdesign')

@login_required(login_url='/login/')
def pdffdesign(request):
  try:
    instance = FDesign.objects.get()
    form = Fd(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.save()
    return render(request, "pdffdesign.html", {"form": form, "i":instance})
  except FDesign.DoesNotExist:
    return HttpResponseRedirect('/fiddesign')

@login_required(login_url='/login/')
def flab(request):
  details = FDesign.objects.get()
        #print str(details.bdesign.url)[2:]
  back = root + '/media/' + str(details.bdesign)
  pic = root + '/static/img/do_not_delete.jpg'
  princi = root + '/media/' + str(details.psign)
  logocentre = root + '/media/' + str(details.ilogo)
  barcode_value = "U617513CSB99"
  barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
  width = 540*mm
  height = 860*mm
        #print str(details.college)
  c = canvas.Canvas("pdf/"+'faculty.pdf')
  c.setPageSize((width, height))
  if back:
    c.drawImage(back, 0, 0, height=height, width=width)
  #c.saveState()
  if logocentre:
    c.drawImage(logocentre, 210*mm, 750*mm, height=100*mm, width=100*mm)
  c.drawImage(pic, 170*mm, height-(540*mm), height=280*mm, width=200*mm)
  c.setFont(str(details.cfont), int(details.cfontsize))
  c.drawCentredString(width/2, 730*mm, str(details.college))
  c.setFont(str(details.addline1font), int(details.addline1fontsize))
  c.drawCentredString(width/2, 710*mm, str(details.addline1))
  c.setFont(str(details.addline2to5font), int(details.addline2to5fontsize))
  c.drawCentredString(width/2, 690*mm,str(details.addline2))
  #c.drawCentredString(width/2, height-(120*mm), "")
  c.drawCentredString(width/2, 670*mm, str(details.addline3))
  c.drawCentredString(width/2, 650*mm, str(details.addline4))
  c.drawCentredString(width/2, 630*mm, str(details.addline5))
  c.setFont(str(details.detfont), int(details.detfontsize))
  c.drawString(50*mm, 250*mm, "Name ")
  c.drawString(190*mm, 250*mm, ": JOMY EMMANUEL")
  c.drawString(50*mm, 150*mm, "Designation ")
  c.drawString(190*mm, 150*mm, ": Assistant Professor")
  c.setFont('Times-Bold', 60)
  c.drawString(420*mm, 20*mm, "Principal")
  c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
  c.showPage()

  c.setFont(str(details.detfont), int(details.detfontsize))
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
def genpdf1(request):
  details = FDesign.objects.get()
  if details is None:
  	return HttpResponseRedirect('/fiddesign')
  q=faculty.objects.all()
  if q.__len__()==0:
  	return render(request,'home.html')
  #print str(details.bdesign.url)[2:]
  back = root +'/media/'+str(details.bdesign)
  princi = root + '/media/'+str(details.psign)
  logocentre = root+'/media/'+ str(details.ilogo)
  barcode_value = "MECF000"
  width = 540*mm
  height = 860*mm
        #print str(details.college)
  c = canvas.Canvas("pdf/"+'front1.pdf')
  for i in q:
    pic = root + i.photo.url
    c.setPageSize((width, height))
    if back:
      c.drawImage(back, 0, 0, height=height, width=width)
    #c.saveState()
    if logocentre:
      c.drawImage(logocentre, 210*mm, 750*mm, height=100*mm, width=100*mm)
    c.drawImage(pic, 170*mm, height-(540*mm), height=280*mm, width=200*mm)
    c.setFont(str(details.cfont), int(details.cfontsize))
    c.drawCentredString(width/2, 730*mm, str(details.college))
    c.setFont(str(details.addline1font), int(details.addline1fontsize))
    c.drawCentredString(width/2, 710*mm, str(details.addline1))
    c.setFont(str(details.addline2to5font), int(details.addline2to5fontsize))
    c.drawCentredString(width/2, 690*mm,str(details.addline2))
    #c.drawCentredString(width/2, height-(120*mm), "")
    c.drawCentredString(width/2, 670*mm, str(details.addline3))
    c.drawCentredString(width/2, 650*mm, str(details.addline4))
    c.drawCentredString(width/2, 630*mm, str(details.addline5))
    c.setFont(str(details.detfont), int(details.detfontsize))
    c.drawString(50*mm, 250*mm, "Name ")
    c.drawString(190*mm, 250*mm,i.name)
    c.drawString(50*mm, 150*mm, "Designation ")
    c.drawString(190*mm, 150*mm,i.designation)
    c.setFont('Times-Bold', 60)
    c.drawString(420*mm, 20*mm, "Principal")
    c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
    c.showPage()
  c.save()
  c = canvas.Canvas("pdf/"+'back1.pdf')
  for i in q:
    c.setPageSize((width, height))
    c.setFont(str(details.detfont), int(details.detfontsize))
    c.drawString(30*mm, 760*mm, "Address ")
    #le=i.address.__len__()
    n=0
        #x=2
    ht=760
    y=re.split(',',i.address)
    for x in y:
	  c.drawString(210*mm, ht*mm,x)
	  ht=ht-40
    c.drawString(30*mm, 360*mm, "Contact No. ")
    c.drawString(210*mm, 360*mm,i.contact)
    c.drawString(30*mm, 280*mm, "Blood Group ")
    c.drawString(210*mm, 280*mm, i.bloodgroup)
    c.drawString(30*mm, 220*mm, "Date Of Birth ")
    c.drawString(210*mm, 220*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
    barcode128 = code128.Code128(barcode_value+str(i.pk), barHeight=50*mm, barWidth=1.5*mm)
    barcode128.drawOn(c, 130*mm, 60*mm)
    c.drawCentredString(width/2, 30*mm, "MECF000"+str(i.pk))
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
def liststud(request):
  queryset_list = stud.objects.all()
  if queryset_list.__len__()==0:
   	messages.error(request, 'List is Empty!')
	return render(request,'liststud.html')

  paginator = Paginator(queryset_list, 30) # Show 25 contacts per page
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
  return render(request,'liststud.html', context)

@login_required(login_url='/login/')
def listfac(request):
	queryset_list = faculty.objects.all()
	if queryset_list.__len__()==0:
		messages.error(request, 'List is Empty!')
		return render(request,'listfac.html')

	context = {
		"object_list" : queryset_list
	}
	return render(request,'listfac.html', context)


@login_required(login_url='/login/')
def singlestud(request):
  if request.method=="POST":
    details=SDesign.objects.get()
    if details is None:
      return HttpResponseRedirect('/siddesign')
    else:
      form=SingleStud(request.POST,request.FILES)
      if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
      else:
        form=SingleStud()
        error_message="Either "+request.POST['admno']+" exists or Form syntax is invalid"
        context={"form":form}
        messages.error(request, error_message)
        return render(request,'singlestud.html',context)
      i=stud.objects.get(admno=request.POST['admno'])
      back = root +'/media/'+str(details.bdesign)
      princi = root + '/media/'+str(details.psign)
      logoright = root+'/media/'+ str(details.ilogo)
      logoleft = root +'/media/'+ str(details.clogo)
      width = 540*mm
      height = 860*mm
      c = canvas.Canvas("pdf/"+str(i.admno).split('/')[0]+'front.pdf')
      pic = root + i.photo.url
      c.setPageSize((width, height))
      if back:
        c.drawImage(back, 0, 0, height=height, width=width)
    #c.saveState()
      if logoleft:
        c.drawImage(logoleft, 20*mm, 740*mm, height=80*mm, width=80*mm)
      if logoright:
        c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
      c.setFont(str(details.cfont), int(details.cfontsize))
      c.drawCentredString(width/2, height-(60*mm),str(details.college))
      c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
      c.drawCentredString(width/2, height-(80*mm),str(details.addline1))
      c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
      c.drawCentredString(width/2, height-(100*mm), str(details.addline2))
      #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
      c.drawCentredString(width/2, height-(120*mm),str(details.addline3))
      c.drawCentredString(width/2, height-(140*mm),str(details.addline4))
      c.setFont(str(details.addline1to5font), int(details.addline1to5fontsize))
      c.drawCentredString(width/2, height-(160*mm), str(details.addline5))
      c.drawImage(pic, 170*mm, height-(375*mm), height=200*mm, width=200*mm)
      c.setFont(str(details.detfont), int(details.detfontsize))
      c.drawString(30*mm, 430*mm, "Name ")
      c.drawString(165*mm, 430*mm,i.name)
      c.setFont(str(details.detfont), int(details.detfontsize))
      c.drawString(30*mm, 340*mm, "Course :")
      c.drawString(165*mm, 340*mm,i.course)
      c.drawString(30*mm, 280*mm, "Branch :")
      c.drawString(165*mm, 280*mm, i.branch)
      c.drawString(30*mm, 180*mm, "ADMN No :")
      c.drawString(165*mm, 180*mm, i.admno)
      c.drawString(30*mm, 120*mm, "Valid Till:")
      c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
      c.drawString(30*mm, 60*mm, "Date Of Birth:")
      c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
      c.setFont('Times-Bold', 60)
      c.drawString(420*mm, 20*mm, "Principal")
      if princi:
        c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
      c.showPage()
      c.save()
      c = canvas.Canvas("pdf/"+str(i.admno).split('/')[0]+'back.pdf')
      barcode_value = ""
      if(i.course[0]=="B"):
        barcode_value+="U"
      else:
        barcode_value+="P"
      barcode_value+=i.admno.split('/')[0]+i.admno.split('/')[1]
      barcode_value+=str(i.clss)
      barcode_value+=str(i.rollno)
      barcode128 = code128.Code128(barcode_value, barHeight=50*mm, barWidth=1.5*mm)
      c.setPageSize((width, height))
      c.setFont(str(details.detfont), int(details.detfontsize))
      barcode128.drawOn(c, 130*mm, 750*mm)
      c.drawString(190*mm, 720*mm, barcode_value)
      c.drawString(30*mm, 630*mm, "Blood Group ")
      c.drawString(210*mm, 630*mm,i.bloodgroup)
      c.drawString(30*mm, 550*mm, "Address ")
      #le=i.address.__len__()
      n=0
          #x=2
      ht=550
      y=re.split(',',i.address)
      for x in y:
        c.drawString(210*mm, ht*mm,x)
        ht=ht-40
      #c.drawString(210*mm, 550*mm, ": FLAT 2A")
      #c.drawString(210*mm, 500*mm, "  SLYLINE BUILDERS")
      #c.drawString(210*mm, 450*mm, "  APJ ROAD")
      #c.drawString(210*mm, 400*mm, "  EDAPPALLY TOLL,")
      #c.drawString(210*mm, 350*mm, "  EDAPPALLY P.O.")
      #c.drawString(210*mm, 300*mm, "  682024")
      c.drawString(30*mm, 170*mm, "Contact No. ")
      c.drawString(210*mm, 170*mm,i.contact1)
      c.drawString(210*mm, 140*mm,i.contact2)
      c.drawString(30*mm, 60*mm, "Signature     :")
      c.rect(160*mm,30*mm,320*mm,70*mm)
      c.showPage()
      c.save()
           ###### TO DISPLAY PDF VIA BROWSER  ###
           #with open('amal.pdf', 'rb') as pdf:
           #   response = HttpResponse(pdf.read(),content_type='application/pdf')
           #   response['Content-Disposition'] = 'filename=some_file.pdf'
           #   return response
           #pdf.closed
      arch=zipfile.ZipFile("pdf/"+"i.zip","w")
      arch.write("pdf/"+str(i.admno).split('/')[0]+'front.pdf')
      arch.write("pdf/"+str(i.admno).split('/')[0]+'back.pdf')
      arch.close()
      adf="pdf/"+i.admno.split('/')[0]+'front.pdf'
      adb="pdf/"+i.admno.split('/')[0]+'back.pdf'
      pho= root + i.photo.url
      i.delete()
      os.system('rm '+pho)
      os.system('rm '+adb)
      os.system('rm '+adf)
      response = HttpResponse(open(root+"/pdf"+'/i.zip', 'rb').read(), content_type='application/zip')
      response['Content-Disposition'] = 'attachment; filename=single.zip'
      return response
  else:
    form=SingleStud()
    return render(request,'singlestud.html',{'form':form})


  