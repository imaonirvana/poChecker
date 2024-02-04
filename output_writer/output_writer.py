class OutputWriter:
    _file_path: str

    def __init__(self, file_path: str):
        self._file_path = file_path

    def write_to_line(self, content: str, line_num: int):
        lines = self.__read_file()

        if line_num < 0 or line_num >= len(lines):
            raise ValueError("Invalid line number")

        start, end = self.get_translated_text_range(lines, line_num)

        del lines[start:end + 1]
        lines.insert(start, self.escape_content_value(content))

        self.__write_file(lines)

    def get_translated_text_range(self, lines: list[str], line_num: int) -> (int, int):
        start = -1
        end = -1

        for i in range(line_num - 1, len(lines)):
            line = lines[i]

            if line.strip().startswith('msgstr'):
                start = i

            if line.strip() == "" and start != -1:
                end = i - 1
                break

        if start != -1 and end == -1:
            end = len(lines) - 1

        return start, end

        pass

    def escape_content_value(self, content: str) -> str:
        return f'msgstr "{content}"\n'

        pass

    def __read_file(self) -> list[str]:
        with open(self._file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        return lines

    def __write_file(self, lines: list[str]):
        with open(self._file_path, 'w', encoding="utf-8") as file:
            file.writelines(lines)
