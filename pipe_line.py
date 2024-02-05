from PipelineInput import PipelineInput
from error_writer import ErrorWriter
from rules.double_quotes_rule.double_quotes_rule import DoubleQuotesRule
from rules.odd_quotes_rule.odd_quotes_rule import OddQuotesRule
from rules.percent_rule.percent_rule import PercentRule
from rules.round_brackets_rule.round_brackets_rule import RoundBracketsRule
from rules.capitalization_rule.capitalization_rule import CapitalizationRule
from rules.base_rule import BaseRule
from rules.single_quotes_rule.single_quotes_rule import SingleQuotesRule
from rules.tilde_rule.tilde_rule import TildeRule


class Pipeline:
    main_steps: list[BaseRule] = [
        RoundBracketsRule(),
        PercentRule(),
        TildeRule(),
        DoubleQuotesRule(),
        SingleQuotesRule(),
        CapitalizationRule(),
        OddQuotesRule(),
    ]

    def process_translation(self, pipeline_input: PipelineInput) -> str:
        result = pipeline_input.get_translated()

        for step in self.main_steps:
            if not step.is_broken(pipeline_input.get_original(), result):
                continue

            result = step.fix_translation(pipeline_input.get_original(), result)
            error_message = step.get_error_message(pipeline_input)

            ErrorWriter.write_error(error_message)

        return result

    pass

    def is_broken(self, original: str, translated: str):
        for step in self.main_steps:
            if step.is_broken(original, translated):
                return True

        return False
