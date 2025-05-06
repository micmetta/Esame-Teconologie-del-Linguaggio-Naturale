import importlib
import en_core_web_sm
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import operator
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
nlp = en_core_web_sm.load()



def frasi_senza_Ner_tags(frasi_train):
    # print("frasi_train:")
    # print(frasi_train)
    frasi_train_senza_NER_tags = []
    for frase_train in frasi_train:
        frase_train_splittata = frase_train.split(" ")
        lista_parole_correnti_senza_Ner_tags = []
        for parola in frase_train_splittata:
            parola_splittata_in_base_allo_spazio_di_tab = parola.split("\t")
            # print("parola_splittata_in_base_allo_spazio_di_tab[0]: ", parola_splittata_in_base_allo_spazio_di_tab[0])
            # print("")
            lista_parole_correnti_senza_Ner_tags.append(parola_splittata_in_base_allo_spazio_di_tab[0])

        # print("")
        # print("")
        frasi_train_senza_NER_tags.append(lista_parole_correnti_senza_Ner_tags)

    # print(frasi_train_senza_NER_tags)
    # print("")
    # print("")

    return frasi_train_senza_NER_tags


def rimozione_punteggiatura(lista_di_definizioni):
    nuova_lista_di_definizioni_senza_punteggiatura = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for definizione in lista_di_definizioni:
        nuova_definizione = []
        for ele in definizione:
            if ele not in punc:
                nuova_definizione.append(ele)
        nuova_lista_di_definizioni_senza_punteggiatura.append(nuova_definizione)

    return nuova_lista_di_definizioni_senza_punteggiatura


#Seleziona le frasi con un certo verbo al proprio interno.
def selezionare_frasi_con_una_certa_parola_al_loro_interno(frasi_train_senza_NER_tags, parola_interesse, lista_declinazioni_parola_interesse):
    lista_frasi_con_parole_interesse = []
    for frase in frasi_train_senza_NER_tags:
        frase = [word for word in frase if word not in stopwords.words('english')]  # elimino le stop words dalla frase corrente

        lemmatizer = WordNetLemmatizer() #(il verbo con ing non lo trasforma al verbo all'infinito)
        ps = PorterStemmer() #mi permette di fare lo stemming di una parola (in modo da portare alla forma infinito del verbo ad es. use tutte le sue declinazioni come ad esempio uses, used, using)
        for i in range(0, len(frase)):
            frase[i] = lemmatizer.lemmatize(frase[i])
            if(frase[i] in lista_declinazioni_parola_interesse):
                #print("frase[i] prima dello stamming:", frase[i])
                frase[i] = ps.stem(frase[i])
                #print("frase[i] prima dopo lo stamming:", frase[i])

        #se la parola d'interesse (verbo scelto) è presente nella frase corrente allora questa frase viene inserita nella lista di frasi che poi verrà restituita dalla funzione.
        if(parola_interesse in frase):
            lista_frasi_con_parole_interesse.append(frase)

    return lista_frasi_con_parole_interesse



#Funzione che restituisce il soggetto (uno tra i possibili) e l'oggetto (uno tra i possibili) di un verbo.
def parole_argomenti_verbo(frase, parola_interesse):
    frase = ' '.join(frase)

    frase_doc = nlp(frase)
    soggetto = ""
    oggetto = ""
    #Ho deciso di selezionare i possibili soggetti e oggetti da considerare altrimenti l'algoritmo prendeva sempre la stessa parola sia come soggetto che come oggetto.
    possibili_soggetti = ['subj', 'nsubjpass', 'nsubj']
    possibili_oggetti = ['pobj', 'dobj', 'obj', 'iobj']

    for token in frase_doc:
        if token.head.lemma_ == parola_interesse: #vedo se la testa della dipendenza è proprio il verbo che mi interessa.

            #token.dep_ = nome della dipendenza sintattica.

            if token.dep_ in possibili_soggetti and soggetto == "":
                soggetto = (token.lemma_, token.pos_) #prendo la parola presente a sinistra del verbo.
                #print("soggetto: ", soggetto)
                #print("token.dep_: ", token.dep_) #stampo la dipendenza sintattica della parola indicata da token.lemma_

            if token.dep_ in possibili_oggetti and oggetto == "":
                oggetto = (token.lemma_, token.pos_) #prendo la parola presente a destra del verbo.
                #print("oggetto: ", oggetto)
                #print("token.dep_: ", token.dep_)  # stampo la dipendenza sintattica della parola indicata da token.lemma_



    return soggetto, oggetto




def ComputeOverlap(signature, context):

    lista_esempi = signature[0]
    lista_glosse = signature[1]
    '''
    print("")
    print("lista_esempi INIZIALE: ", lista_esempi)
    print("lista_glosse INIZIALE: ", lista_glosse)
    print("")
    print("")
    '''

    #Quello che posso fare ora è eliminare le stop words dalla lista_esempi, dalla lista_glosse e dal context:##########

    lista_esempi_dove_ogni_parola_e_un_elemento_della_lista = []
    if (lista_esempi != []):
        for esempio in lista_esempi:
            lista_parole_esempio = esempio.split(" ")
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

    '''
    print("")
    print("lista_esempi_dove_ogni_parola_e_un_elemento_della_lista PRIMA: ")
    print(lista_esempi_dove_ogni_parola_e_un_elemento_della_lista)
    print("")
    print("lista_glosse_dove_ogni_parola_e_un_elemento_della_lista PRIMA: ")
    print(lista_glosse_dove_ogni_parola_e_un_elemento_della_lista)
    print("")
    print("context PRIMA: ")
    print(context)
    print("")
    '''

    #elimino le stop words presenti nella lista_esempi:
    lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw = [word for word in lista_esempi_dove_ogni_parola_e_un_elemento_della_lista if word not in stopwords.words('english')]

    #elimino le stop words presenti nella lista_glosse:
    lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw = [word for word in lista_glosse_dove_ogni_parola_e_un_elemento_della_lista if word not in stopwords.words('english')]

    # elimino le stop words presenti nel context:
    context_senza_ssw = [word for word in context if word not in stopwords.words('english')]
    ####################################################################################################################

    '''
    print("lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw: ")
    print(lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw)
    print("")
    print("lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw: ")
    print(lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw)
    print("")
    print("context_senza_ssw: ")
    print(context_senza_ssw)
    print("")
    '''

    overlap = 0
    lemmatizer = WordNetLemmatizer() #istanzio l'oggetto lemmatizzatore.

    if(lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw != []):
        for parola_esempio in lista_esempi_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw:
                for parola_context in context_senza_ssw:
                    # applico la lemmatizzazione solo a parola_esempio perchè parola_context l'ho lemmatizzata all'inizio del programma quando carico le frasi dal corpus.
                    if(lemmatizer.lemmatize(parola_esempio) == parola_context):
                        #print("parola_esempio: ", parola_esempio)
                        #print("parola_context: ", parola_context)
                        overlap += 1

    for parola_glossa in lista_glosse_dove_ogni_parola_e_un_elemento_della_lista_senza_ssw:
            for parola_context in context_senza_ssw:
                # applico la lemmatizzazione solo a parola_glossa perchè parola_context l'ho lemmatizzata all'inizio del programma quando carico le frasi dal corpus.
                if(lemmatizer.lemmatize(parola_glossa) == parola_context):
                    #print("parola_glossa: ", parola_glossa)
                    #print("parola_context: ", parola_context)
                    overlap += 1


    return overlap




def The_Lesk_Algorithm(lista_parola_pos, frase):

    #print("lista_parola_pos in The_Lesk_Algorithm: ", lista_parola_pos)
    parola_da_disambiguare = lista_parola_pos[0]
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
            '''
            print("context: ", context)
            print("signature: ", signature)
            '''
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



#funzione che mi restituisce i supersensi dei due synsets di input
def supersensi(synset1, synset2):
    # print("synset1.lexname(): ", synset1.lexname())
    # print("synset2.lexname(): ", synset2.lexname())
    return synset1.lexname().split(".")[1], synset2.lexname().split(".")[1]









if __name__ == '__main__':

    #INFO: La stampa delle informazioni in console inizia dopo alcuni minuti.

    ##################################################################################################################################################################################################################
    #INIZIO DEL PROGRAMMA:

    #Caricamento dataset:
    Estrazione_dati_BIO_tagging_Wikipedia_it_e_en = importlib.import_module('.Estrazione_dati_BIO_tagging_Wikipedia_it_e_en', package = 'Risorse utili per esercitazione Hanks')
    frasi_train, tag_possibili, dizionario_indice_numerico_tag, dizionario_per_passare_dal_tag_al_numero, a_s_primo_s = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.caricamento_dati_BIO_tagging_en()
    frasi_test_set = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_test_set_en()
    frasi_validation_set = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_validation_set_en_con_tags()

    #Unisco le frasi di trainining, test e validation sets insieme:
    frasi_dataset = []
    for frase in frasi_train:
        frasi_dataset.append(frase)
    for frase in frasi_test_set:
        frasi_dataset.append(frase)
    for frase in frasi_validation_set:
        frasi_dataset.append(frase)
    ###############################################################


    #Rimuovo i NER tags dal dataset: #######################################################################################
    frasi_train_senza_NER_tags = frasi_senza_Ner_tags(frasi_dataset)

    #rimuovo la punteggiatura dalle frasi:
    # print("frasi_train_senza_NER_tags[0] Prima della rimozione punteggiatura:")
    # print(frasi_train_senza_NER_tags[0])
    # print("")
    frasi_train_senza_NER_tags = rimozione_punteggiatura(frasi_train_senza_NER_tags)
    # print("frasi_train_senza_NER_tags[0] DOPO della rimozione punteggiatura:")
    # print(frasi_train_senza_NER_tags[0])

    #Adesso seleziono solamente le frasi che hanno la parola love al proprio interno:


    parola_interesse = "use"
    lista_declinazioni_parola_interesse = ["use","uses"]
    # parola_interesse = "take"
    # lista_declinazioni_parola_interesse = ["take","takes"]


    frasi_train_senza_NER_tags = selezionare_frasi_con_una_certa_parola_al_loro_interno(frasi_train_senza_NER_tags, parola_interesse, lista_declinazioni_parola_interesse) #ci mette un pò di tempo per farlo perchè il corpus è abbastanza grande
    # print("frasi_train_senza_NER_tags[1] DOPO la selezione con parola d'interesse:")
    # print(frasi_train_senza_NER_tags[10])
    print("")
    print("Numero di frasi con la parola " + parola_interesse + ":", len(frasi_train_senza_NER_tags))
    print("")
    print("")
    ########################################################################################################################


    ##########################################################################################
    #A questo punto posso:
    # 1) Parserizzare le varie frasi presenti nel frasi_train_senza_NER_tags.
    # 2) Eseguire la WSD tramite una mia implementazione dell'algoritmo di LESK per il soggetto e l'oggetto ottenuti per la frase corrente.
    # 3) Ottenere i supersensi dei due best synsets ottenuti per il soggetto e l'oggetto
    # 4) Memorizzarmi in un dizionario tutte le frequenze di ogni coppia di semantic types ottenute.
    # 5) stampo le prime n coppie di semantic_types più ricorrenti negli slots.

    num_frasi_con_subj_e_obj_diversi_da_none = 0
    dizionario_semantic_types = {}
    for frase in frasi_train_senza_NER_tags:
        # frase = [word for word in frase if word not in stopwords.words('english')]  # elimino le stop words dalla frase corrente
        # lemmatizer = WordNetLemmatizer()
        # for i in range(0, len(frase)):
        #     frase[i] = lemmatizer.lemmatize(frase[i])


        #1) Parserizzare le varie frasi presenti nel frasi_train_senza_NER_tags:
        print("")
        print("")
        soggetto, oggetto = parole_argomenti_verbo(frase, parola_interesse)
        #######################################################################

        if(soggetto != "" and oggetto != ""):

            #2) Eseguire la WSD tramite una mia implementazione dell'algoritmo di LESK per il soggetto e l'oggetto ottenuti per la frase corrente.
            #Adesso devo ottenere i synsets associati al soggetto e fare la WSD in modo tale da ottenere il synset migliore per la parola che si trova come soggetto del verbo e per quella che si trova come oggetto del verbo:
            best_synset_soggetto = The_Lesk_Algorithm(soggetto, frase)
            best_synset_oggetto = The_Lesk_Algorithm(oggetto, frase)
            ######################################################################################################################################

            if(best_synset_soggetto is not None and best_synset_oggetto is not None):
                print("")
                print("")
                print("")
                print("")
                print("FRASE CORRENTE:")
                print(frase)
                print("")
                print("soggetto + pos: ", soggetto)
                print("oggetto + pos: ", oggetto)
                print("")
                print("")
                print("best_synset_soggetto: ", best_synset_soggetto)
                print("best_synset_oggetto: ", best_synset_oggetto)
                num_frasi_con_subj_e_obj_diversi_da_none+=1

                # 3) Ottenere i supersensi dei due best synsets ottenuti per il soggetto e l'oggetto:
                supesenso1, supersenso2 = supersensi(best_synset_soggetto, best_synset_oggetto)
                ####################################################################################


                print("supesenso1: ", supesenso1)
                print("supersenso2: ", supersenso2)

                #concateno i due semantic types:
                coppia_semantic_types = supesenso1 + "-" + supersenso2

                #4) Memorizzarmi in un dizionario tutte le frequenze di ogni coppia di semantic types ottenute:
                #Inserisco nel dizionario_semantic_types la coppia_semantic_types corrente qualora non fosse già presente nel dizionario e gli aggiungo 1 come conteggio,
                #altrimenti qualora la coppia fosse già presente nel dizionario incremento il suo conteggio di 1:
                if(coppia_semantic_types in dizionario_semantic_types):
                    dizionario_semantic_types[coppia_semantic_types] += 1
                else:
                    dizionario_semantic_types[coppia_semantic_types] = 1
                ###############################################################################################


    print("")
    print("")
    print("num_frasi_con_subj_e_obj_diversi_da_none: ", num_frasi_con_subj_e_obj_diversi_da_none)
    #ordino il dizionario_semantic_types e lo stampo:
    dizionario_semantic_types_ordinato = dict(sorted(dizionario_semantic_types.items(), key=operator.itemgetter(1), reverse=True))
    print("dizionario_semantic_types_ordinato:")
    print(dizionario_semantic_types_ordinato)
    print("")
    print("")
    #5) stampo le prime n coppie di semantic_types più ricorrenti negli slots:
    n = 10
    primi_n_semantic_types_piu_ricorrenti = list(dizionario_semantic_types_ordinato)[:n]
    for coppia_semantic_types in primi_n_semantic_types_piu_ricorrenti:
        print("La coppia (" + coppia_semantic_types + ") è presente " + str(dizionario_semantic_types_ordinato[coppia_semantic_types]) + " volte su " + str(num_frasi_con_subj_e_obj_diversi_da_none))
        print("")
    ##################################################################################################################################################################################################################



