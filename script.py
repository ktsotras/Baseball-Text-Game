import random
import os
from symbol import single_input
from num2words import num2words

again = 'y'
def play_inning(game_state):
    game_state['top_of_inning'] = True
    while game_state['outs'] < 3:
        at_bat(game_state)
        game_state['balls'] = 0
        game_state['strikes'] = 0
    game_state['outs'] = 0
    game_state['numrunners'] = 0
    game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = False, False, False
    game_state['temp'] = ''
    game_state['top_of_inning'] = False
    while game_state['outs'] < 3:
        at_bat(game_state)
        game_state['balls'] = 0
        game_state['strikes'] = 0
    game_state['outs'] = 0
    game_state['numrunners'] = 0
    game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = False, False, False
    game_state['temp'] = ''

def move_runners(game_state, bases):
    if bases == 0:
        if game_state['numrunners'] == 0:
            game_state['firstbase'] = True
            game_state['numrunners'] = 1
        elif game_state['numrunners'] == 1:
            if game_state['firstbase'] == True:
                game_state['secondbase'] == True
            game_state['numrunners'] = 2
        elif game_state['numrunners'] == 2:
            game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = True, True, True
            game_state['numrunners'] = 3
        elif game_state['numrunners'] == 3:
            add_runs(game_state, 1)
    if bases == 1:
        if game_state['numrunners'] == 0:
            game_state['numrunners'] = 1
        elif game_state['numrunners'] == 1:
            if game_state['thirdbase']:
                add_runs(game_state, 1)
                game_state['thirdbase'] = False
            elif game_state['secondbase']:
                game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = True, False, True
                game_state['numrunners'] = 2
            else:
                game_state['secondbase'] = True
                game_state['numrunners'] = 2
        elif game_state['numrunners'] == 2:
            if game_state['thirdbase'] and game_state['secondbase']:
                game_state['secondbase'] = False
                game_state['numrunners'] = 2
                add_runs(game_state, 1)
            elif game_state['thirdbase'] and game_state['firstbase']:
                game_state['secondbase'], game_state['thirdbase'] = True, False
                game_state['numrunners'] = 2
                add_runs(game_state, 1)
            else:
                game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = True, True, True
                game_state['numrunners'] = 3
        else:
            add_runs(game_state, 1)
        game_state['firstbase'] = True
    if bases == 2:
        if game_state['numrunners'] == 1:
            if game_state['thirdbase'] or game_state['secondbase']:
                game_state['secondbase'], game_state['thirdbase'] = True, False
                game_state['numrunners'] = 1
                add_runs(game_state, 1)
            else:
                game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = False, True, True
                game_state['numrunners'] = 2
        elif game_state['numrunners'] == 2:
            if game_state['thirdbase'] and game_state['secondbase']:
                game_state['thirdbase'] = False
                game_state['numrunners'] = 1
                add_runs(game_state, 2)
            elif game_state['thirdbase'] and game_state['firstbase']:
                game_state['secondbase'], game_state['firstbase'] = True, False
                game_state['numrunners'] = 2
                add_runs(game_state, 1)
            else:
                game_state['thirdbase'], game_state['firstbase'] = True, False
                game_state['numrunners'] = 2
                add_runs(game_state, 1)
        elif game_state['numrunners'] == 3:
            game_state['firstbase'] = False
            game_state['numrunners'] = 2
            add_runs(game_state, 2)
        else:
            game_state['secondbase'] = True
            game_state['numrunners'] = 1
                
    if bases == 3:
        add_runs(game_state, game_state['numrunners'])
        game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = False, False, True
        game_state['numrunners'] = 1
    if bases == 4:
        add_runs(game_state, 1+game_state['numrunners'])
        game_state['firstbase'], game_state['secondbase'], game_state['thirdbase'] = False, False, False
        game_state['numrunners'] = 0


def add_runs(game_state, runs):
    if game_state['top_of_inning']:
        game_state['away_score'] += runs
    else:
        game_state['home_score'] += runs


def at_bat(game_state):
    result = ''
    while result != 'out':
        input()
        display(game_state)
        pitch = ''
        if game_state['top_of_inning']:
            location = input("Where do you want to pitch the ball? ").upper()
            if location != 'OZ':
                pitch = input("Which type of pitch do you want to throw? ").upper()
        else:
            location = input("Where do you want to aim the bat? ").upper()
            if location == 'NS':
                location = 'OZ'
            else:
                pitch = input("Which type of pitch do you expect? ").upper()  
        result = outcome(pitch, location, generate_computer_choice())
        game_state['temp'] = result
        if result == 'strike':
            game_state['strikes'] += 1
        elif result == 'foul':
            if game_state['strikes'] < 2:
                game_state['strikes'] += 1
        elif result == 'ball':
            game_state['balls'] += 1

        if game_state['strikes'] == 3 or result == 'out':
            game_state['outs'] += 1
            return
        elif game_state['balls'] == 4:
            move_runners(game_state, 0)
            return
        elif result == 'single':
            move_runners(game_state, 1)
            return
        elif result == 'double':
            move_runners(game_state, 2)
            return
        elif result == 'triple':
            move_runners(game_state, 3)
            return
        elif result == 'homerun':
            move_runners(game_state, 4)
            return

def generate_computer_choice():
    rand_pitch = random.randrange(1,100)
    if rand_pitch < 51:
        com_pitch = 'FB'
    elif rand_pitch < 71:
        com_pitch = 'CU'
    elif rand_pitch < 86:
        com_pitch = 'CR'
    else:
        com_pitch = 'SL'

    rand_location = random.randrange(1,50)
    if rand_location < 11:
        com_location = 'UI'
    elif rand_location < 21:
        com_location = 'UA'
    elif rand_location < 31:
        com_location = 'DI'
    elif rand_location < 41:
        com_location = 'DA'
    else:
        com_location = 'OZ'

    return com_pitch, com_location

def outcome(pitch, location, computer):
    print(computer)
    com_p = computer[0]
    com_l = computer[1]
    print(com_p)
    print(com_l)
    common_location = len(''.join(set(location).intersection(com_l)))
    print(common_location)
    if location == 'OZ':
        if com_l == 'OZ':
            return 'ball'
        else:
            return 'strike'
    elif com_l == 'OZ':
        return 'strike'
    contact = random.randrange(1,100)
    if pitch == com_p:
        if location == com_l:
            if contact < 26:
                return 'homerun'
            elif contact < 56:
                return 'double'
            elif contact < 86:
                return 'single'
            elif contact < 91:
                return 'triple'
            else:
                return 'foul'
        else:
            if common_location == 1:
                if contact < 11:
                    return 'homerun'
                elif contact < 26:
                    return 'double'
                elif contact < 56:
                    return 'single'
                elif contact < 59:
                    return 'triple'
                elif contact < 91:
                    return 'foul'
                else:
                    return 'out'
            else:
                if contact < 6:
                    return 'homerun'
                elif contact < 14:
                    return 'double'
                elif contact < 26:
                    return 'single'
                elif contact < 66:
                    return 'foul'
                elif contact < 86:
                    return 'strike'
                else:
                    return 'out'
    else:
        if location == com_l:
            if contact < 15:
                return 'homerun'
            elif contact < 31:
                return 'double'
            elif contact < 51:
                return 'single'
            elif contact < 81:
                return 'foul'
            elif contact < 83:
                return 'triple'
            elif contact < 93:
                return 'strike'
            else:
                return 'out'
        else:
            if common_location == 1:
                if contact < 10:
                    return 'homerun'
                elif contact < 24:
                    return 'double'
                elif contact < 41:
                    return 'single'
                elif contact < 75:
                    return 'foul'
                elif contact < 87:
                    return 'strike'
                else:
                    return 'out'
            else:
                if contact < 1:
                    return 'homerun'
                elif contact < 5:
                    return 'double'
                elif contact < 18:
                    return 'single'
                elif contact < 26:
                    return 'foul'
                elif contact < 76:
                    return 'strike'
                else:
                    return 'out'

def num_runners(game_state):
    game_state['numrunners'] = sum([game_state['firstbase'], game_state['secondbase'], game_state['thirdbase']])

def display(game_state):
    os.system('cls' if os.name == 'nt' else 'clear')
    if game_state['top_of_inning']:
        action = 'pitching.'
        half = 'top'
    else:
        action = 'batting.'
        half = 'bottom'

    print('It is the ' + half +' of the ' + num2words(game_state['cur_inning'], to="ordinal_num") + '. You are ' + action)
    num_runners(game_state)
    if game_state['numrunners'] == 1:
        if game_state['firstbase']:
            print('Runner on first')
        elif game_state['secondbase']:
            print('Runner on second')
        else:
            print('Runner on third')
    elif game_state['numrunners'] == 2:
        if game_state['firstbase'] and game_state['secondbase']:
            print('Runners on first and second')
        elif game_state['firstbase'] and game_state['thirdbase']:
            print('Runners on the corners')
        elif game_state['thirdbase'] and game_state['secondbase']:
            print('Runners on second and third')
    elif game_state['numrunners'] == 3:
        print('Bases loaded')
    else:
        print('Bases empty')
    print(game_state['away_team'].title() + ': ' + str(game_state['away_score']))
    print(game_state['home_team'].title() + ': ' + str(game_state['home_score']))
    print('B: ' + str(game_state['balls']) + '  S: ' + str(game_state['strikes']) + '  O: ' + str(game_state['outs']))
    print(f"""                                                    
                                 ▄█▌                   
                                 ┌ █                    
                 ▄ ▀▀▀▌          █                      
                █      ▌        ▄ ▌                     {game_state['temp']}
               ▄      ▌`       ▐ █                      
            ▄▄       █         ██                       
         ,▄       █▀`         ▓█                        
        ▄                    ▐                          
      ╔█           ▌         █`                         
     ▄             █        ▐▀                          
    ┌               ▌▄,,╓▄▄█    |--------|--------|                 |-----------------|   
   ▄█                       ▌   |        |        |                 | Pitch Key       |
  ▐             ▌ ▀█   █▄█ █    |   Up   |   Up   |                 | --------------- |
 ▄█            █    ▀▀█   █`    |   In   |  Away  |                 | FB - Fastball   |  
▐           █'▀          ▀      |        |        |                 | CU - Change up  |
▐           ▌                   |--------|--------|                 | CR - Curveball  |    
 █          █,                  |        |        |                 | SL - Slider     |
  '▀          ▌                 |  Down  |  Down  |                 |-----------------|      
     ▀         █                |   In   |  Away  |                       
       ▀         ,              |        |        |                        
         ▀                      |--------|--------|                        
         ▄        ▌                                      
        ▐        ▀                                
        ▐      █▀   Use 'NS' to not swing the bat and take the pitch.                                     
        /     ▀                                         
       ▐     ▀  Use 'OZ' to throw outside the strikezone. Impossible for batter to hit.                                            
       ▐....▀    
    Type the first letter of each word for location(UI, DA, etc.)""")


def welcome():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('BBB     A     SSS   EEEEE  BBB     A    L      L')
    print('B  B   A A   S      E      B  B   A A   L      L')
    print('BBB   A   A   SSS   EEEEE  BBB   A   A  L      L')
    print('B  B  AAAAA      S  E      B  B  AAAAA  L      L')
    print('BBB   A   A   SSS   EEEEE  BBB   A   A  LLLLL  LLLLL')
    print()
    print('This is a text based Baseball game that is three innings long.')
    print('When pitching you can choose which pitch type and location. \nWhen batting you can choose whether to swing and if so where.')
    print()

def play(game_state):
    print('You are the home team.')
    game_state['home_team'] = input("What is the name of the Home team? ")
    game_state['away_team'] = input("What is the name of the Away team? ")

    while game_state['cur_inning'] < 4:
        play_inning(game_state)
        game_state['cur_inning'] += 1 
    os.system('clear')
    print('This is the end of the game!')
    if game_state['home_score'] == game_state['away_score']:
        print('Huh, I guess you can have a tie in baseball.')
    elif game_state['home_score'] > game_state['away_score']:
        print('You Won!')
    else:
        print('You Lost.')
    print(game_state['away_team'].title() + ': ' + str(game_state['away_score']))
    print(game_state['home_team'].title() + ': ' + str(game_state['home_score']))
 

while again == 'y':
    os.system('clear')
    welcome()
    game_state = {'home_score': 0, 'away_score': 0, 'home_team': '', 'away_team': '', 'cur_inning': 1, 'top_of_inning': True, 'balls': 0, 'strikes': 0, 'outs': 0, 'firstbase': False, 'secondbase': False, 'thirdbase': False, 'numrunners': 0, 'temp': ''}
    play(game_state)
    again = input('Do you want to play again? y/n: ').lower()

print()
print('Goodbye!')
exit()