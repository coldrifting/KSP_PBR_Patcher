class StringWriter:

    def __init__(self):
        self.string = ""
        self.indent_count = 0
        self.tab = "  "
        self.new_line = "\n"

    def indent(self, section_name: str | None = None):
        if len(self.string) > 2 and self.string[-2:] == '}\n':
            self.write()

        if section_name is not None:
            self.write(section_name)

        self.write("{")
        self.indent_count += 1

    def unindent(self):
        if self.string[-3:] == '}\n\n':
            self.string = self.string[:-1]

        self.indent_count -= 1
        self.write("}")

    def write(self, text: str | None = None):
        if text is None:
            self.string += self.new_line
        else:
            self.string += ((self.tab * self.indent_count) + text + self.new_line)

    def get_string(self) -> str:
        return self.string