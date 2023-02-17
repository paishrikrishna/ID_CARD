from django.shortcuts import render  
from django.http import HttpResponse  
from file_upload.forms import StudentForm  
from functions.file_functions import handle_uploaded_file

# import os module
import os



def file_upload_pg(request):  
	if request.method == 'POST':  
		student = StudentForm(request.POST, request.FILES)  
		if student.is_valid():  
			handle_uploaded_file(request.FILES['file'],request.POST['email'])
			return download_file(request.FILES['file'],request.POST['email'])  
			return HttpResponse("File uploaded successfuly")  
	else:  
		student = StudentForm()  
		return render(request,"file_upload.html",{'form':student})




def download_file(f,user_email):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = f'{user_email}_{f.name}.zip'
    # Define the full file path
    filepath = BASE_DIR + '/static/generated_files/' + filename
    # Open the file for reading content
    zip_file = open(filepath,'rb')
    response = HttpResponse(zip_file,content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % f'{filename}.zip'
    print(response)
    return response
