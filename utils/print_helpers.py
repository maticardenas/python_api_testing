from pprint import pprint


def pretty_print(msg: str, indent: int = 2) -> None:
    print()
    pprint(msg, indent=indent)