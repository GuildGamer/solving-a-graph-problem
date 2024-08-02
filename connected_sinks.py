# 1. I first define rules for connection which is a dictionary that hold objects that each object can be connected to based on their position(up, down, left and right) relative to the object in question.
# 2. Then I load the system into the program as an array of arrays
# 3. I then identify all the sinks since they are the objects in question
# 4. I define a function called is_connected_fn that tells me if 2 cells are connected
# 5. I define a function called check_all_connections that checks the cells at positions up, down, left and right around a cell and returns True if they are connected to  a cell that contains the source. If they are connected to another cell that does but the cell does not contain the source, I recursively call the function to check if that cell is connected to the source, since a cell connected to a cell that is connected to the source is also connected to the source.
# 6. in the main function, I iteratively call the  check_all_connections to check if each of the sinks is connected to the source
# 7. For every cell connected to the source, I add it to a list using list comprehension
# 8. I then sort that list
# 9. I convert the sorted array into a string and return the connected_sinks_string

# rules
alphabet = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "*",
]
rules = {
    "╩": {
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": [],
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
    },
    "═": {
        "up": [],
        "down": [],
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
    },
    "║": {
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "left": [],
        "right": [],
    },
    "╔": {
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "up": [],
        "left": [],
    },
    "╗": {
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "up": [],
        "right": [],
    },
    "╚": {
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
        "down": [],
        "left": [],
    },
    "╝": {
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": [],
        "right": [],
    },
    "╠": {
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "left": [],
    },
    "╣": {
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "right": [],
    },
    "╦": {
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        "up": [],
    },
    "╩": {
        "left": ["╦", "╠", "╔", "╩", "╚", "═"],
        "right": ["╩", "╣", "╗", "╦", "╝", "═"],
        "up": ["╦", "║", "╠", "╔", "╗", "╣"],
        "down": [],
    },
}

data = []


# def append_alphabet_to_rules(rules_dict):
#     for key, value in rules.items():
#         for direction, symbols in value.items():
#             if isinstance(symbols, list):  # Ensure we only append to lists
#                 symbols.extend(alphabet)


def is_connected_fn(a, b, b_position):
    # print("A", a, "B", b, "POSITION", b_position)
    if a.isupper() and b.isupper():
        return True

    if a.isupper() and b == "*":
        return True

    if a == "*" and b.isupper():
        return True

    if a.isupper():
        rules[a] = {
            "left": ["╦", "╠", "╔", "╩", "╚", "═"],
            "right": ["╩", "╣", "╗", "╦", "╝", "═"],
            "up": ["╦", "║", "╠", "╔", "╗", "╣"],
            "down": ["╚", "╝", "╣", "╠", "║", "╩"],
        }

    rules[a][b_position].extend(alphabet)

    # print("RULES", rules)
    return b in rules[a][b_position]


def load_data(file_path):
    with open(file_path, "r") as file:
        data = []
        for line in file:
            line_arr = line.strip().split(" ")
            data.append([line_arr[0], int(line_arr[1]), int(line_arr[2])])

        return data


def get_sinks(data):
    sinks = [element for element in data if element[0].isupper()]
    return sinks


def get_element(x, y):
    for element in data:
        if element[1] == x and element[2] == y:
            return element


def check_all_connections(element, previous_direction, memo={}):
    if id(element) in memo:
        return memo[id(element)]

    memo[id(element)] = True
    print("Checking all connections around", element)
    up_cell = [element[1], element[2] + 1]
    down_cell = [element[1], element[2] - 1]
    left_cell = [element[1] - 1, element[2]]
    right_cell = [element[1] + 1, element[2]]

    for direction in ["up", "down", "left", "right"]:
        # Check if it is connected to the cell on top
        if direction == "up":
            up = get_element(up_cell[0], up_cell[1])
            if up and up_cell[0] >= 0 and up_cell[1] >= 0:
                if previous_direction != "down":
                    is_connected = is_connected_fn(element[0], up[0], "up")
                    print("Is connected to UP cell ", f"[{up}]", ":", is_connected)
                    if is_connected and up[0] == "*":
                        return True
                    elif is_connected and up[0] != "*":
                        all_connections = check_all_connections(up, "up", memo)
                        if all_connections == True:
                            return True
                        else:
                            continue
                    else:
                        continue

        # Check if it is connected to the cell on the right
        if direction == "right":
            right = get_element(right_cell[0], right_cell[1])
            if right and right_cell[0] >= 0 and right_cell[1] >= 0:
                if previous_direction != "left":
                    is_connected = is_connected_fn(element[0], right[0], "right")
                    print(
                        "Is connected to RIGHT cell ", f"[{right}]", ":", is_connected
                    )
                    if is_connected and right[0] == "*":
                        return True
                    elif is_connected and right[0] != "*":
                        all_connections = check_all_connections(right, "right", memo)
                        if all_connections == True:
                            return True
                        else:
                            continue
                    else:
                        continue

        # Check if it is connected to the cell on the left
        if direction == "left":
            left = get_element(left_cell[0], left_cell[1])
            if left and left_cell[0] >= 0 and left_cell[1] >= 0:
                if previous_direction != "right":
                    is_connected = is_connected_fn(element[0], left[0], "left")
                    print("Is connected to LEFT cell ", f"[{left}]", ":", is_connected)
                    if is_connected and left[0] == "*":
                        return True
                    if is_connected and left[0] != "*":
                        all_connections = check_all_connections(left, "left", memo)
                        if all_connections == True:
                            return True
                        else:
                            continue
                    else:
                        continue

        # Check if it is connected to the cell down
        if direction == "down":
            down = get_element(down_cell[0], down_cell[1])
            if down and down_cell[0] >= 0 and down_cell[1] >= 0:
                if previous_direction != "up":
                    is_connected = is_connected_fn(element[0], down[0], "down")
                    print("Is connected to DOWN cell ", f"[{down}]", ":", is_connected)
                    if is_connected and down[0] == "*":
                        return True
                    if is_connected and down[0] != "*":
                        all_connections = check_all_connections(down, "down", memo)
                        if all_connections == True:
                            return True
                        else:
                            continue
                    else:
                        continue


def main(file_path):
    global data
    data = load_data(file_path)
    sinks = get_sinks(data)

    connected_sinks = [sink[0] for sink in sinks if check_all_connections(sink, "")]
    sorted_connected_sinks = sorted(connected_sinks)
    connected_sinks_string = "".join(sorted_connected_sinks)

    print(connected_sinks_string)
    return connected_sinks_string


if __name__ == "__main__":
    file_path = input("Enter the path to the txt file with the system: ")
    main(file_path)
