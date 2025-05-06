import numpy as np
import importlib
import copy

def accuratezza(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test):

    # print("tags_assegnati_a_tutte_le_frasi_di_test: ")
    # print(tags_assegnati_a_tutte_le_frasi_di_test)
    # print("")
    # print("")

    # Calcolo il numero totale di parole presenti nel test set:##############################
    num_totale_parole_nel_test_set = 0
    num_frasi_considerate = 0
    for frase_test_set in frasi_test_set:
        #if (num_frasi_considerate < 3): #da togliere
        frase_test_splittata_per_singola_parola = frase_test_set.split(" ")
        frase_test_splittata_per_singola_parola[-1:] = []
        num_totale_parole_nel_test_set += len(frase_test_splittata_per_singola_parola)
        #num_frasi_considerate+=1
    #print("num_totale_parole_nel_test_set: ", num_totale_parole_nel_test_set)
    #########################################################################################


    # tags_assegnati_a_tutte_le_frasi_di_test = [['O', 'O', 'O', 'B-LOC', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
    #   'O', 'O', 'O', 'O', 'O', 'B-PER', 'O', 'I-PER', 'O'],#frase 1
    #  ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
    #   'O', 'O', 'O', 'O', 'O', 'O', 'B-ORG', 'O', 'O', 'O']] #frase 2

    # Adesso calcolo per ogni frase il numero di tags che sono stati predetti correttamente dall'algoritmo: ######################################################
    #num_frasi_considerate = 0
    num_tag_predetti_correttamente = 0
    for indice_frase_test in range(0, len(frasi_test_set)):
        #if (num_frasi_considerate < 3): #da togliere
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        tags_predetti_per_la_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
        # print("frase_test_splittata_per_singola_parola_con_tag:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("tags_predetti_per_la_frase_di_test_corrente:")
        # print(tags_predetti_per_la_frase_di_test_corrente)
        # print("")
        # print("")
        #con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            actual_tag = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
            predicted_tag = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente]
            # print("actual_tag: ", actual_tag)
            # print("predicted_tag: ", predicted_tag)
            # print("")
            if(actual_tag == predicted_tag):
                #vuol dire che l'algoritmo ha predetto il tag corretto:
                # print("actual_tag: ", actual_tag)
                # print("predicted_tag: ", predicted_tag)
                # print("")
                num_tag_predetti_correttamente+=1
        # print("")
        # print("")
        #num_frasi_considerate+=1
    ##############################################################################################################################################################

    return num_tag_predetti_correttamente/num_totale_parole_nel_test_set #restituisce l'accuratezza




#DA QUI PARTONO LE FUNZIONI CHE SERVONO PER CALCOLARE PRECISION E RECALL ##########################################################################################
def calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity(frasi_test_set, entity): #in entity NON CI SARA' MAI O
    #suppongo ad esempio entity = PER (persona) (entity nel nostro caso potrà essere PER,LOC,ORG o MISC)
    #quindi per trovare tutte le persone nel test set devo fare così:
    # - All'inizio metto B-entity in questo modo se entity = PER allora avrò B-PER:

    if(entity == "O"):
        return Exception("ERRORE: Non posso considerare come entity il tag O.")

    entity_B = "B-"+entity
    entity_IN = "I-" + entity
    num_entity_data_in_input = 0

    # 1) Prima devo individuare la parola che è taggata con B-PER
    # 2) Appena trovo questo tag posso incrementare il contatore che tiene conto del numero totale di entità PERSONA nel test set.

    # Inizio con il 1): ######################################################
    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity frase_test_splittata_per_singola_parola_con_tag]:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
            if(tag_reale == entity_B): #1) verifico che si tratti proprio dell'entità che mi è stata data in input.
                num_entity_data_in_input += 1 #qui eseguo il 2)


    # - Un altro caso in cui devo incrementare il contatore è quando c'è ad esempio un I-PER ISOLATO oppure quando c'è una serie di I-PER senza un B-PER iniziale (ad es: (I-PER, I-PER, I-PER)).
    # Per capire se questo I-PER è isolato nella frase devo fare questo:
    # 1) Prima devo individuare la parola che è taggata con I-PER
    # 2) Appena la trovo devo muovermi prima a sinistra rispetto al tag corrente e vedere se non c'è un B-PER o un I-PER:
            # Se c'è un B-PER o un I-PER allora non incremento nulla perchè vuol dire che l'I-PER che ho trovato all'inizio non è isolato e quindi
            # sicuramente ho già considerato quella entity in un altro conteggio.

            # Se invece non c'è prima nè un B-PER e nè un I-PER allora mi muovo a destra rispetto SEMPRE AL TAG CORRENTE INZIALE per vedere se c'è un I-PER:
                # Se c'è un I-PER allora vuol dire che posso incrementare il contatore perchè vuol dire che l'I-PER che ho trovato all'inizio è il primo di una serie. #pensa al caso (I-PER, I-PER, I-PER)
                # altrimenti posso comunque incrementare il contatore perchè vuol dire che ho trovato un I-PER completamente isolato.

                # i casi delle ultime due righe precedenti si fondono e quindi posso dire che:
                # Se invece non c'è prima nè un B-PER e nè un I-PER allora mi muovo a destra rispetto SEMPRE AL TAG CORRENTE INZIALE per vedere se c'è un I-PER:
                # Indipendentemente dal fatto che a destra ci sia o no un I-PER comunque devo incrementare il contatore.


    # Inizio con il 1) Prima devo individuare la parola che è taggata con I-PER: ######################################################
    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entityfrase_test_splittata_per_singola_parola_con_tag]:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
            if (tag_reale == entity_IN):  # 2) Appena la trovo devo muovermi prima a sinistra rispetto al tag corrente e vedere se non c'è un B-PER o un I-PER:

                if(indice_parola_frase_test_corrente > 0): #verifico di non essere all'inizio della frase
                    tag_reale_precedente = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente-1].split("\t")[1]
                    # Se c'è un B-PER o un I-PER allora non incremento nulla perchè vuol dire che l'I-PER che ho trovato all'inizio non è isolato e quindi
                    # sicuramente ho già considerato quella entity in un altro conteggio.
                    # Quindi considero direttamente il caso in cui il tag precedente sia diverso da B-PER e I-PER:
                    if((tag_reale_precedente != entity_B) and (tag_reale_precedente != entity_IN)):
                        # Se invece non c'è prima nè un B-PER e nè un I-PER allora mi muovo a destra rispetto SEMPRE AL TAG CORRENTE INZIALE per vedere se c'è un I-PER:
                        # Indipendentemente dal fatto che a destra ci sia o no un I-PER comunque devo incrementare il contatore.
                        # Quindi in questo caso sono sicuro di dover incrementare il contatore:
                        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entityfrase_test_splittata_per_singola_parola_con_tag]:")
                        # print(frase_test_splittata_per_singola_parola_con_tag)
                        # print("ISOLATOOOOOOOO")
                        num_entity_data_in_input += 1

                else:
                    num_entity_data_in_input += 1  #posso incrementare subito il contatore perchè ho trovato un I-PER all'inizio di una frase.

    #print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity - num_entity_data_in_input]: ", num_entity_data_in_input)

    return num_entity_data_in_input



def pulizia_tags_predetti_in_modo_non_corretto(entity_B, entity_IN, tags_assegnati_a_tutte_le_frasi_di_test): #funzione che mi serve per eliminare tutte le predizioni fatte in maniera scorretta dal modello
    #scorro tutti i tags predetti dal modello:
    for lista_tags_predetti_per_la_frase_corrente in tags_assegnati_a_tutte_le_frasi_di_test:
        #print("lista_tags_predetti_per_la_frase_corrente: ", lista_tags_predetti_per_la_frase_corrente)
        #se c'è una sequenza isolata ad esempio di I-LOC senza un B-LOC avanti allora considero come se il modello avesse predetto O per tutta la sequenza di I-LOC isolati.
        for indice_tag in range(0, len(lista_tags_predetti_per_la_frase_corrente)):

            if((lista_tags_predetti_per_la_frase_corrente[indice_tag] == entity_IN) and (lista_tags_predetti_per_la_frase_corrente[indice_tag-1] != entity_IN)
                and (indice_tag != 0)): #l'ultima condizione in and mi serve per essere sicuro di non star considerando proprio il primissimo tag della prima parola della
                #frase.

                #se entro qui vuol dire che sto considerando il primo I-LOC della sequenza (può darsi che dopo di lui ci siano altri I-LOC)

                #Adesso quindi devo verificare che prima di lui ci sia per forza un B-LOC altrimenti devo assegnare O all'I-LOC corrente e a tutti quelli
                #che ci sono eventualmente dopo di lui:
                if((lista_tags_predetti_per_la_frase_corrente[indice_tag-1] != entity_B)):
                    #devo assegnare O all'I-LOC corrente e a tutti quelli che ci sono eventualmente dopo di lui:
                    indice_tag_del_while = indice_tag
                    while((indice_tag_del_while < len(lista_tags_predetti_per_la_frase_corrente)) and #la prima condizione mi serve per essere sicuro di non non superare l'ultimo elemento della lista
                          (lista_tags_predetti_per_la_frase_corrente[indice_tag_del_while] == entity_IN)):
                        lista_tags_predetti_per_la_frase_corrente[indice_tag_del_while] = "O" #gli assegno O
                        indice_tag_del_while += 1

            elif((indice_tag == 0) and lista_tags_predetti_per_la_frase_corrente[indice_tag] == entity_IN): #qui gestisco il caso in cui c'è ad esempio I-LOC I-LOC ... già sulla prima parola della frase di test
                # devo assegnare O all'I-LOC corrente e a tutti quelli che ci sono eventualmente dopo di lui:
                indice_tag_del_while = indice_tag #in questo caso indice_tag = 0 sicuro.
                while ((indice_tag_del_while < len(lista_tags_predetti_per_la_frase_corrente)) and  # la prima condizione mi serve per essere sicuro di non non superare l'ultimo elemento della lista
                       (lista_tags_predetti_per_la_frase_corrente[indice_tag_del_while] == entity_IN)):
                    lista_tags_predetti_per_la_frase_corrente[indice_tag_del_while] = "O"  # gli assegno O
                    indice_tag_del_while += 1

    # print("")
    # print("")
    # print("tags_assegnati_a_tutte_le_frasi_di_test dopo pulizia tags: ")
    # print(tags_assegnati_a_tutte_le_frasi_di_test)
    # print("")
    # print("")

    return tags_assegnati_a_tutte_le_frasi_di_test



def true_positive_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test_input, entity):
    # suppongo ad esempio entity = PER (persona) (entity nel nostro caso potrà essere PER,LOC,ORG o MISC)
    if (entity == "O"):
        return Exception("ERRORE: Non posso considerare come entity il tag O.")

    entity_B = "B-" + entity
    entity_IN = "I-" + entity
    contatore_true_positive_entiry_corrente = 0

    tags_assegnati_a_tutte_le_frasi_di_test_new = copy.deepcopy(tags_assegnati_a_tutte_le_frasi_di_test_input)
    tags_assegnati_a_tutte_le_frasi_di_test = pulizia_tags_predetti_in_modo_non_corretto(entity_B, entity_IN,tags_assegnati_a_tutte_le_frasi_di_test_new)

    # 1) Mi posiziono sulla frase corrente e scorro tutti i tag reali.
    # 2) Prima devo individuare la parola che è taggata con B-PER.
        # 3) Appena trovo questo tag controllo subito se il modello ha predetto correttamente in quella posizione B-PER oppure direttamente I-PER perchè magari nella frase non c'era
             #prima un B-PER ma c'era direttamente I-PER:
                #se non è così:
                    # allora già posso dire che non è riuscito ad identificare quella persona e quindi NON incremento il contatore true_positive e
                    # vado avanti fino a quando trovo di nuovo un B-PER e ricomincio.
                #se è così:
                    #allora vado avanti e se c'è ad esempio subito dopo il tag I-PER allora controllo che il modello abbia predetto I-PER in quella posizione,
                    #perchè se non l'ha fatto allora vuol dire che non è riuscito ad identificare quella persona completamente e quindi comunque ha sbagliato.
                    #continuo a fare quello detto nelle due righe di sopra fino a quando ci sono ancora I-PER, appena c'è un tag diverso da I-PER (può essere
                    #anche un nuovo B-PER) esco da questi controlli e continuo il ciclo principale che è startato al passo 2).


    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO true_positive_entity] frase_test_splittata_per_singola_parola_con_tag:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("[DENTRO true_positive_entity] len(frase_test_splittata_per_singola_parola_con_tag): ",len(frase_test_splittata_per_singola_parola_con_tag))
        #print(frase_test_splittata_per_singola_parola_con_tag[14])
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)): #1)
            #print("indice_parola_frase_test_corrente: ", indice_parola_frase_test_corrente)


            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
            #print("tag_reale: ", tag_reale)
            if( (tag_reale == entity_B) or (tag_reale == entity_IN) ): #2) Prima devo individuare la parola che è taggata con B-PER o con direttamente I-PER.
                tags_predetti_per_la_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
                tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente]
                #print("tag_predetto in if( (tag_reale == entity_B) or (tag_reale == entity_IN) ): ", tag_predetto)
                #print("")

                if(tag_reale == entity_IN):
                    #devo verificare però che sia un I-entity isolato altrimenti vuol dire che l'ho già considerato nei passi precedenti e quindi rischierei di contare più true positive
                    # del previsto:
                    if(indice_parola_frase_test_corrente > 0):#verifico che non mi trovi sul primo tag della frase perchè altrimenti non posso muovermi all'indietro.
                        tag_reale_precedente = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente-1].split("\t")[1]
                        tag_predetto_precedente = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente-1]
                        #print("tag_reale_precedente in indice_parola_frase_test_corrente > 0: ", tag_reale_precedente)

                        if( ( (tag_reale_precedente == entity_IN) or (tag_reale_precedente == entity_B) ) or ((tag_predetto_precedente == entity_IN) or (tag_predetto_precedente == entity_B)) ): #prima potrebbe esserci stato un entity_IN o un entity_B in entrambi i casi
                            #sicuramente avrò già considerato anche l'entity_IN corrente. Per quanto riguarda le altre due condizioni in or ((tag_predetto_precedente == entity_IN) or (tag_predetto_precedente == entity_B)),
                            #queste servono per assicurarmi che la predizione precedente del modello sia stata entity_IN o entity_B perchè se così fosse allora comunque sicuramente avrò già calcolato correttamente una sola volta il true positive
                            #prima qualora il modello non avesse sbagliato.

                            # print("tag_reale_precedente: ", tag_reale_precedente)
                            # print("tag_predetto_precedente: ", tag_predetto_precedente)
                            #print("dentro tag_reale_precedente == entity_IN")
                            continue #vado all'iterata successiva del ciclo for corrente perchè vuol dire che l'IN-entity corrente l'ho già considerato sicuramente nei passi precedenti.
                        #altrimenti non faccio nulla perchè vuol dire che è un entity_IN isolato.


                errore_successivo = False
                if(tag_predetto == tag_reale):#3) Appena trovo questo tag controllo subito se il modello ha predetto correttamente in quella posizione B-PER o direttamente I-PER.
                    # se è così:
                    #allora vado avanti e se c'è ad esempio subito dopo il tag I-PER allora controllo che il modello abbia predetto I-PER in quella posizione,
                    #perchè se non l'ha fatto allora vuol dire che non è riuscito ad identificare quella persona completamente e quindi comunque ha sbagliato.

                    indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity = indice_parola_frase_test_corrente + 1
                    if(indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity <= (len(frase_test_splittata_per_singola_parola_con_tag)-1)): #controllo se il tag corrente è al massimo l'ultimo della frase e quindi verifico
                        #che non sono uscito fuori dalla lista.

                        tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity].split("\t")[1]

                        #errore_successivo = False
                        while(tag_reale == entity_IN): #continuo a fare quello detto nelle due righe di sopra fino a quando ci sono ancora I-PER
                            tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity]
                            # print("tag_reale nel while: ", tag_reale)
                            # print("tag_predetto nel while: ", tag_predetto)
                            #print("")

                            if(tag_predetto != tag_reale):
                                #print("entrato in tag_predetto != tag_reale.")
                                errore_successivo = True
                                break #esco dal while perchè il modello ha sbagliato un I-entity e quindi vuol dire che non ha individuato l'entità fino alla fine

                            if(indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity < (len(frase_test_splittata_per_singola_parola_con_tag)-2)):
                                #print("entrato in indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity < (len(frase_test_splittata_per_singola_parola_con_tag)-2).")
                                indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity += 1 #adesso devo incrementare questo indice e non più quello iniziale che era indice_parola_frase_test_corrente
                                tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity].split("\t")[1]
                            else:
                                #print("entrato in break.")
                                break #vuol dire che sono arrivato all'ultima parola dalla frase e quindi posso uscire dal while.

                        #gestisco ora il caso in cui ho real: B-ORG I-LOC e pred: B-ORG I-ORG (il modello ha sbagliato perchè non è riscito a trovare l'unica vera entità ORG che era composta
                        # solo da B-ORG).
                        if(tag_reale != entity_IN):
                            #print("entrato in tag_reale != entity_IN")
                            #verifico che anche la predizione fatta dal modello non sia I-ORG
                            tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parole_successiva_a_quella_che_era_taggata_con_B_o_I_entity]
                            if(tag_predetto == entity_IN): #vuol dire che mi trovo nel caso in cui il modello ad esempio ha messo I-ORG ma in realtà lì il tag reale era un altro qualsiasi
                                #(nell'esempio di sopra era I-LOC)
                                #print("entrato in tag_predetto == entity_IN")
                                errore_successivo = True
                        ######################################################################################################################################################################


                    if(errore_successivo == False):
                        #print("entrato in errore_successivo == False")
                        contatore_true_positive_entiry_corrente += 1 #aggiorno il contatore dei true positive perchè vuol dire che l'entità è stata riconosciuta
                        #tutta correttamente.

                    # print("")
                    # print("")

    # print("")
    # print("")
    # print("contatore_true_positive_entiry_corrente: ", contatore_true_positive_entiry_corrente)
    # print("")


    return contatore_true_positive_entiry_corrente



def false_positive_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity):


    # calcolo i false positive per l'entity passata in input.
    # Per farlo seguo questi passi:
    # suppongo che l'entità sia PER.
    # 1) Mi posiziono sulla frase corrente e scorro tutti i tag PREDETTI per questa frase.

    # 1.1) Se il modello ha predetto B-PER allora mi posiziono in corrispondenza di quella parola nel test set e prendo il suo tag:

    # 2) Se il modello ha predetto B-PER allora mi posiziono in corrispondenza di quella parola nel test set e prendo il suo tag:
            #Se è anch'esso B-PER allora non faccio nulla.

            #caso 2.1) - Altrimenti se non è B-PER ma è un qualsiasi altro tag TRANNE I-PER (LOC,ORG,MISC,O - chiaramente per i primi 3 vale sia B che I) vuol dire che il modello
            # ha sbagliato ed ha commesso un errore di FP e quindi incremento il contatore.

                #DOPODICHE' se si è verificato il caso 2.1) faccio questo:
                #Mi posiziono subito dopo il B-PER e se ci sono I-PER li skippo tutti perhè ormai ho già considerato il false positive sull'entita completa e non bisogna incrementare
                #il contatore anche sui successivi I-PER qualora fossero stati sbagliati A MENO CHE i successivi I-PER predetti nella realtà erano dei tags che appartenevano ad un'entità
                #diversa dall'ultima entità considerata e sulla quale ho già calcolato il false positive.


    # 3) Se il modello ha predetto I-PER allora mi posiziono in corrispondenza di quella parola nel test set e prendo il suo tag:
            # Se è anch'esso I-PER allora non faccio nulla.
            # caso 3.1) Altrimenti se non è I-PER ma è un qualsiasi altro tag TRANNE B-PER (LOC,ORG,MISC,O - chiaramente per i primi 3 vale sia B che I) vuol dire che il modello
            # ha sbagliato ed ha commesso un errore di FP e quindi incremento il contatore.

                #DOPODICHE' se si è verificato il caso 3.1) faccio questo:
                #Mi posiziono subito dopo l' I-PER e se ci sono altri I-PER li skippo tutti perhè ormai ho già considerato il false positive sull'entita completa e non bisogna incrementare
                #il contatore anche sui successivi I-PER qualora fossero stati sbagliati A MENO CHE i successivi I-PER predetti nella realtà erano dei tags che appartenevano ad un'entità
                #diversa dall'ultima entità considerata e sulla quale ho già calcolato il false positive.


    entity_B = "B-" + entity
    entity_IN = "I-" + entity
    contatore_false_positive_entity_corrente = 0

    tags_assegnati_a_tutte_le_frasi_di_test_new = copy.deepcopy(tags_assegnati_a_tutte_le_frasi_di_test)
    tags_assegnati_a_tutte_le_frasi_di_test = pulizia_tags_predetti_in_modo_non_corretto(entity_B, entity_IN, tags_assegnati_a_tutte_le_frasi_di_test_new)

    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO false_positive_entity] frase_test_splittata_per_singola_parola_con_tag:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("[DENTRO false_positive_entity] len(frase_test_splittata_per_singola_parola_con_tag): ",len(frase_test_splittata_per_singola_parola_con_tag))
        #print(frase_test_splittata_per_singola_parola_con_tag[14])
        # print("")
        # print("")
        # con il ciclo di sotto prendo il tag predetto dall'algoritmo:
        #for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)): #1)
        indice_parola_frase_test_corrente = 0
        while (indice_parola_frase_test_corrente < len(frase_test_splittata_per_singola_parola_con_tag)): #1)

            tags_predetti_per_la_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
            #print("[DENTRO false_positive_entity] tags_predetti_per_la_frase_di_test_corrente: ", tags_predetti_per_la_frase_di_test_corrente)
            tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente]

            # y_true = [["B-LOC", "B-LOC", "B-LOC", "B-PER", "I-PER", "B-ORG", "I-PER"]]
            # y_pred = [["B-LOC", "I-LOC", "B-LOC", "B-LOC", "I-LOC", "I-LOC", "I-LOC"]]

            if(tag_predetto == entity_B):# 2) Se il modello ha predetto B-PER allora mi posiziono in corrispondenza di quella parola nel test set e prendo il suo tag:
                tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]


                if((tag_reale != entity_B) and (tag_reale != entity_IN)): #Altrimenti se non è B-PER ma è un qualsiasi altro tag  TRANNE I-PER
                    # (LOC,ORG,MISC,O - chiaramente per i primi 3 vale sia B che I) vuol dire che il modello
                    # ha sbagliato ed ha commesso un errore di FP e quindi incremento il contatore.

                #if (tag_reale != entity_B):

                    #sono nel #caso 2.1):
                    # print("tag_predetto: ", tag_predetto)
                    # print("tag_reale: ", tag_reale)
                    contatore_false_positive_entity_corrente += 1
                    ultima_entity_considerata = tag_reale[-3:]
                    #print("dopo incremento contatore_false_positive_entity_corrente (DENTRO if((tag_reale != entity_B) and (tag_reale != entity_IN))) : ", contatore_false_positive_entity_corrente)

                    # DOPODICHE' se si è verificato il caso 2.1) faccio questo:
                    # Mi posiziono subito dopo il B-PER e se ci sono I-PER li skippo tutti perhè ormai ho già considerato il false positive sull'entita completa e non bisogna incrementare
                    # il contatore anche sui successivi I-PER qualora fossero stati sbagliati.
                    #indice_parola_frase_test_corrente_temp = 0 #non è quello del ciclo while
                    indice_parola_frase_test_corrente_temp = indice_parola_frase_test_corrente + 1 #mi sposto verso destra

                    if(indice_parola_frase_test_corrente_temp < (len(frase_test_splittata_per_singola_parola_con_tag))): #controllo di non aver superato l'ultimo elemento della lista
                        tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente_temp]

                        while(tag_predetto == entity_IN):
                            #print("tag_predetto che salto: ", tag_predetto)
                            indice_parola_frase_test_corrente = indice_parola_frase_test_corrente_temp #praticamente mi metto nella posizione in cui c'è ad esempio il primo I-PER
                            #che è immediatamente successivo al B-PER che avevo trovato prima (oppure all'I-PER trovato prima).
                            #E così via vado avanti fino a quando non mi trovo sull'ultimo I-PER:


                            #AGGIUNTO ORA
                            # A MENO CHE i successivi I-PER predetti nella realtà erano dei tags che appartenevano ad un'entità ####################
                            # diversa dall'ultima entità considerata e sulla quale ho già calcolato il false positive:
                            tag_reale_corrente = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
                            if (tag_reale_corrente[-3:] != ultima_entity_considerata):
                                contatore_false_positive_entity_corrente += 1
                                ultima_entity_considerata = tag_reale_corrente[-3:]  # aggiorno l'ultima entity considerata
                            #######################################################################################################################


                            indice_parola_frase_test_corrente_temp += 1 #mi sposto di nuovo verso destra e...
                            if(indice_parola_frase_test_corrente_temp <= (len(frase_test_splittata_per_singola_parola_con_tag)-1)): #controllo che non sono uscito fuori la lista
                                tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente_temp] #... e prendo il tag successivo perchè potrebbe esserci ancora
                                #un I-PER.
                            else:
                                break #esco dal while perchè sono arrivato alla fine della lista.

                            #All'uscita del while ho bisogno ancora di spostarmi verso destra per essere sicuro di non star considerando più I-PER ma questo spostamento viene fatto in
                            #automatico da indice_parola_frase_test_corrente += 1 #incremento l'indice del while di 1 che è presente come ultima istruzione del ciclo while.


            # y_true = [["B-LOC", "B-LOC", "B-LOC", "B-PER", "I-PER", "B-ORG", "I-PER"]]
            # y_pred = [["B-LOC", "I-LOC", "B-LOC", "B-LOC", "I-LOC", "I-LOC", "I-LOC"]]

            elif(tag_predetto == entity_IN): #Se il modello ha predetto I-PER allora mi posiziono in corrispondenza di quella parola nel test set e prendo il suo tag:

                # #prima di fare qualsiasi cosa devo essere certo che l'entity_IN sia un caso isolato e che non sia già stato considerato nei passi precedenti:
                # if(indice_parola_frase_test_corrente > 0): #mi assicuro che non sono all'inzio
                #
                #     tag_predetto_precedente = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente-1]
                #     print("tag_predetto_precedente prima: ", tag_predetto_precedente)
                #     if ((tag_predetto_precedente == entity_IN) or (tag_predetto_precedente == entity_B)):  # prima potrebbe esserci stato un entity_IN o un entity_B in entrambi i casi
                #         # sicuramente avrò già considerato anche l'entity_IN corrente.
                #         print("tag_predetto_precedente: ", tag_predetto_precedente)
                #         # print("dentro tag_reale_precedente == entity_IN")
                #         #indice_parola_frase_test_corrente += 1  # incremento l'indice del while di 1.
                #         break  # vado all'iterata successiva del ciclo while corrente perchè vuol dire che l'IN-entity corrente l'ho già considerato sicuramente nei passi precedenti.
                #
                #     # altrimenti non faccio nulla perchè vuol dire che è un entity_IN isolato.

                #############################################################################################################################################


                tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]


                if((tag_reale != entity_IN) and (tag_reale != entity_B)): # Altrimenti se non è I-PER ma è un qualsiasi altro tag TRANNE B-PER
                    # (LOC,ORG,MISC,O - chiaramente per i primi 3 vale sia B che I) vuol dire che il modello
                    # ha sbagliato ed ha commesso un errore di FP e quindi incremento il contatore.
                    # print("tag_predetto: ", tag_predetto)
                    # print("tag_reale: ", tag_reale)


                    contatore_false_positive_entity_corrente += 1
                    ultima_entity_considerata = tag_reale[-3:]
                    #print("dopo incremento contatore_false_positive_entity_corrente (DENTRO if((tag_reale != entity_IN) and (tag_reale != entity_B)): ", contatore_false_positive_entity_corrente)

                    # DOPODICHE' se si è verificato il caso 3.1) faccio questo:
                    # Mi posiziono subito dopo l' I-PER e se ci sono altri I-PER li skippo tutti perhè ormai ho già considerato il false positive
                    # sull'entita completa e non bisogna incrementare il contatore anche sui successivi I-PER qualora fossero stati sbagliati.
                    #indice_parola_frase_test_corrente_temp = 0  # non è quello del ciclo while
                    indice_parola_frase_test_corrente_temp = indice_parola_frase_test_corrente + 1  # mi sposto verso destra

                    if (indice_parola_frase_test_corrente_temp < (len( frase_test_splittata_per_singola_parola_con_tag))):  # controllo di non essere arrivato all'ultimo elemento della lista
                        tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente_temp]

                        while (tag_predetto == entity_IN):
                            indice_parola_frase_test_corrente = indice_parola_frase_test_corrente_temp  # praticamente mi metto nella posizione in cui c'è ad esempio il primo I-PER
                            # che è immediatamente successivo all'I-PER che avevo trovato prima.
                            # E così via vado avanti fino a quando non mi trovo sull'ultimo I-PER:


                            # A MENO CHE i successivi I-PER predetti nella realtà erano dei tags che appartenevano ad un'entità      ####################
                            # diversa dall'ultima entità considerata e sulla quale ho già calcolato il false positive:
                            tag_reale_corrente = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
                            if (tag_reale_corrente[-3:] != ultima_entity_considerata):
                                contatore_false_positive_entity_corrente += 1
                                ultima_entity_considerata = tag_reale_corrente[-3:]  # aggiorno l'ultima entity considerata
                            ##############################################################################################################################



                            indice_parola_frase_test_corrente_temp += 1  # mi sposto di nuovo verso destra e...

                            if (indice_parola_frase_test_corrente_temp <= (len(frase_test_splittata_per_singola_parola_con_tag)-1)):  # controllo che non sono uscito fuori la lista
                                tag_predetto = tags_predetti_per_la_frase_di_test_corrente[indice_parola_frase_test_corrente_temp]  # ... e prendo il tag successivo perchè potrebbe esserci ancora
                                # un I-PER.
                            else:
                                break  # esco dal while perchè sono arrivato alla fine della lista.


                            # All'uscita del while ho bisogno ancora di spostarmi verso destra per essere sicuro di non star considerando più I-PER ma questo spostamento viene fatto in
                            # automatico da indice_parola_frase_test_corrente += 1 #incremento l'indice del while di 1 che è presente come ultima istruzione del ciclo while.



            indice_parola_frase_test_corrente += 1 #incremento l'indice del while di 1.


    # print("contatore_false_positive_entity_corrente: ", contatore_false_positive_entity_corrente)
    # print("")

    return contatore_false_positive_entity_corrente



#Questa funzione mi dice qual'è la percentuale di accuratezza sulla singola entità passata in input.
def accuratezza_B_I_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity):

    if (entity == "O"):

        num_O_tag_real = 0
        num_O_tag_pred = 0

        # 1) Prima devo individuare la parola che è taggata con O nel test set.
        # 2) Appena trovo questo tag posso incrementare il contatore che tiene conto del numero totale di O nel test set e se il modello ha predetto correttamente in quella posizione
        # il tag O, allora incremento anche num_O_tag_pred.

        # Inizio con il 1): ######################################################
        for indice_frase_test in range(0, len(frasi_test_set)):
            frase_test_corrente = frasi_test_set[indice_frase_test]
            frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
            frase_test_splittata_per_singola_parola_con_tag[
            -1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
            # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity frase_test_splittata_per_singola_parola_con_tag]:")
            # print(frase_test_splittata_per_singola_parola_con_tag)
            # print("")
            # print("")
            # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
            for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
                tag_reale = \
                frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
                if (tag_reale == "O"):  # 1) verifico che si tratti proprio del tag che mi è stato dato in input.
                    num_O_tag_real += 1  # qui eseguo il 2)
                    # print("tag_reale: ", tag_reale)

                    # e se il modello ha predetto correttamente quel tag B allora incremento anche num_O_tag_pred:
                    tag_predetti_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
                    # print("tag_predetto: ", tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente])
                    if (tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente] == "O"):
                        num_O_tag_pred += 1

        if (num_O_tag_real == 0):
            return -1

        acc_tag_O = num_O_tag_pred / num_O_tag_real
        return acc_tag_O



    #print("tags_assegnati_a_tutte_le_frasi_di_test IN accuratezza_B_I_entity: ",tags_assegnati_a_tutte_le_frasi_di_test)

    entity_B = "B-" + entity
    entity_IN = "I-" + entity

    num_B_entity_real = 0
    num_I_entity_real = 0
    num_B_entity_pred = 0  # tiene conto delle predizioni corrette farre per il B tag dell'entity data in input.
    num_I_entity_pred = 0

    # 1) Prima devo individuare la parola che è taggata con B-PER
    # 2) Appena trovo questo tag posso incrementare il contatore che tiene conto del numero totale di entity_B nel test set e se il modello ha predetto correttamente quell'entity_B
    # allora incremento anche num_B_entity_pred.

    # Inizio con il 1): ######################################################
    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity frase_test_splittata_per_singola_parola_con_tag]:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[
                1]
            if (tag_reale == entity_B):  # 1) verifico che si tratti proprio dell'entità che mi è stata data in input.
                num_B_entity_real += 1  # qui eseguo il 2)
                #print("tag_reale: ", tag_reale)

                # e se il modello ha predetto correttamente quell'entity_B allora incremento anche num_B_entity_pred:
                tag_predetti_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
                #print("tag_predetto: ", tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente])
                if (tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente] == entity_B):
                    num_B_entity_pred += 1

    # Adesso devo trovare invece il numero totale di parole a cui è stato assegnato il tag I-PER.
    # 1) Prima devo individuare la parola che è taggata con I-PER
    # 2) Appena trovo questo tag posso incrementare il contatore che tiene conto del numero totale di entity_IN nel test set.
    # Inizio con il 1): ######################################################
    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity frase_test_splittata_per_singola_parola_con_tag]:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]
            if (tag_reale == entity_IN):  # 1) verifico che si tratti proprio dell'entità che mi è stata data in input.
                num_I_entity_real += 1  # qui eseguo il 2)
                #print("tag_reale: ", tag_reale)
                # e se il modello ha predetto correttamente quell'entity_IN allora incremento anche num_IN_entity_pred:
                tag_predetti_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
                #print("tag_predetto: ", tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente])
                if (tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente] == entity_IN):
                    num_I_entity_pred += 1


    # print("num_B_entity_real: ", num_B_entity_real)
    # print("num_B_entity_pred: ", num_B_entity_pred)
    # print("")
    # print("num_I_entity_real: ", num_I_entity_real)
    # print("num_I_entity_pred: ", num_I_entity_pred)

    if ((num_B_entity_real == 0) or (num_I_entity_real == 0)):
        return -1


    accuratezza_B_entity = num_B_entity_pred / num_B_entity_real
    accuratezza_I_entity = num_I_entity_pred / num_I_entity_real
    accuratezza_B_I_entity = (num_B_entity_pred + num_I_entity_pred) / (num_B_entity_real + num_I_entity_real)

    return accuratezza_B_entity, accuratezza_I_entity, accuratezza_B_I_entity




def accuratezza_B_I_consecutivi(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity):

    if (entity == "O"):
        return Exception("ERRORE: Non posso considerare come entity il tag O.")

    #print("tags_assegnati_a_tutte_le_frasi_di_test IN accuratezza_B_I_entity: ", tags_assegnati_a_tutte_le_frasi_di_test)
    entity_B = "B-" + entity
    entity_IN = "I-" + entity
    num_B_I_entity_real = 0
    num_B_I_entity_predetti_correttamente = 0
    # 1) Prima devo individuare la parola che è taggata con B-PER.
    # 2) Appena trovo questo tag verifico che subito dopo ci sia un I-PER.
        # 3) Se avviene quello detto al punto 2) allora incremento il contatore dei B_I_PER.
            # 4) Se 2) e 3) sono rispettate allora controllo se il modello ha predetto nelle posizioni giuste il B-PER e I-PER:
                # se è così allora incremento di uno il num_B_I_entity_predetti_correttamente.
    # Inizio con il 1): ######################################################
    for indice_frase_test in range(0, len(frasi_test_set)):
        frase_test_corrente = frasi_test_set[indice_frase_test]
        frase_test_splittata_per_singola_parola_con_tag = frase_test_corrente.split(" ")
        frase_test_splittata_per_singola_parola_con_tag[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        # print("[DENTRO calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity frase_test_splittata_per_singola_parola_con_tag]:")
        # print(frase_test_splittata_per_singola_parola_con_tag)
        # print("")
        # print("")
        # con il ciclo di sotto prendo ogni tag reale di ogni parola della frase_test_corrente e lo confronto con il tag predetto dall'algoritmo:
        for indice_parola_frase_test_corrente in range(0, len(frase_test_splittata_per_singola_parola_con_tag)):
            tag_reale = frase_test_splittata_per_singola_parola_con_tag[indice_parola_frase_test_corrente].split("\t")[1]

            if (tag_reale == entity_B):  # 1) verifico che si tratti proprio del B-entity dell'entità che mi è stata data in input.
                #print("tag_reale: ", tag_reale)
                if(indice_parola_frase_test_corrente < (len(frase_test_splittata_per_singola_parola_con_tag)-1)):
                    #se è così allora vuol dire che sono sicuro che dopo c'è almeno un'altra parola

                    # 2) Appena trovo questo tag verifico che subito dopo ci sia un I-PER:
                    indice_parola_successiva_frase_test_corrente = indice_parola_frase_test_corrente + 1
                    tag_reale_successivo = frase_test_splittata_per_singola_parola_con_tag[indice_parola_successiva_frase_test_corrente].split("\t")[1]
                    if(tag_reale_successivo == entity_IN):
                        #print("tag_reale_successivo: ", tag_reale_successivo)
                        num_B_I_entity_real += 1  #3) Se avviene quello detto al punto 2) allora incremento il contatore dei B_I_PER.


                    #e se il modello ha predetto correttamente quell'entity_B allora incremento anche num_B_entity_pred:
                    tag_predetti_frase_di_test_corrente = tags_assegnati_a_tutte_le_frasi_di_test[indice_frase_test]
                    if((tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente] == entity_B) and
                        (tag_predetti_frase_di_test_corrente[indice_parola_successiva_frase_test_corrente] == entity_IN)):
                        #print("tag_predetto: ", tag_predetti_frase_di_test_corrente[indice_parola_frase_test_corrente])
                        #print("tag_successivo_predetto:", tag_predetti_frase_di_test_corrente[indice_parola_successiva_frase_test_corrente])
                        num_B_I_entity_predetti_correttamente += 1

    if (num_B_I_entity_real == 0):
        return -1

    accuratezza_B_I_consecutivi_entity = num_B_I_entity_predetti_correttamente/num_B_I_entity_real

    return accuratezza_B_I_consecutivi_entity





def recall(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity):
    #calcolo la recall del modello per l'entity fornita in input:
    numero_istanze_entity_nel_test_set = calcolo_numero_di_istanze_totali_presenti_nel_test_set_per_una_certa_entity(frasi_test_set, entity) #=TP+FN dell'entity

    TP_entity = true_positive_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity)

    # print("DENTRO RECALL:")
    # print("TP_entity: ", TP_entity)
    # print("numero_istanze_entity_nel_test_set: ", numero_istanze_entity_nel_test_set)
    # print("recall = TP_entity / numero_istanze_entity_nel_test_set: ", TP_entity / numero_istanze_entity_nel_test_set)
    # print("")
    # print("")

    if(numero_istanze_entity_nel_test_set == 0):
        return -1 #vuol dire che l'entity non è presente nel test set.

    recall = TP_entity / numero_istanze_entity_nel_test_set


    return recall



def precision(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity):

    # calcolo la recall del modello per l'entity fornita in input:
    TP_entity = true_positive_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity)
    FP_entity = false_positive_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, entity)

    # print("DENTRO PRECISION:")
    # print("TP_entity: ", TP_entity)
    # print("FP_entity: ", FP_entity)
    # print("precision = TP_entity / (TP_entity + FP_entity): ", TP_entity / (TP_entity + FP_entity))
    # print("")
    # print("")


    if((TP_entity + FP_entity) == 0):
        return -1 #vuol dire che l'entity data in input non è presente in nessuna delle frasi_test_set.

    precision = TP_entity / (TP_entity + FP_entity)


    return precision