#======================
# Classe per file CSV
#======================

class ExamException(Exception):
        pass

class CSVTimeSeriesFile:

    def __init__(self, name):

        if not isinstance(name, str):
            raise ExamException('Invalid type for name, only string supported. Got "{}"'.format(type(name)))
        
        # Setto il nome del file
        self.name = name

    def __str__(self):
        pass
    
    def get_data(self):
        
        tempListLoader = []
        output = []

        try:
            my_file = open(self.name, 'r')
        
        except ExamException as e:
            print('Errore nella lettura del file: "{}"'.format(e))
            return None
        
        # Ora inizio a leggere il file linea per linea
        for line in my_file:
               
            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')

            # Se NON sto processando l'intestazione...
            if elements[0] != 'epoch':
                
                try:
                    epoch  = elements[0]
                    temp = elements[1]
                    epoch = round(float(epoch))
                    temp = float(temp)
                
                except: 
                    
                    continue

                # Utilizzo una lista temporanea per caricare i valori nella lista finale
                tempListLoader.append(epoch)
                tempListLoader.append(temp)
                
                output.append(tempListLoader[0:2])
                tempListLoader.clear()
                 
        # Chiudo il file
        my_file.close()

        # Se la lista in output è vuota
        if len(output) == 0:
            raise ExamException("File vuoto")

        # Quando ho processato tutte le righe, ritorno i valori
        return output


time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

#======================
# Dati due timestamp ne verifica l'appartenza alla medesima ora
#======================
def same_hour(prev_epoch, epoch):

    if(prev_epoch//3600 == epoch//3600):
        return True
    else:
        return False

#======================
# Date due differenze di temperatura verifica se hanno segno opposto 
#======================
def inversione(prev_temp_diff, temp_diff):
    
    if(prev_temp_diff > 0 and temp_diff < 0) or (prev_temp_diff < 0 and temp_diff > 0):
        return True
    else: 
        return False

#======================
# Data la lista di differenze di temperatura ne calcola il # di inversioni
#======================
def trend_calc(listaDiff):
    c = 0
    prev_temp = None  
    act_temp = None

    for i in range(1, len(listaDiff)):
        prev_temp = listaDiff[i-1]
        act_temp = listaDiff[i]

        if(inversione(prev_temp, act_temp)):
            c += 1

    return c    

#======================
# Funzione per il calcolo del # di inversioni per ogni ora
#======================
def hourly_trend_changes(data):

    output = []

    if not isinstance(data, list):
        raise ExamException('Errore: data non di tipo lista')

    if len(data) <= 2:
        raise ExamException('Errore: lunghezza di data non sufficiente, servono almeno 2 elementi per calcolare il numero di inversioni')

    #variabili di supporto per memorizzare i dati dell'iterazione precedente
    prev_temp = 0
    prev_epoch = 0

    #lista di supporto per le differenze di temperatura
    listaDiff = []

    # Ciclo sulla lista
    for item in data:
            
        epoch = item[0]
        temp = item[1]

        if not isinstance(epoch, int):
            raise ExamException('Errore: epoch non di tipo int')

        if not isinstance(temp, float):
            raise ExamException('Errore: temp non di tipo float')

        if prev_epoch == 0: 
            #mi servono almeno 2 elementi per calcolare la differenza di temperatura
            pass
            
        else:
            # Calcolo la differenza tra la temperatura attuale e quella precedente
            temp_diff = temp - prev_temp
            # Se appartengono alla stessa ora
            if(same_hour(prev_epoch, epoch)):
                # Preparo la lista per il conteggio
                listaDiff.append(temp_diff)

            else:
               
                # Se il primo giorno del dataset ha una sola misurazione restituisco 0
                # Altrimenti calcolo il trend del giorno precedente o lo inserisco nella lista
                if(len(listaDiff) == 0):
                    output.append(0)
                else:
                    listaDiff.append(temp_diff)
                    output.append(trend_calc(listaDiff))
                    listaDiff.clear()
                    listaDiff.append(temp_diff)
             
        # Assegno la variabile di supporto per l'elemento precedente
        prev_temp = temp
        prev_epoch = epoch
    
    #ultimo giro
    output.append(trend_calc(listaDiff))

    return output


out = hourly_trend_changes(time_series)
print('Lista in output: "{}"'.format(out))