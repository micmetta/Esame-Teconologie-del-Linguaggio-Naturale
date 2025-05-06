import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

import scikitplot as skplt
# import matplotlib.pyplot as plt
#
# from mlxtend.evaluate import confusion_matrix
# from mlxtend.plotting import plot_confusion_matrix
# from matplotlib.pyplot import subplots

'''
################### CARICO IL DATAFRAME DI TRAINING E DI TEST (non lemmi di WN) ################################################################################################################
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
#################################################################################################################################################################################################
'''


################### CARICO IL DATAFRAME DI TRAINING E DI TEST (considerando i lemmi di WN) #######################################################################################################
#Deserializzo sia la lista_di_tutti_i_documenti_di_TRAINING_in_inglese e sia la lista_di_tutti_i_documenti_di_TEST_in_inglese:####
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TRAINING_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TEST_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
#########################################################################


'''
################### CARICO IL DATAFRAME DI TRAINING E DI TEST (considerando i lemmi di WN ma per la disambiguazione in questo caso per ogni lemma considero max 4 lemmi precedenti e max 4 lemmi successivi) #######################################################################################################
#Deserializzo sia la lista_di_tutti_i_documenti_di_TRAINING_in_inglese e sia la lista_di_tutti_i_documenti_di_TEST_in_inglese:####
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET CON MAX 4 PAROLE PRECEDENTI E 4 PAROLE SUCCESSIVE COME CONTESTO.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TRAINING_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET CON MAX 4 PAROLE PRECEDENTI E 4 PAROLE SUCCESSIVE COME CONTESTO.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TEST_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
#########################################################################
'''

######################################################################################################################################################################################################

'''
#DESERIALIZZO TUTTI I CENTROIDI DOVE I NEGS SONO TUTTI I DOCUMENTI CHE NON APPARTENGONO ALLA CLASSE CHE STO CONSIDERANDO (NEGs STANDARD) (ottenuto con il metodo di Rocchio) DI OGNI CLASSE:

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_alt_atheism.txt', 'r') as f:
    s = f.read()
    centroide_classe_alt_atheism = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_comp_graphics.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_graphics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_comp_os_ms_windows_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_os_ms_windows_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_comp_sys_ibm_pc_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_ibm_pc_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_comp_sys_mac_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_mac_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_comp_windows_x.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_windows_x = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_misc_forsale.txt', 'r') as f:
    s = f.read()
    centroide_classe_misc_forsale = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_rec_autos.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_autos = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_rec_motorcycles.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_motorcycles = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_rec_sport_baseball.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_baseball = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_rec_sport_hockey.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_hockey = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_sci_crypt.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_crypt = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_sci_electronics.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_electronics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_sci_med.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_med = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_sci_space.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_space = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_soc_religion_christian.txt', 'r') as f:
    s = f.read()
    centroide_classe_soc_religion_christian = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_talk_politics_guns.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_guns = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_talk_politics_mideast.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_mideast = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_talk_politics_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEGs standard\\c_talk_religion_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_religion_misc = json.loads(s)
###################################################################################
'''


'''
#Qui ho usato la matrice di confusione per trovare i NEGS di ogni classe.

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_alt_atheism.txt', 'r') as f:
    s = f.read()
    centroide_classe_alt_atheism = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_comp_graphics.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_graphics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_comp_os_ms_windows_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_os_ms_windows_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_comp_sys_ibm_pc_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_ibm_pc_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_comp_sys_mac_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_mac_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_comp_windows_x.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_windows_x = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_misc_forsale.txt', 'r') as f:
    s = f.read()
    centroide_classe_misc_forsale = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_rec_autos.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_autos = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_rec_motorcycles.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_motorcycles = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_rec_sport_baseball.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_baseball = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_rec_sport_hockey.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_hockey = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_sci_crypt.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_crypt = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_sci_electronics.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_electronics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_sci_med.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_med = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_sci_space.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_space = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_soc_religion_christian.txt', 'r') as f:
    s = f.read()
    centroide_classe_soc_religion_christian = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_talk_politics_guns.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_guns = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_talk_politics_mideast.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_mideast = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_talk_politics_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG raffinata\\c_talk_religion_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_religion_misc = json.loads(s)
###################################################################################
'''


'''
#Qui ho usato la mia funzione classe più vicina per trovare i NEGS di ogni classe.

#DESERIALIZZO TUTTI I CENTROIDI DOVE I NEGS SONO TUTTI I DOCUMENTI CHE APPARTENGONO ALLA CLASSE (O ALLE CLASSI) CON LE QUALI
# IL CLASSIFICATORE SI CONFONDE MAGGIORMENTE PER LA CLASSE CORRENTE (ottenuto con il metodo di Rocchio):


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_alt_atheism.txt', 'r') as f:
    s = f.read()
    centroide_classe_alt_atheism = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_comp_graphics.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_graphics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_comp_os_ms_windows_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_os_ms_windows_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_comp_sys_ibm_pc_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_ibm_pc_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_comp_sys_mac_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_mac_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_comp_windows_x.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_windows_x = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_misc_forsale.txt', 'r') as f:
    s = f.read()
    centroide_classe_misc_forsale = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_rec_autos.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_autos = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_rec_motorcycles.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_motorcycles = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_rec_sport_baseball.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_baseball = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_rec_sport_hockey.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_hockey = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_sci_crypt.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_crypt = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_sci_electronics.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_electronics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_sci_med.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_med = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_sci_space.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_space = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_soc_religion_christian.txt', 'r') as f:
    s = f.read()
    centroide_classe_soc_religion_christian = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_talk_politics_guns.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_guns = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_talk_politics_mideast.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_mideast = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_talk_politics_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)\\c_talk_religion_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_religion_misc = json.loads(s)
###################################################################################
'''



#QUI SOTTO CONSIDERO I CENTROIDI TENENDO CONTO DEI LEMMI DI WN:
#Ho usato la mia funzione "classe più vicina" per trovare i NEGS di ogni classe.
#Per ottenere questi centroidi ho utilizzato come contesto per un certo lemma tutto il documento in cui quel lemma compariva.

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_alt_atheism.txt', 'r') as f:
    s = f.read()
    centroide_classe_alt_atheism = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_comp_graphics.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_graphics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_comp_os_ms_windows_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_os_ms_windows_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_comp_sys_ibm_pc_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_ibm_pc_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_comp_sys_mac_hardware.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_sys_mac_hardware = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_comp_windows_x.txt', 'r') as f:
    s = f.read()
    centroide_classe_comp_windows_x = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_misc_forsale.txt', 'r') as f:
    s = f.read()
    centroide_classe_misc_forsale = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_rec_autos.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_autos = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_rec_motorcycles.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_motorcycles = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_rec_sport_baseball.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_baseball = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_rec_sport_hockey.txt', 'r') as f:
    s = f.read()
    centroide_classe_rec_sport_hockey = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_sci_crypt.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_crypt = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_sci_electronics.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_electronics = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_sci_med.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_med = json.loads(s)

with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_sci_space.txt', 'r') as f:
    s = f.read()
    centroide_classe_sci_space = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_soc_religion_christian.txt', 'r') as f:
    s = f.read()
    centroide_classe_soc_religion_christian = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_talk_politics_guns.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_guns = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_talk_politics_mideast.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_mideast = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_talk_politics_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_politics_misc = json.loads(s)


with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN\\c_talk_religion_misc.txt', 'r') as f:
    s = f.read()
    centroide_classe_talk_religion_misc = json.loads(s)
###################################################################################



'''
# #QUI SOTTO CONSIDERO I CENTROIDI TENENDO CONTO DEI LEMMI DI WN:
# #Ho usato la mia funzione "classe più vicina" per trovare i NEGS di ogni classe.
# #Per disambiguare ogni lemma come contesto per ciascuno di essi ho utilizzato al max i 4 lemmi precedenti e i 4 lemmi successivi ad esso.

# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_alt_atheism.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_alt_atheism = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_comp_graphics.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_comp_graphics = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_comp_os_ms_windows_misc.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_comp_os_ms_windows_misc = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_comp_sys_ibm_pc_hardware.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_comp_sys_ibm_pc_hardware = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_comp_sys_mac_hardware.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_comp_sys_mac_hardware = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_comp_windows_x.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_comp_windows_x = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_misc_forsale.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_misc_forsale = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_rec_autos.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_rec_autos = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_rec_motorcycles.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_rec_motorcycles = json.loads(s)
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_rec_sport_baseball.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_rec_sport_baseball = json.loads(s)
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_rec_sport_hockey.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_rec_sport_hockey = json.loads(s)
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_sci_crypt.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_sci_crypt = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_sci_electronics.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_sci_electronics = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_sci_med.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_sci_med = json.loads(s)
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_sci_space.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_sci_space = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_soc_religion_christian.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_soc_religion_christian = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_talk_politics_guns.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_talk_politics_guns = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_talk_politics_mideast.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_talk_politics_mideast = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_talk_politics_misc.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_talk_politics_misc = json.loads(s)
#
#
# with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\Centroidi di Rocchio con scelta dei NEG più raffinata (2)-fit_trasform_migliore- i synsets di WN max 4 lemmi precedenti e 4 lemmi successivi\\c_talk_religion_misc.txt', 'r') as f:
#     s = f.read()
#     centroide_classe_talk_religion_misc = json.loads(s)
# ###################################################################################
'''

lista_contenente_tutti_i_centroidi = [] #lista che conterrà tutti i centroidi (mi servirà dopo)
lista_contenente_tutti_i_centroidi.append(centroide_classe_alt_atheism)
lista_contenente_tutti_i_centroidi.append(centroide_classe_comp_graphics)
lista_contenente_tutti_i_centroidi.append(centroide_classe_comp_os_ms_windows_misc)
lista_contenente_tutti_i_centroidi.append(centroide_classe_comp_sys_ibm_pc_hardware)
lista_contenente_tutti_i_centroidi.append(centroide_classe_comp_sys_mac_hardware)
lista_contenente_tutti_i_centroidi.append(centroide_classe_comp_windows_x)
lista_contenente_tutti_i_centroidi.append(centroide_classe_misc_forsale)
lista_contenente_tutti_i_centroidi.append(centroide_classe_rec_autos)
lista_contenente_tutti_i_centroidi.append(centroide_classe_rec_motorcycles)
lista_contenente_tutti_i_centroidi.append(centroide_classe_rec_sport_baseball)
lista_contenente_tutti_i_centroidi.append(centroide_classe_rec_sport_hockey)
lista_contenente_tutti_i_centroidi.append(centroide_classe_sci_crypt)
lista_contenente_tutti_i_centroidi.append(centroide_classe_sci_electronics)
lista_contenente_tutti_i_centroidi.append(centroide_classe_sci_med)
lista_contenente_tutti_i_centroidi.append(centroide_classe_sci_space)
lista_contenente_tutti_i_centroidi.append(centroide_classe_soc_religion_christian)
lista_contenente_tutti_i_centroidi.append(centroide_classe_talk_politics_guns)
lista_contenente_tutti_i_centroidi.append(centroide_classe_talk_politics_mideast)
lista_contenente_tutti_i_centroidi.append(centroide_classe_talk_politics_misc)
lista_contenente_tutti_i_centroidi.append(centroide_classe_talk_religion_misc)


#A questo punto devo calcolare il peso associato ad ogni termine presente sia in lista_di_tutti_i_documenti_di_TRAINING_in_inglese che
# lista_di_tutti_i_documenti_di_TEST_in_inglese con il prodotto:
# time-frequency (tf) * inverse document frequency (idf):


#CAMBIAMENTO #########################################
vectorizer = TfidfVectorizer()
vectorizer.fit(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
vectors_train  = vectorizer.transform(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
######################################################



feature_names = vectorizer.get_feature_names()
# print("feature_names: ")
# print(feature_names)
dense_train = vectors_train.todense()
denselist_train = dense_train.tolist()
df_train = pd.DataFrame(denselist_train, columns=feature_names)
#print("")
#print("df_train:")
#print(df_train) #[360 rows x 16648 columns], (360 = numero di documenti totali presenti nel training set), 16648 = numero di lemmi totali (senza duplicati) presenti nel training set.
#df_train.to_csv("Dataframe_documenti_rappresentati_da_lemmi_TRAINING.csv")



#CAMBIAMENTO #########################################
#vectorizer = TfidfVectorizer()
vectors_test  = vectorizer.transform(lista_di_tutti_i_documenti_di_TEST_in_inglese)
######################################################





feature_names = vectorizer.get_feature_names()
dense_test = vectors_test.todense()
denselist_test = dense_test.tolist()
df_test = pd.DataFrame(denselist_test, columns=feature_names)
print("")
print("df_test:")
print(len(df_test))
################### FINE CARICAMENTO DEL DATAFRAME DI TRAINING E DI TEST ################################################################################################################



#PRIMA DI POTER CLASSIFICARE OGNI DOCUMENTO DI TEST DEVO FARE IN MODO CHE ESSO ABBIA LA STESSA LUNGHEZZA DEL CENTROIDE DI OGNI CLASSE (ovvero 16648 (da 0 a 16647)):

#dizionario che mi servirà per passare dall'indice numerico della classe alla stringa del nome della classe:
dizionario_da_indice_numerico_a_classe = {0:"c_alt_atheism", 1:"c_comp_graphics", 2:"c_comp_os_ms_windows_misc", 3:"c_comp_sys_ibm_pc_hardware", 4:"c_comp_sys_mac_hardware",
                                              5:"c_comp_windows_x", 6:"c_misc_forsale", 7:"c_rec_autos", 8:"c_rec_motorcycles", 9:"c_rec_sport_baseball", 10:"c_rec_sport_hockey",
                                              11:"c_sci_crypt",12:"c_sci_electronics", 13:"c_sci_med", 14:"c_sci_space", 15:"c_soc_religion_christian", 16:"c_talk_politics_guns",
                                              17:"c_talk_politics_mideast", 18:"c_talk_politics_misc",19:"c_talk_religion_misc"}
num_documenti_predetto_correttamente = 0
NUM_DOCUMENTI_DI_TEST_TOTALI = 40
vettore_predizioni = []
vettore_risposte_corrette = []
for i in range(0, df_test.shape[0]): #scorro tutti gli esempi di test
    nome_classe_reale_del_documento_corrente = ""
    if(i<=1):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[0]
    elif((i==2) or (i==3)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[1]
    elif((i==4) or (i==5)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[2]
    elif ((i == 6) or (i == 7)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[3]
    elif ((i == 8) or (i == 9)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[4]
    elif ((i == 10) or (i == 11)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[5]
    elif ((i == 12) or (i == 13)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[6]
    elif ((i == 14) or (i == 15)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[7]
    elif ((i == 16) or (i == 17)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[8]
    elif ((i == 18) or (i == 19)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[9]
    elif ((i == 20) or (i == 21)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[10]
    elif ((i == 22) or (i == 23)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[11]
    elif ((i == 24) or (i == 25)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[12]
    elif ((i == 26) or (i == 27)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[13]
    elif ((i == 28) or (i == 29)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[14]
    elif ((i == 30) or (i == 31)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[15]
    elif ((i == 32) or (i == 33)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[16]
    elif ((i == 34) or (i == 35)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[17]
    elif ((i == 36) or (i == 37)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[18]
    elif ((i == 38) or (i == 39)):nome_classe_reale_del_documento_corrente = dizionario_da_indice_numerico_a_classe[19]

    documento_di_test_corrente = df_test.iloc[i]
    documento_di_test_utilizzabile = []
    print("documento_di_test_corrente: ")
    print(documento_di_test_corrente)
    print("")
    cont = 0 #contatore delle colonne (posso anche toglierlo)

    for nome_colonna_df_train in df_train:
        if(nome_colonna_df_train in df_test): #controllo che il lemma sia presente come colonna nel documento_di_test_corrente.
            #print("PRESENTE!")
            #print("nome_colonna_df_train: ", nome_colonna_df_train)
            valore_colonna_corrente = documento_di_test_corrente[nome_colonna_df_train]
            #if(valore_colonna_corrente != 0):
            #print("valore_colonna_corrente: ", valore_colonna_corrente)
            #print("indice di posizione: ", cont)
            documento_di_test_utilizzabile.append(valore_colonna_corrente) #aggiungo il peso associato al lemma corrente nel vettore documento_di_test_utilizzabile.
        else:
            #print("NON PRESENTE!")
            #print("nome_colonna_df_train: ", nome_colonna_df_train)
            #documento_di_test_utilizzabile[cont] = 0 #siccome il documento di test non ha quella colonna (quel lemma) allora metto 0.
            documento_di_test_utilizzabile.append(0) #aggiungo il peso 0 per il lemma corrente nel vettore documento_di_test_utilizzabile perchè quel lemma non è presente nel documento di test.

        #print("")
        cont+=1

    #Adesso poichè ho il documento_di_test_utilizzabile che sarà della stessa lunghezza di ogni centroide, posso CALCOLARE LA SIMILARITA' DEL COSENO TRA IL
    #VETTORE documento_di_test_utilizzabile e ogni centroide che rappresenta ogni classe.

    #Chiaramente la predizione del modello per il documento corrente sarà la classe che viene rappresentata dal centroide che ha ottenuto il valore di similarità del coseno
    #più alto con documento_di_test_utilizzabile corrente:

    print("documento_di_test_utilizzabile (dopo): ")
    print(documento_di_test_utilizzabile)
    print("len(documento_di_test_utilizzabile (dopo)): ")
    print(len(documento_di_test_utilizzabile))
    #print("cont: ", cont) #16648 colonne
    #print("documento_di_test_utilizzabile[1608]: ", documento_di_test_utilizzabile[1608])
    #print("documento_di_test_utilizzabile[4498]: ", documento_di_test_utilizzabile[4498])
    print("")
    #print("documento_train[687]: ", documento_train[687]) #0.016699220661753302
    #print("centroide[687]: ", centroide[687])
    #print("len(centroide): ", len(centroide))
    #print("")
    #print("")

    sim_coseno_max_per_il_documento_corrente = 0
    classe_predetta = 0
    for indice_centroide in range(0, len(lista_contenente_tutti_i_centroidi)):
        centroide_corrente = lista_contenente_tutti_i_centroidi[indice_centroide]
        sim_coseno_corrente = 1 - spatial.distance.cosine(centroide_corrente, documento_di_test_utilizzabile)
        if(sim_coseno_corrente > sim_coseno_max_per_il_documento_corrente):
            #aggiorno la sim coseno max e la classe predetta:
            sim_coseno_max_per_il_documento_corrente = sim_coseno_corrente
            classe_predetta = indice_centroide

    #A questo punto in classe predetta ho la predizione fatta dal modello per il documento corrente, solo che per avere la stringa del nome della classe predetta
    #devo usare il dizionario definito sopra:
    nome_classe_predetta = dizionario_da_indice_numerico_a_classe[classe_predetta]
    if(nome_classe_predetta == nome_classe_reale_del_documento_corrente):
        num_documenti_predetto_correttamente += 1 #predizione corretta

    vettore_risposte_corrette.append(nome_classe_reale_del_documento_corrente)
    vettore_predizioni.append(nome_classe_predetta)

print("")
print("")
print("num_documenti_predetto_correttamente: ", num_documenti_predetto_correttamente)
print("NUM_DOCUMENTI_DI_TEST_TOTALI: ", NUM_DOCUMENTI_DI_TEST_TOTALI)
print("Accuratezza finale: ", num_documenti_predetto_correttamente/NUM_DOCUMENTI_DI_TEST_TOTALI)
print("")
print("")


######################################### CREO LA MATRICE DI CONFUSIONE ################################################

import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt


print("vettore_risposte_corrette:")
print(vettore_risposte_corrette)
print("vettore_predizioni:")
print(vettore_predizioni)
# skplt.metrics.plot_confusion_matrix(vettore_predizioni,vettore_risposte_corrette)
# plt.show()

cm = confusion_matrix(vettore_risposte_corrette, vettore_predizioni)
cmp = ConfusionMatrixDisplay(cm, display_labels=np.arange(20))
fig, ax = plt.subplots(figsize=(10,10))
cmp.plot(ax=ax)
plt.show()
########################################################################################################################