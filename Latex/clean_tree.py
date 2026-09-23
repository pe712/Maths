from pathlib import Path

def clean_tmp_files():
    tmp_extensions = [
"aux",
"auxlock",
"pytxcode",
"md5",
"fdb_latexmk",
"fls",
"out",
"preamble",
"log",
"sol",
]
    for extension in tmp_extensions:
        pattern = f"*.{extension}"
        for p in Path(".").rglob(pattern):
            p.unlink()

if __name__ == "__main__":
    clean_tmp_files()
