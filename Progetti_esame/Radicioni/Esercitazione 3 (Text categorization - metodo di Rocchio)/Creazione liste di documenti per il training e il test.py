import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
import os
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize import RegexpTokenizer
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import random


#Funzione che dato il nome di un documento, restituisce in output le sue parole all’interno di una lista (elimina anche i segni di punteggiatura e quindi anche i -,?,!, ecc..).
#controlla però se elimina anche < perchè nei documenti del sistema operativo ce ne sono tanti e possono essere utili per capire che quel documento appartiene a quella categoria)..
def split_to_words(input_filename):
    # read data from file
    with open(input_filename, 'r') as reader:
        input_raw_text = reader.read()
    #print('\nInput raw text is: \n{}'.format(input_raw_text))
    # split data into words
    custom_tokenizer = RegexpTokenizer('\w+')
    word_list = custom_tokenizer.tokenize(input_raw_text)
    return word_list



#Funzione per convertire una lista di input s in una stringa:
# Function to convert
def listToString(s):
    # inizializzo una stringa vuota
    str1 = " "

    # restituisco la stringa
    return (str1.join(s))



def creo_lista_documenti_training_set_e_test_set():
    lista_di_tutti_i_documenti_di_TRAINING_in_inglese = []
    lista_di_tutti_i_documenti_di_TEST_in_inglese = []
    #Scorro le varie classi e i vari documenti presenti all'interno di ogni classe:
    for cartella, sottocartelle, files in os.walk(os.getcwd()):
        if not ( (cartella.endswith("Esercitazione 3")) or (cartella.endswith("20_NGs_400")) ): #non mi devo trovare in nessuna delle due cartelle altrimenti perchè devo considerare solamente le cartelle
            #che hanno i documenti al proprio interno.
            #print(f"Ci troviamo nella cartella: '{cartella}'") #utile
            #print(f"Le sottocartelle presenti sono: '{sottocartelle}'")
            #print(f"I files presenti sono: {files}") utile

            #if(cartella.endswith("alt.atheism") or cartella.endswith("comp.graphics")):
                #seleziono in maniera randomica il 90% dei file (ovvero 18 files) di ogni classe che userò nel training set.
                # I restanti 2 files di ogni classe li inserirò nel test set:
                lista_di_indici_frasi_selezionate = random.sample(range(20), 18) #ogni elemento di questa lista sarà un valore compreso tra 0 e 19
                print("lista_di_indici_frasi_selezionate: ", lista_di_indici_frasi_selezionate)
                print("")
                indice_numerico_file_corrente = 0
                for file in files:
                    #if(file.endswith("0000000") or (file.endswith("0000001"))): #chiaramente questo ad un certo punto dovrai toglierlo.
                    if(indice_numerico_file_corrente in lista_di_indici_frasi_selezionate): #se il file corrente è presente nella lista di indici dei files di training allora continuo
                        #adesso sono sicuro di trovarmi nel primissimo documento chiamato 0000000.
                        print("Nome cartella corrente: ", cartella)
                        print("Nome file corrente: ", file)
                        #Apro il documento_corrente in lettura:
                        #documento_corrente = open(cartella+"\\"+file, "r").read() #metto la cartella perchè essa contiene tutto il percorso che mi permetterà di aprire il documento corretto.
                        #print("documento_corrente: ", documento_corrente)
                        #print("")
                        #print("")
                        documento_in_lista = split_to_words(cartella+"\\"+file)
                        print("documento in lista: ", documento_in_lista)

                        #adesso elimino le stop words presenti nel documento
                        documento_in_lista_senza_stop_words = [word for word in documento_in_lista if word not in stopwords.words('english')]
                        print("documento_in_lista_senza_stop_words: ", documento_in_lista_senza_stop_words)

                        #Adesso ho il documento in formato di lista che contiene tutte le parole del documento originale senza i segni di punteggiatura e senza le stop words.

                        #A questo punto quindi devo ottenere i lemmi di tutte le parole presenti in documento_in_lista_senza_stop_words:
                        # Istanzio il Lemmatizer
                        lemmatizer = WordNetLemmatizer()
                        # Applico il lemmatizer al documento_in_lista_senza_stop_words e aggiungo tutti i lemmi che ottengo in una lista che chiamo lista_di_lemmi_documento_corrente:
                        lista_di_lemmi_documento_corrente = [] #conterrà i lemmi delle parole del documento corrente.
                        for word in documento_in_lista_senza_stop_words:
                            lista_di_lemmi_documento_corrente.append(lemmatizer.lemmatize(word))
                        print("lista_di_lemmi_documento_corrente: ", lista_di_lemmi_documento_corrente)

                        #Adesso ho la lista di lemmi del documento corrente. (puoi ancora migliorare la lemmatizzazione volendo)

                        #Prima però devo trasformare la lista corrente in una stringa:
                        stringa_di_lemmi_documento_corrente = listToString(lista_di_lemmi_documento_corrente)
                        print("stringa_di_lemmi_documento_corrente: ", stringa_di_lemmi_documento_corrente)
                        lista_di_tutti_i_documenti_di_TRAINING_in_inglese.append(stringa_di_lemmi_documento_corrente)
                        print("")
                        print("")

                    else:
                        #Qui faccio gli stessi passi presenti nell'if di sopra ma alla fine otterò la lista_di_tutti_i_documenti_del_corpus_inglese
                        #solo per  IL TEST SET:
                        print("Nome cartella corrente: ", cartella)
                        print("Nome file corrente: ", file)
                        print("FARA' PARTE DEL TEST SET !")
                        # Apro il documento_corrente in lettura:
                        #documento_corrente = open(cartella + "\\" + file, "r").read()  # metto la cartella perchè essa contiene tutto il percorso che mi permetterà di aprire il documento corretto.
                        # print("documento_corrente: ", documento_corrente)
                        # print("")
                        # print("")
                        documento_in_lista = split_to_words(cartella + "\\" + file)
                        print("documento in lista: ", documento_in_lista)

                        # adesso elimino le stop words presenti nel documento
                        documento_in_lista_senza_stop_words = [word for word in documento_in_lista if word not in stopwords.words('english')]
                        print("documento_in_lista_senza_stop_words: ", documento_in_lista_senza_stop_words)

                        # Adesso ho il documento in formato di lista che contiene tutte le parole del documento originale senza i segni di punteggiatura e senza le stop words.

                        # A questo punto quindi devo ottenere i lemmi di tutte le parole presenti in documento_in_lista_senza_stop_words:
                        # Istanzio il Lemmatizer
                        lemmatizer = WordNetLemmatizer()
                        # Applico il lemmatizer al documento_in_lista_senza_stop_words e aggiungo tutti i lemmi che ottengo in una lista che chiamo lista_di_lemmi_documento_corrente:
                        lista_di_lemmi_documento_corrente = []  # conterrà i lemmi delle parole del documento corrente.
                        for word in documento_in_lista_senza_stop_words:
                            lista_di_lemmi_documento_corrente.append(lemmatizer.lemmatize(word))
                        print("lista_di_lemmi_documento_corrente: ", lista_di_lemmi_documento_corrente)

                        # Adesso ho la lista di lemmi del documento corrente. (puoi ancora migliorare la lemmatizzazione volendo)

                        # Prima però devo trasformare la lista corrente in una stringa:
                        stringa_di_lemmi_documento_corrente = listToString(lista_di_lemmi_documento_corrente)
                        print("stringa_di_lemmi_documento_corrente: ", stringa_di_lemmi_documento_corrente)
                        lista_di_tutti_i_documenti_di_TEST_in_inglese.append(stringa_di_lemmi_documento_corrente)
                        print("")
                        print("")

                    indice_numerico_file_corrente += 1 #incremento il contatore del numero di file
                #print("")

    return lista_di_tutti_i_documenti_di_TRAINING_in_inglese, lista_di_tutti_i_documenti_di_TEST_in_inglese


'''
#Questa parte commentata mi è servita per crearmi le liste di documenti per il training e per il test !!!:

lista_di_tutti_i_documenti_di_TRAINING_in_inglese, lista_di_tutti_i_documenti_di_TEST_in_inglese = creo_lista_documenti_training_set_e_test_set()
print("lista_di_tutti_i_documenti_di_TRAINING_in_inglese:")
print(lista_di_tutti_i_documenti_di_TRAINING_in_inglese) #in ogni documento ci sono solo i lemmi dei termini orginali (le stop-words non ci sono)
print("")
print("")
print("lista_di_tutti_i_documenti_di_TEST_in_inglese:")
print(lista_di_tutti_i_documenti_di_TEST_in_inglese) #in ogni documento ci sono solo i lemmi dei termini orginali (le stop-words non ci sono)
print("")
print("")


#Serializzo sia la lista_di_tutti_i_documenti_di_TRAINING_in_inglese e sia la lista_di_tutti_i_documenti_di_TEST_in_inglese:####
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese.txt', 'w') as f:
    str = json.dumps(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
    f.write(str)
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese.txt', 'w') as f:
    str = json.dumps(lista_di_tutti_i_documenti_di_TEST_in_inglese)
    f.write(str)
print("LE DUE LISTE SONO STATE SERIALIZZATE CORRETTAMENTE.")
######################################################################
'''


#Deserializzo sia la lista_di_tutti_i_documenti_di_TRAINING_in_inglese e sia la lista_di_tutti_i_documenti_di_TEST_in_inglese:####
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TRAINING_in_inglese.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TRAINING_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
with open('C:\\Users\\miky9\\PycharmProjects\\pythonProject\\Progetti TLN\\Radicioni\\Esercitazione 3\\lista_di_tutti_i_documenti_di_TEST_in_inglese.txt', 'r') as f:
    s = f.read()
    lista_di_tutti_i_documenti_di_TEST_in_inglese = json.loads(s)
    #print("lista_di_tutti_i_documenti_del_corpus_inglese deserializzata: ", lista_di_tutti_i_documenti_del_corpus_inglese)
print("LE DUE LISTE SONO STATE DESERIALIZZATE CORRETTAMENTE.")
print("")
#########################################################################


'''
#A questo punto devo calcolare il peso associato ad ogni termine presente sia in lista_di_tutti_i_documenti_di_TRAINING_in_inglese che
# lista_di_tutti_i_documenti_di_TEST_in_inglese con il prodotto:
# time-frequency (tf) * inverse document frequency (idf):
vectorizer = TfidfVectorizer()
vectors_train  = vectorizer.fit_transform(lista_di_tutti_i_documenti_di_TRAINING_in_inglese)
feature_names = vectorizer.get_feature_names()
# print("feature_names: ")
# print(feature_names)
dense_train = vectors_train.todense()
denselist_train = dense_train.tolist()
df_train = pd.DataFrame(denselist_train, columns=feature_names)
print("")
print("df_train.iloc[0]:")
print(df_train.iloc[0]) #[360 rows x 16648 columns], (360 = numero di documenti totali presenti nel training set), 16648 = numero di lemmi totali (senza duplicati) presenti nel training set.
#df_train.to_csv("Dataframe_documenti_rappresentati_da_lemmi_TRAINING.csv")



vectorizer = TfidfVectorizer()
vectors_test  = vectorizer.fit_transform(lista_di_tutti_i_documenti_di_TEST_in_inglese)
feature_names = vectorizer.get_feature_names()
dense_test = vectors_test.todense()
denselist_test = dense_test.tolist()
df_test = pd.DataFrame(denselist_test, columns=feature_names)
print("")
print("df_test:")
print(df_test) #[40 rows x 3317 columns], (40 = numero di documenti totali presenti nel test set), 3317 = numero di lemmi totali (senza duplicati) presenti nel test set.
print("")
print("vectors_train: ", vectors_train)
print("")
print("vectors_test: ", vectors_test)
#df_test.to_csv("Dataframe_documenti_rappresentati_da_lemmi_TEST.csv")


#I primi 18 documenti (indice da 0 a 17) della lista_di_tutti_i_documenti_di_TRAINING_in_inglese appartengono alla classe "alt.atheism" e così via..
#I primi 2 (indice da 0 a 1) documenti della lista_di_tutti_i_documenti_di_TEST_in_inglese appartengono alla classe "alt.atheism" e così via..
'''


#DOPODICHE' VA A "Algoritmo di Rocchio (con scelta dei NEGs standard).py" oppure A "Algoritmo di Rocchio con scelta dei NEGs più raffinata usando la matrice di confusione.py"
# oppure A "Algoritmo di Rocchio con scelta dei NEG più raffinata usando la sim del coseno per trovare la classe dei NEGs.py" --->