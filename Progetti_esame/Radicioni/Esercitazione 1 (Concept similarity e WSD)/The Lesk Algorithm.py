import nltk
# nltk.download('wordnet')
# nltk.download('semcor')
from nltk.corpus import semcor
import re
from nltk.corpus import wordnet as wn
import numpy as np


def ComputeOverlap(signature, context):
    lista_esempi = signature[0]
    glossa = signature[1]
    print("lista_esempi: ", lista_esempi)
    overlap = 0
    if(lista_esempi != []):
        for esempio in lista_esempi:
            lista_parole_esempio = esempio.split(" ")
            print("lista_parole_esempio: ", lista_parole_esempio)
            for parola_esempio in lista_parole_esempio:
                for parola_context in context:
                    if(parola_esempio == parola_context):
                        print("parola_esempio: ", parola_esempio)
                        print("parola_context: ", parola_context)
                        overlap += 1

    lista_parole_glossa = glossa.split(" ")
    print("lista_parole_glossa: ", lista_parole_glossa)
    for parola_glossa in lista_parole_glossa:
        for parola_context in context:
            if (parola_glossa == parola_context):
                print("parola_glossa: ", parola_glossa)
                print("parola_context: ", parola_context)
                overlap += 1

    return overlap




def The_Lesk_Algorithm(word, sentence, tutti_i_sensi_della_parola_da_disambiguare):
    print("word DENTRO LESK: ", word)
    print("sentence DENTRO LESK: ", sentence)
    #tutti_i_sensi_della_parola_di_input = wn.synsets(word)
    print("tutti_i_sensi_della_parola_di_input: ", tutti_i_sensi_della_parola_da_disambiguare)
    #best_sense = wn.synsets(word)[0] #inizilizzo best_sense con il senso più frequente.
    best_sense = tutti_i_sensi_della_parola_da_disambiguare[0]

    print("best_sense iniziale: ", best_sense)
    print("")
    print("")

    max_overlap = 0
    context = sentence #inizializzo il contesto con tutte le parole della frase (context è una lista di parole)

    for senso in tutti_i_sensi_della_parola_da_disambiguare:
        print("senso corrente: ", senso)
        lista_esempi = senso.examples() #è una lista di frasi (può anche non essercene neanche una di frase e quindi sarà [])
        #print("lista_esempi: ", lista_esempi)
        glossa = senso.definition() #la glossa è una stringa e non sarà mai vuota.
        #print("glossa: ", glossa)
        signature = []
        signature.append(lista_esempi)
        signature.append(glossa)
        print("context: ", context)
        print("signature: ", signature)
        overlap = ComputeOverlap(signature, context)
        print("overlap: ", overlap)

        if(overlap > max_overlap):
            max_overlap = overlap
            best_sense = senso
        print("")
        print("")


    return best_sense



def lemma_list(sent):
    return [l.label() if isinstance(l, nltk.tree.Tree) else None for l in sent]




'''
#print(semcor.tagged_sents(tag="sem")[0])
print(len(semcor.sents()[0]))

#print(semcor.tagged_sents()[0])
print(lemma_list(semcor.tagged_sents(tag="sem")[0]))
print(len(lemma_list(semcor.tagged_sents(tag="sem")[0])))
'''

#inizio

#seleziono randomicamente le 50 frasi da considerare: #(min = 0, max = 37176)
#print("len(semcor.sents()): ", len(semcor.sents()))
lista_di_indici_frasi_selezionate = np.random.randint(low=0, high=37177, size=50) #nella funzione devo mettere 37176+1 come max. high=37177
print("lista_di_indici_frasi_selezionate: ", lista_di_indici_frasi_selezionate)


num_parole_disambiguate = 0
num_parole_disambiguate_correttamente = 0

for indice_frase_scelta in lista_di_indici_frasi_selezionate:
    print("")
    print("")
    frase_di_input = []
    #print(semcor.sents()[0])
    for parola in semcor.sents()[indice_frase_scelta]:
        #print(parola)
        frase_di_input.append(parola)
    print("frase_di_input: ", frase_di_input)

    # print("")
    # print("")
    # tagged_sentence = [[str(c) for c in s] for s in semcor.tagged_sents(tag='sem')[26255:26255+1]] #prendo solo la prima frase
    # print(tagged_sentence)
    print("")
    print("")

    lista_parole_frase_di_input_con_synset = []
    for s in semcor.tagged_sents(tag='sem')[indice_frase_scelta:indice_frase_scelta+1]:
        for c in s:
            #print(str(c))
            lista_parole_frase_di_input_con_synset.append(str(c))

    print("")
    print("lista_parole_frase_di_input_con_synset:")
    print(lista_parole_frase_di_input_con_synset)
    print("")

    lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata = [] #conterrà tutte le coppie costitute da parola-synset_associato (dove chiaramente
    #ogni parola sarà però un nome perchè sono quelli che a noi interessano).
    for parola_parole_piu_synset_di_appartenenza in lista_parole_frase_di_input_con_synset:
        parola_parole_piu_synset_di_appartenenza_splittata = parola_parole_piu_synset_di_appartenenza.split(" ")
        if(len(parola_parole_piu_synset_di_appartenenza_splittata) > 1):

            #se entro qui vuol dire che NON sto considerando le parole senza synset (le STOPWORDS - SW):
            print(parola_parole_piu_synset_di_appartenenza_splittata)
            synset_di_appartenenza = parola_parole_piu_synset_di_appartenenza_splittata[0]
            insieme_di_parole_assegnate_a_quel_synset = parola_parole_piu_synset_di_appartenenza_splittata[1:]
            print("synset_di_appartenenza: ", synset_di_appartenenza)
            print("insieme_di_parole_assegnate_a_quel_synset: ", insieme_di_parole_assegnate_a_quel_synset)
            #adesso cerco a caso dei sostantivi tra le parole della frase corrente

            if ("Lemma" in synset_di_appartenenza):
                synset_di_appartenenza_splittato = synset_di_appartenenza.split("Lemma")

                #synset_di_appartenenza_splittato.remove("(") #rimuovo dalla lista le tutte le "(" perchè sono inutili.
                if (synset_di_appartenenza_splittato[0] == "("):
                    synset_di_appartenenza_splittato.remove("(")  # rimuovo dalla lista le tutte le "(" perchè sono inutili.
                #print("synset_di_appartenenza_splittato: ", synset_di_appartenenza_splittato)



                #A questo punto avrò solamente questo ad esempio: ["('group.n.01.group')"] ovvero solo il synset corretto (o i synset) associato a quell'insieme di parole presenti in insieme_di_parole_assegnate_a_quel_synset.
                #insieme_di_parole_assegnate_a_quel_synset = ['(NE', 'Fulton', 'County', 'Grand', 'Jury))'].

                #Adesso posso controllare se il synset corrente appartiene alla categoria dei nomi:
                #print("synset_di_appartenenza_splittato[0]: ", synset_di_appartenenza_splittato[0])
                synset_di_appartenenza_splittato_in_base_al_punto = synset_di_appartenenza_splittato[0].split(".")
                print("synset_di_appartenenza_splittato_in_base_al_punto: ", synset_di_appartenenza_splittato_in_base_al_punto)
                print("")

                tag = synset_di_appartenenza_splittato_in_base_al_punto[1]
                #print("tag: ", tag)

                if(tag == "n"): #a noi interessano solo i sostantivi perchè solo questi devi considerare nell algoritmo di LESK
                    #print("synset_di_appartenenza_splittato_in_base_al_punto: ", synset_di_appartenenza_splittato_in_base_al_punto)
                    nome_synset_gold = synset_di_appartenenza_splittato_in_base_al_punto[0].split("'")[1] + "." + synset_di_appartenenza_splittato_in_base_al_punto[1] + "." + synset_di_appartenenza_splittato_in_base_al_punto[2]
                    #print("nome_synset_gold: ", nome_synset_gold)
                    #Adesso nella variabile nome_synset_gold ci sarà tutto il nome del synset corrente (che è sicuramente associato ad un nome).

                    #Adesso devo prendere tutte le parole associate a questo synset e metterle in una lista:
                    lista_termini = []
                    for termine in insieme_di_parole_assegnate_a_quel_synset:
                        if(termine != "(NE"):
                            #print("termine: ", termine)
                            termine = re.sub("\)", "", termine)
                            lista_termini.append(termine)
                    #print("lista_termini: ", lista_termini)


                    for parola in lista_termini:
                        coppia_parola_rispettivo_synset = []
                        coppia_parola_rispettivo_synset.append(parola)
                        coppia_parola_rispettivo_synset.append(str(nome_synset_gold))
                        lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata.append(coppia_parola_rispettivo_synset)

            else:
                continue #salto il synset corrente perchè già so che non si tratta di un nome.

    print("")
    print("lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata: ")
    print(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata)
    print("len(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata): ", len(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata) )
    print("")


    #Seleziono in maniera casuale un nome presente in questa lista:
    #PER IL MOMENTO LO SELEZIONO IO:
    #lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata[0] = ['Fulton', 'group.n.01']
    #DEVO VERIFICARE CHE IL TERMINE SELEZIONATO SIA VERAMENTE AMBIGUO ALTRIMENTI non lo considero e ne utilizzo un altro:
    num_max_sostantivi_frase_scelta = len(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata)

    for i in range(0, num_max_sostantivi_frase_scelta):
        parola_da_disambiguare = str(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata[i][0])
        synset_gold = str(lista_di_coppie_di_parola_con_rispettivo_synset_presenti_nella_frase_selezionata[i][1])
        tutti_i_sensi_della_parola_da_disambiguare = wn.synsets(parola_da_disambiguare) #alcuni synset non hanno nei vari synset possibili quello che è veramente quello reale (es: Grand)

        #controllo se tutti_i_sensi_della_parola_da_disambiguare c'è quello gold altrimenti lo aggiungo io:
        presente = False
        for synset in tutti_i_sensi_della_parola_da_disambiguare:
            if(synset.name() == synset_gold):
                presente = True
                break
        if(presente == False):
            tutti_i_sensi_della_parola_da_disambiguare.append(wn.synset(synset_gold))


        #DEVO VERIFICARE CHE L'INSIEME DI TUTTI I SENSI POSSIBILI NON SIA VUOTO:
        if(len(tutti_i_sensi_della_parola_da_disambiguare) >= 1):
            print("")
            print("")
            print("parola_da_disambiguare: ", parola_da_disambiguare)
            print("len(tutti_i_sensi_della_parola_da_disambiguare): ", len(tutti_i_sensi_della_parola_da_disambiguare))
            print("synset_gold: ", synset_gold)
            print("")
            #best_sense = The_Lesk_Algorithm(parola_da_disambiguare, frase_di_input, tutti_i_sensi_della_parola_da_disambiguare) #ricordati di cambiare la FRASE DI INPUT IN MANIERA RANDOMICA !!!!
            best_sense = The_Lesk_Algorithm(parola_da_disambiguare, frase_di_input, tutti_i_sensi_della_parola_da_disambiguare)

            print("synset_gold: ", synset_gold)
            print("best_sense per la parola " + parola_da_disambiguare + ": " + str(best_sense))

            num_parole_disambiguate += 1

            if(best_sense.name() == synset_gold):
                print("corretto!!")
                num_parole_disambiguate_correttamente += 1

print("num_parole_disambiguate: ", num_parole_disambiguate)
print("num_parole_disambiguate_correttamente: ", num_parole_disambiguate_correttamente)
print("accuratezza totale: ", (num_parole_disambiguate_correttamente/num_parole_disambiguate) )

