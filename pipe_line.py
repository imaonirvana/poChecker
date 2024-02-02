from error_writer import ErrorWriter
from pipeline_error_writter import PipelineErrorWriter
from rules.double_quotes_rule.double_quotes_rule import DoubleQuotesRule
from rules.round_brackets_rule.round_brackets_rule import RoundBracketsRule
from rules.capitalization_rule.capitalization_rule import CapitalizationRule
from rules.base_rule import BaseRule
from rules.single_quotes_rule.single_quotes_rule import SingleQuotesRule
from rules.tilde_rule.tilde_rule import TildeRule


class Pipeline:
    main_steps: list[BaseRule] = [
        RoundBracketsRule(),
        CapitalizationRule(),
        DoubleQuotesRule(),
        SingleQuotesRule(),
        TildeRule(),
    ]
    error_writer: PipelineErrorWriter

    def __init__(self, file_path, line_num):
        self.error_writer = error_writer
        self.file_path = file_path
        self.line_num = line_num

    def process_translation(self, original: str, translated: str) -> str:
        result = translated

        for step in self.main_steps:
            if not step.is_broken(original, result):
                continue

            result = step.fix_translation(original, translated)
            error_message = step.get_error_message(original, translated, self.file_path, self.line_num)

            ErrorWriter.write_error(self.file_path, self.line_num, error_message)


        return result

    pass

    def is_broken(self, original: str, translated: str):
        for step in self.main_steps:
            if step.is_broken(original, translated):
                return True

        return False
