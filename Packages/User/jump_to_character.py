import sublime
import sublime_plugin


class JumpToCharacterCommand(sublime_plugin.TextCommand):

    def run(self, edit, character="", adjustment=0):
        if not character:
            return

        cursor_position = self.view.sel()[0].begin()
        region = self.view.find(character, cursor_position, sublime.LITERAL)

        if region.begin() == cursor_position:
            cursor_position += 1
            region = self.view.find(character, cursor_position)

        if region:
            new_cursor_position = region.begin()
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(new_cursor_position + adjustment))
