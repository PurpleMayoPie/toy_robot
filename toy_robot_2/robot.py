
# global command_list
# command_list = []
# global coordinates_global
# coordinates_global = [0,0]


"""Allowing the robot to be named"""
def name_toy_robot():
    name = input("What do you want to name your robot? ")
    print(name, end = ":")
    print(" Hello kiddo!")
    return name


def print_to_user(command, name, command_list, coordinates_global):
    robot_position = track_coordinates(command, command_list, coordinates_global)
    # print(robot_position, "print")
    if command == "help":
         print("\n".join(help_command(name)))
    if robot_position == False:
        print(name + ": Sorry, I cannot go outside my safe zone.")
        print(" > " + name + " now at position " + "(" + str(coordinates_global[0]) + "," + str(coordinates_global[1]) + ").")
    else:
        if command[0].casefold() == "forward":
                print("\n".join(forward_command(command, name)))
        elif command[0].casefold() == "back":
                print("\n".join(back_command(command, name)))
        elif command[0].casefold() == "left":
                print(" > " + name + " turned left.")
        elif command[0].casefold() == "right":
                print(" > " + name + " turned right.")
        elif command[0].casefold() == "sprint" and command[1] != "0":
            new_command = ["forward", command[1]]
            print("\n".join(forward_command(new_command, name)))
            command[1] = str(int(command[1]) - 1)
            new_command[1] = command[1]
            return print_to_user(command, name, command_list, coordinates_global)
            

        if str(command).casefold() != "help" and str(command).casefold() != "off":  
            print(" > " + name + " now at position " + "(" + str(robot_position[0]) + "," + str(robot_position[1]) + ").")


def command_history(command, command_list):
    command_list.append(command)
    return command_list

"""Give the robot something to do"""
def robot_command(name, command_list, coordinates_global):
    print(name, end = ":")
    command = input(" What must I do next? ")
    command_list = command_history(command, command_list)
    movement = command.split()
    if command.casefold() == "off":
        print(name, end = ":")
        print(" Shutting down..")
    elif command.casefold() == "help":
         print_to_user("help", name, command_list, coordinates_global)
         robot_command(name, command_list, coordinates_global)

  
    elif movement[0].casefold() == "forward":
         print_to_user(movement, name, command_list, coordinates_global)
         robot_command(name, command_list,  coordinates_global)

    elif movement[0].casefold() == "back":
         print_to_user(movement, name, command_list, coordinates_global)
         robot_command(name, command_list, coordinates_global)

    elif movement[0].casefold() == "right":
         print_to_user(movement, name, command_list, coordinates_global)
         robot_command(name, command_list, coordinates_global)

    elif movement[0].casefold() == "left":
         print_to_user(movement, name, command_list,  coordinates_global)
         robot_command(name, command_list, coordinates_global)
    elif movement[0].casefold() == "sprint":

        print_to_user(movement, name, command_list, coordinates_global)
        robot_command(name, command_list, coordinates_global)
    else:
        print(name, end = ":")
        print(" Sorry, I did not understand", "'" + command +"'.")
        robot_command(name, command_list, coordinates_global)

def help_command(name):
    possible_commands =["I can understand these commands:" , "OFF  - Shut down robot", "HELP - provide information about commands",
"FORWARD - Move robot forward", "BACK - move toy robot back by set steps.", "RIGHT - turn robot right.", "LEFT - turn robot left",
"SPRINT - run forward"] 
    return possible_commands



def forward_command(movement, name):
    command = [" > " + name + " moved forward by " + movement[1] + " steps."]
    return command

def sprint_command(command, name ,command_list, coordinates_global):
    new_command = ["forward", command[1]]
    print(new_command)
    coordinates_global =  track_coordinates(new_command, command_list, coordinates_global)
    if coordinates_global == False:
        return False
    command[1] = str(int(command[1]) - 1)
    print(command[1])
    return print_to_user(command, name, command_list, coordinates_global)

def back_command(movement, name):
    command = [" > " + name+ " moved back by " + movement[1] + " steps."]
    return command



def track_coordinates(command, command_list, coordinates_global):
    coordinates = [0,0]
    coordinates[0] = coordinates_global[0]
    coordinates[1] = coordinates_global[1]
    if command[0] == "sprint":
        command = ["forward", command[1]]
    if command_list.count("right") == command_list.count("left"):
        if command[0].casefold() == "forward":
            coordinates[1] = coordinates[1] + int(command[1])
        if command[0].casefold() == "back":
            coordinates[1] = coordinates[1] - int(command[1])
    elif command_list.count("right") == 1 or command_list.count("left") == 3:
        if command[0].casefold() == "forward":
            coordinates[0] = coordinates[0] + int(command[1])
        elif command[0].casefold() == "back":
            coordinates[0] = coordinates[0] - int(command[1])
    elif command_list.count("left") == 1 or command_list.count("right") == 3:
        if command[0].casefold() == "forward":
            coordinates[0] = coordinates[0] - int(command[1])
        elif command[0].casefold() == "back":
            coordinates[0] = coordinates[0] + int(command[1])
    elif command_list.count("left") == 2 or command_list.count("right") == 2:
        if command[0].casefold() == "forward":
            coordinates[1] = coordinates[1] - int(command[1])
        if command[0].casefold() == "back":
            coordinates[1] = coordinates[1] + int(command[1])

    if coordinates[0] > -100 and coordinates[0] < 100 and coordinates[1] > -200 and coordinates[1] < 200:
        coordinates_global[0] = coordinates[0]
        coordinates_global[1] = coordinates[1]
        return coordinates_global
        
    else:
        return False



def robot_start():
    """This is the entry function, do not change"""
    name = name_toy_robot()
    robot_command(name, [], [0,0])
    pass


if __name__ == "__main__":
    robot_start()
