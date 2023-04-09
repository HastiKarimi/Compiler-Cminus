# todo : symbol table (done) , handling errors, transitions, parser alternate (done), output file (done)
# negar, hasti, hasti, negar

import string


class State:

    def __init__(self, id: int, terminality_status: int, error_string: str = "empty", type_id: int = 0):
        self.transitions = []
        self.id = id
        self.error_str = error_string
        # terminality status:
        # 0: is none-terminal
        # 1: is terminal and non star
        # 2: is terminal and with star
        self.terminality_status = terminality_status
        self.type_id = type_id

    def add_transition(self, ascii_ranges: [int, int], goal_state: int):
        self.transitions.append((ascii_ranges, goal_state))

    def get_next_state(self, character: str) -> int:
        for transition in self.transitions:
            ascii_ranges, goal_state = transition
            input_ascii = ord(character)
            for (begin, end) in ascii_ranges:
                if begin <= input_ascii <= end:
                    return goal_state
        return -1

    def get_error(self, character: str = "") -> str:
        return self.error_str


# symbols = [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"]  # 0
# star = ["*"]  # 1
# equal = ["="]  # 2
# slash = ["/"]  # 3
# whitespaces = ["\n", "\r", "\t", "\v", "\f", " "]  # 4
# eof = ["\0"]  # 5
# letters = list(string.ascii_letters)  # 6
# digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]  # 7
char_groups = [[";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"], ["*"], ["="], ["/"],
               ["\n", "\r", "\t", "\v", "\f", " "], ["\0"], list(string.ascii_letters),
               ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]


def make_transition(chars_id: list[int], goal_states: list[int], state: State):
    for i in range(len(chars_id)):
        for char in char_groups[i]:
            state.add_transition(char, goal_states[i])


class Scanner:
    state_list = []
    s = State(id=0, terminality_status=0, error_string="Invalid input")
    make_transition(chars_id=[7, 5, 6, 0, 2, 3, 4, 1], goal_states=[1, 0, 3, 5, 6, 9, "?"],
                    state=s)  # TODO add transition for *

    state_list.append(s)

    s = State(id=1, terminality_status=0, error_string="Invalid number")
    make_transition(chars_id=[0, 1, 2, 3, 4, 5, 7], goal_states=[2, 2, 2, 2, 2, 0, 1],
                    state=s)

    state_list.append(s)

    s = State(id=2, terminality_status=2, type_id=1)
    state_list.append(s)

    s = State(id=3, terminality_status=0, error_string="Invalid input")
    make_transition(chars_id=[0, 1, 2, 3, 4, 5, 6, 7], goal_states=[4, 4, 4, 4, 4, 0, 3, 3],
                    state=s)

    def __init__(self, input_file, output_file, lex_file, sym_file):
        self.input_file = input_file
        self.output_file = output_file
        self.lex_file = lex_file
        self.sym_file = sym_file
        self.types = {1: "NUM", 2: "ID", 3: "KEYWORD", 4: "SYMBOL", 5: "COMMENT", 6: "WHITESPACE"}

        # elements of the symbol table - keywords should go first.
        self.keywords = []
        self.identifiers = []

        self.line_number = 0
        self.current_line = ""
        self.start_pnt = -1
        self.end_pnt = -1
        self.errors = []

    # returns a tuple (next_char, line_updated)
    def get_next_char(self):
        line_updated = False
        if self.line_number == 0 or self.end_pnt == len(self.current_line) - 1:
            self.current_line = self.input_file.readline()
            if len(self.current_line) == 0:
                return '\0'
            self.end_pnt = -1
            self.line_number += 1
            line_updated = True

        if self.start_pnt == self.end_pnt:
            self.start_pnt = self.end_pnt + 1
        self.end_pnt += 1
        return self.current_line[self.end_pnt], line_updated

    # if a type (id, number,...) is valuable for parser, returns true, else false
    @staticmethod
    def is_type_parsable(self, type_id: int):
        return type_id not in [5, 6]

    # output:
    #   the next token valuable for parser
    #   None if no other token is available
    def get_next_token(self, write_to_file=True):
        state_id = 0
        while self.state_list[state_id].terminality_status == 0:
            next_char, line_updated = self.get_next_char()
            next_state_id = self.state_list[state_id].get_next_state(next_char)
            # the id of eof state is 0
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
            token = self.types[type_id], lexeme
            self.install_in_symbol_table(token)
            if write_to_file:
                self.update_sym_file()
                self.update_output_file(token, line_updated)
            return token
        else:
            return self.get_next_token()

    def handle_error(self, state_id: int, char: str):
        lexeme = self.current_line[self.start_pnt: self.end_pnt + 1]
        self.errors.append([self.line_number, lexeme, self.state_list[state_id].get_error()])
        # self.lex_file.write(self.state_list[state_id].get_error())

    def install_in_symbol_table(self, token):
        keyword_type = "KEYWORD"
        id_type = "ID"
        type, lexeme = token
        if type == keyword_type:
            if lexeme not in self.keywords:
                self.keywords.append(lexeme)
        elif type == id_type:
            if lexeme not in self.identifiers:
                self.identifiers.append(lexeme)

    # todo can have performance improvements if the order of symbols does not matter
    def update_sym_file(self):
        text = ""
        index_separator = ".\t"
        index = 0
        for keyword in self.keywords:
            index += 1
            text += index + index_separator + keyword + "\n"
        for identifier in self.identifiers:
            index += 1
            text += index + index_separator + identifier + "\n"

        self.sym_file.truncate(0)
        self.sym_file.seek(0)
        self.sym_file.write(text)

    #   new_token: the token (type, lexeme) to add to output file
    #   line_updated: a bool that shows if the token is for a new line (we should update the line numbre in file)
    def update_output_file(self, new_token, line_updated: bool):
        type, lexeme = new_token
        text = ""
        if line_updated:
            if self.line_number != 0:
                text += "\n"
            text += self.line_number + ".\t"
        else:
            text += " "
        text += "(" + type + ", " + lexeme + ")"
        self.output_file.write(text)


# initialize a scanner and call get_next_token repeatedly

in_file = open("input.txt", "r")
out_file = open("tokens.txt", "w+")
lex_file = open("lexical_errors.txt", "w+")
sym_file = open("symbol_table.txt", "w+")

scanner = Scanner(
    input_file=in_file,
    output_file=out_file,
    lex_file=lex_file,
    sym_file=sym_file
)

while True:
    token = scanner.get_next_token()
    if token is None:
        break

in_file.close()
out_file.close()
lex_file.close()
sym_file.close()


# todo
def add_states(scanner: Scanner):
    pass
