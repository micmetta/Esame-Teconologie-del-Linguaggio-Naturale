import csv
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn
import re
import numpy as np


# DEVI CREARE I CONTESTI Ctx(w) per ogni Frame name, FE e LU,
# quindi w può essere uno dei tre elementi appena citati.
#
#
# DOPODICHE DEVI CREARE IL CONTESTO Ctx(s) per ogni possibile synset s presente
# a cui è associato il termine w.



#IN QUESTA IMPLEMENTAZIONE SIA PER I FRAMES, CHE PER I FEs CHE PER LE LUs come contesto (Ctx(w)) ho utilizzato sempre tutte queste informazioni:
# - DEF. frame di appartenenza.
# - DEF. di tutti i FEs e i nomi stessi di tutti i FEs del frame di appartenenza.
# - I nomi stessi di tutte le LUs del frame di appartenenza.




#A differenza della funzione depth di sopra, in depth_fino_LCS devo memorizzarmi la distanza minima del synset dal synset_primo_antenato_comune perchè devo considerare
# sempre il percorso più breve.
def depth_fino_LCS(synset, synset_primo_antenato_comune, prof_corrente_raggiunta, prof_min_raggiunta_fino_ad_ora):  # all'inizio quando invoco la funzione depth il secondo e il terzo parametro saranno 0.
    # calcolo la distanza tra il synset di input e la radice di Wordnet:

    # print("synset dentro depth_fino_LCS INIZIO: ", synset)
    # print("")
    # print("")

    prof_corrente_raggiunta += 1
    # print("type(synset): ", type(synset))

    if (synset.name() == synset_primo_antenato_comune.name()):  # controllo se con la chiamata corrente sono arrivato al synset dell'LCS che ho passato in input
        prof_corrente_raggiunta -= 1
        if (prof_corrente_raggiunta < prof_min_raggiunta_fino_ad_ora):
            prof_min_raggiunta_fino_ad_ora = prof_corrente_raggiunta

        return prof_min_raggiunta_fino_ad_ora

    else:
        lista_iperonimi = wn.synset(synset.name()).hypernyms()
        #print("lista_iperonimi DENTRO depth_fino_LCS: ", lista_iperonimi)
        if (lista_iperonimi != []): #ricorda che l'iperonimo di entity.n.01 è [] quindi quando ottengo [] vuol dire che mi devo per forza fermare nel salire.
            for iperonimo in lista_iperonimi:
                prof_min_raggiunta_fino_ad_ora = depth_fino_LCS(iperonimo, synset_primo_antenato_comune, prof_corrente_raggiunta, prof_min_raggiunta_fino_ad_ora)
        else:
            prof_corrente_raggiunta -= 1
            if (prof_corrente_raggiunta < prof_min_raggiunta_fino_ad_ora):
                prof_min_raggiunta_fino_ad_ora = prof_corrente_raggiunta

            return prof_min_raggiunta_fino_ad_ora

    # print("synset dentro depth: ", synset)
    # print("prof_max_raggiunta_fino_ad_ora (DENTRO DEPTH): ", prof_max_raggiunta_fino_ad_ora)
    # print("")

    return prof_min_raggiunta_fino_ad_ora



# Se non vuoi far uscire mai 0 basta che parti da 1 alla prima chiamata sia con prof_corrente_raggiunta che con prof_max_raggiunta_fino_ad_ora invece di 0.
def depth(synset, prof_corrente_raggiunta,
          prof_max_raggiunta_fino_ad_ora):  # all'inizio quando invoco la funzione depth il secondo e il terzo parametro saranno 0.
    # calcolo la distanza tra il synset di input e la radice di Wordnet:

    # print("synset dentro depth INIZIO: ", synset)
    # print("")
    # print("")

    prof_corrente_raggiunta += 1
    # print("type(synset): ", type(synset))

    if (synset.name() == 'entity.n.01'):  # controllo se con la chiamata corrente
        # prof_corrente_raggiunta -= 1
        if (prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
            prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

        return prof_max_raggiunta_fino_ad_ora

    else:
        lista_iperonimi = wn.synset(synset.name()).hypernyms()
        #print("lista_iperonimi DENTRO DEPTH: ", lista_iperonimi)
        if (lista_iperonimi != []):
            for iperonimo in lista_iperonimi:
                prof_max_raggiunta_fino_ad_ora = depth(iperonimo, prof_corrente_raggiunta,
                                                       prof_max_raggiunta_fino_ad_ora)
        else:
            # prof_corrente_raggiunta -= 1
            if (prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
                prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

            return prof_max_raggiunta_fino_ad_ora

    # print("synset dentro depth: ", synset)
    # print("prof_max_raggiunta_fino_ad_ora (DENTRO DEPTH): ", prof_max_raggiunta_fino_ad_ora)
    # print("")

    return prof_max_raggiunta_fino_ad_ora




def len_tra_due_synsets(s1,s2):

    min_path = np.inf
    #synset_concetto_corrente_associato_a_w1 = s1
    #synset_concetto_corrente_associato_a_w2 = s2
    len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = 0  # inizializzo len(c1,c2) = 0.
    LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = 0  # l'LCS migliore devo resettarlo ogni volta che considera una nuova coppia
    # di concetti c1 e c2.
    #print("synset_concetto_corrente_associato_a_w1: ", synset_concetto_corrente_associato_a_w1)
    #print("synset_concetto_corrente_associato_a_w2: ", synset_concetto_corrente_associato_a_w2)
    #print("")


    #############################################################################################################################################################################
    # Adesso controllo se synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2 già coincidono, perchè se fosse così allora potrei già dire che in questo
    # caso qual è la distanza tra questi due synset che sarà appunto 0.
    if (s1 == s2):
        len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = 0


    #############################################################################################################################################################################

    else:
        # Se entro qui vuol dire che non sono stato fortunato e quindi devo percorre la gerarchia per ottenere la distanza minima tra synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2.
        # CI POSSONO ESSERE 2 casi possibili per trovare tale distanza:
        # 1) (caso fortunato) Uno tra synset_concetto_corrente_associato_a_w1 (ovvero s1 corrente) e synset_concetto_corrente_associato_a_w2 (ovvero s2 corrente) è già IPERONIMO dell'altro,
        # e quindi di conseguenza l'altro è un iponimo dell'altro.
        # QUindi in questo caso len(s1,s2) = partendo dal synset (che può essere s1 o s2) che è l'iponimo dell'altro conto quanti passi impiego per arrivare all'altro synset seguendo
        # le relazioni di iperonimia.

        # 2) (caso più complicato) Quello detto nel caso 1) non avviene e quindi vuol dire che per trovare la distanza minima posso fare in questo modo:
        # 2.1) Trovo l'LCS di s1 corrente e s2 corrente.
        # 2.2) Una volta trovato l'LCS per trovare la distanza tra s1 e s2 faccio questo:
        # partendo da s1 conto quanti passi faccio per arrivare all'LCS e li sommo al numero di passi che faccio partendo dall'LCS per arrivare ad s2.
        # il valore di questa somma sarà in questo caso len(s1,s2).

        '''
        - NON CONSIDERARLO...
        # 3) (caso più complicato) Quello detto nel caso 1) non avviene e quindi vuol dire che per trovare la distanza minima posso fare in questo modo:
        # 2.1) Trovo l'iponimo più vicino di s1 corrente e s2 corrente.
        # 2.2) Una volta trovato l'iponimo più vicino per trovare la distanza tra s1 e s2 faccio questo:
        # partendo da s1 conto quanti passi faccio per arrivare all'iponimo in comune più vicino e li sommo al numero di passi che faccio partendo dall'iponimo in comune
        # più vicino per arrivare ad s2.

        # Il valore MINIMO TRA QUELLO OTTENUTO AL PASSO 2 E AL PASSO 3 sarà in questo caso len(s1,s2).
        '''

        # ESEGUO IL CASO 1 (più fortunato):
        # Per fare quello suddetto per il caso 1 innanzitutto creo due liste:
        # 1 -> che conterrà TUTTI gli iperonimi di synset_concetto_corrente_associato_a_w1
        # 2 -> che conterrà TUTTI gli iperonimi di synset_concetto_corrente_associato_a_w2
        lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1 = []
        lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2 = []

        # Creo poi due pile:
        # 1 -> che utilizzerò per riuscire a trovare tutti gli iperonimi di synset_concetto_corrente_associato_a_w1
        # 2 -> che utilizzerò per riuscire a trovare tutti gli iperonimi di synset_concetto_corrente_associato_a_w2
        pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1 = []
        pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2 = []

        # Adesso il PASSO INIZIALE è quello di inserire nella pila_1 tutti gli iperonimi iniziali di synset_concetto_corrente_associato_a_w1
        # e nella pila_2 tutti gli iperonimi iniziali di synset_concetto_corrente_associato_a_w2:

        pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(wn.synset(s1))
        lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1 = wn.synset(s1).hypernyms()
        for iperonimo in lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1:
            pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo)

        pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(wn.synset(s2))
        lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w2 = wn.synset(s2).hypernyms()
        for iperonimo in lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w2:
            pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo)

        ################################################################################################################################################################################
        # Adesso il passo successivo consiste nel creare due while dove con il primo vado a ciclare su tutti i possibili iperonimi di synset_concetto_corrente_associato_a_w1
        # partendo dai primi iperonimi inseriti nella pila nel passo iniziale, mentre con il secondo faccio la stessa cosa ma questa volta per il synset_concetto_corrente_associato_a_w2:

        # Primo while:
        while pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:  # continuo fino a quando la pila non è vuota.
            # 1) Il primo passo nel while sarà quello di poppare un elemento dalla pila_1 e memorizzarlo nella lista_1
            iperonimo_poppato = pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.pop()

            # print("iperonimo_poppato: ")
            # print(iperonimo_poppato)

            # 2) Il secondo passo nel while sarà invece quello di:

            #   1) Salvare nella lista_1 l'iperonimo appena poppato.
            #   2) trovare tutti gli iperonimi dell'elemento appena poppato dalla pila_1 e pusharli nella pila_1.
            lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo_poppato)  # 1)
            # 2):
            for iperonimo_poppato_iter in iperonimo_poppato.hypernyms():  # devo ciclare su tutti i possibili iperonimi dell'iperonimo appena poppato
                pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo_poppato_iter)

        # Secondo while:
        while pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:  # continuo fino a quando la pila non è vuota.
            # 1) Il primo passo nel while sarà quello di poppare un elemento dalla pila_2 e memorizzarlo nella lista_2
            iperonimo_poppato = pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.pop()

            # 2) Il secondo passo nel while sarà invece quello di:

            #   1) Salvare nella lista_2 l'iperonimo appena poppato.
            #   2) trovare tutti gli iperonimi dell'elemento appena poppato dalla pila_1 e pusharli nella pila_2.
            lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo_poppato)  # 1)
            # 2)
            for iperonimo_poppato_iter in iperonimo_poppato.hypernyms():
                pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(
                    iperonimo_poppato_iter)
        ################################################################################################################################################################################

        # A questo punto dopo i due cicli while nella lista_1 avrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w1
        # e nella lista_2 vrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w2.
        '''
        print("")
        print("lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1: ")
        print(lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1)
        print("")
        print("lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2: ")
        print(lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2)
        '''

        # Adesso quello che devo fare è questo:
        # 1) Devo controllare se in una delle due liste c'è un synset che corrisponde all'altro perchè se così fosse vuol dire che mi trovo nel caso fortunato (il caso 1):
        dist = 0
        caso_fortunato = False
        nome_synset_iperonimo_dell_altro_trovato = wn.synset('entity.n.01')
        for ss in lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:
            dist += 1
            if (ss.name() == "entity.n.01"):
                dist = 0  # resetto la distanza perchè quel percorso che stavo considerando è terminato.
            elif (ss.name() == s2):
                caso_fortunato = True
                break

        if not caso_fortunato:  # lo eseguo solo se synset_concetto_corrente_associato_a_w2 non è un iperonimo di synset_concetto_corrente_associato_a_w1
            dist = 0
            synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2 = False
            # caso_fortunato = False #sarà sicuramente ancora False se entro qui dentro.
            for ss in lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:
                dist += 1
                if (ss.name() == "entity.n.01"):
                    dist = 0  # resetto la distanza perchè quel percorso che stavo considerando è terminato.
                # print("")
                elif (ss.name() == s1):
                    synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2 = True
                    caso_fortunato = True
                    break
            '''
            print("")
            print("synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2: ",synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2)
            '''
            if (synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2):
                # se entro qui vuol dire che synset_concetto_corrente_associato_a_w1 (s1) è un iperonimo di synset_concetto_corrente_associato_a_w2 (s2)
                '''
                print("s1 è un iperonimo di s2 e quest'ultimo si trova ad una distanza da s1 pari a: ", dist)
                print("l's1 che è iperonimo di s2 è il seguente: ", nome_synset_iperonimo_dell_altro_trovato)
                '''
                if (dist < min_path):  # Aggiorno len(s1,s2) solamente se ho trovato una distanza più piccola rispetto a quella trovata fino a quel momento.
                    len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist

        else:  # se entro qui vuol dire che synset_concetto_corrente_associato_a_w2 (s2) è un iperonimo di synset_concetto_corrente_associato_a_w1 (s1)
            '''
            print("s2 è un iperonimo di s1 e quest'ultimo si trova ad una distanza da s1 pari a: ", dist)
            print("l's2 che è iperonimo di s1 è il seguente: ", nome_synset_iperonimo_dell_altro_trovato)
            '''
            if (dist < min_path):  # Aggiorno len(s1,s2) solamente se ho trovato una distanza più piccola rispetto a quella trovata fino a quel momento.
                len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist
        ##################################################################################################################################################################

        ##################################################################################################################################################################
        # ORA GESTISCO IL CASO 2):
        if (caso_fortunato == False):
            # se entro qui vuol dire che sono sicuro di non trovarmi nel caso 1) e quindi devo gestire per forza il caso 2).
            '''
            print("Gestisco il caso 2).")
            '''
            # 2) (caso più complicato) Quello detto nel caso 1) non avviene e quindi vuol dire che per trovare la distanza minima posso fare in questo modo:
            # 2.1) Trovo l'LCS di s1 corrente e s2 corrente.
            # 2.2) Una volta trovato l'LCS per trovare la distanza tra s1 e s2 faccio questo:
            # partendo da s1 conto quanti passi faccio per arrivare all'LCS e li sommo al numero di passi che faccio partendo dall'LCS per arrivare ad s2.
            # il valore di questa somma sarà in questo caso len(s1,s2).

            # Eseguo il passo 2.1):

            # Adesso quello che devo fare è questo:
            # 0) Devo controllare se nelle due liste c'è qualche synset in comune, qualora fosse così faccio questo (prima o poi qualcosa troverò al massimo potrà essere la radice di Wordnet l'unico synset in comune):
            # 1) Calcolo la distanza di questo synset dalla radice.
            # 2) Se questa distanza è maggiore di LCS_migliore trovato fino a quel momento allora aggiorno l'LCS_migliore, altrimenti non faccio nulla.

            # Invece di usare le liste puoi usare gli insiemi in modo da non avere duplicati (velocizza algoritmo).
            synset_primo_antenato_comune = wn.synset('entity.n.01')  # all'inizio setto questo come synset LCS ma è chiaro che potrà essere aggiornato.
            for synset_lista_1 in lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:  # 0):
                for synset_lista_2 in lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:  # 0):
                    if (synset_lista_1 == synset_lista_2):  # qualora fosse così faccio questo:
                        '''
                        print("")
                        print("Antenato comune trovato: ", synset_lista_1)
                        print("")
                        '''
                        distanza_antenato_comune_da_radice_wn = depth(synset_lista_1, 0, 0)  # 1)
                        '''
                        print("distanza_antenato_comune_da_radice_wn: ", distanza_antenato_comune_da_radice_wn)
                        '''
                        if (distanza_antenato_comune_da_radice_wn > LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2):  # 2)
                            synset_primo_antenato_comune = synset_lista_1  # aggiorno il synset dell'LCS perchè se entro in questo if vuol dire che ho trovato un antenato più profondo e quindi migliore.
                            LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = distanza_antenato_comune_da_radice_wn
                            '''
                            print("LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 aggiornato: ",LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2)
                            '''
                        '''
                        print("")
                        '''
            # eseguo il passo 2.2) -> Una volta trovato l'LCS per trovare la distanza tra s1 e s2 faccio questo:
            # partendo da s1 conto quanti passi faccio per arrivare all'LCS e li sommo al numero di passi che faccio partendo dall'LCS per arrivare ad s2.
            # il valore di questa somma sarà in questo caso len(s1,s2):

            # Parto da synset_concetto_corrente_associato_a_w1 e conto quanti passi impiego per arrivare all'LCS:
            # Per fare questo utilizzo la FUNZIONE depth_fino_LCS(...) che mi permette di calcolare la distanza tra il s1 e l'LCS di s1 e s2:
            '''
            print("synset_primo_antenato_comune FINALE: ", synset_primo_antenato_comune)
            print("wn.synset(synset_concetto_corrente_associato_a_w1): ",wn.synset(synset_concetto_corrente_associato_a_w1))
            print("wn.synset(synset_concetto_corrente_associato_a_w2): ",wn.synset(synset_concetto_corrente_associato_a_w2))
            '''
            dist_minima_tra_s1_e_LCS = depth_fino_LCS(wn.synset(s1), synset_primo_antenato_comune, 0, np.inf)
            dist_minima_tra_s2_e_LCS = depth_fino_LCS(wn.synset(s2), synset_primo_antenato_comune, 0, np.inf)

            '''
            print("dist_minima_tra_s1_e_LCS FINALE: ", dist_minima_tra_s1_e_LCS)
            print("dist_minima_tra_s2_e_LCS FINALE: ", dist_minima_tra_s2_e_LCS)
            '''

            len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist_minima_tra_s1_e_LCS + dist_minima_tra_s2_e_LCS  # il valore di questa somma sarà in questo caso len(s1,s2).
        #####################################################################################################################################################################


    return len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2  #termine funzione len_tra_due_synsets(s1,s2)





def concetti_associati_ai_synset_associati_al_termine_di_input(termine):
    lista_concetti_synset_associati_a_termine = [] #è una lista che avrà come elementi delle coppie fatte in questo modo: (concetto,synset), dove
    #il concetto è un termine che è presente in uno stesso synset con il termine di input.
    #il synset è proprio quello detto nella frase precedente.
    for ss in wn.synsets(termine):
        # print('\n' + str(ss))
        # print(ss.name(), ss.lemma_names())
        concetti_associati_al_termine_di_input_presenti_nel_synset_corrente = ss.lemma_names()
        synset_corrente = ss.name()
        # print("concetti associati a " + termine + ": ", concetti_associati_al_termine_di_input_presenti_nel_synset_corrente)
        print("concetti_associati_al_termine_di_input_presenti_nel_synset_corrente: ", concetti_associati_al_termine_di_input_presenti_nel_synset_corrente)
        print("synset_corrente: ", synset_corrente)


        #Ogni elemento trovato correntemento e il rispettivo synset lo aggiungo alla lista_concetti_synset_associati_a_termine:
        for concetto in concetti_associati_al_termine_di_input_presenti_nel_synset_corrente:
            #if(concetto != termine):
                #Creo la coppia concetto-synset (dove synset mi dice qual è il synset in cui è presente il concetto):
                concetto_synset_corrente = []
                concetto_synset_corrente.append(concetto)
                concetto_synset_corrente.append(synset_corrente)
                #####################################################################################################

                #Aggiungo alla lista_concetti_synset_associati_a_termine la coppia concetto_synset_corrente che ho appena trovato:
                lista_concetti_synset_associati_a_termine.append(concetto_synset_corrente)

    print("")
    print("lista_concetti_synset_associati_a " + termine + ":")
    print(lista_concetti_synset_associati_a_termine)
    print("")

    return lista_concetti_synset_associati_a_termine


def creo_contesto_w(nome_frame_originale_a_cui_appartiene_la_LU_corrente): #w = nome_LU_corrente

    frame = fn.frame_by_name(nome_frame_originale_a_cui_appartiene_la_LU_corrente)
    #Come Ctx_w di ogni LU userò queste informazioni (quindi adesso Ctx_w sarà una lista):
    # 1) Definizione del frame a cui appartiene quella LU
    # 2) Definizione di tutti i FEs del frame a cui appartiene quella LU
    # 3) Tutte le LUs che appartengono al frame a cui appartiene la LU


    # 1) METTO IN Ctx_w LA DEFINIZIONE del frame a cui appartiene quella LU:
    Ctx_w = frame.definition
    print("Contesto del frame corrente: ", Ctx_w)
    print("")
    Ctx_w = Ctx_w.split(" ")
    print("Contesto del frame corrente dopo primo split: ", Ctx_w)
    print("")

    ########## FACCIO UNA PULIZIA SULLE PAROLE DEL CONTESTO CORRENTE #################################
    try:
        while True:
            Ctx_w.remove("")  # rimuovo tutte le parole vuote
    except ValueError:
        pass

    indice_parola = -1
    for parola in Ctx_w:
        indice_parola += 1
        # print("parola: ", parola)

        if (parola[0] == "'"):
            parola_new = parola.replace("'", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)
            # print(parola)

        if (parola[-1] == "."):
            parola_new = parola.replace(".", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)

        if (parola[-1] == ","):
            parola_new = parola.replace(",", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)

        if (len(parola) >= 2):
            if (parola[-2] == "."):
                parola_new = parola.replace(".", "")
                del Ctx_w[indice_parola]
                Ctx_w.insert(indice_parola, parola_new)

        if (parola[-1] == "'"):
            parola_new = parola.replace("'", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)

            parola_new = Ctx_w[indice_parola]
            #print("parola_new: ", parola_new)
            if(len(parola_new) >= 1):
                if (parola_new[-1] == "."):
                    parola_new_2 = parola_new.replace(".", "")
                    del Ctx_w[indice_parola]
                    Ctx_w.insert(indice_parola, parola_new_2)

        # Ci sono alcune parole come questa: Undesirable_event che sono legate da _, quindi dovresti toglierlo altrimenti quando fai l'overlap non verrà considerata praticamente!!!
        # Quindi qui splitto le parole separate da _ :
        if ("_" in parola):
            del Ctx_w[indice_parola]  # cancello subito la parola composta
            lista_parole_splittate_da_underscore = parola.split("_")
            indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore = indice_parola
            for parola_in_lista_parole_splittate_da_underscore in lista_parole_splittate_da_underscore:
                Ctx_w.insert(indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore,
                             parola_in_lista_parole_splittate_da_underscore)
                indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore += 1  # incremento la posizione in cui inserire le varie parole che prima erano composte in un'unica parola
                # che aveva l'underscore, quindi ad es per la parola Undesirable_event avrò due parole che saranno Undesirable e event che verranno aggiunte come due parole distinte
                # in Ctx_w


    # Devo trovare la LU w di input nel frame identificato da nome_frame_originale_a_cui_appartiene_la_LU_corrente e prendere la definizione della LU:
    # 2) METTO IN Ctx_w TUTTE LE Definizione di tutti i FEs del frame a cui appartiene quella LU
    print("Stampo tutti i FEs del frame chiamato " + nome_frame_originale_a_cui_appartiene_la_LU_corrente + ":")
    print("")
    FEs = frame.FE.keys()
    for fe in FEs:
        fed = frame.FE[fe]
        print("FE che sto considerando in questo momento: ", fe)
        print("definizione_frame_element_w: ", fed.definition)
        #print("")
        Ctx_w.append(fe)
        #prima di inserire la definizione del fe corrente in Ctx_w devo prima splittarla in modo da avere le singole parole e poi pulire le singole parole dai caratteri inutili:
        definizione_fe_corrente = fed.definition
        lista_parole_definizione_fe_corrente = definizione_fe_corrente.split(" ")
        try:
            while True:
                lista_parole_definizione_fe_corrente.remove("")  # rimuovo tutte le parole vuote
        except ValueError:
            pass

        indice_parola = -1
        for parola in lista_parole_definizione_fe_corrente:
            indice_parola += 1
            #print("parola: ", parola)

            if (parola[0] == "'"):
                parola_new = parola.replace("'", "")
                del lista_parole_definizione_fe_corrente[indice_parola]
                lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new)
                # print(parola)

            if (parola[-1] == "."):
                parola_new = parola.replace(".", "")
                del lista_parole_definizione_fe_corrente[indice_parola]
                lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new)

            if (parola[-1] == ","):
                parola_new = parola.replace(",", "")
                del lista_parole_definizione_fe_corrente[indice_parola]
                lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new)

            if (len(parola) >= 2):
                if (parola[-2] == "."):
                    parola_new = parola.replace(".", "")
                    del lista_parole_definizione_fe_corrente[indice_parola]
                    lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new)

            if (parola[-1] == "'"):
                parola_new = parola.replace("'", "")
                del lista_parole_definizione_fe_corrente[indice_parola]
                lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new)

                parola_new = lista_parole_definizione_fe_corrente[indice_parola]
                # print("parola_new: ", parola_new)
                if (len(parola_new) >= 1):
                    if (parola_new[-1] == "."):
                        parola_new_2 = parola_new.replace(".", "")
                        del lista_parole_definizione_fe_corrente[indice_parola]
                        lista_parole_definizione_fe_corrente.insert(indice_parola, parola_new_2)

        #Adesso posso finalmente aggiungere tutte le parole della definizione presenti in lista_parole_definizione_fe_corrente all'interno di Ctx_w:
        for parola in lista_parole_definizione_fe_corrente:
            Ctx_w.append(parola)

    print("")
    print("")



    # 3) METTO IN Ctx_w TUTTE LE LUs che appartengono al frame a cui appartiene la LU corrente (che sarebbe la w di input):
    FEs = frame.lexUnit.keys()
    print("Stampo tutte le LUs del frame chiamato " + nome_frame_originale_a_cui_appartiene_la_LU_corrente + ":")
    for lu in FEs:
        if(" " in lu):
            lu = lu[:-2]
            lu_splittata = lu.split(" ")
            for parola in lu_splittata:
                print(parola)
                Ctx_w.append(parola)

        else:
            print(lu[:-2])
            Ctx_w.append(lu[:-2])
        print("")

    print("")
    print("")
    print("Ctx_w: ", Ctx_w)
    print("")

    return Ctx_w



def ComputeOverlap(signature, context):

    lista_esempi = signature[0]
    lista_glosse = signature[1]
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

    for glossa in lista_glosse:
        lista_parole_glossa = glossa.split(" ")
        #print("lista_parole_glossa: ", lista_parole_glossa)
        for parola_glossa in lista_parole_glossa:
            for parola_context in context:
                if(parola_glossa == parola_context):
                    #print("parola_glossa: ", parola_glossa)
                    #print("parola_context: ", parola_context)
                    overlap += 1


    return overlap



def The_Lesk_Algorithm(word, sentence, tutti_i_sensi_della_parola_da_disambiguare): #sentence = Ctx_w

    print("word DENTRO LESK: ", word)
    print("sentence DENTRO LESK: ", sentence)
    # tutti_i_sensi_della_parola_di_input = wn.synsets(word)
    print("tutti_i_sensi_della_parola_di_input: ", tutti_i_sensi_della_parola_da_disambiguare)
    best_sense = wn.synsets(word)[0].name()  # inizilizzo best_sense con il senso più frequente.
    # best_sense = tutti_i_sensi_della_parola_da_disambiguare[0]

    print("best_sense iniziale: ", best_sense)
    print("")
    print("")

    max_overlap = 0
    context = sentence  # inizializzo il contesto con tutte le parole della sentence che in questo caso è Ctx(w) (context è una lista di parole)

    for senso in tutti_i_sensi_della_parola_da_disambiguare:
        print("senso corrente: ", senso)

        # Adesso prendo solamente gli esempi e la glossa del senso corrente:
        lista_esempi = wn.synset(senso).examples()  # è una lista di frasi (può anche non essercene neanche una di frase e quindi sarà [])
        print("lista_esempi: ", lista_esempi)
        glossa = wn.synset(senso).definition()  # la glossa è una stringa e non sarà mai vuota.
        print("glossa: ", glossa)
        print("")
        print("")
        ###################################################################

        # Ora in aggiunta prendo tutti gli iperonimi del senso corrente:
        lista_iperonimi_senso_corrente = wn.synset(senso).hypernyms()

        # Adesso per ogni iperonimo trovato prendo tutti i suoi esempi e la glossa e li salvo rispettivamente
        # nella lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente e nella lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente:
        lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente = []
        lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente = []
        for iperonimo in lista_iperonimi_senso_corrente:
            esempi_iperonimo_corrente = iperonimo.examples()
            glossa_iperonimo_corrente = iperonimo.definition()
            lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente.append(
                glossa_iperonimo_corrente)  # aggiungo la glossa dell'iperonimo corrente
            for esempio in esempi_iperonimo_corrente:  # aggiungo tutti gli esempi dell'iperonimo corrente
                lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente.append(esempio)
        ################################################################

        # Adesso faccio la stessa cosa fatta sopra per gli iperonimi ma ora la faccio per gli iponimi:
        # Ora in aggiunta prendo tutti gli iponimi del senso corrente:
        lista_iponimi_senso_corrente = wn.synset(senso).hyponyms()

        lista_completa_degli_esempi_degli_iponimi_del_senso_corrente = []
        lista_completa_delle_glosse_degli_iponimi_del_senso_corrente = []
        for iponimo in lista_iponimi_senso_corrente:
            esempi_iponimo_corrente = iponimo.examples()
            glossa_iponimo_corrente = iponimo.definition()
            lista_completa_delle_glosse_degli_iponimi_del_senso_corrente.append(glossa_iponimo_corrente)
            for esempio in esempi_iponimo_corrente:
                lista_completa_degli_esempi_degli_iponimi_del_senso_corrente.append(esempio)

        ###############################################################################################

        # print("lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente: ")
        # print(lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente)
        # print("lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente: ")
        # print(lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente)
        # print("")
        # print("lista_completa_delle_glosse_degli_iponimi_del_senso_corrente: ")
        # print(lista_completa_delle_glosse_degli_iponimi_del_senso_corrente)
        # print("lista_completa_degli_esempi_degli_iponimi_del_senso_corrente: ")
        # print(lista_completa_degli_esempi_degli_iponimi_del_senso_corrente)
        # print("")
        # print("")

        # Adesso faccio in modo di aggiungere alla lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente la glossa = wn.synset(senso).definition() del senso corrente
        # che ho già trovato all'inizio del ciclo for corrente:
        lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente.append(glossa)

        # faccio la stessa cosa di sopra anche per la lista_completa_delle_glosse_degli_iponimi_del_senso_corrente:
        # lista_completa_delle_glosse_degli_iponimi_del_senso_corrente.append(glossa) #NON SERVE METTERE LA GLOSSA DEL SENSO CORRENTE ANCHE IN QUESTA LISTA PERCHE' ALLA FINE UNIREMO LE DUE
        # LISTE

        ###################################################################################################################################################################################
        # Adesso creo un'unica lista completa in cui considero sia gli esempi degli iperonimi e sia quelli degli iponimi:
        lista_completa_esempi_senso_corrente_iperonimi_e_iponimi = []
        if (lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente != []):
            for esempio in lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)

        if (lista_completa_degli_esempi_degli_iponimi_del_senso_corrente != []):
            for esempio in lista_completa_degli_esempi_degli_iponimi_del_senso_corrente:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)

        # infine aggiungo alla lista_completa_esempi_senso_corrente_iperonimi_e_iponimi anche gli esempi del senso corrente presenti in lista_esempi creata all'inizio di questo ciclo for:
        if (lista_esempi != []):
            for esempio in lista_esempi:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)
        ###################################################################################################################################################################################

        ###################################################################################################################################################################################
        # Faccio la stessa cosa fatta sopra per gli esempi anche per le glosse degli iperonimi e iponimi:
        lista_completa_glosse_senso_corrente_iperonimi_e_iponimi = []
        for glossa in lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente:
            lista_completa_glosse_senso_corrente_iperonimi_e_iponimi.append(glossa)

        for glossa in lista_completa_delle_glosse_degli_iponimi_del_senso_corrente:
            lista_completa_glosse_senso_corrente_iperonimi_e_iponimi.append(glossa)

        # In questo caso Non serve che aggiungo alla lista_completa_glosse_senso_corrente_iperonimi_e_iponimi anche la glossa del senso corrente presenti nella variabile glossa creata
        # all'inizio di questo ciclo for perchè l'ho già fatto prima.
        ###################################################################################################################################################################################

        print("lista_completa_esempi_senso_corrente_iperonimi_e_iponimi:")
        print(lista_completa_esempi_senso_corrente_iperonimi_e_iponimi)
        print("")
        print("lista_completa_glosse_senso_corrente_iperonimi_e_iponimi: ")
        print(lista_completa_glosse_senso_corrente_iperonimi_e_iponimi)
        print("")
        print("")

        signature = []
        # signature.append(lista_esempi)
        signature.append(lista_completa_esempi_senso_corrente_iperonimi_e_iponimi)
        # signature.append(glossa)
        signature.append(lista_completa_glosse_senso_corrente_iperonimi_e_iponimi)  # adesso la signature conterrà la lista di liste degli esempi e la lista di liste delle glosse.
        print("context: ", context)
        print("signature: ", signature)
        overlap = ComputeOverlap(signature, context) #context è una lista di parole
        print("overlap: ", overlap)

        if (overlap > max_overlap):
            max_overlap = overlap
            best_sense = senso

        print("")
        print("")

    return best_sense





##########################################################################################################################################################################################

############################################      INIZIO:     ##########################################################

num_synsets_predetti_correttamente = 0
num_synsets_predetti_in_totale = 0

lista_nomi_synsets_gold_sbagliati_dal_sistema = []
lista_nomi_contenente_synsets_predetti_in_maniera_errata = []


# Con il codice di sotto prendo le info salvate sul file chiamato "annotazioni mie dei frames" e per ogni frame presente lì dentro prendo prima tutti i concetti presenti nei vari synsets
#associati a quel determinato frame su wordnet e poi man mano per ciascuno di essi mi creo il contesto Ctx(w) e Ctx(s)
# in modo da calcolare lo score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1.
#Chiaramente alla fine l'algoritmo sceglierà come synset s da assegnare ad ogni frame quello che massimizza tale score.

columns_names = True
#header = ["Nome_frame", "nome_synset_wn"]
with open('annotazioni mie dei frames.csv', 'r', encoding='UTF8', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        if not columns_names:
            # if(considero_solo_i_primi_termini < 1):
            print(row)
            #w = in questo caso è il nome frame che ho mappato a mano su wordnet su un certo synset, in realtà
            #non è detto che io abbia mappato su wordnet esattamente il nome del frame originale perchè ho dovuto fare delle semplificazioni per il problema della multiword expression.
            nome_frame_originale = row[0]
            w = row[1] #prendo il nome del frame che ho mappato (quindi non è detto che sia quello originale)
            synset_frame_gold = row[2]

            print("nome_frame_originale: ", nome_frame_originale)
            print("nome_frame_mappato: ", w)
            print("synset_frame_gold: ", synset_frame_gold)
            print("")

            # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synsets associati al termine nome_frame
            tutti_i_concetti_associati_a_w = concetti_associati_ai_synset_associati_al_termine_di_input(w)
            print("tutti_i_concetti_associati_a_w: ", tutti_i_concetti_associati_a_w)
            print("")

            #1.2) Addesso da tutti_i_concetti_associati_a_w prendo solo i synsets li metto in un insieme che chiamo insieme_di_synsets_associati_a_w:
            insieme_di_synsets_associati_a_w = set() #mi basta un set perchè in questo modo sono sicuro di non avere synsets duplicati:
            for coppia_concetto_synset in tutti_i_concetti_associati_a_w:
                insieme_di_synsets_associati_a_w.add(coppia_concetto_synset[1]) #aggiungo solo il synset della coppia (esso si trova in seconda posizione)
            print("insieme_di_synsets_associati_a_w: ", insieme_di_synsets_associati_a_w)
            print("len(insieme_di_synsets_associati_a_w): ", len(insieme_di_synsets_associati_a_w))
            print("")


            #2) Dopodichè per il frame corrente (identificato da w) devo calcolarmi il suo contesto:
            #Ctx_w = creo_contesto_frame_w(nome_frame_originale)
            Ctx_w = creo_contesto_w(nome_frame_originale)

            #3) Dopodichè posso iniziare il ciclo per calcolare score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1:
            # DEVO VERIFICARE CHE L'INSIEME DI TUTTI I SENSI POSSIBILI NON SIA VUOTO:
            if (len(insieme_di_synsets_associati_a_w) >= 1):
                best_sense = The_Lesk_Algorithm(w, Ctx_w, insieme_di_synsets_associati_a_w) #chiamo l'algoritmo di Lesk passandogli il termine w da disambiguare
                #il suo contesto Ctx_w e l'insieme di possibili sensi che possono essere associati a w.
                print("best_sense trovato dall'algoritmo di LESK per la parola -" + w + "- :", best_sense)
                print("")
                print("")

                if (best_sense == synset_frame_gold):
                    num_synsets_predetti_correttamente += 1
                else:
                    lista_nomi_synsets_gold_sbagliati_dal_sistema.append(synset_frame_gold)
                    lista_nomi_contenente_synsets_predetti_in_maniera_errata.append(best_sense)

                num_synsets_predetti_in_totale += 1

        else:
            columns_names = False

##########################################################################################################################################################################################



# Con il codice di sotto invece prendo le info salvate sul file chiamato "annotazioni mie dei FEs" e per ogni FE presente lì dentro prendo prima tutti i concetti presenti nei vari synsets
#associati a quel determinato FE su wordnet e poi man mano per ciascuno di essi mi creo il contesto Ctx(w) e Ctx(s)
# in modo da calcolare lo score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1.
#Chiaramente alla fine l'algoritmo sceglierà come synset s da assegnare ad ogni frame quello che massimizza tale score.


columns_names = True
with open('annotazioni mie dei FEs.csv', 'r', encoding='UTF8', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        if not columns_names:
            # if(considero_solo_i_primi_termini < 1):
            print(row)
            #w = in questo caso è il nome frame che ho mappato a mano su wordnet su un certo synset, in realtà
            #non è detto che io abbia mappato su wordnet esattamente il nome del frame originale perchè ho dovuto fare delle semplificazioni per il problema della multiword expression.
            nome_frame_originale_a_cui_appartiene_il_fe_corrente = row[0]
            w = row[1] #prendo il nome del FE che ho mappato su wornet a mano.
            synset_frame_element_gold = row[2]

            print("nome_frame_originale_a_cui_appartiene_il_fe_corrente: ", nome_frame_originale_a_cui_appartiene_il_fe_corrente)
            print("nome_frame_element_mappato: ", w)
            print("synset_frame_element_gold: ", synset_frame_element_gold)
            print("")

            # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synsets associati al termine nome_frame
            tutti_i_concetti_associati_a_w = concetti_associati_ai_synset_associati_al_termine_di_input(w)
            print("tutti_i_concetti_associati_a_w: ", tutti_i_concetti_associati_a_w)
            print("")

            #1.2) Addesso da tutti_i_concetti_associati_a_w prendo solo i synsets li metto in un insieme che chiamo insieme_di_synsets_associati_a_w:
            insieme_di_synsets_associati_a_w = set() #mi basta un set perchè in questo modo sono sicuro di non avere synsets duplicati:
            for coppia_concetto_synset in tutti_i_concetti_associati_a_w:
                insieme_di_synsets_associati_a_w.add(coppia_concetto_synset[1]) #aggiungo solo il synset della coppia (esso si trova in seconda posizione)
            print("insieme_di_synsets_associati_a_w: ", insieme_di_synsets_associati_a_w)
            print("len(insieme_di_synsets_associati_a_w): ", len(insieme_di_synsets_associati_a_w))
            print("")


            #2) Dopodichè per il frame corrente (identificato da w) devo calcolarmi il suo contesto:
            #Ctx_w = creo_contesto_frame_element_w(nome_frame_originale_a_cui_appartiene_il_fe_corrente, w)
            Ctx_w = creo_contesto_w(nome_frame_originale_a_cui_appartiene_il_fe_corrente)

            #3) Dopodichè posso iniziare il ciclo per calcolare score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1:
            # DEVO VERIFICARE CHE L'INSIEME DI TUTTI I SENSI POSSIBILI NON SIA VUOTO:
            if (len(insieme_di_synsets_associati_a_w) >= 1):
                best_sense = The_Lesk_Algorithm(w, Ctx_w, insieme_di_synsets_associati_a_w) #chiamo l'algoritmo di Lesk passandogli il termine w da disambiguare
                #il suo contesto Ctx_w e l'insieme di possibili sensi che possono essere associati a w.
                print("best_sense trovato dall'algoritmo di LESK per il frame element -" + w + "- :", best_sense)
                print("")
                print("")

                if (best_sense == synset_frame_element_gold):
                    num_synsets_predetti_correttamente += 1
                else:
                    lista_nomi_synsets_gold_sbagliati_dal_sistema.append(synset_frame_element_gold)
                    lista_nomi_contenente_synsets_predetti_in_maniera_errata.append(best_sense)

                num_synsets_predetti_in_totale += 1

        else:
            columns_names = False

##########################################################################################################################################################################################



# Con il codice di sotto invece prendo le info salvate sul file chiamato "annotazioni mie delle LUs" e per ogni LU presente lì dentro prendo prima tutti i concetti presenti nei vari synsets
#associati a quella determinato LU su wordnet e poi man mano per ciascuno di essi mi creo il contesto Ctx(w) e Ctx(s)
# in modo da calcolare lo score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1.
#Chiaramente alla fine l'algoritmo sceglierà come synset s da assegnare ad ogni LU quello che massimizza tale score.


columns_names = True
with open('annotazioni mie delle LUs.csv', 'r', encoding='UTF8', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        if not columns_names:
            # if(considero_solo_i_primi_termini < 1):
            print(row)
            #w = in questo caso è il nome frame che ho mappato a mano su wordnet su un certo synset, in realtà
            #non è detto che io abbia mappato su wordnet esattamente il nome del frame originale perchè ho dovuto fare delle semplificazioni per il problema della multiword expression.
            nome_frame_originale_a_cui_appartiene_la_LU_corrente = row[0]
            w = row[1] #prendo il nome del FE che ho mappato su wornet a mano.
            w = w.split(".")[0]
            synset_LU_gold = row[2]

            print("nome_frame_originale_a_cui_appartiene_la_LU_corrente: ", nome_frame_originale_a_cui_appartiene_la_LU_corrente)
            print("nome_LU_mappata: ", w)
            print("synset_LU_gold: ", synset_LU_gold)
            print("")


            # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synsets associati al termine nome_frame
            tutti_i_concetti_associati_a_w = concetti_associati_ai_synset_associati_al_termine_di_input(w)
            print("tutti_i_concetti_associati_a_w: ", tutti_i_concetti_associati_a_w)
            print("")

            #1.2) Addesso da tutti_i_concetti_associati_a_w prendo solo i synsets li metto in un insieme che chiamo insieme_di_synsets_associati_a_w:
            insieme_di_synsets_associati_a_w = set() #mi basta un set perchè in questo modo sono sicuro di non avere synsets duplicati:
            for coppia_concetto_synset in tutti_i_concetti_associati_a_w:
                insieme_di_synsets_associati_a_w.add(coppia_concetto_synset[1]) #aggiungo solo il synset della coppia (esso si trova in seconda posizione)
            print("insieme_di_synsets_associati_a_w: ", insieme_di_synsets_associati_a_w)
            print("len(insieme_di_synsets_associati_a_w): ", len(insieme_di_synsets_associati_a_w))
            print("")



            #2) Dopodichè per la LU corrente (identificato da w) devo calcolarmi il suo contesto:
            Ctx_w = creo_contesto_w(nome_frame_originale_a_cui_appartiene_la_LU_corrente) #Ctx_w sarà una lista di parole.


            #3) Dopodichè posso iniziare il ciclo per calcolare score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1:
            if (len(insieme_di_synsets_associati_a_w) >= 1):# DEVO VERIFICARE CHE L'INSIEME DI TUTTI I SENSI POSSIBILI NON SIA VUOTO:

                best_sense = The_Lesk_Algorithm(w, Ctx_w, insieme_di_synsets_associati_a_w) #chiamo l'algoritmo di Lesk passandogli il termine w da disambiguare
                #il suo contesto Ctx_w e l'insieme di possibili sensi che possono essere associati a w.
                print("best_sense trovato dall'algoritmo di LESK per la LU -" + w + "- :", best_sense)
                print("")
                print("")

                if(best_sense == synset_LU_gold):
                    num_synsets_predetti_correttamente += 1
                else:
                    lista_nomi_synsets_gold_sbagliati_dal_sistema.append(synset_LU_gold)
                    lista_nomi_contenente_synsets_predetti_in_maniera_errata.append(best_sense)


                num_synsets_predetti_in_totale += 1


        else:
            columns_names = False

##########################################################################################################################################################################################

print("num_synsets_predetti_correttamente: ", num_synsets_predetti_correttamente)
print("num_synsets_predetti_in_totale: ", num_synsets_predetti_in_totale)
print("Accuratezza finale sistema: ", num_synsets_predetti_correttamente/num_synsets_predetti_in_totale)
print("")



################    PROVO A VALUTARE GLI ERRORI COMMESSI DAL SISTEMA:    ################
print("lista_nomi_synsets_gold_sbagliati_dal_sistema:")
print(lista_nomi_synsets_gold_sbagliati_dal_sistema)
print("")
print("lista_nomi_contenente_synsets_predetti_in_maniera_errata:")
print(lista_nomi_contenente_synsets_predetti_in_maniera_errata)
print("")


valore_distanze_totali_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata = 0
lista_valori_distanze = []


NUM_TOT_SYNSETS_SBAGLIATI = len(lista_nomi_synsets_gold_sbagliati_dal_sistema)
for i in range(0, len(lista_nomi_synsets_gold_sbagliati_dal_sistema)):
    #print("lista_nomi_synsets_gold_sbagliati_dal_sistema[i]: ", lista_nomi_synsets_gold_sbagliati_dal_sistema[i])
    #print("lista_nomi_contenente_synsets_predetti_in_maniera_errata[i]: ", lista_nomi_contenente_synsets_predetti_in_maniera_errata[i])
    #print("len_tra_due_synsets(lista_nomi_synsets_gold_sbagliati_dal_sistema[i], lista_nomi_contenente_synsets_predetti_in_maniera_errata[i]): ", len_tra_due_synsets(lista_nomi_synsets_gold_sbagliati_dal_sistema[i], lista_nomi_contenente_synsets_predetti_in_maniera_errata[i]))
    valore_distanze_totali_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata = len_tra_due_synsets(lista_nomi_synsets_gold_sbagliati_dal_sistema[i], lista_nomi_contenente_synsets_predetti_in_maniera_errata[i])
    lista_valori_distanze.append(valore_distanze_totali_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata)
    #print("")
    #print("")


media_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata = np.mean(lista_valori_distanze)
dev_std_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata = np.std(lista_valori_distanze)
print("")
print("")
print("valore_distanze_totali_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata: ", valore_distanze_totali_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata)
print("")
print("media_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata: ", media_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata)
print("dev_std_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata: ", dev_std_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata)
#La media_delle_distanze_tra_i_synsets_gold_sbagliati_e_i_synsets_predetti_in_maniera_errata:  8.3 (probabilmente è un pò alto.. sistema non proprio buono perchè quando sbaglia il synset giusto assegna un synset che è abbastanza lontano da quello originale.
############################################     FINE     ##############################################################