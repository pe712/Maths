from pathlib import Path

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
            "./latex_styles/remarque.png"
        ]
    }
}

content_cours = {
    "Seconde":{
        "Ensemble de nombres" : [
            "./Seconde/C1 Ensembles de nombres/Seconde_Nombres.pdf"
        ],
        "Etude des variations d'une fonction" : [
            "./Seconde/C8 Etude des variations d'une fonction/Seconde_Variations.pdf"
        ],
        "Fonctions de référence" : [
            "./Seconde/C9 Fonctions de référence/Seconde_Fonctions_reference.pdf"
        ],
    }
}

def produce_content():
    with open("./content.html", "w", encoding='utf-8') as file:
        for h1, v1 in direct_content.items():
            file.write(f"<h1>{h1}</h1>\n")
            for h2, v2 in v1.items():
                file.write(f"<h2>{h2}</h2>\n")
                for source_str in v2:
                    source = Path(source_str)
                    file.write(
                        f'<a href="{source_str}" download>{source.name}</a><br>\n'
                    )

        for h1, v1 in content_cours.items():
            file.write(f"<h1>{h1}</h1>\n")
            for chapnumber, (h2, v2) in enumerate(v1.items()):
                file.write(f"<h2>Chapitre {chapnumber+1}: {h2}</h2>\n")
                for source_str in v2:
                    source = Path(source_str)
                    file.write(
                        f'<a href="{source_str}" download>{source.name}</a>\n'
                    )
                    tex_source_str = source_str.replace(source.suffix, ".tex")
                    file.write(
                        f'<a href="{tex_source_str}" download>source</a><br>\n'
                    )
    
if __name__ == "__main__":
    produce_content()