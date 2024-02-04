from rules.base_rule import BaseRule
import re


REG_EX = r"(?<=\S)\'(?=\S)(?![.,'!#%])"


class SingleQuotesRule(BaseRule):
    def fix_translation(self, original: str, translated: str) -> str:
        return re.sub(REG_EX, '`', translated)

    def is_broken(self, original: str, translated: str) -> bool:
        return bool(re.search(REG_EX, translated))

    def get_error_message(self, pipeline_input) -> str:
        return self.generate_base_error_message("Single quote mismatch", pipeline_input)
