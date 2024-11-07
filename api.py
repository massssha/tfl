import subprocess


mat_path = r"C:\Users\User\tfl\MAT\tfl-lab2\main.py"

process = subprocess.Popen(
    ['python', mat_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)


def isin(word):
    try:
        process.stdin.write('isin\n')
        process.stdin.write(f'{word}\n')
        process.stdin.flush()

        response = process.stdout.readline()
        if response[0] == 'T':
            return 1
        return 0
    except Exception as e:
        print(f"Error isin: {e}")
        return None


def table(table):
    try:
        process.stdin.write('table\n')

        request = ""
        for suffix in table.suffixes:
            request += (suffix + " ")
        request.strip()
        request += "\n"

        for i in range(len(table.prefixes)):
            row_str = " ".join(map(str, table.rows[i]))
            request += f"{table.prefixes[i]} {row_str}\n"
        request += "end"

        process.stdin.write(f'{request}\n')
        process.stdin.flush()

        response = process.stdout.readline()
        return response[:-1]
    except Exception as e:
        print(f"Error table: {e}")
        return None
