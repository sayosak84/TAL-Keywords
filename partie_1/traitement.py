import re

PATH_test = ["jpco_1_1_011001.txt", "jpco_1_1_015001.txt", "jpco_1_1_015003.txt", "jpco_1_1_015004.txt",
             "jpco_1_1_015007.txt", "jpco_1_1_015008.txt", "jpco_1_1_015009.txt", "jpco_1_2_021001.txt",
             "jpco_1_2_021002.txt", "jpco_1_2_025001.txt"]

PATH_validation = ["jpco_2_1_015006.txt", "jpco_2_1_015007.txt", "jpco_2_1_015008.txt", "jpco_2_1_015009.txt",
                   "jpco_2_1_015010.txt", "jpco_2_1_015011.txt", "jpco_2_1_015012.txt", "jpco_2_1_015013.txt",
                   "jpco_2_1_015014.txt", "jpco_2_1_015015.txt", "jpco_2_1_015016.txt", "jpco_2_1_015017.txt"]


def treatment(PATH, directory_corpus, directory_filter):
    for url in PATH:
        with open(directory_corpus + url, "r", encoding="utf-8") as f:
            text = "".join(f.readlines()).lower()  # Extraction du text

            with open(directory_filter + "key_" + url, "w",
                      encoding="utf-8") as file:  # Extraction des clé de chaque text
                file.write("".join("".join(re.split(r'keywords\t |\n', "".join(re.findall(r'keywords.*\n', text))))))

            """
            -   Dans un premier temps nous filtrons le corpus en supprimant le type, la date, adress, le journal, 
                doi,..., ainsi que les mots clés tels que title, abstract et __section__.
            -   Nous modifions tout les minisule en majuscule.
            """
            s = "".join(re.split(r'type.*\n|'
                                 r'date.*\n|'
                                 r'address.*\n|'
                                 r'journal.*\n|'
                                 r'doi.*\n|'
                                 r'author.*\n|'
                                 r'acronyms.*\n|'
                                 r'keywords.*\n|'
                                 r'__section__\s|'
                                 r'abstract\t|'
                                 r'title\t|', text))

            """
            -   Dans un second temps, nous supprimons toutes les formules et les balises incluses entre 
                <mml:*(n'importe)>*</math> à partir du premier <mml:*> trouvé, puis entre 
                < tex-math >*< /tex-math > à partir du premier < tex-math > trouvé 
            """
            while "<mml:" in s:
                s = s[:s.index("<mml:")] + s[s.index("</math>") + len("</math>"):]

            while "< tex-math >" in s:
                s = s[:s.index("< tex-math >")] + s[s.index("< /tex-math >") + len("< /tex-math >"):]

            """
            -   Dans un troisième temps nous assurons de garder que des mots alphabétiques en supprimant les numéros et les caractères spéciaux.
            """
            s = ' '.join(list(filter(('').__ne__, re.findall(r'[a-zA-Z]*', s))))

            """
            -   Puis nous supprimons les uns-grammes.
            """
            #s = ''.join(list(filter((' ').__ne__, re.split(r'\b[a-zA-Z]\b', s))))

            """
            -   Et en fin nous filtrons les espaces supplémentaires ajoutés lors du pré-traitement
            """
            #s = ' '.join(re.split(r'  ', s))

            with open(directory_filter + url, "w", encoding="utf-8") as file_2:
                file_2.write(s)  # Créer un fichier du corpus pré-traité


if __name__ == '__main__':
    treatment(PATH_test, "../10_JPCO/", "../data_test_filter/")  # Test
    treatment(PATH_validation, "../12_TEST_JPCO/", "../data_validation_filter/")  # Validation
