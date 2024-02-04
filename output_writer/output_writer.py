class OutputWriter:
    _file_path: str

    def __init__(self, file_path: str):
        self._file_path = file_path

    def write_to_line(self, content: str, line_num: int):
        with open(self._file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        if line_num < 0 or line_num >= len(lines):
            raise ValueError("Invalid line number")

        if 'msgstr' in lines[line_num - 1]:
            lines[line_num - 1] = f'msgstr "{content}"\n'

        else:
            lines[line_num - 1] = f'"{content}"\n'

        with open(self._file_path, 'w', encoding="utf-8") as file:
            file.writelines(lines)
