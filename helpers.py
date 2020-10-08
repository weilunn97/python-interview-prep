from json import loads, dumps


def compare_dict(d1, d2, path=""):
    print(f"\nCOMPARING...")
    print(f"D1 : {d1}")
    print(f"D2 : {d2}")

    # FOR EACH KEY IN D1
    for k in d1:

        # CHECK FOR ITS PRESENCE IN D2
        if k not in d2:
            print(f"{path} : KEY {k} MISSING FROM {d2}")
        else:

            # MAKE A RECURSIVE CALL IF THE VALUE IS OF TYPE DICT
            if type(d1[k]) is dict:
                if path == "":
                    path = f"DICT[{k}]"
                else:
                    path += f"[{k}]"
                compare_dict(d1[k], d2[k], path)

            # OTHERWISE, COMPARE THEIR VALUES DIRECTLY
            else:
                if d1[k] != d2[k]:
                    print(f"{path} : VALUE MISMATCH")
                    print(f"    - {k} : {d1[k]}")
                    print(f"    + {k} : {d2[k]}")


def json_to_dict(json_str):
    return loads(json_str)


def dict_to_json(dictionary):
    return dumps(dictionary)


d1 = {'a': {'b': {'cs': 10}, 'c': {'cs': 20, 'ce': 40}}}
d2 = {'a': {'b': {'cs': 30}, 'c': {'cs': 20}}, 'd': {'q': {'cs': 50}}}
compare_dict(d1, d2)
compare_dict(d2, d1)
