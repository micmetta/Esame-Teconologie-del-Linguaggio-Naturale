import csv
from scipy import stats


columns_names = True
lista_ris_original = []
lista_ris_new = []
with open('WordSim353.csv', 'r') as f:
    reader_original = csv.reader(f)
    #with open('Risultati Wu & Palmer.csv', 'r') as file:
    #with open('Leackock & Chodorow.csv', 'r') as file:
    with open('Risultati Shortest path.csv', 'r') as file:

        reader_new = csv.reader(file)

        for row in reader_original:
            if not columns_names:
                sim_original = float(row[2])
                lista_ris_original.append(sim_original)
            else:
                columns_names = False

        columns_names = True
        for row in reader_new:
            if not columns_names:
                sim_new = float(row[2])
                lista_ris_new.append(sim_new)
            else:
                columns_names = False

        print("lista_ris_original: ", lista_ris_original)
        print("")
        print("lista_ris_new: ", lista_ris_new)
        #A questo punto nelle due liste ho i vari valori di similarità dei due dataset e quindi posso calcolare il coeff. di Pearson:
        coeff_pearson = stats.spearmanr(lista_ris_original, lista_ris_new)

        print("coeff_pearson: ", coeff_pearson)