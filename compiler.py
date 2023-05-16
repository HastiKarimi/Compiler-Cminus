import string
from scanner import Scanner


class State:

    def __init__(self, id: int, terminality_status: int, type_id: int = 0, error_string: str = "Invalid input"):
        self.transitions = {}
        self.id = id
        self.error_str = error_string
        # terminality status:
        # 0: is none-terminal
        # 1: is terminal and non star
        # 2: is terminal and with star
        self.terminality_status = terminality_status
        self.type_id = type_id

    def add_transition(self, char: str, goal_state: int):
        self.transitions[char] = goal_state

    def get_next_state(self, character: str) -> int:
        if character in self.transitions:
            return self.transitions[character]
        elif "all" in self.transitions and character != "\0":
            return self.id
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
# every other thing # 8
char_groups = [[";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"], ["*"], ["="], ["/"],
               ["\n", "\r", "\t", "\v", "\f", " "], ["\0"], list(string.ascii_letters),
               ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["all"]]


def make_transition(chars_id: list[int], goal_states: list[int], state: State):
    if len(chars_id) != len(goal_states):
        print("basi wrong")

    for i in range(len(chars_id)):
        for char in char_groups[chars_id[i]]:
            state.add_transition(char, goal_states[i])


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
        scanner.write_error_file()
        break

in_file.close()
out_file.close()
lex_file.close()
sym_file.close()
