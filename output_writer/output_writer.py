class OutputWriter:
    _file_path: str

    def __init__(self, file_path):
        self._file_path = file_path

    def write_to_line(self, content: str, line_num: int):
        with open(self._file_path, 'r') as file:
            lines = file.readlines()

        if line_num < 1 or line_num > len(lines):
            raise ValueError("Invalid line number")

        lines[line_num + 1] = 'msgstr "' + content + '"' + '\n'

        with open(self._file_path, 'w') as file:
            file.writelines(lines)
        pass