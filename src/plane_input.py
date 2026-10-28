def plane_kind(numbers):
    if len(numbers) == 9:
        return "triangle"
    if len(numbers) == 12:
        return "trapezoid"
    raise ValueError("a plane row must have 9 or 12 numbers, got " + str(len(numbers)))

def read_planes(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        raise ValueError(str(path) + ": cannot read CSV file") from None

    planes = []
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "":
            continue
        try:
            numbers = [float(x) for x in line.split(",")]
        except ValueError:
            raise ValueError("row " + str(line_number) + ": contains a non-numeric value") from None
        plane_kind(numbers)
        planes.append(numbers)
    return planes