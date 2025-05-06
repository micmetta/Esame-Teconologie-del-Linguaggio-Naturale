from nltk.corpus import framenet as fn
from nltk.corpus.reader.framenet import PrettyList

from operator import itemgetter
from pprint import pprint
import nltk
import re
import sys
import hashlib
import random
from random import randint
from random import seed
from nltk.corpus import wordnet as wn



def print_frames_with_IDs():
    for x in fn.frames():
        print('{}\t{}'.format(x.ID, x.name))

def get_frams_IDs():
    return [f.ID for f in fn.frames()]

def getFrameSetForStudent(surname, list_len=5):
    nof_frames = len(fn.frames())
    base_idx = (abs(int(hashlib.sha512(surname.encode('utf-8')).hexdigest(), 16)) % nof_frames)
    print('\nstudent: ' + surname)
    framenet_IDs = get_frams_IDs()
    i = 0
    offset = 0
    seed(1)
    while i < list_len:
        fID = framenet_IDs[(base_idx+offset)%nof_frames]
        f = fn.frame(fID)
        fNAME = f.name
        print('\tID: {a:4d}\tframe: {framename}'.format(a=fID, framename=fNAME))
        offset = randint(0, nof_frames)
        i += 1


#getFrameSetForStudent('Metta') #stampiamo quali frames vengono attivati con il nostro cognome

#Per l'esercitazione dobbiamo fare questo:
#- Prendiamo il gruppo di frames attivati dal nostro cognome e li analizziamo.
#- Per analizzarli si intende andare a disambiguare i vari elementi di ogni frame andandoli a
#mappare su Wordnet (lo facciamo noi a mano).
#- Dopodichè la stessa operazione la facciamo fare al programma.
#- Infine valutiamo l'output del programma rispetto alla nostra annotazione (che assumiamo essere
# l'annotazione gold).


# student: Metta
# 	ID: 1822	frame: Being_included (included è aggettivo)
# 	ID: 2831	frame: Emergency
# 	ID:  388	frame: Atonement (espiazione)
# 	ID: 2018	frame: Collocation_image_schema (Schema dell'immagine di collocazione)
# 	ID: 2656	frame: Law_enforcement_agency

'''
- Being 
- Emergency
- Atonement 
- Collocation
- Agency
'''
'''
print("")
#controll se per ogni termine esiste almeno un synset a cui sono associati su wordnet:
lista_termini = ["Being", "Emergency", "Atonement", "COllocation", "Agency"]
for termine in lista_termini:
    print("synsent/s associati a " + termine + ": " + str(wn.synsets(termine)))
######################################################################################
print("")
print(wn.synset('being.n.01').definition())
print(wn.synset('being.n.01'))

for ss in wn.synsets("agency"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
'''
########################################################################################################################
#Adesso mappo ogni FEs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i FEs di ogni frame:
print("Info sul frame chiamato Being_included:")
frame = fn.frame_by_name('Being_included')
print(frame)
print("")
print("Tutti i frame element del frame Being_included: ")
print(sorted([x for x in frame.FE])) #PER STAMPARE I FEs DI UN CERTO FRAME (in questo caso 'Being_included')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
[FE] 2 frame elements
            Core: Part (10786), Whole (10785)
'''

print("Stampo tutte le definizioni dei frame elements del frame Being_included:")
FEs = frame.FE.keys()
for fe in FEs:
    fed = frame.FE[fe]
    print('\tFE: {}\tDEF: {}'.format(fe, fed.definition)) #stampiamo la definizione del FE trovato

for ss in wn.synsets("whole"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")

########################################################################################################################

########################################################################################################################
#Adesso mappo ogni FEs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i FEs di ogni frame:
print("Info sul frame chiamato Emergency:")
frame = fn.frame_by_name('Emergency')
print(frame)
print("")
print("Tutti i frame elements del frame Emergency: ")
print(sorted([x for x in frame.FE])) #PER STAMPARE I FEs DI UN CERTO FRAME (in questo caso 'Emergency')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutti i frame element del frame Emergency: 
['Circumstances', 'Domain', 'Duration', 'Entity', 'Experiencer', 'Frequency', 'Manner', 'Place', 'Time', 'Timespan', 'Undesirable_event']
'''

print("Stampo tutte le definizioni dei frame elements del frame Emergency:")
FEs = frame.FE.keys()
for fe in FEs:
    fed = frame.FE[fe]
    print('\tFE: {}\tDEF: {}'.format(fe, fed.definition)) #stampiamo la definizione del FE trovato


for ss in wn.synsets("Event"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")

########################################################################################################################


########################################################################################################################
#Adesso mappo ogni FEs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i FEs di ogni frame:
print("Info sul frame chiamato Atonement:")
frame = fn.frame_by_name('Atonement')
print(frame)
print("")
print("Tutti i frame elements del frame Atonement: ")
print(sorted([x for x in frame.FE])) #PER STAMPARE I FEs DI UN CERTO FRAME (in questo caso 'Atonement')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutti i frame element del frame Emergency: 
['Agent', 'Amends', 'Degree', 'Manner', 'Place', 'Purpose', 'Time', 'Wrong']
'''

print("Stampo tutte le definizioni dei frame elements del frame Atonement:")
FEs = frame.FE.keys()
for fe in FEs:
    fed = frame.FE[fe]
    print('\tFE: {}\tDEF: {}'.format(fe, fed.definition)) #stampiamo la definizione del FE trovato


for ss in wn.synsets("Wrong"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
########################################################################################################################


########################################################################################################################
#Adesso mappo ogni FEs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i FEs di ogni frame:
print("Info sul frame chiamato Collocation_image_schema:")
frame = fn.frame_by_name('Collocation_image_schema')
print(frame)
print("")
print("Tutti i frame elements del frame Collocation_image_schema: ")
print(sorted([x for x in frame.FE])) #PER STAMPARE I FEs DI UN CERTO FRAME (in questo caso 'Collocation_image_schema')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutti i frame element del frame Emergency: 
['Ground', 'Profiled_region']
'''

print("Stampo tutte le definizioni dei frame elements del frame Collocation_image_schema:")
FEs = frame.FE.keys()
for fe in FEs:
    fed = frame.FE[fe]
    print('\tFE: {}\tDEF: {}'.format(fe, fed.definition)) #stampiamo la definizione del FE trovato


for ss in wn.synsets("region"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")

########################################################################################################################


########################################################################################################################
#Adesso mappo ogni FEs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i FEs di ogni frame:
print("Info sul frame chiamato Law_enforcement_agency:")
frame = fn.frame_by_name('Law_enforcement_agency')
print(frame)
print("")
print("Tutti i frame elements del frame Law_enforcement_agency: ")
print(sorted([x for x in frame.FE])) #PER STAMPARE I FEs DI UN CERTO FRAME (in questo caso 'Law_enforcement_agency')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.

'''
Tutti i frame elements del frame Law_enforcement_agency: 
['Agency', 'Descriptor', 'Jurisdiction', 'Members', 'Name', 'Period_of_existence', 'Place', 'Purpose']
'''

print("Stampo tutte le definizioni dei frame elements del frame Law_enforcement_agency:")
FEs = frame.FE.keys()
for fe in FEs:
    fed = frame.FE[fe]
    print('\tFE: {}\tDEF: {}'.format(fe, fed.definition)) #stampiamo la definizione del FE trovato


for ss in wn.synsets("Purpose"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")

########################################################################################################################




#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#ADESSO CERCO LE LUs di ogni frame:

#Il frame: Being_included NON HA LUs
#Adesso mappo ogni LUs di ogni frame su un certo synset di Wordnet:
#Innanzitutto devo ottenere tutti i LUs di ogni frame:

########################################################################################################################
print("Info sul frame chiamato Emergency:") #ha solo 1 LU.
frame = fn.frame_by_name('Emergency')
print(frame)
print("")
print("Tutte le LUs del frame Emergency: ")
print(sorted([x for x in frame.lexUnit])) #PER STAMPARE tutte le LUs DI UN CERTO FRAME (in questo caso 'Being_included')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutte le LUs del frame Emergency: 
['emergency.n']
'''

print("Stampo tutte le definizioni delle LUs del frame Emergency:")
LUs = frame.lexUnit.keys()
for lu in LUs:
    fed = frame.lexUnit[lu]
    print('\tFE: {}\tDEF: {}'.format(lu, fed.definition)) #stampiamo la definizione della LU trovata

print("")
print("")
print("Stampo tutti i synset che sono associati alla parola che sto considerando:")
for ss in wn.synsets("emergency"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
########################################################################################################################


########################################################################################################################
print("Info sul frame chiamato Atonement:")
frame = fn.frame_by_name('Atonement')
print(frame)
print("")
print("Tutte le LUs del frame Atonement: ")
print(sorted([x for x in frame.lexUnit])) #PER STAMPARE tutte le LUs DI UN CERTO FRAME (in questo caso 'Being_included')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutte le LUs del frame Atonement: 
['atone.v', 'atonement.n', 'atoner.n', 'expiate.v', 'expiation.n', 'expiator.n', 'expiatory.a']
'''

print("Stampo tutte le definizioni delle LUs del frame Atonement:")
LUs = frame.lexUnit.keys()
for lu in LUs:
    fed = frame.lexUnit[lu]
    print('\tFE: {}\tDEF: {}'.format(lu, fed.definition)) #stampiamo la definizione della LU trovata

print("")
print("")
print("Stampo tutti i synset che sono associati alla parola che sto considerando:")
for ss in wn.synsets("expiatory"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
########################################################################################################################



########################################################################################################################
print("Info sul frame chiamato Collocation_image_schema:") #non ha LUs
frame = fn.frame_by_name('Collocation_image_schema')
print(frame)
print("")
print("Tutte le LUs del frame Collocation_image_schema: ")
print(sorted([x for x in frame.lexUnit])) #PER STAMPARE tutte le LUs DI UN CERTO FRAME (in questo caso 'Being_included')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutte le LUs del frame Collocation_image_schema: 
['atone.v', 'atonement.n', 'atoner.n', 'expiate.v', 'expiation.n', 'expiator.n', 'expiatory.a']
'''

print("Stampo tutte le definizioni delle LUs del frame Collocation_image_schema:")
LUs = frame.lexUnit.keys()
for lu in LUs:
    fed = frame.lexUnit[lu]
    print('\tFE: {}\tDEF: {}'.format(lu, fed.definition)) #stampiamo la definizione della LU trovata

print("")
print("")
print("Stampo tutti i synset che sono associati alla parola che sto considerando:")
for ss in wn.synsets("expiatory"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
########################################################################################################################



########################################################################################################################
print("Info sul frame chiamato Law_enforcement_agency:")
frame = fn.frame_by_name('Law_enforcement_agency')
print(frame)
print("")
print("Tutte le LUs del frame Law_enforcement_agency: ")
print(sorted([x for x in frame.lexUnit])) #PER STAMPARE tutte le LUs DI UN CERTO FRAME (in questo caso 'Being_included')
#usiamo questa istruzione che ci permette di ordinarli in ordine alfabetico. I frame appartenenti al dominio medico sono in genere
#molto più ricchi rispetto agli altri come ad esempio quello della Percezione.
'''
Tutte le LUs del frame Law_enforcement_agency: 
['fire department.n', 'police department.n', 'police.n']
'''

print("Stampo tutte le definizioni delle LUs del frame Law_enforcement_agency:")
LUs = frame.lexUnit.keys()
for lu in LUs:
    fed = frame.lexUnit[lu]
    print('\tFE: {}\tDEF: {}'.format(lu, fed.definition)) #stampiamo la definizione della LU trovata

print("")
print("")
print("Stampo tutti i synset che sono associati alla parola che sto considerando:")
for ss in wn.synsets("police"):
    print(ss.name()) #nome synset
    print(ss.lemma_names()) #lista nomi concetti presenti in quel synset
    print("")
    print("")
########################################################################################################################