import pandas as pd




def handle_uploaded_file(f,user_email):  
    file_path = f'static/uploaded_files/{user_email}_{f.name}'
    with open(file_path, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

    read_file(file_path)




def read_file(file_path):
    print(file_path)
    df = pd.read_excel(file_path)
    print(df.head(5))