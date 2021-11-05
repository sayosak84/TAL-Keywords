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


def treatment(PATH, directory_corpus, directory_best_grammes):
    n_grammes_files = []

    for url in PATH:
        with open(directory_corpus + url, "r", encoding="utf-8") as f:
            text = "".join(f.readlines()).lower()  # Récupérer le text
            # sfdgrnh a fgh b cd kfrpkg
            def one_gramme():
                # Resortir les n-grammes dans une liste (ici 1-gramme)
                s = re.findall("\w{1}", "".join(re.findall(r" \w{1} ", text)))
                # Retourner un dictionnaire comme clé le n-gramme et valeur son occurence dans le text
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            def two_grammes():
                s = re.findall("\w{2}", "".join(re.findall(r" \w{2} ", text)))
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            def three_grammes():
                s = re.findall("\w{3}", "".join(re.findall(r" \w{3} ", text)))
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            def four_grammes():
                s = re.findall("\w{4}", "".join(re.findall(r" \w{4} ", text)))
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            def five_grammes():
                s = re.findall("\w{5}", "".join(re.findall(r" \w{5} ", text)))
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            def six_grammes():
                s = re.findall("\w{6}", "".join(re.findall(r" \w{6} ", text)))
                return dict(sorted(dict([(i, len(list(j))) for i, j in groupby(sorted(s))]).items(), key=lambda t: t[1],
                                   reverse=True)[:6])

            # Créer pour chaque fichier un fichier contenant les 5 ou 6 grammes les plus significatives
            with open(directory_best_grammes + url, "w", encoding="utf-8") as file:
                file.write(";".join(list(one_gramme().keys()) + list(two_grammes().keys()) +
                                    list(three_grammes().keys()) + list(four_grammes().keys()) +
                                    list(five_grammes().keys()) + list(six_grammes().keys())
                                    )
                           )

    return n_grammes_files


if __name__ == '__main__':
    treatment(PATH_test, "../data_test_filter/", "best_n_grammes_test/")                        # Test
    treatment(PATH_validation, "../data_validation_filter/", "best_n_grammes_validation/")      # Validation
