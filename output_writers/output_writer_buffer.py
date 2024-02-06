class BufferItem:
    def __init__(self, content: str, start: int, end: int):
        self.content = content
        self.start = start
        self.end = end


class OutputWriterBuffer:
    items: list[BufferItem]

    def __init__(self):
        self.items = []

    def append(self, content: str, start: int, end: int):
        self.items.append(BufferItem(content, start, end))

    def apply_on_lines(self, lines: list[str]):
        result = []
        current_end = -1

        for i in range(0, len(lines)):
            if i <= current_end:
                continue

            buffer_item = self.__try_get_buffer_item(i)

            if buffer_item is None:
                line = lines[i]
                result.append(line)
                continue

            result.append(self.escape_content_value(buffer_item.content))
            current_end = buffer_item.end

        return result

    def __try_get_buffer_item(self, start: int):
        result = None

        for i in range(0, len(self.items)):
            item = self.items[i]

            if item.start != start:
                continue

            result = item
            break

        return result

    def escape_content_value(self, content: str) -> str:
        return f'msgstr "{content}"\n'

        pass
