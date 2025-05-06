from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
from scipy import spatial
from nltk.corpus import wordnet as wn


#IN QUESTO CODICE QUELLO CHE FARO' SARA' QUESTO:
# 1) PRENDERO' OGNI LEMMA DI OGNI DOCUMENTO E LO MAPPERO' SU WN DA CUI OTTERRO' UNO O PIU' SYNSETS ASSOCIATI A QUEL LEMMA.
# 2) QUALORA IL NUMERO DEI SYNSETS OTTENUTI PER UN CERTO LEMMA FOSSE MAGGIORE DI 1 ALLORA DEVO ESEGUIRE LA DISAMBIGUAZIONE USANDO L'ALGORITMO DI LESK.


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


def ComputeOverlap(signature, context):
    lista_esempi = signature[0]
    glossa = signature[1]
    #print("lista_esempi: ", lista_esempi)
    overlap = 0
    if(lista_esempi != []):
        for esempio in lista_esempi:
            lista_parole_esempio = esempio.split(" ")
            #print("lista_parole_esempio: ", lista_parole_esempio)
            for parola_esempio in lista_parole_esempio:
                for parola_context in context:
                    if(parola_esempio == parola_context):
                        #print("parola_esempio: ", parola_esempio)
                        #print("parola_context: ", parola_context)
                        overlap += 1

    lista_parole_glossa = glossa.split(" ")
    #print("lista_parole_glossa: ", lista_parole_glossa)
    for parola_glossa in lista_parole_glossa:
        for parola_context in context:
            if (parola_glossa == parola_context):
                #print("parola_glossa: ", parola_glossa)
                #print("parola_context: ", parola_context)
                overlap += 1

    return overlap


def The_Lesk_Algorithm(word, sentence, tutti_i_sensi_della_parola_da_disambiguare):
    #print("word DENTRO LESK: ", word)
    #print("sentence DENTRO LESK: ", sentence)
    #tutti_i_sensi_della_parola_di_input = wn.synsets(word)
    #print("tutti_i_sensi_della_parola_di_input: ", tutti_i_sensi_della_parola_da_disambiguare)
    #best_sense = wn.synsets(word)[0] #inizilizzo best_sense con il senso più frequente.
    best_sense = tutti_i_sensi_della_parola_da_disambiguare[0]

    # print("best_sense iniziale: ", best_sense)
    # print("")
    # print("")

    max_overlap = 0
    context = sentence #inizializzo il contesto con tutte le parole della frase (context è una lista di parole)

    for senso in tutti_i_sensi_della_parola_da_disambiguare:
        #print("senso corrente: ", senso)
        lista_esempi = senso.examples() #è una lista di frasi (può anche non essercene neanche una di frase e quindi sarà [])
        #print("lista_esempi: ", lista_esempi)
        glossa = senso.definition() #la glossa è una stringa e non sarà mai vuota.
        #print("glossa: ", glossa)
        signature = []
        signature.append(lista_esempi)
        signature.append(glossa)
        #print("context: ", context)
        #print("signature: ", signature)
        overlap = ComputeOverlap(signature, context)
        #print("overlap: ", overlap)

        if(overlap > max_overlap):
            max_overlap = overlap
            best_sense = senso
        #print("")
        #print("")


    return best_sense



print("len(lista_di_tutti_i_documenti_di_TRAINING_in_inglese): ", len(lista_di_tutti_i_documenti_di_TRAINING_in_inglese))
print("len(lista_di_tutti_i_documenti_di_TEST_in_inglese): ", len(lista_di_tutti_i_documenti_di_TEST_in_inglese))
print(lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0])


#Mappo prima i lemmi dei documenti di training:
for indice_documento in range(0, len(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)):

    print("indice documento considerato: ", indice_documento)
    #if(lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] == lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0]): #da togliere

    # print("")
    # print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento]: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento])
    # print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0]: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0])
    # print("")

    #print(documento_training)
    # 1) PRENDERO' OGNI LEMMA DI OGNI DOCUMENTO E LO MAPPERO' SU WN DA CUI OTTERRO' UNO O PIU' SYNSETS ASSOCIATI A QUEL LEMMA.
    documento_training_in_lista_di_lemmi = lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento].split(" ")
    #print("documento_training_in_lista_di_lemmi: ", documento_training_in_lista_di_lemmi)
    if(documento_training_in_lista_di_lemmi != ['']):

        indice_lemma = 0
        for lemma in documento_training_in_lista_di_lemmi:
            # print("lemma: ", lemma)
            # print("indice lemma: ", indice_lemma)
            # print("len(lista_di_tutti_i_documenti_di_TRAINING_in_inglese): ", len(documento_training_in_lista_di_lemmi))

            sentence = []
            if(indice_lemma == 0): #se il lemma corrente è il primo del documento allora per disambiguarlo considero lui stesso e gli altri 4 lemmi che si trovano dopo di lui
                sentence.append(lemma)#aggiungo il lemma corrente alla sentence
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 4])

            elif(indice_lemma == 1):
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])

            elif(indice_lemma == 2):
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])

                if(indice_lemma < len(documento_training_in_lista_di_lemmi)-5):
                    sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])

            elif (indice_lemma == 3):

                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])

                if ((indice_lemma < len(documento_training_in_lista_di_lemmi) - 4)):
                    sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])

                if (indice_lemma < len(documento_training_in_lista_di_lemmi) - 5):
                    sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])


            elif(indice_lemma == (len(documento_training_in_lista_di_lemmi)-1)): #per l'ultimo lemma di ogni documento considero come contesto solo lui stesso e le 4 parole precedenti
                #ad esso.
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 4])


            elif (indice_lemma == (len(documento_training_in_lista_di_lemmi)-2)): #penultimo
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])


            elif (indice_lemma == (len(documento_training_in_lista_di_lemmi)-3)): #terzultimo
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])


            elif (indice_lemma == (len(documento_training_in_lista_di_lemmi)-4)): #quartultimo lemma del documento corrente
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])



            else: #altrimenti considero coem sentence: il lemma corrente, i quattro lemmi dopo di lui e i 4 lemmi prima di lui
                sentence.append(lemma)
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_training_in_lista_di_lemmi[indice_lemma + 4])



            tutti_i_sensi_della_parola_da_disambiguare = wn.synsets(lemma)
            #print("tutti_i_sensi_della_parola_da_disambiguare: ", tutti_i_sensi_della_parola_da_disambiguare)

            if(tutti_i_sensi_della_parola_da_disambiguare != []): #potrebbero esserci dei lemmi che non sono presenti su Wordnet.


                best_sense = The_Lesk_Algorithm(lemma, sentence, tutti_i_sensi_della_parola_da_disambiguare) #come contesto utilizzo tutto il documento di training
                #print("best_sense: ", best_sense)

                #adesso prendo tutti gli altri lemmi presenti nel best_sense (best_synset) del lemma corrente e li aggiungo al documento di training corrente.
                lista_lemmi_da_aggiungere_al_documento_di_training = best_sense.lemma_names()
                for lemma_da_aggiungere in lista_lemmi_da_aggiungere_al_documento_di_training:
                    if(lemma_da_aggiungere.lower() != lemma.lower()): #non aggiungo di nuovo il lemma che già c'era nel documento.
                        #print("lemma_da_aggiungere: ", lemma_da_aggiungere)
                        lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] =  lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] + " " + lemma_da_aggiungere    #in questo modo nel documento avrò tutti i lemmi che avevo già prima più quelli
                        #che si trovano nel synset migliore per il lemma corrente. Questa aggiunta in teoria dovrebbe aiutare l'algoritmo di Rocchio nel cercare i centroidi e quindi nel
                        #riuscire a classificare correttamente i documenti.
                #print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] DOPO: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento])
            indice_lemma += 1

    print("")
    print("")


print("")
print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0] Dopo:")
print(lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0])


#SERIALIZZO la lista di documenti di training che contiene anche i lemmi presi da WN:
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET CON MAX 4 PAROLE PRECEDENTI E 4 PAROLE SUCCESSIVE COME CONTESTO.txt', 'w') as f:
    str = json.dumps(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
    f.write(str)



#Dopodichè Mappo tutti i lemmi dei documenti di test:
for indice_documento in range(0, len(lista_di_tutti_i_documenti_di_TEST_in_inglese)):

    print("indice documento considerato: ", indice_documento)
    #if(lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] == lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0]): #da togliere

    # print("")
    # print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento]: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento])
    # print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0]: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[0])
    # print("")

    #print(documento_training)
    # 1) PRENDERO' OGNI LEMMA DI OGNI DOCUMENTO E LO MAPPERO' SU WN DA CUI OTTERRO' UNO O PIU' SYNSETS ASSOCIATI A QUEL LEMMA.
    documento_test_in_lista_di_lemmi = lista_di_tutti_i_documenti_di_TEST_in_inglese[indice_documento].split(" ")

    if (documento_test_in_lista_di_lemmi != ['']):
        indice_lemma = 0
        for lemma in documento_test_in_lista_di_lemmi:
            #print("lemma: ", lemma)
            sentence = []
            if (indice_lemma == 0):  # se il lemma corrente è il primo del documento allora per disambiguarlo considero lui stesso e gli altri 4 lemmi che si trovano dopo di lui
                sentence.append(lemma)  # aggiungo il lemma corrente alla sentence
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 4])

            elif (indice_lemma == 1):
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])

            elif (indice_lemma == 2):
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])

                if (indice_lemma < len(documento_test_in_lista_di_lemmi) - 5):
                    sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])

            elif (indice_lemma == 3):

                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])

                if ((indice_lemma < len(documento_test_in_lista_di_lemmi) - 4)):
                    sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])

                if (indice_lemma < len(documento_test_in_lista_di_lemmi) - 5):
                    sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])


            elif (indice_lemma == (len(documento_test_in_lista_di_lemmi) - 1)):
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 4])



            elif (indice_lemma == (len(documento_test_in_lista_di_lemmi) - 2)):  # penultimo
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])


            elif (indice_lemma == (len(documento_test_in_lista_di_lemmi) - 3)):  # terzultimo
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])


            elif (indice_lemma == (len(documento_test_in_lista_di_lemmi) - 4)):  # quartultimo lemma del documento corrente
                sentence.append(lemma)
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])



            else:  # altrimenti considero coem sentence: il lemma corrente, i quattro lemmi dopo di lui e i 4 lemmi prima di lui
                sentence.append(lemma)

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma - 4])

                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 1])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 2])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 3])
                sentence.append(documento_test_in_lista_di_lemmi[indice_lemma + 4])




            #if(lemma == "In"):
            tutti_i_sensi_della_parola_da_disambiguare = wn.synsets(lemma)
            #print("tutti_i_sensi_della_parola_da_disambiguare: ", tutti_i_sensi_della_parola_da_disambiguare)

            if(tutti_i_sensi_della_parola_da_disambiguare != []): #potrebbero esserci dei lemmi che non sono presenti su Wordnet.
                best_sense = The_Lesk_Algorithm(lemma, sentence, tutti_i_sensi_della_parola_da_disambiguare) #come contesto utilizzo tutto il documento di training
                #print("best_sense: ", best_sense)

                #adesso prendo tutti gli altri lemmi presenti nel best_sense (best_synset) del lemma corrente e li aggiungo al documento di training corrente.
                lista_lemmi_da_aggiungere_al_documento_di_training = best_sense.lemma_names()
                for lemma_da_aggiungere in lista_lemmi_da_aggiungere_al_documento_di_training:
                    if(lemma_da_aggiungere.lower() != lemma.lower()): #non aggiungo di nuovo il lemma che già c'era nel documento.
                        #print("lemma_da_aggiungere: ", lemma_da_aggiungere)
                        lista_di_tutti_i_documenti_di_TEST_in_inglese[indice_documento] = lista_di_tutti_i_documenti_di_TEST_in_inglese[indice_documento] + " " + lemma_da_aggiungere    #in questo modo nel documento avrò tutti i lemmi che avevo già prima più quelli
                        #che si trovano nel synset migliore per il lemma corrente. Questa aggiunta in teoria dovrebbe aiutare l'algoritmo di Rocchio nel cercare i centroidi e quindi nel
                        #riuscire a classificare correttamente i documenti.
                #print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento] DOPO: ", lista_di_tutti_i_documenti_di_TRAINING_in_inglese[indice_documento])

            indice_lemma += 1


    print("")
    print("")


print("")
print("lista_di_tutti_i_documenti_di_TEST_in_inglese[0] Dopo:")
print(lista_di_tutti_i_documenti_di_TEST_in_inglese[0])

#SERIALIZZO la lista di documenti di training che contiene anche i lemmi presi da WN:
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese_CON_AGGIUNTA_LEMMI_DI_WORDNET CON MAX 4 PAROLE PRECEDENTI E 4 PAROLE SUCCESSIVE COME CONTESTO.txt', 'w') as f:
     str = json.dumps(lista_di_tutti_i_documenti_di_TEST_in_inglese)
     f.write(str)


print("LE DUE LISTE SONO STATE SERIALIZZATE CORRETTAMENTE.")
######################################################################

#DOPO VAI AL CODICE "Algoritmo di Rocchio con scelta dei NEG più raffinata usando la sim del coseno (usando i synsets di wordnet sia per per il contesto con tutto il documento e sia per il contesto usando max 4 lemmi precedenti e successivi).py" ----->