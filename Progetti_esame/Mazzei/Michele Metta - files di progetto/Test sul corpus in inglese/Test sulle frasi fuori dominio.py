
import numpy as np
import importlib
import json


Estrazione_dati_BIO_tagging_Wikipedia_en = importlib.import_module("Estrazione_dati_BIO_tagging_Wikipedia_it_e_en")
Calcolo_metriche = importlib.import_module("Calcolo_metriche")
tecniche_smoothing = importlib.import_module("Smoothing")

def calcolo_prob_di_emissione(parola,frasi_corpus,dizionario_count_tags):
    #Per ogni tag, devo calcolare quanto è probabile che alla parola di input nel corpus sia stato associato il tag corrente.
    #esempio P(wi|ti) = P("Paolo"|N) = C("Paolo",N)/C(N)
    #ove:
    # - C("Paolo",N) = numero di volte che la parola "Paolo" è stata taggata come N (nome) nel corpus.
    # - C(N) = numero di volte che il tag N è stato associato ad una parola nel corpus.
    #b_s_o_t = {"N": 0, "V": 0, "A": 0, "D": 0}

    # Questo qui sotto è un dizionario che mi dirà per ogni possibile tag qual è la probabilità che la parola data in input possa essere taggata con quel tag specifico,
    # è anche detta prob. di emissione per ogni tag della parola che viene data in input alla funzione.
    b_s_o_t = {"B-PER":0, "I-PER":0,
               "B-ORG":0, "I-ORG":0,
               "B-LOC":0, "I-LOC":0,
               "B-MISC":0,"I-MISC":0,
               "O":0
               }
    ################################################ CALCOLO b_s_o_1: ##################################################
    #devo scorrere tutte le parole del corpus:
    num_tag_B_PER_per_la_parola_di_input = 0
    num_tag_I_PER_per_la_parola_di_input = 0
    num_tag_B_ORG_per_la_parola_di_input = 0
    num_tag_I_ORG_per_la_parola_di_input = 0
    num_tag_B_LOC_per_la_parola_di_input = 0
    num_tag_I_LOC_per_la_parola_di_input = 0
    num_tag_B_MISC_per_la_parola_di_input = 0
    num_tag_I_MISC_per_la_parola_di_input = 0
    num_tag_O_per_la_parola_di_input = 0

    # print("len(frasi_corpus): ", len(frasi_corpus))
    # print("")
    parola_di_input_presente_nel_training_set = False
    for frase in frasi_corpus:
        frase = frase.split(" ")
        frase[-1:] = []  # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
        #print("frase: ", frase)
        for i in range(0, len(frase)):
            parola_corrente = frase[i].split("\t")[0]
            tag_assegnato_alla_parola_corrente = frase[i].split("\t")[1]

            if(parola_corrente == parola):
                parola_di_input_presente_nel_training_set = True

                if (tag_assegnato_alla_parola_corrente == "B-PER"):
                    num_tag_B_PER_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-PER"):
                    num_tag_I_PER_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-ORG"):
                    num_tag_B_ORG_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-ORG"):
                    num_tag_I_ORG_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-LOC"):
                    num_tag_B_LOC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-LOC"):
                    num_tag_I_LOC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "B-MISC"):
                    num_tag_B_MISC_per_la_parola_di_input += 1
                elif (tag_assegnato_alla_parola_corrente == "I-MISC"):
                    num_tag_I_MISC_per_la_parola_di_input += 1
                else:
                    num_tag_O_per_la_parola_di_input += 1

    ##############################

    b_s_o_t["B-PER"] = num_tag_B_PER_per_la_parola_di_input / dizionario_count_tags["B-PER"]
    b_s_o_t["I-PER"] = num_tag_I_PER_per_la_parola_di_input / dizionario_count_tags["I-PER"]
    b_s_o_t["B-ORG"] = num_tag_B_ORG_per_la_parola_di_input / dizionario_count_tags["B-ORG"]
    b_s_o_t["I-ORG"] = num_tag_I_ORG_per_la_parola_di_input / dizionario_count_tags["I-ORG"]
    b_s_o_t["B-LOC"] = num_tag_B_LOC_per_la_parola_di_input / dizionario_count_tags["B-LOC"]
    b_s_o_t["I-LOC"] = num_tag_I_LOC_per_la_parola_di_input / dizionario_count_tags["I-LOC"]
    b_s_o_t["B-MISC"] = num_tag_B_MISC_per_la_parola_di_input / dizionario_count_tags["B-MISC"]
    b_s_o_t["I-MISC"] = num_tag_I_MISC_per_la_parola_di_input / dizionario_count_tags["I-MISC"]
    b_s_o_t["O"] = num_tag_O_per_la_parola_di_input / dizionario_count_tags["O"]

    # print("parola: ", parola)
    # print("num_tag_B-PER_per_la_parola_di_input: ", num_tag_B_PER_per_la_parola_di_input)
    # print("num_tag_I-PER_per_la_parola_di_input: ", num_tag_I_PER_per_la_parola_di_input)
    # print("num_tag_B-ORG_per_la_parola_di_input: ", num_tag_B_ORG_per_la_parola_di_input)
    # print("num_tag_I-ORG_per_la_parola_di_input: ", num_tag_I_ORG_per_la_parola_di_input)
    # print("num_tag_B-LOC_per_la_parola_di_input: ", num_tag_B_LOC_per_la_parola_di_input)
    # print("num_tag_I-LOC_per_la_parola_di_input: ", num_tag_I_LOC_per_la_parola_di_input)
    # print("num_tag_B-MISC_per_la_parola_di_input: ", num_tag_B_MISC_per_la_parola_di_input)
    # print("num_tag_I-MISC_per_la_parola_di_input: ", num_tag_I_MISC_per_la_parola_di_input)
    # print("num_tag_O_per_la_parola_di_input: ", num_tag_O_per_la_parola_di_input)
    # print("")
    # print("dizionario_count_tags[B-PER]: ", dizionario_count_tags["B-PER"])
    # print("dizionario_count_tags[I-PER]: ", dizionario_count_tags["I-PER"])
    # print("dizionario_count_tags[B-ORG]: ", dizionario_count_tags["B-ORG"])
    # print("dizionario_count_tags[I-ORG]: ", dizionario_count_tags["I-ORG"])
    # print("dizionario_count_tags[B-LOC]: ", dizionario_count_tags["B-LOC"])
    # print("dizionario_count_tags[I-LOC]: ", dizionario_count_tags["I-LOC"])
    # print("dizionario_count_tags[B-MISC]: ", dizionario_count_tags["B-MISC"])
    # print("dizionario_count_tags[I-MISC]: ", dizionario_count_tags["I-MISC"])
    # print("dizionario_count_tags[O]: ", dizionario_count_tags["O"])

    # QUI FACCIO LO SMOOTHING:####
    if (parola_di_input_presente_nel_training_set == False):
        print("LA PAROLA " + parola + " NON è PRESENTE NEL TRAINING SET!!")
        #b_s_o_t = tecniche_smoothing.sempre_O(b_s_o_t)
        #b_s_o_t = tecniche_smoothing.O_B_MISC_stessa_prob(b_s_o_t)
        #b_s_o_t = tecniche_smoothing.uniforme_su_tutti_i_tags(b_s_o_t)
        b_s_o_t = tecniche_smoothing.statistica_development_set_en()
        print("b_s_o_t della parola mancante: ", b_s_o_t)
    #################################################################################################################################################


    return b_s_o_t



def Viterbi(frase_di_input, tag_possibili, a_s_primo_s, lista_di_prob_di_emissione, dizionario_indice_numerico_tag, dizionario_per_passare_dal_tag_al_numero):

    #Settaggio: ###################################
    frase_di_input = frase_di_input.split(" ") #per poter capire da quante parole è costituita la frase
    #print("frase_di_input: ", frase_di_input)
    #print("")
    #di input.
    #print(frase_di_input)
    T = len(frase_di_input) #numero di parole della frase si input
    #print("T: ", T)
    N = len(tag_possibili) #numero di tag totali
    # a_0_s = probabilita_start
    # bs_o_1 = probabilita_emissione_prima_parola_frase_test
    ###############################################

    #creo la matrice di Viterbi:#######
    #Matrice = {(0, 3): 1, (2, 1): 2, (4, 3): 3} #come creare un dizionario per una matrice sparsa
    viterbi = np.zeros((N+2, T))
    #viterbi = {}
    # backpointer = np.zeros((N, T))

    # Perchè le righe del backpointer sono N+2?
    # Perchè dipendono direttamente dal numero di tags possibili e +2 perchè bisogna aggiungere lo start S e l'end E (ogni array interno è una riga della matrice backpointer) e
    # poichè la frase di test sarà composta da T parole allora il numero di colonne saranno proprio T.
    backpointer = np.full((N+2,T),"aaaaaa")  # creo il backpointer come una matrice con N+2 righe e T colonne riempita con il carattere "aaaaaa" che uso solo come segnaposto; metto esattamente
    #6 "a" come segnaposto perchè il tag più lungo è I-MISC ed è lungo esattamente 6 caratteri.

    # print("matrice di Viterbi all'inizio:")
    # print(viterbi)
    ##################################


    #initialization step:################
    bs_o_1 = lista_di_prob_di_emissione[0] #prendo le probabilità di emissione della prima parola della frase di input (quindi di "Paolo")
    for s in range(0, N): #s partirà dal tag "N" e arriverà fino al tag "D"
        tag_da_considerare_per_l_emissione = dizionario_indice_numerico_tag[s]

        if ((bs_o_1[tag_da_considerare_per_l_emissione] != 0) and (a_s_primo_s[tag_da_considerare_per_l_emissione + "|" + "S"] != 0)):
            viterbi[s, 0] = np.log(a_s_primo_s[tag_da_considerare_per_l_emissione + "|" + "S"]) + np.log(bs_o_1[tag_da_considerare_per_l_emissione])  # o_1 indica che sto calcolando le prob. di emissione per la prima parola della frase di input e con [s] indico che lo sto facendo
        else:
            viterbi[s, 0] = a_s_primo_s[tag_da_considerare_per_l_emissione + "|" + "S"] * bs_o_1[tag_da_considerare_per_l_emissione]


        backpointer[s,0] = "S" #serve per ricordarmi che sono partito dallo start e quindi per ogni tag della prima colonna che fa riferimento alla prima parola della frase di input
        #metto 0 (potrei anche eliminarlo come passo perchè poichè sto utilizzando comunque una matrice settata con 0s allora sicuramente nella prima colonna già ci sono gli 0s)

    # dizionario_indice_numerico_tag = {0: "N", 1: "V", 2: "A", 3: "D"}
   # recursion step: ##############################
    for t in range(1,T): #nell'esempio t partirà dalla seconda parola della frase di input (ovvero "ama") e arriverà fino all'ultima parola della frase di
        #input (ovvvero "Francesca").
        for s in range(0, N): #nell'esempio s partirà dal tag N e arriverà fino al tag 3 che è associato nel dizionario_indice_numerico_tag al tag D.
            tag_da_considerare_per_l_emissione = dizionario_indice_numerico_tag[s]
            dizionario_per_la_parola_corrente_presente_nella_lista_prob_di_emissione = lista_di_prob_di_emissione[t] #serve per prendere dalla lista di dizionari il dizionario della parola t-esima che mi serve.
            b_s_o_t_per_la_parola_corrente = dizionario_per_la_parola_corrente_presente_nella_lista_prob_di_emissione[tag_da_considerare_per_l_emissione] #prendo la prob. di emissione tra la parola t-esima e il tag s-esimo


            #calcolo il max:############
            max = np.NINF
            tag_max_parola_precedente = 0
            valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t = 0
            for s_primo in range(0,N): #s_primo va messo a destra della barra di condizionamento perchè indica il tag da cui partiamo per la parola precedente precedente mentre
                #s va messo a sinistra della barra perchè indica il tag che stiamo considerando per la parola corrente
                tag_sinistro = dizionario_indice_numerico_tag[s]
                tag_destro = dizionario_indice_numerico_tag[s_primo]

                if ((viterbi[s_primo, t - 1] != 0) and (a_s_primo_s[tag_sinistro + "|" + tag_destro] != 0)):
                    max_temp = viterbi[s_primo, t - 1] + np.log(a_s_primo_s[tag_sinistro + "|" + tag_destro])
                else:
                    max_temp = viterbi[s_primo, t - 1] * a_s_primo_s[tag_sinistro + "|" + tag_destro]


                if ((max_temp > max) and (max_temp != 0)):
                    max = max_temp
                    #print("max: ", max)

                    if (b_s_o_t_per_la_parola_corrente != 0):
                        valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t = max_temp + np.log(b_s_o_t_per_la_parola_corrente)
                    else:
                        valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t = max_temp * b_s_o_t_per_la_parola_corrente

                    tag_max_parola_precedente = dizionario_indice_numerico_tag[s_primo]


            #aggiungo il valore max nella matrice di Viterbi:
            viterbi[s,t] = valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t
            #memorizzo nel backpointer il tag assegnato alla parola precedente che ha vinto e che quindi
            #mi ha portato nell tag corrente per la parola corrente:
            #print("Metto nel backpointer in posizione "+str(s)+","+str(t)+" il tag che mi ha fatto arrivare lì che è "+str(tag_max_parola_precedente))
            backpointer[s,t] = tag_max_parola_precedente
            # print("")
            # print("")
            ############################

    #################################################

    #termination step:
    max = np.NINF
    tag_max_parola_precedente = 0
    valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t = 0
    for s in range(0,N):  # s_primo va messo a destra della barra di condizionamento perchè indica il tag da cui partiamo per la parola precedente precedente mentre
        # s va messo a sinistra della barra perchè indica il tag che stiamo considerando per la parola corrente
        tag_sinistro = "E"
        tag_destro = dizionario_indice_numerico_tag[s]


        if (viterbi[s, T - 1] != 0 and a_s_primo_s[tag_sinistro + "|" + tag_destro] != 0):
            max_temp = viterbi[s, T - 1] + np.log(a_s_primo_s[tag_sinistro + "|" + tag_destro])
        else:
            max_temp = viterbi[s, T - 1] * a_s_primo_s[tag_sinistro + "|" + tag_destro]  # ho messo come indice T-1 invece di T perchè si parte da 0 quindi l'ultima parola è la T-1.

        if ((max_temp > max) and (max_temp != 0)):
            max = max_temp
            #print("max: ", max)
            valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t = max_temp
            tag_max_parola_precedente = dizionario_indice_numerico_tag[s]



    # aggiungo il valore max nella matrice di Viterbi:
    viterbi[-1,T-1] = valore_da_mettere_eventualmente_nella_matrice_di_Viterbi_in_pos_s_t #metto -1 come indice di riga per posizionarmi esattamente sull'ultima riga della matrice di Viterbi e
    #come indice di colonna metto T-1 per posizionarmi sempre esattamente sull'ultima colonna della matrice di Viterbi.
    # memorizzo nel backpointer il tag assegnato alla parola precedente che ha vinto e che quindi
    # mi ha portato nell tag corrente per la parola corrente:
    #print("Metto nel backpointer in posizione " + str(s) + "," + str(t) + " il tag che mi ha fatto arrivare lì che è " + str(tag_max_parola_precedente))
    backpointer[-1,T-1] = tag_max_parola_precedente
    ####################

    #tag_possibili = ["N", "V", "A", "D"]
    #Adesso per restituire in output la soluzione finale usando il backpointer devo fare così (man mano salverò i vari tag in un vettore
    # che poi verrà restituito in output dall'algoritmo):
    #Devo innanzitutto posizionarmi sull'ultima cella in basso a destra della matrice di Viterbi perchè essa mi dice qual è il tag più probabile da associare all'ultima parola della frase in input:
    vettore_tags_finali = []
    tag_assegnato_all_ultima_parola_della_frase_di_input = backpointer[-1,-1]
    vettore_tags_finali.append(tag_assegnato_all_ultima_parola_della_frase_di_input)
    print("tag assegnato ALL'ULTIMA PAROLA della frase di test: ", tag_assegnato_all_ultima_parola_della_frase_di_input)
    # Adesso creo un ciclo che mi permetterà di recuperare tutti i tag assegnati dall'algoritmo alle restanti parole: ########################################
    # - Quando posizione_parola_in_matrice_di_viterbi = 1 allora
    #  siccome sotto ho -posizione_parola_in_matrice_di_viterbi allora
    #  avrò backpointer[riga_su_cui_devo_posizionarmi_nel_backpointer,-1].
    # - Quando invece posizione_parola_in_matrice_di_viterbi = 2 allora
    #  sotto avrò backpointer[riga_su_cui_devo_posizionarmi_nel_backpointer,-2].
    # - E così via fino a quando arrivo al numero massimo di parole -1 presente nella frase di test.
    # -1 perchè chiaramente per l'ultima parola già so qual è il tag che l'algoritmo gli ha assegnato e l'ho già prelevato prima con backpointer[-1,-1].
    for posizione_parola_in_matrice_di_viterbi in range(1, T):
        # Adesso sapendo qual è il tag assegnato dall'algoritmo all'ultima parola rimango sempre sull'ultima colonna del backpointer e mi posiziono in corrispondenza nella cella in corrispondenza proprio
        # del tag che è stato assegnato all'ultima parola.
        # ES: suppongo che il tag assegnato all'ultima parola sia A, allora poichè so che il tag A corrisponde alla riga 2 (partendo da 0) del backpointer allora mi posiziono
        # nella cella backpointer[2,-1] e leggo il tag che c'è. Questo sarà proprio il tag che è stato assegnato dall'algoritmo alla penultima parola (che nel nostro esempio è "ama")
        riga_su_cui_devo_posizionarmi_nel_backpointer = dizionario_per_passare_dal_tag_al_numero[tag_assegnato_all_ultima_parola_della_frase_di_input]
        tag_assegnato_alla_parola_corrente_della_frase_di_input = backpointer[riga_su_cui_devo_posizionarmi_nel_backpointer, -posizione_parola_in_matrice_di_viterbi]  # c'era backpointer[riga_su_cui_devo_posizionarmi_nel_backpointer,-1]
        vettore_tags_finali.append(tag_assegnato_alla_parola_corrente_della_frase_di_input)
        print("tag assegnato alla parola numero " + str(T-posizione_parola_in_matrice_di_viterbi) + " della frase di test: ",tag_assegnato_alla_parola_corrente_della_frase_di_input)
    print("")
    print("")
    ############################################################################################################################################################

    return vettore_tags_finali[::-1] #inverto il vettore_tags_finali in modo da restituire i tags ordinati dalla prima parola all'ultima parola della frase di test.




tags_assegnati_a_tutte_le_frasi_di_test = [] #mi servirà per memorizzare tutte le predizioni fatte per tutte le frasi di test (puoi crearlo dinamicamente con numpy)
#Creo un dizionario che tiene conto delle parole per le quali sono stati già calcolate le prob. di emissione, in questo modo velocizzo l'algoritmo in quanto
#per le parole per cui è già stata calcolata la prob. di emissione non dovrò ricalcolarla nuovamente. (Più l'algoritmo considera nuove parole e più la prob. che la velocità di esecuzione aumenti si incrementa)
# Esempio di come sarà il dizionario di dizionari:
# dizionario_con_prob_di_emissione_di_parole_gia_considerate = {"parola1":{b_s_o_t_parola_1},
#                                                               "parola2":{b_s_o_t_parola_2}
#                                                               }
#dizionario_con_prob_di_emissione_di_parole_gia_considerate = {} #dizionario di dizionari

frasi_test_fuori_dominio_en = Estrazione_dati_BIO_tagging_Wikipedia_en.frasi_test_fuori_dominio_en()
frasi_train, tag_possibili, dizionario_indice_numerico_tag, dizionario_per_passare_dal_tag_al_numero, a_s_primo_s = Estrazione_dati_BIO_tagging_Wikipedia_en.caricamento_dati_BIO_tagging_en()
dizionario_count_tags_en = Estrazione_dati_BIO_tagging_Wikipedia_en.calcolo_C_s(frasi_train) #Questa funzione mi permette di poter calcolare per ogni possible tag il Count(tag) ovvero il numero di volte in cui un certo tag è
#stato assegnato ad una parola del training set.


print("")
print("frasi_test_fuori_dominio_en: ")
print(frasi_test_fuori_dominio_en)
print("")


#Deserializzo il dizionario a_s_primo_s:
# Loading it from file
with open('a_s_primo_s.json', 'r') as json_file:
    a_s_primo_s = json.load(json_file)

#Deserializzo il dizionario_con_prob_di_emissione_di_parole_gia_considerate:
with open('dizionario_con_prob_di_emissione_di_parole_gia_considerate.json', 'r') as json_file:
    dizionario_con_prob_di_emissione_di_parole_gia_considerate = json.load(json_file)
############################################################################


# Questo codice mi serve per assegnare una prob. bassissima a tutte le prob. di transizione che hanno prob. pari a 0.
for k, v in a_s_primo_s.items():
    #print(k+": " + str(v))
    if(a_s_primo_s[k] == 0):
        a_s_primo_s[k] = 1e-80
###################################################################################################################



for frase_test in frasi_test_fuori_dominio_en:
    #if(num_frasi_considerate < 3): #considero solo le prime 3 frasi di test
    #print("frase_test: ")
    #print(frase_test)
    lista_di_prob_di_emissione = []
    frase_test_splittata_per_singola_parola = frase_test.split(" ")
    frase_test_splittata_per_singola_parola[-1:] = [] # elimino l'ultimo elemento della lista perchè sarebbe '' e quindi non serve a nulla.
    #print("frase_test_splittata_per_singola_parola: ")
    #print(frase_test_splittata_per_singola_parola)
    #print("")
    #print("")
    for i in range(0, len(frase_test_splittata_per_singola_parola)):
        parola_frase_test_con_tag = frase_test.split(" ")[i]
        parola_frase_test = parola_frase_test_con_tag.split("\t")[0]
        #print("parola_frase_test: ", parola_frase_test)
        if ((parola_frase_test in dizionario_con_prob_di_emissione_di_parole_gia_considerate) == False):
            # se entro qui vuol dire che le prob. di emissione per la parola corrente ancora non le ho calcolate (perchè la parola corrente è sconosciuta) e quindi lo faccio ora.
            b_s_o_t = calcolo_prob_di_emissione(parola_frase_test,frasi_train, dizionario_count_tags_en)
            dizionario_con_prob_di_emissione_di_parole_gia_considerate[parola_frase_test] = b_s_o_t
        else:
            # se entro qui vuol dire che posso subito prendere le prob. di emissione per la parola corrente perchè sono state già calcolate.
            b_s_o_t = dizionario_con_prob_di_emissione_di_parole_gia_considerate[parola_frase_test]
            # print("La prob. di emissione della parola " + parola_frase_test + " è già presente.")
            # print("prob. di emissione: ", b_s_o_t)

        lista_di_prob_di_emissione.append(b_s_o_t) #il primo elemento della lista sarà la prob. di emissione della prima parola della frase di test (quindi ad es. nell'esercizio giocattolo era "Paolo")
    # print("")
    # print("")
    # print("")
    # print("")
    # print("lista_di_prob_di_emissione per ogni tag per ogni parola della frase di input:")
    # print(lista_di_prob_di_emissione)
    # print("")
    # print("")
    #############################################################################################################################################

    ###################################
    #All'algoritmo di Viterbi darò solamente la frase di test corrente come una semplice stringa senza i tag, quindi tolgo i tag dalla frase corrente:
    frase_di_test_da_dare_in_input_a_Viterbi = ""
    prima_parola = True
    tags_assegnati_frase_di_test_corrente = [] #conterrà i tags ordinati dalla prima parola all'ultima che vengono assegnati dall'algoritmo di Viterbi alle parole della frase di test corrente.
    for parola_con_tag in frase_test_splittata_per_singola_parola:
        parola_senza_tag = parola_con_tag.split("\t")[0]
        if(prima_parola):
            frase_di_test_da_dare_in_input_a_Viterbi = frase_di_test_da_dare_in_input_a_Viterbi + parola_senza_tag
            prima_parola = False
        else:
            frase_di_test_da_dare_in_input_a_Viterbi = frase_di_test_da_dare_in_input_a_Viterbi + " " + parola_senza_tag
    print("frase_di_test_da_dare_in_input_a_Viterbi: ", frase_di_test_da_dare_in_input_a_Viterbi)
    print("")
    ####################################

    ########################################################################################################################
    #Eseguo l'algoritmo di Viterbi e prendo i risultati dei tag assegnati ad ogni parola della frase data in input:
    tags_assegnati_frase_di_test_corrente = Viterbi(frase_di_test_da_dare_in_input_a_Viterbi, tag_possibili, a_s_primo_s, lista_di_prob_di_emissione, dizionario_indice_numerico_tag, dizionario_per_passare_dal_tag_al_numero)
    # print("")
    # print("")
    # print("tags_assegnati_frase_di_test_corrente (dalla prima all'ultima parola):")
    # print(tags_assegnati_frase_di_test_corrente)
    # print("")
    # print("")
    #MEMORIZZO I TAGS ASSEGNATI DALL'ALGORITMO ALLA FRASE DI TEST CORRENTE IN UNA LISTA CHE CONTERRA' TUTTE LE PREDIZIONI FATTE PER OGNI FRASE DI TEST, IN MODO TALE CHE ####
    #SUCCESSIVAMENTE POTRO' UTILIZZARLA PER CALCOLARE LE VARIE METRICHE:
    tags_assegnati_a_tutte_le_frasi_di_test.append(tags_assegnati_frase_di_test_corrente)
    ################################################################################################################################################################

    #num_frasi_considerate+=1
    ########################################################################################################################
#####################################################################

print("")
print("TAGS PREDETTI PER OGNI FRASE DI TEST: ")
print(tags_assegnati_a_tutte_le_frasi_di_test)
print("")

accuratezza_modello = Calcolo_metriche.accuratezza(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test)
print("accuratezza_modello: ", accuratezza_modello)

print("")
precision_modello = Calcolo_metriche.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("precisione_modello PER: ", precision_modello)
precision_modello = Calcolo_metriche.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("precisione_modello LOC: ", precision_modello)
precision_modello = Calcolo_metriche.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("precisione_modello ORG: ", precision_modello)
precision_modello = Calcolo_metriche.precision(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("precisione_modello MISC: ", precision_modello)

print("")
recall_modello = Calcolo_metriche.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("recall_modello PER: ", recall_modello)
recall_modello = Calcolo_metriche.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("recall_modello LOC: ", recall_modello)
recall_modello = Calcolo_metriche.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("recall_modello ORG: ", recall_modello)
recall_modello = Calcolo_metriche.recall(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("recall_modello MISC: ", recall_modello)
print("")

print("")
acc_modello_B_I_PER = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("acc_modello_B_I_PER: ", acc_modello_B_I_PER)
acc_modello_B_I_LOC = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("acc_modello_B_I_LOC: ", acc_modello_B_I_LOC)
acc_modello_B_I_ORG = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("acc_modello_B_I_ORG: ", acc_modello_B_I_ORG)
acc_modello_B_I_MISC = Calcolo_metriche.accuratezza_B_I_entity(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("acc_modello_B_I_MISC: ", acc_modello_B_I_MISC)
print("")

print("")
acc_modello_B_I_consecutivi_PER = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "PER")
print("acc_modello_B_I_consecutivi_PER: ", acc_modello_B_I_consecutivi_PER)
acc_modello_B_I_consecutivi_LOC = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "LOC")
print("acc_modello_B_I_consecutivi_LOC: ", acc_modello_B_I_consecutivi_LOC)
acc_modello_B_I_consecutivi_ORG = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "ORG")
print("acc_modello_B_I_consecutivi_ORG: ", acc_modello_B_I_consecutivi_ORG)
acc_modello_B_I_consecutivi_MISC = Calcolo_metriche.accuratezza_B_I_consecutivi(frasi_test_fuori_dominio_en, tags_assegnati_a_tutte_le_frasi_di_test, "MISC")
print("acc_modello_B_I_consecutivi_MISC: ", acc_modello_B_I_consecutivi_MISC)
print("")