from pathlib import Path

file_path = Path(__file__).parent.parent / 'assets'

def read_txt(file_name: str) -> str:
    with open(file_path / file_name) as file:
        return file.read()