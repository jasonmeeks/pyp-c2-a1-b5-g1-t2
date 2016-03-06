import os
import random
import sys
import collections

# This doesn't work on cloud9 but works locally
output_to_text = False
if output_to_text:
    orig_stdout = sys.stdout
    f = file('out.txt', 'w')
    sys.stdout = f

board = []

row_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
col_label = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

"""
This is the nested dictionary where we store all the data on each ship. Here
we will store name, size, if the ship is placed, how many hits it has, and
if it is sunk. As a ship gets hit, we will increment 'hits' and check if 
'hits' == 'size'. When that is true, we set 'is_sunk' to True.
"""

ship_info = {
            "A" : {'name': "Aircraft Carrier", 'size': 5, 'hits': 0, 'is_placed': False, 'is_sunk': False},
            "B" : {'name': "Battleship", 'size': 4, 'hits': 0, 'is_placed': False, 'is_sunk': False},
            "C" : {'name': "Cruiser", 'size': 3, 'hits': 0, 'is_placed': False, 'is_sunk': False},
            "S" : {'name': "Submarine", 'size': 3, 'hits': 0, 'is_placed': False, 'is_sunk': False},
            "D" : {'name': "Destroyer", 'size': 2, 'hits': 0, 'is_placed': False, 'is_sunk': False}
            }
            
statistics = {
             'hits': 0,
             'misses': 0,
             'total_guesses' : 0,
             'prev_guess' : "",
             'hit_streak' : 0,
             'biggest_hit_streak' : 0,
             'miss_streak' : 0,
             'biggest_miss_streak' : 0,
             'ships_destroyed': 0,
             'times_cheated' : 0
             }

ai_targetting = {
                "last_hit_coord": "",
                "ship": "",
                "left": True,
                "right": True,
                "up": True,
                "down": True,
                "guess_dir": "",
                "aim_radius": 1,
                "dir_count": 0,
                "aim_tries": 0
               } 


for x in range(10):
    board.append(["-"] * 10)
    
def print_board(board):
    x = 0
    print "   " + "  ".join(col_label)
    for row in board:
        print row_label[x] + "  " + "  ".join(row)
        x += 1
    print ""
    
def print_statistics():
    percentage = (float(statistics['hits']) / statistics['total_guesses']) * 100
    print "\nGame Statistics:"
    print "Hits:                 " + str(statistics['hits'])
    print "Misses:               " + str(statistics['misses'])
    print "Total Guesses:        " + str(statistics['total_guesses'])
    print "Percentage Hit:       " + str(round(percentage, 2)) + "%"
    print "Biggest Hit Streak:   " + str(statistics['biggest_hit_streak'])
    print "Biggest Miss Streak:  " + str(statistics['biggest_miss_streak'])
    print "Ships Destroyed:      " + str(statistics['ships_destroyed'])
    print "Times Cheated:        " + str(statistics['times_cheated'])


def get_ship_orientation():
# Gets ship orientation input
    while True:
        print "\nShip orientation options:\
            \nH for Horizontal\
            \nV for Vertical\
            \nG to see Game Board\n"
        orientation = (raw_input("Please choose orientation of the ship: ")).upper()
        if orientation == "G":
            print_board(board)
            continue
        elif orientation == "H":
            print "Horizontal ship orientation selected"
            return orientation           
        elif orientation == "V":
            print "Vertical ship orientation selected"
            return orientation
        else:
            print "\nPlease choose H or V"
            continue

        
def get_ship_coordinate(orientation):
# Gets ship coordinate as input
    while True:
        print "\nEnter a coordinate for row A-J and column 1-10:\
            \nExample: 'A4'\
            \nEnter 'G' to see Game Board\n"
        if orientation == "H":
            coordinate = (raw_input("\nEnter the left-most coordinate of the ship: ")).upper()
        elif orientation == "V":
            coordinate = (raw_input("\nEnter coordinate for the top of the ship: ")).upper()
        if orientation == "G":
            print_board(board)
            continue
        else:
            row, col = coordinate[0], coordinate[1:]
            # Check if row and column are in our row and column label list
            if row in row_label and col in col_label:
                print "Coordinate " + coordinate + " selected.\n"
                return coordinate
            else:
                print "Coordinate invalid. Try again.\n"
                continue
        

def check_boundaries(ship_letter, orientation, coordinate):
# Make sure the ship fits in boundries of game board
    # Split coordinate in to row and column data
    row, col = coordinate[0], coordinate[1:]
    # Match the coordinate info with row and column index in grid
    row_index = row_label.index(row)
    col_index = col_label.index(col)
    # Make sure the ship size + row/column index don't exceed gameboard length
    if orientation == "H":
        if col_index + ship_info[ship_letter]['size'] > len(col_label):
            return False
        return True
    elif orientation == "V":
        if row_index + ship_info[ship_letter]['size'] > len(row_label):
            return False
        return True
    return None # error case
    
    
def space_available(ship_letter, orientation, coordinate):
    # Split coordinate in to row and column data
    row, col = coordinate[0], coordinate[1:]
    # Match the coordinate info with row and column index in grid
    row_index = row_label.index(row)
    col_index = col_label.index(col)
    # Check if all the spaces you are trying to place in are still empty "-"s
    if orientation == "H":
        for x in range(ship_info[ship_letter]['size']):
            if board[row_index][col_index + x] != "-":
                return False
        return True
    elif orientation == "V":
        for x in range(ship_info[ship_letter]['size']):
            if board[row_index + x][col_index] != "-":
                return False
        return True
    return None # error case
    

def place_ship(ship_letter, orientation, coordinate):
# Place ship letter on game board
    # Split coordinate in to row and column data
    row, col = coordinate[0], coordinate[1:]
    # Match the coordinate info with row and column index in grid
    row_index = row_label.index(row)
    col_index = col_label.index(col)
    # Replace each "-" with the ship letter provided
    if orientation == "H":
        for x in range(ship_info[ship_letter]['size']):
            board[row_index][col_index + x] = ship_letter
    elif orientation == "V":
        for x in range(ship_info[ship_letter]['size']):
            board[row_index + x][col_index] = ship_letter


def get_rand_orientation():    
    orientation = random.choice( ['H', 'V'] )
    return  orientation

 
def get_rand_ship():
    while True:
        ship_letter = random.choice( ['A', 'B', 'C', 'S', 'D'] )
        if ship_info[ship_letter]['is_placed'] == False:
            return ship_letter
        else:
            continue

   
def get_rand_coord():
    # THis will be used to get random coordinates 
    row_coord = chr(random.randrange(97,107)).upper()
    col_coord = str(random.randint(1,10))
    return row_coord + col_coord
 

def reset_aim():
    # This resets the aim after the last hit has been exhausted
    ai_targetting['last_hit_coord'] = ""
    ai_targetting['ship'] = ""
    ai_targetting['left'] = True
    ai_targetting['right'] = True
    ai_targetting['up'] = True
    ai_targetting['down'] = True
    ai_targetting['guess_dir'] = ""
    ai_targetting['dir_count'] = 0
    ai_targetting['aim_radius'] = 1


def check_aim():
    # Check to see if there are still directions that haven't been misses
    if ai_targetting['left'] or ai_targetting['right'] or ai_targetting['up'] or ai_targetting['down']:
        return True
    return False


def check_edge_case(row_index, col_index):
    # This checks for an error where it tries to guess out of bounds
    if ((ai_targetting['guess_dir'] == 'left' and col_index == 0) or 
    (ai_targetting['guess_dir'] == 'right' and col_index == (len(col_label) - 1)) or 
    (ai_targetting['guess_dir'] == 'up' and row_index == 0) or 
    (ai_targetting['guess_dir'] == 'down' and row_index == (len(row_label) - 1))):
        return True
    else:
        return False


def ai_aimed_coord(direction):
    """ 
    If we have a hit, the AI starts on that coordinate and exhausts all outward directions
    until miss or out of bounds. This code receives the direction and the radius
    and checks to see if the next target is in the boundary. If it is not, it stops looking
    in that direction
    """
    row, col = ai_targetting['last_hit_coord'][0], ai_targetting['last_hit_coord'][1:]
    row_index = row_label.index(row)
    col_index = col_label.index(col)
    in_bounds = False
    if ai_targetting[direction] == True:
        ai_targetting['guess_dir'] = direction
        if direction == 'up':
            row_aimed = row_index - ai_targetting['aim_radius']
            if row_aimed < len(row_label):
                in_bounds = True
                coordinate = row_label[row_aimed] + col_label[col_index]
            else:
                ai_targetting[direction] = False
        elif direction == 'down':
            row_aimed = row_index + ai_targetting['aim_radius']
            if row_aimed < len(row_label):
                in_bounds = True
                coordinate = row_label[row_aimed] + col_label[col_index]
            else:
                ai_targetting[direction] = False
        elif direction == 'right':
            col_aimed = col_index + ai_targetting['aim_radius']
            if col_aimed < len(col_label):
                in_bounds = True
                coordinate = row_label[row_index] + col_label[col_aimed]
            else:
                ai_targetting[direction] = False
        elif direction == 'left':
            col_aimed = col_index - ai_targetting['aim_radius']
            if col_aimed < len(col_label):
                in_bounds = True
                coordinate = row_label[row_index] + col_label[col_aimed]
            else:
                ai_targetting[direction] = False
        if in_bounds:
            # print "Hit coordinate:     " + ai_targetting['last_hit_coord']
            # print "Guessing direction: " + direction
            # print "Target coordinate:  " + coordinate
            # print "Aiming left:  " + str(ai_targetting['left'])
            # print "Aiming right: " + str(ai_targetting['right'])
            # print "Aiming up:    " + str(ai_targetting['up'])
            # print "Aiming down:  " + str(ai_targetting['down'])
            return coordinate



def ai_get_coord():
    """
    If there is a hit, uses AI targetting for next coordinate. Otherwise, generate random coordinate

    This AI takes the coordinate of the first hit, and goes outward in each direction one at a time until
    it encounters a miss in that direction. It keeps going until all directions hit miss or boundary.
    """
    aim_tries = 0
    directions = ['left', 'right', 'up', 'down']
    while True:
        # If there was a hit and not all directions have been exhausted( encounted a miss)
        if ai_targetting['last_hit_coord'] != "" and check_aim():
            coordinate = ai_aimed_coord(directions[ai_targetting['dir_count']])            
            if ai_targetting['dir_count'] < 3:
                ai_targetting['dir_count'] += 1
            else:
                ai_targetting['dir_count'] = 0
                ai_targetting['aim_radius'] += 1
            if not coordinate:
                continue
        else:
            reset_aim()
            coordinate = get_rand_coord()
        row, col = coordinate[0], coordinate[1:]
        row_index = row_label.index(row)
        col_index = col_label.index(col) 
        # If the coordinate is good, return it to program
        if board[row_index][col_index] != "*" and board[row_index][col_index] != "X":
            return coordinate
        # If the target is a miss, stop guessing in that direction
        elif board[row_index][col_index] == "X":
            ai_targetting[ai_targetting['guess_dir']] = False
        # If the target is already hit and the target will be a boundary next, stop this direction
        elif board[row_index][col_index] == "*" and check_edge_case(row_index, col_index):
            ai_targetting[ai_targetting['guess_dir']] = False
        else:
            aim_tries += 1



def not_cheating(coordinate, response):
    # Check if user is cheating and gives wrong response
    sunk = False
    row, col = coordinate[0], coordinate[1:]
    row_index = row_label.index(row)
    col_index = col_label.index(col)  
    # Update hit counter for ship if it is a hit and check to see if sunk
    if board[row_index][col_index] != "-":
        hits = ship_info[board[row_index][col_index]]['hits']
        size = ship_info[board[row_index][col_index]]['size']
        if (hits + 1) == size:
            sunk = True
    if response == "H":
        if board[row_index][col_index] != "-" and not sunk:
            ship_info[board[row_index][col_index]]['hits'] += 1
            return True
        return False
    elif response == "M":
        if board[row_index][col_index] == "-":
            return True
        return False
    elif response == "S":
        if board[row_index][col_index] != "-" and sunk:
            ship_info[board[row_index][col_index]]['hits'] += 1
            ship_info[board[row_index][col_index]]['is_sunk'] = True
            return True
        return False       
    else: # if it receives G or bad input
        return True


def ai_attack(human_response=True):
    # AI guesses coordinates and attacks ships that have been placed
    coordinate = ai_get_coord()
    row, col = coordinate[0], coordinate[1:]
    row_index = row_label.index(row)
    col_index = col_label.index(col)  
    print_board(board)
    while True:
        print "\nComputer: Attacking " + coordinate + "..."
        print "\nHit, Miss, or Sunk?\
            \nH for Hit\
            \nM for Miss\
            \nS for Sunk\
            \nG to see Game Board\n"
        if human_response:
            response = (raw_input("Please choose one: ")).upper()
        else:
            # For AI vs AI mode    
            response = random.choice(['H', 'M', 'S'])
        not_cheater = not_cheating(coordinate, response)
        if not not_cheater:
            statistics['times_cheated'] += 1
            print "\nSTOP CHEATING SCRUB!!!"
        if response == "G":
            print_board(board)
            continue
        # Update statistics and gameplay for a hit
        elif response == "H":
            if not_cheater:
                print ship_info[board[row_index][col_index]]['name'] + " hit!"
                print "\nComputer: YES!!!\n"
                # For the first hit, store the coordinates of the hit for AI targetting
                if ai_targetting['last_hit_coord'] == "":
                    ai_targetting['last_hit_coord'] = coordinate
                board[row_index][col_index] = "*"
                statistics['hits'] += 1
                statistics['miss_streak'] = 0
                statistics['total_guesses'] += 1
                if statistics['prev_guess'] == "H" or statistics['prev_guess'] == "S":
                    statistics['hit_streak'] +=1
                    if statistics['hit_streak'] > statistics['biggest_hit_streak']:
                        statistics['biggest_hit_streak'] = statistics['hit_streak']
                statistics['prev_guess'] = "H"
                break
            else:
                continue
        # Update statistics and gameplay for a miss
        elif response == "M":
            if not_cheater:
                print "\nComputer: I missed? :( \n"
                # For a miss, if AI targetting is on, stop looking in directions that are misses
                if ai_targetting['last_hit_coord'] != "":
                    ai_targetting[ai_targetting['guess_dir']] = False
                board[row_index][col_index] = "X"
                statistics['misses'] += 1
                statistics['total_guesses'] += 1
                statistics['hit_streak'] = 0
                if statistics['prev_guess'] == "M":
                    statistics['miss_streak'] +=1
                    if statistics['miss_streak'] > statistics['biggest_miss_streak']:
                        statistics['biggest_miss_streak'] = statistics['miss_streak']
                statistics['prev_guess'] = "M"
                break
            else:
                continue
        # Update statistics and gameplay when ship is sunk
        elif response == "S":
            if not_cheater:
                print ship_info[board[row_index][col_index]]['name'] + " destroyed!"
                print "\nComputer: KABOOM!\n"
                board[row_index][col_index] = "*"
                statistics['hits'] += 1
                statistics['miss_streak'] = 0
                statistics['total_guesses'] += 1
                statistics['ships_destroyed'] += 1
                if statistics['prev_guess'] == "H" or statistics['prev_guess'] == "S":
                    statistics['hit_streak'] +=1
                    if statistics['hit_streak'] > statistics['biggest_hit_streak']:
                        statistics['biggest_hit_streak'] = statistics['hit_streak']
                statistics['prev_guess'] = "S"
                break
            else:
                continue
        else:
            print "\nPlease enter valid input"
            continue
        

def defend_placement():
    '''
    If they enter a ship, we get the orientation and coordinate, then
    check and make sure it is in the boundary and there is space for
    the ship. If so, place the boat and and update ship count and 
    is_placed for that ship to reflect boat placement.
    
    This is pulling ship_info data from a nested dictionary I made at the 
    top so that we could make the code cleaner (it was really bad w/o it)
    '''    
    ship_count = 0
    # Loop until all 5 ships are placed
    while ship_count < 5:
        print "Please place one of each ship.\
            \nA to place Aircraft Carrier (Size: 5)\
            \nB to place Battleship       (Size: 4)\
            \nC to place Cruiser          (Size: 3)\
            \nS to place Submarine        (Size: 3)\
            \nD to place Destroyer        (Size: 2)\
            \nG to see Game Board\n"         
        ship_letter = (raw_input("Please enter ship type: ")).upper()
        # Print game board if they want it
        if ship_letter == "G":
            print_board(board)
            continue
        elif ship_letter in ship_info:
            if ship_info[ship_letter]['is_placed'] == False:
                while ship_info[ship_letter]['is_placed'] == False:
                    orientation = get_ship_orientation()
                    coordinate = get_ship_coordinate(orientation)
                    boundary_check = check_boundaries(ship_letter, orientation, coordinate)
                    if boundary_check:
                        space_check = space_available(ship_letter, orientation, coordinate)
                        if space_check == False:
                            print "There is already another ship there!\n"
                    else:
                        print "Ship out of bounds.\n"
                    if  boundary_check and space_check:
                        print "Location Valid. Placing ship.\n"
                        place_ship(ship_letter, orientation, coordinate)
                        ship_count += 1
                        ship_info[ship_letter]['is_placed'] = True
                        print "Ship placed!\n"
                        print_board(board)
                    else:
                        print "Location Invalid. Try again.\n"
                        continue
            else:
                print ship_info[ship_letter]['name'] + " already placed! Try another.\n"

        else:
            print "Please choose valid ship option\n"
            continue
    else:
        print "All ships placed correctly! Congratulations!\n"


def attack_placement():
    '''
    The computer will randomly place ships on the board. The user will then enter coordinates
    and attempt to sink all the ships. Once the ships have all be sunk the game will end.
    '''
    
    ship_count = 0
    # Loop until all 5 ships are placed
    while ship_count < 5:
        orientation = get_rand_orientation()
        ship_letter = get_rand_ship()
        coordinate = get_rand_coord()
        boundary_check = check_boundaries(ship_letter, orientation, coordinate)
        if boundary_check:
            space_check = space_available(ship_letter, orientation, coordinate)
        if  boundary_check and space_check:
            place_ship(ship_letter, orientation, coordinate)
            ship_count += 1
            ship_info[ship_letter]['is_placed'] = True
        else:
            continue
    else:
        print "Computer: My ships are in position. Bring it on!\n"
        print_board(board)


def defend():
    # Defend mode game
    game_over = False
    print "\nEntering defend mode...\n"
    defend_placement()
    print "Computer beginning its attack...\n"
    while game_over == False:
        ai_attack()
        for ship in ship_info:
            if ship_info[ship]['is_sunk'] == False:
                break
        else:
            game_over = True
            continue
    else:
        print "\nGame over!\n"
        print ""
        print_board(board)
        print_statistics()
        # sys.exit()

def attack():
    # Attack mode game
    print "\nEntering attack mode...\n"
    attack_placement()

def ai_mode():
    # AI places ships and AI attacks
    # This mode is to look at statistics for AI performance
    # and help debug if necessary
    game_over = False
    human_response = False
    print "\nEntering AI mode...\n"
    attack_placement()
    print "Computer beginning its attack..."
    while game_over == False:
        ai_attack(human_response)
        for ship in ship_info:
            # print ship, ship_info[ship]['is_sunk']
            if ship_info[ship]['is_sunk'] == False:
                break
        else:
            game_over = True
            continue
    else:
        print "\nGame over!\n"
        print ""
        print_board(board)
        print_statistics()
        # sys.exit()    


def start_game():
    # Main game method
    while True:
        print "\nWelcome to Battleship! Prepare to die.\n"
        print "Please choose game mode.\
            \nA for Attack Mode\
            \nD for Defend Mode\
            \nC for Computer Fight\
            \nQ to Quit\n"
        choice = (raw_input("Enter choice: ")).upper()
        if choice.upper() == 'A':
            attack()
            break
        elif choice.upper() == 'D':
            defend()
            break
        elif choice.upper() == 'C':
            ai_mode()
            break
        elif choice.upper() == 'Q':
            sys.exit()
        else:
            print "Invalid choice"
            continue

start_game()

if output_to_text:
    sys.stdout = orig_stdout
    f.close()
