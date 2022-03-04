import pygments.token
import pygments.lexers

def process(filename):
    file = open(filename, "r")
    lines = file.read()
    file.close()
    lexer = pygments.lexers.guess_lexer_for_filename(filename, lines)
    tokens = lexer.get_tokens(lines)
    tokens = list(tokens)

    processed = []
    stripped = []
    for token in tokens:
        if token[0] == pygments.token.Name:
            processed.append("V")
            stripped.append(token[1])
        elif token[0] in pygments.token.Literal.String:
            processed.append("S")
            stripped.append(token[1])
        elif token[0] in pygments.token.Name.Function:
            processed.append("F")
            stripped.append(token[1])
        elif token[0] in pygments.token.Comment:
            processed.append('\n')
            stripped.append('\n')
        elif tokens[0] == pygments.token.Text:
            pass
        else:
            processed.append(token[1])
            stripped.append(token[1])

    processed = str("".join(processed)) # join all the tokens
    processed = "".join([s for s in processed.strip().splitlines(True) if s.strip()]) # remove blank lines

    stripped = str("".join(stripped))  # join all the tokens
    stripped = "".join([s for s in stripped.strip().splitlines(True) if s.strip()])  # remove blank lines

    with open(filename + '_Stripped', "w") as text_file:
        text_file.write(stripped)
        text_file.close()

    #with open(filename + '_Processed', "w") as text_file:
    #    text_file.write(processed)
    #    text_file.close()

    return processed
