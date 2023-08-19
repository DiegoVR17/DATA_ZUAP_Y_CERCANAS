def cleandata(file,porcentaje,datos):
    import numpy as np
    import pandas as pd

    with open("DIEGO_DATA_PCA/"+file) as f:
        station = f.read().splitlines() #lista con el nombre de los archivos csv
    
    frames = []
    for i in range(len(station)):
        frames.append(pd.read_csv('DIEGO_DATA_PCA/'+station[i]))
    
    d = pd.concat(frames) 
            
    if (datos == 1): 
        #Para algunos datos la fecha y hora estan en 'Unamed 0:' y para otros en 'Fecha_Hora'
        if (('Unnamed: 0' in d.columns) and ('Fecha_Hora' in d.columns)):
            d['fecha_hora'] = d['Unnamed: 0'].fillna(d['Fecha_Hora']) #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Unnamed: 0'], d['Fecha_Hora'], d['fecha_hora'])
        elif ('Fecha_Hora' in d.columns):
            d['fecha_hora'] = d['Fecha_Hora'] #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Fecha_Hora'], d['fecha_hora'])
        elif ('Unnamed: 0' in d.columns):
            d['fecha_hora'] = d['Unnamed: 0'] #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Unnamed: 0'], d['fecha_hora'])
            
        k = abs(((d[d==-9999.0]).sum())/9999.0)# Missing values in columns

        to_delete = (k>= (len(d)*(porcentaje/100))).tolist() # Eliminar las columnas que tengan el 10% o mas de datos faltantes
        columns = d.columns.tolist()
        index_to_delete = []
        for i in range(len(to_delete)):
            if(to_delete[i]):
                index_to_delete.append(i)
                index_to_delete.append(i+1)
        for i in index_to_delete:
            del(d[columns[i]])

        final_columns = d.columns.tolist()
        for i in final_columns:
            if(len(d[(d[i]==-9999.0)])>0):
                d = d.drop(d[(d[i]==-9999.0)].index.to_list(), axis=0) #Elimnar las filas que tengan datos malos

        #Matriz con solo las columnas de calidad
        calidad = d[d.columns[[d.columns.to_list().index(s) for s in d.columns.to_list() if s.__contains__("calidad")]].to_list()]

        calidad_columns = calidad.columns.tolist()
        for i in calidad_columns:
            if(len(d[(d[i]>=2.6)])>0):
                d = d.drop(d[(d[i]>=2.6)].index.to_list(), axis=0) #Elimnar las filas que tengan datos de calidad malos
                calidad = calidad.drop(calidad[(calidad[i]>=2.6)].index.to_list(), axis=0)



    elif (datos == 2):
        d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
        del(d['fecha_hora'])
        d = d[d.index.minute == 0] #Obtener los datos cada hora

        k = abs(((d[d==-999.0]).sum())/999.0)# Missing values in columns

        to_delete = (k>= (len(d)*(porcentaje/100))).tolist() # Eliminar las columnas que tengan el 10% o mas de datos faltantes
        columns = d.columns.tolist()
        index_to_delete = []
        for i in range(len(to_delete)):
            if(to_delete[i]):
                index_to_delete.append(i)
                index_to_delete.append(i+1)

        for i in index_to_delete:
            del(d[columns[i]])

        final_columns = d.columns.tolist()
        for i in final_columns:
            if(len(d[(d[i]==-999.0)])>0):
              d = d.drop(d[(d[i]==-999.0)].index.to_list(), axis=0) #Elimnar las filas que tengan datos malos

        #Matriz con solo las columnas de calidad
        calidad = d[d.columns[[d.columns.to_list().index(s) for s in d.columns.to_list() if s.__contains__("Calidad")]].to_list()]

        calidad_columns = calidad.columns.tolist()
        for i in calidad_columns:
            if(len(d[(d[i]!=1.0)])>0):
              d = d.drop(d[(d[i]!=1.0)].index.to_list(), axis=0) #Elimnar las filas que tengan datos de calidad malos
              calidad = calidad.drop(calidad[(calidad[i]!=1.0)].index.to_list(), axis=0)
      
    elif (datos == 3):
        #Para algunos datos la fecha y hora estan en 'Unamed 0:' y para otros en 'Fecha_Hora'
        if (('Unnamed: 0' in d.columns) and ('Fecha_Hora' in d.columns)):
            d['fecha_hora'] = d['Unnamed: 0'].fillna(d['Fecha_Hora']) #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Unnamed: 0'], d['Fecha_Hora'], d['fecha_hora'])
        elif ('Fecha_Hora' in d.columns):
            d['fecha_hora'] = d['Fecha_Hora'] #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Fecha_Hora'], d['fecha_hora'])
        elif ('Unnamed: 0' in d.columns):
            d['fecha_hora'] = d['Unnamed: 0'] #Se unifica la fecha y hora en una columna 'id'
            d.index = pd.to_datetime(d['fecha_hora']) #Definir como id la fecha y hora
            del(d['Unnamed: 0'], d['fecha_hora'])

        #Delete all columns except pm25 and calidad_pm25
        columns_to_delete = d.columns.to_list()
        del columns_to_delete[1:3] #We don't want delete pm25 and calidad_pm25
        d = d.drop(columns=columns_to_delete)

        #Delete pm25 rows that have -9999.0
        if(len(d[(d['pm25']==-9999.0)])>0):
            d = d.drop(d[(d['pm25']==-9999.0)].index.to_list(), axis=0)

        #Delete calidad_pm25 rows where are higher than 2.6
        if(len(d[(d['calidad_pm25']>=2.6)])>0):
            d = d.drop(d[(d['calidad_pm25']>=2.6)].index.to_list(), axis=0)

    return d
