in_file = open("input.txt")
out_file = open("tokens.txt", "w")
lex_file = open("lexical_errors.txt", "w")
sym_file = open("symbol_table.txt")


# types = {1: "NUM", 2: "ID", 3: "KEYWORD", 4: "SYMBOL", 5: "COMMENT", 6: "WHITESPACE"}


class State:

    def __init__(self, id: int, error_string: str, terminality_status: int, type_id: int = 0):
        self.transitions = []
        self.id = id
        self.error_str = error_string
        self.terminality_status = terminality_status  # 0: is none-terminal
        # 1: is terminal and non star
        # 2: is terminal and with star
        self.type_id = type_id

    def add_transition(self, ascii_ranges: list[(int, int)], goal_state: int):
        self.transitions.append((ascii_ranges, goal_state))

    def get_next_state(self, character: str) -> int:
        for transition in self.transitions:
            ascii_ranges, goal_state = transition
            input_ascii = ord(character)
            for (begin, end) in ascii_ranges:
                if input_ascii >= begin and input_ascii <= end:
                    return goal_state
        return -1

    def get_error(self, character: str = "") -> str:
        return self.error_str


class Scanner:
    def __init__(self, input_file, out_file, lex_file, sym_file):
        self.input_file = input_file
        self.out_file = out_file
        self.lex_file = lex_file
        self.sym_file = sym_file
        self.state_list = []
        self.types = {1: "NUM", 2: "ID", 3: "KEYWORD", 4: "SYMBOL", 5: "COMMENT", 6: "WHITESPACE"}

        self.line_number = 0
        self.current_line = ""
        self.start_pnt = -1
        self.end_pnt = -1

    def get_next_char(self):
        if self.line_number == 0 or self.end_pnt == len(self.current_line) - 1:
            self.current_line = self.input_file.readline()
            if len(self.current_line) == 0:
                return '\0'
            self.end_pnt = -1
            self.line_number += 1

        if self.start_pnt == self.end_pnt:
            self.start_pnt = self.end_pnt + 1
        self.end_pnt += 1
        return self.current_line[self.end_pnt]

    # if a type (id, number,...) is suitable for parser, returns true, else false
    @staticmethod
    def is_type_parsable(self, type_id: int):
        return type_id not in [5, 6]

    def get_next_token(self):
        state_id = 0
        while self.state_list[state_id].terminality_status == 0:
            next_char = self.get_next_char()
            next_state_id = self.state_list[state_id].get_next_state(next_char)
            if next_state_id == 0:
                return None
            if next_state_id == -1:
                self.handle_error(state_id, next_char)
                self.start_pnt = self.end_pnt
                return self.get_next_token()

            state_id = next_state_id

        if self.state_list[state_id].terminality_status == 2:
            self.end_pnt -= 1

        lexeme = self.current_line[self.start_pnt: self.end_pnt + 1]
        type_id = self.state_list[state_id].type_id

        if self.is_type_parsable(type_id):
            return self.types[type_id], lexeme
        else:
            return self.get_next_token()

    def handle_error(self, state_id: int, char: str):
        self.lex_file.write(self.state_list[state_id].get_error())
