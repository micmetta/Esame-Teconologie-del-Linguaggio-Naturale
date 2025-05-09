In questo repository è presente la cartella "Progetti_esame", che raccoglie tutti i progetti realizzati per l’esame di **Tecnologie del Linguaggio Naturale (TLN)** durante la laurea magistrale.

- I progetti sono organizzati in sottocartelle, suddivise in base ai tre professori che hanno tenuto le rispettive parti del corso.

## 📌 Progetto – Prof. A. Mazzei

- **Named Entity Recognition (NER)** su corpus italiano e inglese (annotati in BIO);
- Confronto tra modelli probabilistici: **HMM**, **MEMM** e due baseline;
- Analisi delle performance con metriche di Accuracy, Precision, Recall per entità: PER, LOC, ORG, MISC;
- Codice interamente sviluppato in Python.


## 📌 Progetti – Prof. D. Radicioni

- **Concept Similarity & Word Sense Disambiguation (WSD)**: uso di metriche (Wu & Palmer, Leacock-Chodorow, Shortest Path) su WordNet.
- **Text Categorization** tramite rappresentazioni vettoriali e metodo di Rocchio.
- **FrameNet to WordNet Mapping**: disambiguazione automatica di FrameName, Frame Elements e Lexical Units tramite grafi semantici.


## 📌 Progetti – Prof. L. Di Caro

### 🔹 1. Semantica lessicale e disambiguazione
Una raccolta di esercitazioni teorico-pratiche su:
- **Topic Modeling** con LDA su articoli di Wikipedia e visualizzazione tramite `pyLDAvis`;
- **Document Segmentation** ispirata al metodo Text-Tiling;
- **False Friends Detection** tra inglese e italiano usando metriche semantiche (Wu & Palmer);
- **Teoria di Hanks**: analisi valenziale su verbi in corpus annotato;
- **Content2Form** (Onomasiologia): assegnazione di concetti da definizioni lessicali;
- **Defs**: calcolo della similarità tra definizioni e misure di specificità/concretezza.

### 🔹 2. FCA per Ontology Learning
Utilizzo dell’**Analisi dei Concetti Formali (Formal Concept Analysis)** per costruire automaticamente una tassonomia a partire da dati non strutturati (corpus testuale). L’algoritmo elabora frasi tramite parsing dipendente (Spacy), costruisce matrici di adiacenza e genera concetti latenti visualizzabili in forma di lattice.

### 🔹 3. Plagiarism Detection Code
Sviluppo di un algoritmo per la **rilevazione automatica del plagio** tra due script Python:
- Estrazione di caratteristiche lessicali, strutturali e commenti;
- Costruzione di vettori TF;
- Calcolo di **cosine similarity** e **Longest Common Subsequence (LCS)**;
- Combinate per ottenere uno score finale che classifica i casi in: *Plagio Forte*, *Plagio Debole* o *Plagio Assente*.
