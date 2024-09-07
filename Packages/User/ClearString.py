import sublime
import sublime_plugin
import re


class ClearFirstStringCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cursor_position = self.view.sel()[0].begin()
        line_region = self.view.line(cursor_position)
        line_content = self.view.substr(line_region)

        matches = list(re.finditer(r'(["\'`])(?:\\.|(?!\1).)*\1', line_content))

        found_next_string = False

        for match in matches:
            quote_char = match[0][0]
            start = match.start(0) + line_region.begin()
            end = match.end(0) + line_region.begin()

            if start <= cursor_position <= end:
                found_next_string = True
                continue

            if found_next_string or cursor_position < start:
                self.clear_and_jump(edit, start, end, quote_char)
                return

        if matches:
            start = matches[0].start(0) + line_region.begin()
            end = matches[0].end(0) + line_region.begin()
            quote_char = matches[0][0]
            self.clear_and_jump(edit, start, end, quote_char)

    def clear_and_jump(self, edit, start, end, quote_char):
        string_region = sublime.Region(start, end)

        self.view.sel().clear()
        self.view.sel().add(string_region)
        self.view.replace(edit, string_region, quote_char + quote_char)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(start + 1, start + 1))
