def plane_kind(numbers):
    if len(numbers) == 9:
        return "triangle"
    if len(numbers) == 12:
        return "trapezoid"
    raise ValueError("a plane row must have 9 or 12 numbers, got " + str(len(numbers)))