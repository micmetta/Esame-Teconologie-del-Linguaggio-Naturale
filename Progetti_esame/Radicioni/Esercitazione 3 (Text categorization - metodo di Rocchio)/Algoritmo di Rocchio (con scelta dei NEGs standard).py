from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json

################### CARICO IL DATAFRAME DI TRAINING E DI TEST ################################################################################################################


#Deserializzo sia la lista_di_tutti_i_documenti_di_TRAINING_in_inglese e sia la lista_di_tutti_i_documenti_di_TEST_in_inglese:####
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TRAINING_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TEST_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
print("LE DUE LISTE SONO STATE DESERIALIZZATE CORRETTAMENTE.")
print("")
#########################################################################



#A questo punto devo calcolare il peso associato ad ogni termine presente sia in lista_di_tutti_i_documenti_di_TRAINING_in_inglese che
# lista_di_tutti_i_documenti_di_TEST_in_inglese con il prodotto:
# time-frequency (tf) * inverse document frequency (idf):
vectorizer = TfidfVectorizer()
vectors_train  = vectorizer.fit_transform(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
feature_names = vectorizer.get_feature_names()
# print("feature_names: ")
# print(feature_names)
dense_train = vectors_train.todense()
denselist_train = dense_train.tolist()
df_train = pd.DataFrame(denselist_train, columns=feature_names)
print("")
print("df_train:")
print(df_train) #[360 rows x 16648 columns], (360 = numero di documenti totali presenti nel training set), 16648 = numero di lemmi totali (senza duplicati) presenti nel training set.
#df_train.to_csv("Dataframe_documenti_rappresentati_da_lemmi_TRAINING.csv")


# vectorizer = TfidfVectorizer()
# vectors_test  = vectorizer.fit_transform(lista_di_tutti_i_documenti_di_TEST_in_inglese)
# feature_names = vectorizer.get_feature_names()
# dense_test = vectors_test.todense()
# denselist_test = dense_test.tolist()
# df_test = pd.DataFrame(denselist_test, columns=feature_names)
# print("")
# print("df_test:")
# print(df_test) #[40 rows x 3317 columns], (40 = numero di documenti totali presenti nel test set), 3317 = numero di lemmi totali (senza duplicati) presenti nel test set.
# print("")
# #print("vectors_train: ", vectors_train)
# print("")
# #print("vectors_test: ", vectors_test)
# #df_test.to_csv("Dataframe_documenti_rappresentati_da_lemmi_TEST.csv")


################### FINE CARICAMENTO DEL DATAFRAME DI TRAINING E DI TEST ################################################################################################################




######################################################################################################################################################################
#A questo punto devo usare il df_train per crearmi I PROFILI utilizzando il metodo di Rocchio:
#(IN QUESTO CASO UTILIZZO COME NEGs tutti i documenti che appartengono alle altre classi) - metodo standard.



#I primi 18 documenti (indice da 0 a 17) del df_train appartengono alla classe "alt.atheism".
#I successivi 18 documenti (indice da 18 a 35) del df_train appartengono alla classe "comp.graphics".
#I successivi 18 documenti (indice da 36 a 53) del df_train appartengono alla classe "comp.os.ms-windows.misc".
#I successivi 18 documenti (indice da 54 a 71) del df_train appartengono alla classe "comp.sys.ibm.pc.hardware".
#I successivi 18 documenti (indice da 72 a 89) del df_train appartengono alla classe "comp.sys.mac.hardware".
#I successivi 18 documenti (indice da 90 a 107) del df_train appartengono alla classe "comp.windows.x".
#I successivi 18 documenti (indice da 108 a 125) del df_train appartengono alla classe "misc.forsale".
#I successivi 18 documenti (indice da 126 a 143) del df_train appartengono alla classe "rec.autos".
#I successivi 18 documenti (indice da 144 a 161) del df_train appartengono alla classe "rec.motorcycles".
#I successivi 18 documenti (indice da 162 a 179) del df_train appartengono alla classe "rec.sport.baseball".
#I successivi 18 documenti (indice da 180 a 197) del df_train appartengono alla classe "rec.sport.hockey".
#I successivi 18 documenti (indice da 198 a 215) del df_train appartengono alla classe "sci.crypt".
#I successivi 18 documenti (indice da 216 a 233) del df_train appartengono alla classe "sci.electronics".
#I successivi 18 documenti (indice da 234 a 251) del df_train appartengono alla classe "sci.med".
#I successivi 18 documenti (indice da 252 a 269) del df_train appartengono alla classe "sci.space".
#I successivi 18 documenti (indice da 270 a 287) del df_train appartengono alla classe "soc.religion.christian".
#I successivi 18 documenti (indice da 288 a 305) del df_train appartengono alla classe "talk.politics.guns".
#I successivi 18 documenti (indice da 306 a 323) del df_train appartengono alla classe "talk.politics.mideast".
#I successivi 18 documenti (indice da 324 a 341) del df_train appartengono alla classe "talk.politics.misc".
#I successivi 18 documenti (indice da 342 a 359) del df_train appartengono alla classe "talk.religion.misc".


beta = 16
gamma = 4
#definisco i vari centroidi di ogni classe:
c_alt_atheism = []
c_comp_graphics = []
c_comp_os_ms_windows_misc = []
c_comp_sys_ibm_pc_hardware = []
c_comp_sys_mac_hardware = []
c_comp_windows_x = []
c_misc_forsale = []
c_rec_autos = []
c_rec_motorcycles = []
c_rec_sport_baseball = []
c_rec_sport_hockey = []
c_sci_crypt = []
c_sci_electronics = []
c_sci_med = []
c_sci_space = []
c_soc_religion_christian = []
c_talk_politics_guns = []
c_talk_politics_mideast = []
c_talk_politics_misc = []
c_talk_religion_misc = []


dizionario_da_indice_classe_a_estremo_sinistro_j_1 = {0:0, 1:18, 2:36, 3:54, 4:72, 5:90, 6:108, 7:126, 8:144, 9:162, 10:180,
                                                    11:198, 12:216, 13:234, 14:252, 15:270, 16:288, 17:306, 18:324, 19:342}

dizionario_da_indice_classe_a_estremo_destro_j_1 = {0:18, 1:36, 2:54, 3:72, 4:90, 5:108, 6:126, 7:144, 8:162, 9:180, 10:198,
                                                    11:216, 12:234, 13:252, 14:270, 15:288, 16:306, 17:324, 18:342, 19:360}

POS_i = 18
NEG_i = 18*19 #18 documenti per ogni classe tranne quella corrente che sto considerando in quel momento (dopo dovrai cambiarlo..).

for i in range(0, 20): #i = indice che scorre tutte le classi (che sono 20 in totale) (mi permette di considerare ogni centroide ci).
    for k in range (0, 16648): #colonna max = 16647; #k = indice che scorre tutte le feature per ogni centroide di ogni classe i-esima.

        # - Innanzitutto calcolo la sommatoria su tutti i documenti che appartengono alla classe i-esima:
        estremo_sinistro_j_1 = dizionario_da_indice_classe_a_estremo_sinistro_j_1[i]
        estremo_destro_j_1 = dizionario_da_indice_classe_a_estremo_destro_j_1[i]

        sommatoria_su_tutti_i_documenti_che_appartengono_alla_classe_i = 0
        for j_1 in range(estremo_sinistro_j_1, estremo_destro_j_1): #classe alt_atheism #questo j=j_1 e 18=estremo_destro_j_1
            # per i == 0 (prima classe di documenti), j_1 andrà da: 0 a 17
            # per i == 1, j_1 andrà da: 18 a 35
            #e così via..
            documento_corrente = df_train.iloc[j_1]
            w_k_j = df_train.iloc[j_1,k]
            valore_interno_sommatoria = w_k_j / POS_i
            sommatoria_su_tutti_i_documenti_che_appartengono_alla_classe_i = sommatoria_su_tutti_i_documenti_che_appartengono_alla_classe_i + valore_interno_sommatoria
            #print("documento_corrente classe alt_atheism:")
            #print(documento_corrente)


        # - Adesso invece calcolo la sommatoria su tutti i documenti che non appartengono alla classe i-esima:
        sommatoria_su_tutti_i_documenti_che_non_appartengono_alla_classe_i = 0
        for j_2 in range(0, 360):  # non classe alt_atheism #questo j = j_2
            if( (j_2 < estremo_sinistro_j_1) or (j_2 >= estremo_destro_j_1) ):
                #per i == 0 (prima classe di documenti): (j_2 < 0) or (j_2 >= 18)
                #per i == 1: (j_2 < 18) or (j_2 >= 36)
                # e così via..
                documento_corrente = df_train.iloc[j_2]
                w_k_j = df_train.iloc[j_2, k]
                valore_interno_sommatoria = w_k_j / NEG_i
                sommatoria_su_tutti_i_documenti_che_non_appartengono_alla_classe_i = sommatoria_su_tutti_i_documenti_che_non_appartengono_alla_classe_i + valore_interno_sommatoria
                #print("documento_corrente NON classe alt_atheism:")
                #print(documento_corrente)

        f_k_i = (beta*sommatoria_su_tutti_i_documenti_che_appartengono_alla_classe_i) - (gamma*sommatoria_su_tutti_i_documenti_che_non_appartengono_alla_classe_i)

        #print("") documento corrente
        print("classe i-esima: ", i)
        print("k: ", k)
        print("f_k_i: ", f_k_i)

        #Adesso posso aggiungere la feature appena creata al centroide della classe i-esima che sto considerando in quel momento:

        if (i==0):  # vuol dire che la feature k-esima che sto considerando farà parte del centroide che rappresenta la classe alt_atheism
            c_alt_atheism.append(f_k_i)  # aggiungo al centroide di questa classe la nuova feature appena creata

        elif(i==1):
            c_comp_graphics.append(f_k_i)

        elif(i==2):
            c_comp_os_ms_windows_misc.append(f_k_i)

        elif(i==3):
            c_comp_sys_ibm_pc_hardware.append(f_k_i)

        elif(i==4):
            c_comp_sys_mac_hardware.append(f_k_i)

        elif(i==5):
            c_comp_windows_x.append(f_k_i)

        elif(i==6):
            c_misc_forsale.append(f_k_i)

        elif(i==7):
            c_rec_autos.append(f_k_i)

        elif(i==8):
            c_rec_motorcycles.append(f_k_i)

        elif(i==9):
            c_rec_sport_baseball.append(f_k_i)

        elif(i==10):
            c_rec_sport_hockey.append(f_k_i)

        elif(i==11):
            c_sci_crypt.append(f_k_i)

        elif(i==12):
            c_sci_electronics.append(f_k_i)

        elif(i==13):
            c_sci_med.append(f_k_i)

        elif(i==14):
            c_sci_space.append(f_k_i)

        elif(i==15):
            c_soc_religion_christian.append(f_k_i)

        elif(i==16):
            c_talk_politics_guns.append(f_k_i)

        elif(i==17):
            c_talk_politics_mideast.append(f_k_i)

        elif(i==18):
            c_talk_politics_misc.append(f_k_i)

        else:
            c_talk_religion_misc.append(f_k_i)


    #print("c_alt_atheism: ")
    #print(c_alt_atheism)
    #print("")


print("len(c_alt_atheism): ", len(c_alt_atheism))
print("len(c_comp_graphics): ", len(c_comp_graphics))
print("len(c_comp_os_ms_windows_misc): ", len(c_comp_os_ms_windows_misc))
print("len(c_comp_sys_ibm_pc_hardware): ",len(c_comp_sys_ibm_pc_hardware))
print("len(c_comp_sys_mac_hardware): ",len(c_comp_sys_mac_hardware))
print("len(c_comp_windows_x): ",len(c_comp_windows_x))
print("len(c_misc_forsale): ",len(c_misc_forsale))
print("len(c_rec_autos): ",len(c_rec_autos))
print("len(c_rec_motorcycles): ",len(c_rec_motorcycles))
print("len(c_rec_sport_baseball): ",len(c_rec_sport_baseball))
print("len(c_rec_sport_hockey): ",len(c_rec_sport_hockey))
print("len(c_sci_crypt): ",len(c_sci_crypt))
print("len(c_sci_electronics): ",len(c_sci_electronics))
print("len(c_sci_med): ",len(c_sci_med))
print("len(c_sci_space): ",len(c_sci_space))
print("len(c_soc_religion_christian): ",len(c_soc_religion_christian))
print("len(c_talk_politics_guns): ",len(c_talk_politics_guns))
print("len(c_talk_politics_mideast): ",len(c_talk_politics_mideast))
print("len(c_talk_politics_misc): ",len(c_talk_politics_misc))
print("len(c_talk_religion_misc): ",len(c_talk_religion_misc))


#ADESSO MI SALVO TUTTI I CENTROIDI DI OGNI CLASSE in modo tale da non doverli ricalcolare ogni volta:

#Serializzo le liste di tutti i centroidi:####
with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_alt_atheism.txt', 'w') as f:
    str = json.dumps(c_alt_atheism)
    f.write(str)
with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_comp_graphics.txt', 'w') as f:
    str = json.dumps(c_comp_graphics)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_comp_os_ms_windows_misc.txt', 'w') as f:
    str = json.dumps(c_comp_os_ms_windows_misc)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_comp_sys_ibm_pc_hardware.txt', 'w') as f:
    str = json.dumps(c_comp_sys_ibm_pc_hardware)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_comp_sys_mac_hardware.txt', 'w') as f:
    str = json.dumps(c_comp_sys_mac_hardware)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_comp_windows_x.txt', 'w') as f:
    str = json.dumps(c_comp_windows_x)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_misc_forsale.txt', 'w') as f:
    str = json.dumps(c_misc_forsale)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_rec_autos.txt', 'w') as f:
    str = json.dumps(c_rec_autos)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_rec_motorcycles.txt', 'w') as f:
    str = json.dumps(c_rec_motorcycles)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_rec_sport_baseball.txt', 'w') as f:
    str = json.dumps(c_rec_sport_baseball)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_rec_sport_hockey.txt', 'w') as f:
    str = json.dumps(c_rec_sport_hockey)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_sci_crypt.txt', 'w') as f:
    str = json.dumps(c_sci_crypt)
    f.write(str)

with open(
        '/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_sci_electronics.txt', 'w') as f:
    str = json.dumps(c_sci_electronics)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_sci_med.txt', 'w') as f:
    str = json.dumps(c_sci_med)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_sci_space.txt', 'w') as f:
    str = json.dumps(c_sci_space)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_soc_religion_christian.txt', 'w') as f:
    str = json.dumps(c_soc_religion_christian)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_talk_politics_guns.txt', 'w') as f:
    str = json.dumps(c_talk_politics_guns)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_talk_politics_mideast.txt', 'w') as f:
    str = json.dumps(c_talk_politics_mideast)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_talk_politics_misc.txt', 'w') as f:
    str = json.dumps(c_talk_politics_misc)
    f.write(str)

with open('/Progetti TLN/Radicioni/Esercitazione 3/Centroidi di Rocchio con scelta dei NEGs standard/Centroidi di Rocchio con scelta dei NEGs standard/c_talk_religion_misc.txt', 'w') as f:
    str = json.dumps(c_talk_religion_misc)
    f.write(str)

print("TUTTE LE LISTE DEI CENTROIDI DI OGNI CLASSE SONO STATE SERIALIZZATE CORRETTAMENTE.") #start 12:37
######################################################################

#DOPODICHE' VAI A CLASSIFICAZIONE DOCUMENTI DI TEST --->
######################################################################################################################################################################