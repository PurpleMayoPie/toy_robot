"""
TODO: You can either work from this skeleton, or you can build on your solution for Toy Robot 2 exercise.
"""
def globals():
    # list of valid command names
    global valid_commands
    valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint', 'replay', 'replay silent', "replay reversed", "replay reversed silent"]
    global command_list
    command_list = []
    # valid_flags = ["reversed", "silent"]
    # variables tracking position and direction
    global position_x
    position_x = 0
    global position_y
    position_y = 0
    global directions
    directions = ['forward', 'right', 'back', 'left']
    global current_direction_index
    current_direction_index = 0

    # area limit vars
    global min_y, max_y, min_x, max_x
    min_y, max_y = -200, 200
    min_x, max_x = -100, 100


def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name

def arrange_command(command):
    """
    Changes the arrangement of and replay commands to make the esier to handle.
    """
    command1 = command.split()
    i = 0
    command = command.lower()
    while i <= len(list(command)):
        temp = list()
        if command.count("replay") != 0:
            temp.append("replay")
            i += 1
        if command.count("reversed") != 0:
            temp.append("reversed")
            i += 1
        if command.count("silent") != 0:
            temp.append("silent")
            i += 1
        i += 1
    for j in range(len(command1)):
            if command1[j].isdecimal() or command1[j].split()[0].isdigit() and command1.split()[-1].isdigit():
                temp.append(command1[j])
    command = " ".join(temp)
    return command


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    temp = command.split()
    if command.count("replay") and command.count(",") == 0:
        command = arrange_command(command)
    if command.count("replay") != 1 or command == "off" or command.count(",") > 0:
        while len(command) == 0 or not valid_command(command) or command.count(",") > 0:
            output(robot_name, "Sorry, I did not understand '"+command+"'.")
            command = input(prompt)
        track_commands(command.lower())
    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """
    (command_name, arg1) = split_command_input(command)
    check_int = command.split()
    if command.count(",") >= 1:
        return False
    if command.lower() == "replay" or command.lower() == "replay reversed" or command.lower() == "replay silent" or command.lower() == "replay reversed silent" and check_int[-1] == int(): #or len(check_int) == 2:
        return True
    return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1))# or str(arg1) == "silent" or str(arg1) == "reversed" or command == "replay reversed silent"


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY  - replays a set of commands
REPLAY SILENT  - replays commands silently
REPLAY REVERSED - replays commands in revers order
"""


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """

    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def track_commands(command):
    """
    Tracks the history of previous commands and adds them to a list,
    excluding any replay, help and off commands.
    """
    if command.count("replay") == 0 and command != "help" and command != "off":
        command_list.append(command)
    return command_list

def arrange_command_list(command):
    """
    Rearanges the command list I will run with my replay command accordingly
    """
    temp = list()
    if command.isdigit():
        i = len(command_list) - int(command)
        while i <= len(command_list) - 1:
            temp.append(command_list[i])
            i += 1
    return temp


def do_replay(robot_name, command, command_list):
    """
    The replay command
    """
    useable_command = command_list
    if command.split()[-1].isdigit() or command.split()[-1].split()[-1].isdigit():
        useable_command = arrange_command_list(command.split()[-1])
    reverse = ""
    silent = ""
    if command.count("reversed") == 1:
        reverse = " in reverse"
        useable_command.reverse()
    if command.count("silent") == 0:
        for i in range(len(useable_command)):
            handle_command(robot_name, useable_command[i])
    else:
        silent = " silently"
        for i in range(len(useable_command)):
            step_holder = useable_command[i].split()
            if useable_command[i] == "left":
                do_left_turn(robot_name)
            elif useable_command[i] == "right":
                do_right_turn(robot_name)
            else:
             update_position(int(step_holder[1]))
    return True, ' > ' + robot_name + ' replayed ' + str(len(useable_command)) + ' commands' + reverse + silent + '.'


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """
    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        (do_next, command_output) = False, f"{robot_name}: Shutting down.." 
    elif command_name == 'help':
        (do_next, command_output) = do_help()
    elif command_name == 'forward':
        (do_next, command_output) = do_forward(robot_name, int(arg))
    elif command_name == 'back':
        (do_next, command_output) = do_back(robot_name, int(arg))
    elif command_name == 'right':
        (do_next, command_output) = do_right_turn(robot_name)
    elif command_name == 'left':
        (do_next, command_output) = do_left_turn(robot_name)
    elif command_name == 'sprint':
        (do_next, command_output) = do_sprint(robot_name, int(arg))
    elif command_name == 'replay' or command == "replay silent" or command == "replay reversed":
        (do_next, command_output) = do_replay(robot_name, command, command_list)
    print(command_output)
    if command != "off":
        show_position(robot_name)
    return do_next


def robot_start():
    """This is the entry point for starting my robot"""

    global position_x, position_y, current_direction_index, command_list
    globals()
    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")

    position_x = 0
    position_y = 0
    current_direction_index = 0

    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)

if __name__ == "__main__":
    robot_start()
