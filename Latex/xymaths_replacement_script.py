import re
import os
import sys

def strip(text):
    # remove \vspace{-5mm}
    text = re.sub(r"\\vspace\{-5mm\}", "", text)
    
    # Find the index of \chapter and \end{document}
    chapter_index = text.find("\LARGE{\TITLE}")
    end_document_index = text.find("\end{document}")
    # If \TITLE and \end{document} are found, slice the content between them
    if chapter_index != -1 and end_document_index != -1:
        # Extract the content between \chapter and \end{document}, inclusive
        text = text[chapter_index:end_document_index + len(r"\end{document}")]
    else:
        print("No \TITLE or \end{document} found in the input file")
        return
    
    text = re.sub(r"\\LARGE{\\TITLE}}", "", text)
    text = re.sub(r"\\end{document}", "", text)
    return text.strip()


def replace_latex_content(file_path, output_path):
    # Define replacement patterns
    replacements = [
        (r"\\bgdef", r"\\begin{defi}{}{}"),
        (r"\\endef", r"\\end{defi}"),
        (r"\\bgex", r"\\begin{ex}{}{}"),
        (r"\\enex", r"\\end{ex}"),
        (r"\\bgmp", r"\\begin{minipage}"),
        (r"\\enmp", r"\\end{minipage}"),
        (r"\\bgen", r"\\begin{enumerate}"),
        (r"\\enen", r"\\end{enumerate}"),
        (r"\\bg{prop}", r"\\begin{prop}{}{}"),
        (r"a\)", r"label=\\alph*"),
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
