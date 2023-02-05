def get_similar_keys(dictionary: dict, value: str, delimiter: str = ''):
    similar_values: str = ''

    for key, _ in dictionary.items():
        if value in key or key in value:
            similar_values += key + delimiter

    return similar_values if not similar_values else similar_values[:-len(delimiter)]


def get_similar_values(list_of_values: list, value: str, delimiter: str = ''):
    similar_values: str = ''

    for list_value in list_of_values:
        if value in list_value or list_value in value:
            similar_values += list_value + delimiter

    return similar_values if not similar_values else similar_values[:-len(delimiter)]
