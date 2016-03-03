import sys

board = []

row_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
col_label = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for x in range(10):
    board.append(["O"] * 10)
    
def print_board(board):
    x = 0
    print "   " + "  ".join(col_label)
    for row in board:
        print row_label[x] + "  " + "  ".join(row)
        x += 1

def start_game():
    while True:
        print "\nWelcome to Battleship! Prepare to die.\n"
        choice = raw_input("Enter A for Attack mode, D for Defend mode, \
or Q to quit: ")
        if choice.upper() == 'A':
            attack()
            break
        elif choice.upper() == 'D':
            defend()
            break
        elif choice.upper() == 'Q':
            sys.exit()
        else:
            print "Please enter A or D"
            continue

    
        
def defend_placement():
    #This method will take ship placements from Defender and validate placement of ships
    all_ships_placed = False
    carrier_placed = False
    sub_placed = False
    patrol_placed = False
    
    print """
Please place one of each ship:
A to place Aircraft Carrier
S to place Submarine
P to place Patrol Boat 
"""
    while all_ships_placed == False:
    # Lets user input ships until one of each has been placed    
        ship = raw_input("Please enter ship type: ")
        if ship.upper() == 'A':
            if carrier_placed == False:
                while True:
                    direction = raw_input("Please enter H for horizontal positioning or V for vertical ship positioning: ")
                    
                #check positon, place carrier
                carrier_placed = True
            else:
                print "Aircraft Carrier already placed! Try another."
        elif ship.upper() == 'S':
            if sub_placed == False:
                #check positon, place carrier
                sub_placed = True
            else:
                print "Submarine already placed! Try another."
        elif ship.upper() == 'P':        
            if patrol_placed == False:
                #check positon, place carrier
                patrol_placed = True
            else:
                print "Patrol Boat already placed! Try another."
        else:
            print "Please choose A, S, or P"
            continue
        all_ships_placed = carrier_placed and sub_placed and patrol_placed
                
            





start_game()
print_board(board)
