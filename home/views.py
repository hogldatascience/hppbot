from django.shortcuts import render, redirect
from . import upl_data
from django.http import HttpResponse
from .models import *
import pandas as pd
import csv
import zipfile
from io import StringIO, BytesIO
import datetime
from django.contrib.auth import logout
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):

    return render(request, "home.html")

def load_upload_data(request):

    return render(request, 'upload_data.html')

def load_monitor(request):
    # return HttpResponse('This is the home page')

    return render(request, 'monitor.html')

def load_site(request):
    # return HttpResponse('This is the home page')

    return render(request, 'site.html')

def load_kavumu(request):
    # return HttpResponse('This is the home page')

    return render(request, 'kavumu.html')

def upload_data_ftn(request):

    if 'logout_html' in request.POST:

        logout(request)

        return redirect('index')

    if request.method == "POST":

        up_data_type = request.POST["file_type_html"]

        file = request.FILES['selected_file_html']

        # obj = ExcelFile.objects.create(file = file)
        #obj = ExcelFile(file = file)

        #path = str(obj.file)

        # print(file, " *************************")
        # print(path, " *************************")
        # print(obj, " ..............................")

        msg = upl_data.update_db(file, up_data_type, file)

        return render(request, "upload_data.html", {'message': msg})

def load_export(request):

    return render(request, 'export.html')

def new_export_ftn(request):

    if 'logout_html' in request.POST:

        logout(request)

        return redirect('index')

    up_data_type = request.POST["file_type_html"]

    start = request.POST["start_time_html"]
    end = request.POST["end_time_html"]

    start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    if up_data_type == "All":

        obj_lst = []

        names_lst = ["P (kW)", "U1 P (kW)", "U2 P (kW)", "H (m)", "U1 Y (%)", "U2 Y (%)", "Uab (kV)", "Ubc (kV)", "Uca (kV)", "Intake Data"]

        obj_lst.append(P_kW.objects)
        obj_lst.append(U1_P_kW.objects)
        obj_lst.append(U2_P_kW.objects)
        obj_lst.append(H_m.objects)
        obj_lst.append(U1_Y.objects)
        obj_lst.append(U2_Y.objects)
        obj_lst.append(Uab_kV.objects)
        obj_lst.append(Ubc_kV.objects)
        obj_lst.append(Uca_kV.objects)
        obj_lst.append(intake_data.objects)

        zipped_file = BytesIO()

        with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zipped:

            for i in range (len(obj_lst)):

                csv_data = StringIO()
                writer = csv.writer(csv_data, delimiter=',')

                if i == len(obj_lst) - 1:

                    writer.writerow(['Date', 'Time', 'Bridge', 'Upstream', 'Downstream', 'Bridge_Shaped',
                    'Upstream_Shaped', 'Downstream_Shaped', 'Bridge_Code', 'Upstream_Code',
                    'Downstream_Code'])

                    for member in obj_lst[i].values_list('Date', 'Time', 'Bridge', 'Upstream', 'Downstream', 'Bridge_Shaped',
                    'Upstream_Shaped', 'Downstream_Shaped', 'Bridge_Code', 'Upstream_Code',
                    'Downstream_Code'):

                        a = member[0]

                        if a >= start and a <= end:

                            writer.writerow(member)      
                    
                else:
                    writer.writerow(['Date', 'Time', 'Minimum', 'Maximum', 'Average', 'Minimum_Shaped',
                    'Maximum_Shaped', 'Average_Shaped', 'Minimum_Code', 'Maximum_Code',
                    'Average_Code'])

                    for member in obj_lst[i].values_list('Date', 'Time', 'Minimum', 'Maximum', 'Average', 'Minimum_Shaped',
                    'Maximum_Shaped', 'Average_Shaped', 'Minimum_Code', 'Maximum_Code',
                    'Average_Code'):

                        a = member[0]

                        if a >= start and a <= end:

                            writer.writerow(member)                 

                zipped.writestr("{} from {} to {}.csv".format(names_lst[i], start, end), csv_data.getvalue())

        zipped_file.seek(0)

        response = HttpResponse(zipped_file, content_type='application/octet-stream')

        response['Content-Disposition'] = 'attachment; filename=Scada Data from {} to {}.zip'.format(start, end)
        
        return response

    if up_data_type == "P (kW)":
        objs = P_kW.objects.all()

    if up_data_type == "U1 P (kW)":
        objs = U1_P_kW.objects.all()

    if up_data_type == "U2 P (kW)":
        objs = U2_P_kW.objects.all()

    if up_data_type == "H (m)":
        objs = H_m.objects.all()  

    if up_data_type == "U1 Y (%)":
        objs = U1_Y.objects.all()

    if up_data_type == "U2 Y (%)":
        objs = U2_Y.objects.all()

    if up_data_type == "Uab (kV)":
        objs = Uab_kV.objects.all()

    if up_data_type == "Ubc (kV)":
        objs = Ubc_kV.objects.all() 

    if up_data_type == "Uca (kV)":
        objs = Uca_kV.objects.all() 

    if up_data_type == "Intake Data":

        objs = intake_data.objects.all()

        response = HttpResponse(content_type = 'text/csv')

        writer = csv.writer(response)       

        writer.writerow(['Date', 'Time', 'Bridge', 'Upstream', 'Downstream', 'Bridge_Shaped',
       'Upstream_Shaped', 'Downstream_Shaped', 'Bridge_Code', 'Upstream_Code',
       'Downstream_Code'])

        for member in objs.values_list('Date', 'Time', 'Bridge', 'Upstream', 'Downstream', 'Bridge_Shaped',
        'Upstream_Shaped', 'Downstream_Shaped', 'Bridge_Code', 'Upstream_Code',
        'Downstream_Code'):

            a = member[0]

            if a >= start and a <= end:

                writer.writerow(member)

        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(up_data_type)

        return response

    response = HttpResponse(content_type = 'text/csv')

    writer = csv.writer(response)

    writer.writerow(['Date', 'Time', 'Minimum', 'Maximum', 'Average', 'Minimum_Shaped',
       'Maximum_Shaped', 'Average_Shaped', 'Minimum_Code', 'Maximum_Code',
       'Average_Code'])

    for member in objs.values_list('Date', 'Time', 'Minimum', 'Maximum', 'Average', 'Minimum_Shaped',
       'Maximum_Shaped', 'Average_Shaped', 'Minimum_Code', 'Maximum_Code',
       'Average_Code'):

        a = member[0]

        if a >= start and a <= end:

            writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(up_data_type)

    return response

def logout_ftn(request):

    if 'logout_html' in request.POST:

        logout(request)

        return redirect('index')
