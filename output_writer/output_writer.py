class OutputWriter:
    _file_path: str

    def __init__(self, file_path):
        self._file_path = file_path

    def write_to_line(self, content: str, line_num: int):
        # logic to write to line
        pass