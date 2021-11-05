import re

PATH_test = ["jpco_1_1_011001.txt", "jpco_1_1_015001.txt", "jpco_1_1_015003.txt", "jpco_1_1_015004.txt",
             "jpco_1_1_015007.txt", "jpco_1_1_015008.txt", "jpco_1_1_015009.txt", "jpco_1_2_021001.txt",
             "jpco_1_2_021002.txt", "jpco_1_2_025001.txt"]

PATH_validation = ["jpco_2_1_015006.txt", "jpco_2_1_015007.txt", "jpco_2_1_015008.txt", "jpco_2_1_015009.txt",
                   "jpco_2_1_015010.txt", "jpco_2_1_015011.txt", "jpco_2_1_015012.txt", "jpco_2_1_015013.txt",
                   "jpco_2_1_015014.txt", "jpco_2_1_015015.txt", "jpco_2_1_015016.txt", "jpco_2_1_015017.txt"]


def evaluation(PATH, directory, directory_key, path_result):
    result = ""         # Chaine qui contenir les résultats
    for url in PATH:    # Pour chaque modèle obtenu
        with open(directory + url, "r", encoding="utf-8") as f:
            n_grammes = f.readlines()[0].split(";")   # Keywords best_n_grammes

            def calculate_precision():
                with open(directory_key + "key_" + url, "r", encoding="utf-8") as file:
                    keys = re.split(r'; ', "".join(file.readlines()))   # Keywords du corpus
                    i = 0
                    for n_gramme in n_grammes:  # Je teste si l'algorithme le modèle le keywords
                        for keyword in keys:
                            if n_gramme in keyword:
                                i += 1

                    return url + " : " + str(i / len(keys)) + "\n"

            result += calculate_precision()

    with open(path_result, "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == '__main__':
    evaluation(PATH_test, "best_n_grammes_test/","../data_test_filter/", "result_test_best_n_grammes.txt")  # Test
    evaluation(PATH_validation, "best_n_grammes_validation/","../data_validation_filter/", "result_validation_best_n_grammes.txt")  # Validation
