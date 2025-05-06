
import importlib
import json


# Questo codice mi serve per trovare tutte le parole che compaiono una sola volta nel development set e per calcolare le prob. di emissione da utilizzare per le
# parole sconosciute utilizzando la distribuzione di prob. sui vari ner tags calcolata in base alle parole che compaiono una sola volta nel VS:


'''
#Questo codice commentato mi è servito per prendere tutte le parole presenti nel VS una sola volta e salvarle in un unico file di testo chiamato
#"parole che compaiono una sola volta nel Validation Set_en.txt"

#leggo le frasi dal validation set (in questo caso inglese):
file_train = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\en\\val.conllu", "r", encoding="utf8")
frasi_corpus = []
frase_corrente = ""
line = file_train.readline()
while line != "":
    line = line.split()
    #print(line)
    if(line != []):
        frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
    else:
        frasi_corpus.append(frase_corrente)
        frase_corrente = ""
    line = file_train.readline()
#print(frasi_corpus)
#print("")
#print("")
#print("Numero totale di frasi:", len(frasi_corpus))
file_train.close()


num_tag_B_PER = 0
num_tag_I_PER = 0
num_tag_B_ORG = 0
num_tag_I_ORG = 0
num_tag_B_LOC = 0
num_tag_I_LOC = 0
num_tag_B_MISC = 0
num_tag_I_MISC = 0
num_tag_O = 0
contatore_numero_parole_che_compaiono_una_sola_volta_nel_VS = 0
parole_che_compaiono_una_sola_volta_nel_corpus = []
print(frasi_corpus[0])
for frase in frasi_corpus:
    frase = frase.split(" ")
    frase[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
    #print("frase: ", frase)
    for i in range(0, len(frase)):
        parola_corrente = frase[i].split("\t")[0]
        tag_assegnato_alla_parola = frase[i].split("\t")[1]
        numero_di_volte_che_compare_la_parola_corrente_nel_corpus = 0
        esci_dal_ciclo = False

        #riparto con un altro ciclo in cui scorro tutto il corpus dall'inizio alla fine per vedere quante volte compare la parola corrente (1 volta comparirà sicuramete perchè altrimenti non
        #la starei considerando):
        for frase_for_interno in frasi_corpus:
            frase_for_interno = frase_for_interno.split(" ")
            frase_for_interno[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
            # print("frase: ", frase)
            if(esci_dal_ciclo):
                break
            else:
                for i in range(0, len(frase_for_interno)):
                    parola = frase_for_interno[i].split("\t")[0]
                    if (parola_corrente == parola):
                        numero_di_volte_che_compare_la_parola_corrente_nel_corpus += 1
                        if(numero_di_volte_che_compare_la_parola_corrente_nel_corpus > 1):
                            #devo uscire dal ciclo corrente perchè vuol dire che parola_corrente è presente nel corpus più di una volta e quindi non mi interessa considerarla:
                            #print("La parola " + parola_corrente + " è presente più di una volta nel corpus quindi non la considero.")
                            esci_dal_ciclo = True
                            break
        if(numero_di_volte_che_compare_la_parola_corrente_nel_corpus == 1):
            #print("La parola " + parola_corrente + " è presente una sola volta nel corpus quindi devo considerarla con il suo tag che è "+tag_assegnato_alla_parola+".")
            print(parola_corrente+"\t"+tag_assegnato_alla_parola)
            contatore_numero_parole_che_compaiono_una_sola_volta_nel_VS += 1
            print("contatore_numero_parole_che_compaiono_una_sola_volta_nel_VS: ", contatore_numero_parole_che_compaiono_una_sola_volta_nel_VS)
            print("")
            parole_che_compaiono_una_sola_volta_nel_corpus.append(parola_corrente+"\t"+tag_assegnato_alla_parola)
            if (tag_assegnato_alla_parola == "B-PER"):
                num_tag_B_PER += 1
            elif (tag_assegnato_alla_parola == "I-PER"):
                num_tag_I_PER += 1
            elif (tag_assegnato_alla_parola == "B-ORG"):
                num_tag_B_ORG += 1
            elif (tag_assegnato_alla_parola == "I-ORG"):
                num_tag_I_ORG += 1
            elif (tag_assegnato_alla_parola == "B-LOC"):
                num_tag_B_LOC += 1
            elif (tag_assegnato_alla_parola == "I-LOC"):
                num_tag_I_LOC += 1
            elif (tag_assegnato_alla_parola == "B-MISC"):
                num_tag_B_MISC += 1
            elif (tag_assegnato_alla_parola == "I-MISC"):
                num_tag_I_MISC += 1
            else:
                num_tag_O += 1


print("parole_che_compaiono_una_sola_volta_nel_corpus:")
print(parole_che_compaiono_una_sola_volta_nel_corpus) #le ho salvate nel file chiamato "parole che compaiono una sola volta nel Validation Set.txt


#mi salvo in questo dizionario per ogni tag quante parole presenti nel validation set sono state taggate con esso:
dizionario_num_parole_per_ogni_tag = {"B-PER":0, "I-PER":0,
                                      "B-ORG":0, "I-ORG":0,
                                      "B-LOC":0, "I-LOC":0,
                                      "B-MISC":0,"I-MISC":0,
                                      "O":0}

dizionario_num_parole_per_ogni_tag["B-PER"] = num_tag_B_PER
dizionario_num_parole_per_ogni_tag["I-PER"] = num_tag_I_PER
dizionario_num_parole_per_ogni_tag["B-ORG"] = num_tag_B_ORG
dizionario_num_parole_per_ogni_tag["I-ORG"] = num_tag_I_ORG
dizionario_num_parole_per_ogni_tag["B-LOC"] = num_tag_B_LOC
dizionario_num_parole_per_ogni_tag["I-LOC"] = num_tag_I_LOC
dizionario_num_parole_per_ogni_tag["B-MISC"] = num_tag_B_MISC
dizionario_num_parole_per_ogni_tag["I-MISC"] = num_tag_I_MISC
dizionario_num_parole_per_ogni_tag["O"] = num_tag_O

# with open('dizionario_num_parole_per_ogni_tag_nel_Development_Set_en.json', 'w', encoding='UTF-8') as json_file:
#     json.dump(dizionario_num_parole_per_ogni_tag, json_file)
################################################################################################################


file = open("parole che compaiono una sola volta nel Validation Set_en.txt", "w", encoding='UTF-8')
file.write(parole_che_compaiono_una_sola_volta_nel_corpus)
file.close()
'''


with open('dizionario_num_parole_per_ogni_tag_nel_Development_Set_en.json', 'r') as json_file:
    dizionario_num_parole_per_ogni_tag_nel_Development_Set = json.load(json_file)

file = open('parole che compaiono una sola volta nel Validation Set_en.txt', 'r', encoding='UTF-8')
lista_parole_che_compaiono_una_sola_volta_nel_VS = file.read()
file.close()

lista_parole_che_compaiono_una_sola_volta_nel_VS = lista_parole_che_compaiono_una_sola_volta_nel_VS.split(",")
print("num di parole che compaiono una sola volta: ", len(lista_parole_che_compaiono_una_sola_volta_nel_VS)) #17673
num_parole_totali_che_compaiono_una_sola_volta_nel_VS = len(lista_parole_che_compaiono_una_sola_volta_nel_VS)

probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing = {"B-PER": 0, "I-PER": 0,
                                                                            "B-ORG": 0, "I-ORG": 0,
                                                                            "B-LOC": 0, "I-LOC": 0,
                                                                            "B-MISC": 0, "I-MISC": 0,
                                                                            "O": 0
                                                                            }

probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["B-PER"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["B-PER"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["I-PER"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["I-PER"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["B-ORG"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["B-ORG"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["I-ORG"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["I-ORG"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["B-LOC"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["B-LOC"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["I-LOC"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["I-LOC"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["B-MISC"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["B-MISC"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["I-MISC"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["I-MISC"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS
probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing["O"] = dizionario_num_parole_per_ogni_tag_nel_Development_Set["O"] / num_parole_totali_che_compaiono_una_sola_volta_nel_VS

print("le prob. di emissione sono queste: ")
print(probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing)

#serializzo le prob. di emissione calcolate con questa tecnica di smoothing:#####################################################################################################
# with open('dizionario_con_prob_di_emissione_di_parole_gia_considerate_VS.json', 'w', encoding='UTF-8') as json_file:
#     json.dump(probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing, json_file)
# print("Il dizionario che contiene le prob. di emissione già calcolate è stato serializzato correttamente.")
with open('prob_di_emissione_pre_calcolate_per_le_parole_sconosciute_assegnate_dalla_tecnica_che_utilizza_il_DS_en.json', 'w', encoding='UTF-8') as json_file:
    json.dump(probabilita_di_emissione_finali_assegnate_da_questa_tecnica_di_smoothing, json_file)
print("Il dizionario che contiene le prob. di emissione già calcolate è stato serializzato correttamente.")
##################################################################################################################################################################################