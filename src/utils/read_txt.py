def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()

    return file_contents