from PipelineInput import PipelineInput
from rules.base_rule import BaseRule


class OddQuotesRule(BaseRule):
    def fix_translation(self, original: str, translated: str) -> str:
        return translated

    def is_broken(self, original: str, translated: str) -> bool:
        single_quotes_translated = translated.count("'")

        if single_quotes_translated % 2 == 1:
            return True

    def get_error_message(self, pipeline_input: PipelineInput) -> str:
        return self.generate_base_error_message("Odd number of single quotes", pipeline_input)
