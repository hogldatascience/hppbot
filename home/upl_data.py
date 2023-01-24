import pandas as pd
import warnings
import calendar
import numpy as np
import re
warnings.filterwarnings("ignore")

import psycopg2
from sqlalchemy import create_engine

# engine = create_engine('postgresql://postgres:HOGLpostgres2022!@34.28.64.252/scada_db')

engine = create_engine('postgresql://postgres:hogl23@localhost/hppbot_data')

def update_db(up_data, up_data_type, file_name):

    file_name = str(file_name).split('.csv')[0]

    if up_data_type == "Intake Data":

        if 'Levels_' not in file_name:

            return "Error: You selected Intake Data and uploaded '{}'. Please rename your file correctly!".format(file_name) 

        else:

            # print(file_name)        

            # data_in = pd.read_csv(up_data)

            # print(up_data_type)

            # return "Printed" 

            df = pd.read_csv(up_data)

            df['Date Time'] = df['Date'] + ' ' + df['Time']
            df['Date Time'] = pd.to_datetime(df['Date Time'])
            df = df[["Date Time", "Bridge", "Upstream", "Downstream", "Difference"]]

            df = df.sort_values(by="Date Time")
            df = df.reset_index(drop=True)

            df['Date Time'] = df['Date Time'].values.astype('<M8[m]')
            df = df.drop_duplicates(subset='Date Time')
            
            df['Date Time'] = df['Date Time'].astype("string")

            start_time = df['Date Time'][0]
            end_time = df['Date Time'].iloc[-1]

            year_ = start_time.split('-')[0]
            month_ = start_time.split('-')[1]
            day_ = start_time.split('-')[2].split(' ')[0]
            expected_start_time = year_ + '-' + month_ + '-' +  day_ + ' ' + '00:00:00'

            if expected_start_time != start_time:

                df_temp = pd.DataFrame([[expected_start_time]], columns=['Date Time'])
                df = pd.concat([df_temp, df]).reset_index(drop=True)

            expected_end_time = year_ + '-' + month_ + '-' +  day_ + ' ' + '23:59:00'

            if expected_end_time != end_time:
                
            #     print("Not Equal")
                
                #Add the expected end time

                df_temp = pd.DataFrame([[expected_end_time]], columns=['Date Time'])
                df = pd.concat([df, df_temp]).reset_index(drop=True)  

            df['Date Time'] =  pd.to_datetime(df['Date Time'])

            # if is_available(engine, "home_cedric_box", df['Date Time'].dt.date[0]):
                
            #     return "Data for the same time range already exist in the database."

            df_new = df.set_index('Date Time')
            df_new = df_new.resample('60S', base=0).mean()
            df_new.reset_index(inplace=True)

            df_new["Bridge_Shaped"] = df_new["Bridge"].copy()
            df_new["Upstream_Shaped"] = df_new["Upstream"].copy()
            df_new["Downstream_Shaped"] = df_new["Downstream"].copy()

            df_new["Bridge_Code"] = 1
            df_new["Upstream_Code"] = 1
            df_new["Downstream_Code"] = 1

            df_new["Date"] = df_new["Date Time"].dt.date
            df_new["Time"] = df_new["Date Time"].dt.time

            df_new = df_new[['Date', 'Time', 'Bridge', 'Upstream', 'Downstream', 'Difference', 'Bridge_Shaped',
                'Upstream_Shaped', 'Downstream_Shaped', 'Bridge_Code', 'Upstream_Code',
                'Downstream_Code']]

            fill_missing(df_new, "Bridge", "Bridge_Shaped", "Bridge_Code", 10)
            fill_missing(df_new, "Upstream", "Upstream_Shaped", "Upstream_Code", 10)
            fill_missing(df_new, "Downstream", "Downstream_Shaped", "Downstream_Code", 10)

            # df.to_sql('cedric_box_data', engine, if_exists = 'append', index = False)

            df_new.to_sql('box_intake_data', engine, if_exists = 'append', index = False)

            return "Updated Successfully!"

    try:
    
        data_in = pd.read_csv(up_data)

        status = "Success"

        if data_in.columns[0] != 'SELECTED VARIABLE':
            status = 'Fail'
            return "Error: The first header should be 'SELECTED VARIABLE' but it is '{}'".format(data_in.columns[0])

        if data_in.iloc[10][0].split(':')[1].strip() != '1 minute':
            status = 'Fail'
            return "Error: Please upload data by Minute!"
            
        if up_data_type == 'H (m)' and data_in.iloc[4][0].split(':')[1].strip() != 'h (m)':
            status = 'Fail'
            return "Error: You selected 'H (m)' and uploaded '{}'".format(data_in.iloc[4][0].split(':')[1].strip())
            
            
        if up_data_type == 'P (kW)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
                
            if ('U1' in file_name) or ('U2' in file_name):
                status = 'Fail'  
                return "Error: You selected 'P (kW)' and uploaded '{}'".format(file_name)                
            
        if up_data_type == 'U1 P (kW)':

            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'U1 P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            
            if ('u1' not in file_name.lower()) or ('p' not in file_name.lower()) or ('kw' not in file_name.lower()) or ('u2' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U1 P (kW)' and uploaded '{}'. Please rename your file correctly!".format(file_name)
                                   
        if up_data_type == 'U1 Y (%)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'Yw (%)':
                status = 'Fail'
                return "Error: You selected 'U1 Y (%)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
            
            if ('u1' not in file_name.lower()) or ('y' not in file_name.lower()) or ('%' not in file_name) or ('u2' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U1 Y (%)' and uploaded '{}'. Please rename your file correctly!".format(file_name)

        if up_data_type == 'U2 P (kW)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'U2 P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            if ('u2' not in file_name.lower()) or ('p' not in file_name.lower()) or ('kw' not in file_name.lower()) or ('u1' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U2 P (kW)' and uploaded '{}'. Please rename your file correctly!".format(file_name)

        if up_data_type == 'U2 Y (%)':

            if data_in.iloc[4][0].split(':')[1].strip() != 'Yw (%)':
                status = 'Fail'
                return "Error: You selected 'U2 Y (%)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            if ('u2' not in file_name.lower()) or ('y' not in file_name.lower()) or ('%' not in file_name) or ('u1' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U2 Y (%)' and uploaded '{}'. Please rename your file correctly!".format(file_name)
            
                
        if up_data_type == 'Uab (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Uab (kV)':
                status = 'Fail'
                return "Error: You selected 'Uab (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                    
        if up_data_type == 'Ubc (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Ubc (kV)':
                status = 'Fail'
                return "Error: You selected 'Ubc (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                    
                    
        if up_data_type == 'Uca (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Uca (kV)':
                status = 'Fail'
                return "Error: You selected 'Uca (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())

        df = data_in.drop(data_in.index[0:12])
        df[["Sample", "Date", "Time", "First value", "Last value", "Minimum", "Maximum", "Average"]] = df['SELECTED VARIABLE'].str.split(';', expand=True)
        df = df[["Date", "Time", "Minimum", "Maximum", "Average"]]
        df.reset_index(drop=True, inplace=True)
        df = df.applymap(lambda x: x.replace('"', ''))

    except pd.errors.ParserError:

        return "{} data for the same time range already exist in the database.".format(up_data_type)
    
        data_in = pd.read_csv(up_data, sep = '.', index_col=None)

        #print(data_in.head(5))

        status = "Success"

        if data_in.columns[0] != 'SELECTED VARIABLE':
            status = 'Fail'
            return "Error: The first header should be 'SELECTED VARIABLE' but it is '{}'".format(data_in.columns[0])

        if data_in.iloc[10][0].split(':')[1].strip() != '1 minute':
            status = 'Fail'
            return "Error: Please upload data by Minute!"
            
        if up_data_type == 'H (m)' and data_in.iloc[4][0].split(':')[1].strip() != 'h (m)':
            status = 'Fail'
            return "Error: You selected 'H (m)' and uploaded '{}'".format(data_in.iloc[4][0].split(':')[1].strip())
                       
        if up_data_type == 'P (kW)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                                
            if ('U1' in file_name) or ('U2' in file_name):
                status = 'Fail'  
                return "Error: You selected 'P (kW)' and uploaded '{}'".format(file_name)                
            
        if up_data_type == 'U1 P (kW)':

            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'U1 P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            
            if ('u1' not in file_name.lower()) or ('p' not in file_name.lower()) or ('kw' not in file_name.lower()) or ('u2' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U1 P (kW)' and uploaded '{}'. Please rename your file correctly!".format(file_name)
                                  
        if up_data_type == 'U1 Y (%)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'Yw (%)':
                status = 'Fail'
                return "Error: You selected 'U1 Y (%)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
            
            if ('u1' not in file_name.lower()) or ('y' not in file_name.lower()) or ('%' not in file_name) or ('u2' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U1 Y (%)' and uploaded '{}'. Please rename your file correctly!".format(file_name)

        if up_data_type == 'U2 P (kW)':
            
            if data_in.iloc[4][0].split(':')[1].strip() != 'P (kW)':
                status = 'Fail'
                return "Error: You selected 'U2 P (kW)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            if ('u2' not in file_name.lower()) or ('p' not in file_name.lower()) or ('kw' not in file_name.lower()) or ('u1' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U2 P (kW)' and uploaded '{}'. Please rename your file correctly!".format(file_name)

        if up_data_type == 'U2 Y (%)':

            if data_in.iloc[4][0].split(':')[1].strip() != 'Yw (%)':
                status = 'Fail'
                return "Error: You selected 'U2 Y (%)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                
            if ('u2' not in file_name.lower()) or ('y' not in file_name.lower()) or ('%' not in file_name) or ('u1' in file_name.lower()):
                status = 'Fail'
                return "Error: You selected 'U2 Y (%)' and uploaded '{}'. Please rename your file correctly!".format(file_name)
            
                
        if up_data_type == 'Uab (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Uab (kV)':
                status = 'Fail'
                return "Error: You selected 'Uab (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                    
        if up_data_type == 'Ubc (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Ubc (kV)':
                status = 'Fail'
                return "Error: You selected 'Ubc (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())
                    
                    
        if up_data_type == 'Uca (kV)':
                    
            if data_in.iloc[4][0].split(':')[1].strip() != 'Uca (kV)':
                status = 'Fail'
                return "Error: You selected 'Uca (kV)' and uploaded '{}'!".format(data_in.iloc[4][0].split(':')[1].strip())


        df = data_in.drop(data_in.index[0:12])
        df[["Sample", "Date", "Time", "First value", "Last value", "Minimum", "Maximum", "Average"]] = df['SELECTED VARIABLE'].str.split(';', expand=True)
        df = df[["Date", "Time", "Minimum", "Maximum", "Average"]]
        df.reset_index(drop=True, inplace=True)
        df = df.applymap(lambda x: x.replace('"', ''))
        df = df.applymap(lambda x: x.replace(',', '.'))

    df.Minimum = df.Minimum.astype(float)
    df.Maximum = df.Maximum.astype(float)
    df.Average = df.Average.astype(float)

    df['Date Time'] = df['Date'] + ' ' + df['Time']
    df = df[["Date Time", "Minimum", "Maximum", "Average"]]
    
    start_time = df['Date Time'][0]
    end_time = df['Date Time'].iloc[-1]

    year_ = start_time.split('-')[0]
    month_ = start_time.split('-')[1]

    expected_start_time = year_ + '-' + month_ + '-' +  '01' + ' ' + '00:00:00'

    if expected_start_time != start_time:

        #Add the expected start time
        df_temp = pd.DataFrame([[expected_start_time]], columns=['Date Time'])
        df = pd.concat([df_temp, df]).reset_index(drop=True)


    last_day = calendar.monthrange(int(year_), int(month_))[1]
    expected_end_time = year_ + '-' + month_ + '-' +  str(last_day) + ' ' + '23:59:00'
    
    if expected_end_time != end_time:

        #Add the expected end time
        df_temp = pd.DataFrame([[expected_end_time]], columns=['Date Time'])
        df = pd.concat([df, df_temp]).reset_index(drop=True)

    df['Date Time'] =  pd.to_datetime(df['Date Time'], format = "%Y-%m-%d %H:%M:%S")

    name = re.sub('[(%)]', '', up_data_type).lower().strip()
    name = re.sub('[ ]', '_', name)
    name = "scada_{}".format(name)

    # if is_available(engine, name, df['Date Time'].dt.date[0]):
        
    #     return "{} data for the same time range already exist in the database.".format(up_data_type)

    df = df.set_index('Date Time')
    df_new = df.resample('60S', base=0).mean()
    df_new.reset_index(inplace=True)

    df_new["Minimum_Shaped"] = df_new["Minimum"].copy()
    df_new["Maximum_Shaped"] = df_new["Maximum"].copy()
    df_new["Average_Shaped"] = df_new["Average"].copy()

    df_new["Minimum_Code"] = 1
    df_new["Maximum_Code"] = 1
    df_new["Average_Code"] = 1

    df_new["Date"] = df_new["Date Time"].dt.date
    df_new["Time"] = df_new["Date Time"].dt.time

    df_new = df_new[['Date', 'Time', 'Minimum', 'Maximum', 'Average', 'Minimum_Shaped',
        'Maximum_Shaped', 'Average_Shaped', 'Minimum_Code', 'Maximum_Code',
        'Average_Code']]

    fill_missing(df_new, "Minimum", "Minimum_Shaped", "Minimum_Code", 20)
    fill_missing(df_new, "Maximum", "Maximum_Shaped", "Maximum_Code", 20)
    fill_missing(df_new, "Average", "Average_Shaped", "Average_Code", 20)

    df_new.to_sql(name, engine, if_exists = 'append', index = False)

    return "{} Updated Successfully!".format(file_name)

def fill_missing(df_new, variable, variable_shaped, variable_code, diff_thresh):
    
    for i in df_new.loc[df_new.isnull().any(axis=1)].index:
        
        if i == 0 or i == len(df_new) - 1:
            
            df_new[variable_shaped].loc[i] = 0
            df_new[variable_code].loc[i] = 3
            
    
        if i > 0 and i != len(df_new) - 1:

            if not pd.isna(df_new[variable].loc[i - 1]):

                df_temp = df_new.loc[i:]        

                idx = df_temp[variable].first_valid_index()
                
                if idx - i < 5:

                    val_before = df_new[variable].loc[i - 1]
                    val_after = df_new[variable].loc[idx]
                    
                    diff = pct_diff(val_before, val_after)

                    if diff <= diff_thresh:

                        df_new[variable_shaped].loc[i:idx - 1] = np.linspace(val_before, val_after, idx - i + 2)[1:-1]
                        df_new[variable_code].loc[i:idx - 1] = 2 #Linear interpolation

                    else:
                        df_new[variable_shaped].loc[i:idx - 1] = 0 
                        df_new[variable_code].loc[i:idx - 1] = 3


                if idx - i >= 5:
                    df_new[variable_shaped].loc[i:idx - 1] = 0 
                    df_new[variable_code].loc[i:idx - 1] = 3

def pct_diff(x, y):
    
    try:
    
        diff = (abs(x - y) / (abs(x + y)/2)) * 100

        return diff
    
    except ZeroDivisionError:
        
        return 0

def is_available(engine, name, val): 
    
    statement = f'select distinct on ("Date") "Date" from public.{name};'
    
    df_sql = pd.read_sql(statement, engine)
    
    if val in df_sql["Date"].values:
    
        return True