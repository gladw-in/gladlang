"""Source detachment – recursively removes source text references from AST nodes to free memory."""


def detach_value(value):
    if isinstance(value, (list, tuple)):
        for item in value:
            detach_value(item)

    elif hasattr(value, "position_start"):
        detach_source_from_node(value)


def detach_source_from_node(node, visited=None):
    if node is None:
        return

    if visited is None:
        visited = {}

    node_identifier = id(node)
    if node_identifier in visited and visited[node_identifier] is node:
        return

    visited[node_identifier] = node

    if hasattr(node, "position_start") and node.position_start:
        node.position_start.detach_source()

    if hasattr(node, "position_end") and node.position_end:
        node.position_end.detach_source()

    try:
        items = vars(node).items()
    except TypeError:
        items = []
        for name in dir(node):
            if name.startswith("__") or callable(getattr(node, name)):
                continue

            items.append((name, getattr(node, name)))

    for _, value in items:
        detach_value(value)
