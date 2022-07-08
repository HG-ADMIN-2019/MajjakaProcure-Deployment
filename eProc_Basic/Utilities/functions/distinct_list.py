def distinct_list(data_list):
    """

    """
    return set(data_list)


def distinct_dictionary_list(dictionary_list, key):
    """

    """
    value_list = []
    dic_list = []
    for dictionary in dictionary_list:
        for dic_key, dic_value in dictionary.items():
            if dic_key == key:
                if dic_value not in value_list:
                    value_list.append(dic_value)
                    dic_list.append(dictionary)
    return dic_list
