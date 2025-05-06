import nltk
from nltk.corpus import wordnet as wn
#nltk.download('wordnet')
import csv
import numpy as np


def concetti_associati_ai_synset_associati_al_termine_di_input(termine):
    lista_concetti_synset_associati_a_termine = []  # è una lista che avrà come elementi delle coppie fatte in questo modo: (concetto,synset), dove
    # il concetto è un termine che è presente in uno stesso synset con il termine di input.
    # il synset è proprio quello detto nella frase precedente.
    for ss in wn.synsets(termine):
        # print('\n' + str(ss))
        # print(ss.name(), ss.lemma_names())
        concetti_associati_al_termine_di_input_presenti_nel_synset_corrente = ss.lemma_names()
        synset_corrente = ss.name()
        # print("concetti associati a " + termine + ": ", concetti_associati_al_termine_di_input_presenti_nel_synset_corrente)

        # print("concetti_associati_al_termine_di_input_presenti_nel_synset_corrente: ",concetti_associati_al_termine_di_input_presenti_nel_synset_corrente)
        # print("synset_corrente: ", synset_corrente)

        # Ogni elemento trovato correntemento e il rispettivo synset lo aggiungo alla lista_concetti_synset_associati_a_termine (tranne il termine di input):
        for concetto in concetti_associati_al_termine_di_input_presenti_nel_synset_corrente:
            # if(concetto != termine):
            # Creo la coppia concetto-synset (dove synset mi dice qual è il synset in cui è presente il concetto):
            concetto_synset_corrente = []
            concetto_synset_corrente.append(concetto)
            concetto_synset_corrente.append(synset_corrente)
            #####################################################################################################

            # Aggiungo alla lista_concetti_synset_associati_a_termine la coppia concetto_synset_corrente che ho appena trovato:
            lista_concetti_synset_associati_a_termine.append(concetto_synset_corrente)

    print("")
    print("lista_concetti_synset_associati_a " + termine + ":")
    print(lista_concetti_synset_associati_a_termine)
    print("")

    return lista_concetti_synset_associati_a_termine


# Se non vuoi far uscire mai 0 basta che parti da 1 alla prima chiamata sia con prof_corrente_raggiunta che con prof_max_raggiunta_fino_ad_ora invece di 0.
def depth(synset, prof_corrente_raggiunta, prof_max_raggiunta_fino_ad_ora):  # all'inizio quando invoco la funzione depth il secondo e il terzo parametro saranno 0.
    # calcolo la distanza tra il synset di input e la radice di Wordnet:
    print("synset dentro depth INIZIO: ", synset)
    print("")
    print("")

    prof_corrente_raggiunta += 1
    # print("type(synset): ", type(synset))

    if (synset == "entity.n.01"):  # controllo se con la chiamata corrente sono arrivato alla entity
        prof_corrente_raggiunta -= 1
        if (prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
            prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

        return prof_max_raggiunta_fino_ad_ora

    else:
        lista_iperonimi = wn.synset(synset).hypernyms()
        print("lista_iperonimi DENTRO DEPTH: ", lista_iperonimi)
        if (lista_iperonimi != []):
            for iperonimo in lista_iperonimi:
                prof_max_raggiunta_fino_ad_ora = depth(iperonimo.name(), prof_corrente_raggiunta,prof_max_raggiunta_fino_ad_ora)
        else:
            prof_corrente_raggiunta -= 1
            if (prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
                prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

            return prof_max_raggiunta_fino_ad_ora

    # print("synset dentro depth: ", synset)
    # print("prof_max_raggiunta_fino_ad_ora (DENTRO DEPTH): ", prof_max_raggiunta_fino_ad_ora)
    # print("")

    return prof_max_raggiunta_fino_ad_ora


# A differenza della funzione depth di sopra, in depth_fino_LCS devo memorizzarmi la distanza minima del synset dal synset_primo_antenato_comune perchè devo considerare
# sempre il percorso più breve.
def depth_fino_LCS(synset, synset_primo_antenato_comune, prof_corrente_raggiunta, prof_min_raggiunta_fino_ad_ora):  # all'inizio quando invoco la funzione depth il secondo e il terzo parametro saranno 0.
    # calcolo la distanza tra il synset di input e la radice di Wordnet:
    print("synset dentro depth_fino_LCS INIZIO: ", synset)
    print("")
    print("")

    prof_corrente_raggiunta += 1
    # print("type(synset): ", type(synset))

    if (synset.name() == synset_primo_antenato_comune):  # controllo se con la chiamata corrente sono arrivato al synset dell'LCS che ho passato in input
        prof_corrente_raggiunta -= 1
        if (prof_corrente_raggiunta < prof_min_raggiunta_fino_ad_ora):
            prof_min_raggiunta_fino_ad_ora = prof_corrente_raggiunta

        return prof_min_raggiunta_fino_ad_ora

    else:
        lista_iperonimi = wn.synset(synset.name()).hypernyms()
        print("lista_iperonimi DENTRO depth_fino_LCS: ", lista_iperonimi)
        if (lista_iperonimi != []):
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


def Shortest_path(DEPTH_MAX, tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2):
    distanza_max_antenato_comune_dalla_radice_di_wordnet = np.NINF #-inf
    max = 0
    sim_massima_gia_raggiunta = False

    # 1) Quello che devo fare all'inizio è ciclare su tutte le possibili coppie (concetto,synset) presenti nelle due
    # due liste di input:

    # tutti_i_concetti_associati_a_w1 = [['', 'sexual_activity.n.01']]
    # tutti_i_concetti_associati_a_w2 = [['', 'sexual_love.n.02']]

    # tutti_i_concetti_associati_a_w2 = [['', 'sexual_activity.n.01']]
    # tutti_i_concetti_associati_a_w1 = [['', 'sexual_love.n.02']]

    #tutti_i_concetti_associati_a_w1 = [['', 'dog.n.01']] #36 val di similarità
    #tutti_i_concetti_associati_a_w2 = [['', 'cat.n.01']]

    print("")
    print("")
    print("tutti_i_concetti_associati_a_w1 dentro Shortest_path: ", tutti_i_concetti_associati_a_w1)
    print("tutti_i_concetti_associati_a_w2 dentro Shortest_path: ", tutti_i_concetti_associati_a_w2)

    for coppia_concetto_synset_w1_corrente in tutti_i_concetti_associati_a_w1:
        for coppia_concetto_synset_w2_corrente in tutti_i_concetti_associati_a_w2:

            print("")
            print("")
            print("")
            print("")
            # 2) Per ogni possibile coppia_concetto_synset_w1_corrente e coppia_concetto_synset_w2_corrente
            # calcolo la metrica Shortest_path che è questa qui:
            # sim(c1, c2) = cs(c1, c2) = ( (2*depth_MAX) - len(c1,c2) ).
            # Poi però devo considerare il max perchè in questa esercitazione gli input sono i termini e non i sensi.

            # Per ottenere il punto 2) ho bisogno di seguire questi passi intermedi:
            # 2.1) Per prima cosa devo cercare di calcolare len(synset_concetto_corrente_associato_a_w1, synset_concetto_corrente_associato_a_w2), ovvero la distanza tra il
            # synset_concetto_corrente_associato_a_w1 e il synset_concetto_corrente_associato_a_w2.

            # 2.1.1) Per fare il 2.1) Quello che faccio è innanzitutto selezionare il synset di coppia_concetto_synset_w1_corrente e quello di coppia_concetto_synset_w2_corrente
            # in modo da poterli usare come chiavi per iniziare a scalare la gerarchia di wordnet:
            synset_concetto_corrente_associato_a_w1 = coppia_concetto_synset_w1_corrente[1]  # synset_concetto_corrente_associato_a_w1 = synset a cui è associato il concetto c1 corrente
            synset_concetto_corrente_associato_a_w2 = coppia_concetto_synset_w2_corrente[1]  # synset_concetto_corrente_associato_a_w2 = synset a cui è associato il concetto c2 corrente
            len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = 0  # inizializzo len(c1,c2) = 0.

            print("synset_concetto_corrente_associato_a_w1: ", synset_concetto_corrente_associato_a_w1)
            print("synset_concetto_corrente_associato_a_w2: ", synset_concetto_corrente_associato_a_w2)
            print("")

            #############################################################################################################################################################################
            # Adesso controllo se synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2 già coincidono, perchè se fosse così allora potrei già dire che in questo
            # caso qual è la distanza tra questi due synset che sarà appunto 0.

            #CONTROLLA CHE QUESTA UGUAGLIANZA DI SOTTO NON VALGA ANCHE PER ENTITY!!!!!!!

            if (synset_concetto_corrente_associato_a_w1 == synset_concetto_corrente_associato_a_w2):
                len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = 0
                sim_massima_gia_raggiunta = True
                '''
                # scelgo uno dei due su cui calcolare la distanza con la radice tanto sono uguali:
                profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2 = depth(
                    (wn.synset(synset_concetto_corrente_associato_a_w1)), 0, 0)

                if (profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2 > LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2):
                    # se entro qui vuol dire che la profondità massima precedente è stata battuta per cui devo aggiornare l'LCS_migliore trovato fino a quel momento:
                    LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2
                '''

            #############################################################################################################################################################################

            else:
                # Se entro qui vuol dire che non sono stato fortunato e quindi devo percorre la gerarchia per ottenere la distanza minima tra synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2.
                # CI POSSONO ESSERE 2 casi possibili per trovare tale distanza:

                # 1) (caso fortunato) Uno tra synset_concetto_corrente_associato_a_w1 (ovvero s1 corrente) e synset_concetto_corrente_associato_a_w2 (ovvero s2 corrente) è già IPERONIMO dell'altro,
                # e quindi di conseguenza l'altro è un iponimo dell'altro.
                # Quindi in questo caso len(s1,s2) = partendo dal synset (che può essere s1 o s2) che è l'iponimo dell'altro conto quanti passi impiego per arrivare all'altro synset seguendo
                # le relazioni di iperonimia.

                # 2) (caso più complicato) Quello detto nel caso 1) non avviene e quindi vuol dire che per trovare la distanza minima posso fare in questo modo:
                # 2.1) Trovo l'LCS di s1 corrente e s2 corrente.
                # 2.2) Una volta trovato l'LCS per trovare la distanza tra s1 e s2 faccio questo:
                # partendo da s1 conto quanti passi faccio per arrivare all'LCS e li sommo al numero di passi che faccio partendo dall'LCS per arrivare ad s2.
                # il valore di questa somma sarà in questo caso len(s1,s2).


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

                pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(
                    wn.synset(synset_concetto_corrente_associato_a_w1))
                lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1 = wn.synset(
                    synset_concetto_corrente_associato_a_w1).hypernyms()
                for iperonimo in lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1:
                    pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo)

                pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(
                    wn.synset(synset_concetto_corrente_associato_a_w2))
                lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w2 = wn.synset(
                    synset_concetto_corrente_associato_a_w2).hypernyms()
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
                    lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(
                        iperonimo_poppato)  # 1)
                    # 2):
                    for iperonimo_poppato_iter in iperonimo_poppato.hypernyms():  # devo ciclare su tutti i possibili iperonimi dell'iperonimo appena poppato
                        pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(
                            iperonimo_poppato_iter)

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
                        pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo_poppato_iter)
                ################################################################################################################################################################################


                # A questo punto dopo i due cicli while nella lista_1 avrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w1
                # e nella lista_2 avrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w2.
                print("")
                print("lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1: ")
                print(lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1)
                print("")
                print("lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2: ")
                print(lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2)
                print("")

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
                    elif (ss.name() == synset_concetto_corrente_associato_a_w2):
                        caso_fortunato = True
                        nome_synset_iperonimo_dell_altro_trovato = synset_concetto_corrente_associato_a_w2
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
                        elif (ss.name() == synset_concetto_corrente_associato_a_w1):
                            synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2 = True
                            caso_fortunato = True
                            nome_synset_iperonimo_dell_altro_trovato = synset_concetto_corrente_associato_a_w1
                            break
                    print("")
                    print("synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2: ",synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2)

                    if (synset_concetto_corrente_associato_a_w1_e_un_iperonimo_di_synset_concetto_corrente_associato_a_w2):
                        # se entro qui vuol dire che synset_concetto_corrente_associato_a_w1 (s1) è un iperonimo di synset_concetto_corrente_associato_a_w2 (s2)
                        print("s1 è un iperonimo di s2 e quest'ultimo si trova ad una distanza da s1 pari a: ", dist)
                        print("l's1 che è iperonimo di s2 è il seguente: ", nome_synset_iperonimo_dell_altro_trovato)

                        if (dist < min_path):  # Aggiorno len(s1,s2) solamente se ho trovato una distanza più piccola rispetto a quella trovata fino a quel momento.len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist

                else:  # se entro qui vuol dire che synset_concetto_corrente_associato_a_w2 (s2) è un iperonimo di synset_concetto_corrente_associato_a_w1 (s1)
                    print("s2 è un iperonimo di s1 e quest'ultimo si trova ad una distanza da s1 pari a: ", dist)
                    print("l's2 che è iperonimo di s1 è il seguente: ", nome_synset_iperonimo_dell_altro_trovato)

                    if (dist < min_path):  # Aggiorno len(s1,s2) solamente se ho trovato una distanza più piccola rispetto a quella trovata fino a quel momento.
                        len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist
                ##################################################################################################################################################################
                '''


                ##################################################################################################################################################################
                # ORA GESTISCO IL CASO 2):
                #if (caso_fortunato == False):
                    # se entro qui vuol dire che sono sicuro di non trovarmi nel caso 1) e quindi devo gestire per forza il caso 2).
                    #print("Gestisco il caso 2).")
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

                #Controllo se s1 è un iperonimo di s2:
                s1_iperonimo_di_s2 = False
                for synset_lista_2 in lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:
                    print("synset_lista_2: ", synset_lista_2.name())
                    print("synset_concetto_corrente_associato_a_w1: ", synset_concetto_corrente_associato_a_w1)

                    if(synset_lista_2.name() == synset_concetto_corrente_associato_a_w1):
                        print("s1 è iperonimo di s2 e quindi il LCS in questo caso è s1!!!")
                        s1_iperonimo_di_s2 = True
                        distanza_antenato_comune_da_radice_wn = depth(synset_lista_2.name(), 0, 0)
                        if (distanza_antenato_comune_da_radice_wn > distanza_max_antenato_comune_dalla_radice_di_wordnet):
                            synset_primo_antenato_comune = synset_concetto_corrente_associato_a_w1
                            #LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = distanza_antenato_comune_da_radice_wn
                            distanza_max_antenato_comune_dalla_radice_di_wordnet = distanza_antenato_comune_da_radice_wn
                            print("distanza_max_antenato_comune_dalla_radice_di_wordnet AGGIORNATO: ", distanza_max_antenato_comune_dalla_radice_di_wordnet)
                            len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = depth_fino_LCS(synset_lista_2, synset_primo_antenato_comune, 0, np.inf)


                s2_iperonimo_di_s1 = False
                if(s1_iperonimo_di_s2 == False):
                    # Controllo se s2 è un iperonimo di s1:
                    for synset_lista_1 in lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:
                        if (synset_lista_1.name() == synset_concetto_corrente_associato_a_w2):
                            print("s2 è iperonimo di s1 e quindi il LCS in questo caso è s2!!!")
                            s2_iperonimo_di_s1 = True
                            distanza_antenato_comune_da_radice_wn = depth(synset_lista_1.name(), 0, 0)
                            if (distanza_antenato_comune_da_radice_wn > distanza_max_antenato_comune_dalla_radice_di_wordnet):
                                synset_primo_antenato_comune = synset_concetto_corrente_associato_a_w2
                                #LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = distanza_antenato_comune_da_radice_wn
                                distanza_max_antenato_comune_dalla_radice_di_wordnet = distanza_antenato_comune_da_radice_wn
                                print("distanza_max_antenato_comune_dalla_radice_di_wordnet AGGIORNATO: ", distanza_max_antenato_comune_dalla_radice_di_wordnet)
                                len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = depth_fino_LCS(synset_lista_1, synset_primo_antenato_comune, 0, np.inf)



                #SE SIA s1_iperonimo_di_s2 CHE s2_iperonimo_di_s1 SONO FALSE ALLORA VUOL DIRE CHE IL LCS NON E' NESSUNO DEI DUE E QUINDI DEVO TROVARLO SCANDENDO
                #TUTTE E DUE LE LISTE CHE CONTENGONO RISPETTIVAMENTE TUTTI GLI IPERONIMI DI S1 E TUTTI QUELLI DI S2.
                if((s1_iperonimo_di_s2 == False) and (s2_iperonimo_di_s1 == False)):

                    for synset_lista_1 in lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:  # 0):
                        for synset_lista_2 in lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:  # 0):
                            if (synset_lista_1.name() == synset_lista_2.name()):  # qualora fosse così faccio questo:
                                print("")
                                print("Antenato comune trovato: ", synset_lista_1)
                                print("")
                                distanza_antenato_comune_da_radice_wn = depth(synset_lista_1.name(), 0, 0)  # 1)
                                print("distanza_antenato_comune_da_radice_wn: ", distanza_antenato_comune_da_radice_wn)
                                if (distanza_antenato_comune_da_radice_wn > distanza_max_antenato_comune_dalla_radice_di_wordnet):  # 2)
                                    distanza_max_antenato_comune_dalla_radice_di_wordnet = distanza_antenato_comune_da_radice_wn
                                    synset_primo_antenato_comune = synset_lista_1  # aggiorno il synset dell'LCS perchè se entro in questo if vuol dire che ho trovato un antenato più profondo e quindi migliore.
                                    print("distanza_max_antenato_comune_dalla_radice_di_wordnet AGGIORNATO: ", distanza_max_antenato_comune_dalla_radice_di_wordnet)

                                    #LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = distanza_antenato_comune_da_radice_wn
                                    #print("LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 aggiornato: ", LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2)
                                print("")


                    # eseguo il passo 2.2) -> Una volta trovato l'LCS per trovare la distanza tra s1 e s2 faccio questo:
                    # partendo da s1 conto quanti passi faccio per arrivare all'LCS e li sommo al numero di passi che faccio partendo dall'LCS per arrivare ad s2.
                    # il valore di questa somma sarà in questo caso len(s1,s2):

                    # Parto da synset_concetto_corrente_associato_a_w1 e conto quanti passi impiego per arrivare all'LCS:
                    # Per fare questo utilizzo la FUNZIONE depth_fino_LCS(...) che mi permette di calcolare la distanza tra il s1 e l'LCS di s1 e s2:
                    print("synset_primo_antenato_comune FINALE: ", synset_primo_antenato_comune)
                    print("wn.synset(synset_concetto_corrente_associato_a_w1): ",wn.synset(synset_concetto_corrente_associato_a_w1))
                    print("wn.synset(synset_concetto_corrente_associato_a_w2): ",wn.synset(synset_concetto_corrente_associato_a_w2))
                    dist_minima_tra_s1_e_LCS = depth_fino_LCS(wn.synset(synset_concetto_corrente_associato_a_w1), synset_primo_antenato_comune.name(), 0, np.inf)
                    dist_minima_tra_s2_e_LCS = depth_fino_LCS(wn.synset(synset_concetto_corrente_associato_a_w2), synset_primo_antenato_comune.name(), 0, np.inf)
                    print("dist_minima_tra_s1_e_LCS FINALE: ", dist_minima_tra_s1_e_LCS)
                    print("dist_minima_tra_s2_e_LCS FINALE: ", dist_minima_tra_s2_e_LCS)
                    len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 = dist_minima_tra_s1_e_LCS + dist_minima_tra_s2_e_LCS  # il valore di questa somma sarà in questo caso len(s1,s2).
                    #####################################################################################################################################################################

            # Solo adesso posso essere sicuro di aver trovato la distanza len(c1,c2) più piccola in assoluto tra tutti i possibili synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2.
            # Quindi posso finalmente calcolare la metrica di Shortest path per synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2 correnti:

            # sim(c1,c2) = sim_path(c1,c2) = ( (2*depth_MAX) - len(c1,c2) ) (Shortest path).
            # print("")
            # print("wn.synset(synset_concetto_corrente_associato_a_w1) PRIMA DI CALCOLARE LA METRICA: ", wn.synset(synset_concetto_corrente_associato_a_w1))
            # print("wn.synset(synset_concetto_corrente_associato_a_w2) PRIMA DI CALCOLARE LA METRICA: ", wn.synset(synset_concetto_corrente_associato_a_w2))
            # print("")

            if (sim_massima_gia_raggiunta):
                # se entro qui vuol dire che sono stato fortunato perchè posso già dire che la len(c1,c2) = 0 e quindi posso restituire la similarità max
                # per questa metrica che è 2*depth_Max:
                return 2 * DEPTH_MAX  # termine funzione Shortest_path


            print("")
            sim_path_c1_c2 = (2 * DEPTH_MAX) - len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2
            # print("LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2: ",LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2)
            print("len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2 più piccola trovata: ",len_synset_concetto_corrente_associato_a_w1_synset_concetto_corrente_associato_a_w2)
            print("sim_path_c1_c2 corrente: ", sim_path_c1_c2)

            # Ora controllo se cs_c1_c2 corrente è maggiore del max, perchè se così fosse allora devo aggiornare il max:
            if (sim_path_c1_c2 > max):
                max = sim_path_c1_c2  # aggiorno il max
                print("max aggiornato: ", max)

            print("")
            print("")


    return max  # alla fine restituisco il max che sarà proprio il valore di similarità della metrica Shortest path per le due parole w1 e w2 iniziali.
                # termine funzione Shortest_path.




# Carico i dati:
header = ["Word 1", "Word 2", "Risultati"]
data = []  # qui metterò mano mano le coppie con la rispettiva similarità calcolata.
columns_names = True
#considero_solo_i_primi_termini = 0  # dopo questo dovrò toglierlo per poter considerare tutte le coppie di termini.
# DEPTH_MAX = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets()) #è una costante quindi la calcolo una sola volta.
DEPTH_MAX = 20

with open('WordSim353.csv', 'r') as f:
    reader = csv.reader(f)
    # open the file in the write mode
    with open('Risultati Shortest path.csv', 'w', encoding='UTF8', newline='') as file:

        # create the csv writer
        writer = csv.writer(file)
        # write the header
        writer.writerow(header)

        for row in reader:
            if not columns_names:
                #if(considero_solo_i_primi_termini < 1):
                    print(row)
                    w1 = row[0]
                    w2 = row[1]

                    #w1 = "love"
                    #w2 = "sex"

                    print("w1: ", w1)
                    print("w2: ", w2)


                    #considero_solo_i_primi_termini += 1

                    # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w1
                    tutti_i_concetti_associati_a_w1 = concetti_associati_ai_synset_associati_al_termine_di_input(w1)

                    # 2) La seconda cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w2
                    tutti_i_concetti_associati_a_w2 = concetti_associati_ai_synset_associati_al_termine_di_input(w2)

                    #print("tutti_i_concetti_associati_a_w1: ", tutti_i_concetti_associati_a_w1)
                    #print("tutti_i_concetti_associati_a_w2: ", tutti_i_concetti_associati_a_w2)

                    # 3) La terza cosa da fare è quella di calcolare tra ogni possibile coppia di concetti associati ai
                    # vari synset di w1 e w2 che sono presenti rispettivamente in tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2 il valore sim(c1,c2) ove in questo script
                    # sim_shortest_Path(c1,c2) = cs(c1,c2) = 2*depth_MAX - len(s1,s2).

                    # Per fare quello appena detto chiamo la funzione che ho creato per implementare Shortest Path passandogli DEPTH_MAX, tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2 in input:
                    sp = Shortest_path(DEPTH_MAX, tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2)
                    #print("Shortest_path max: ", sp)

                    # Salvo i due termini e il valore di similarità restituito dalla metrica Wu & Palmer per essi all'interno su un file (che poi userò per calcolare i coeff. di Pearson e Spearman).
                    data = [w1, w2, sp]
                    # write the data
                    writer.writerow(data)


            else:
                columns_names = False

'''
#formula di partenza:
sim(w1,w2) = considero solo il max tra tutti i possibili c1-app-s(w1) e c2-app-s(w2) di --> [sim(c1,c2)] 

ove in questo caso:
sim(c1,c2) = cs(c1,c2) = 2*depth(LCS) / (depth(s1) + depth(s2))
ove:
depth(LCS) = è il più basso (ovvero il primo) antenato comune tra c1 e c2
depth(c1) = distanza fra la radice di Wordnet e il synset di c1
depth(c2) = distanza fra la radice di Wordnet e il synset di c2
'''



