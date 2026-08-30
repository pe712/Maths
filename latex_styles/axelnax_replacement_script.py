import re
import os
import sys

def strip(text):
    # remove \vspace{-5mm}
    text = re.sub(r"\\vspace\{-5mm\}", "", text)
    
    # Find the index of \chapter and \end{document}
    chapter_index = text.find(r"\chapter")
    end_document_index = text.find(r"\end{document}")
    # If \chapter and \end{document} are found, slice the content between them
    if chapter_index != -1 and end_document_index != -1:
        # Extract the content between \chapter and \end{document}, inclusive
        text = text[chapter_index:end_document_index + len(r"\end{document}")]
    else:
        print("No \\chapter or \\end{document} found in the input file")
        return
    
    text = re.sub(r"\\chapter\{.*?\}", "", text)  # Removes \chapter{...}
    text = re.sub(r"\\end{document}", "", text)  # Removes \chapter{...}
    return text.strip()
    
def replace_latex_content(file_path, output_path):
    # Define replacement patterns
    replacements = [
        (r"\\begin{dft}", r"\\begin{defi}{}{}"),
        (r"\\end{dft}", r"\\end{defi}"),
        (r"\\begin{rmq}", r"\\begin{rem}{}{}"),
        (r"\\end{rmq}", r"\\end{rem}"),
        (r"\\begin{ex}", r"\\begin{ex}{}{}"),
        (r"\\end{ex}", r"\\end{ex}"),
        (r"\\begin{demoe}", r"\\begin{deme}{}{}"),
        (r"\\end{demoe}", r"\\end{deme}"),
        (r"\\begin{demo}", r"\\begin{dem}{}{}"),
        (r"\\end{demo}", r"\\end{dem}"),
        (r"\\begin{prop}", r"\\begin{prop}{}{}"),
        (r"\\end{prop}", r"\\end{prop}"),  
        (r"\\begin{meth}", r"\\begin{methode}{}{}"),
        (r"\\end{meth}", r"\\end{methode}"),
        (r"\\begin{thm}", r"\\begin{thm}{}{}"),
        (r"\\end{thm}", r"\\end{thm}"),
        (r"\\item\[•\]", r"\\item "),
        (r"enumerate", r"itemize"),
        (r"\\Rep", r"\\oij"),
        (r"\\rep", r"\\oij"),
        (r"\\Intg", r"\\of"),
        (r"\\Intd", r"\\fo"),
        (r"\\Coor", r"\\coordvp"),
        (r"\\V", r"\\v"),
        (r"\\Syst", r"\\syst"),
        (r"\\euro", r"€"),
        (r"\\hfill$\\blacksquare$", r""),
        (r"\\hfill $\blacksquare$", r""),
    ]
 
    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Strip the content
    content = strip(content)

    # Apply replacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Write the modified content to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Replacements done! Output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
   
    input_tex_file = sys.argv[1]
    output_path = os.path.splitext(input_tex_file)[0] + "_stripped.tex"
    
    replace_latex_content(input_tex_file, output_path)
