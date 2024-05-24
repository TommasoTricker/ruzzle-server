def calculate_average_line_length(filename):
    """
    This function calculates the average line length in characters (excluding newline) of a file.

    Args:
        filename: The path to the file.

    Returns:
        The average line length as a float, or None if the file is empty.
    """

    total_length = 0
    line_count = 0

    with open(filename, "r") as file:
        for line in file:
            # Remove trailing newline character
            stripped_line = line.rstrip("\n")
            # Add length of the stripped line
            total_length += len(stripped_line)
            line_count += 1

    # Check if there were any lines in the file
    if line_count == 0:
        return None

    # Calculate and return average line length
    return total_length / line_count


# Example usage
filename = "dictionary_eng.txt"
average_length = calculate_average_line_length(filename)

if average_length is not None:
    print(
        f"The average line length in '{filename}' is {average_length:.2f} characters (excluding newline)."
    )
else:
    print(f"The file '{filename}' is empty.")
