"""StatementListNode – represents a sequence of statements (a block)."""


class StatementListNode:
    def __init__(self, statement_nodes, position_start, position_end):
        self.statement_nodes = statement_nodes
        self.position_start = position_start
        self.position_end = position_end

    def __repr__(self):
        return f'[{", ".join(map(str, self.statement_nodes))}]'
