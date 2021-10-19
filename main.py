import glob
import re
from rake_nltk import Rake
import nltk

#nltk.download('stopwords')
#nltk.download('punkt')

def deleteMathKeyWords(pathToOutputDir):
    s = ""
    with open(pathToOutputDir, "r", encoding="utf-8") as f:
        s = "".join(re.split(r'keywords.*\n|', "".join(f.readlines()).lower()))

        while "<mml:" in s:
            s = s[:s.index("<mml:")] + s[s.index("</math>") + len("</math>"):]

        while "< tex-math >" in s:
            s = s[:s.index("< tex-math >")] + s[s.index("< /tex-math >") + len("< /tex-math >"):]

        s = ' '.join(re.findall(r'\n|[a-zA-Z]*', s))
        s = ''.join(re.split(r' \w{1,2} ', s))
        s = re.sub(r" {2,}", " ", s)

    pathToOutputDir = pathToOutputDir.split("/")
    f = open("resulsWalid/result_" + pathToOutputDir[1], "w")
    f.write(s)
    f.close()



def SplitFile(pathToOutputDir):

    title, acronyms , abstract, section = "", "", "", ""
    isTitle, isAcronyms , isAbstract, isSection = False, False, False, False

    with open(pathToOutputDir, "r") as file:

        for line in file:

            # Title part
            if "title" in line or "TITLE" in line:
                isTitle, isAcronyms , isAbstract, isSection = True, False, False, False

            # Acronyme part
            if "acronyms" in line or "ACRONYMS" in line:
                isTitle, isAcronyms , isAbstract, isSection = False, True, False, False

            # Abstract part
            if "abstract" in line or "ABSTRACT" in line:
                isTitle, isAcronyms , isAbstract, isSection = False, False, True, False
                line = line.lower()
                line = line.lstrip("abstract")

            # Section part
            if "__section__" in line or "__SECTION__" in line:
                isTitle, isAcronyms , isAbstract, isSection = False, False, False, True
                line = line.lower()
                line = line.lstrip("__section__")

            # line = line.replace("-\n", "")
            # line = line.replace("-\r", "")
            # line = line.replace("\n", " ")
            # line = line.replace("\r", " ")

            if isTitle:  # Is title
                line = line.lower()
                line = line.split("\t")
                # line = line.lstrip("abstract\t")
                title += line[1]

            if isAcronyms:  # Is acronyme
                line = line.lower()
                line = line.split("\t")
                # line = line.lstrip("abstract\t")
                acronyms += line[1]

            if isAbstract:  # Is abstract
                line = line.lower()
                abstract += line

            if isSection:  # Is section
                line = line.lower()
                section += line

    allText = title + acronyms + abstract + section

    pathToOutputDir = pathToOutputDir.split("/")
    f = open("results/result_" + pathToOutputDir[1], "w")
    f.write(allText)
    f.close()
    return allText

if __name__ == '__main__':

    files = glob.glob("data/*.txt")
    for f_path in files:
        SplitFile(f_path)

    files = glob.glob("results/*.txt")
    for f_path in files:
        deleteMathKeyWords(f_path)








