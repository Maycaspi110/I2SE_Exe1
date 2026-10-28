def plane_kind(numbers):

      # Decide the plane shape by counting the numbers in a CSV row:
    # 9 numbers = 3 points = triangle, 12 numbers = 4 points = trapezoid.

    if len(numbers) == 9:
        return "triangle"
    if len(numbers) == 12:
        return "trapezoid"

     # Edge case E3: wrong amount of numbers
    raise ValueError("a plane row must have 9 or 12 numbers, got " + str(len(numbers)))

def read_planes(path):

     # Read the CSV file and return a list of planes (each a list of numbers).
    # Any bad row stops the program with a clear message (our design decision)

    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:  # Edge case E1: file missing or unreadable
        raise ValueError(str(path) + ": cannot read CSV file") from None

     # enumerate numbers the lines from 1, so errors can name the row
    planes = []
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "":
            continue

        # Edge case E4: something that is not a number
        try:
            numbers = [float(x) for x in line.split(",")]
        except ValueError:
            raise ValueError("row " + str(line_number) + ": contains a non-numeric value") from None
        plane_kind(numbers)
        planes.append(numbers)
    return planes