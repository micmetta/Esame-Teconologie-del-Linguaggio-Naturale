import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
import nltk
from nltk.corpus import wordnet as wn


def rimozione_punteggiatura(lista_di_definizioni):
    nuova_lista_di_definizioni_senza_punteggiatura = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for definizione in lista_di_definizioni:
        for ele in definizione:
            #print("ele: ", ele)
            if ele in punc:
                definizione = definizione.replace(ele, "")
                #print("tolto..")
        nuova_lista_di_definizioni_senza_punteggiatura.append(definizione)

    return nuova_lista_di_definizioni_senza_punteggiatura


def rimozione_punteggiatura_da_una_lista(definizione):
    #nuova_lista_di_definizione = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    #for ele in definizione:
    for i in range(0, len(definizione)):
        #print("ele: ", ele)
        if definizione[i] in punc:
            definizione[i] = definizione[i].replace(definizione[i], "")
            #print("tolto..")
    #nuova_lista_di_definizione.append(definizione)

    return definizione


def rimozione_stringa_vuota(lista_di_definizioni):
    nuova_lista_di_definizioni = []
    #esempio di lista_di_definizioni:  [['negative', 'emotion', ''], ['Reaction', 'anger', 'violence', 'oneself', 'others', 'arising', 'forms', 'feelings']]
    for definizione in lista_di_definizioni:
        while ("" in definizione):
            definizione.remove("")
        nuova_lista_di_definizioni.append(definizione)

    return nuova_lista_di_definizioni


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


def n_parole_piu_frequenti(lista_definizioni_per_concetto_corrente, n):

    #ESEMPIO DI lista_definizioni_per_concetto_corrente data in input:
    #[['Range', 'concepts', 'human', 'beings', 'feel', 'certain', 'situations'], ['Something', 'feel'], ['Something', 'animal', 'feel'],
    # ['something', 'think', 'makes', 'feel', 'good', 'bad'], ['Human', 'sensation', 'arising', 'form', 'feelings'],
    # ['State', 'mind', 'living', 'percieve'], ['Feeling', 'human', 'animal', 'express', 'towards', 'others'],
    # ['A', 'sentiment', 'living', 'entity', 'feel', 'express', 'throw', 'words', 'body.'], ['feel', 'certain', 'moment'],
    # ['feeling', 'experienced', 'sentient', 'beings', 'cause', 'events', 'happening', 'outside', 'world', 'well', "being's", 'ming'],
    # ['feeling', 'deriving', "one's", 'circumstances', 'relationships', 'others'], ['feeling', 'love', 'anger,', 'feelings', 'general'],
    # ['sentimental', 'reation', 'action'], ['something', 'feel'], ['human', 'feeling,', 'eg', 'happyness,', 'sadness,', 'love'], ['general', 'concept', 'feeling'],
    # ['A', 'feeling', 'deriving', 'human', 'life'], ['human', 'sensation', ''], ['An', 'animal', 'feeling'], ['Emotion', 'psychic', 'state'], ['something', 'human', 'feel'],
    # ['Human', 'sensation', 'affect', 'someones', 'mood', 'either', 'positive', 'negative', 'way'], ['feeling', 'living'], ['feeling'],
    # ['A', 'particular', 'state', 'mind', 'person', 'caused', 'something', 'internal', 'external'], ['A', 'mental', 'reaction'], ['strong', 'feeling'],
    # ['Feeling/State', 'felt', 'living', 'beings'], ['The', 'mental', 'state', 'agent'], ['Mental', 'mood', ''], ['feeling', 'dued', 'something'],
    # ['Emotion', 'feeling', 'created', 'physical', 'mental', 'stimulus.']]

    #Ricorda: Considero ogni parola in minuscolo per far funzionare bene gli overlap.
    dizionario_parole_definizioni_con_frequenza = {}
    for definizione in lista_definizioni_per_concetto_corrente:

        lista_parole_definizione_corrente = []

        for parola in definizione:
            if (parola.lower() not in lista_parole_definizione_corrente): #se la parola corrente non l'ho già considerata nella definizione corrente allora faccio quello
                #detto qui sotto, altrimenti passo alla parola successiva della definizione corrente.

                if(parola.lower() in dizionario_parole_definizioni_con_frequenza):
                    #vuol dire che la parola è già presente nel dizionario e quindi mi basta aumentare la sua frequenza:
                    dizionario_parole_definizioni_con_frequenza[parola.lower()] = dizionario_parole_definizioni_con_frequenza[parola.lower()] + 1
                else:
                    #vuol dire che la parola non è presente nel dizionario e quindi la devo aggiungere e inserisco la sua frequenza corrente che in questo caso sarà 1:
                    dizionario_parole_definizioni_con_frequenza[parola.lower()] = 1

                lista_parole_definizione_corrente.append(parola.lower()) #aggiungo la parola alla lista per ricordarmi che questa l'ho già considerata nella definizione
                #corrente.

    '''
    print("")
    print("")
    print("")
    print("dizionario_parole_definizioni_con_frequenza:")
    print(dizionario_parole_definizioni_con_frequenza)
    print("")
    '''

    #Adesso prendo le 5 parole più frequenti
    sorted_dizionario_parole_definizioni_con_frequenza = dict(sorted(dizionario_parole_definizioni_con_frequenza.items(), key=operator.itemgetter(1), reverse=True))
    '''
    print("sorted_dizionario_parole_definizioni_con_frequenza: ")
    print(sorted_dizionario_parole_definizioni_con_frequenza)
    print("")
    '''

    prime_n_parole_piu_frequenti = list(sorted_dizionario_parole_definizioni_con_frequenza)[:n]
    '''
    print("Le prime " + str(n) + " parole più frequenti:")
    print(prime_n_parole_piu_frequenti)
    print("")
    print("")
    print("")
    '''


    return prime_n_parole_piu_frequenti


def ComputeOverlap(signature, context):

    lista_lemmi = signature[0]
    glossa = signature[1]
    lista_esempi = signature[2]
    overlap = 0

    for lemma in lista_lemmi:
        for parola_context in context:
            if(lemma.lower() == parola_context.lower()):
                # print("lemma.lower(): ", lemma.lower())
                # print("parola_context.lower(): ", parola_context.lower())
                overlap += 1

    #lista_parole_glossa = glossa.split(" ")
    #print("lista_parole_glossa: ", lista_parole_glossa)
    for parola_glossa in glossa:
        for parola_context in context:
            if (parola_glossa.lower() == parola_context.lower()):
                # print("parola_glossa.lower(): ", parola_glossa.lower())
                # print("parola_context.lower(): ", parola_context.lower())
                overlap += 1

    #print("lista_esempi: ", lista_esempi)
    if (lista_esempi != []):
        for esempio in lista_esempi:
            #lista_parole_esempio = esempio.split(" ")
            #print("lista_parole_esempio: ", lista_parole_esempio)
            for parola_esempio in esempio:
                for parola_context in context:
                    if (parola_esempio.lower() == parola_context.lower()):
                        # print("parola_esempio.lower(): ", parola_esempio.lower())
                        # print("parola_context.lower(): ", parola_context.lower())
                        overlap += 1

    return overlap




def The_Lesk_Algorithm_score(nome_senso_corrente, lista_definizioni_per_concetto_corrente):


    #best_sense = wn.synsets(word)[0] #inizilizzo best_sense con il senso più frequente.
    #best_sense = tutti_i_sensi_della_parola_da_disambiguare[0]

    synset_corrente = wn.synset(nome_senso_corrente)
    '''
    print("synset_corrente in LESK: ", synset_corrente)
    '''
    lemmi_associati_al_synset_corrente_associato_al_GENUS_corrente = synset_corrente.lemma_names()  # prendo i lemmi associati al synset corrente associato al GENUS corrente
    definizione_associata_al_synset_corrente_associato_al_GENUS_corrente = synset_corrente.definition()
    lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente = synset_corrente.examples()
    '''
    print("lemmi_associati_al_synset_corrente_associato_al_GENUS_corrente: ",lemmi_associati_al_synset_corrente_associato_al_GENUS_corrente)
    print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente: ",definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    print("esempi_associati_al_synset_corrente_associato_al_GENUS_corrente: ",lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente)
    print("lista_iponimi_synset_corrente_associato_al_GENUS_corrente: ",lista_iponimi_synset_corrente_associato_al_GENUS_corrente)
    print("")
    print("")
    '''

    # context sarà una lista DI PAROLE che conterrà tutte le parole delle definizioni del concetto corrente (ad es: Emotion)
    context = []
    for definizione in lista_definizioni_per_concetto_corrente:
        for parola in definizione:
            context.append(parola)
    ########################################################################################################################


    # signature sarà una lista di liste che conterrà:
    # - Come prima lista --> una lista che contiene tutti i lemmi del synset corrente che è uno dei possibili synset (ad es: feeling.n.01).
    # - Come seconda lista --> che contiene la definizione, detta anche glossa (sottoforma di una lista di parole) del synset corrente che è uno dei possibili synset (ad es: feeling.n.01).
    # - Come terza lista --> che contiene tutti gli esempi (ciascun esempio è una lista di parole) del synset corrente che è uno dei possibili synset (ad es: feeling.n.01).

    ############################################################################################################################################################
    #Eseguo un passo di preprocessing per:
    # 1) Eliminare dalla glossa tutte le stop words.
    # 2) Eliminare le stringhe vuote.
    # 3) Lemmatizzare tutte le parole rimanenti.
    # 4) Infine elimino la punteggiatura.
    # print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente PRIMA DELL'ELIMINAZIONE STOP WORDS:")
    # print(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)

    #1):
    definizione_associata_al_synset_corrente_associato_al_GENUS_corrente = [word for word in definizione_associata_al_synset_corrente_associato_al_GENUS_corrente.split(" ") if word not in stopwords.words('english') and word.lower() != 'a' and word.lower() != 'the' and word.lower() != 'an']
    # print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente DOPO DELL'ELIMINAZIONE STOP WORDS:")
    # print(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)

    #2)
    definizione_associata_al_synset_corrente_associato_al_GENUS_corrente = rimozione_stringa_vuota_da_una_lista(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    # print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente DOPO l'eliminazione stringa vuota:")
    # print(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)

    #3):
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)):
        definizione_associata_al_synset_corrente_associato_al_GENUS_corrente[i] = lemmatizer.lemmatize(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente[i])
    #4):
    '''
    print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente: ")
    print(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    '''
    definizione_associata_al_synset_corrente_associato_al_GENUS_corrente = rimozione_punteggiatura_da_una_lista(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    # print("definizione_associata_al_synset_corrente_associato_al_GENUS_corrente DOPO I 3 PASSI:")
    # print(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    # print("")
    # print("")
    # print("")
    ############################################################################################################################################################



    ############################################################################################################################################################
    # Eseguo un passo di preprocessing per:
    # 1) Eliminare dalla lista degli esempi tutte le stop words.
    # 2) Eliminare dalla lista degli esempi le stringhe vuote.
    # 3) Lemmatizzare tutte le parole rimanenti nella lista degli esempi.
    # 4) Infine elimino la punteggiatura dalla lista degli esempi.
    # 1):
    nuova_lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente = []
    for esempio in lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente:
        # print("esempio PRIMA:")
        # print(esempio)
        # 1):
        nuovo_esempio = [word for word in esempio.split(" ") if word.lower() not in stopwords.words('english') and word.lower() != 'a' and word.lower() != 'the' and word.lower() != 'an']
        # print("esempio DOPO EL. SW:")
        # print(nuovo_esempio)

        # 2):
        nuovo_esempio = rimozione_stringa_vuota_da_una_lista(nuovo_esempio)
        # print("esempio DOPO rimozione_stringa_vuota_da_una_lista:")
        # print(nuovo_esempio)

        # 3):
        lemmatizer = WordNetLemmatizer()
        for i in range(0, len(nuovo_esempio)):
            #print("nuovo_esempio[i]: ", nuovo_esempio[i])
            nuovo_esempio[i] = lemmatizer.lemmatize(nuovo_esempio[i].lower())
        # print("")
        # print("")
        # print("esempio DOPO lemmatizzazione:")
        # print(nuovo_esempio)
        # print("")
        # print("")

        # 4):
        nuovo_esempio = rimozione_punteggiatura_da_una_lista(nuovo_esempio)
        # print("esempio DOPO rimozione_punteggiatura_da_una_lista:")
        # print(nuovo_esempio)

        nuova_lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente.append(nuovo_esempio)

    # print("nuova_lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente DOPO I 3 PASSI:")
    # print(nuova_lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente)
    # print("")
    # print("")
    # print("")
    ############################################################################################################################################################



    # associati al concetto corrente (ad es: Emotion)
    signature = []
    signature.append(lemmi_associati_al_synset_corrente_associato_al_GENUS_corrente)
    signature.append(definizione_associata_al_synset_corrente_associato_al_GENUS_corrente)
    signature.append(nuova_lista_esempi_associati_al_synset_corrente_associato_al_GENUS_corrente)
    '''
    print("context: ", context)
    print("signature: ", signature)
    '''
    #calcolo l'Overlap tra la signature e il contesto:
    overlap = ComputeOverlap(signature, context)
    '''
    print("overlap: ", overlap)
    print("")
    print("")
    '''

    return overlap #restitusico l'overlap ovvero lo score tra la signature e il contesto


#Prende in input: nome concetto corrente, lista_definizioni_per_concetto_corrente (che è una lista di liste in cui ogni lista interna è una lista di parole di una certa frase).
#Restituisce: lista_definizioni_per_concetto_corrente senza concetto_corrente.
def eliminazione_cicolarita_diretta(concetto_corrente, lista_definizioni_per_concetto_corrente):
    nuova_lista_definizioni_per_concetto_corrente = []
    for lista_parole_frase_corrente in lista_definizioni_per_concetto_corrente:
        nuova_lista_parole_frase_corrente = []
        for parola in lista_parole_frase_corrente:
            if(parola.lower() != concetto_corrente.lower() and parola.lower() != "ei"):
                nuova_lista_parole_frase_corrente.append(parola)

        nuova_lista_definizioni_per_concetto_corrente.append(nuova_lista_parole_frase_corrente)

    return nuova_lista_definizioni_per_concetto_corrente





if __name__ == '__main__':

    definizioni_df = pd.ExcelFile("definizioni.xlsx").parse("Foglio1")
    print("definizioni_df:")
    print(definizioni_df)


    lista_definizioni_per_concetto_corrente = []
    num_max_di_definizioni = definizioni_df.shape[1] - 1 #-1 perchè la prima colonna contiene i concetti.
    for riga in range(definizioni_df.shape[0]):

        dizionario_synsets_con_rispettivi_scores = {}
        lista_definizioni_per_concetto_corrente = []
        concetto_corrente = definizioni_df["Unnamed: 0"].iloc[riga]
        print("")
        print("")
        print("")
        print("")
        print("Concetto corrente: ", concetto_corrente)
        for colonna in range(1, definizioni_df.shape[1]):
            lista_definizioni_per_concetto_corrente.append(
                definizioni_df.iloc[riga:riga + 1, colonna:colonna + 1].values[0][0])

        ########################################################################################################################
        '''
        print("lista_definizioni_per_concetto_corrente PRIMA DELLA RIMOZIONE DELLA PUNTEGGIATURA: ")
        print(lista_definizioni_per_concetto_corrente)
        '''

        lista_definizioni_per_concetto_corrente = rimozione_punteggiatura(lista_definizioni_per_concetto_corrente)

        '''
        print("lista_definizioni_per_concetto_corrente DOPO RIMOZIONE PUNTEGGIATURA: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        print("")
        '''
        ########################################################################################################################

        ########################################################################################################################
        '''
        print("lista_definizioni_per_concetto_corrente PRIMA: ")
        print(lista_definizioni_per_concetto_corrente)
        '''
        # Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
        for i in range(0, len(lista_definizioni_per_concetto_corrente)):
            definizione_corrente = lista_definizioni_per_concetto_corrente[i]
            definizione_corrente = definizione_corrente.split(" ")
            '''
            print("definizione_corrente: ")
            print(definizione_corrente)
            print("")
            print("")
            '''
            # Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
            lista_definizioni_per_concetto_corrente[i] = [word for word in definizione_corrente if word not in stopwords.words('english') and word.lower() != 'a' and word.lower() != 'the' and word.lower() != 'an' and word.lower() != 'u' and word.lower() != 'eg' and word.lower() != "it’s"]
        '''
        print("lista_definizioni_per_concetto_corrente senza stop words: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        '''

        ########################################################################################################################

        ########################################################################################################################
        # Adesso elimino tutte le stringhe vuote nelle definizioni:
        lista_definizioni_per_concetto_corrente = rimozione_stringa_vuota(lista_definizioni_per_concetto_corrente)

        print("lista_definizioni_per_concetto_corrente senza stop words e senza stringhe vuote: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")

        ########################################################################################################################


        ########################################################################################################################
        # Rimozione circolarità diretta:
        # - Rimuovo da ogni frase tutte le parole che sono uguali al concetto_corrente:
        lista_definizioni_per_concetto_corrente = eliminazione_cicolarita_diretta(concetto_corrente,lista_definizioni_per_concetto_corrente)
        print("lista_definizioni_per_concetto_corrente senza stop words e senza stringhe vuote e SENZA CIRCOLARITA' DIRETTA: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        ########################################################################################################################


        # Adesso lista_definizioni_per_concetto_corrente è diventata una lista di liste in cui ogni elemento della lista iniziale è una definizione e
        # ogni definizione è a sua volta una lista di parole singole (senza stop words) che sono presenti in quella definizione.

        ########################################################################################################################
        # Adesso applico la lemmatizzazione alle parole delle definizioni:
        lemmatizer = WordNetLemmatizer()
        for definizione in lista_definizioni_per_concetto_corrente:
            for i in range(0, len(definizione)):
                definizione[i] = lemmatizer.lemmatize(definizione[i])
        '''
        print("lista_definizioni_per_concetto_corrente senza stop words e dopo aver applicato la lemmatizzazione: ")
        print(lista_definizioni_per_concetto_corrente)
        '''
        ########################################################################################################################

        ########################################################################################################################
        # Adesso trovo le n parole più frequenti nelle definizioni per il concetto corrente:
        n = 45
        n_parole_piu_frequenti_per_concetto_corrente = n_parole_piu_frequenti(lista_definizioni_per_concetto_corrente, n)  # n=45 in questo caso.
        print("n_parole_piu_frequenti_per_concetto_corrente: ", n_parole_piu_frequenti_per_concetto_corrente)
        ########################################################################################################################

        ##############################################################################
        # # Adesso considero come GENUS la parola più frequente per il concetto corrente:
        # GENUS_per_concetto_corrente = n_parole_piu_frequenti_per_concetto_corrente[0]
        # print("GENUS_per_concetto_corrente: ", GENUS_per_concetto_corrente)
        # print("")
        #Adesso considero come GENUS le prime 5 parole più frequente per il concetto corrente:
        for GENUS_per_concetto_corrente in n_parole_piu_frequenti_per_concetto_corrente:
            print("GENUS_per_concetto_corrente: ", GENUS_per_concetto_corrente)
            print("")
            ##############################################################################

            ############################################################################################################################################################
            # dizionario_synsets_con_rispettivi_scores = {}

            # Adesso mi collego a Wordnet e prendo:
            # 1) Tutti i synsets associati al GENUS.
            # 2) Per ogni synset associato al GENUS prendo i lemmi, la definizione e gli esempi e inoltre prendo tutti i loro relativi iponimi.
            # 3) Per ogni iponimo ottenuto prendo i suoi lemmi, la sua definizione e gli esempi ad esso associato.
            for ss in wn.synsets(GENUS_per_concetto_corrente):
                nome_synset_corrente = ss.name()
                #print("nome_synset_corrente: ", nome_synset_corrente)
                ###############################################################################################################################
                # Adesso POSSO CALCOLARE LO SCORE DEL synset_corrente FACENDO L'OVERLAP CON TUTTE LE DEFINIZIONI del concetto corrente (che sarà ad es. EMOTION):
                # Chiaramente in dizionario_synsets_con_rispettivi_scores mi memorizzo il nome del synset e lo score che ha ottenuto:
                score_synset_corrente = The_Lesk_Algorithm_score(nome_synset_corrente, lista_definizioni_per_concetto_corrente)
                #print("score_synset_corrente: ", score_synset_corrente)
                dizionario_synsets_con_rispettivi_scores[nome_synset_corrente] = score_synset_corrente
                #print("dizionario_synsets_con_rispettivi_scores:")
                #print(dizionario_synsets_con_rispettivi_scores)
                # print("")
                # print("")
                # print("")
                ###############################################################################################################################

                #####################################################################################################
                # DOPODICHE' CALCOLO LO SCORE DI TUTTI GLI IPONIMI DEL synset_corrente FACENDO sempre L'OVERLAP CON TUTTE LE DEFINIZIONI DEL concetto corrente (ad es: EMOTION):
                # Chiaramente in dizionario_synsets_con_rispettivi_scores mi memorizzo il nome del synset e lo score che ha ottenuto:
                # #3) Per ogni iponimo ottenuto prendo i suoi lemmi, la sua definizione e gli esempi ad esso associato:
                lista_iponimi_synset_corrente_associato_al_GENUS_corrente = wn.synset(nome_synset_corrente).hyponyms()
                for iponimo in lista_iponimi_synset_corrente_associato_al_GENUS_corrente:
                    nome_iponimo_corrente = iponimo.name()
                    #print("nome_iponimo_corrente: ", nome_iponimo_corrente)
                    score_iponimo_corrente = The_Lesk_Algorithm_score(nome_iponimo_corrente, lista_definizioni_per_concetto_corrente)
                    dizionario_synsets_con_rispettivi_scores[nome_iponimo_corrente] = score_iponimo_corrente
                #####################################################################################################

        ###############################################################################################################################
        # ADESSO ORDINO IL dizionario_synsets_con_rispettivi_scores e prendo solo i primi n synset che saranno quelli con lo score maggiore:
        n = 5
        sorted_dizionario_synsets_con_rispettivi_scores = dict(sorted(dizionario_synsets_con_rispettivi_scores.items(), key=operator.itemgetter(1), reverse=True))
        print("sorted_dizionario_synsets_con_rispettivi_scores:")
        print(sorted_dizionario_synsets_con_rispettivi_scores)
        print("")
        primi_n_synset_con_score_maggiore = list(sorted_dizionario_synsets_con_rispettivi_scores)[:n]
        # print("primi_n_synset_con_score_maggiore:")
        # print(primi_n_synset_con_score_maggiore)
        print("")
        print("")
        ###############################################################################################################################

        print("I primi " + str(n) + " synsets per il concetto " + concetto_corrente + " sono i seguenti:")
        print("")
        for synset in primi_n_synset_con_score_maggiore:
            definizione_synset_corrente = wn.synset(synset).definition()
            print("- Synset(" + str(synset) + "):", definizione_synset_corrente)
            #print(definizione_synset_corrente)
            print("")

        ############################################################################################################################################################