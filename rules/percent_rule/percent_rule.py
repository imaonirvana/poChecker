from rules.base_rule import BaseRule
import re


REG_EX = r'\'*\(*\{*\[*%([\w\.\-\>\|{})\[\](%\']+)'
baned_parts = ["%%"]


class PercentRule(BaseRule):
    def fix_translation(self, original: str, translated: str) -> str:
        original_parts = self._get_parts(original)
        translated_parts = self._get_parts(translated)

        if not self._is_parts_broken(original_parts, translated_parts):
            return translated

        result = list()
        start = 0

        for part_index in range(0, min(len(translated_parts), len(original_parts))):
            original_part = original_parts[part_index]
            translated_part = translated_parts[part_index]

            if not original_part or not translated_part:
                continue

            result.append(translated[start:translated_part.start()])
            result.append(original[original_part.start():original_part.end()])
            start = translated_part.end()

        result.append(translated[start:])

        return ''.join(result)

    def is_broken(self, original: str, translated: str) -> bool:
        original_parts = self._get_parts(original)
        translated_parts = self._get_parts(translated)

        return self._is_parts_broken(original_parts, translated_parts)

    def get_error_message(self, pipeline_input) -> str:
        return self.generate_base_error_message("Percent rule mismatch", pipeline_input)

    def _get_parts(self, text: str):
        result = []

        for part in list(re.finditer(REG_EX, text)):
            if part.groups()[0] in baned_parts:
                continue

            result.append(part)

        return result

    def _is_parts_broken(self, original_parts, translated_parts) -> bool:
        for original_part, translated_part in zip(original_parts, translated_parts):
            original_part_str = original_part.groups()[0]
            translated_part_str = translated_part.groups()[0]

            if original_part_str != translated_part_str:
                return True

        return False
