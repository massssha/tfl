from table import *


def main():
    table = Table()
    table_response = ""

    while table_response != "TRUE":
        while table.index_extend < table.start_closed_table:
            table.extend()
            table.closed()

        table_response = api.table(table)
        if table_response != "TRUE":
            suffix = ""
            for letter in reversed(table_response):
                suffix = letter + suffix
                if table.suffixes_dict.get(suffix) is None:
                    table.suffixes.append(suffix)
                    table.suffixes_dict[suffix] = 1

            for i in range(len(table.prefixes)):
                table.row_isin(i)

            table.closed()

    table.write_dfa()


if __name__ == '__main__':
    print("Started")
    main()
