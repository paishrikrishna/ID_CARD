import pandas as pd 
import pdfkit
from datetime import datetime, timedelta
import code128
import random
import os
from zipfile import ZipFile
import shutil



#path = "./Generated/paishrikrishna98"

    


def get_all_file_paths(directory):
  
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return file_paths   

#generate costum html file using the arguments
def HTMLgen(code,first_name,last_name,function,date_of_birth,picture,expiration_date):
    html= r"""<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="@base_dir/static/css/card.css"><body><div class="face face-front" ><img src="@base_dir/static/RES/front.png"></div><div id="infoi"><img src="@picture" height="89.5" width="83" />
        <div style="margin-left: 1.3cm;margin-top: -0.6cm;">
            <br>
            <div style="font-size: 0.7em;margin-top: 5%;font-family: sans-serif;color: aliceblue;text-transform: uppercase;"><b>@fname</b> @lname</div><br>
        <div style="font-size: 0.7em;margin-top: -0.4cm;font-family: sans-serif;color: aliceblue;text-t ransform: capitalize;">@function</div>
        </div>
    </div>
    <div id="info">
        <br><div style="font-size: 0.7em;margin-top: 0.6%;font-family: sans-serif;text-transform: uppercase;">@code</div>
        <br><div style="font-size: 0.7em;margin-top: -0.6%;font-family: sans-serif;text-transform: capitalize;">@date_of_birth</div>
        <br><div style="font-size: 0.7em;margin-top: -0.6%;font-family: sans-serif;text-transform: capitalize;">@expiration_date</div>
    </div>
    <div id="BARCODE"><img src="@base_dir/static/RES/bar.png"  height="20" width="120"/></div>

</body>"""
    html = html.replace("@picture",picture)
    html = html.replace("@code",str(code))
    html = html.replace("@fname",first_name)
    html = html.replace("@lname",last_name)
    html = html.replace("@function",function)
    html = html.replace("@date_of_birth",date_of_birth)
    html = html.replace("@expiration_date",expiration_date)
    html = html.replace("@base_dir",os.getcwd().replace("/functions/file_functions.py",""))
    f= open(f"{os.getcwd().replace('functions/file_functions.py','')}/static/RES/index.html","w")
    f.write(html)
    f.close()
    return 
#generate a file bar.png contains barcode of the 10 digits code  
def BARgen(code):
    code128.image(code).save(f"{os.getcwd().replace('functions/file_functions.py','')}/static/RES/bar.png")
    return
#generate costum pdf file using the existing html file // code argument is only to name the file generated
def PDFgen(code,generated_file_path):
    try:
        os.mkdir(generated_file_path)
    except:
        pass
    #config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    options = {'dpi': 365,'margin-top': '0in','margin-bottom': '0in','margin-right': '0in','margin-left': '0in','page-size': 'A8',"orientation": "Landscape",'disable-smart-shrinking': ''}
    pdfkit.from_file(f'{os.getcwd().replace("/functions/file_functions.py","")}/static/RES/index.html', f'{generated_file_path}/{code}.pdf', options = options)
    return
#complete with random digits an integer x until it contains 10 digits
def complete(x):
    x=str(x)
    while len(x)<10:
            x+=str(random.randint(0,9))
    return int(x)



def id_card_creation(file_path,generated_file_path):
    data=pd.read_excel(file_path)

    data['code'] = data['code'].apply(lambda x: complete(x))

    data['submission_date']=pd.to_datetime(data['submission_date'])
    data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])

    data["expiration_date"] = data["submission_date"] + timedelta(days=15)

    data['date_of_birth']=data['date_of_birth'].dt.strftime('%d-%m-%Y')
    data['submission_date']=data['submission_date'].dt.strftime('%d-%m-%Y')
    data['expiration_date']=data['expiration_date'].dt.strftime('%d-%m-%Y')

    
    for index, row in data.head(n=5).iterrows()    :
        code=row[0]
        fname = row[1]
        lname = row[2]
        func  = row[3]
        dob   = row[4]
        ed    = row[5]
        pic   = row[6]
        BARgen(code)
        HTMLgen(code,fname,lname,func,dob,pic,ed)
        PDFgen(code,generated_file_path)

    file_paths = get_all_file_paths(generated_file_path)

    with ZipFile(f'{generated_file_path}.zip','w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    
    shutil.rmtree(f"{os.getcwd().replace('functions/file_functions.py','')}/{generated_file_path}", ignore_errors=True)



def handle_uploaded_file(f,user_email):  
    file_path = f'static/uploaded_files/{user_email}_{f.name}'

    generated_file_path = f'static/generated_files/{user_email}_{f.name}'

    with open(file_path, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

    read_file(file_path,generated_file_path)




def read_file(file_path,generated_file_path):
    print(file_path)
    df = pd.read_excel(file_path,engine='openpyxl')
    id_card_creation(file_path,generated_file_path)





