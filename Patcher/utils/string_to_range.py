from utils.exceptions import ArgumentException


def string_to_range(range_input: str) -> list[int]:
    output: list[int] = []

    groups = range_input.split(",")
    for group in groups:
        group_start_end = group.split("-")
        if len(group_start_end) > 2:
            raise ArgumentException(f"Invalid format: {group}")

        if len(group_start_end) == 1:
            output.append(int(group_start_end[0]))
        else:
            start = int(group_start_end[0])
            end = int(group_start_end[1])
            for i in range(start, end + 1):
                output.append(i)

    return output