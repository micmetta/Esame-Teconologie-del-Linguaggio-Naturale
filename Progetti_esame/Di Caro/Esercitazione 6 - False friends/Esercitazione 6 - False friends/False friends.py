from nltk.corpus import semcor
import nltk
import numpy as np
import re
import json
import importlib
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn



def punteggiatura_nella_parola(parola):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~\n'''
    for c in parola:
        for el in punc:
            if(c == el):
                return True

    return False


# Procedura che serve per individuare tutte le coppie parola-synset del tipo [['window', 'window.n.01'], ['Mahzeer', 'person.n.01'], ecc..] partendo da un insieme di frasi casuali
# estratte dal corpus SemCor.
# Dopodichè prende oggni nuova coppia e le inserisce in una lista che viene successivamente serializzata che si trova nel percorso path_lista_di_coppie dato in input.
def individuazione_coppie_parola_synset(path_lista_di_coppie, num_frasi_da_considerare):
    lista_coppie_parola_synset = [] #lista di liste che conterrà le coppie parola-synset, es: [['window', 'window.n.01'], ['Mahzeer', 'person.n.01'], ecc..]

    lista_di_indici_frasi_selezionate = np.random.randint(low=0, high=37177, size=num_frasi_da_considerare)
    print("lista_di_indici_frasi_selezionate: ", lista_di_indici_frasi_selezionate)

    for indice_frase_scelta in lista_di_indici_frasi_selezionate:
        print("")
        print("")
        frase_di_input = []
        #print(semcor.sents()[0])
        for parola in semcor.sents()[indice_frase_scelta]:
            #print(parola)
            frase_di_input.append(parola)
        print("frase_di_input: ", frase_di_input)

        lista_parole_frase_di_input_con_synset = []
        for s in semcor.tagged_sents(tag='sem')[indice_frase_scelta:indice_frase_scelta+1]:
            for c in s:
                #print(str(c))
                lista_parole_frase_di_input_con_synset.append(str(c))

        print("lista_parole_frase_di_input_con_synset:")
        print(lista_parole_frase_di_input_con_synset)
        print("")
        print("")

        lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata = []  # conterrà tutte le coppie costitute da parola-synset_associato (dove chiaramente
        # ogni parola sarà però un nome perchè sono quelli che a noi interessano).
        for parola_parole_piu_synset_di_appartenenza in lista_parole_frase_di_input_con_synset:
            parola_parole_piu_synset_di_appartenenza_splittata = parola_parole_piu_synset_di_appartenenza.split(" ")
            if (len(parola_parole_piu_synset_di_appartenenza_splittata) > 1):

                # se entro qui vuol dire che NON sto considerando le parole senza synset (le STOPWORDS - SW):
                #print(parola_parole_piu_synset_di_appartenenza_splittata)
                synset_di_appartenenza = parola_parole_piu_synset_di_appartenenza_splittata[0]
                insieme_di_parole_assegnate_a_quel_synset = parola_parole_piu_synset_di_appartenenza_splittata[1:]
                print("synset_di_appartenenza: ", synset_di_appartenenza)
                print("insieme_di_parole_assegnate_a_quel_synset: ", insieme_di_parole_assegnate_a_quel_synset)

                # adesso cerco i sostantivi, verbi, aggettivi, ecc.. tra le parole della frase corrente
                if ("Lemma" in synset_di_appartenenza):
                    synset_di_appartenenza_splittato = synset_di_appartenenza.split("Lemma")

                    if (synset_di_appartenenza_splittato[0] == "("):
                        synset_di_appartenenza_splittato.remove("(")  # rimuovo dalla lista le tutte le "(" perchè sono inutili.

                    synset_di_appartenenza_splittato_in_base_al_punto = synset_di_appartenenza_splittato[0].split(".")
                    print("synset_di_appartenenza_splittato_in_base_al_punto: ", synset_di_appartenenza_splittato_in_base_al_punto)
                    print("")

                    tag = synset_di_appartenenza_splittato_in_base_al_punto[1]
                    # print("tag: ", tag)

                    if (tag == "n" or tag == "v" or tag == "a" or tag == "s"):  # a noi non interessano solo i sostantivi
                        # print("synset_di_appartenenza_splittato_in_base_al_punto: ", synset_di_appartenenza_splittato_in_base_al_punto)
                        nome_synset_gold = synset_di_appartenenza_splittato_in_base_al_punto[0].split("'")[1] + "." + synset_di_appartenenza_splittato_in_base_al_punto[1] + "." + synset_di_appartenenza_splittato_in_base_al_punto[2]
                        # print("nome_synset_gold: ", nome_synset_gold)
                        # Adesso nella variabile nome_synset_gold ci sarà tutto il nome del synset corrente (che è sicuramente associato ad un nome).

                        # Adesso devo prendere tutte le parole associate a questo synset e metterle in una lista:
                        lista_termini = []
                        for termine in insieme_di_parole_assegnate_a_quel_synset:
                            if (termine != "(NE"):
                                termine = re.sub("\)", "", termine)
                                lista_termini.append(termine)

                        for parola in lista_termini:
                            coppia_parola_rispettivo_synset = []
                            coppia_parola_rispettivo_synset.append(parola)
                            coppia_parola_rispettivo_synset.append(str(nome_synset_gold))
                            lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata.append(coppia_parola_rispettivo_synset)

                else:
                    continue  #salto il synset corrente perchè già so che non si tratta di un nome, agg, verbo

        print("")
        print("lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata: ")
        print(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata)
        print("")

        for coppia in lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata:
            lista_coppie_parola_synset.append(coppia)
        print("lista_coppie_parola_synset AGGIORNATA:")
        print(lista_coppie_parola_synset)


    #Deserializzo la lista_coppie_parola_synset:
    with open(path_lista_di_coppie, 'r') as json_file:
        lista_coppie_parola_synset_deserializzata = json.load(json_file)

    for coppia in lista_coppie_parola_synset:
        if(coppia not in lista_coppie_parola_synset_deserializzata):
            lista_coppie_parola_synset_deserializzata.append(coppia)

    #Serializzo la lista_coppie_parola_synset DOPO L'AGGIORNAMENTO FATTO SOPRA, in modo tale da aumentare sempre di più il numero di coppie parola-synset a
    # disposizione per passare alla fase successiva:
    with open(path_lista_di_coppie, 'w') as json_file:
        json.dump(lista_coppie_parola_synset_deserializzata, json_file)


#Funzione che prende in input una lista di liste in cui ogni lista interna è una coppia composta da: parola - synset ad essa associato.
#es. di input: [ ['ignores', 'ignore.v.01'], ['sordid', 'seamy.s.02'], ['financial', 'fiscal.a.01'], ... ]
def get_coppie_parole_con_dist_edit_giusta(lista_coppie_parola_synset_deserializzata, soglia_dist_edit):
    lista_coppie_di_parole = []
    lemmatizer = WordNetLemmatizer()

    for coppia_corrente in lista_coppie_parola_synset_deserializzata:
        parola1 = coppia_corrente[0].lower()
        ss1 = coppia_corrente[1] #nome synset associato alla parola1
        for coppia_corrente_temp in lista_coppie_parola_synset_deserializzata:
            parola2 = coppia_corrente_temp[0].lower()
            ss2 = coppia_corrente_temp[1] #nome synset associato alla parola2


            if((ss1 != "person.n.01") and (ss2 != "person.n.01")): #Questo controllo mi serve per essere certo di non star considerando dei nomi di persona.

                #Adesso verifico che sia parola1 che parola2 non siano numeri:
                if not (parola1.isnumeric() or parola2.isnumeric()):

                    #Adesso lemmatizzo sia parola1 che parola2:
                    parola1 = lemmatizer.lemmatize(parola1)
                    parola2 = lemmatizer.lemmatize(parola2)
                    ##########################################

                    #sia parola1 che parola2 devono avere lunghezza almeno pari a 3 (dopo averle lemmatizzate) e non devono contenere al proprio interno simboli di punteggiatura.
                    if( (len(parola1) >= 3 and len(parola2) >= 3)
                        and
                        (punteggiatura_nella_parola(parola1) == False and punteggiatura_nella_parola(parola2) == False) ):

                        if (parola1 != parola2):
                            nuova_coppia_parole = []
                            nuova_coppia_parole_contrario = []

                            nuova_coppia_parole.append(parola1)
                            nuova_coppia_parole.append(parola2)
                            nuova_coppia_parole_contrario.append(parola2)
                            nuova_coppia_parole_contrario.append(parola1)

                            # Con l'if di sotto, verifico che sia la coppia di parole corrente (parola1 - parola2) e sia la coppa contraria (parola2 - parola1)
                            # non siano già presente nella lista_coppie_di_parole, in modo tale da evitare duplicati inutili.
                            if ((nuova_coppia_parole not in lista_coppie_di_parole) and (nuova_coppia_parole_contrario not in lista_coppie_di_parole)):

                                #Infine controllo che la coppia corrente abbia effettivamente il valore della edit distance minore di una certa soglia.
                                if(nltk.edit_distance(parola1,parola2) < soglia_dist_edit):
                                    lista_coppie_di_parole.append(nuova_coppia_parole)
                                    print("nuova_coppia_parole AGGIUNTA:", nuova_coppia_parole)

    return lista_coppie_di_parole


# Funzione che prende in input un certo termine e mi restituisce tutti i possibili synsets di WN associati a quel termine.
def concetti_associati_ai_synset_associati_al_termine_di_input(termine):
    lista_concetti_synset_associati_a_termine = [] #è una lista che avrà come elementi tutti i synsets associati al termine dato in input.
    for ss in wn.synsets(termine): #ciclo su tutti i synset associati al termine di input
        synset_corrente = ss.name()
        lista_concetti_synset_associati_a_termine.append(synset_corrente)


    return lista_concetti_synset_associati_a_termine



# Funzione che prende in input due insiemi di concetti (uno per w1 e l'altro per w2) e mi restituisce questo valore:
#           MAX                  [sim(c1, c2)]
# (su tutti i possibili c1 e c2)
def Wu_and_Palmer(tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2):
    max = 0
    for c1 in tutti_i_concetti_associati_a_w1:
        for c2 in tutti_i_concetti_associati_a_w2:
            sim_tra_c1_e_c2_correnti = wn.wup_similarity(wn.synset(c1), wn.synset(c2))
            if sim_tra_c1_e_c2_correnti > max:
                max = sim_tra_c1_e_c2_correnti

    return max





#L’obiettivo di questa esercitazione è stato quello di creare un algoritmo che fosse in grado di individuare coppie di termini della lingua inglese
# che potessero essere considerati dei “false friends”. Poiché in questo caso, consideriamo una sola lingua, possiamo considerare come false friends
# due termini che dal punto di vista della forma sono quasi identici ma che differiscono notevolmente nel significato che assumono.
# Le risorse principali utilizzate per questa esercitazione sono state:
# -	Wordnet, per ottenere i possibili sensi associati ad un certo termine.
# -	Semcor, che invece è un corpus già utilizzato nella seconda parte del corso. Esso contiene al proprio interno circa 37000 frasi annotate
# a diversi livelli (per ogni parola in ogni frase contiene anche il synset di WN di riferimento), che è stato utilizzato per ottenere le frasi nelle
# quali andare a cercare le possibili parole che potrebbero essere false friends.
if __name__ == '__main__':

    path_lista_di_coppie = 'Risorse utili False friends\\lista_coppie_parola_synset.json'

    '''
            #Le due istruzioni qui sotto le ho utilizzate per prendere da SemCor alcune frasi casuali che ho utilizzato per ottenere le parole su cui 
            #poi andare ad applicare la metrica di Wu&Palmer.
            
    num_frasi_da_considerare = 3000
    individuazione_coppie_parola_synset(path_lista_di_coppie, num_frasi_da_considerare)
    #####################################################################################################################################################################
    '''

    # - Deserializzo la lista_coppie_parola_synset:#############################################################
    with open(path_lista_di_coppie, 'r') as json_file:
        lista_coppie_parola_synset_deserializzata = json.load(json_file)
    print("len(lista_coppie_parola_synset_deserializzata):", len(lista_coppie_parola_synset_deserializzata))

    #print("lista_coppie_parola_synset_deserializzata:")
    #print(lista_coppie_parola_synset_deserializzata)
    print("")
    print("")
    ##########################################################################################################


    ########################################################################################################
    # - Creo le coppie di parole:
    soglia_dist_edit = 2
    lista_coppie_parole = get_coppie_parole_con_dist_edit_giusta(lista_coppie_parola_synset_deserializzata, soglia_dist_edit)
    print("lista_coppie_parole:")
    print(lista_coppie_parole)
    print("")
    print("")
    ########################################################################################################

    soglia_sim_minima = 0.20
    lista_coppie_sim = []  # lista di liste che conterrà solo le coppie di parole che hanno una sim. minore di soglia_sim_minima.

    # - Individuo i false friends della lingua inglese, ovvero tutte quelle coppie di parole che pur avendo una somiglianza elevata a livello letterale,
    # mantengono pur sempre una similarità bassa a livello semantico.
    for coppia_parole in lista_coppie_parole:
        w1 = coppia_parole[0]
        w2 = coppia_parole[1]

        # 1) La prima cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w1
        tutti_i_concetti_associati_a_w1 = concetti_associati_ai_synset_associati_al_termine_di_input(w1)

        # 2) La seconda cosa da fare è considerare tutti i concetti che appartengono ai synset associati al termine w2
        tutti_i_concetti_associati_a_w2 = concetti_associati_ai_synset_associati_al_termine_di_input(w2)

        # print("tutti_i_concetti_associati_a_w1: ", tutti_i_concetti_associati_a_w1)
        # print("tutti_i_concetti_associati_a_w2: ", tutti_i_concetti_associati_a_w2)

        # 3) La terza cosa da fare è quella di calcolare tra ogni possibile coppia di concetti associati ai
        # vari synset di w1 e w2 che sono presenti rispettivamente in tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2 il valore sim_Wu&Palmer(c1,c2),
        # ove:
        # sim(c1,c2) = cs(c1,c2) = 2*depth(LCS) / (depth(s1) + depth(s2)) (Wu & Palmer)

        #spiegazione componenti formula Wu&Palmet:
        # LCS = Lowest Common Subsumer, ovvero è il primo antenato comune (presente in Wordnet) tra i sensi s1 ed s2.
        # depth(x) = è una funzione che misura la distanza tra la radice di Wordnet e il synset x.


        # Per fare quello appena detto chiamo la funzione creata sopra chiamata Wu_and_Palmer,
        # passandogli in input: tutti_i_concetti_associati_a_w1 e tutti_i_concetti_associati_a_w2.
        # QUELLO CHE FARA' LA FUNZIONE Wu_and_Palmer è questo:

        #           MAX                  [sim(c1, c2)]
        # (su tutti i possibili c1 e c2, dove c1 app. all'insieme dei possibili synsets di w1 e c1 app. all'insieme dei possibili synsets di w2)
        # Una volta ottenuto tale max, posso quindi dire di aver ottenuto:
        # sim(w1,w2) = #           MAX                  [sim(c1, c2)]
                       # (su tutti i possibili c1 e c2, dove c1 appartiene all'insieme dei possibili synsets di w1 e c1 appartiene all'insieme dei possibili synsets di w2)


        swp = Wu_and_Palmer(tutti_i_concetti_associati_a_w1, tutti_i_concetti_associati_a_w2)

        print("w1 - w2: ", w1 + " - " + w2)
        print("wu_and_palmer similarity: ", swp)
        print("")
        print("")

        if (swp < soglia_sim_minima):

            nuova_aggiunta = []
            nuova_aggiunta.append(w1)
            nuova_aggiunta.append(w2)
            nuova_aggiunta.append(swp)
            lista_coppie_sim.append(nuova_aggiunta)

    print("len(lista_coppie_sim):", len(lista_coppie_sim))
    print("lista_coppie_sim:")
    print(lista_coppie_sim) #stampo la lista di coppie di termini che hanno una distanza di edit < 2 ma che hanno una similarità < 0.20.