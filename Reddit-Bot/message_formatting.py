def format_message(message):
    lines = message.split("\n")
    formatted_lines = [f"> {line}" for line in lines]
    formatted_message = "\n".join(formatted_lines)
    return formatted_message