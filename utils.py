from csv import reader


def map_from_csv(path):
    with open(path) as file:
        data = list(reader(file, delimiter=","))
    return data
