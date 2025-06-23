import base64


def generate_token(*values: int | str | None) -> str:
    """
    Could I create a secure token using a secret key with the hmac algorithm? Yes.
    I want to spend more time on this? No, also, it's not a security problem.
    """
    serialized_values = []

    for value in values:
        if isinstance(value, str):
            serialized_values.append(f"s{value}")
        elif isinstance(value, int):
            serialized_values.append(f"i{value}")
        else:
            serialized_values.append("")

    if len(serialized_values) == 0:
        return ""

    token = ";".join(serialized_values)

    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")


def decode_token(token: str) -> tuple[int | str | None, ...]:
    if token == "":
        return tuple()

    token = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
    values = token.split(";")
    parsed_values = []

    for value in values:
        if value.startswith("s"):
            parsed_values.append(value[1:])
        elif value.startswith("i"):
            parsed_values.append(int(value[1:]))
        else:
            parsed_values.append(None)

    return tuple(parsed_values)
