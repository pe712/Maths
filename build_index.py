from pathlib import Path
import re
import os

# content_cours = {
#     "Seconde":{
#         "Ensemble de nombres" : [
#             "./Seconde/C1 Ensembles de nombres/Seconde_Nombres.pdf"
#         ],
#         "Etude des variations d'une fonction" : [
#             "./Seconde/C8 Etude des variations d'une fonction/Seconde_Variations.pdf"
#         ],
#         "Fonctions de référence" : [
#             "./Seconde/C9 Fonctions de référence/Seconde_Fonctions_reference.pdf"
#         ],
#     }
# }

header  = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>My test page</title>
  </head>
  <body>
"""

footer = """
  </body>
</html>
"""

direct_content= {
    "Latex" : {
        "Styles" : [
            "./latex_styles/commandes.tex",
            "./latex_styles/environnements.tex",
            "./latex_styles/layout_cours.sty",
            "./latex_styles/packages.tex",
            "./latex_styles/layout_algo.sty"
        ],
        "Icones" : [
            "./latex_styles/icons/ampoule.png",
            "./latex_styles/icons/calc.png",
            "./latex_styles/icons/demo.png",
            "./latex_styles/icons/fond_ecran_original.jpg",
            "./latex_styles/icons/ic_ampoule.png",
            "./latex_styles/icons/image_page_de_garde.jpg",
            "./latex_styles/icons/lever_la_main.png",
            "./latex_styles/icons/livre.png",
            "./latex_styles/icons/nocalc.png",
            "./latex_styles/icons/quote-mark-left.jpg",
            "./latex_styles/icons/quote-mark-right.jpg",
            "./latex_styles/icons/remarque.png"
        ]
    }
}

grade = "Seconde"
def discover_courses():
    content_cours = []
    path = f"./{grade}"
    grade_pattern = fr"^{grade}_.+\.pdf"
    chapter_pattern = r"^C\d+ .+$"
    strict_chapter_pattern = r"C\d+ "

    for folder in sorted(os.listdir(path)):
        if re.search(chapter_pattern, folder):
            chaptername = re.sub(strict_chapter_pattern, '', folder)
            files = []
            for filename in os.listdir(f"{path}/{folder}"):
                if re.search(grade_pattern, filename):
                    files.append(f"{path}/{folder}/{filename}")
            chapter = [chaptername, files]
            content_cours.append(chapter)
    return content_cours

def build_index():
    content_cours = discover_courses()
    
    with open("./index.html", "w", encoding='utf-8') as file:
        file.write(header)

        for h1, v1 in direct_content.items():
            file.write(f"<h1>{h1}</h1>\n")
            for h2, v2 in v1.items():
                file.write(f"<h2>{h2}</h2>\n")
                for source_str in v2:
                    source = Path(source_str)
                    file.write(
                        f'<a href="{source_str}" download>{source.name}</a><br>\n'
                    )

        file.write(f"<h1>{grade}</h1>\n")
        for chapnumber, (chaptitle, courses) in enumerate(content_cours):
            file.write(f"<h2>Chapitre {chapnumber+1}: {chaptitle}</h2>\n")
            for source_str in courses:
                source = Path(source_str)
                file.write(
                    f'<a href="{source_str}" download>{source.name}</a>\n'
                )
                tex_source_str = source_str.replace(source.suffix, ".tex")
                file.write(
                    f'<a href="{tex_source_str}" download>source</a><br>\n'
                )

        file.write(footer)

if __name__ == "__main__":
    build_index()