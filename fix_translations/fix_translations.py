import re

REG_EX = r'\$\(([^\)]+)\)'


class FixTranslations:
    @staticmethod
    def fix_translation(original: str, translated: str) -> str:
        original_parts = FixTranslations._get_parts(original)
        translated_parts = FixTranslations._get_parts(translated)

        if not FixTranslations._is_broken(original_parts, translated_parts):
            return translated

        result = list()
        start = 0

        for part_index in range(0, len(translated_parts)):
            original_part = original_parts[part_index]
            translated_part = translated_parts[part_index]

            if not original_part or not translated_part:
                continue

            result.append(translated[start:translated_part.start()])
            result.append(original[original_part.start():original_part.end()])
            start = translated_part.end()

        result.append(translated[start:])

        return ''.join(result)

    @staticmethod
    def is_broken(original: str, translated: str) -> bool:
        original_parts = FixTranslations._get_parts(original)
        translated_parts = FixTranslations._get_parts(translated)

        return FixTranslations._is_broken(original_parts, translated_parts)

    @staticmethod
    def _is_broken(original_parts, translated_parts) -> bool:
        for part_index in range(0, len(translated_parts)):
            original_part = original_parts[part_index].groups()
            translated_part = translated_parts[part_index].groups()

            if not (original_part == translated_part):
                return True

        return False

    @staticmethod
    def _get_parts(text: str):
        return list(re.finditer(REG_EX, text))
