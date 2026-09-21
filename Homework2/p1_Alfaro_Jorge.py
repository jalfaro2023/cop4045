"""Problem 1: number source lines and extract Python functions."""

import ast
import io
from pathlib import Path
import tokenize


def line_number(input_file: str, output_file: str) -> None:
    """Copy a text file, prefixing every line with its 1-based number."""
    try:
        source, target = Path(input_file), Path(output_file)
        if source.resolve() == target.resolve() or (
                target.exists() and source.samefile(target)):
            raise ValueError("Input and output must be different files.")
        with source.open(encoding="utf-8") as reader:
            lines = reader.readlines()
        with target.open("w", encoding="utf-8") as writer:
            for number, line in enumerate(lines, 1):
                writer.write(f"{number}: {line}")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Could not number the file: {error}")
        raise


def parse_functions(filename: str) -> tuple[tuple[int, str, str, str], ...]:
    """Return functions sorted by name as (line, name, arguments, code).

    Include nested functions and methods. Keep docstrings and '#' inside
    strings; remove comment tokens and empty lines from the returned code.
    """
    try:
        with tokenize.open(filename) as reader:
            source = reader.read()
        functions = []
        for node in ast.walk(ast.parse(source, filename)):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            code = ast.get_source_segment(source, node)
            lines = code.splitlines(keepends=True)
            tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
            depth, start, end = 0, None, None
            offsets = [0]
            for line in lines:
                offsets.append(offsets[-1] + len(line))
            for token in tokens:
                if token.type == tokenize.COMMENT:
                    row, column = token.start
                    lines[row - 1] = lines[row - 1][:column] + "\n"
                if token.type == tokenize.OP and end is None:
                    if token.string == "(":
                        if start is None:
                            start = offsets[token.end[0] - 1] + token.end[1]
                        depth += 1
                    elif token.string == ")" and start is not None:
                        depth -= 1
                        if depth == 0:
                            end = offsets[token.start[0] - 1] + token.start[1]
            arguments = code[start:end]
            cleaned = "\n".join(line.rstrip() for line in lines if line.strip())
            functions.append((node.lineno, node.name, arguments, cleaned + "\n"))
        return tuple(sorted(functions, key=lambda item: item[1]))
    except (OSError, UnicodeError, SyntaxError, tokenize.TokenError) as error:
        print(f"Could not parse Python functions: {error}")
        raise


def main() -> None:
    """Demonstrate both functions using this source file."""
    print("Student: Jorge Alfaro | FAU ID: Z23697022 | Problem 1")
    source = Path(__file__).resolve()
    destination = str(source) + ".txt"
    line_number(str(source), destination)
    print(f"Numbered source saved to {destination}")
    print(parse_functions(str(source)))


if __name__ == "__main__":
    main()
