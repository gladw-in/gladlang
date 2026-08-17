"""DictNode – represents dictionary literals {key: value, ...}."""


class DictNode:
    def __init__(self, key_value_pairs, position_start, position_end):
        self.key_value_pairs = key_value_pairs
        self.position_start = position_start
        self.position_end = position_end
