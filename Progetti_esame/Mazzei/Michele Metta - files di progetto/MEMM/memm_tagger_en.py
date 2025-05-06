#################################################
# ================ DO NOT MODIFY ================
#################################################
import sys
import math
import numpy as np
from collections import Counter
from sklearn import linear_model
from scipy import sparse
import pickle
import importlib

Calcolo_metriche = importlib.import_module("Calcolo_metriche")
Estrazione_dati_BIO_tagging_Wikipedia_it_e_en = importlib.import_module("Estrazione_dati_BIO_tagging_Wikipedia_it_e_en")


# Dictionary to store indices for each feature
feature_vocab = {}

# Dictionary to store the indices of each POS tag
label_vocab = {}

#################################################
# ============== IMPLEMENT BELOW ================
#################################################

# Control variables, use for debugging and testing
verbose = True
use_greedy = False

####################################################################################
# FEEL FREE TO CHANGE MINIMUM_FEAT_COUNT AND L2_REGULARIZATION_COEFFICIENT IF NEEDED
####################################################################################

# Minimum number of observations for a feature to be included in model
MINIMUM_FEAT_COUNT = 2
# L2 regularization strength; range is (0,infinity), with stronger regularization -> 0 (in this package)
L2_REGULARIZATION_STRENGTH = 0.9  # default: 1
# percent of data to use
PERCENT_OF_DATA_TO_TRAIN = 1
PERCENT_OF_DATA_TO_TEST = 0.1


# load up any external resources here
def initialize():
    """
        :return (dictionary data - any format that you wish, which
        can be reused in get_features below)
    """
    data = {}
    return data


def get_features(index, sequence, tag_index_1, data):
    """
        :params
        index: the index of the current word in the sequence to featurize
        sequence: the sequence of words for the entire sentence
        tag_index_1: gives you the POS
        tag for the previous word.
        data: the data you have built in initialize()
        to enrich your feature representation. Use data as you see fit.
        :return (feature dictionary)
        features are in the form of {feature_name: feature_value}
        Calculate the values of each feature for a given
        word in a sequence.
        The current implementation returns the following as features:
        the current word, the tag of the previous word, and whether an
        index the the last in the sequence.
    """
    features = {}

    def remove_puncuation(a):
        res = a
        for i in ",.:!$%#@":
            res = res.replace(i, "")
        return res

    features["UNIGRAM_%s" % sequence[index].lower()] = 1
    features["PREVIOUS_TAG_%s" % tag_index_1] = 1
    features["PREFIX_{0}".format(sequence[index]).lower()[:3]] = 1
    features["SUFFIX_{0}".format(sequence[index]).lower()[-2:]] = 1

    if remove_puncuation(sequence[index].lower().strip()).replace("s", "").isnumeric():
        features["NUMERIC"] = 1

    # print("index (in get_features): ", index)
    # print("")
    if sequence[index].strip()[0].isupper():
        features["FIRST_UPPER"] = 1

    if index != 0:
        features["BIGRAM_{0}_{1}".format(sequence[index].lower(), sequence[index - 1].lower())] = 1
    else:
        features["FIRST_WORD_IN_SEQUENCE"] = 1

    if index != len(sequence) - 1:
        features["BIGRAM_{0}_{1}".format(sequence[index].lower(), sequence[index + 1].lower())] = 1
    else:
        features["LAST_WORD_IN_SEQUENCE"] = 1

    if index >= 1 and index < len(sequence) - 1:
        w1 = sequence[index].lower()
        w2 = sequence[index - 1].lower()
        w3 = sequence[index + 1].lower()
        features["TRIGRAM_{0}_{1}_{2}".format(w2, w1, w3)] = 1

    return features


def viterbi_decode(Y_pred):
    """
        :return
        list of POS tag indices, defined in label_vocab,
        in order of sequence
        :param
        Y_pred: Tensor of shape N * M * L, where
        N is the number of words in the current sequence,
        L is the number of POS tag labels
        M = L + 1, where M is the number of possible previous labels
        which includes L + "START"

        M_{x,y,z} is the probability of a tag (label_vocab[current_tag] = z)
        given its current position x in the sequence and
        its previous tag (label_vocab[previous_tag] = y)
        Consider the sentence - "I have a dog". Here, N = 4.
        Assume that there are only 3 possible tags: {PRP, VBD, NN}
        M_{0, 3, 2} would give you the probability of "I" being a "NN" if
        it is preceded by "START". "START" is the last index of all lablels,
        and in our example denoted by 3.
    """
    start_index = Y_pred[0].shape[0] - 1
    cur = start_index
    (N, M, L) = Y_pred.shape

    # list of POS tag indices to be returned
    path = []

    viterbi = np.zeros(shape=(N, L))  # SENTENCE LENGTH (N) x  TAG (L)
    backpointers = np.zeros(shape=(N, L), dtype=np.int32)
    for i in range(N):
        if i == 0:
            viterbi[i] = np.log(Y_pred[i, start_index])
            backpointers[i] = np.array([start_index] * L)
        else:
            for s in range(L):
                values = [viterbi[i - 1, s2] + np.log(Y_pred[i, s2, s]) for s2 in range(L)]
                viterbi[i, s] = np.max(values)
                backpointers[i, s] = np.argmax(values)
    # backtrack to get the path
    cur = np.argmax(viterbi[N - 1])
    path.append(cur)
    i = N - 1
    while i > 0:
        path.append(backpointers[i, cur])
        cur = backpointers[i, cur]
        i -= 1
    return path[::-1]


#################################################
# ================ DO NOT MODIFY ================
#################################################
def load_data_test_set():
    """
        load data from filename and return a list of lists
        all_toks = [toks1, toks2, ...] where toks1 is
                a sequence of words (sentence)
        all_labs = [labs1, labs2, ...] where labs1 is a sequence of
                labels for the corresponding sentence
    """
    Estrazione_dati_BIO_tagging_Wikipedia_en = importlib.import_module("Estrazione_dati_BIO_tagging_Wikipedia_it_e_en")
    frasi_test_con_tag = Estrazione_dati_BIO_tagging_Wikipedia_en.frasi_test_set_en() #prendo tutte le frasi di test con i rispettivi tags assegnati ad ogni parola.
    #print(frasi_test_con_tag[0])
    all_toks = [] #è la lista che conterrà tutte le frasi di test
    all_labs = [] #è la lista che conterrà tutti i tag per ogni frase di test
    for frase_test in frasi_test_con_tag:
        frase_corrente = []
        tags_frase_corrente = []
        frase_test_splittata_per_singola_parola = frase_test.split(" ")
        frase_test_splittata_per_singola_parola[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        #print("frase_test_splittata_per_singola_parola: ")
        #print(frase_test_splittata_per_singola_parola)
        # print("")
        # print("")
        for i in range(0, len(frase_test_splittata_per_singola_parola)):
            parola_frase_train_con_tag = frase_test.split(" ")[i]
            parola_frase_train_senza_tag = parola_frase_train_con_tag.split("\t")[0]
            tag_parola_train_corrente = parola_frase_train_con_tag.split("\t")[1]
            # print("parola_frase_train_senza_tag: ", parola_frase_train_senza_tag)
            # print("tag_parola_train_corrente: ", tag_parola_train_corrente)
            frase_corrente.append(parola_frase_train_senza_tag)
            tags_frase_corrente.append(tag_parola_train_corrente)
        # print("frase_corrente: ", frase_corrente)
        # print("tags_frase_corrente: ", tags_frase_corrente)
        all_toks.append(frase_corrente)
        all_labs.append(tags_frase_corrente)
    # print("all_toks: ", all_toks)
    # print("all_labs: ", all_labs)


    return all_toks, all_labs


def load_data():
    """
        load data from filename and return a list of lists
        all_toks = [toks1, toks2, ...] where toks1 is
                a sequence of words (sentence)
        all_labs = [labs1, labs2, ...] where labs1 is a sequence of
                labels for the corresponding sentence
    """
    Estrazione_dati_BIO_tagging_Wikipedia_en = importlib.import_module("Estrazione_dati_BIO_tagging_Wikipedia_it_e_en")
    frasi_train_con_tag = Estrazione_dati_BIO_tagging_Wikipedia_en.frasi_training_set_en_con_tag()
    #print(frasi_train_con_tag[0])
    all_toks = [] #è la lista che conterrà tutte le frasi di training
    all_labs = [] #è la lista che conterrà tutti i tag per ogni frase di training
    for frase_train in frasi_train_con_tag:
        frase_corrente = []
        tags_frase_corrente = []
        frase_train_splittata_per_singola_parola = frase_train.split(" ")
        frase_train_splittata_per_singola_parola[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        print("frase_train_splittata_per_singola_parola: ")
        print(frase_train_splittata_per_singola_parola)
        print("")
        print("")
        for i in range(0, len(frase_train_splittata_per_singola_parola)):
            parola_frase_train_con_tag = frase_train.split(" ")[i]
            parola_frase_train_senza_tag = parola_frase_train_con_tag.split("\t")[0]
            tag_parola_train_corrente = parola_frase_train_con_tag.split("\t")[1]
            # print("parola_frase_train_senza_tag: ", parola_frase_train_senza_tag)
            # print("tag_parola_train_corrente: ", tag_parola_train_corrente)
            frase_corrente.append(parola_frase_train_senza_tag)
            tags_frase_corrente.append(tag_parola_train_corrente)
        # print("frase_corrente: ", frase_corrente)
        # print("tags_frase_corrente: ", tags_frase_corrente)
        all_toks.append(frase_corrente)
        all_labs.append(tags_frase_corrente)
    # print("all_toks: ", all_toks)
    # print("all_labs: ", all_labs)


    # file = open(filename)
    # all_toks = []
    # all_labs = []
    # toks = []
    # labs = []
    # for line in file:
    #     # Skip the license
    #     if "This data is licensed from" in line:
    #         continue
    #     cols = line.rstrip().split("\t")
    #     if len(cols) < 2:
    #         all_toks.append(toks)
    #         all_labs.append(labs)
    #         toks = []
    #         labs = []
    #         continue
    #     toks.append(cols[0])
    #     labs.append(cols[1])
    #
    # if len(toks) > 0:
    #     all_toks.append(toks)
    #     all_labs.append(labs)

    return all_toks, all_labs


#def train(filename, data):
def train(data):
    """
        train a model to generate Y_pred
    """
    #all_toks, all_labs = load_data(filename)
    all_toks, all_labs = load_data()

    '''
    - NON DEVO FARLO PERCHE' HO GIA' IL TRAINING E TEST SET SEPARATI.
    # # subsample data
    # number_of_data_to_use = int(len(all_toks) * PERCENT_OF_DATA_TO_TRAIN)
    # indices_to_use = np.random.choice(range(len(all_toks)), number_of_data_to_use)
    # all_toks = np.array(all_toks)[indices_to_use]
    # all_labs = np.array(all_labs)[indices_to_use]
    '''


    vocab = {}

    # X_verbose is a list of feature objects for the entire train dataset.
    # Each feature object is a dictionary defined by
    # get_features and corresponds to a word
    # Y_verbose is a list of labels for all words in the entire train dataset
    X_verbose = []
    Y_verbose = []

    feature_counts = Counter()

    for i in range(len(all_toks)):
        toks = all_toks[i] #toks conterrà tutte le parole della frase i-esima che si sta considerando in questo momento.
        labs = all_labs[i] #labs conterrà tutte le etichette assegnate ad ogni parola presente nella frase i-esima.

        #print("frase corrente: ", toks)
        for j in range(len(toks)): #j è l'indice che scorre tutte le parole della frase i-esima che si sta considerando in un certo momento
            prev_lab = labs[j - 1] if j > 0 else "START" #prev_lab = etichetta assegnata alla parola precedente a quella j-esima che si sta considerando in questo momento (se j=0 allora come etichetta precedente mette lo start)
            # print("j: ", j)
            # print("parola j-esima: ", toks[j])
            feats = get_features(j, toks, prev_lab, data) #j = indice della parola che stiamo considerando della frase i - esima, toks = tutte le parole della frase i-esima, prev_lab = etichetta assegnata alla parola precedente a quella j-esima
            X_verbose.append(feats)
            Y_verbose.append(labs[j])
            for feat in feats:
                feature_counts[feat] += 1

    # construct label_vocab (dictionary) and feature_vocab (dictionary)
    # label_vocab[pos_tag_label] = index_for_the_pos_tag
    # feature_vocab[feature_name] = index_for_the_feature
    feature_id = 1
    label_id = 0

    # create unique integer ids for each label and each feature above the minimum count threshold
    for i in range(len(X_verbose)):
        feats = X_verbose[i]
        true_label = Y_verbose[i]

        for feat in feats:
            if feature_counts[feat] >= MINIMUM_FEAT_COUNT:
                if feat not in feature_vocab:
                    feature_vocab[feat] = feature_id
                    feature_id += 1
        if true_label not in label_vocab:
            label_vocab[true_label] = label_id
            label_id += 1

    # START has last id
    label_vocab["START"] = label_id

    # create train input and output to train the logistic regression model
    # create sparse input matrix

    # X is documents x features empty sparse matrix
    X = sparse.lil_matrix((len(X_verbose), feature_id))
    Y = []

    print_message("Number of features: %s" % len(feature_vocab))

    for i in range(len(X_verbose)):
        feats = X_verbose[i]
        true_label = Y_verbose[i]
        for feat in feats:
            if feat in feature_vocab:
                X[i, feature_vocab[feat]] = feats[feat]
        Y.append(label_vocab[true_label])

    # fit model
    print("fit model...")
    log_reg = linear_model.LogisticRegression(C=L2_REGULARIZATION_STRENGTH, penalty='l2', n_jobs=4, max_iter=500)
    log_reg.fit(sparse.coo_matrix(X), Y)

    return log_reg


def greedy_decode(Y_pred):
    """
        greedy decoding to get the sequence of label predictions
    """
    cur = label_vocab["START"]
    preds = []
    for i in range(len(Y_pred)):
        pred = np.argmax(Y_pred[i, cur])
        preds.append(pred)
        cur = pred
    return preds


def test(log_reg, data):
    """
        predict labels using the trained model
        and evaluate the performance of model
    """
    #all_toks, all_labs = load_data(filename)
    all_toks, all_labs = load_data_test_set() #aggiunto io

    '''
    - NON DEVO FARLO PERCHE' HO GIA' IL TRAINING E TEST SET SEPARATI.
    # subsample data
    # number_of_data_to_use = int(len(all_toks) * PERCENT_OF_DATA_TO_TEST)
    # indices_to_use = np.random.choice(range(len(all_toks)), number_of_data_to_use)
    # all_toks = np.array(all_toks)[indices_to_use]
    # all_labs = np.array(all_labs)[indices_to_use]
    '''


    # possible output labels = all except START
    L = len(label_vocab) - 1

    correct = 0.
    total = 0.

    num_features = len(feature_vocab) + 1

    tags_assegnati_a_tutte_le_frasi_di_test = []


    # for each sequence (sentence) in the test dataset
    for i in range(len(all_toks)):

        toks = all_toks[i]
        labs = all_labs[i]

        if len(toks) == 0:
            continue

        N = len(toks)

        X_test = []
        # N x prev_tag x cur_tag
        Y_pred = np.zeros((N, L + 1, L))

        # vector of true labels
        Y_test = []

        # for each token (word) in the sentence
        for j in range(len(toks)):

            true_label = labs[j]
            Y_test.append(true_label)

            # for each preceding tag of the word
            for possible_previous_tag in label_vocab:
                X = sparse.lil_matrix((1, num_features))

                feats = get_features(j, toks, possible_previous_tag, data)
                valid_feats = {}
                for feat in feats:
                    if feat in feature_vocab:
                        X[0, feature_vocab[feat]] = feats[feat]

                # update Y_pred with the probabilities of all current tags
                # given the current word, previous tag and other data/feature
                prob = log_reg.predict_proba(X)
                Y_pred[j, label_vocab[possible_previous_tag]] = prob

        # decode to get the predictions
        predictions = decode(Y_pred) #predictions conterrà tutte le predizione del MEMM fatte per ogni frase del test set. (E' una lista)
        # print("frase di test appena analizzata: ", toks)
        # print("Y_test(corrette): ", Y_test)
        # print("tag_predetti: ")
        # print(predictions)
        # print("")


        tags_assegnati_a_tutte_le_frasi_di_test.append(predictions) #tags_assegnati_a_tutte_le_frasi_di_test sarà una lista di lista che conterrà per ogni frase di test le
        #predizioni sui tags che sono state fatte dal MEMM.


        # evaluate the performance of the model by checking predictions
        # against true labels (questo viene fatto per ogni frase di test).
        tag_predetti_correttamente_frase_corrente = 0
        tag_totali_frase_corrente = 0
        for k in range(len(predictions)):
            if Y_test[k] in label_vocab and predictions[k] == label_vocab[Y_test[k]]:
                correct += 1 #conta il numero di tag predetti correttamente in totale su tutte le frasi di test.
                tag_predetti_correttamente_frase_corrente += 1

            total += 1 #conta il numero di parole totali presenti nel test set.
            tag_totali_frase_corrente += 1

        #print("Development Accuracy: %.3f (%s/%s)." % (correct / total, correct, total), end="\r")
        print("tag_predetti_correttamente_frase_corrente: ", tag_predetti_correttamente_frase_corrente)
        print("tag_totali_frase_corrente: ", tag_totali_frase_corrente)
        accuratezza_frase_corrente = (tag_predetti_correttamente_frase_corrente / tag_totali_frase_corrente)
        print("Accuratezza_frase_corrente: ", accuratezza_frase_corrente)
        print("")
        print("")


    print("label_vocab: ", label_vocab)
    print("numero totale frasi di test: ", len(all_toks))
    print("numero di tags predetti in maniera corretta su tutto il test set: ", correct)
    print("numero di tags totali in tutto il test set: ", total)
    print("Accuratezza totale MEMM: ", correct/total)

    print("")
    print("")
    print("len(tags_assegnati_a_tutte_le_frasi_di_test): ", len(tags_assegnati_a_tutte_le_frasi_di_test))
    # print("tags_assegnati_a_tutte_le_frasi_di_test PRIMA: ", tags_assegnati_a_tutte_le_frasi_di_test)
    # print("label_vocab: ", label_vocab)

    #Adesso in tags_assegnati_a_tutte_le_frasi_di_test sono presenti tutte le predizioni fatte dal MEMM per ogni frase di test.##############################
    #Le predizioni però non sono del tipo "B-PER", "I-LOC", ecc... ma sono del tipo 6, 4, ecc..
    #dove ogni valore intero è associato un certo NER TAG.
    #Quindi a questo punto quello che devo fare è questo:
    #1) Prendo tutte le predizioni fatte dal MEMM per ogni singola frase scandendo la lista di lista tags_assegnati_a_tutte_le_frasi_di_test:
    for tags_predetti_frase_corrente in tags_assegnati_a_tutte_le_frasi_di_test:
        for indice_tag_predetto_frase_corrente in range(0, len(tags_predetti_frase_corrente)):
            #2) Sostituisco tutti i valori interi con i rispettivi NER TAGS usando il label_vocab:
            if(tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 0): #RICORDA CHE GLI INDICI NEL DIZIONARIO label_vocab CAMBIANO IN BASE AL TEST SET CHE USI.
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "O"
            elif(tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 1):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "B-LOC"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 2):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "I-LOC"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 3):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "B-ORG"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 4):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "B-MISC"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 5):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "I-MISC"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 6):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "B-PER"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 7):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "I-PER"
            elif (tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] == 8):
                tags_predetti_frase_corrente[indice_tag_predetto_frase_corrente] = "I-ORG"

    #A questo punto la lista di liste chiamata tags_assegnati_a_tutte_le_frasi_di_test conterrà per ogni frase tutti i nomi dei NER TAGS che sono stati predetti dal MEMM.
    #print("tags_assegnati_a_tutte_le_frasi_di_test DOPO: ", tags_assegnati_a_tutte_le_frasi_di_test)
    ###########################################################################################################################################################


    print("")
    print("")
    #Calcolo anche per il MEMM la precision e la recall:
    print("")
    frasi_test_set = Estrazione_dati_BIO_tagging_Wikipedia_it_e_en.frasi_test_set_en() #estraggo tutte le frasi presenti nel test set con la funzione che ho creato.

    #frasi_test_set = frasi_test_set[:10]
    precision_modello = Calcolo_metriche.precision(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
    print("precisione_modello PER: ", precision_modello)
    precision_modello = Calcolo_metriche.precision(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
    print("precisione_modello LOC: ", precision_modello)
    precision_modello = Calcolo_metriche.precision(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
    print("precisione_modello ORG: ", precision_modello)
    precision_modello = Calcolo_metriche.precision(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
    print("precisione_modello MISC: ", precision_modello)

    print("")
    recall_modello = Calcolo_metriche.recall(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
    print("recall_modello PER: ", recall_modello)
    recall_modello = Calcolo_metriche.recall(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
    print("recall_modello LOC: ", recall_modello)
    recall_modello = Calcolo_metriche.recall(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
    print("recall_modello ORG: ", recall_modello)
    recall_modello = Calcolo_metriche.recall(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
    print("recall_modello MISC: ", recall_modello)
    print("")

    print("")
    acc_modello_B_I_PER = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test, "PER")
    print("acc_modello_B_I_PER: ", acc_modello_B_I_PER)
    acc_modello_B_I_LOC = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
    print("acc_modello_B_I_LOC: ", acc_modello_B_I_LOC)
    acc_modello_B_I_ORG = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
    print("acc_modello_B_I_ORG: ", acc_modello_B_I_ORG)
    acc_modello_B_I_MISC = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
    print("acc_modello_B_I_MISC: ", acc_modello_B_I_MISC)
    acc_modello_O = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_set, tags_assegnati_a_tutte_le_frasi_di_test,"O")
    print("acc_modello_O: ", acc_modello_O)
    print("")


    # print("")
    # acc_modello_B_I_consecutivi_PER = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test,"PER")
    # print("acc_modello_B_I_consecutivi_PER: ", acc_modello_B_I_consecutivi_PER)
    # acc_modello_B_I_consecutivi_LOC = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test,"LOC")
    # print("acc_modello_B_I_consecutivi_LOC: ", acc_modello_B_I_consecutivi_LOC)
    # acc_modello_B_I_consecutivi_ORG = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test,"ORG")
    # print("acc_modello_B_I_consecutivi_ORG: ", acc_modello_B_I_consecutivi_ORG)
    # acc_modello_B_I_consecutivi_MISC = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_set,tags_assegnati_a_tutte_le_frasi_di_test,"MISC")
    # print("acc_modello_B_I_consecutivi_MISC: ", acc_modello_B_I_consecutivi_MISC)
    # print("")

    print("Esecuzione terminata.")
    ####################################################






def print_message(m):
    num_stars = 10
    if verbose:
        print("*" * num_stars + m + "*" * num_stars)


def decode(Y_pred):
    """
        select the decoding algorithm
    """
    if use_greedy:
        return greedy_decode(Y_pred)
    else:
        return viterbi_decode(Y_pred)


# usage: python memm_tagger_it.py -t wsj.pos.train wsj.pos.dev
def main():
    print_message("Initialize Data")
    data = initialize()

    print_message("Train Model")
    log_reg = train(data)

    print_message("Test Model")
    #test(sys.argv[3], log_reg, data)
    test(log_reg, data)

    print("Esecuzione terminata.")

    # if sys.argv[1] == "-t":
    #     print_message("Initialize Data")
    #     data = initialize()
    #     print_message("Train Model")
    #     log_reg = train(sys.argv[2], data)
    #     print_message("Test Model")
    #     test(sys.argv[3], log_reg, data)
    #     print()
    # else:
    #     print("Usage: python memm_tagger_it.py -t wsj.pos.train wsj.pos.dev")


if __name__ == "__main__":
    main()
