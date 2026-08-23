"""C3-linearization-style MRO (method resolution order) computation."""


class InterpreterComputeMro:
    def compute_mro(self, class_value):
        merge_lists = [[class_value]]
        for parent in class_value.superclasses:
            merge_lists.append(parent.mro[:])

        merge_lists.append(class_value.superclasses[:])
        mro = []

        while True:
            merge_lists = [sequence for sequence in merge_lists if sequence]
            if not merge_lists:
                break

            chosen_head = None
            for sequence in merge_lists:
                candidate = sequence[0]
                is_valid = True
                for other_sequence in merge_lists:
                    if candidate in other_sequence[1:]:
                        is_valid = False
                        break

                if is_valid:
                    chosen_head = candidate
                    break

            if not chosen_head:
                return None, "Inconsistent inheritance hierarchy (Cycle or bad MRO)"

            mro.append(chosen_head)
            for sequence in merge_lists:
                if sequence and sequence[0] == chosen_head:
                    sequence.pop(0)

        return mro, None
