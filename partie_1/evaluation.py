import re
from partie_1.RAKE import rake

PATH_test = ["jpco_1_1_011001.txt", "jpco_1_1_015001.txt", "jpco_1_1_015003.txt", "jpco_1_1_015004.txt",
             "jpco_1_1_015007.txt", "jpco_1_1_015008.txt", "jpco_1_1_015009.txt", "jpco_1_2_021001.txt",
             "jpco_1_2_021002.txt", "jpco_1_2_025001.txt"]

PATH_validation = ["jpco_2_1_015006.txt", "jpco_2_1_015007.txt", "jpco_2_1_015008.txt", "jpco_2_1_015009.txt",
                   "jpco_2_1_015010.txt", "jpco_2_1_015011.txt", "jpco_2_1_015012.txt", "jpco_2_1_015013.txt",
                   "jpco_2_1_015014.txt", "jpco_2_1_015015.txt", "jpco_2_1_015016.txt", "jpco_2_1_015017.txt"]


def evaluation(PATH, directory, path_result):
    """
    -   Filtrer la liste des stopwords a fin d'enlever les phrases avec des #
    """
    with open("../fonctionnels_en.txt", "r", encoding="utf-8") as f:
        s = "".join(re.split(r'#.*\n', "".join(f.readlines())))

        with open("../fonctionnels_en_filter.txt", "w", encoding="utf-8") as file:
            file.write(s)

    algo = rake.Rake("../fonctionnels_en_filter.txt")  # Faire appel à la class
    result = ""         # Chaine qui contenir les résultats
    for url in PATH:    # Pour chaque corpus
        with open(directory + url, "r", encoding="utf-8") as f:
            # J'utilise l'algorithme et je converti les résultats en un dictionnaire
            keywords = dict(algo.run("".join(f.readlines())))

            def calculate_precision():
                with open(directory + "key_" + url, "r", encoding="utf-8") as file:
                    i = 0
                    keys = re.split(r'; ', "".join(file.readlines()))
                    for key in keys:  # Je teste si l'algorithme à généré les keywords
                        if key in keywords:
                            i += 1

                    return url + " : " + str(i / len(keys)) + "\n"

            result += calculate_precision()

    with open(path_result, "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == '__main__':
    evaluation(PATH_test, "../data_test_filter/", "result_test_rake.txt")  # Test
    evaluation(PATH_validation, "../data_validation_filter/", "result_validation_rake.txt")  # Validation
