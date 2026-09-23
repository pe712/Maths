from pathlib import Path
import re
import os

header  = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Maths lycée - PE BAVIERE </title>
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
            "./Latex/latex_styles_12_09_2026.zip",
        ]
    }
}

GRADE = "Seconde"
path = f"./{GRADE}"

class Chapter:
    GRADE_PATTERN = fr"^{GRADE}_.+\.pdf"
    CHAPTER_FOLDER_PATTERN = r"^C(\d+) (.+)$"

    def __init__(self, path, folder_name):
        match = re.search(self.CHAPTER_FOLDER_PATTERN, folder_name)
        if match:
            self.chapnumber = int(match.group(1))
            self.chaptername = match.group(2)
            self.files =[]
            for filename in os.listdir(f"{path}/{folder_name}"):
                if re.search(self.GRADE_PATTERN, filename):
                    self.files.append(f"{path}/{folder_name}/{filename}")
        else:
            raise Exception(f"folder_name={folder_name} does not match the pattern={self.CHAPTER_FOLDER_PATTERN}")

    @classmethod
    def match(self, folder_name):
        return re.search(self.CHAPTER_FOLDER_PATTERN, folder_name)

def discover_courses():
    content_cours = []
    for folder_name in os.listdir(path):
        if Chapter.match(folder_name):
            chapter = Chapter(path, folder_name)
            content_cours.append(chapter)

    content_cours.sort(key=lambda chapter: chapter.chapnumber)
    return content_cours

def build_index():

    with open("./index.html", "w", encoding='utf-8') as file:
        file.write(header)

        for chaptername, chaptercontent in direct_content.items():
            file.write(f"<h1>{chaptername}</h1>\n")
            for subchaptername, files in chaptercontent.items():
                file.write(f"<h2>{subchaptername}</h2>\n")
                for source_str in files:
                    source = Path(source_str)
                    file.write(
                        f'<a href="{source_str}" download>{source.name}</a><br>\n'
                    )

        content_cours = discover_courses()
        file.write(f"<h1>{GRADE}</h1>\n")
        for chapter in content_cours:
            file.write(f"<h2>Chapitre {chapter.chapnumber}: {chapter.chaptername}</h2>\n")
            for source_str in chapter.files:
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