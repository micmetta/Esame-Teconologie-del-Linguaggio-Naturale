import csv
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn
import re

# DEVI CREARE I CONTESTI Ctx(w) per ogni Frame name, FE e LU,
# quindi w può essere uno dei tre elementi appena citati.
#
#
# DOPODICHE DEVI CREARE IL CONTESTO Ctx(s) per ogni possibile synset s presente
# a cui è associato il termine w.




#IN QUESTA IMPLEMENTAZIONE PER I FRAMES, come contesto (Ctx(w)) ho utilizzato queste informazioni:
# - DEF. frame di appartenenza.



#IN QUESTA IMPLEMENTAZIONE PER I FEs, come contesto (Ctx(w)) ho utilizzato queste informazioni:
# - SOLO LA DEF. del FE corrente.


#IN QUESTA IMPLEMENTAZIONE PER le LUs, come contesto (Ctx(w)) ho utilizzato queste informazioni:
# - Definizione del frame a cui appartiene quella LU corrente.
# - Definizione di tutti i FEs del frame a cui appartiene quella LU corrente.
# - Tutti nomi delle LUs che appartengono al frame a cui appartiene la LU corrente.





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


#Creo il contesto Ctx(w) per ogni frame usando la definizione del frame originale presente su Framenet: (COME CONTESTO DEL FRAME USO SOLAMENTE LA SUA DEFINIZIONE)
def creo_contesto_frame_w(nome_frame_originale):
    frame = fn.frame_by_name(nome_frame_originale)
    #print(frame)
    Ctx_w = frame.definition
    print("Contesto del frame corrente: ", Ctx_w)
    print("")
    Ctx_w = Ctx_w.split(" ")
    print("Contesto del frame corrente dopo primo split: ", Ctx_w)
    print("")

    ########## FACCIO UNA PULIZIA SULLE PAROLE DEL CONTESTO CORRENTE #################################
    try:
        while True:
            Ctx_w.remove("") #rimuovo tutte le parole vuote
    except ValueError:
        pass

    indice_parola = -1
    for parola in Ctx_w:
        indice_parola += 1
        #print("parola: ", parola)

        if(parola[0]=="'"):
            parola_new = parola.replace("'","")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)
            #print(parola)

        if (parola[-1] == "."):
            parola_new = parola.replace(".", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)

        if (parola[-1] == ","):
            parola_new = parola.replace(",", "")
            del Ctx_w[indice_parola]
            Ctx_w.insert(indice_parola, parola_new)

        if(len(parola) >= 2):
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
            if (parola_new[-1] == "."):
                parola_new_2 = parola_new.replace(".", "")
                del Ctx_w[indice_parola]
                Ctx_w.insert(indice_parola, parola_new_2)

        #Ci sono alcune parole come questa: Undesirable_event che sono legate da _, quindi dovresti toglierlo altrimenti quando fai l'overlap non verrà considerata praticamente!!!
        #Quindi qui splitto le parole separate da _ :
        if("_" in parola):
            del Ctx_w[indice_parola] #cancello subito la parola composta
            lista_parole_splittate_da_underscore = parola.split("_")
            indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore = indice_parola
            for parola_in_lista_parole_splittate_da_underscore in lista_parole_splittate_da_underscore:
                Ctx_w.insert(indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore, parola_in_lista_parole_splittate_da_underscore)
                indice_parole_da_aggiungere_dovute_alla_separazione_con_undescore += 1 #incremento la posizione in cui inserire le varie parole che prima erano composte in un'unica parola
                #che aveva l'underscore, quindi ad es per la parola Undesirable_event avrò due parole che saranno Undesirable e event che verranno aggiunte come due parole distinte
                #in Ctx_w

    for parola in Ctx_w:
        print("parola: ", parola)

    ########## FINE PULIZIA SULLE PAROLE DEL CONTESTO CORRENTE #################################

    print("Contesto del frame corrente dopo pulizia: ", Ctx_w)
    print("")


    return Ctx_w



def creo_contesto_frame_element_w(nome_frame_originale_a_cui_appartiene_il_FE_corrente, w): #w = nome_frame_element_corrente

    frame = fn.frame_by_name(nome_frame_originale_a_cui_appartiene_il_FE_corrente)
    Ctx_w = ""
    # print(frame)

    #Adesso il Ctx_w restituito sarà una lista e non più un'unica stringa perchè devo considerare non solo la definizione del frame ma anche quella del frame element w dato in input
    #e anche quella di tutti gli altri FEs del

    # Ctx_w = frame.definition
    # print("Contesto del frame corrente: ", Ctx_w)
    # print("")
    # Ctx_w = Ctx_w.split(" ")
    # print("Contesto del frame corrente dopo primo split: ", Ctx_w)
    # print("")

    #Devo trovare il FE w di input nel frame identificato da nome_frame_originale e prendere la definizione del FE:
    print("Stampo tutti i frame elements del frame chiamato " + nome_frame_originale_a_cui_appartiene_il_FE_corrente + ":")
    FEs = frame.FE.keys()
    for fe in FEs:
        fed = frame.FE[fe]
        #print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))  # stampiamo anche la definizione del fe trovato
        if(fe == w):
            Ctx_w = fed.definition
            print("FE che sto considerando in questo momento: ", fe)
            print("definizione_frame_element_w: ", Ctx_w)


    ########## FACCIO UNA PULIZIA SULLE PAROLE DEL CONTESTO CORRENTE #################################

    Ctx_w = Ctx_w.split(" ")
    print("")
    print("definizione_frame_element_w dopo split: ", Ctx_w)
    print("")

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
            print("parola_new: ", parola_new)
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

    for parola in Ctx_w:
        print("parola: ", parola)

    ########## FINE PULIZIA SULLE PAROLE DEL CONTESTO CORRENTE #################################
    print("")
    print("Contesto del frame element corrente dopo pulizia: ", Ctx_w)
    print("")


    return Ctx_w


def creo_contesto_LU_w(nome_frame_originale_a_cui_appartiene_la_LU_corrente): #w = nome_LU_corrente

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
        #print("FE che sto considerando in questo momento: ", fe)
        #print("definizione_frame_element_w: ", fed.definition)
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
            # print("parola: ", parola)

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





def The_Lesk_Algorithm(word, sentence, tutti_i_sensi_della_parola_da_disambiguare):
    print("word DENTRO LESK: ", word)
    print("sentence DENTRO LESK: ", sentence)
    #tutti_i_sensi_della_parola_di_input = wn.synsets(word)
    print("tutti_i_sensi_della_parola_di_input: ", tutti_i_sensi_della_parola_da_disambiguare)
    best_sense = wn.synsets(word)[0].name() #inizilizzo best_sense con il senso più frequente.
    #best_sense = tutti_i_sensi_della_parola_da_disambiguare[0]

    print("best_sense iniziale: ", best_sense)
    print("")
    print("")

    max_overlap = 0
    context = sentence #inizializzo il contesto con tutte le parole della sentence che in questo caso è Ctx(w) (context è una lista di parole)

    for senso in tutti_i_sensi_della_parola_da_disambiguare:
        print("senso corrente: ", senso)

        #Adesso prendo solamente gli esempi e la glossa del senso corrente:
        lista_esempi = wn.synset(senso).examples() #è una lista di frasi (può anche non essercene neanche una di frase e quindi sarà [])
        print("lista_esempi: ", lista_esempi)
        glossa = wn.synset(senso).definition() #la glossa è una stringa e non sarà mai vuota.
        print("glossa: ", glossa)
        print("")
        print("")
        ###################################################################

        #Ora in aggiunta prendo tutti gli iperonimi del senso corrente:
        lista_iperonimi_senso_corrente = wn.synset(senso).hypernyms()

        #Adesso per ogni iperonimo trovato prendo tutti i suoi esempi e la glossa e li salvo rispettivamente
        # nella lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente e nella lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente:
        lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente = []
        lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente = []
        for iperonimo in lista_iperonimi_senso_corrente:
            esempi_iperonimo_corrente = iperonimo.examples()
            glossa_iperonimo_corrente = iperonimo.definition()
            lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente.append(glossa_iperonimo_corrente) #aggiungo la glossa dell'iperonimo corrente
            for esempio in esempi_iperonimo_corrente: #aggiungo tutti gli esempi dell'iperonimo corrente
                lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente.append(esempio)
        ################################################################

        #Adesso faccio la stessa cosa fatta sopra per gli iperonimi ma ora la faccio per gli iponimi:
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

        print("lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente: ")
        print(lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente)
        print("lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente: ")
        print(lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente)
        print("")
        print("lista_completa_delle_glosse_degli_iponimi_del_senso_corrente: ")
        print(lista_completa_delle_glosse_degli_iponimi_del_senso_corrente)
        print("lista_completa_degli_esempi_degli_iponimi_del_senso_corrente: ")
        print(lista_completa_degli_esempi_degli_iponimi_del_senso_corrente)
        print("")
        print("")

        # Adesso faccio in modo di aggiungere alla lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente la glossa = wn.synset(senso).definition() del senso corrente
        # che ho già trovato all'inizio del ciclo for corrente:
        lista_completa_delle_glosse_degli_iperonimi_del_senso_corrente.append(glossa)

        #faccio la stessa cosa di sopra anche per la lista_completa_delle_glosse_degli_iponimi_del_senso_corrente:
        #lista_completa_delle_glosse_degli_iponimi_del_senso_corrente.append(glossa) #NON SERVE METTERE LA GLOSSA DEL SENSO CORRENTE ANCHE IN QUESTA LISTA PERCHE' ALLA FINE UNIREMO LE DUE
        #LISTE

        ###################################################################################################################################################################################
        #Adesso creo un'unica lista completa in cui considero sia gli esempi degli iperonimi e sia quelli degli iponimi:
        lista_completa_esempi_senso_corrente_iperonimi_e_iponimi = []
        if(lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente != []):
            for esempio in lista_completa_degli_esempi_degli_iperonimi_del_senso_corrente:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)

        if(lista_completa_degli_esempi_degli_iponimi_del_senso_corrente != []):
            for esempio in lista_completa_degli_esempi_degli_iponimi_del_senso_corrente:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)



        #infine aggiungo alla lista_completa_esempi_senso_corrente_iperonimi_e_iponimi anche gli esempi del senso corrente presenti in lista_esempi creata all'inizio di questo ciclo for:
        if (lista_esempi != []):
            for esempio in lista_esempi:
                lista_completa_esempi_senso_corrente_iperonimi_e_iponimi.append(esempio)
        ###################################################################################################################################################################################


        ###################################################################################################################################################################################
        #Faccio la stessa cosa fatta sopra per gli esempi anche per le glosse degli iperonimi e iponimi:
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
        #signature.append(lista_esempi)
        signature.append(lista_completa_esempi_senso_corrente_iperonimi_e_iponimi)
        #signature.append(glossa)
        signature.append(lista_completa_glosse_senso_corrente_iperonimi_e_iponimi) #adesso la signature conterrà la lista di liste degli esempi e la lista di liste delle glosse.
        print("context: ", context)
        print("signature: ", signature)
        overlap = ComputeOverlap(signature, context)
        print("overlap: ", overlap)

        if(overlap > max_overlap):
            max_overlap = overlap
            best_sense = senso

        print("")
        print("")


    return best_sense





def The_Lesk_Algorithm_LU(word, sentence, tutti_i_sensi_della_parola_da_disambiguare): #sentence = Ctx_w

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
            Ctx_w = creo_contesto_frame_w(nome_frame_originale)

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
            Ctx_w = creo_contesto_frame_element_w(nome_frame_originale_a_cui_appartiene_il_fe_corrente, w)

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
            Ctx_w = creo_contesto_LU_w(nome_frame_originale_a_cui_appartiene_la_LU_corrente) #Ctx_w sarà una lista di parole.


            #3) Dopodichè posso iniziare il ciclo per calcolare score(s,w) = |Ctx(w) intersezione Ctx(s)| + 1:
            if (len(insieme_di_synsets_associati_a_w) >= 1):# DEVO VERIFICARE CHE L'INSIEME DI TUTTI I SENSI POSSIBILI NON SIA VUOTO:

                best_sense = The_Lesk_Algorithm_LU(w, Ctx_w, insieme_di_synsets_associati_a_w) #chiamo l'algoritmo di Lesk passandogli il termine w da disambiguare
                #il suo contesto Ctx_w e l'insieme di possibili sensi che possono essere associati a w.
                print("best_sense trovato dall'algoritmo di LESK per la LU -" + w + "- :", best_sense)
                print("")
                print("")

                if(best_sense == synset_LU_gold):
                    num_synsets_predetti_correttamente += 1
                num_synsets_predetti_in_totale += 1


        else:
            columns_names = False

##########################################################################################################################################################################################

print("num_synsets_predetti_correttamente: ", num_synsets_predetti_correttamente)
print("num_synsets_predetti_in_totale: ", num_synsets_predetti_in_totale)
print("Accuratezza finale sistema: ", num_synsets_predetti_correttamente/num_synsets_predetti_in_totale)

############################################     FINE     ##############################################################