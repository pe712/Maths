import re
import os
import json
from pathlib import Path

texfile_preamble = """
\\documentclass[10pt,a4paper,openany,twoside]{book}

\\usepackage{layout_cours}

\\begin{document}

"""

texfile_endamble = """
\\end{document}
"""

# To modify if the script is moved
root = Path(__file__).parent.parent.resolve()

class Exo:
    BOOK_PREFIX = "Bordas_Indice_2nde_2023"
    BOOK_PATH = "Seconde/Bordas_Indice_2nde_2023"
    # BOOK_PREFIX = "Bordas_Indice_Tle_Techno_2020"
    # BOOK_PATH = "Terminale/T STMG/Bordas_Indice_Tle_Techno_2020"

    def __init__(self, pagenumber, required_exonumber, book_prefix=BOOK_PREFIX):
        self.required_exonumber = required_exonumber
        self.pagenumber = pagenumber
        self.__book_prefix = book_prefix
        self.__book_path =  root / Exo.BOOK_PATH


        pattern = "^" + book_prefix+"_p_"+str(self.pagenumber)+"_exo_" + ".*" + str(required_exonumber) + ".*\\.jpg$"
        self._file_path = None
        for filename in os.listdir(self.__book_path):
            if re.search(pattern, filename):
                self._file_path = filename
        if self._file_path is None:
            self._file_fullpath = "Exo not found : "+book_prefix+"_p_"+str(self.pagenumber)+"_exo_" + str(required_exonumber) + ".jpg"
        else:
            self.__resolve_file_fullpath()
        self.__extract_exonumbers()

    def __resolve_file_fullpath(self):
        self._file_fullpath = self.__book_path/self._file_path
        self._file_fullpath = self._file_fullpath.relative_to(root)
        self._file_fullpath = str(self._file_fullpath)
        self._file_fullpath = self._file_fullpath.replace("\\", "/")
        curdir = str(Path(os.curdir).absolute().relative_to(root))
        curdir.replace("\\", "/")
        nb_parents = len(curdir.split("/"))
        self._file_fullpath = "".join("../" for _ in range(nb_parents)) + self._file_fullpath

    def __extract_exonumbers(self):
        self.exonumbers = set()
        if self._file_path:
            pattern_exonumber ="^" + self.__book_prefix+"_p_"+str(self.pagenumber)+"_exo(.*)\\.jpg"
            match = re.match(pattern_exonumber, self._file_path).group(1)
            self.exonumbers = re.findall(r"_(\d+)", match)
            self.exonumbers =  {int(exonum) for exonum in self.exonumbers}

    def __str__(self):
        return "\\includegraphics[width=0.5\\textwidth]{"+self._file_fullpath+"}\n\n"


class ExoSection:
    def __init__(self, exo_section_title=None):
        self.exo_section_title = exo_section_title
        self.exos = []
        self.page_numbers = set()

    def append(self, exo:Exo):
        self.exos.append(exo)
        self.page_numbers.add(exo.pagenumber)

    def filter(self):
        filtered_exos = []
        known_exercises = set()
        for exo in self.exos:
            if not exo.required_exonumber in known_exercises:
                filtered_exos.append(exo)
                known_exercises.update(exo.exonumbers)
        self.exos =  filtered_exos

    def __str__(self):
        _page_numbers = sorted(list(self.page_numbers))
        if len(_page_numbers)==0:
            print_pagenumbers = ""
        elif len(_page_numbers)==1:
            print_pagenumbers = f" [page {_page_numbers[0]}]"
        else:
            print_pagenumbers = f" [pages: {_page_numbers.pop(0)}"
            for pagenumber in _page_numbers:
                print_pagenumbers+=f", {pagenumber}"
            print_pagenumbers+="]"
        if self.exo_section_title is None:
            raise Exception("exo_section_title is empty")
        return "\sectionexo{"+self.exo_section_title+print_pagenumbers+"}\n"

class ExoPattern:
    pass

def build_exercises_sheet(filename, filetitle, classname, section_title, sections:list[ExoSection], twice=False):
    if twice: n=2
    else: n=1
    with open(filename, "w", encoding='utf-8') as file:
        file.write(texfile_preamble)
        file.write("\\titre{"+filetitle+"}\n")
        file.write("\\classe{"+classname+"}\n")
        for _ in range(n):
            file.write("\\setcounter{sectionexo}{0}\n")
            file.write("\\thispagestyle{premierepage}\n")
            file.write("\\entetecategory{Exercices}\n")
            file.write("\\enteteperso\n\n")
            file.write("\\pagenumbering{Alph}\n")
            file.write("\\section*{"+section_title+"}\n")
            file.write("\\begin{exercicesnofoot}\n")
            for section in sections:
                if section.exo_section_title is not None:
                    file.write(str(section))
                for exo in section.exos:
                    file.write("\\hspace{-1.1cm}\n")
                    file.write(str(exo))
            file.write("\\end{exercicesnofoot}\n\n")
            file.write("\\newpage\n")
            file.write("\\pagenumbering{arabic}\n")

        file.write(texfile_endamble)

def read_tex_exercises(filename):
    sections = []
    pattern_exo = r" *\\begin{bookexo}{(\d+) p\.(\d+)}\\end{bookexo}"
    pattern_double_exos = r" *\\begin{bookexos}{(\d+), *(\d+) p\.(\d+)*}\\end{bookexos}"
    pattern_multi_exos = r" *\\begin{bookexos}{(\d+)-(\d+) p\.(\d+)*}\\end{bookexos}"
    pattern_multi_exos2 = r" *\\begin{bookexos}{(\d+) à (\d+) p\.(\d+)*}\\end{bookexos}"
    pattern_section_exo = r" *\\sectionexo{(.+)}"
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            section_match = re.match(pattern_section_exo, line)
            if section_match:
                exo_section_title = section_match.group(1)
                sections.append(ExoSection(exo_section_title))
            if len(sections)==0:
                sections.append(ExoSection())
            current_section = sections[-1]
            exo_match = re.match(pattern_exo, line)
            double_exos_match =  re.match(pattern_double_exos, line)
            multi_exos_match =  re.match(pattern_multi_exos, line)
            multi_exos2_match =  re.match(pattern_multi_exos2, line)
            if exo_match:
                exonumber, pagenumber = exo_match.groups()
                current_section.append(Exo(pagenumber, exonumber))
            elif double_exos_match:
                exonumber1, exonumber2, pagenumber = double_exos_match.groups()
                for exonumber in [exonumber1, exonumber2]:
                    current_section.append(Exo(pagenumber, exonumber))
            elif multi_exos_match:
                first, last, pagenumber = multi_exos_match.groups()
                for exonumber in range(int(first), int(last)+1):
                    current_section.append(Exo(pagenumber, exonumber))
            elif multi_exos2_match:
                first, last, pagenumber = multi_exos2_match.groups()
                for exonumber in range(int(first), int(last)+1):
                    current_section.append(Exo(pagenumber, exonumber))
    return sections

def read_json_exercices(filename):
    sections = []
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        for exo_section_title, exos in data.items():
            section = ExoSection(exo_section_title)
            for exo in exos:
                section.append(Exo(exo[0], exo[1]))
            sections.append(section)
    return sections

def read_exercises(filename):
    extension = str(Path(filename).suffix)
    if extension == ".tex":
        return read_tex_exercises(filename)
    elif extension == ".json":
        return read_json_exercices(filename)
    else:
        raise Exception(f"Unrecognized extension : {extension}")

if __name__ == "__main__":
    output_filename = "Seconde_revisions.tex"
    filetitle = ""
    classname = "Seconde"
    # classname = "Terminale STMG"
    section_title = "Bordas 2023"
    # section_title = "Bordas 2020"
    twice=False
    input_filename = "exos.json"
    sections = read_exercises(input_filename)
    for section in sections:
        section.filter()
    build_exercises_sheet(output_filename, filetitle, classname, section_title, sections, twice=twice)