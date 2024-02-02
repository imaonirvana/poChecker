from error_writer import ErrorWriter


class PipelineErrorWriter:
    def __init__(self, file_path, line_num):
        self.file_path = file_path
        self.line_num = line_num

    def write_error(self, message: str):
        ErrorWriter.write_error(self.file_path, self.line_num, message)
