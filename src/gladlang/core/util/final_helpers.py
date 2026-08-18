"""Final constant detection – checks if a name is a constant anywhere in the symbol table chain."""


def is_final_anywhere(current_table, variable_name):
    while current_table:
        if not current_table._finals_count:
            current_table = current_table.parent
            continue

        with current_table._lock:
            if variable_name in current_table.finals:
                return True

        current_table = current_table.parent

    return False
