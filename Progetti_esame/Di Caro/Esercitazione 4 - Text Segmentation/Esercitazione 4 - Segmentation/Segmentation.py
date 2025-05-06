import random
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from nltk.corpus import wordnet as wn
from operator import itemgetter
import json


def ComputeOverlap(signature, context):

    lista_esempi = signature[0]
    lista_glosse = signature[1]
    # print("")
    # print("")
    # print("")
    # print("")
    # print("")
    # print("lista_esempi INIZIALE in compute Overlap: ", lista_esempi)
    # print("lista_glosse INIZIALE in compute Overlap: ", lista_glosse)
    # print("")
    # print("")


    #Quello che posso fare ora è eliminare le stop words dalla lista_esempi, dalla lista_glosse e dal context:##########

    lista_esempi_dove_ogni_parola_e_un_elemento_della_lista = []
    if (lista_esempi != []):
        for esempio in lista_esempi:
            if(type(esempio) == type("stringa")):
                lista_parole_esempio = esempio.split(" ")
            else:
                lista_parole_esempio = esempio
            # print("lista_parole_esempio: ", lista_parole_esempio)
            for parola_esempio in lista_parole_esempio:
                lista_esempi_dove_ogni_parola_e_un_elemento_della_lista.append(parola_esempio)


    lista_glosse_dove_ogni_parola_e_un_elemento_della_lista = []
    if (lista_glosse != []):
        for glossa in lista_glosse:
            lista_parole_glossa = glossa.split(" ")
            # print("lista_parole_esempio: ", lista_parole_esempio)
            for parola_glossa in lista_parole_glossa:
                lista_glosse_dove_ogni_parola_e_un_elemento_della_lista.append(parola_glossa)


    #elimino le stop words presenti nella lista_esempi:
    lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw = [word for word in lista_esempi_dove_ogni_parola_e_un_elemento_della_lista if word not in stopwords.words('english')]

    #elimino le stop words presenti nella lista_glosse:
    lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw = [word for word in lista_glosse_dove_ogni_parola_e_un_elemento_della_lista if word not in stopwords.words('english')]

    # elimino le stop words presenti nel context:
    context_senza_ssw = [word for word in context if word not in stopwords.words('english')]
    ####################################################################################################################


    overlap = 0

    if(lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw != []):
        for parola_esempio in lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw:
                for parola_context in context_senza_ssw:
                    if(parola_esempio == parola_context):
                        #print("parola_esempio: ", parola_esempio)
                        #print("parola_context: ", parola_context)
                        overlap += 1

    for parola_glossa in lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw:
            for parola_context in context_senza_ssw:
                if(parola_glossa == parola_context):
                    #print("parola_glossa: ", parola_glossa)
                    #print("parola_context: ", parola_context)
                    overlap += 1

    return overlap



def The_Lesk_Algorithm(parola_da_disambiguare, frase):

    #print("lista_parola_pos in The_Lesk_Algorithm: ", lista_parola_pos)
    #parola_da_disambiguare = lista_parola_pos[0]
    #pos = lista_parola_pos[1]

    #print("wn.synsets(parola_da_disambiguare) in The_Lesk_Algorithm: ", wn.synsets(parola_da_disambiguare))
    best_sense = None
    if(wn.synsets(parola_da_disambiguare) != []):

        best_sense = wn.synsets(parola_da_disambiguare)[0] #inizilizzo best_sense con il senso più frequente.
        '''
        print("parola_da_disambiguare DENTRO LESK: ", parola_da_disambiguare)
        print("contesto DENTRO LESK: ", frase)
        print("best_sense iniziale: ", best_sense)
        print("")
        print("")
        '''

        max_overlap = 0
        context = frase #inizializzo il contesto con tutte le parole della sentence che in questo caso è Ctx(w) (context è una lista di parole)
        tutti_i_sensi_della_parola_da_disambiguare = wn.synsets(parola_da_disambiguare)
        '''
        print("tutti_i_sensi_della_parola_da_disambiguare:")
        print(tutti_i_sensi_della_parola_da_disambiguare)
        '''


        for senso in tutti_i_sensi_della_parola_da_disambiguare:

            '''
            print("senso corrente: ", senso)
            '''
            #Adesso prendo solamente gli esempi e la glossa del senso corrente:
            lista_esempi = senso.examples() #è una lista di frasi (può anche non essercene neanche una di frase e quindi sarà [])
            '''
            print("lista_esempi: ", lista_esempi)
            '''
            glossa = senso.definition() #la glossa è una stringa e non sarà mai vuota.
            '''
            print("glossa: ", glossa)
            print("")
            print("")
            '''
            ###################################################################

            #Ora in aggiunta prendo tutti gli iperonimi del senso corrente:
            lista_iperonimi_senso_corrente = senso.hypernyms()

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
            lista_iponimi_senso_corrente = senso.hyponyms()

            lista_completa_degli_esempi_degli_iponimi_del_senso_corrente = []
            lista_completa_delle_glosse_degli_iponimi_del_senso_corrente = []
            for iponimo in lista_iponimi_senso_corrente:
                esempi_iponimo_corrente = iponimo.examples()
                glossa_iponimo_corrente = iponimo.definition()
                lista_completa_delle_glosse_degli_iponimi_del_senso_corrente.append(glossa_iponimo_corrente)
                for esempio in esempi_iponimo_corrente:
                    lista_completa_degli_esempi_degli_iponimi_del_senso_corrente.append(esempio)

            ###############################################################################################

            '''
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
            '''

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


            '''
            print("lista_completa_esempi_senso_corrente_iperonimi_e_iponimi:")
            print(lista_completa_esempi_senso_corrente_iperonimi_e_iponimi)
            print("")
            print("lista_completa_glosse_senso_corrente_iperonimi_e_iponimi: ")
            print(lista_completa_glosse_senso_corrente_iperonimi_e_iponimi)
            print("")
            print("")
            '''

            signature = []
            #signature.append(lista_esempi)
            signature.append(lista_completa_esempi_senso_corrente_iperonimi_e_iponimi)
            #signature.append(glossa)
            signature.append(lista_completa_glosse_senso_corrente_iperonimi_e_iponimi) #adesso la signature conterrà la lista di liste degli esempi e la lista di liste delle glosse.

            # print("context in Lesk: ", context)
            # print("signature in Lesk: ", signature)

            overlap = ComputeOverlap(signature, context)
            '''
            print("overlap: ", overlap)
            '''
            if(overlap > max_overlap):
                max_overlap = overlap
                best_sense = senso
            '''
            print("")
            print("")
            '''

    return best_sense



def rimozione_punteggiatura_da_una_lista(definizione):

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~\n'''
    nuova_definizione = []
    for i in range(0, len(definizione)):
        parola_corrente = ""
        for c in definizione[i]:  # per ogni carattere della parola corrente
            non_aggiungere_carattere = False
            for el in punc:
                if el == c:
                    non_aggiungere_carattere = True
            if not non_aggiungere_carattere:
                parola_corrente = parola_corrente + str(c)

        nuova_definizione.append(parola_corrente)

    return nuova_definizione



def rimozione_stringa_vuota_da_una_lista(definizione):
    # print("definizione in rimozione_stringa_vuota_da_una_lista:")
    # print(definizione)

    # nuova_lista_di_definizione = []
    #esempio di lista_di_definizioni:  ['negative', 'emotion', '']
    for parola in definizione:
        if(parola == ""):
            definizione.remove('')
    # nuova_lista_di_definizione.append(definizione)

    return definizione



def eliminazione_duplicati(lista_minimi_locali_suddivisi_per_cluster):
    nuova_lista_minimi_locali_suddivisi_per_cluster = []
    for lista_minimi_locali_cluster_corrente in lista_minimi_locali_suddivisi_per_cluster:
        nuova_lista_minimi_locali_cluster_corrente = []
        for i in range(0, len(lista_minimi_locali_cluster_corrente)):
            if(lista_minimi_locali_cluster_corrente[i] not in nuova_lista_minimi_locali_cluster_corrente):
                nuova_lista_minimi_locali_cluster_corrente.append(lista_minimi_locali_cluster_corrente[i])

        nuova_lista_minimi_locali_suddivisi_per_cluster.append(nuova_lista_minimi_locali_cluster_corrente)

    return nuova_lista_minimi_locali_suddivisi_per_cluster



#esempio di lista_coppie_posizione_minimo_locale_gia_considerati: [[2, 0.022222222222222223], [23, 0.047619047619047616], [13, 0.0], [2, 0.027777]]
def eliminazione_duplicati_da_una_lista_di_liste(lista_coppie_posizione_minimo_locale_gia_considerati):
    nuova_lista_coppie_posizione_minimo_locale_gia_considerati = []

    for coppia in lista_coppie_posizione_minimo_locale_gia_considerati:
        posizione_barra = coppia[0]
        no_aggiunta = False

        for i in range(0, len(nuova_lista_coppie_posizione_minimo_locale_gia_considerati)):
            if(nuova_lista_coppie_posizione_minimo_locale_gia_considerati[i][0] == posizione_barra):
                no_aggiunta = True

        if not no_aggiunta:
            nuova_lista_coppie_posizione_minimo_locale_gia_considerati.append(coppia)


    return nuova_lista_coppie_posizione_minimo_locale_gia_considerati




def get_frasi_a_coppie(lista_frasi_documento):
    lista_coppie_di_frasi = []
    for i in range(0, len(lista_frasi_documento)):
        coppia_frasi_correnti = []
        if(i < len(lista_frasi_documento)-1): #per essere sicuro di non uscire fuori dalla lista_frasi_documento
            coppia_frasi_correnti.append(lista_frasi_documento[i])
            coppia_frasi_correnti.append(lista_frasi_documento[i+1])

            lista_coppie_di_frasi.append(coppia_frasi_correnti)

    return lista_coppie_di_frasi



def get_frasi_a_triplette(cluster):
    lista_triplette_di_frasi = []
    for i in range(0, len(cluster)):
        tripletta_frasi_correnti = []
        if (i == 0):
            tripletta_frasi_correnti.append(cluster[0])
            tripletta_frasi_correnti.append(cluster[1])
            tripletta_frasi_correnti.append(cluster[2])

            lista_triplette_di_frasi.append(tripletta_frasi_correnti)


        elif(i < len(cluster)-2):  # per essere sicuro di non uscire fuori dalla lista
            tripletta_frasi_correnti.append(cluster[i])
            tripletta_frasi_correnti.append(cluster[i+1])
            tripletta_frasi_correnti.append(cluster[i+2])

            lista_triplette_di_frasi.append(tripletta_frasi_correnti)

    return lista_triplette_di_frasi




def overlap_tra_frasi(frase1, frase2):

    # print("frase1: ", frase1)
    # print("frase2: ", frase2)
    frase1 = frase1.split(" ")
    frase2 = frase2.split(" ")

    # print("frase1 dopo lo split: ", frase1)
    # print("frase2 dopo lo split: ", frase2)

    #rimuovo la punteggiatura e le stringhe vuote dalle due frasi:
    frase1 = rimozione_punteggiatura_da_una_lista(frase1)
    frase2 = rimozione_punteggiatura_da_una_lista(frase2)

    frase1 = rimozione_stringa_vuota_da_una_lista(frase1)
    frase2 = rimozione_stringa_vuota_da_una_lista(frase2)
    ##############################################################

    #elimino le stop words dalle due frasi:
    frase1 = [word for word in frase1 if word.lower() not in stopwords.words('english')]
    frase2 = [word for word in frase2 if word.lower() not in stopwords.words('english')]
    ######################################

    #lemmatizzo tutte le parole delle due frasi:
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(frase1)):
        # print("nuovo_esempio[i]: ", nuovo_esempio[i])
        frase1[i] = lemmatizer.lemmatize(frase1[i].lower())

    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(frase2)):
        # print("nuovo_esempio[i]: ", nuovo_esempio[i])
        frase2[i] = lemmatizer.lemmatize(frase2[i].lower())
    ############################################

    # print("frase1 dopo pre-processing: ", frase1)
    # print("frase2 dopo pre-processing: ", frase2)


    ##############################################################################################################################################################################
    #Per ogni frase faccio questo:
        # - Per ciascun lemma della frase:
            # - mi collego a WN e prendo tutto l'insieme di synset ad esso associato (qualora non esistessa vado al lemma successivo)
            # - applico la WSD usando come contesto del lemma corrente tutta la frase in cui esso si trova.
            # - una volta ottenuto il miglior synset per il lemma corrente prendo tutti i lemmi di questo synset, la definizione e tutti gli esempi (qualora ci fossero)
            # e li inserisco nella frase corrente (in realtà per favorire ancora meglio l'overlap ho considerato anche tutti gli iperonimi e iponimi del synset corrente).
    #Tutto questo lo faccio per cercare di favorire l'overlap lessicale tra le frasi.



    ##############################################################################################################################################################################
    #Frase 1:
    # print("")
    # print("")
    # print("frase1 PRIMA:", frase1)
    frase1_finale = []
    for lemma in frase1:
        best_synset_per_lemma_corrente = The_Lesk_Algorithm(lemma, frase1)
        # print("lemma corrente: ", lemma)
        # print("best_synset_per_lemma_corrente dopo aver applicato Lesk: ", best_synset_per_lemma_corrente)

        if(best_synset_per_lemma_corrente is not None):

            lista_lemmi_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.lemmas()
            lista_definizione_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.definition().split(" ")
            lista_esempi_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.examples()

            # print("lista_lemmi_best_synset_per_lemma_corrente:", lista_lemmi_best_synset_per_lemma_corrente)
            # print("lista_definizione_best_synset_per_lemma_corrente:", lista_definizione_best_synset_per_lemma_corrente)
            # print("lista_esempi_best_synset_per_lemma_corrente prima LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
            # print("")

            for lemma_best_synset in lista_lemmi_best_synset_per_lemma_corrente:
                frase1_finale.append(lemma_best_synset.name())

            #elimino le stop words dalla definizione corrente e lemmatizzo tutte le parole e dopodichè l'aggiungo alla frase1:
            lista_definizione_best_synset_per_lemma_corrente = [word for word in lista_definizione_best_synset_per_lemma_corrente if word.lower() not in stopwords.words('english')]
            lemmatizer = WordNetLemmatizer()
            for i in range(0, len(lista_definizione_best_synset_per_lemma_corrente)):
                # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                lista_definizione_best_synset_per_lemma_corrente[i] = lemmatizer.lemmatize(lista_definizione_best_synset_per_lemma_corrente[i].lower())
            for parola in lista_definizione_best_synset_per_lemma_corrente:
                frase1_finale.append(parola)
            #################################################################################################################


            # elimino le stop words per ogni esempio del best synset corrente e lemmatizzo tutte le parole e dopodichè l'aggiungo alla frase1:
            if(lista_esempi_best_synset_per_lemma_corrente != []):
                for i in range(0, len(lista_esempi_best_synset_per_lemma_corrente)):
                    if(type(lista_esempi_best_synset_per_lemma_corrente[i]) == type("stringa")):
                        lista_esempi_best_synset_per_lemma_corrente[i] = [word for word in lista_esempi_best_synset_per_lemma_corrente[i].split(" ") if word.lower() not in stopwords.words('english')]
                    else:
                        lista_esempi_best_synset_per_lemma_corrente[i] = [word for word in lista_esempi_best_synset_per_lemma_corrente[i] if word.lower() not in stopwords.words('english')]


                lemmatizer = WordNetLemmatizer()
                for esempio in lista_esempi_best_synset_per_lemma_corrente:
                    for i in range(0, len(esempio)):
                        esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                #print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
                for lista_esempi in lista_esempi_best_synset_per_lemma_corrente: #lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                    for esempio in lista_esempi:
                        frase1_finale.append(esempio)
            #################################################################################################################


            # Aggiungo per il lemma corrente nella frase 1 anche tutti i lemmi di tutti gli iperonimi del best_synset_per_lemma_corrente:
            for iperonimo in best_synset_per_lemma_corrente.hypernyms():
                #print("iperonimo corrente del lemma corrente: ", iperonimo)
                for lemma_in_iperonimo_corrente in iperonimo.lemmas():
                    #print("lemma_in_iperonimo_corrente: ", lemma_in_iperonimo_corrente.name())
                    frase1_finale.append(lemma_in_iperonimo_corrente.name())

                ####################################################################
                '''
                # - L'aggiunta del codice qui sotto non ha portato i miglioramenti sperati
                #Aggiungo anche la definizione e gli esempi dell'iperonimo corrente:
                #definizione:
                lista_definizione_iperonimo_corrente = iperonimo.definition().split(" ")
                lista_definizione_iperonimo_corrente = [word for word in lista_definizione_iperonimo_corrente if word.lower() not in stopwords.words('english')]
                lemmatizer = WordNetLemmatizer()
                for i in range(0, len(lista_definizione_iperonimo_corrente)):
                    # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                    lista_definizione_iperonimo_corrente[i] = lemmatizer.lemmatize(lista_definizione_iperonimo_corrente[i].lower())
                for parola in lista_definizione_iperonimo_corrente:
                    frase1_finale.append(parola)

                #esempi (se ci sono):
                lista_esempi_iperonimo_corrente = iperonimo.examples()
                if (lista_esempi_iperonimo_corrente != []):
                    for i in range(0, len(lista_esempi_iperonimo_corrente)):
                        if (type(lista_esempi_iperonimo_corrente[i]) == type("stringa")):
                            lista_esempi_iperonimo_corrente[i] = [word for word in lista_esempi_iperonimo_corrente[i].split(" ") if word.lower() not in stopwords.words('english')]
                        else:
                            lista_esempi_iperonimo_corrente[i] = [word for word in lista_esempi_iperonimo_corrente[i] if word.lower() not in stopwords.words('english')]

                    lemmatizer = WordNetLemmatizer()
                    for esempio in lista_esempi_iperonimo_corrente:
                        for i in range(0, len(esempio)):
                            esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                    # print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
                    for lista_esempi in lista_esempi_iperonimo_corrente:  # lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                        for esempio in lista_esempi:
                            frase1_finale.append(esempio)
                '''
                ####################################################################


            ############################################################################################################################
            # Aggiungo per il lemma corrente nella frase 1 anche tutti i lemmi di tutti gli iponimi del best_synset_per_lemma_corrente:
            for iponimo in best_synset_per_lemma_corrente.hyponyms():
                #print("iponimo corrente del lemma corrente: ", iponimo)
                for lemma_in_iponimo_corrente in iponimo.lemmas():
                    #print("lemma_in_iponimo_corrente: ", lemma_in_iponimo_corrente.name())
                    frase1_finale.append(lemma_in_iponimo_corrente.name())

                ####################################################################
                '''
                # - L'aggiunta del codice qui sotto non ha portato i miglioramenti sperati
                # Aggiungo anche la definizione e gli esempi dell'iponimo corrente:
                # definizione:
                lista_definizione_iponimo_corrente = iponimo.definition().split(" ")
                lista_definizione_iponimo_corrente = [word for word in lista_definizione_iponimo_corrente if word.lower() not in stopwords.words('english')]
                lemmatizer = WordNetLemmatizer()
                for i in range(0, len(lista_definizione_iponimo_corrente)):
                    # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                    lista_definizione_iponimo_corrente[i] = lemmatizer.lemmatize(lista_definizione_iponimo_corrente[i].lower())
                for parola in lista_definizione_iponimo_corrente:
                    frase1_finale.append(parola)

                # esempi (se ci sono):
                lista_esempi_iponimo_corrente = iponimo.examples()
                if (lista_esempi_iponimo_corrente != []):
                    for i in range(0, len(lista_esempi_iponimo_corrente)):
                        if (type(lista_esempi_iponimo_corrente[i]) == type("stringa")):
                            lista_esempi_iponimo_corrente[i] = [word for word in lista_esempi_iponimo_corrente[i].split(" ") if word.lower() not in stopwords.words('english')]
                        else:
                            lista_esempi_iponimo_corrente[i] = [word for word in lista_esempi_iponimo_corrente[i] if word.lower() not in stopwords.words('english')]

                    lemmatizer = WordNetLemmatizer()
                    for esempio in lista_esempi_iponimo_corrente:
                        for i in range(0, len(esempio)):
                            esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                    # print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
                    for lista_esempi in lista_esempi_iponimo_corrente:  # lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                        for esempio in lista_esempi:
                            frase1_finale.append(esempio)
                '''
                ####################################################################

            ############################################################################################################################



    frase1_finale = rimozione_punteggiatura_da_una_lista(frase1_finale)
    # print("frase1_finale DOPO:", frase1_finale)
    # print("")
    # print("")
    # print("")
    ##############################################################################################################################################################################


    ##############################################################################################################################################################################
    # Frase 2:
    # print("")
    # print("")
    # print("frase2 PRIMA:", frase2)
    frase2_finale = []
    for lemma in frase2:

        best_synset_per_lemma_corrente = The_Lesk_Algorithm(lemma, frase2)
        # print("lemma corrente: ", lemma)
        # print("best_synset_per_lemma_corrente dopo aver applicato Lesk: ", best_synset_per_lemma_corrente)

        if (best_synset_per_lemma_corrente is not None):

            lista_lemmi_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.lemmas()
            lista_definizione_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.definition().split(" ")
            lista_esempi_best_synset_per_lemma_corrente = best_synset_per_lemma_corrente.examples()

            # print("lista_lemmi_best_synset_per_lemma_corrente:", lista_lemmi_best_synset_per_lemma_corrente)
            # print("lista_definizione_best_synset_per_lemma_corrente:",lista_definizione_best_synset_per_lemma_corrente)
            # print("lista_esempi_best_synset_per_lemma_corrente prima LEMMATIZZAZIONE:",lista_esempi_best_synset_per_lemma_corrente)

            for lemma_best_synset in lista_lemmi_best_synset_per_lemma_corrente:
                frase2_finale.append(lemma_best_synset.name())

            # elimino le stop words dalla definizione corrente e lemmatizzo tutte le parole e dopodichè l'aggiungo alla frase2:
            lista_definizione_best_synset_per_lemma_corrente = [word for word in lista_definizione_best_synset_per_lemma_corrente if word.lower() not in stopwords.words('english')]
            lemmatizer = WordNetLemmatizer()
            for i in range(0, len(lista_definizione_best_synset_per_lemma_corrente)):
                # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                lista_definizione_best_synset_per_lemma_corrente[i] = lemmatizer.lemmatize(lista_definizione_best_synset_per_lemma_corrente[i].lower())
            for parola in lista_definizione_best_synset_per_lemma_corrente:
                frase2_finale.append(parola)
            #################################################################################################################

            # elimino le stop words per ogni esempio del best synset corrente e lemmatizzo tutte le parole e dopodichè l'aggiungo alla frase2:
            if (lista_esempi_best_synset_per_lemma_corrente != []):
                for i in range(0, len(lista_esempi_best_synset_per_lemma_corrente)):
                    if (type(lista_esempi_best_synset_per_lemma_corrente[i]) == type("stringa")):
                        lista_esempi_best_synset_per_lemma_corrente[i] = [word for word in lista_esempi_best_synset_per_lemma_corrente[i].split(" ") if word.lower() not in stopwords.words('english')]
                    else:
                        lista_esempi_best_synset_per_lemma_corrente[i] = [word for word in lista_esempi_best_synset_per_lemma_corrente[i] if word.lower() not in stopwords.words('english')]

                lemmatizer = WordNetLemmatizer()
                for esempio in lista_esempi_best_synset_per_lemma_corrente:
                    for i in range(0, len(esempio)):
                        esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                #print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:",lista_esempi_best_synset_per_lemma_corrente)
                for lista_esempi in lista_esempi_best_synset_per_lemma_corrente:  # lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                    for esempio in lista_esempi:
                        frase2_finale.append(esempio)
            #################################################################################################################


            # Aggiungo per il lemma corrente nella frase 2 anche tutti i lemmi di tutti gli iperonimi del best_synset_per_lemma_corrente:
            for iperonimo in best_synset_per_lemma_corrente.hypernyms():
                #print("iperonimo corrente del lemma corrente: ", iperonimo)
                for lemma_in_iperonimo_corrente in iperonimo.lemmas():
                    #print("lemma_in_iperonimo_corrente: ", lemma_in_iperonimo_corrente.name())
                    frase2_finale.append(lemma_in_iperonimo_corrente.name())

                ####################################################################
                '''
                # - L'aggiunta del codice qui sotto non ha portato i miglioramenti sperati
                # Aggiungo anche la definizione e gli esempi dell'iperonimo corrente:
                # definizione:
                lista_definizione_iperonimo_corrente = iperonimo.definition().split(" ")
                lista_definizione_iperonimo_corrente = [word for word in lista_definizione_iperonimo_corrente if
                                                            word.lower() not in stopwords.words('english')]
                lemmatizer = WordNetLemmatizer()
                for i in range(0, len(lista_definizione_iperonimo_corrente)):
                    # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                    lista_definizione_iperonimo_corrente[i] = lemmatizer.lemmatize(lista_definizione_iperonimo_corrente[i].lower())
                for parola in lista_definizione_iperonimo_corrente:
                    frase2_finale.append(parola)

                # esempi (se ci sono):
                lista_esempi_iperonimo_corrente = iperonimo.examples()
                if (lista_esempi_iperonimo_corrente != []):
                    for i in range(0, len(lista_esempi_iperonimo_corrente)):
                        if (type(lista_esempi_iperonimo_corrente[i]) == type("stringa")):
                            lista_esempi_iperonimo_corrente[i] = [word for word in
                                                                      lista_esempi_iperonimo_corrente[i].split(" ") if
                                                                      word.lower() not in stopwords.words('english')]
                        else:
                            lista_esempi_iperonimo_corrente[i] = [word for word in
                                                                      lista_esempi_iperonimo_corrente[i] if
                                                                      word.lower() not in stopwords.words('english')]

                    lemmatizer = WordNetLemmatizer()
                    for esempio in lista_esempi_iperonimo_corrente:
                        for i in range(0, len(esempio)):
                            esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                    # print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
                    for lista_esempi in lista_esempi_iperonimo_corrente:  # lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                        for esempio in lista_esempi:
                            frase2_finale.append(esempio)
                '''
                ######################################################################

            ############################################################################################################################

            # Aggiungo per il lemma corrente nella frase 2 anche tutti i lemmi di tutti gli iponimi del best_synset_per_lemma_corrente:
            for iponimo in best_synset_per_lemma_corrente.hyponyms():
                #print("iponimo corrente del lemma corrente: ", iponimo)
                for lemma_in_iponimo_corrente in iponimo.lemmas():
                    #print("lemma_in_iponimo_corrente: ", lemma_in_iponimo_corrente.name())
                    frase2_finale.append(lemma_in_iponimo_corrente.name())

                ####################################################################
                # Aggiungo anche la definizione e gli esempi dell'iponimo corrente:
                '''
                # - L'aggiunta del codice qui sotto non ha portato i miglioramenti sperati
                # definizione:
                lista_definizione_iponimo_corrente = iponimo.definition().split(" ")
                lista_definizione_iponimo_corrente = [word for word in lista_definizione_iponimo_corrente if
                                                          word.lower() not in stopwords.words('english')]
                lemmatizer = WordNetLemmatizer()
                for i in range(0, len(lista_definizione_iponimo_corrente)):
                    # print("nuovo_esempio[i]: ", nuovo_esempio[i])
                    lista_definizione_iponimo_corrente[i] = lemmatizer.lemmatize(lista_definizione_iponimo_corrente[i].lower())
                for parola in lista_definizione_iponimo_corrente:
                    frase2_finale.append(parola)

                # esempi (se ci sono):
                lista_esempi_iponimo_corrente = iponimo.examples()
                if (lista_esempi_iponimo_corrente != []):
                    for i in range(0, len(lista_esempi_iponimo_corrente)):
                        if (type(lista_esempi_iponimo_corrente[i]) == type("stringa")):
                            lista_esempi_iponimo_corrente[i] = [word for word in
                                                                    lista_esempi_iponimo_corrente[i].split(" ") if
                                                                    word.lower() not in stopwords.words('english')]
                        else:
                            lista_esempi_iponimo_corrente[i] = [word for word in lista_esempi_iponimo_corrente[i] if
                                                                    word.lower() not in stopwords.words('english')]

                    lemmatizer = WordNetLemmatizer()
                    for esempio in lista_esempi_iponimo_corrente:
                        for i in range(0, len(esempio)):
                            esempio[i] = lemmatizer.lemmatize(esempio[i].lower())

                    # print("lista_esempi_best_synset_per_lemma_corrente dopo LEMMATIZZAZIONE:", lista_esempi_best_synset_per_lemma_corrente)
                    for lista_esempi in lista_esempi_iponimo_corrente:  # lista_esempi_best_synset_per_lemma_corrente è una lista di liste per questo devo fare 2 cicli for
                        for esempio in lista_esempi:
                            frase2_finale.append(esempio)
                    ####################################################################
                '''


            ############################################################################################################################



    frase2_finale = rimozione_punteggiatura_da_una_lista(frase2_finale)
    # print("frase2_finale DOPO:", frase2_finale)
    # print("")
    # print("")
    # print("")

    ##############################################################################################################################################################################


    #Trasformo le due frasi in due insiemi in modo tale da poter calcolare la loro intersezione in maniera corretta:
    frase1_finale = set(frase1_finale)
    frase2_finale = set(frase2_finale)
    ###############################################################################################################

    parole_comuni = frase1_finale.intersection(frase2_finale) #prendo le parole comuni (qualora ci fosse una parola presente più volte in una frase questa verrebbe considerata comunque una sola volta)
    num_parole_comuni = len(parole_comuni)
    if(len(frase1_finale) >= len(frase2_finale)):
        denominatore = len(frase2_finale)
    else:
        denominatore = len(frase1_finale)

    print("Overlap lessicale tra le parole correnti (alla fine di overlap tra frasi): ", num_parole_comuni/denominatore)
    print("")
    print("")


    return num_parole_comuni/denominatore





def eliminizaione_coppia_di_input(copia_lista_minimi_locali_per_cluster_corrente, coppia_che_sto_considerando_adesso):
    nuova_copia_lista_minimi_locali_per_cluster_corrente = []
    for coppia in copia_lista_minimi_locali_per_cluster_corrente:
        if(coppia != coppia_che_sto_considerando_adesso):
            nuova_copia_lista_minimi_locali_per_cluster_corrente.append(coppia)

    return nuova_copia_lista_minimi_locali_per_cluster_corrente




#esempio di lista_coppie_posizione_minimo_locale_gia_considerati: [[2, 0.022222222222222223], [23, 0.047619047619047616], [13, 0.0]]
def ordinamento_lista_di_lista(lista_coppie_posizione_minimo_locale_gia_considerati):

    lista_coppie_posizione_minimo_locale_gia_considerati = eliminazione_duplicati_da_una_lista_di_liste(lista_coppie_posizione_minimo_locale_gia_considerati)
    print("lista_coppie_posizione_minimo_locale_gia_considerati (DEVE ESSERE SENZA DUPLICATI) in ordinamento_lista_di_lista: ", lista_coppie_posizione_minimo_locale_gia_considerati)

    num_elementi_lista_coppie_posizione_minimo_locale_gia_considerati = len(lista_coppie_posizione_minimo_locale_gia_considerati)
    lista_coppie_posizione_minimo_locale_gia_considerati_ordinata = []
    cicla = True

    while(cicla):
        posizione_minima_finora = np.inf
        coppia_da_inserire = []
        for coppia in lista_coppie_posizione_minimo_locale_gia_considerati:
            posizione_barra_coppia_corrente = coppia[0]
            if((posizione_barra_coppia_corrente < posizione_minima_finora) and (coppia not in lista_coppie_posizione_minimo_locale_gia_considerati_ordinata)):
                coppia_da_inserire = coppia
                posizione_minima_finora = posizione_barra_coppia_corrente


        lista_coppie_posizione_minimo_locale_gia_considerati_ordinata.append(coppia_da_inserire)
        lista_coppie_posizione_minimo_locale_gia_considerati.remove(coppia_da_inserire)

        if(len(lista_coppie_posizione_minimo_locale_gia_considerati_ordinata) != num_elementi_lista_coppie_posizione_minimo_locale_gia_considerati):
            cicla = True
        else:
            cicla = False #vuol dire che ho ordinato tutti gli elementi


    return lista_coppie_posizione_minimo_locale_gia_considerati_ordinata




def get_valori_minimi_locali_ad_n_alla_volta(lista_primi_num_max_min_locali_considerati, n):


    lista_di_liste_barre_possibili = []
    for coppia_corrente in lista_primi_num_max_min_locali_considerati:
        for numero_barra in range(0, n-1): #c'è n-1 perchè la posizione di una barra la considero già con coppia_corrente.
            for coppia_temp in lista_primi_num_max_min_locali_considerati:
                if (coppia_corrente != coppia_temp):
                    if(coppia_corrente[0] not in lista_di_liste_barre_possibili and coppia_temp[0] not in lista_di_liste_barre_possibili):
                        lista_coppia_posizioni = []
                        lista_coppia_posizioni.append(coppia_corrente[0])
                        lista_coppia_posizioni.append(coppia_temp[0])
                        lista_di_liste_barre_possibili.append(lista_coppia_posizioni)

    print("")
    print("lista_di_liste_barre_possibili DOPO LA PRIMA PARTE: ", lista_di_liste_barre_possibili)
    print("")


    for coppia_corrente in lista_primi_num_max_min_locali_considerati:
        for numero_barra in range(0, n-1): #c'è n-1 perchè la posizione di una barra la considero già con coppia_corrente.
            for coppia_temp in lista_primi_num_max_min_locali_considerati:
                if (coppia_corrente != coppia_temp):
                    if (coppia_corrente[0] not in lista_di_liste_barre_possibili and coppia_temp[0] not in lista_di_liste_barre_possibili):
                        lista_coppia_posizioni = []
                        lista_coppia_posizioni.append(coppia_corrente[0])
                        lista_coppia_posizioni.append(coppia_temp[0])
                        lista_di_liste_barre_possibili.append(lista_coppia_posizioni)


    #mantengo solo le coppie (che potrebbero essere anche più di due perchè dipende dal numero di barre iniziali) che sono ordinate:
    lista_di_liste_barre_possibili_senza_coppie_inverse = []
    for coppia_posizioni in lista_di_liste_barre_possibili:
        if (coppia_posizioni == sorted(coppia_posizioni)):
            lista_di_liste_barre_possibili_senza_coppie_inverse.append(coppia_posizioni)
    ################################################################################################################################


    ####################################################################################
    #elimino eventuali duplicati
    nuova_lista_di_liste_barre_possibili_senza_coppie_inverse = []
    for coppia_posizioni_corrente in lista_di_liste_barre_possibili_senza_coppie_inverse:
        if(coppia_posizioni_corrente not in nuova_lista_di_liste_barre_possibili_senza_coppie_inverse):
            nuova_lista_di_liste_barre_possibili_senza_coppie_inverse.append(coppia_posizioni_corrente)

    lista_di_liste_barre_possibili_senza_coppie_inverse = nuova_lista_di_liste_barre_possibili_senza_coppie_inverse
    ####################################################################################



    print("lista_di_liste_barre_possibili_senza_coppie_inverse FINALE: ", lista_di_liste_barre_possibili_senza_coppie_inverse)
    print("")
    print("")



    return lista_di_liste_barre_possibili_senza_coppie_inverse




#La funzione di sotto mi permette di consideroare solamente i primi num_max_min_locali minimi locali più piccoli.
def get_primi_num_max_min_locali(lista_minimi_locali_suddivisi_per_cluster, num_max_min_locali):

    lista_completa_coppie_posizione_minimi_locali_ordinati = []
    for lista_minimi_locali_cluster_corrente in lista_minimi_locali_suddivisi_per_cluster:
        for coppia_posizione_minimo in lista_minimi_locali_cluster_corrente:
            lista_completa_coppie_posizione_minimi_locali_ordinati.append(coppia_posizione_minimo)

    # adesso ordino la lista_completa_coppie_posizione_minimi_locali_ordinati in base ai valori dei minimi (e non alle posizioni delle barre9:
    lista_completa_coppie_posizione_minimi_locali_ordinati = sorted(
        lista_completa_coppie_posizione_minimi_locali_ordinati, key=itemgetter(1))
    print("")
    print("")
    print("lista_completa_coppie_posizione_minimi_locali_ordinati:")
    print(lista_completa_coppie_posizione_minimi_locali_ordinati)

    lista_primi_num_max_min_locali_considerati = []
    for coppia_posizione_minimo in lista_completa_coppie_posizione_minimi_locali_ordinati:
        lista_primi_num_max_min_locali_considerati.append(coppia_posizione_minimo)
        if (len(lista_primi_num_max_min_locali_considerati) == num_max_min_locali): #appena raggiungo il num_max_min_locali esco dal for e la funzione restituisce lista_primi_num_max_min_locali_considerati
            break
    #####################################################################################################################################################


    return lista_primi_num_max_min_locali_considerati



def trova_barre_migliori(lista_primi_num_max_min_locali_considerati, n, num_frasi_documento, lista_frasi_documento):


    print("lista_primi_num_max_min_locali_considerati in trova_barre_migliori:")
    print(lista_primi_num_max_min_locali_considerati)
    print("")

    #Adesso posso considerare i minimi locali rimasti (che sono presenti in lista_primi_num_max_min_locali_considerati) ad n alla volta dove n = num. di barre.
    if(n>1):
        lista_di_minimi_locali_presi_ad_n_alla_volta = get_valori_minimi_locali_ad_n_alla_volta(lista_primi_num_max_min_locali_considerati, n)
    else:
        lista_di_minimi_locali_presi_ad_n_alla_volta = []
        #vuol dire che ho solo una barra da dover posizionare:
        for coppia in lista_primi_num_max_min_locali_considerati:
            lista = []
            lista.append(coppia[0])
            lista_di_minimi_locali_presi_ad_n_alla_volta.append(lista)

    print("lista_di_minimi_locali_presi_ad_n_alla_volta: ", lista_di_minimi_locali_presi_ad_n_alla_volta)
    print("")
    print("")

    coesione_media_clusters_migliore = 0
    posizioni_barre_migliori = []

    for posizioni_barre_correnti in lista_di_minimi_locali_presi_ad_n_alla_volta:

        print("")
        print("")
        # print("posizioni_barre_correnti considerate adesso: ", posizioni_barre_correnti)
        posizioni_barre_correnti.insert(0, 0) #inserisco lo 0 in prima posizione nella lista_posizioni_linee_di_separazione per avere ad esempio questa lista di barre [0, 5, 27]
        print("posizioni_barre_correnti considerate adesso: ", posizioni_barre_correnti)
        # ottengo i clusters secondo le posizioni delle barre correnti
        clusters_correnti = get_clusters(posizioni_barre_correnti, n, num_frasi_documento, lista_frasi_documento)

        # ottengo l'overlap lessicale tra ogni coppia di frasi di ogni cluster e la coesione dei vari clusters
        lista_coesione_dei_vari_clusters_correnti, overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster = get_overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster(clusters_correnti)

        #coesione_media_clusters_correnti = np.mean(lista_coesione_dei_vari_clusters_correnti)
        coesione_media_clusters_correnti = np.mean(lista_coesione_dei_vari_clusters_correnti)
        print("coesione_media_clusters_correnti: ", coesione_media_clusters_correnti)

        if(coesione_media_clusters_correnti > coesione_media_clusters_migliore):
            #faccio l'aggiornamento delle barre perchè con queste barre la coesione media dei clusters migliora:
            coesione_media_clusters_migliore = coesione_media_clusters_correnti
            posizioni_barre_migliori = posizioni_barre_correnti
            print("posizioni_barre_migliori TROVATE FINO AD ORA: ", posizioni_barre_migliori)
            print("coesione_media_clusters_migliore FINO AD ORA: ", coesione_media_clusters_migliore)
            print("")
            print("")


    return posizioni_barre_migliori, coesione_media_clusters_migliore



def get_clusters(lista_posizioni_linee_di_separazione, num_linee_di_separazione, num_frasi_documento, lista_frasi_documento):

    #lista_posizioni_linee_di_separazione.insert(0, 0) #inserisco lo 0 in prima posizione nella lista_posizioni_linee_di_separazione per avere ad esempio questa lista di barre [0, 5, 27]
    #print("lista_posizioni_linee_di_separazione: ", lista_posizioni_linee_di_separazione)


    ########    mi serve per risolvere il problema di quando non ho almeno due frasi in un cluster  ########
    for i in range(1, num_linee_di_separazione + 1):

        if ((lista_posizioni_linee_di_separazione[i] - lista_posizioni_linee_di_separazione[i - 1]) == 1):
            lista_posizioni_linee_di_separazione[i] = lista_posizioni_linee_di_separazione[i] + 1  # sposto la barra i-esima di una posizione in modo tale da essere sicuro di poter avere almeno
            # due frasi in ogni cluster.
            print("barre aggiustate primo if: ", lista_posizioni_linee_di_separazione)

        if ((lista_posizioni_linee_di_separazione[i] - lista_posizioni_linee_di_separazione[i - 1]) == 0):
            lista_posizioni_linee_di_separazione[i] = lista_posizioni_linee_di_separazione[i] + 2  # sposto la barra i-esima di due posizioni in modo tale da essere sicuro di poter avere almeno
            # due frasi in ogni cluster.
            print("barre aggiustate secondo if: ", lista_posizioni_linee_di_separazione)

        if (i == num_linee_di_separazione - 1):

            if ((lista_posizioni_linee_di_separazione[i] == num_frasi_documento - 1)):
                lista_posizioni_linee_di_separazione[i] = lista_posizioni_linee_di_separazione[i] - 1  # sposto l'ultima barra un pò prima perchè altrimenti nell'ultimo cluster avrei
                # solamente una frase.
                print("barre aggiustate terzo if: ", lista_posizioni_linee_di_separazione)

        if ((lista_posizioni_linee_di_separazione[i] - lista_posizioni_linee_di_separazione[i - 1]) < 0):
            differenza = (-1 * (lista_posizioni_linee_di_separazione[i] - lista_posizioni_linee_di_separazione[i - 1]))  # ad es 1 vuol dire che nella barra precedente c'è una sola frase in più
            # per essere sicuro di avere almeno 2 frasi in ogni cluster la barra in posizione i deve essere spostata del numero di posizioni risultanti dall'equazione di sotto:
            lista_posizioni_linee_di_separazione[i] = lista_posizioni_linee_di_separazione[i] + differenza + (2 - lista_posizioni_linee_di_separazione[i] + differenza)
    ################################################################################################################



    # Passo 2) Adesso per ogni gruppo di frasi presenti in ogni cluster calcolo la loro coesione andando a calcolare la sovrapposizione lessicale tra tutte le parole presenti in ogni
    # frase di quel cluster.
    # Per farlo faccio questo:
    # 2.1) Individuo i clusters correnti secondo la suddivisione migliore trovata fino a quel momento.
    # 2.2) Per ogni coppia di frasi sequenziali (in maniera sequenziale, ovvero le prime due frasi presenti nel cluster corrente,
    # dopo per la seconda e la terza, dopo per la terza e la quarta, e così via..) calcolo l'overlap lessicale e aggiungo ad una variabile somma l'overlap
    # tra ogni coppia, in modo tale che alla fine, dopo che avrò considerato tutte le coppie sequenziali, potrò ottenere un valore medio di overlap per il cluster corrente
    # che sarà proprio il valore di coesione di quel cluster.
    # 2.3)  Dopodichè

    if(num_linee_di_separazione > 1):

        # 2.1):
        # with open(path_documento, 'r') as documento:
        clusters_correnti = []
        for i in range(0, len(lista_posizioni_linee_di_separazione)):
            cluster_corrente = []  # sarà una lista di liste dove ogni lista interna è una coppia_frase_indice_frase_nel_documento

            if (i == 0):
                # se entro qui vuol dire che devo selezionare le frasi del primo cluster; esse saranno comprese in questo range: 1 <= frasi_cluster_1 <= lista_posizioni_linee_di_separazione[1]-1:
                # indice_frase_corrente = 1

                for indice_frase in range(0, lista_posizioni_linee_di_separazione[1]):  # 0 e 1                               #c'era lista_posizioni_linee_di_separazione[1]-1
                    coppia_frase_indice_frase_nel_documento = []  # sarà una lista di liste che conterrà la coppia frase - indice di questa frase nel documento

                    coppia_frase_indice_frase_nel_documento.append(lista_frasi_documento[indice_frase])
                    coppia_frase_indice_frase_nel_documento.append(indice_frase)

                    cluster_corrente.append(coppia_frase_indice_frase_nel_documento)

                clusters_correnti.append(cluster_corrente)
                print("cluster_corrente: ")
                print(cluster_corrente)
                print("")
                print("")

            else:
                if (i < len(lista_posizioni_linee_di_separazione) - 1):  # devo accertarmi di non essere ancora arrivato alla fine della lista_posizioni_linee_di_separazione altrimenti
                    # non avrò un estremo destro nella lista perchè sarà il numero max di frasi del documento.
                    for indice_frase in range(0, num_frasi_documento):
                        coppia_frase_indice_frase_nel_documento = []

                        if lista_posizioni_linee_di_separazione[i] <= indice_frase <= lista_posizioni_linee_di_separazione[i + 1] - 1:  # c'era if ((lista_posizioni_linee_di_separazione[i]-1 <= indice_frase <= lista_posizioni_linee_di_separazione[i+1]-2)):
                            coppia_frase_indice_frase_nel_documento.append(lista_frasi_documento[indice_frase])
                            coppia_frase_indice_frase_nel_documento.append(indice_frase)

                            cluster_corrente.append(coppia_frase_indice_frase_nel_documento)

                    clusters_correnti.append(cluster_corrente)
                    print("cluster_corrente: ")
                    print(cluster_corrente)
                    print("")
                    print("")

                else:
                    for indice_frase in range(0, num_frasi_documento):
                        # print("frase: ", frase)                                                               #da 29 a 44
                        if (lista_posizioni_linee_di_separazione[i] <= indice_frase <= num_frasi_documento - 1):  # c'ra if (lista_posizioni_linee_di_separazione[i]-1 <= indice_frase <= num_frasi_documento):
                            coppia_frase_indice_frase_nel_documento = []

                            coppia_frase_indice_frase_nel_documento.append(lista_frasi_documento[indice_frase])
                            coppia_frase_indice_frase_nel_documento.append(indice_frase)

                            cluster_corrente.append(coppia_frase_indice_frase_nel_documento)

                    clusters_correnti.append(cluster_corrente)
                    print("cluster_corrente: ")
                    print(cluster_corrente)
                    print("")
                    print("")

        print("")
        print("")
        print("clusters_correnti:")
        print(clusters_correnti)
        print("")
        print("")
        print("")
        print("")

    else:
        # - Se entro qui vuol dire che devo posizionare solo una barra e considerare solamente 2 clusters:

        clusters_correnti = []
        for i in range(0, len(lista_posizioni_linee_di_separazione)):
            cluster_corrente = []

            if (i == 0):
                # se entro qui vuol dire che devo selezionare le frasi del primo cluster; esse saranno comprese in questo range: 1 <= frasi_cluster_1 <= lista_posizioni_linee_di_separazione[1]-1:
                # indice_frase_corrente = 1

                for indice_frase in range(0, lista_posizioni_linee_di_separazione[1]):  # 0 e 1                               #c'era lista_posizioni_linee_di_separazione[1]-1
                    coppia_frase_indice_frase_nel_documento = []  # sarà una lista di liste che conterrà la coppia frase - indice di questa frase nel documento

                    coppia_frase_indice_frase_nel_documento.append(lista_frasi_documento[indice_frase])
                    coppia_frase_indice_frase_nel_documento.append(indice_frase)

                    cluster_corrente.append(coppia_frase_indice_frase_nel_documento)

                clusters_correnti.append(cluster_corrente)
                print("cluster_corrente: ")
                print(cluster_corrente)
                print("")
                print("")

            else:
                #allora vuol dire che devo considerare le frasi del secondo cluster; esse andarnno da lista_posizioni_linee_di_separazione[1] <= frasi cluster <= num_frasi_documento - 1
                for indice_frase in range(0, num_frasi_documento):
                    # print("frase: ", frase)
                    if (lista_posizioni_linee_di_separazione[1] <= indice_frase <= num_frasi_documento - 1):
                        coppia_frase_indice_frase_nel_documento = []

                        coppia_frase_indice_frase_nel_documento.append(lista_frasi_documento[indice_frase])
                        coppia_frase_indice_frase_nel_documento.append(indice_frase)

                        cluster_corrente.append(coppia_frase_indice_frase_nel_documento)

                clusters_correnti.append(cluster_corrente)
                print("cluster_corrente: ")
                print(cluster_corrente)
                print("")
                print("")


    return clusters_correnti



def get_overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster(clusters_correnti):

    # Adesso sempre PER OGNI CLUSTER TROVATO:
    # 2.2) Per ogni coppia di frasi sequenziali (in maniera sequenziale, ovvero le prime due frasi presenti nel cluster corrente,
    # dopo per la seconda e la terza, dopo per la terza e la quarta, e così via..) calcolo l'overlap lessicale e aggiungo ad una variabile somma l'overlap
    # tra ogni coppia, in modo tale che alla fine, dopo che avrò considerato tutte le coppie sequenziali, potrò ottenere un valore medio di overlap per il cluster corrente
    # che sarà proprio il valore di coesione di quel cluster:
    lista_coesione_dei_vari_clusters_correnti = []

    # la lista di liste di sotto conterrà ad es: [ [0, 0.11], [1, 0.10], [2, 0.15], ... ]
    # dove per la prima lista [0, 0.11]:
    # - 0 indica che l'overlap presente a destra (ovvero 0.11) indica la sovrapposizione lessicale che c'è tra la frase 0 e la frase 1.
    # - 0.11 è il valore di sovrapposizione lessicale che c'è tra la frase 0 e la frase 1.
    overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster = []  # sarà una lista di liste

    # indice_prima_frase_coppia = 0

    for cluster in clusters_correnti:
        overlap_lessicale_tra_le_varie_coppie_di_frasi_solo_per_il_cluster_corrente = []

        lista_di_frasi_considerate_a_coppie = get_frasi_a_coppie(cluster)

        print("")
        print("")
        print("lista_di_frasi_considerate_a_coppie nel cluster corrente:")
        print(lista_di_frasi_considerate_a_coppie)
        # print("")
        # print("")

        # calcolo l'overlap lessicale per ogni coppia di frasi:
        somma = 0  # conterrà la somma di tutti gli overlap tra tutte le coppie sequenziali del cluster corrente.
        for coppia_frasi_sequenziali in lista_di_frasi_considerate_a_coppie:
            lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ = []

            frase1 = coppia_frasi_sequenziali[0][0]
            frase2 = coppia_frasi_sequenziali[1][0]
            print("")
            print("")
            print("frase1: ", frase1)
            print("frase2: ", frase2)

            overlap_tra_coppia_di_frasi_sequenziali_correnti = overlap_tra_frasi(frase1, frase2)

            lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ.append(coppia_frasi_sequenziali[0][1])
            lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ.append(overlap_tra_coppia_di_frasi_sequenziali_correnti)
            overlap_lessicale_tra_le_varie_coppie_di_frasi_solo_per_il_cluster_corrente.append(lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ)

            # print("frase1:", frase1)
            # print("frase2:", frase2)
            # print("overlap_tra_coppia_di_frasi_sequenziali_correnti:", overlap_tra_coppia_di_frasi_sequenziali_correnti)
            # print("")
            # print("")

            somma += overlap_tra_coppia_di_frasi_sequenziali_correnti  # aggiungo ad una variabile somma l'overlap tra ogni coppia

            # indice_prima_frase_coppia+=1

        print("overlap_lessicale_tra_le_varie_coppie_di_frasi_solo_per_il_cluster_corrente:")
        print(overlap_lessicale_tra_le_varie_coppie_di_frasi_solo_per_il_cluster_corrente)

        coesione_cluster_corrente = somma / len(lista_di_frasi_considerate_a_coppie)
        lista_coesione_dei_vari_clusters_correnti.append(coesione_cluster_corrente)
        overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster.append(overlap_lessicale_tra_le_varie_coppie_di_frasi_solo_per_il_cluster_corrente)

    print("")
    print("")
    print("")
    print("lista_coesione_dei_vari_clusters_correnti:", lista_coesione_dei_vari_clusters_correnti)

    print("")
    print("len(overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster):",len(overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster))
    print("overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster:")
    print(overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster)
    print("")
    print("")
    print("")
    print("")


    return lista_coesione_dei_vari_clusters_correnti, overlap_lessicale_tra_le_varie_coppie_di_frasi_suddivise_per_cluster




def get_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento(lista_frasi_documento):

    lista_di_frasi_documento_considerate_a_coppie = get_frasi_a_coppie(lista_frasi_documento)

    print("lista_di_frasi_documento_considerate_a_coppie: ")
    print(lista_di_frasi_documento_considerate_a_coppie)

    # calcolo l'overlap lessicale per ogni coppia di frasi:
    lista_di_lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ = []
    indice_prima_frase_coppia = 0

    for coppia_frasi_sequenziali in lista_di_frasi_documento_considerate_a_coppie:
        lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ = []

        frase1 = coppia_frasi_sequenziali[0]
        frase2 = coppia_frasi_sequenziali[1]
        print("")
        print("")
        print("frase1: ", frase1)
        print("frase2: ", frase2)

        overlap_tra_coppia_di_frasi_sequenziali_correnti = overlap_tra_frasi(frase1, frase2)
        lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ.append(indice_prima_frase_coppia)
        lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ.append(overlap_tra_coppia_di_frasi_sequenziali_correnti)

        lista_di_lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ.append(lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ)


        indice_prima_frase_coppia+=1


    return lista_di_lista_con_indice_prima_frase_coppia_e_overlap_lessicale_tra_lei_e_la_succ



def text_tiling(path_documento, num_linee_di_separazione, num_max_min_locali):

    lista_frasi_documento = []
    with open(path_documento, 'r', encoding="UTF-8") as documento:
        for frase in documento:
            lista_frasi_documento.append(frase)
    documento.close()


    num_frasi_documento = len(lista_frasi_documento)
    print("num_frasi_documento: ", num_frasi_documento)
    print("")
    print("lista_frasi_documento: ", lista_frasi_documento)
    print("")
    print("")


    lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento = get_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento(lista_frasi_documento)
    print("lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento (NON ORDINATA in base all'overlap): ")
    print(lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento)
    lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento = sorted(lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento, key=itemgetter(1))
    print("lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento (ORDINATA in base all'overlap): ")
    print(lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento)

    lista_primi_num_max_min_locali_considerati = []

    for coppia_posizione_minimo in lista_overlap_lessicale_tra_le_varie_coppie_di_frasi_documento:
        lista_primi_num_max_min_locali_considerati.append(coppia_posizione_minimo)
        if (len(lista_primi_num_max_min_locali_considerati) == num_max_min_locali):  # appena raggiungo il num_max_min_locali esco dal for e la funzione restituisce lista_primi_num_max_min_locali_considerati
            break


    print("")
    print("")
    print("lista_primi_num_max_min_locali_considerati:", lista_primi_num_max_min_locali_considerati)

    posizioni_migliori_barre, coesione_media_clusters_migliore = trova_barre_migliori(lista_primi_num_max_min_locali_considerati, num_linee_di_separazione, num_frasi_documento, lista_frasi_documento)
    print("posizioni_migliori_barre: ", posizioni_migliori_barre)
    print("coesione_media_clusters_migliore: ", coesione_media_clusters_migliore)
    print("")
    print("")


    return posizioni_migliori_barre


def stampa_e_salva_2_paragrafi(file_path, lista_posizioni_linee_di_separazione_finali):
    frase_0_appena_stampata = False
    posizione_barra_precedente = 0
    print("")
    print("")
    print("Frasi del documento stampate SECONDO LA SUDDIVISIONE TROVATA: ")
    print("")
    print("")
    with open(file_path, 'w', encoding="UTF-8") as f:
        for posizione in lista_posizioni_linee_di_separazione_finali:

            if (posizione == 0):
                # Vuol dire che sono all'inizio e quindi devo stampare la prima frase del documento:
                print(lista_frasi_documento[0])
                f.write(lista_frasi_documento[0])
                frase_0_appena_stampata = True

            if (posizione > 0 and frase_0_appena_stampata == True):
                # Allora vuol dire che devo stampare tutte le frasi fino alla posizione corrente (la frase 0 l'ho già stampata):
                for i in range(1, posizione + 1):  # parto da 1 perchè la frase 0 l'ho già stampata. Arrivo fino a posizione+1 perchè la funzione range non considera l'ultimo numero.
                    print(lista_frasi_documento[i])
                    f.write(lista_frasi_documento[i])
                f.write('\n')
                frase_0_appena_stampata = False
                posizione_barra_precedente = posizione + 1

        # A questo punto sono sicuro che questa posizione è l'ultima della lista_posizioni_linee_di_separazione_finali e quindi adesso devo stampare tutti i documenti
        # che vanno da posizione_barra_precedente fino alla fine del documento:
        for i in range(posizione_barra_precedente, len(lista_frasi_documento)):
            print(lista_frasi_documento[i])
            f.write(lista_frasi_documento[i])
        # f.write('\n')
        print("")


def stampa_e_salva_3_paragrafi(file_path, lista_posizioni_linee_di_separazione_finali):
    # lista_frasi_segmentate = []
    frase_0_appena_stampata = False
    entra_else = False
    posizione_barra_precedente = 0
    print("")
    print("")
    print("Frasi del documento stampate SECONDO LA SUDDIVISIONE TROVATA: ")
    print("")
    print("")
    with open(file_path, 'w', encoding="UTF-8") as f:
        for posizione in lista_posizioni_linee_di_separazione_finali:

            if (posizione == 0):
                # Vuol dire che sono all'inizio e quindi devo stampare la prima frase del documento:
                print(lista_frasi_documento[0])
                f.write(lista_frasi_documento[0])
                frase_0_appena_stampata = True

            elif ((posizione > 0) and (frase_0_appena_stampata == True)):
                # Allora vuol dire che devo stampare tutte le frasi fino alla posizione corrente (la frase 0 l'ho già stampata):
                for i in range(1, posizione + 1):  # parto da 1 perchè la frase 0 l'ho già stampata. Arrivo fino a posizione+1 perchè la funzione range non considera l'ultimo numero.
                    print(lista_frasi_documento[i])
                    f.write(lista_frasi_documento[i])
                f.write('\n')
                print("")
                frase_0_appena_stampata = False
                posizione_barra_precedente = posizione + 1

            elif ((posizione > 0) and (posizione == lista_posizioni_linee_di_separazione_finali[2])):
                for i in range(posizione_barra_precedente, posizione + 1):
                    print(lista_frasi_documento[i])
                    f.write(lista_frasi_documento[i])
                f.write('\n')
                print("")
                posizione_barra_precedente = posizione + 1

        # Allora sono sicuro che questa posizione è l'ultima della lista_posizioni_linee_di_separazione_finali e quindi adesso devo stampare tutti i documenti
        # che vanno da posizione_barra_precedente fino alla fine del documento:
        for i in range(posizione_barra_precedente, len(lista_frasi_documento)):
            print(lista_frasi_documento[i])
            f.write(lista_frasi_documento[i])
        # f.write('\n')
        print("")




if __name__ == '__main__':

    path_documento = "paragrafi_Segmentation/3_paragrafi_corpus.txt" #separazioni giuste: 0, 12, 22 (impostare 2 linee di separazione).
    #path_documento = "paragrafi_Segmentation/2_paragrafi_corpus.txt" #separazioni giuste: 0, 10 (impostare 1 linea di separazione).

    # Il secondo parametro della funzione sottostante è il numero di linee di separazione,
    # Il terzo parametro della funzione sottostante è il numero di minimi locali più piccoli che l'algoritmo dovrà considerare.
    lista_posizioni_linee_di_separazione_finali = text_tiling(path_documento, 2, 3)
    print("lista_posizioni_linee_di_separazione_finali: ", lista_posizioni_linee_di_separazione_finali) #lista_posizioni_linee_di_separazione_finali ottenute dall'algoritmo:  [0, 12, 22]

    #######################################################################
    #       STAMPO I RISULTATI OTTENUTI e li serializzo:
    lista_frasi_documento = []
    with open(path_documento, 'r', encoding="UTF-8") as documento:
        for frase in documento:
            lista_frasi_documento.append(frase)
    documento.close()

    if(path_documento == "paragrafi_Segmentation/2_paragrafi_corpus.txt"):
        stampa_e_salva_2_paragrafi("paragrafi_Segmentation\\2_paragrafi_corpus_risultati_segmentation.txt", lista_posizioni_linee_di_separazione_finali)

    else:
        stampa_e_salva_3_paragrafi("paragrafi_Segmentation\\3_paragrafi_corpus_risultati_segmentation.txt", lista_posizioni_linee_di_separazione_finali)
    #######################################################################