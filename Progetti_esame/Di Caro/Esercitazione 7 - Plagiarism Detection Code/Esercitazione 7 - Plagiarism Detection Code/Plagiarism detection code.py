from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pylcs



def get_file_text(path_file):
    testo_file = []
    with open(path_file, 'r', encoding="UTF-8") as file:
        for frase in file:
            testo_file.append(frase)
    file.close()

    return testo_file


#L'input della funzione è una lista di liste in cui ogni lista interna contiene tutte le parole usate in una certa istruzione del codice che si trova su una certa riga.
def rimozione_stringa_vuota(file):
    nuovo_file = []
    for lista_parole_istruzione_corrente in file:
        if(lista_parole_istruzione_corrente != ['']):
            nuovo_file.append(lista_parole_istruzione_corrente)

    #rimuovo anche le stringhe vuote eventuali che ci sono nelle liste interne:
    nuovo_file_finale = []
    for lista_parole_istruzione_corrente in nuovo_file:
        nuova_lista_parole_istruzione_corrente = []
        for parola in lista_parole_istruzione_corrente:
            if(parola != ''):
                nuova_lista_parole_istruzione_corrente.append(parola)

        nuovo_file_finale.append(nuova_lista_parole_istruzione_corrente)

    return nuovo_file_finale


#Il file di input è una lista di istruzioni, ogni istruzione è una stringa.
def rimozione_carattere_a_capo(file):
    nuovo_file = []
    for istruzione in file:
        nuova_istruzione = []
        for parola in istruzione.split(" "):
            nuova_parola = ""
            for i in range(0, len(parola)):
                if(parola[i] != "\n"):
                    nuova_parola = nuova_parola + parola[i]

            nuova_istruzione.append(nuova_parola)

        nuovo_file.append(nuova_istruzione)

    nuovo_file = rimozione_stringa_vuota(nuovo_file)

    return nuovo_file

#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
def get_nomi_classi(file):
    nomi_classi = []
    for istruzione_corrente in file:
        for i in range(0, len(istruzione_corrente)):
            if (istruzione_corrente[i] == "class"):
                # allora vuol dire che la parola successiva è sicuramente il nome di una classe:
                nome_classe = istruzione_corrente[i+1]
                nomi_classi.append(nome_classe)

    return nomi_classi


#Funzione che mi permette di eliminare la punteggiatura "):" da un argomento di una funzione:
def rimozione_punteggiatura_argomento(nome_argomento):
    nuovo_argomento = ""
    for c in nome_argomento:
        if(c != ")" and c != ":" and c != ","):
            nuovo_argomento = nuovo_argomento + c

    return nuovo_argomento



#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
#Qusta funzione restituisce sia tutti i nomi associati alle funzioni del codice python dato in input e sia i nomi dei rispettivi argomenti sottoforma di lista di liste.
def get_nomi_funzioni_e_nomi_rispettivi_argomenti(file):
    nomi_funzioni_e_nomi_rispettivi_argomenti = []

    for istruzione_corrente in file:
        for i in range(0, len(istruzione_corrente)):
            if(istruzione_corrente[i] == "def"):
                lista_nome_funzione_corrente_e_suoi_argomenti = []
                nome_funzione_e_suoi_argomenti = ""
                for j in range(i+1, len(istruzione_corrente)): #questo ciclo mi serve per poter ottenere correttamente sia il nome della funz. che quello di tutti i suoi argomenti in una stringa sola.
                    nome_funzione_e_suoi_argomenti = nome_funzione_e_suoi_argomenti + istruzione_corrente[j]

                # Allora vuol dire che adesso in nome_funzione_e_suoi_argomenti ci sarà:
                # nome_funzione(argomento1,argomento2,...):
                # print("nome_funzione_e_suoi_argomenti:")
                # print(nome_funzione_e_suoi_argomenti)
                # print("")
                # Quindi eseguo uno split su "(" per avere: ["nome_funzione", "argomento1", "argomento2",...,"argomentoFinale):"]
                lista_nome_funzione_e_argomenti = nome_funzione_e_suoi_argomenti.split("(")
                argomenti = lista_nome_funzione_e_argomenti[1]
                lista_argomenti = argomenti.split(",")
                # print("lista_nome_funzione_e_argomenti:")
                # print(lista_nome_funzione_e_argomenti)
                # print("solo lista_argomenti:")
                # print(lista_argomenti)
                # print("")
                # print("")
                # Quindi prendo il nome della funzione:
                nome_funzione = lista_nome_funzione_e_argomenti[0]
                lista_nome_funzione_corrente_e_suoi_argomenti.append(nome_funzione)

                #Adesso prendo i nomi degli argomenti della funzione corrente:
                for i in range(0, len(lista_argomenti)):
                    nome_argomento_pulito = rimozione_punteggiatura_argomento(lista_argomenti[i])
                    lista_nome_funzione_corrente_e_suoi_argomenti.append(nome_argomento_pulito)

                #Adesso posso aggiungere alla lista di liste nomi_funzioni_e_nomi_rispettivi_argomenti sia il nome della nuova funzione trovata e sia i nomi di tutti i suoi argomenti:
                nomi_funzioni_e_nomi_rispettivi_argomenti.append(lista_nome_funzione_corrente_e_suoi_argomenti) #ogni lista interna contiene il nome di una certa funzioni e quello di tutti i suoi argomenti.


    nomi_funzioni = []
    nomi_argomenti = []
    for lista_interna in nomi_funzioni_e_nomi_rispettivi_argomenti:
        nomi_funzioni.append(lista_interna[0])
        for i in range(1, len(lista_interna)):
            nomi_argomenti.append(lista_interna[i])

    return nomi_funzioni, nomi_argomenti



#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
def get_nomi_variabili(file):
    nomi_variabili = []
    for istruzione_corrente in file:
        for i in range(0, len(istruzione_corrente)):
            if (istruzione_corrente[i] == "=" or istruzione_corrente[i] == "!=" or istruzione_corrente[i] == "=="):
                # allora vuol dire che la parola precedente era sicuramente il nome di una variabile:
                nome_variabile = istruzione_corrente[i-1]
                nomi_variabili.append(nome_variabile)

    return nomi_variabili


#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
def get_nomi_librerie(file):
    nomi_librerie = []
    for istruzione_corrente in file:
        for i in range(0, len(istruzione_corrente)):
            if (istruzione_corrente[i] == "import" and istruzione_corrente[i+1] != "*"):
                # allora vuol dire che la parola successiva è sicuramente il nome di una libreria:
                nome_libreria = istruzione_corrente[i+1]
                nomi_librerie.append(nome_libreria)
            elif(istruzione_corrente[i] == "from" and istruzione_corrente[i+2] == "import"):
                # allora vuol dire che la parola che c'è in mezzo è sicuramente il nome di una libreria:
                nome_libreria = istruzione_corrente[i+1]
                nomi_librerie.append(nome_libreria)


    return nomi_librerie


#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
#L'output sarà una lista (chiamata commenti) che conterrà tutti i commenti su singola riga insieme, quindi questo vuol dire che la lista commenti
#conterrà tutte le parole insieme presenti nei commenti su singola riga.
def get_commenti_singola_riga(file):
    commenti = []
    for istruzione_corrente in file:
        for i in range(0, len(istruzione_corrente)):
            if (istruzione_corrente[i] == "#"):
                # allora vuol dire che dalla parola successiva c'è sicuramente il commento:
                if(i < len(istruzione_corrente)-1): #devo essere sicuro che dopo # ci sia un qualcosa
                    for j in range(i+1, len(istruzione_corrente)):
                        commenti.append(istruzione_corrente[j]) #aggiungo il commento alla lista commenti.

    return commenti


#L'input di questa funzione è una lista di liste in cui ogni lista interna contiene un'istruzione python.
def get_commenti_su_righe_multiple(file):
    # print("file: ")
    # print(file)
    # print("")
    commenti_su_righe_multiple = []
    start_commento_multiplo = False

    for istruzione_corrente in file:

        if((istruzione_corrente == ['"""'] or istruzione_corrente == ["'''"]) and start_commento_multiplo == False):
            start_commento_multiplo = True #vuol dire che il commento multiplo è iniziato.
            continue

        elif((istruzione_corrente == ['"""'] or istruzione_corrente == ["'''"]) and start_commento_multiplo == True):
            start_commento_multiplo = False #vuol dire che il commento multiplo è finito.
            continue

        if(start_commento_multiplo): #solo se mi trovo nel commento multiplo aggiungo le stringhe del commento nella lista chiamata commenti_su_righe_multiple.
            for stringa in istruzione_corrente:
                commenti_su_righe_multiple.append(stringa)


    return commenti_su_righe_multiple



#L'input di questa funzione è una lista di stringhe.
def rimuovi_stringa_vuota(file):
    nuovo_file = []
    for stringa in file:
        if(stringa != ''):
            nuovo_file.append(stringa)

    return nuovo_file


#L'input di questa funzione è una lista di parole.
def rimuovi_punteggiatura(file):
    nuovo_file = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~\n'''

    #print("file in rimuovi_punteggiatura:", file)

    for parola in file:
        nuova_parola = ""
        for c in parola:
            non_aggiungere_carattere = False
            for el in punc:
                if(c == el):
                    non_aggiungere_carattere = True
            if not non_aggiungere_carattere:
                nuova_parola = nuova_parola + str(c)

        nuovo_file.append(nuova_parola)

    nuovo_file = rimuovi_stringa_vuota(nuovo_file) #rimuovo anche eventuali stringhe vuote presenti nel nuovo_file

    return  nuovo_file



#L'input di questa funzione è una lista di parole che sono presenti o in commenti su righe singole o in commenti su righe multiple.
def delete_sw_e_punteggiatura_e_stringhe_vuote_commenti(file):
    file = [word for word in file if word.lower() not in stopwords.words('english')]
    file = rimuovi_punteggiatura(file)

    return file


#L'input di questa funzione è una lista di parole che sono presenti o in commenti su righe singole o in commenti su righe multiple.
def lemmatizzazione(file):
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(file)):
        file[i] = lemmatizer.lemmatize(file[i].lower())

    return file


#Mi restituisce tutte le liste date in input in un'unica stringa.
def get_string_file(nomi_classi_file, nomi_funzioni_file, nomi_argomenti_file, nomi_variabili_file, nomi_librerie_file, commenti_file):

    nomi_classi_file = ' '.join(nomi_classi_file)
    nomi_funzioni_file = ' '.join(nomi_funzioni_file)
    nomi_argomenti_file = ' '.join(nomi_argomenti_file)
    nomi_variabili_file = ' '.join(nomi_variabili_file)
    nomi_librerie_file = ' '.join(nomi_librerie_file)
    commenti_file = ' '.join(commenti_file)

    string = nomi_classi_file + " " + nomi_funzioni_file + " " + nomi_argomenti_file + " " + nomi_variabili_file + " " + nomi_librerie_file + " " + commenti_file

    return string


def delete_duplicati(corpus):
    nuovo_corpus = []
    for stringa in corpus:
        if(stringa not in nuovo_corpus):
            nuovo_corpus.append(stringa)

    return nuovo_corpus



if __name__ == '__main__':

    # Ottengo i due files .py da confrontare:
    file_originale = get_file_text("Risorse utili per Plagiarism detection code/File_originale.py") #è una lista
    file_plagio = get_file_text("Risorse utili per Plagiarism detection code/File_no_plagio.py") #è una lista
    print("file_originale:")
    print(file_originale)
    print("")
    print("file_plagio:")
    print(file_plagio)
    print("")
    print("")
    ##########################

    #Elimino dai due files tutti gli \n:
    file_originale = rimozione_carattere_a_capo(file_originale)
    file_plagio = rimozione_carattere_a_capo(file_plagio)
    print("file_originale dopo rimozione \\n:")
    print(file_originale)
    print("")
    print("file_plagio dopo rimozione \\n:")
    print(file_plagio)
    print("")
    print("")
    ##########################


    #Ottengo per entrambi i codici python:
    # - Nomi classi.
    # - Nomi funzioni e procedure.
    # - Nomi argomenti funzioni e procedure.
    # - Nomi variabili.
    # - Nomi librerie.
    # - Commenti su singole righe e su righe multiple.

    #nomi classi:
    nomi_classi_file_originale = get_nomi_classi(file_originale)
    print("nomi_classi_file_originale:")
    print(nomi_classi_file_originale)
    print("")
    nomi_classi_file_plagio = get_nomi_classi(file_plagio)
    print("nomi_classi_file_plagio:")
    print(nomi_classi_file_plagio)
    print("")
    print("")


    #nomi funzioni:
    nomi_funzioni_file_originale, nomi_argomenti_file_originale = get_nomi_funzioni_e_nomi_rispettivi_argomenti(file_originale)
    print("nomi_funzioni_file_originale:")
    print(nomi_funzioni_file_originale)
    print("nomi_argomenti_file_originale:")
    print(nomi_argomenti_file_originale)
    print("")
    nomi_funzioni_file_plagio, nomi_argomenti_file_plagio = get_nomi_funzioni_e_nomi_rispettivi_argomenti(file_plagio)
    print("nomi_funzioni_file_plagio:")
    print(nomi_funzioni_file_plagio)
    print("nomi_argomenti_file_plagio:")
    print(nomi_argomenti_file_plagio)
    print("")
    print("")


    #nomi variabili:
    nomi_variabili_file_originale = get_nomi_variabili(file_originale)
    print("nomi_variabili_file_originale:")
    print(nomi_variabili_file_originale)
    print("")
    nomi_variabili_file_plagio = get_nomi_variabili(file_plagio)
    print("nomi_variabili_file_plagio:")
    print(nomi_variabili_file_plagio)
    print("")


    #nomi librerie:
    nomi_librerie_file_originale = get_nomi_librerie(file_originale)
    print("nomi_librerie_file_originale:")
    print(nomi_librerie_file_originale)
    print("")
    nomi_librerie_file_plagio = get_nomi_librerie(file_plagio)
    print("nomi_librerie_file_plagio:")
    print(nomi_librerie_file_plagio)
    print("")
    ###############################


    #commenti su una riga:
    commenti_singola_riga_file_originale = get_commenti_singola_riga(file_originale)
    # print("commenti_singola_riga_file_originale:")
    # print(commenti_singola_riga_file_originale)
    # print("")
    commenti_singola_riga_file_plagio = get_commenti_singola_riga(file_plagio)
    # print("commenti_singola_riga_file_plagio:")
    # print(commenti_singola_riga_file_plagio)
    # print("")
    ###############################

    #commenti su righe multiple:
    commenti_righe_multiple_file_originale = get_commenti_su_righe_multiple(file_originale)
    # print("commenti_righe_multiple_file_originale:")
    # print(commenti_righe_multiple_file_originale)
    # print("")
    commenti_righe_multiple_file_plagio = get_commenti_su_righe_multiple(file_plagio)
    # print("commenti_righe_multiple_file_plagio:")
    # print(commenti_righe_multiple_file_plagio)
    # print("")
    ###############################

    #Unisco i commenti su singole righe con i commenti su righe multiple:
    commenti_file_originale = []
    commenti_file_plagio = []

    commenti_file_originale += commenti_singola_riga_file_originale
    commenti_file_originale += commenti_righe_multiple_file_originale

    commenti_file_plagio += commenti_singola_riga_file_plagio
    commenti_file_plagio += commenti_righe_multiple_file_plagio

    # print("commenti_file_originale:")
    # print(commenti_file_originale)
    # print("")
    # print("commenti_file_plagio:")
    # print(commenti_file_plagio)
    # print("")
    #####################################################################


    #rimuovo le stop words, la punteggiatura dai commenti su righe singole e su righe multiple ed eventuali stringhe vuote:
    commenti_file_originale = delete_sw_e_punteggiatura_e_stringhe_vuote_commenti(commenti_file_originale)
    # print("commenti_singola_riga_file_originale senza sw:")
    # print(commenti_file_originale)
    # print("")
    commenti_file_plagio = delete_sw_e_punteggiatura_e_stringhe_vuote_commenti(commenti_file_plagio)
    # print("commenti_file_plagio senza sw:")
    # print(commenti_file_plagio)
    # print("")
    ########################################################################


    #lemmatizzo tutte le parole rimenti per i commenti su righe singole e per quelli su righe multiple:
    #rimuovo le stop words e la punteggiatura dai commenti su righe singole e su righe multiple:
    commenti_file_originale = lemmatizzazione(commenti_file_originale)
    print("commenti_file_originale senza sw, senza punteggiatura e con lemm.:")
    print(commenti_file_originale)
    print("")
    commenti_file_plagio = lemmatizzazione(commenti_file_plagio)
    print("commenti_file_plagio senza sw, senza punteggiatura e con lemm.:")
    print(commenti_file_plagio)
    print("")
    print("")
    print("")
    ########################################################################


    # ADESSO CREO I VETTORI TF PER I DUE files python e calcolo la sim tra i due file python per vedere se c'è stato il plagio o meno.
    stringa_file_originale = get_string_file(nomi_classi_file_originale, nomi_funzioni_file_originale, nomi_argomenti_file_originale, nomi_variabili_file_originale, nomi_librerie_file_originale, commenti_file_originale)
    stringa_file_plagio = get_string_file(nomi_classi_file_plagio, nomi_funzioni_file_plagio, nomi_argomenti_file_plagio, nomi_variabili_file_plagio, nomi_librerie_file_plagio, commenti_file_plagio)

    print("")
    print("stringa_file_originale:")
    print(stringa_file_originale)
    print("")
    print("stringa_file_plagio:")
    print(stringa_file_plagio)
    print("")

    #vectorizer = TfidfVectorizer()
    vectorizer = CountVectorizer()
    vettori = vectorizer.fit_transform([stringa_file_originale, stringa_file_plagio]).toarray()

    #print(vectors)
    vettore_file_originale = vettori[0]
    vettore_file_plagio = vettori[1]

    print("vettore_file_originale in tf:")
    print(vettore_file_originale)
    print("")
    print("vettore_file_plagio in tf:")
    print(vettore_file_plagio)
    print("")
    print("")

    # print("len(vettore_file_originale): ", len(vettore_file_originale))
    # print("len(vettore_file_plagio): ", len(vettore_file_plagio))
    # print("")
    # print("")

    sim_coseno = cosine_similarity([vettore_file_originale, vettore_file_plagio])[0][1]

    print("sim_coseno: ", sim_coseno)
    ###############################################################################################################


    #Calcolo la LCS dei due script:
    LONGEST_COMMON_SUBSEQUENCE = pylcs.lcs_sequence_length(stringa_file_originale, stringa_file_plagio)
    print("LONGEST_COMMON_SUBSEQUENCE: ", LONGEST_COMMON_SUBSEQUENCE)
    num_caratteri_totali_stringa_file_originale = len(stringa_file_originale)
    print("num_caratteri_totali_stringa_file_originale: ", num_caratteri_totali_stringa_file_originale)
    score_LCS = LONGEST_COMMON_SUBSEQUENCE/num_caratteri_totali_stringa_file_originale
    print("score_LCS: ", score_LCS)
    # print("")
    # print("")

    score_medio_finale = (sim_coseno + score_LCS)/2
    print("score_medio_finale: ", score_medio_finale)
    print("")

    #Soglie:
    if (score_medio_finale > 0.50):
        print("Plagio FORTE.")
    elif (0.30 <= score_medio_finale <= 0.50):
        print("Plagio DEBOLE.")
    else:
        print("Plagio ASSENTE.")
    ###############################################################################################################