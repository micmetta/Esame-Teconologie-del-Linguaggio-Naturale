import numpy as np
import importlib
import json


Estrazione_dati_BIO_tagging_Wikipedia_it_e_en = importlib.import_module("Estrazione_dati_BIO_tagging_Wikipedia_it_e_en")
Calcolo_metriche_en = importlib.import_module("Calcolo_metriche")
frasi_training_set_en_senza_tag = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_training_set_en_senza_tag()
frasi_training_set_en_con_tag = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_training_set_en_con_tag()
#frasi_test_set_en = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_test_set_en()
frasi_test_fuori_dominio_en = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_test_fuori_dominio_en()


def parola_presente_nel_training_set(parola):
    frasi_corpus = frasi_training_set_en_senza_tag
    #print(frasi_corpus)
    parola_presente = False
    for frase in frasi_corpus:
        if(parola_presente):
            break
        frase = frase.split(" ")
        frase[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        #print("frase: ", frase)
        for parola_corrente in frase:
            if(parola_corrente == parola):
                parola_presente = True
                break
    return parola_presente



def tag_piu_frequente(parola):
    frasi_corpus = frasi_training_set_en_con_tag
    num_tag_B_PER_per_la_parola_di_input = 0
    num_tag_I_PER_per_la_parola_di_input = 0
    num_tag_B_ORG_per_la_parola_di_input = 0
    num_tag_I_ORG_per_la_parola_di_input = 0
    num_tag_B_LOC_per_la_parola_di_input = 0
    num_tag_I_LOC_per_la_parola_di_input = 0
    num_tag_B_MISC_per_la_parola_di_input = 0
    num_tag_I_MISC_per_la_parola_di_input = 0
    num_tag_O_per_la_parola_di_input = 0
    # print("len(frasi_corpus): ", len(frasi_corpus))
    # print("")
    for frase in frasi_corpus:
        frase = frase.split(" ")
        frase[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("frase: ", frase)
        for i in range(0, len(frase)):
            parola_corrente = frase[i].split("\t")[0]
            tag_assegnato_alla_parola_corrente = frase[i].split("\t")[1]
            if (parola_corrente == parola):
                if (tag_assegnato_alla_parola_corrente == "B-PER"):
                    num_tag_B_PER_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-PER"):
                    num_tag_I_PER_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-ORG"):
                    num_tag_B_ORG_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-ORG"):
                    num_tag_I_ORG_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-LOC"):
                    num_tag_B_LOC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-LOC"):
                    num_tag_I_LOC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-MISC"):
                    num_tag_B_MISC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-MISC"):
                    num_tag_I_MISC_per_la_parola_di_input += 1
                else:
                    num_tag_O_per_la_parola_di_input += 1

    #A questo punto posso capire qual è il tag piu' frequente per la parola di input.
    #Per farlo, metto tutti i valori dei tag per la parola in un dizionario e poi prendo il tag massimo
    dizionario_count_tags_parola_di_input = {}
    dizionario_count_tags_parola_di_input["B-PER"] = num_tag_B_PER_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["I-PER"] = num_tag_I_PER_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["B-ORG"] = num_tag_B_ORG_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["I-ORG"] = num_tag_I_ORG_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["B-LOC"] = num_tag_B_LOC_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["I-LOC"] = num_tag_I_LOC_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["B-MISC"] = num_tag_B_MISC_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["I-MISC"] = num_tag_I_MISC_per_la_parola_di_input
    dizionario_count_tags_parola_di_input["O"] = num_tag_O_per_la_parola_di_input

    tag_piu_frequente = max(dizionario_count_tags_parola_di_input, key=dizionario_count_tags_parola_di_input.get)
    ################################################################################

    return tag_piu_frequente





############################################################     MAIN BASELINE    ##########################################################################################################################

tags_assegnati_a_tutte_le_frasi_di_test = [] #mi servirà per memorizzare tutte le predizioni fatte per tutte le frasi di test (puoi crearlo dinamicamente con numpy)

#Creo un dizionario normale che tiene conto delle parole per le quali è già stato trovato il tag più frequente, in questo modo velocizzo l'algoritmo in quanto
#per queste parole non dovrò trovarlo nuovamente. (Più l'algoritmo considera nuove parole e più la prob. che la velocità di esecuzione aumenti si incrementa)
# Esempio di come sarà il dizionario:
# dizionario_con_tag_piu_frequente_di_parole_gia_considerate = {"parola1":"B-PER",
#                                                               "parola2":"O",
#                                                                ...,
#                                                               }
#dizionario_con_tag_piu_frequente_di_parole_gia_considerate = {}


#deserializzo il dizionario_con_tag_piu_frequente_di_parole_gia_considerate che ho già pre-calcolato:
with open('dizionario_con_tag_piu_frequente_di_parole_gia_considerate_en_B-MISC.json', 'r') as json_file:
    dizionario_con_tag_piu_frequente_di_parole_gia_considerate = json.load(json_file)
#####################################################################################################


######################################################################################################
for frase_test in frasi_test_fuori_dominio_en:
    tags_assegnati_frase_di_test_corrente = []  # conterrà i tags ordinati dalla prima parola all'ultima che vengono assegnati dalla baseline alle parole della frase di test corrente.
    #if(num_frasi_considerate < 3): #considero solo le prime 3 frasi di test
    print("frase_test: ")
    print(frase_test)
    frase_test_splittata_per_singola_parola = frase_test.split(" ")
    frase_test_splittata_per_singola_parola[-1:] = [] # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
    print("frase_test_splittata_per_singola_parola: ")
    print(frase_test_splittata_per_singola_parola)
    print("")
    print("")
    for i in range(0, len(frase_test_splittata_per_singola_parola)): #scorro tutte le parole della frase di test corrente
        parola_frase_test_con_tag = frase_test.split(" ")[i]
        parola_frase_test = parola_frase_test_con_tag.split("\t")[0]
        print("parola_frase_test: ", parola_frase_test)

        #controllo subito se il tag più frequente per la parola corrente l'ho già memorizzato:
        if ((parola_frase_test in dizionario_con_tag_piu_frequente_di_parole_gia_considerate) == False):
            #Se entro qui vuol dire che non ho ancora memorizzato il tag più probabile per la parola corrente.

            #Controllo se la parola è presente nel training set:
            if(parola_presente_nel_training_set(parola_frase_test)):
                #vuol dire che la parola è presente nel training set quindi devo trovare qual è il tag che gli viene assegnato più frequentemente:
                tag_max = tag_piu_frequente(parola_frase_test)
                tags_assegnati_frase_di_test_corrente.append(tag_max)
                #memorizzo il tag più frequente nel dizionario (ottimizzazione):
                dizionario_con_tag_piu_frequente_di_parole_gia_considerate[parola_frase_test] = tag_max
                print("tag_max: ", tag_max)
            else:
                #gli assegno il tag O
                tags_assegnati_frase_di_test_corrente.append("B-MISC")
                #memorizzo il tag più frequente nel dizionario (ottimizzazione):
                dizionario_con_tag_piu_frequente_di_parole_gia_considerate[parola_frase_test] = "B-MISC"
                print("tag_max assegnato: "+"B-MISC")

        else:
            #Se entro qui vuol dire che ho già memorizzato il tag più frequente per la parola corrente:
            tag_max = dizionario_con_tag_piu_frequente_di_parole_gia_considerate[parola_frase_test]
            tags_assegnati_frase_di_test_corrente.append(tag_max)
            print("tag_max già memorizzato ed era: ", tag_max)

    tags_assegnati_a_tutte_le_frasi_di_test.append(tags_assegnati_frase_di_test_corrente)
    ####################################################

#Serializzo il dizionario_con_tag_piu_frequente_di_parole_gia_considerate in modo tale che dalla volta successiva li avrò già tutti a disposizione:
# Dumping it to file
# with open('dizionario_con_tag_piu_frequente_di_parole_gia_considerate_en.json', 'w') as json_file:
#     json.dump(dizionario_con_tag_piu_frequente_di_parole_gia_considerate, json_file)
# print("Il dizionario che contiene i tag più frequenti già calcolati per ogni parola è stato serializzato correttamente.")
###################################################################################################################################################


print("")
print("TAGS PREDETTI PER OGNI FRASE DI TEST: ")
print(tags_assegnati_a_tutte_le_frasi_di_test)
print("")


#Adesso calcolo l'accuratezza della baseline:
accuratezza_baseline = Calcolo_metriche_en.accuratezza(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test)
print("accuratezza_baseline: ", accuratezza_baseline)
print("")
precision_modello = Calcolo_metriche_en.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("precisione_modello PER: ", precision_modello)
precision_modello = Calcolo_metriche_en.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("precisione_modello LOC: ", precision_modello)
precision_modello = Calcolo_metriche_en.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("precisione_modello ORG: ", precision_modello)
precision_modello = Calcolo_metriche_en.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("precisione_modello MISC: ", precision_modello)


print("")
recall_modello = Calcolo_metriche_en.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("recall_modello PER: ", recall_modello)
recall_modello = Calcolo_metriche_en.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("recall_modello LOC: ", recall_modello)
recall_modello = Calcolo_metriche_en.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("recall_modello ORG: ", recall_modello)
recall_modello = Calcolo_metriche_en.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("recall_modello MISC: ", recall_modello)
print("")


print("")
acc_modello_B_I_PER = Calcolo_metriche_en.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("acc_modello_B_I_PER: ", acc_modello_B_I_PER)
acc_modello_B_I_LOC = Calcolo_metriche_en.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("acc_modello_B_I_LOC: ", acc_modello_B_I_LOC)
acc_modello_B_I_ORG = Calcolo_metriche_en.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("acc_modello_B_I_ORG: ", acc_modello_B_I_ORG)
acc_modello_B_I_MISC = Calcolo_metriche_en.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("acc_modello_B_I_MISC: ", acc_modello_B_I_MISC)
print("")

print("")
acc_modello_B_I_consecutivi_PER = Calcolo_metriche_en.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("acc_modello_B_I_consecutivi_PER: ", acc_modello_B_I_consecutivi_PER)
acc_modello_B_I_consecutivi_LOC = Calcolo_metriche_en.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("acc_modello_B_I_consecutivi_LOC: ", acc_modello_B_I_consecutivi_LOC)
acc_modello_B_I_consecutivi_ORG = Calcolo_metriche_en.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("acc_modello_B_I_consecutivi_ORG: ", acc_modello_B_I_consecutivi_ORG)
acc_modello_B_I_consecutivi_MISC = Calcolo_metriche_en.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("acc_modello_B_I_consecutivi_MISC: ", acc_modello_B_I_consecutivi_MISC)
print("")


print("Esecuzione terminata.")
############################################################################################################################################################################################################
