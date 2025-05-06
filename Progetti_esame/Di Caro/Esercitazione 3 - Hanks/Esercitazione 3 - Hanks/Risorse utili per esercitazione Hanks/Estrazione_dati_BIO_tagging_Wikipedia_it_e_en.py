import numpy as np
import pandas as pd
import csv
from datasets import load_dataset, load_metric, concatenate_datasets

def caricamento_dati_BIO_tagging_en ():
    #leggo le frasi dal training set:
    file_train = open("Risorse utili per esercitazione Hanks/datasets_en/train.conllu", "r", encoding="utf8")
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


    ########################### variabili utili: ############################################
    #B-PER, I-PER
    #B-ORG, I-ORG
    #B-LOC, I-LOC
    #B-MISC, I-MISC
    #O
    tag_possibili = ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC", "O"]
    #Il dizionario qui sotto verrà utilizzato per capire quale valore numerico è associato ad ogni tag nell'algoritmo di Viterbi.
    dizionario_indice_numerico_tag = {0:"B-PER", 1:"I-PER",
                                      2:"B-ORG", 3:"I-ORG",
                                      4:"B-LOC", 5:"I-LOC",
                                      6:"B-MISC", 7:"I-MISC",
                                      8:"O",
                                      }
    #Mi servirà alla fine dell'algoritmo di Viterbi.
    dizionario_per_passare_dal_tag_al_numero = {"B-PER":0, "I-PER":1,
                                                "B-ORG":2, "I-ORG":3,
                                                "B-LOC":4, "I-LOC":5,
                                                "B-MISC":6,"I-MISC":7,
                                                "O":8}
    #Nel dizionario di sotto invece, metterò tutte le probabilità di transizione da un qualsiasi tag ad un altro qualsiasi tag.
    a_s_primo_s = {
                    #B-PER:
                    "B-PER|S":0,"B-PER|B-PER":0,"I-PER|B-PER":0,"B-ORG|B-PER":0,"I-ORG|B-PER":0,"B-LOC|B-PER":0,"I-LOC|B-PER":0,"B-MISC|B-PER":0,"I-MISC|B-PER":0,"O|B-PER":0,"E|B-PER":0,
                    #I-PER:
                    "I-PER|S":0,"B-PER|I-PER":0,"I-PER|I-PER":0,"B-ORG|I-PER":0,"I-ORG|I-PER":0,"B-LOC|I-PER":0,"I-LOC|I-PER":0,"B-MISC|I-PER":0,"I-MISC|I-PER":0,"O|I-PER":0,"E|I-PER":0,
                    #B-ORG:
                    "B-ORG|S":0,"B-PER|B-ORG":0,"I-PER|B-ORG":0,"B-ORG|B-ORG":0,"I-ORG|B-ORG":0,"B-LOC|B-ORG":0,"I-LOC|B-ORG":0,"B-MISC|B-ORG":0,"I-MISC|B-ORG":0,"O|B-ORG":0,"E|B-ORG":0,
                    #I-ORG:
                    "I-ORG|S":0,"B-PER|I-ORG":0,"I-PER|I-ORG":0,"B-ORG|I-ORG":0,"I-ORG|I-ORG":0,"B-LOC|I-ORG":0,"I-LOC|I-ORG":0,"B-MISC|I-ORG":0,"I-MISC|I-ORG":0,"O|I-ORG":0,"E|I-ORG":0,
                    #B-LOC:
                    "B-LOC|S":0,"B-PER|B-LOC":0,"I-PER|B-LOC":0,"B-ORG|B-LOC":0,"I-ORG|B-LOC":0,"B-LOC|B-LOC":0,"I-LOC|B-LOC":0,"B-MISC|B-LOC":0,"I-MISC|B-LOC":0,"O|B-LOC":0,"E|B-LOC":0,
                    #I-LOC:
                    "I-LOC|S":0,"B-PER|I-LOC":0,"I-PER|I-LOC":0,"B-ORG|I-LOC":0,"I-ORG|I-LOC":0,"B-LOC|I-LOC":0,"I-LOC|I-LOC":0,"B-MISC|I-LOC":0,"I-MISC|I-LOC":0,"O|I-LOC":0,"E|I-LOC":0,
                    #B-MISC:
                    "B-MISC|S":0,"B-PER|B-MISC":0,"I-PER|B-MISC":0,"B-ORG|B-MISC":0,"I-ORG|B-MISC":0,"B-LOC|B-MISC":0,"I-LOC|B-MISC":0,"B-MISC|B-MISC":0,"I-MISC|B-MISC":0,"O|B-MISC":0,"E|B-MISC":0,
                    #I-MISC:
                    "I-MISC|S":0,"B-PER|I-MISC":0,"I-PER|I-MISC":0,"B-ORG|I-MISC":0,"I-ORG|I-MISC":0,"B-LOC|I-MISC":0,"I-LOC|I-MISC":0,"B-MISC|I-MISC":0,"I-MISC|I-MISC":0,"O|I-MISC":0,"E|I-MISC":0,
                    #O:
                    "O|S":0,"B-PER|O":0,"I-PER|O":0,"B-ORG|O":0,"I-ORG|O":0,"B-LOC|O":0,"I-LOC|O":0,"B-MISC|O":0,"I-MISC|O":0,"O|O":0,"E|O":0,
                  }
    #########################################################################################


    return frasi_corpus,tag_possibili,dizionario_indice_numerico_tag,dizionario_per_passare_dal_tag_al_numero,a_s_primo_s




def caricamento_dati_BIO_tagging_it ():
    #leggo le frasi dal training set:
    file_train = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\it\\train.conllu", "r", encoding="utf8")
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


    ########################### variabili utili: ############################################
    #B-PER, I-PER
    #B-ORG, I-ORG
    #B-LOC, I-LOC
    #B-MISC, I-MISC
    #O
    tag_possibili = ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC", "O"]
    #Il dizionario qui sotto verrà utilizzato per capire quale valore numerico è associato ad ogni tag nell'algoritmo di Viterbi.
    dizionario_indice_numerico_tag = {0:"B-PER", 1:"I-PER",
                                      2:"B-ORG", 3:"I-ORG",
                                      4:"B-LOC", 5:"I-LOC",
                                      6:"B-MISC", 7:"I-MISC",
                                      8:"O",
                                      }
    #Mi servirà alla fine dell'algoritmo di Viterbi.
    dizionario_per_passare_dal_tag_al_numero = {"B-PER":0, "I-PER":1,
                                                "B-ORG":2, "I-ORG":3,
                                                "B-LOC":4, "I-LOC":5,
                                                "B-MISC":6,"I-MISC":7,
                                                "O":8}
    #Nel dizionario di sotto invece, metterò tutte le probabilità di transizione da un qualsiasi tag ad un altro qualsiasi tag.
    a_s_primo_s = {
                    #B-PER:
                    "B-PER|S":0,"B-PER|B-PER":0,"I-PER|B-PER":0,"B-ORG|B-PER":0,"I-ORG|B-PER":0,"B-LOC|B-PER":0,"I-LOC|B-PER":0,"B-MISC|B-PER":0,"I-MISC|B-PER":0,"O|B-PER":0,"E|B-PER":0,
                    #I-PER:
                    "I-PER|S":0,"B-PER|I-PER":0,"I-PER|I-PER":0,"B-ORG|I-PER":0,"I-ORG|I-PER":0,"B-LOC|I-PER":0,"I-LOC|I-PER":0,"B-MISC|I-PER":0,"I-MISC|I-PER":0,"O|I-PER":0,"E|I-PER":0,
                    #B-ORG:
                    "B-ORG|S":0,"B-PER|B-ORG":0,"I-PER|B-ORG":0,"B-ORG|B-ORG":0,"I-ORG|B-ORG":0,"B-LOC|B-ORG":0,"I-LOC|B-ORG":0,"B-MISC|B-ORG":0,"I-MISC|B-ORG":0,"O|B-ORG":0,"E|B-ORG":0,
                    #I-ORG:
                    "I-ORG|S":0,"B-PER|I-ORG":0,"I-PER|I-ORG":0,"B-ORG|I-ORG":0,"I-ORG|I-ORG":0,"B-LOC|I-ORG":0,"I-LOC|I-ORG":0,"B-MISC|I-ORG":0,"I-MISC|I-ORG":0,"O|I-ORG":0,"E|I-ORG":0,
                    #B-LOC:
                    "B-LOC|S":0,"B-PER|B-LOC":0,"I-PER|B-LOC":0,"B-ORG|B-LOC":0,"I-ORG|B-LOC":0,"B-LOC|B-LOC":0,"I-LOC|B-LOC":0,"B-MISC|B-LOC":0,"I-MISC|B-LOC":0,"O|B-LOC":0,"E|B-LOC":0,
                    #I-LOC:
                    "I-LOC|S":0,"B-PER|I-LOC":0,"I-PER|I-LOC":0,"B-ORG|I-LOC":0,"I-ORG|I-LOC":0,"B-LOC|I-LOC":0,"I-LOC|I-LOC":0,"B-MISC|I-LOC":0,"I-MISC|I-LOC":0,"O|I-LOC":0,"E|I-LOC":0,
                    #B-MISC:
                    "B-MISC|S":0,"B-PER|B-MISC":0,"I-PER|B-MISC":0,"B-ORG|B-MISC":0,"I-ORG|B-MISC":0,"B-LOC|B-MISC":0,"I-LOC|B-MISC":0,"B-MISC|B-MISC":0,"I-MISC|B-MISC":0,"O|B-MISC":0,"E|B-MISC":0,
                    #I-MISC:
                    "I-MISC|S":0,"B-PER|I-MISC":0,"I-PER|I-MISC":0,"B-ORG|I-MISC":0,"I-ORG|I-MISC":0,"B-LOC|I-MISC":0,"I-LOC|I-MISC":0,"B-MISC|I-MISC":0,"I-MISC|I-MISC":0,"O|I-MISC":0,"E|I-MISC":0,
                    #O:
                    "O|S":0,"B-PER|O":0,"I-PER|O":0,"B-ORG|O":0,"I-ORG|O":0,"B-LOC|O":0,"I-LOC|O":0,"B-MISC|O":0,"I-MISC|O":0,"O|O":0,"E|O":0,
                  }
    #########################################################################################


    return frasi_corpus,tag_possibili,dizionario_indice_numerico_tag,dizionario_per_passare_dal_tag_al_numero,a_s_primo_s


#Questa è la funzione che mi permette di poter calcolare per ogni possible tag il Count(tag) ovvero il numero di volte in cui un certo tag è
#stato assegnato ad una parola del training set.
def calcolo_C_s(frasi_corpus):
    dizionario_count_tags = {"B-PER":0, "I-PER":0,
               "B-ORG":0, "I-ORG":0,
               "B-LOC":0, "I-LOC":0,
               "B-MISC":0,"I-MISC":0,
               "O":0
               }
    # calcolo C_s con s che scorre tutti i possibili tag:##############################################
    C_B_PER = 0  # numero di parole a cui è stato associato il tag B-PER nel corpus
    C_I_PER = 0  # numero di parole a cui è stato associato il tag I-PER nel corpus
    C_B_ORG = 0
    C_I_ORG = 0
    C_B_LOC = 0
    C_I_LOC = 0
    C_B_MISC = 0
    C_I_MISC = 0
    C_O = 0
    for frase in frasi_corpus:
        frase = frase.split(" ")
        frase[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("frase: ", frase)
        for i in range(0, len(frase)):
            tag_assegnato_alla_parola_corrente = frase[i].split("\t")[1]
            if (tag_assegnato_alla_parola_corrente == "B-PER"):
                C_B_PER += 1
            elif (tag_assegnato_alla_parola_corrente == "I-PER"):
                C_I_PER += 1
            elif (tag_assegnato_alla_parola_corrente == "B-ORG"):
                C_B_ORG += 1
            elif (tag_assegnato_alla_parola_corrente == "I-ORG"):
                C_I_ORG += 1
            elif (tag_assegnato_alla_parola_corrente == "B-LOC"):
                C_B_LOC += 1
            elif (tag_assegnato_alla_parola_corrente == "I-LOC"):
                C_I_LOC += 1
            elif (tag_assegnato_alla_parola_corrente == "B-MISC"):
                C_B_MISC += 1
            elif (tag_assegnato_alla_parola_corrente == "I-MISC"):
                C_I_MISC += 1
            else:
                C_O += 1
    dizionario_count_tags["B-PER"] = C_B_PER
    dizionario_count_tags["I-PER"] = C_I_PER
    dizionario_count_tags["B-ORG"] = C_B_ORG
    dizionario_count_tags["I-ORG"] = C_I_ORG
    dizionario_count_tags["B-LOC"] = C_B_LOC
    dizionario_count_tags["I-LOC"] = C_I_LOC
    dizionario_count_tags["B-MISC"] = C_B_MISC
    dizionario_count_tags["I-MISC"] = C_I_MISC
    dizionario_count_tags["O"] = C_O
    # PUOI CALCOLARLO UNA VOLTA SOLA..
    # print("")
    # print("Numero di volte che il tag B-PER è stato assegnato ad una parola nel corpus: ", C_B_PER)
    # print("Numero di volte che il tag I-PER è stato assegnato ad una parola nel corpus: ", C_I_PER)
    # print("Numero di volte che il tag B-ORG è stato assegnato ad una parola nel corpus: ", C_B_ORG)
    # print("Numero di volte che il tag I-ORG è stato assegnato ad una parola nel corpus: ", C_I_ORG)
    # print("Numero di volte che il tag B-LOC è stato assegnato ad una parola nel corpus: ", C_B_LOC)
    # print("Numero di volte che il tag I-LOC è stato assegnato ad una parola nel corpus: ", C_I_LOC)
    # print("Numero di volte che il tag B-MISC è stato assegnato ad una parola nel corpus: ", C_B_MISC)
    # print("Numero di volte che il tag I-MISC è stato assegnato ad una parola nel corpus: ", C_I_MISC)
    # print("Numero di volte che il tag O è stato assegnato ad una parola nel corpus: ", C_O) #87526
    # print("")

    return dizionario_count_tags


def frasi_training_set_en_senza_tag():
    file_train = open("datasets_en/train.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_train.readline()
    while line != "":
        line = line.split()
        # print(line)
        if (line != []):
            frase_corrente = frase_corrente + line[1] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_train.readline()
    # print(frasi_corpus)
    # print("")
    # print("")
    # print("Numero totale di frasi:", len(frasi_corpus))
    file_train.close()

    return frasi_corpus



def frasi_training_set_it_senza_tag():
    file_train = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\it\\train.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_train.readline()
    while line != "":
        line = line.split()
        # print(line)
        if (line != []):
            frase_corrente = frase_corrente + line[1] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_train.readline()
    # print(frasi_corpus)
    # print("")
    # print("")
    # print("Numero totale di frasi:", len(frasi_corpus))
    file_train.close()

    return frasi_corpus


def frasi_training_set_en_con_tag():
    file_train = open("datasets_en/train.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_train.readline()
    while line != "":
        line = line.split()
        # print(line)
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_train.readline()
    # print(frasi_corpus)
    # print("")
    # print("")
    # print("Numero totale di frasi:", len(frasi_corpus))
    file_train.close()

    return frasi_corpus


def frasi_training_set_it_con_tag():
    file_train = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\it\\train.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_train.readline()
    while line != "":
        line = line.split()
        # print(line)
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_train.readline()
    # print(frasi_corpus)
    # print("")
    # print("")
    # print("Numero totale di frasi:", len(frasi_corpus))
    file_train.close()

    return frasi_corpus


def frasi_test_set_en(): #con tags
    file_test = open("Risorse utili per esercitazione Hanks/datasets_en/test.conllu", "r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus



def frasi_test_set_it(): #con tags
    file_test = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\it\\test.conllu", "r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus



def frasi_validation_set_en_con_tags():
    file_test = open("Risorse utili per esercitazione Hanks/datasets_en/val.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus



def frasi_validation_set_it_con_tags():
    file_test = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\Datasets BIO tagg\\it\\val.conllu","r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus



def frasi_test_fuori_dominio_it(): #con tags
    file_test = open("C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Mazzei\\frasi_fuori_dominio.conllu", "r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus


def frasi_test_fuori_dominio_en(): #con tags
    file_test = open("frasi_fuori_dominio.conllu", "r", encoding="utf8")
    frasi_corpus = []
    frase_corrente = ""
    line = file_test.readline()
    while line != "":
        line = line.split()
        if (line != []):
            frase_corrente = frase_corrente + line[1] + "\t" + line[2] + " "
        else:
            frasi_corpus.append(frase_corrente)
            frase_corrente = ""
        line = file_test.readline()
    file_test.close()

    return frasi_corpus


#x = caricamento_dati_BIO_tagging_it()

