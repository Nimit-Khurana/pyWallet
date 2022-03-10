from terminaltables import AsciiTable


def tablify(data):
    table_data = [["id", "user", "site", "username", "password", "url", "additional_info", "media"]]
    for d in data:
        table_data.append(list(d))
    table = AsciiTable(table_data)
    return table.table

def clear_screen():
   print('\x1b[1J')
   return True