import re
import os
from pathlib import Path

texfile_preamble = """
\\documentclass[10pt,a4paper,openany,twoside]{book}

\\usepackage{layout_cours}

\\begin{document}

"""

texfile_endamble = """
\end{document}
"""

# To modify if the script is moved
root = Path(__file__).parent.parent

class Exo:
    BOOK_PREFIX = "Bordas_Indice_2nde_2019"
    BOOK_PATH = "Seconde/Bordas_Indice_2nde_2019"

    def __init__(self, pagenumber, required_exonumber, book_prefix=BOOK_PREFIX):
        self.required_exonumber = required_exonumber
        self.pagenumber = pagenumber
        self.__book_prefix = book_prefix
        self.__book_path =  root / Exo.BOOK_PATH


        pattern = "^" + book_prefix+"_p_"+str(self.pagenumber)+"_exo_" + ".*" + str(required_exonumber) + ".*\.jpg$"
        self._file_path = None
        for filename in os.listdir(self.__book_path):
            if re.search(pattern, filename):
                self._file_path = filename
        if self._file_path is None:
            self._file_fullpath = "Exo not found : "+book_prefix+"_p_"+str(self.pagenumber)+"_exo_" + str(required_exonumber) + ".jpg"
        else:
            self.__extract_exonumbers()
            self.__resolve_file_fullpath()

    def __resolve_file_fullpath(self):
        self._file_fullpath = self.__book_path/self._file_path
        self._file_fullpath = self._file_fullpath.relative_to(root)
        self._file_fullpath = str(self._file_fullpath)
        self._file_fullpath = self._file_fullpath.replace("\\", "/")
        curdir = str(Path(os.curdir).absolute().relative_to(root))
        nb_parents = len(curdir.split("\\"))
        self._file_fullpath = "".join("../" for _ in range(nb_parents)) + self._file_fullpath

    def __extract_exonumbers(self):
        pattern_exonumber ="^" + self.__book_prefix+"_p_"+str(self.pagenumber)+r"_exo(.*)\.jpg"
        match = re.match(pattern_exonumber, self._file_path).group(1)
        self.exonumbers = re.findall(r"_(\d+)", match)
        self.exonumbers =  {int(exonum) for exonum in self.exonumbers}

    def __str__(self):
        return "\\includegraphics[width=0.5\\textwidth]{"+self._file_fullpath+"}\n\n"

def build_exercises_sheet(filename, filetitle, classname, section_title, exos:list):
    filename+=".tex"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(texfile_preamble)
        file.write("\\titre{"+filetitle+"}\n")
        file.write("\\classe{"+classname+"}\n")
        file.write("\\enteteperso\n\n")
        file.write("\\pagenumbering{Alph}\n")
        file.write("\\section*{"+section_title+"}\n")
        file.write("\\begin{exercicesnofoot}\n")
        for exo in exos:
            file.write("\\hspace{-1.5cm}\n")
            file.write(str(exo))
        file.write("\\end{exercicesnofoot}\n\n")
        file.write("\\newpage\n")
        file.write("\\pagenumbering{arabic}\n")
        file.write(texfile_endamble)

def filter(exos:list[Exo]):
    filtered_exos = []
    known_exercises = set()
    for exo in exos:
        if not exo.required_exonumber in known_exercises:
            filtered_exos.append(exo)
            known_exercises.update(exo.exonumbers)
    return filtered_exos

if __name__ == "__main__":
    filename = "Seconde_test"
    filetitle = "Equation de degré un et équation produit nul"
    classname = "Seconde"
    section_title = "Bordas 2019"
    exos = [Exo(104, 115), Exo(104, 119), Exo(104, 120), Exo(104, 121), Exo(104, 124), Exo(113, 197)]
    exos = filter(exos)
    build_exercises_sheet(filename, filetitle, classname, section_title, exos)