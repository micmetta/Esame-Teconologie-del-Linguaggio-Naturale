import concepts
import graphviz
from pathlib import Path
import os
import json
import random
import spacy
from nltk.corpus import stopwords
import csv


#Funzione che prende in input una frase (sottoforma di stringa) e restituisce il suo parser a dipendenze.
def get_parser_a_dipendenze(frase):
    parser_frase = nlp(frase)

    #Adesso rimuovo le stopwords e la punteggiatura dal parser corrente:
    parser_frase_senza_sw = [word for word in parser_frase if word.text.lower() not in stop_words]

    return parser_frase_senza_sw



def get_frase_casuale(path):
    lista_frasi = []
    with open(path, "r") as file:
        for frase in file:
            lista_frasi.append(frase)

    #num_frase_casuale = random.randint(0, len(lista_frasi)-1) #scelta randomica
    num_frase_casuale = 7 #per test

    # print("lista_frasi:", lista_frasi)
    # print("num_frase_casuale:", num_frase_casuale)
    print("lista_frasi[num_frase_casuale]:")
    print(lista_frasi[num_frase_casuale])
    print("")

    return lista_frasi[num_frase_casuale]



def get_matrice_adiacenza(path):
    return concepts.load_csv(path)


# Questa funzione prende in input il parser di una frase.
# In output restituisce una lista di liste in cui ogni lista interna è una coppia formata da [nome_dipendenza,parola].
# Es di output: [[nome_dipendenza,parola1], [nome_dipendenza,parola2], [nome_dipendenza,parola3]]
def get_lista_coppie_dipendenza_parola(parser_frase):
    lista_coppie = []
    for token in parser_frase:
        # token.text -> parola sotto la testa.
        # token.tag_ -> PoS della parola.
        # token.head.text -> testa della dipendenza.
        # token.dep_ -> nome della dipendenza che và dalla testa alla parola sotto la testa.
        print(token.text, token.tag_, token.head.text, token.dep_)
        #dizionario[token.dep_] = token.text
        nuova_coppia = []
        nuova_coppia.append(token.dep_)
        nuova_coppia.append(token.text)
        lista_coppie.append(nuova_coppia)

    print("")
    print("")

    return lista_coppie



def eliminazione_duplicati(features_da_marcare_per_parola_corrente):
    nuova_lista_senza_dupl = []
    for feature in features_da_marcare_per_parola_corrente:
        if not feature in nuova_lista_senza_dupl:
            nuova_lista_senza_dupl.append(feature)

    return nuova_lista_senza_dupl




def creazione_matrice_adiacenza(lista_di_coppie_nome_dipendenza_parola, path_matrice_adiacenza):
    features = []
    # features.append("") #mi serve per poter inserire le parole nella primissima colonna
    # Nella lista features inserirò tutti i nomi delle features (ovvero delle dipendenze) che poi diventeranno ovviamente i nomi delle colonne della matrice di adiacenza.
    for coppia in lista_di_coppie_nome_dipendenza_parola:
        if not coppia[0] in features:
            features.append(coppia[0])
    print("features:")
    print(features)
    print("")
    print("")
    #############################################################################################################################################


    ###########################################################################################################################################
    # Adesso creo una lista di liste che per ogni parola tiene traccia di quali features dovrò assegnargli nella matrice di adiacenza:
    lista_parole_features = [] #questa sarà la lista di lista citata pocanzi.
    parole_gia_considerate = []
    for coppia in lista_di_coppie_nome_dipendenza_parola:
        parola_corrente_iniziale = coppia[1]

        if(parola_corrente_iniziale not in parole_gia_considerate): #se ancora non ho considerato la parola_corrente_iniziale allora continuo altrimenti vuol dire che già so quali sono
            #le features che dovrò segnare con "X" per quella parola.

            lista_features_parola_corrente = []
            lista_features_parola_corrente.append(parola_corrente_iniziale) #in modo tale da tenere traccia delle features da assegnare ad ogni termine della frase.

            for i in range(0, len(lista_di_coppie_nome_dipendenza_parola)):
                coppia_corrente = lista_di_coppie_nome_dipendenza_parola[i]
                parola_corrente = coppia_corrente[1]
                if(parola_corrente == parola_corrente_iniziale):
                    lista_features_parola_corrente.append(coppia_corrente[0])

            print("parola_corrente_iniziale: ", parola_corrente_iniziale)
            print("lista_features_parola_corrente: ", lista_features_parola_corrente)
            print("")
            lista_parole_features.append(lista_features_parola_corrente) #aggiungo la lista_features_parola_corrente alla lista_parole_features finale.
            parole_gia_considerate.append(parola_corrente_iniziale)

    print("")
    print("")
    print("lista_parole_features:")
    print(lista_parole_features)
    print("")
    print("")
    ###########################################################################################################################################

    ###########################################################################################################################################
    # - A questo punto POSSO CREARE LA MATRICE DI ADIACENZA:
    file = open(path_matrice_adiacenza, "w", encoding="utf-8") #apro il file

    # - Per prima cosa aggiungo le features al file:###################
    features_matrice = ""
    for feature in features:
        features_matrice += ","
        features_matrice = features_matrice + feature
    file.write(features_matrice + "\n")
    ###########################################################################################################################################

    ####################################################################################################################
    # - Dopodichè creo le righe del file (ovvero della matrice di adiacenza):
    for lista_feature_parola_corrente in lista_parole_features:
        parola_corrente = lista_feature_parola_corrente[0]
        features_da_marcare_per_parola_corrente = []
        for i in range(1, len(lista_feature_parola_corrente)):
            features_da_marcare_per_parola_corrente.append(lista_feature_parola_corrente[i])
        print("parola_corrente:", parola_corrente)

        #- Adesso elimino i duplicati, questo perchè a volte potrebbero capitare casi come ad es. questo:
        # parola_corrente: football
        # features_da_marcare_per_parola_corrente:
        # ['compound', 'compound']
        # Poichè in questo caso la features 'compound' compare due volte per la parola football allora devo per forza essere sicuro di aver eliminato eventuali duplicati:
        features_da_marcare_per_parola_corrente = eliminazione_duplicati(features_da_marcare_per_parola_corrente)
        print("features_da_marcare_per_parola_corrente SENZA eventuali DUPLICATI:")
        print(features_da_marcare_per_parola_corrente)
        print("")
        ################################################################################

        ################################################################################
        #Creo una nuova riga nella matrice di adiacenza per la parola_corrente:
        riga = parola_corrente #il primo elemento di ogni riga sarà sempre il concetto, in questo codice per me ogni concetto è una parola della frase di input (senza considerare le stop words).
        for feature_corrente in features:
            if(feature_corrente in features_da_marcare_per_parola_corrente):
                # allora vuol dire che devo inserire una "X" per la parola corrente in corrispondenza della feature_corrente:
                riga += ",X"
            else:
                riga += ","  # altrimenti non inserisco nulla perchè vuol dire che per la parola_corrente (ovvero il concetto corrente) il valore di quella feature sarà 0.

        file.write(riga + "\n")
        ################################################################################

    ####################################################################################################################

    file.close() #chiudo il file.



if __name__ == '__main__':

    os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
    nlp = spacy.load("en_core_web_sm")
    stop_words = stopwords.words("english")
    stop_words.append('.')
    stop_words.append(',')
    stop_words.append(';')
    stop_words.append(':')
    stop_words.append('-')
    stop_words.append('(')
    stop_words.append(')')
    stop_words.append('"')
    stop_words.append('\n')

    # - Prendo una frase casuale:
    frase = get_frase_casuale("Risorse FCA\\Frasi corpus\\frasi")

    # - Ottengo il parser a dipendenze della frase:
    parser_frase = get_parser_a_dipendenze(frase)

    # - Chiamo la funzione sottostante che mi restituirà una lista di liste in cui ogni lista interna sarà una coppia formata da [nome_dipendenza,parola].
    lista_di_coppie_nome_dipendenza_parola = get_lista_coppie_dipendenza_parola(parser_frase)
    print("lista_di_coppie_nome_dipendenza_parola:")
    print(lista_di_coppie_nome_dipendenza_parola)
    print("")
    print("")

    # - A questo punto posso usare la lista di liste ottenuta sopra, per creare la matrice di adiacenza che salverò in matrice_adiacenza.csv:
    creazione_matrice_adiacenza(lista_di_coppie_nome_dipendenza_parola, "Risorse FCA\\matrice_di_adiacenza.csv")


    # - Infine applico la FCA alla matrice di adiacenza generata pocanzi:
    matrice_adiacenza = get_matrice_adiacenza("Risorse FCA\\matrice_di_adiacenza.csv")
    print("matrice_adiacenza:")
    print(matrice_adiacenza)
    print("")
    fca = matrice_adiacenza.lattice.graphviz(directory="./Risorse FCA/Risultati", view=True, filename="lattice")
    #print("Contesto formale:")
    #print(fca)