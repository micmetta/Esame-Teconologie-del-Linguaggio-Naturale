import nltk
from nltk.corpus import wordnet as wn
#nltk.download('wordnet')
import csv


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



#Se non vuoi far uscire mai 0 basta che parti da 1 alla prima chiamata sia con prof_corrente_raggiunta che con prof_max_raggiunta_fino_ad_ora invece di 0.
def depth(synset, prof_corrente_raggiunta, prof_max_raggiunta_fino_ad_ora): #all'inizio quando invoco la funzione depth il secondo e il terzo parametro saranno 0.
    #calcolo la distanza tra il synset di input e la radice di Wordnet:
    print("synset dentro depth INIZIO: ", synset)
    print("")
    print("")

    prof_corrente_raggiunta += 1
    #print("type(synset): ", type(synset))

    if(synset.name() == 'entity.n.01'): #controllo se con la chiamata corrente
        #prof_corrente_raggiunta -= 1
        if(prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
            prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

        return prof_max_raggiunta_fino_ad_ora

    else:
        lista_iperonimi = wn.synset(synset.name()).hypernyms()
        print("lista_iperonimi DENTRO DEPTH: ", lista_iperonimi)
        if(lista_iperonimi != []):
            for iperonimo in lista_iperonimi:
                prof_max_raggiunta_fino_ad_ora = depth(iperonimo, prof_corrente_raggiunta, prof_max_raggiunta_fino_ad_ora)
        else:
            #prof_corrente_raggiunta -= 1
            if (prof_corrente_raggiunta > prof_max_raggiunta_fino_ad_ora):
                prof_max_raggiunta_fino_ad_ora = prof_corrente_raggiunta

            return prof_max_raggiunta_fino_ad_ora


    # print("synset dentro depth: ", synset)
    # print("prof_max_raggiunta_fino_ad_ora (DENTRO DEPTH): ", prof_max_raggiunta_fino_ad_ora)
    # print("")

    return prof_max_raggiunta_fino_ad_ora





def Wu_and_Palmer(tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2):

    max = 0
    #1) Quello che devo fare all'inizio è ciclare su tutte le possibili coppie (concetto,synset) presenti nelle due
    #due liste di input:

    # tutti_i_concetti_associati_a_w1 = [['', 'sexual_activity.n.01']]
    # tutti_i_concetti_associati_a_w2 = [['', 'sexual_love.n.02']]

    # tutti_i_concetti_associati_a_w1 = [['', 'sexual_activity.n.01']]
    # tutti_i_concetti_associati_a_w2 = [['', 'sexual_love.n.02']]

    #tutti_i_concetti_associati_a_w1 = [['', 'Jerusalem.n.01']]
    #tutti_i_concetti_associati_a_w2 = [['', 'Israel.n.01']]

    print("")
    print("")
    print("tutti_i_concetti_associati_a_w1 dentro wp: ", tutti_i_concetti_associati_a_w1)
    print("tutti_i_concetti_associati_a_w2 dentro wp: ", tutti_i_concetti_associati_a_w2)

    for coppia_concetto_synset_w1_corrente in tutti_i_concetti_associati_a_w1:
        for coppia_concetto_synset_w2_corrente in tutti_i_concetti_associati_a_w2:

            print("")
            print("")
            print("")
            print("")
            #2) Per ogni possibile coppia_concetto_synset_w1_corrente e coppia_concetto_synset_w2_corrente
            # calcolo la metrica di Wu & Palmer che è questa qui:
            # sim(c1, c2) = cs(c1, c2) = 2 * depth(LCS) / (depth(s1) + depth(s2)).
            # Poi però devo considerare il max perchè in questa esercitazione gli input sono i termini e non i sensi.

            #Per ottenere il punto 2) ho bisogno di seguire questi passi intermedi:
            #2.1) Per prima cosa devo cercare di calcolare depth(LCS), ovvero la distanza tra la radice di Wordnet e il primo antenato comune
            #tra coppia_concetto_synset_w1_corrente e coppia_concetto_synset_w2_corrente:

            #2.1.1) Per fare il 2.1) Quello che faccio è innanzitutto selezionare il synset di coppia_concetto_synset_w1_corrente e quello di coppia_concetto_synset_w2_corrente
            #in modo da poterli usare come chiavi per iniziare a scalare la gerarchia di wordnet attraverso la relazione di iperonimia e trovare il primo synset in comune:
            synset_concetto_corrente_associato_a_w1 = coppia_concetto_synset_w1_corrente[1]
            synset_concetto_corrente_associato_a_w2 = coppia_concetto_synset_w2_corrente[1]
            LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = 0 #l'LCS migliore devo resettarlo ogni volta che considera una nuova coppia
            #di concetti c1 e c2.


            print("synset_concetto_corrente_associato_a_w1: ", synset_concetto_corrente_associato_a_w1)
            print("synset_concetto_corrente_associato_a_w2: ", synset_concetto_corrente_associato_a_w2)
            print("")

            #############################################################################################################################################################################
            #Adesso controllo se synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2 già coincidono, perchè se fosse così allora potrei già dire che in questo
            #caso qual è la distanza tra questo synset e la radice di Wordnet. Non è detto che questo sia poi effettivamente l'LCS finale:
            if(synset_concetto_corrente_associato_a_w1 == synset_concetto_corrente_associato_a_w2):

                #scelgo uno dei due su cui calcolare la distanza con la radice tanto sono uguali:
                profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2 = depth((wn.synset(synset_concetto_corrente_associato_a_w1)),0,0)

                if(profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2 > LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2):
                    #se entro qui vuol dire che la profondità massima precedente è stata battuta per cui devo aggiornare l'LCS_migliore trovato fino a quel momento:
                    LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = profondita_primo_antenato_comune_a_synset_concetto_corrente_associato_a_w1_e_a_synset_concetto_corrente_associato_a_w2
            #############################################################################################################################################################################

            else:
                #Se entro qui vuol dire che non sono stato fortunato e quindi devo risalire la gerarchia tramite le relazioni di iperonimia per ottenere tutti gli antenati
                #sia di synset_concetto_corrente_associato_a_w1 che di synset_concetto_corrente_associato_a_w2:

                #Per fare quello suddetto innanzitutto creo due liste:
                #1 -> che conterrà TUTTI gli iperonimi di synset_concetto_corrente_associato_a_w1
                #2 -> che conterrà TUTTI gli iperonimi di synset_concetto_corrente_associato_a_w2
                lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1 = []
                lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2 = []

                #Creo poi due pile:
                #1 -> che utilizzerò per riuscire a trovare tutti gli iperonimi di synset_concetto_corrente_associato_a_w1
                #2 -> che utilizzerò per riuscire a trovare tutti gli iperonimi di synset_concetto_corrente_associato_a_w2
                pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1 = []
                pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2 = []


                #Adesso il PASSO INIZIALE è quello di inserire nella pila_1 tutti gli iperonimi iniziali di synset_concetto_corrente_associato_a_w1
                #e nella pila_2 tutti gli iperonimi iniziali di synset_concetto_corrente_associato_a_w2:

                pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(wn.synset(synset_concetto_corrente_associato_a_w1))
                lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1 = wn.synset(synset_concetto_corrente_associato_a_w1).hypernyms()
                for iperonimo in lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w1:
                    pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo)

                pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(wn.synset(synset_concetto_corrente_associato_a_w2))
                lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w2 = wn.synset(synset_concetto_corrente_associato_a_w2).hypernyms()
                for iperonimo in lista_di_iperonimi_iniziali_associati_a_synset_concetto_corrente_associato_a_w2:
                    pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo)


                ################################################################################################################################################################################
                #Adesso il passo successivo consiste nel creare due while dove con il primo vado a ciclare su tutti i possibili iperonimi di synset_concetto_corrente_associato_a_w1
                #partendo dai primi iperonimi inseriti nella pila nel passo iniziale, mentre con il secondo faccio la stessa cosa ma questa volta per il synset_concetto_corrente_associato_a_w2:

                #Primo while:
                while pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1: #continuo fino a quando la pila non è vuota.
                    #1) Il primo passo nel while sarà quello di poppare un elemento dalla pila_1 e memorizzarlo nella lista_1
                    iperonimo_poppato = pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.pop()

                    # print("iperonimo_poppato: ")
                    # print(iperonimo_poppato)

                    # 2) Il secondo passo nel while sarà invece quello di:

                    #   1) Salvare nella lista_1 l'iperonimo appena poppato.
                    #   2) trovare tutti gli iperonimi dell'elemento appena poppato dalla pila_1 e pusharli nella pila_1.
                    lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo_poppato) #1)
                    #2):
                    for iperonimo_poppato_iter in iperonimo_poppato.hypernyms(): #devo ciclare su tutti i possibili iperonimi dell'iperonimo appena poppato
                        pila_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1.append(iperonimo_poppato_iter)


                # Secondo while:
                while pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2: #continuo fino a quando la pila non è vuota.
                    # 1) Il primo passo nel while sarà quello di poppare un elemento dalla pila_2 e memorizzarlo nella lista_2
                    iperonimo_poppato = pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.pop()

                    # 2) Il secondo passo nel while sarà invece quello di:

                    #   1) Salvare nella lista_2 l'iperonimo appena poppato.
                    #   2) trovare tutti gli iperonimi dell'elemento appena poppato dalla pila_1 e pusharli nella pila_2.
                    lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo_poppato) #1)
                    #2)
                    for iperonimo_poppato_iter in iperonimo_poppato.hypernyms():
                        pila_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2.append(iperonimo_poppato_iter)
                ################################################################################################################################################################################


                #A questo punto dopo i due cicli while nella lista_1 avrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w1
                #e nella lista_2 vrò tutti gli iperonimi possibili di synset_concetto_corrente_associato_a_w2.
                print("")
                print("lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1: ")
                print(lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1)
                print("")
                print("lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2: ")
                print(lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2)



                #Adesso quello che devo fare è questo:
                # 0) Devo controllare se nelle due liste c'è qualche synset in comune, qualora fosse così faccio questo:
                # 1) Calcolo la distanza di questo synset dalla radice.
                # 2) Se questa distanza è maggiore di LCS_migliore trovato fino a quel momento allora aggiorno l'LCS_migliore, altrimenti non faccio nulla.


                #Invece di usare le liste puoi usare gli insiemi in modo da non avere duplicati (velocizza algoritmo)
                for synset_lista_1 in lista_1_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w1:#0):
                    for synset_lista_2 in lista_2_contenete_tutti_gli_iperonimi_di_synset_concetto_corrente_associato_a_w2:#0):
                        if(synset_lista_1 == synset_lista_2): #qualora fosse così faccio questo:
                            print("")
                            print("Antenato comune trovato: ", synset_lista_1)
                            print("")
                            distanza_antenato_comune_da_radice_wn = depth(synset_lista_1, 0, 0) #1)
                            print("distanza_antenato_comune_da_radice_wn: ", distanza_antenato_comune_da_radice_wn)
                            if(distanza_antenato_comune_da_radice_wn > LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2): #2)
                                LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 = distanza_antenato_comune_da_radice_wn
                                print("LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2 aggiornato: ", LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2)
                            print("")

                ####################################################################################################################################################


            #Solo adesso posso essere sicuro di aver trovato l'LCS migliore in assoluto per synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2.
            #Quindi posso finalmente calcolare la metrica di Wu & Palmer per synset_concetto_corrente_associato_a_w1 e synset_concetto_corrente_associato_a_w2 correnti
            # (non è ancora detto che sia quella massima):
            # sim(c1,c2) = cs(c1,c2) = 2*depth(LCS) / (depth(c1) + depth(c2)) (Wu & Palmer).
            # print("")
            # print("wn.synset(synset_concetto_corrente_associato_a_w1) PRIMA DI CALCOLARE LA METRICA: ", wn.synset(synset_concetto_corrente_associato_a_w1))
            # print("wn.synset(synset_concetto_corrente_associato_a_w2) PRIMA DI CALCOLARE LA METRICA: ", wn.synset(synset_concetto_corrente_associato_a_w2))
            # print("")

            print("")
            depth_c1 = depth(wn.synset(synset_concetto_corrente_associato_a_w1),0,0)
            depth_c2 = depth(wn.synset(synset_concetto_corrente_associato_a_w2),0,0)
            cs_c1_c2 = (2*LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2) / (depth_c1 + depth_c2)
            print("LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2: ", LCS_migliore_per_synset_concetto_corrente_associato_a_w1_e_per_synset_concetto_corrente_associato_a_w2)
            print("depth_c1: ", depth_c1)
            print("depth_c2: ", depth_c2)
            print("cs_c1_c2 corrente: ", cs_c1_c2)

            #Ora controllo se cs_c1_c2 corrente è maggiore del max, perchè se così fosse allora devo aggiornare il max:
            if(cs_c1_c2 > max):
                max = cs_c1_c2 #aggiorno il max
                print("max aggiornato: ", max)
            print("")
            print("")


    return max #alla fine restituisco il max che sarà proprio il valore di similarità della metrica Wu and Palmer per le due parole w1 e w2 iniziali.






#Carico i dati:
header = ["Word 1", "Word 2", "Risultati"]
data = [] #qui metterò mano mano le coppie con la rispettiva similarità calcolata.
columns_names = True
#considero_solo_i_primi_termini = 0 #dopo questo dovrò toglierlo per poter considerare tutte le coppie di termini.
with open('WordSim353.csv', 'r') as f:
    reader = csv.reader(f)
    # open the file in the write mode
    with open('Risultati Wu & Palmer.csv', 'w', encoding='UTF8', newline='') as file:

        #create the csv writer
        writer = csv.writer(file)
        #write the header
        writer.writerow(header)

        for row in reader:
            if not columns_names:
                #if(considero_solo_i_primi_termini < 1):
                    print(row)
                    w1 = row[0]
                    w2 = row[1]

                    # w1 = "Jerusalem"
                    # w2 = "Israel"

                    print("w1: ", w1)
                    print("w2: ", w2)
                    #considero_solo_i_primi_termini += 1

                    # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w1
                    tutti_i_concetti_associati_a_w1 = concetti_associati_ai_synset_associati_al_termine_di_input(w1)

                    # 2) La seconda cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w2
                    tutti_i_concetti_associati_a_w2 = concetti_associati_ai_synset_associati_al_termine_di_input(w2)

                    print("tutti_i_concetti_associati_a_w1: ", tutti_i_concetti_associati_a_w1)
                    print("tutti_i_concetti_associati_a_w2: ", tutti_i_concetti_associati_a_w2)

                    # 3) La terza cosa da fare è quella di calcolare tra ogni possibile coppia di concetti associati ai
                    # vari synset di w1 e w2 che sono presenti rispettivamente in tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2 il valore sim(c1,c2) ove in questo script
                    # sim(c1,c2) = cs(c1,c2) = 2*depth(LCS) / (depth(s1) + depth(s2)) (Wu & Palmer).

                    # Per fare quello appena detto chiamo la funzione che ho creato per implementare Wu & Palmer) passandogli tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2 in input:
                    sim_Wu_and_Palmer_di_w1_e_w2 = Wu_and_Palmer(tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2)
                    print("sim_Wu_and_Palmer_di_w1_e_w2: ", sim_Wu_and_Palmer_di_w1_e_w2)

                    #Salvo i due termini e il valore di similarità restituito dalla metrica Wu & Palmer per essi all'interno su un file (che poi userò per calcolare i coeff. di Pearson e Spearman).
                    data = [w1,w2,sim_Wu_and_Palmer_di_w1_e_w2]
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



