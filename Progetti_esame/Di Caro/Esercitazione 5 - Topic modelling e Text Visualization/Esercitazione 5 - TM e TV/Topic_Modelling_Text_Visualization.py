from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from gensim import corpora
from gensim import models
import pyLDAvis.gensim_models
import gensim
import re

#funzione che rimuove la punteggiatura da un documento (che sarà una lista di liste dove le liste interne sono le frasi)
def rimozione_punteggiatura_da_un_documento(documento):

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~\n'''
    nuovo_documento = []

    for frase in documento:
        nuova_frase = []
        #for i in range(0, len(frase)):
        frase_splittata = frase.split(" ")
        for parola in frase_splittata:
            parola_corrente = ""
            for c in parola:  # per ogni carattere della parola corrente
                non_aggiungere_carattere = False
                for el in punc:
                    if el == c:
                        non_aggiungere_carattere = True
                if not non_aggiungere_carattere:
                    parola_corrente = parola_corrente + str(c)

            nuova_frase.append(parola_corrente)

        nuovo_documento.append(nuova_frase)

    return nuovo_documento


#Funzione che prende in input la lista di frasi del documento e restituisce una nuova lista di documenti in cui ogni documento è praticamente una riga presente in "documenti TM-TV.txt".
def get_frasi(lista_frasi_documento):

    nuova_lista_frasi_documento = []
    for frasi in lista_frasi_documento:
        lista_frasi = frasi.split("\n")
        for frase in lista_frasi:
            nuova_lista_frasi_documento.append(frase)

    return nuova_lista_frasi_documento


#l'input di questa funzione è una lista di frasi dove ogni frase è a sua volta una lista di parole.
def rimozione_stringa_vuota_da_una_lista_di_frasi(lista_frasi_documento):
    # print("definizione in rimozione_stringa_vuota_da_una_lista:")
    # print(definizione)
    nuova_lista_frasi_documento = []
    for frase in lista_frasi_documento:
        for parola in frase:
            if(parola == ""):
                frase.remove('')
        if(frase != []):
            nuova_lista_frasi_documento.append(frase)

    return nuova_lista_frasi_documento



#l'input di questa funzione è una lista di liste in cui le liste interne sono le sequenze di parole di ogni frase.
def eliminazione_stop_words_dal_documento(lista_frasi_documento):
    nuova_lista_frasi_documento = []
    for lista_parole_frase_corrente in lista_frasi_documento:
        nuova_lista_parole_frase_senza_sw = [word for word in lista_parole_frase_corrente if word.lower() not in stopwords.words('english')]
        nuova_lista_frasi_documento.append(nuova_lista_parole_frase_senza_sw)

    return nuova_lista_frasi_documento


#l'input di questa funzione è una lista di liste in cui le liste interne sono le sequenze di parole di ogni frase.
def lemmatizzazione_parole_frasi_documento(lista_frasi_documento):
    lemmatizer = WordNetLemmatizer()
    nuova_lista_frasi_documento = []

    for lista_parole_frase_corrente in lista_frasi_documento:
        nuova_lista_parole_lemmatizzate_frase_corrente = []
        for i in range(0, len(lista_parole_frase_corrente)):
            nuova_lista_parole_lemmatizzate_frase_corrente.append(lemmatizer.lemmatize(lista_parole_frase_corrente[i].lower()))
        nuova_lista_frasi_documento.append(nuova_lista_parole_lemmatizzate_frase_corrente)

    return nuova_lista_frasi_documento


def get_parole_cluster_corrente(cluster):
    #Devo prendere solamente le parole che sono presenti tra "".
    lista_termini_cluster = re.findall('"(.+?)"', str(cluster))

    return lista_termini_cluster


def get_cluster_documento(lista_termini_documento, cluster_0, cluster_1, cluster_2):
    sim_cluster_0 = 0
    for termine_cluster in cluster_0:
        for termine_documento in lista_termini_documento:
            if(termine_cluster == termine_documento):
                sim_cluster_0+=1

    sim_cluster_1 = 0
    for termine_cluster in cluster_1:
        for termine_documento in lista_termini_documento:
            if (termine_cluster == termine_documento):
                sim_cluster_1 += 1

    sim_cluster_2 = 0
    for termine_cluster in cluster_2:
        for termine_documento in lista_termini_documento:
            if (termine_cluster == termine_documento):
                sim_cluster_2 += 1


    print("sim_cluster_0: ", sim_cluster_0)
    print("sim_cluster_1: ", sim_cluster_1)
    print("sim_cluster_2: ", sim_cluster_2)
    if(sim_cluster_0 > sim_cluster_1):
        if(sim_cluster_0 > sim_cluster_2): best_cluster=0
        else: best_cluster=2
    else:
        if(sim_cluster_1 > sim_cluster_2): best_cluster=1
        else: best_cluster=2


    return best_cluster



if __name__ == '__main__':

    path_documento = "Risorse_Topic_Modelling_Text_Visualization\\documenti TM-TV.txt"
    lista_frasi_documento = []
    with open(path_documento, 'r', encoding="UTF-8") as documento:
        for frase in documento:
            lista_frasi_documento.append(frase)
    documento.close()


    #Creo una lista di liste dove ogni lista interna sarà un documento.
    #IN QUESTA ESERCITAZIONE OGNI RIGA DEL FILE CHIAMATO "documenti TM-TV.txt" corrisponderà ad un documento.
    #Ho deciso di fare questo in modo tale da avere un pò più di una frase per ogni documento riguardante un certo topic.
    lista_frasi_documento = get_frasi(lista_frasi_documento) #get_frasi è la funzione che mi permette di considerare ogni riga di "documenti TM-TV.txt" come un unico documento (che ovviamente parlerà di un certo argomento)
    print("lista_frasi_documento:")
    print(lista_frasi_documento)
    print("")


    # #1) rimuovo la punteggiatura e i caratteri inutili dalle frasi del documento:
    lista_frasi_documento = rimozione_punteggiatura_da_un_documento(lista_frasi_documento)
    print("lista_frasi_documento pulita: ", lista_frasi_documento)
    print("")

    # 2) elimino la stringa vuota da ogni frase del documento:
    lista_frasi_documento = rimozione_stringa_vuota_da_una_lista_di_frasi(lista_frasi_documento)
    print("lista_frasi_documento dopo rimozione stringa vuota: ", lista_frasi_documento)
    print("")

    #3 elimino le stop words dalle frasi presenti nel documento:
    lista_frasi_documento = eliminazione_stop_words_dal_documento(lista_frasi_documento)
    print("lista_frasi_documento dopo elimin. sw: ", lista_frasi_documento)
    print("")


    #4 lemmatizzo le parole delle frasi presenti nel documento:
    lista_frasi_documento = lemmatizzazione_parole_frasi_documento(lista_frasi_documento)
    print("lista_frasi_documento dopo lemmatizzazione: ", lista_frasi_documento)
    print("")
    print("")
    print("")


    #4) Elimino da lista_frasi_documento tutte le parole che compaiono 1 sola volta:
    frequency = defaultdict(int)
    for lista_parole_frase_corrente in lista_frasi_documento:
        for token in lista_parole_frase_corrente:
            frequency[token] += 1

    print("dizionario frequenza parole nella collezione di documenti: ")
    print(frequency)
    print("")


    lista_frasi_documento = [
        [token for token in text if frequency[token] > 1]
        for text in lista_frasi_documento
    ]

    print("lista_frasi_documento:")
    print(lista_frasi_documento)
    print("")
    ################################################################################

    #5)
    #dizionario: conterrà il mapping tra ogni parola e il suo id univoco:
    dizionario = corpora.Dictionary(lista_frasi_documento)
    # print("dizionario[0]:")
    # print(dizionario[0])
    print("Parole presenti nel dizionario (Parola:idUnivoco):")
    print(dizionario.token2id)
    print("")

    # DOPO L'ESECUZIONE DELLA FUNZIONE doc2bow nella lista di liste chiamata corpus memorizzo questo:
    # - corpus è una lista di liste in cui OGNI LISTA INTERNA corrisponde AD UN DOCUMENTO DELLA COLLEZIONE.
    # - in corpus OGNI DOCUMENTO E' STATO VETTORIZZATO IN UN VETTORE tf (time-frequency).
    # - sempre in corpus, ogni vettore (quindi ogni documento) contiene delle coppie fatte in questo modo:
    #   (0,1), (1, 1), (2, 1), (3, 1), (4, 2), ecc...
    #   in cui il primo valore di ogni coppia corrisponde all'intendificativo univoco della parola (ad es. nel mio esempio 0:"behavior") mentre il secondo valore della coppia indica semplicemente
    #   la frequenza di tale parola nel documento considerato.
    # - chiaramente se un certo indice di una certa parola non è presente nel vettore rappresentante un certo documento, vuol dire che QUELLA PAROLA NON E' PRESENTE NEL DOCUMENTO CONSIDERATO.

    corpus = [dizionario.doc2bow(text) for text in lista_frasi_documento]
    print("corpus:")
    print(corpus)
    print("")
    #Stampo il corpus (per facilitare la comprensione) che per ogni documento mi dice quali sono le parole in essa contenuta e con quale frequenza:
    corpus_readable = [[(dizionario[id], freq) for id, freq in cp] for cp in corpus]
    print("corpus human-readable:")
    print(corpus_readable)
    print("")
    print("")


    # # #6): applico la trasformazione tf-idf ai documenti del corpus
    # tfidf = models.TfidfModel(corpus)  # step 1
    # corpus_tfidf = tfidf[corpus]
    # print("corpus_tfidf (Ogni vettore tf-idf qui sotto, rappresenta un documento.")
    # for doc in corpus_tfidf:
    #     print(doc)
    # print("")


    ########################################
    #Applicazione tecnica LDA:
    # update_every: Number of documents to be iterated through for each update.
    # chunksize: Number of documents to be used in each training chunk.
    # passes: Number of passes through the corpus during training.
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dizionario, num_topics=3, update_every=12, chunksize=12, passes=12)
    #lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dizionario, num_topics=3)
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dizionario)
    #pyLDAvis.save_html(vis, 'Risorse_Topic_Modelling_Text_Visualization\\Risultati visualizzazione TM-TV.html') #SALVO i topics trovati
    ########################################

    print("")
    print("lda_model topics trovati:")
    print(lda_model.print_topics())
    print(type(lda_model.print_topics()))

    #Passi successivi:
    # 1) Considero tutte le parole presenti in un certo topics come un cluster (cluster_0 = music, cluster_1 = physics, cluster_2 = Artificial Intelligence.
    # 2) Dopodichè applico un algoritmo di clustering per associare ogni documento presente nel mio copus (documenti Ym-TV.txt) ad un certo cluster.

    #1)
    cluster_0 = lda_model.print_topics()[0]
    cluster_1 = lda_model.print_topics()[1]
    cluster_2 = lda_model.print_topics()[2]

    cluster_0 = get_parole_cluster_corrente(cluster_0)
    cluster_1 = get_parole_cluster_corrente(cluster_1)
    cluster_2 = get_parole_cluster_corrente(cluster_2)

    #Stampo quelli che per me saranno i centroidi di ogni cluster:
    print("termini cluster_0: ", cluster_0)
    print("termini cluster_1: ", cluster_1)
    print("termini cluster_2: ", cluster_2)
    print("")


    #2)
    documenti_cluster_0 = []
    documenti_cluster_1 = []
    documenti_cluster_2 = []
    indice_documento_corrente = 0
    for lista_termini_documento in lista_frasi_documento:
        cluster_documento_corrente = get_cluster_documento(lista_termini_documento, cluster_0, cluster_1, cluster_2)
        print("indice_documento_corrente: ", indice_documento_corrente)
        print("cluster_documento_corrente: ", cluster_documento_corrente)
        indice_documento_corrente+=1
        print("")