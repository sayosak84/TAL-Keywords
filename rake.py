# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
# Automatic keyword extraction from indi-vidual documents.
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re
import operator

debug = False
test = True


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path):
        self.stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stop_words_path)

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords


if test:
    text = '''  superconductivity two dimensional repulsive rashba gas low electron density 
 total density states dos renormalization group time reversal symmetry trs 
 superconductivity low density rashba gas renormalization group collective modes majorana zero modes repulsive interaction 
 study the superconducting instability and the resulting superconducting states two dimensional repulsive fermi gas with rashba spin orbit coupling low electron density namely the fermi energy lower than the energy the dirac point induced rashba coupling 
 find that superconductivity enhanced the dimensionless fermi energy decreases due two reasons 
 first the density states increases 
 second the particle hole bubble becomes more anisotropic resulting increasing effective attraction 
 the superconducting state always the total angular momentum channel with chern number breaking time reversal symmetry spontaneously 
 although putative leggett mode expected due the two gap nature the superconductivity find that always damped 
 more importantly once sufficiently large zeeman coupling applied the superconducting state the chern number can tuned and majorana zero modes exist the vortex cores 
 despite effect originating from relativity spin orbit coupling soc has found its way into nonrelativistic physics 
 condensed matter physics novel systems with soc playing significant role are found recently such topological insulators two dimensional rashba gases interfaces oxides weyl semimetals and soc induced mott insulators and other states series while ultracold quantum gases although atoms are neutral synthetic soc can generated atom light interaction see for review 
 turning superconductivity non centrosymmetric superconductors where soc mixes spin singlet and triplet pairings have been extensively studied and superconductivity related soc was observed oxide interfaces 
 here study repulsive gas with rashba soc low density 
 the single particle hamiltonian and where the effective mass characterizes the strength rashba soc and components are pauli matrices and the direction normal the system 
 unitary transformation helicity basis one finds the dispersion where the helicity and the rashba momentum 
 have shifted the energy which will compensated the shift the fermi energy 
 the spin degeneracy lifted resulting two bands touching dirac point 
 this system the competition between the three energy scales the fermi energy coulomb repulsion and the rashba energy determines the system phases 
 define the dimensionless fermi energy 
 low density refer the regime shown figure 
 while the low density limit the fermi energy much smaller than coulomb interaction and soc energy and wigner crystalline phases are found focus the weak coupling limit tot although tot discussed below where the short range repulsion and ntot the total density states dos fermi energy 
 investigate the instability the system superconducting states 
 earlier papers the high density case with was studied 
 was found that decreases from large value general superconductivity enhanced and the total angular momentum channel which cooper pairs condense decreases from large value arithmetic sequence with step 
 finally becomes 
 the superconductivity predominantly resides the outer fermi surface and interband coupling induces small gap the inner fermi surface 
 the superconducting state breaks time reversal symmetry trs and both fermi surfaces are fully gapped 
 figure the dispersion relation fixing with the helicity labeled 
 low density the fermi level indicated the dashed line below the dirac point energy the two fermi surfaces the annulus between which filled electrons with helicity 
 the black arrows represent the direction the spins around the fermi surfaces 
 topological change the fermi surface occurs below which the low density regime are interested 
 shown figure there electron like and hole like fermi surface between which the annulus filled electrons 
 the fermi wave vectors rescaled are where corresponding the outer and inner fermi surface respectively 
 note that the two fermi surfaces have the same helicity 
 the dos the fermi surface where 
 likely that superconductivity further enhanced since the total dos increases with decreasing tot 
 addition wonder what topological change the fermi surfaces may bring about the dielectric functions which can give rise the attraction nonzero channels 
 the enhancement conventional superconductivity attractive rashba gases low density has been studied while here address the problem with repulsion which leads unconventional superconductivity 
 following the renormalization group approach developed find that low density the superconducting instability always occurs channel and the critical temperature increases with decreasing 
 the increasing could many orders magnitude although the resulting still quite low due the weak coupling nature our formalism 
 recent theme condensed matter physics search for majorana fermions various systems 
 addition intrinsic chiral wave superconductors spin orbit coupled systems such topological insulators semiconductors with zeeman splitting proximity wave superconductors and hole doped semiconductors also support majorana fermion modes the vortex cores 
 show that the intrinsic superconducting state have found can also host majorana fermions once sufficiently large zeeman field applied and the topological phase diagram derived 
 also study the collective modes the superconducting state 
 due the two gap nature addition the usual bogoliubov anderson goldstone bag mode which pushed plasma energy collective mode corresponding the oscillation the phase difference the two gaps the leggett mode could also exist 
 however the values the interband and intraband couplings the whole parameter regime not support undamped leggett mode 
 methods 
 perturbative expansion and approach 
 study the system with onsite repulsive interactions the interacting hamiltonian which where positive 
 the interacting hamiltonian the helicity basis reads where the annihilation operator the helicity basis and the angle 
 following the weak coupling approach developed and integrating out high energy modes from the bandwidth low energy cutoff derive the effective action for the low energy modes where kbt and and sup sup are grassmann numbers 
 have focused the cooper channel the couplings which are the only marginally relevant ones and decomposed the couplings into angular momentum channels where 
 since channel dominates one cannot get attractive interactions 
 therefore higher orders and look for nonvanishing terms higher angular momentum channels 
 second order have particle hole bubble and particle particle bubble the latter which only has component 
 the correction from the particle hole bubble shown figure where the dielectric function where since cooper pairs are expected form between electrons near the fermi surfaces and are restricted fermi surface and respectively 
 straightforward calculations show that can written the form where cos real function that depends the dimensionless fermi energy but not and independently 
 then the renormalized coupling appearing equation reads where the fourier component cos cos cos 
 the functions cos are plotted figure 
 and connect with the same functions calculated but changes sign due the change the helicity the inner fermi surface 
 clearly the functions depend more strongly smaller 
 the fourth order there only one term that satisfies two conditions being finite nonzero angular momentum channel and having logarithmic divergence which may give rise instability 
 this term shown figure 
 including the renormalized couplings become defining the dimensionless bare coupling and the dimensionless renormalized coupling find the flow equation where the matrix multiplication and the bare couplings have been replaced the renormalized couplings 
 the solution with the initial condition the scale the superconducting transition temperature given the largest energy which the renormalized coupling diverges where chosen such way that given the most negative among all the 
 find that long although increases general with when 
 the intraband and intraband couplings are shown figure 
 the effective coupling plotted figures and units and ntot respectively 
 results 
 effective couplings and critical temperature 
 the critical temperature given where the bandwidth and the effective coupling channel given where and are the intraband couplings the outer and inner bands respectively and the interband coupling 
 they are shown figure channel 
 can seen and are negligible above and superconductivity predominantly resides the outer fermi surface and the inner fermi surface participates only quite low density 
 the effective coupling plotted figures and units and ntot respectively 
 although seems can acquire any large value from figure our weak coupling approach the result not justified for untot and see from figure that the effective coupling still restricted small the justifiable parameter regime 
 however can increase many orders magnitude decreases 
 fixed superconductor insulator transition expected the density the gas decreases since wigner crystal state should exist strong coupling but are not concerned with this case 
 topological phase diagram with zeeman field 
 discussed the ground state breaks trs spontaneously and the system goes either superconducting state both which have the same energy 
 due soc the paring term the hamiltonian has both triplet and singlet part which reads where and are the triplet and singlet pairing strength respectively and the angle between and axis 
 search for majorana fermions instead solving the bogoliubov gennes equations the presence vortices apply index theorem proved that superconductors with odd chern number can support majorana zero modes 
 the chern number this state has been shown and 
 have odd apply zeeman field which couples the system since now the hamiltonian breaks trs the two states with have different energies 
 pointed the system favors state and favors state 
 these two cases are related time reversal operation just consider the former case 
 calculate the chern number and find three topological phases depending the position fermi level and shown figure 
 the topological phase diagram can explained follows 
 when the dirac point gapped and chern number well defined for each band the superconducting state 
 due the winding spin around the band with helicity carries chern number 
 addition the phase winding the order parameter superimposes the chern number each band 
 therefore the inner and outer band carry chern number and respectively 
 when the fermi level crosses both bands and the chern number the sum the two 
 when the fermi level either crosses the outer band twice which case the electron pocket and hole pocket contribute opposite chern number thus does not cross any band and hence 
 between these two parameter regimes when the fermi level only crosses the outer band and then 
 this case according the index theorem mentioned above majorana zero modes exist the edge and the vortex cores 
 low density only the left part the phase diagram figure available 
 collective modes 
 collective modes superconductors were first studied bogoliubov and anderson 
 they found goldstone mode accompanying the spontaneous breaking gauge symmetry neutral system which corresponds the phase oscillations the superconducting order parameter 
 charged system this called bag mode pushed the plasma frequency 
 two band superconductors leggett predicted another collective mode corresponding the oscillations the relative phase the two superconducting condensates 
 the superconducting state derived above due the two gap nature addition bag mode leggett mode also expected exist 
 the detailed calculations are carried out the supplemental material 
 effectively channel have two band superconductor 
 actually the bare interaction were attractive superconductivity would occur channel and the superconducting state would also have two band nature 
 thus our approach also applies that case 
 find both bag and leggett modes while the former pushed plasma energy the latter has dispersion where the above are the dos and where the total particle number band and labels the outer and inner band 
 note that the second term equation does not appear two band wave superconductor 
 order for leggett mode exist necessary for positive hence 
 however the whole parameter regime shown figure does not satisfy this condition thus this mode must damped our model 
 but other soc superconductors leggett mode could exist 
 discussion and conclusion 
 looking for various ways increase the critical temperature superconductors important direction condensed matter physics 
 showed that increasing rashba soc decreasing the fermi energy can strongly enhance superconductivity repulsive fermi gas the low density regime 
 shown figure assume fixed the effective attraction can increased ten times decreasing resulting much higher than that the high density regime 
 although such superconductivity still too weak observe our weak coupling approach wonder soc helps strongly correlated systems which worthy further study 
 real materials the underlying lattice will affect the model several aspects 
 the dos suppressed although increasing with lowering will not diverge 
 the particle hole bubble will also affected 
 due these two consequences the behavior will modified but the trend that increases with lowering will probably remain the same 
 moreover the spontaneous trs breaking state may not stable unless the two pairing components the state and order parameter belong the same irreducible representation the point group which can satisfied the lattice has threefold rotational symmetry 
 conclusion have investigated the superconducting instability rashba gas with repulsive interaction low density the weak coupling limit 
 the density decreases the superconducting transition temperature increases significantly 
 the superconducting state always channel 
 when zeeman field applied the state can have odd chern number and hence majorana zero modes are supported 
 although leggett mode does not exist due the specific parameters expect appear other spin orbit coupled superconductors because the two gap nature   '''
    # Split text into sentences
    sentenceList = split_sentences(text)
    #stoppath = "FoxStoplist.txt" #Fox stoplist contains "numbers", so it will not find "natural numbers" like in Table 1.1
    stoppath = "SmartStoplist.txt"  #SMART stoplist misses some of the lower-scoring keywords in Figure 1.5, which means that the top 1/3 cuts off one of the 4.0 score words in Table 1.1
    stopwordpattern = build_stop_word_regex(stoppath)

    # generate candidate keywords
    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

    # calculate individual word scores
    wordscores = calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    if debug: print(keywordcandidates)

    sortedKeywords = sorted(keywordcandidates.items(), key=operator.itemgetter(1), reverse=True)
    if debug: print(sortedKeywords)

    totalKeywords = len(sortedKeywords)
    if debug: print(totalKeywords)
    print(sortedKeywords[0:(totalKeywords//3)])

    sortedwWords= sorted(wordscores.items(), key=operator.itemgetter(1), reverse=True)

    rake = Rake("SmartStoplist.txt")
    keywords = rake.run(text)
    print(keywords)

    print ("##############################")

    for score , word in sortedwWords:
        print (score, " : " , word)