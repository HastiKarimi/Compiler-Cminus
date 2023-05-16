import string
from scanner import Scanner


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
