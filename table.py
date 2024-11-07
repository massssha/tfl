import api
from operator import itemgetter
from itertools import groupby

alphabet = ['S', 'N', 'W', 'E']


def concat(prefix, suffix):
    if suffix == 'e':
        word = prefix
    elif prefix == 'e':
        word = suffix
    else:
        word = prefix + suffix
    return word


def equal_rows(row_first, row_second):
    for i in range(len(row_first)):
        if row_first[i] != row_second[i]:
            return False
    return True


class Table:
    prefixes, suffixes = ['e'], ['e']
    rows = [[0]]
    prefixes_dict = {'e': 1}
    suffixes_dict = {'e': 1}

    index_extend = 0
    start_closed_table = 1

    def row_isin(self, row_index):
        row = self.rows[row_index]
        suffixes = self.suffixes
        for j in range(len(row), len(suffixes)):
            suffix = suffixes[j]
            word = concat(self.prefixes[row_index], suffix)
            row.append(api.isin(word))

    def extend(self):
        index_extend, start_closed_table = self.index_extend, self.start_closed_table
        prefixes, suffixes = self.prefixes, self.suffixes
        rows = self.rows

        for i in range(index_extend, start_closed_table):
            prefix = prefixes[i]
            for letter in alphabet:
                prefix_extend = concat(prefix, letter)
                if self.prefixes_dict.get(prefix_extend) is None:
                    self.prefixes_dict[prefix_extend] = 1
                    prefixes.append(prefix_extend)
                    rows.append([])
                    self.row_isin(len(prefixes) - 1)

        self.index_extend = start_closed_table

    def closed(self):
        start_closed_table = self.start_closed_table
        prefixes = self.prefixes
        rows = self.rows

        for i in range(start_closed_table, len(prefixes)):
            count_equal_rows = sum(int(equal_rows(rows[i], rows[j])) for j in range(self.start_closed_table))
            if count_equal_rows == 0:
                prefixes[i], prefixes[self.start_closed_table] = prefixes[self.start_closed_table], prefixes[i]
                rows[i], rows[self.start_closed_table] = rows[self.start_closed_table], rows[i]
                self.start_closed_table += 1

    def write_dfa(self):
        f = open('dfa.txt', 'w')
        prefixes, rows = self.prefixes, self.rows
        main_prefixes = {}
        extend_prefixes = {}
        for i in range(self.start_closed_table):
            main_prefixes[prefixes[i]] = [str(i + 1), rows[i]]
        for i in range(self.start_closed_table, len(prefixes)):
            for p in main_prefixes:
                if equal_rows(rows[i], main_prefixes[p][1]):
                    extend_prefixes[prefixes[i]] = main_prefixes[p][0]
                    break

        f.write("digraph {\n")
        f.write("\trankdir = LR\n")
        f.write("\tstart [shape = point]\n")
        f.write(f"\tstart -> 1\n")
        for p in main_prefixes:
            prefix_state = main_prefixes[p][0]
            if main_prefixes[p][1][0] == 1:
                f.write(f"\t{prefix_state} [shape = doublecircle]\n")

            transition = []
            for letter in alphabet:
                state = concat(p, letter)
                if main_prefixes.get(state) is not None:
                    transition.append(main_prefixes[state][0])
                else:
                    transition.append(extend_prefixes[state])

            transitions_with_alphabet = list(zip(transition, alphabet))
            transitions_with_alphabet.sort(key=itemgetter(0))
            for state, group in groupby(transitions_with_alphabet, key=itemgetter(0)):
                labels = ', '.join(label for _, label in group)
                f.write(f"\t{prefix_state} -> {state} [label = \"{labels}\"]\n")

        f.write("}")
        f.close()
        print("Saved in dfa.txt")


