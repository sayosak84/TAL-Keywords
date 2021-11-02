import re
from itertools import groupby

"""- Ré-exécuter le fichier traitement de partie 1 en mettant en commentaire les lignes 57 et 62 (à fin de ne pas 
supprimer les uns-grammes) """

PATH_test = ["jpco_1_1_011001.txt", "jpco_1_1_015001.txt", "jpco_1_1_015003.txt", "jpco_1_1_015004.txt",
             "jpco_1_1_015007.txt", "jpco_1_1_015008.txt", "jpco_1_1_015009.txt", "jpco_1_2_021001.txt",
             "jpco_1_2_021002.txt", "jpco_1_2_025001.txt"]

PATH_validation = ["jpco_2_1_015006.txt", "jpco_2_1_015007.txt", "jpco_2_1_015008.txt", "jpco_2_1_015009.txt",
                   "jpco_2_1_015010.txt", "jpco_2_1_015011.txt", "jpco_2_1_015012.txt", "jpco_2_1_015013.txt",
                   "jpco_2_1_015014.txt", "jpco_2_1_015015.txt", "jpco_2_1_015016.txt", "jpco_2_1_015017.txt"]


def treatment(PATH, directory_corpus):
    n_grammes_files = []

    for url in PATH:
        with open(directory_corpus + url, "r", encoding="utf-8") as f:
            text = "".join(f.readlines()).lower()  # Récupérer le text

            def one_gramme():
                ml = {}
                s = re.findall("\w{1}", "".join(
                    re.findall(r" \w{1} ", text)))  # Resortir les n-grammes dans une liste (ici 1-gramme)
                return [{i: len(list(j))} for i, j in groupby(
                    sorted(s))]  # Retourner un dictionnaire comme clé le n-gramme et valeur son occurence dans le text

            def two_grammes():
                ml = {}
                s = re.findall("\w{2}", "".join(re.findall(r" \w{2} ", text)))
                return [{i: len(list(j))} for i, j in groupby(sorted(s))]

            def three_grammes():
                ml = {}
                s = re.findall("\w{3}", "".join(re.findall(r" \w{3} ", text)))
                return [{i: len(list(j))} for i, j in groupby(sorted(s))]

            def four_grammes():
                ml = {}
                s = re.findall("\w{4}", "".join(re.findall(r" \w{4} ", text)))
                return [{i: len(list(j))} for i, j in groupby(sorted(s))]

            def five_grammes():
                ml = {}
                s = re.findall("\w{5}", "".join(re.findall(r" \w{5} ", text)))
                return [{i: len(list(j))} for i, j in groupby(sorted(s))]

            def six_grammes():
                ml = {}
                s = re.findall("\w{6}", "".join(re.findall(r" \w{6} ", text)))
                return [{i: len(list(j))} for i, j in groupby(sorted(s))]

            n_grammes_files.append((one_gramme(), two_grammes(), three_grammes(), four_grammes(), five_grammes(),
                                    six_grammes()))

    return n_grammes_files


if __name__ == '__main__':
    print(treatment(PATH_test, "../data_test_filter/"))         # Test
    print(treatment(PATH_validation, "../data_validation_filter/"))   # Validation
