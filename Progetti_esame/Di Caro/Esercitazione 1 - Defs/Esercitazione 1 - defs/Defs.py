import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator


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


def rimozione_stringa_vuota(lista_di_definizioni):
    nuova_lista_di_definizioni = []
    #esempio di lista_di_definizioni:  [['negative', 'emotion', ''], ['Reaction', 'anger', 'violence', 'oneself', 'others', 'arising', 'forms', 'feelings']]
    for definizione in lista_di_definizioni:
        while ("" in definizione):
            definizione.remove("")
        nuova_lista_di_definizioni.append(definizione)

    return nuova_lista_di_definizioni




def calcolo_somma_frequenze_delle_prime_n_parole_piu_frequenti(lista_definizioni_per_concetto_corrente, n):

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

    print("")
    print("")
    print("")
    print("dizionario_parole_definizioni_con_frequenza:")
    print(dizionario_parole_definizioni_con_frequenza)
    print("")

    #Adesso prendo le 5 parole più frequenti
    sorted_dizionario_parole_definizioni_con_frequenza = dict(sorted(dizionario_parole_definizioni_con_frequenza.items(), key=operator.itemgetter(1), reverse=True))
    print("sorted_dizionario_parole_definizioni_con_frequenza: ")
    print(sorted_dizionario_parole_definizioni_con_frequenza)
    print("")

    prime_n_parole_piu_frequenti = list(sorted_dizionario_parole_definizioni_con_frequenza)[:n]
    print("Le prime " + str(n) + " parole più frequenti:")
    print(prime_n_parole_piu_frequenti)
    print("")
    print("")
    print("")

    somma_frequenze_delle_prime_n_parole = 0
    for parola in prime_n_parole_piu_frequenti:
        frequenza_parola_corrente = sorted_dizionario_parole_definizioni_con_frequenza[parola]
        somma_frequenze_delle_prime_n_parole = somma_frequenze_delle_prime_n_parole + frequenza_parola_corrente

    #print("somma_frequenze_delle_prime_n_parole: ", somma_frequenze_delle_prime_n_parole)


    return somma_frequenze_delle_prime_n_parole




def calcolo_score_di_sovrapposizione_tra_i_due_concetti_correnti(lista_definizioni_per_la_coppia_di_concetti_corrente):

    #ESEMPIO di lista_definizioni_per_la_coppia_di_concetti_corrente (in questo caso Person-Brick):
    # [

    # Inizio termini per Person:
    # [
    # ['Human', ''], ['Human'],
    #   ['The', 'generic', 'person', 'human,', 'describe', 'single', 'human', 'precise', 'feature'], ['human'],
    #   ['Living', 'human', 'belonging', 'group', 'society'], ['Mammal', 'descending', 'ape'],
    #   ['Living', 'entity,', 'human', 'being,', 'sentient.'], ['A', 'human', 'being.'],
    #   ['human'], ['human'], ['human', ''], ['living'], ['human', 'characteristic'], ['human', 'being,', 'individual'],
    #   ['animal', 'feeling'], ['human'], ['human', ''], ['Person', 'human'], ['A', 'person', 'human'],
    #   ['person', 'human'], ['Member', 'homo', 'sapiens', ''], ['human'], ['human'],
    #   ['An', 'individual', 'homo', 'sapiens', 'specie'], ['A', 'human'], ['human'], ['Human', 'being,', 'man', 'woman'],
    #   ['A', 'specific', 'human'], ['Human', ''], ['living', 'entity'],
    #   ['There', 'single', 'answer', 'question', 'mean', 'human', 'vary', 'person', 'person', 'Some', 'may', 'say',
    #    'human', 'defined', 'certain', 'physical', 'characteristics,', 'ability', 'walk', 'upright', 'two', 'legs,',
    #    'certain', 'cognitive', 'abilities,', 'ability', 'think', 'reason.', 'Others', 'may', 'say', 'human', 'certain',
    #    'emotion', 'experiences,', 'love,', 'compassion,', 'happiness.', 'Ultimately,', 'mean', 'human', 'complex',
    #    'unique', 'question', 'individual', 'must', 'answer', 'themselves.']
    #    ],
    #    #Fine termini per Person:

    # Inizio termini per Brick:
    #  [
    #  ['object', 'made', 'material', '(e.g.', 'clay),', 'usually', 'aim', 'constructing', 'building'],
    #   ['block', 'material,', 'used', 'construction'],
    #   ['It’s', 'object', 'basic', 'element', 'construction,', 'like', 'building'],
    #   ['piece', 'material', 'used', 'build', 'something'],
    #   ['Parallelepiped', 'object', 'used', 'construction', 'building'],
    #   ['Construction', 'tool', 'resistnat', 'material', 'polygonal', 'shape'],
    #   ['Material', 'used', 'construction', 'buildings,', 'different', 'shape', 'size'],
    #   ['An', 'object', 'used', 'build', 'wall'], ['Red', 'object', 'used', 'build', 'construction'],
    #   ['block', 'material', '(e.i.', 'clay)', 'generally', 'used', 'cunstruction', 'building'],
    #   ['Object', 'used', 'construction', 'Es.', 'Brick', 'wall'],
    #   ['phyisical', 'object', 'usually', 'made', 'clay', 'used', 'build', 'house'],
    #   ['physical', 'material', 'house', 'construction'], ['object', 'used', 'construction', '(house', 'well', 'eg.)'],
    #   ['object', 'used', 'costruction', 'buildings,', 'made', 'clay', 'material'], ['Part', 'build'],
    #   ['block', 'material', ''], ['object', 'used', 'build', 'something', 'like', 'building'],
    #   ['Block', 'material', 'used', 'building', 'construction'],
    #   ['A', 'brick', 'object', 'used', 'construction', 'building'],
    #   ['block', 'material', 'used', 'build', 'construction'], ['Object', 'used', 'element', 'build', 'thing'],
    #   ['material', 'made', 'clay', 'used', 'build', 'structure'], ['piece', 'material', 'used', 'build', 'something'],
    #   ['An', 'object', 'usually', 'used', 'constructing', 'buildings,', 'usually', 'rectangular-shaped'],
    #   ['A', 'rectangular-shaped', 'object', 'made', 'clay', 'used', 'build', 'construction'],
    #   ['material', 'used', 'construction'],
    #   ['small', 'rectangular', 'block', 'typically', 'made', 'fired', 'sun-dried', 'clay,', 'used', 'building'],
    #   ['Material', 'used', 'construction'], ['An', 'object', 'made', 'build', 'something', ''],
    #   ['object', 'used', 'build', 'something'],
    #   ['A', 'brick', 'rectangular', 'block', 'ceramic', 'material', 'used', 'construction']
    #   ]
    #   Fine termini per Brick:
    #
    #   ]

    lista_definizioni_concetto_1 = lista_definizioni_per_la_coppia_di_concetti_corrente[0]
    lista_definizioni_concetto_2 = lista_definizioni_per_la_coppia_di_concetti_corrente[1]
    dizionario_frequenza_parole_nelle_definizioni_concetto_1 = {} #conterrà tutte le frequenze delle parole di tutte le definizioni del concetto 1
    dizionario_frequenza_parole_nelle_definizioni_concetto_2 = {} #conterrà tutte le frequenze delle parole di tutte le definizioni del concetto 2

    for definizione_1 in lista_definizioni_concetto_1:

        parole_considerate_gia_nella_definizione_corrente = []

        for parola_1 in definizione_1:
            if (parola_1.lower() not in parole_considerate_gia_nella_definizione_corrente):  # se la parola corrente non l'ho già considerata nella definizione corrente allora faccio quello
                # detto qui sotto, altrimenti passo alla parola successiva della definizione corrente. (In questo modo sono certo di considerare al più una sola volta una stessa parola
                # in ogni definizione).

                if (parola_1.lower() in dizionario_frequenza_parole_nelle_definizioni_concetto_1):
                    # vuol dire che la parola è già presente nel dizionario e quindi mi basta aumentare la sua frequenza:
                    dizionario_frequenza_parole_nelle_definizioni_concetto_1[parola_1.lower()] = dizionario_frequenza_parole_nelle_definizioni_concetto_1[parola_1.lower()] + 1
                else:
                    # vuol dire che la parola non è presente nel dizionario e quindi la devo aggiungere e inserisco la sua frequenza corrente che in questo caso sarà 1:
                    dizionario_frequenza_parole_nelle_definizioni_concetto_1[parola_1.lower()] = 1

                parole_considerate_gia_nella_definizione_corrente.append(parola_1.lower())  # aggiungo la parola alla lista per ricordarmi che questa l'ho già considerata nella definizione
                # corrente.



    for definizione_2 in lista_definizioni_concetto_2:

        parole_considerate_gia_nella_definizione_corrente = []

        for parola_2 in definizione_2:
            if (parola_2.lower() not in parole_considerate_gia_nella_definizione_corrente):  # se la parola corrente non l'ho già considerata nella definizione corrente allora faccio quello
                # detto qui sotto, altrimenti passo alla parola successiva della definizione corrente. (In questo modo sono certo di considerare al più una sola volta una stessa parola
                #in ogni definizione).

                if (parola_2.lower() in dizionario_frequenza_parole_nelle_definizioni_concetto_2):
                    # vuol dire che la parola è già presente nel dizionario e quindi mi basta aumentare la sua frequenza:
                    dizionario_frequenza_parole_nelle_definizioni_concetto_2[parola_2.lower()] = dizionario_frequenza_parole_nelle_definizioni_concetto_2[parola_2.lower()] + 1
                else:
                    # vuol dire che la parola non è presente nel dizionario e quindi la devo aggiungere e inserisco la sua frequenza corrente che in questo caso sarà 1:
                    dizionario_frequenza_parole_nelle_definizioni_concetto_2[parola_2.lower()] = 1

                parole_considerate_gia_nella_definizione_corrente.append(parola_2.lower())  # aggiungo la parola alla lista per ricordarmi che questa l'ho già considerata nella definizione
                # corrente.


    print("")
    print("")
    print("")
    sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_1 = dict(sorted(dizionario_frequenza_parole_nelle_definizioni_concetto_1.items(), key=operator.itemgetter(1), reverse=True))
    sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_2 = dict(sorted(dizionario_frequenza_parole_nelle_definizioni_concetto_2.items(), key=operator.itemgetter(1),reverse=True))

    print("sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_1:")
    print(sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_1)
    print("sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_2:")
    print(sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_2)
    print("")

    #- ADESSO FACCIO L'OVERLAP TRA LE PRIME n parole più frequenti dei 2 concetti presenti NEI DUE DIZIONARI PER VEDERE QUAL E' LA SOVRAPPOSIZIONE TRA I DUE CONCETTI INIZIALI SECONDO LE DEFINIZIONI DI ENTRAMBI
    # I CONCETTI:
    prime_n_parole_piu_frequenti_concetto_1 = list(sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_1)
    prime_n_parole_piu_frequenti_concetto_2 = list(sorted_dizionario_frequenza_parole_nelle_definizioni_concetto_2)

    print("prime_n_parole_piu_frequenti_concetto_1:")
    print(prime_n_parole_piu_frequenti_concetto_1)
    print("prime_n_parole_piu_frequenti_concetto_2:")
    print(prime_n_parole_piu_frequenti_concetto_2)

    num_di_parole_in_comune_tra_i_due_concetti = 0
    for el1 in prime_n_parole_piu_frequenti_concetto_1:
        for el2 in prime_n_parole_piu_frequenti_concetto_2:
            if(el1 == el2):
                #print("OVERLAP!!!")
                #print(el1, el2)
                num_di_parole_in_comune_tra_i_due_concetti += 1


    #ORA NORMALIZZO LO SCORE DI SOVRAPPOSIZIONE IN BASE ALLA LUNGHEZZA DELLA LISTA PIU' PICCOLA TRA QUELLA DEI DUE CONCETTI:
    if(len(prime_n_parole_piu_frequenti_concetto_1) < len(prime_n_parole_piu_frequenti_concetto_2)):
        denominatore = len(prime_n_parole_piu_frequenti_concetto_1)
    else:
        denominatore = len(prime_n_parole_piu_frequenti_concetto_2)


    score_di_sovrapposizione_per_i_due_concetti_correnti = num_di_parole_in_comune_tra_i_due_concetti/denominatore
    print("score di sovrapposizione: ", score_di_sovrapposizione_per_i_due_concetti_correnti)


    return score_di_sovrapposizione_per_i_due_concetti_correnti



#Prende in input: nome concetto corrente, lista_definizioni_per_concetto_corrente (che è una lista di liste in cui ogni lista interna è una lista di parole di una certa frase).
#Restituisce: lista_definizioni_per_concetto_corrente senza concetto_corrente.
def eliminazione_cicolarita_diretta(concetto_corrente, lista_definizioni_per_concetto_corrente):
    nuova_lista_definizioni_per_concetto_corrente = []
    for lista_parole_frase_corrente in lista_definizioni_per_concetto_corrente:
        nuova_lista_parole_frase_corrente = []
        for parola in lista_parole_frase_corrente:
            if(parola.lower() != concetto_corrente.lower()):
                nuova_lista_parole_frase_corrente.append(parola)

        nuova_lista_definizioni_per_concetto_corrente.append(nuova_lista_parole_frase_corrente)

    return nuova_lista_definizioni_per_concetto_corrente



if __name__ == '__main__':

    ################################################################################################################################################################################
    # PARTE 1: CALCOLO SIMILARITA' TRA LE DEFINIZIONI CREATE:

    definizioni_df = pd.ExcelFile("definizioni.xlsx").parse("Foglio1")
    print("definizioni_df:")
    print(definizioni_df)
    dizionario_similarita_per_ogni_concetto = {"Emotion":0, "Person":0, "Revenge":0, "Brick":0}


    lista_definizioni_per_concetto_corrente = []
    num_max_di_definizioni = definizioni_df.shape[1] - 1 #-1 perchè la prima colonna contiene i concetti.
    for riga in range(definizioni_df.shape[0]):
        print("")
        print("")
        print("")
        #if(riga == 0): #poi la toglierai
        lista_definizioni_per_concetto_corrente = []
        concetto_corrente = definizioni_df["Unnamed: 0"].iloc[riga]
        print("Concetto corrente: ", concetto_corrente)
        for colonna in range(1, definizioni_df.shape[1]):
            lista_definizioni_per_concetto_corrente.append(definizioni_df.iloc[riga:riga+1, colonna:colonna+1].values[0][0])


        ########################################################################################################################
        print("lista_definizioni_per_concetto_corrente PRIMA DELLA RIMOZIONE DELLA PUNTEGGIATURA: ")
        print(lista_definizioni_per_concetto_corrente)

        lista_definizioni_per_concetto_corrente = rimozione_punteggiatura(lista_definizioni_per_concetto_corrente)

        print("lista_definizioni_per_concetto_corrente DOPO RIMOZIONE PUNTEGGIATURA: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        print("")
        ########################################################################################################################


        ########################################################################################################################
        print("lista_definizioni_per_concetto_corrente PRIMA: ")
        print(lista_definizioni_per_concetto_corrente)

        #Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
        for i in range (0, len(lista_definizioni_per_concetto_corrente)):
            definizione_corrente = lista_definizioni_per_concetto_corrente[i]
            definizione_corrente = definizione_corrente.split(" ")
            print("definizione_corrente: ")
            print(definizione_corrente)
            print("")
            print("")
            # Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
            lista_definizioni_per_concetto_corrente[i] = [word for word in definizione_corrente if word not in stopwords.words('english') and word.lower() != 'a' and word.lower() != 'the' and word.lower() != 'an']


        print("lista_definizioni_per_concetto_corrente senza stop words: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        ########################################################################################################################


        ########################################################################################################################
        # Adesso elimino tutte le stringhe vuote nelle definizioni:
        lista_definizioni_per_concetto_corrente = rimozione_stringa_vuota(lista_definizioni_per_concetto_corrente)
        print("lista_definizioni_per_concetto_corrente senza stop words e senza stringhe vuote: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        ########################################################################################################################


        ########################################################################################################################
        #Rimozione circolarità diretta:
        #- Rimuovo da ogni frase tutte le parole che sono uguali al concetto_corrente:
        lista_definizioni_per_concetto_corrente = eliminazione_cicolarita_diretta(concetto_corrente,lista_definizioni_per_concetto_corrente)
        print("lista_definizioni_per_concetto_corrente senza stop words e senza stringhe vuote e SENZA CIRCOLARITA' DIRETTA: ")
        print(lista_definizioni_per_concetto_corrente)
        print("")
        ########################################################################################################################

        #Adesso lista_definizioni_per_concetto_corrente è diventata una lista di liste in cui ogni elemento della lista iniziale è una definizione e
        #ogni definizione è a sua volta una lista di parole singole (senza stop words) che sono presenti in quella definizione.

        ########################################################################################################################
        #Adesso applico la lemmatizzazione alle parole delle definizioni:
        lemmatizer = WordNetLemmatizer()
        for definizione in lista_definizioni_per_concetto_corrente:
            for i in range(0, len(definizione)):
                definizione[i] = lemmatizer.lemmatize(definizione[i])
        ########################################################################################################################

        print("lista_definizioni_per_concetto_corrente senza stop words e dopo aver applicato la lemmatizzazione: ")
        print(lista_definizioni_per_concetto_corrente)


        ########################################################################################################################
        #Adesso trovo le parole più frequenti nelle definizioni per il concetto corrente:
        n = 5
        somma_frequenze_delle_prime_n_parole_piu_frequenti = calcolo_somma_frequenze_delle_prime_n_parole_piu_frequenti(lista_definizioni_per_concetto_corrente, n) #n=5

        #Infine calcolo lo score finale che mi dirà quanto le definizioni del concetto corrente sono simili tra loro con un valore
        # che sarà compreso tra 0 e 1:
        #- somma_frequenze_delle_prime_n_parole_piu_frequenti sarà il numeratore della formula.
        #- num_max_di_definizioni * n = sarà il denominatore della formula perchè la similarità massima ce l'avrò solamente quando tutte le definizioni (ovvero num_max_di_definizioni)
        # per il concetto corrente conterranno al proprio interno tutte le prime n parole più frequenti.
        print("somma_frequenze_delle_prime_n_parole per il concetto " + concetto_corrente + ":", somma_frequenze_delle_prime_n_parole_piu_frequenti)
        dizionario_similarita_per_ogni_concetto[concetto_corrente] = somma_frequenze_delle_prime_n_parole_piu_frequenti/(num_max_di_definizioni*n)
        ########################################################################################################################


    print("")
    print("")
    print("dizionario_similarita_per_ogni_concetto:") #STAMPO I RISULTATI DEL PUNTO 1)
    print(dizionario_similarita_per_ogni_concetto)
    print("")
    print("")

    ################################################################################################################################################################################

    ################################################################################################################################################################################
    # PARTE 2: AGGREGAZIONE SIMILARITA' SU CONCRETEZZA/SPECIFICITA':
    # ASTRATTI: GENERICO-SPECIFICO -> Emotion-Revenge
    # CONCRETI: GENERICO-SPECIFICO -> Person-Brick
    # SPECIFICI: ASTRATTO-CONCRETO -> Revenge-Brick
    # GENERICI: ASTRATTO-CONCRETO -> Emotion-Person

    dizionario_similarita_di_aggregazione = {"Emotion-Revenge":0, "Person-Brick":0, "Revenge-Brick":0, "Emotion-Person":0} #astratti, #concreti, #specifici, #generici

    # ASTRATTI: GENERICO-SPECIFICO -> Emotion-Revenge:
    dizionario_similarita_di_aggregazione["Emotion-Revenge"] = (dizionario_similarita_per_ogni_concetto["Emotion"] + dizionario_similarita_per_ogni_concetto["Revenge"])/2

    # CONCRETI: GENERICO-SPECIFICO -> Person-Brick:
    dizionario_similarita_di_aggregazione["Person-Brick"] = (dizionario_similarita_per_ogni_concetto["Person"] + dizionario_similarita_per_ogni_concetto["Brick"])/2

    # SPECIFICI: ASTRATTO-CONCRETO -> Revenge-Brick:
    dizionario_similarita_di_aggregazione["Revenge-Brick"] = (dizionario_similarita_per_ogni_concetto["Revenge"] + dizionario_similarita_per_ogni_concetto["Brick"])/2

    # GENERICI: ASTRATTO-CONCRETO -> Emotion-Person
    dizionario_similarita_di_aggregazione["Emotion-Person"] = (dizionario_similarita_per_ogni_concetto["Emotion"] + dizionario_similarita_per_ogni_concetto["Person"])/2

    print("dizionario_similarita_di_aggregazione:") #STAMPO I RISULTATI DEL PUNTO 2)
    print(dizionario_similarita_di_aggregazione)
    print("")
    print("")
    ################################################################################################################################################################################



    ################################################################################################################################################################################
    # - AGGIUNTA MIA...
    # - DA QUI IN POI CALCOLO L'OVERLAP TRA LE PRIME n parole più frequenti delle coppie di concetti aggregati SU CONCRETEZZA/SPECIFICITA', PER VEDERE
    # QUAL E' LA SOVRAPPOSIZIONE TRA I DUE CONCETTI INIZIALI SECONDO LE DEFINIZIONI DI ENTRAMBI I CONCETTI.
    # QUINDI DI FATTO STO CALCOLANDO LA SIMILARITA' RISPETTO ALLE DEFINIZIONI DATE PER OGNI COPPIA DI CONCETTI AGGREGATI SULLE DUE DIMENSIONI SOPRA CITATE.

    #All'inizio la prima coppia per la quale calcolo la similarità sarà Person e Brick:
    dizionario_similarita_coppie_di_concetti = {"Emotion-Revenge": 0, "Person-Brick": 0, "Revenge-Brick": 0, "Emotion-Person": 0}
    num_max_di_definizioni = 2*(definizioni_df.shape[1] - 1) #-1 perchè la prima colonna contiene i concetti, 2* c'è perchè adesso sto considerando una coppia di concetti quindi il numero massimo
    #di colonne deve essere moltiplicato per 2.
    righe_per_la_coppia_Person_Brick = [1,3] #"Person-Brick" --> Person in riga 1, Break in riga 3 del dataframe.
    righe_per_la_coppia_Emotion_Person = [0,1]
    righe_per_la_coppia_Revenge_Brick = [2,3]
    righe_per_la_coppia_Emotion_Revenge = [0,2]

    lista_di_coppie_di_concetti = [ [righe_per_la_coppia_Person_Brick], [righe_per_la_coppia_Emotion_Person], [righe_per_la_coppia_Revenge_Brick], [righe_per_la_coppia_Emotion_Revenge] ]

    for coppia_concetti_corrente in lista_di_coppie_di_concetti:
        for lista_righe_concetti_correnti in coppia_concetti_corrente:

            concetto_corrente_1 = definizioni_df["Unnamed: 0"].iloc[lista_righe_concetti_correnti[0]]
            concetto_corrente_2 = definizioni_df["Unnamed: 0"].iloc[lista_righe_concetti_correnti[1]]
            lista_definizioni_per_la_coppia_di_concetti_corrente = []  # conterrà ad esempio durante la prima iterata tutte le definizioni sia di Person che di Brick insieme.
            print("concetto_corrente_1: ", concetto_corrente_1)
            print("concetto_corrente_2: ", concetto_corrente_2)


            for riga in lista_righe_concetti_correnti:
                print("")
                print("")
                print("")
                #if(riga == 0): #poi la toglierai
                lista_definizioni_per_concetto_corrente = []

                # concetto_corrente_1 = definizioni_df["Unnamed: 0"].iloc[riga]
                # concetto_corrente_2 = definizioni_df["Unnamed: 0"].iloc[riga]
                # print("concetto_corrente_1: ", concetto_corrente_1)
                # print("concetto_corrente_2: ", concetto_corrente_2)

                for colonna in range(1, definizioni_df.shape[1]):
                    lista_definizioni_per_concetto_corrente.append(definizioni_df.iloc[riga:riga+1, colonna:colonna+1].values[0][0])

                ########################################################################################################################
                print("lista_definizioni_per_concetto_corrente PRIMA DELLA RIMOZIONE DELLA PUNTEGGIATURA: ")
                print(lista_definizioni_per_concetto_corrente)

                lista_definizioni_per_concetto_corrente = rimozione_punteggiatura(lista_definizioni_per_concetto_corrente)

                print("lista_definizioni_per_concetto_corrente DOPO RIMOZIONE PUNTEGGIATURA: ")
                print(lista_definizioni_per_concetto_corrente)
                print("")
                print("")
                ########################################################################################################################


                #Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
                for i in range (0, len(lista_definizioni_per_concetto_corrente)):
                    definizione_corrente = lista_definizioni_per_concetto_corrente[i]
                    definizione_corrente = definizione_corrente.split(" ")
                    print("definizione_corrente: ")
                    print(definizione_corrente)
                    print("")
                    print("")
                    # Tolgo le stopwords dalle definizioni ottenute per il concetto corrente:
                    lista_definizioni_per_concetto_corrente[i] = [word for word in definizione_corrente if word not in stopwords.words('english') and word.lower() != 'a' and word.lower() != 'the' and word.lower() != 'an']

                print("lista_definizioni_per_concetto_corrente senza stop words per coppia di concetti: ")
                print(lista_definizioni_per_concetto_corrente)
                print("")
                ########################################################################################################################


                ########################################################################################################################
                #Adesso elimino tutte le stringhe vuote nelle definizioni:
                lista_definizioni_per_concetto_corrente = rimozione_stringa_vuota(lista_definizioni_per_concetto_corrente)
                print("lista_definizioni_per_concetto_corrente senza stop words e senza stringhe vuote: ")
                print(lista_definizioni_per_concetto_corrente)
                print("")
                ########################################################################################################################


                #Adesso lista_definizioni_per_concetto_corrente è diventata una lista di liste in cui ogni elemento della lista iniziale è una definizione e
                #ogni definizione è a sua volta una lista di parole singole (senza stop words) che sono presenti in quella definizione.


                ########################################################################################################################
                #Adesso applico la lemmatizzazione alle parole delle definizioni:
                lemmatizer = WordNetLemmatizer()
                for definizione in lista_definizioni_per_concetto_corrente:
                    for i in range(0, len(definizione)):
                        definizione[i] = lemmatizer.lemmatize(definizione[i])
                ########################################################################################################################

                print("lista_definizioni_per_concetto_corrente senza stop words e dopo aver applicato la lemmatizzazione: ")
                print(lista_definizioni_per_concetto_corrente)

                lista_definizioni_per_la_coppia_di_concetti_corrente.append(lista_definizioni_per_concetto_corrente)

            print("")
            print("")
            print("")
            print("lista_definizioni_per_la_coppia_di_concetti_corrente:")
            print(lista_definizioni_per_la_coppia_di_concetti_corrente)
            print("")
            print("lista_definizioni_per_la_coppia_di_concetti_corrente:")
            print(lista_definizioni_per_la_coppia_di_concetti_corrente[0])
            print("lista_definizioni_per_la_coppia_di_concetti_corrente:")
            print(lista_definizioni_per_la_coppia_di_concetti_corrente[1])

            #n = 5
            # prime_n_parole_piu_frequenti_per_una_coppia_di_concetti = n_parole_piu_frequenti_in_una_lista_definizioni_per_una_coppia_di_concetti(lista_definizioni_per_la_coppia_di_concetti_corrente, n, concetto_corrente_1, concetto_corrente_2)
            score_di_sovrapposizione_tra_i_due_concetti_correnti = calcolo_score_di_sovrapposizione_tra_i_due_concetti_correnti(lista_definizioni_per_la_coppia_di_concetti_corrente)

            print("")
            print("")
            print("Lo score di sovrapposizione tra i due concetti_correnti ("+ concetto_corrente_1 + " e " + concetto_corrente_2+ ") è il seguente: ", score_di_sovrapposizione_tra_i_due_concetti_correnti)

            ########################################################################################################################
            # print("")
            # print("")
            # print("num_definizioni_con_parole_piu_frequenti (sarebbe il Numeratore score di similarità): ", somma_prime_n_parole_piu_frequenti_per_una_coppia_di_concetti)
            # print("num_max_di_definizioni considerando la coppia di concetti: ", num_max_di_definizioni)
            # print("numero delle prima parole considerate (ovvero valore di n): ", n)
            # print("Denominatore score di similarità (num_max_di_definizioni*n): ", num_max_di_definizioni*n)
            dizionario_similarita_coppie_di_concetti[str(concetto_corrente_1)+"-"+str(concetto_corrente_2)] = score_di_sovrapposizione_tra_i_due_concetti_correnti
            ########################################################################################################################


    print("")
    print("")
    print("")
    print("")
    print("dizionario_similarita_coppie_di_concetti:") ##STAMPO I RISULTATI DEL PUNTO 3)
    print(dizionario_similarita_coppie_di_concetti)
    ################################################################################################################################################################################