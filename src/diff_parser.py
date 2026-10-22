def parse_diff(raw_diff: str) -> list:
    # Implementation for parsing the diff
    structured_diff = []
    some_file = None
    current_line_num = 0
    new_lines_count = 0

    header = True
    # recognize the diff format and extract relevant information
    raw_diff_lines = raw_diff.splitlines()

    for line in raw_diff_lines:
        if line.startswith("diff --git"):
            header = True
            if some_file is not None and len(some_file["additions"]) > 0:
                structured_diff.append(some_file)

            some_file = {"old_file": "", "new_file": "", "hunks": [], "additions": []}
            some_file["old_file"] = line.split()[2][2:]
            some_file["new_file"] = line.split()[3][2:]

        elif line.startswith("@@"):
            header = False

            new_range = line.split()[2][1:]  # for example, "1,5"
            start, separator, count = new_range.partition(",")
            current_line_num = int(start)
            new_lines_count = int(count) if separator else 1

            some_file["hunks"].append((current_line_num, new_lines_count))

        elif line.startswith("+"):
            if header is False:
                some_file["additions"].append({"line": line[1:], "line_num": current_line_num})
                current_line_num += 1
            else:
                continue

        elif line.startswith("-") or line.startswith("\\"):
            continue

        elif header is False:
            current_line_num +=  1

    if some_file is not None and len(some_file["additions"]) > 0:
        structured_diff.append(some_file)

    return structured_diff
