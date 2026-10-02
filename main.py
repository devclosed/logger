# --- variables storage ---
variables = {}   # name -> value
types = {}       # name -> type
errors  = []     # list of error messages

# --- read file ---
file = open("game.log", "r")
text = file.read()
file.close()

lines = text.split("\n")

for i, line in enumerate(lines):
    line_number = i + 1
    program = line.strip()

    # skip empty lines
    if program == "":
        continue

    # skip comments
    if program.startswith("//"):
        continue

    # --- SAY ---
    if program.startswith("say "):
        message = program[4:].strip()

        if message.startswith('"') and message.endswith('"'):
            print(message[1:-1])
        elif message in variables:
            print(variables[message])
        else:
            print(message)

    # --- DECLARE ---
    elif program.startswith("int ") or program.startswith("float ") or program.startswith("str "):
        left_part, right_part = program.split("=", 1)
        left_part = left_part.strip()
        right_part = right_part.strip()

        type_and_name = left_part.split()
        vartype = type_and_name[0]
        varname = type_and_name[1]

        # --- CHECK TYPE ---
        is_text  = right_part.startswith('"') and right_part.endswith('"')
        is_int   = right_part.isdigit() or (right_part.startswith("-") and right_part[1:].isdigit())
        is_float = False

        if not is_text and not is_int:
            try:
                float(right_part)
                is_float = True
            except ValueError:
                is_float = False

        # --- RULES ---
        if vartype == "int":
            if is_text:
                errors.append("line " + str(line_number) + ": cannot put text into int")
                continue
            if is_float:
                errors.append("line " + str(line_number) + ": cannot put float into int")
                continue
            if not is_int:
                errors.append("line " + str(line_number) + ": int value must be a number")
                continue
            variables[varname] = int(right_part)

        elif vartype == "float":
            if is_text:
                errors.append("line " + str(line_number) + ": cannot put text into float")
                continue
            if not (is_int or is_float):
                errors.append("line " + str(line_number) + ": float value must be a number")
                continue
            variables[varname] = float(right_part)

        elif vartype == "str":
            if not is_text:
                errors.append("line " + str(line_number) + ": str value must be in quotes")
                continue
            variables[varname] = right_part[1:-1]

        types[varname] = vartype

    # --- CALCULATOR ---
    else:
        parts = program.split()
        left  = int(parts[0]) if parts[0].isdigit() else variables[parts[0]]
        op    = parts[1]
        right = int(parts[2]) if parts[2].isdigit() else variables[parts[2]]

        if op == "+":
            result = left + right
        elif op == "-":
            result = left - right
        elif op == "*":
            result = left * right
        elif op == "/":
            result = left / right

        print(result)

# --- SHOW ERRORS ---
if len(errors) > 0:
    print("")
    print("=== Logger: found " + str(len(errors)) + " error(s) ===")
    for err in errors:
        print("  " + err)