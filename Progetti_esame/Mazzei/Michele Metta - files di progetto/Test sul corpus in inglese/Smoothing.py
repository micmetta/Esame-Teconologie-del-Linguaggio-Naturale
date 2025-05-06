
####################################################### Qui ho implementato le varie tecniche di smoothing. ###################################################################

import importlib
import json

def sempre_O(b_s_o_t): #assegna prob. 1 al tag O per la parola non presente nel training set.
    b_s_o_t["O"] = 1
    return b_s_o_t

def O_B_MISC_stessa_prob(b_s_o_t): #assegna la stessa prob. di emissione (0.5 ciascuno) ai tag O e B-MISC per la parola che non è presente nel training set.
    b_s_o_t["O"] = 0.5
    b_s_o_t["B-MISC"] = 0.5
    return b_s_o_t

def uniforme_su_tutti_i_tags(b_s_o_t): #assegna la stessa prob. di emissione (1/num_tags_NER) a tutti i tags.
    print("len(b_s_o_t.keys()): ", len(b_s_o_t.keys()))
    numero_chiavi_dizionario = len(b_s_o_t.keys())
    b_s_o_t["B-PER"] = 1/numero_chiavi_dizionario
    b_s_o_t["I-PER"] = 1/numero_chiavi_dizionario
    b_s_o_t["B-ORG"] = 1/numero_chiavi_dizionario
    b_s_o_t["I-ORG"] = 1/numero_chiavi_dizionario
    b_s_o_t["B-LOC"] = 1/numero_chiavi_dizionario
    b_s_o_t["I-LOC"] = 1/numero_chiavi_dizionario
    b_s_o_t["B-MISC"] = 1/numero_chiavi_dizionario
    b_s_o_t["I-MISC"] = 1/numero_chiavi_dizionario
    b_s_o_t["O"] = 1/numero_chiavi_dizionario
    return b_s_o_t


def statistica_development_set_en(): #en
    # Le prob. di emissione per ogni tag assegnate da questa tecniche alle parole sconosciute le ho pre-calcolate nello script chiamato
    # "calcolo la distribuzione di prob delle parole che compaiono una sola volta nel validation set.py".
    with open('prob_di_emissione_pre_calcolate_per_le_parole_sconosciute_assegnate_dalla_tecnica_che_utilizza_il_DS_en.json', 'r') as json_file:
        dizionari_prob_emissione_per_ogni_tag = json.load(json_file)
    # print("dizionari_prob_emissione_per_ogni_tag: ", dizionari_prob_emissione_per_ogni_tag)

    return dizionari_prob_emissione_per_ogni_tag


def statistica_development_set(): #ita
    # Le prob. di emissione per ogni tag assegnate da questa tecniche alle parole sconosciute le ho pre-calcolate nello script chiamato
    # "calcolo la distribuzione di prob delle parole che compaiono una sola volta nel validation set.py".
    with open('prob_di_emissione_pre_calcolate_per_le_parole_sconosciute_assegnate_dalla_tecnica_che_utilizza_il_DS.json', 'r') as json_file:
        dizionari_prob_emissione_per_ogni_tag = json.load(json_file)
    # print("dizionari_prob_emissione_per_ogni_tag: ", dizionari_prob_emissione_per_ogni_tag)

    return dizionari_prob_emissione_per_ogni_tag

