from django.shortcuts import render  
from django.http import HttpResponse  
from file_upload.forms import StudentForm  
from functions.file_functions import handle_uploaded_file



def file_upload_pg(request):  
	if request.method == 'POST':  
		student = StudentForm(request.POST, request.FILES)  
		if student.is_valid():  
			handle_uploaded_file(request.FILES['file'],request.POST['email'])  
			return HttpResponse("File uploaded successfuly")  
	else:  
		student = StudentForm()  
		return render(request,"file_upload.html",{'form':student})




