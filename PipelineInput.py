class PipelineInput:
    def __init__(self,  original: str, translated: str, file_path: str, line_num: int):
        self.__original = original
        self.__translated = translated
        self.__file_path = file_path
        self.__line_num = line_num

    def get_original(self):
        return self.__original

    def get_translated(self):
        return self.__translated

    def get_file_path(self) -> str:
        return self.__file_path

    def get_line_num(self):
        return  self.__line_num