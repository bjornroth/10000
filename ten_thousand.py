import random

# create a roll of n dice
def new_roll(n):
    roll = []
    for i in range(n):
        roll.append(random.randint(1, 6))
    return roll

# check if roll contains points
def legal_roll(roll):
    legal = False
    if 1 in roll or 5 in roll:
        legal = True

    for i in range(1, 7):
        if 3 <= roll.count(i):
            legal = True

    return legal

# calculate points from a roll
def calc_points(calc_roll):
    # make copy so we don't destroy the parameter!
    roll = list(calc_roll)
    points = 0
    while legal_roll(roll):
        # first find triplets
        # iterate backwards so we can delete with impunity
        # we're not using a for loop so we can jump in larger steps
        # when we find a triplet
        i = len(roll) - 1
        while i >= 0:
            if len(roll) >= 3:
                if roll[i] == roll[i-1] == roll[i-2]:
                    if roll[i] == 1:
                        points += 1000
                    else:
                        points += roll[i] * 100
                    del roll[i-2:i+1]
                    i -= 2
            i -= 1
        # now all triplets are found and removed, find
        # single dice points
        # iterate backwards so we can delete with impunity
        for i in range(len(roll) - 1, -1, -1):
            if roll[i] == 1:
                points += 100
                del roll[i]
            elif roll[i] == 5:
                points += 50
                del roll[i]
    return points

# return True if any player is over 10000
def any_player_above_10k(scoreboard):
    return max(scoreboard) > 10000

# play one player
def player_new_roll(kept_dice, score):
    roll_score = score
    keep_rolling = True

    while keep_rolling:
        r = new_roll(6 - len(kept_dice))
        r.sort()
        print("roll: {}".format(r))
        if legal_roll(r):
            legal_choice = False
            kept_temp = []
            while not legal_choice:
                keep = input("Which dice to keep? (dice numbers with space between) ")
                keep_indexes = keep.split(' ')
                keep_indexes = [int(x)-1 for x in keep_indexes]
                for i in keep_indexes:
                    kept_temp.append(r[i])
                if not legal_roll(kept_temp):
                    print("Not valid, try again")
                else:
                    legal_choice = True
            kept_dice += kept_temp
            for i in sorted(keep_indexes, reverse=True):
                del r[i]
            print("Kept: {}".format(kept_dice))
            roll_score += calc_points(kept_temp)
            print("{} = {} points, roll score now {}".format(kept_temp, calc_points(kept_temp), roll_score))
            if len(kept_dice) == 6:
                print("Congrats, roll all dice again!")
                kept_dice = []
            cont = input("Continue rolling {} dice? ".format(6 - len(kept_dice)))
            if cont[0] != 'y':
                return kept_dice, roll_score
        else:
            print("Sorry, no dice valid")
            keep_rolling = False
            kept_dice = []
            roll_score = 0
    return kept_dice, roll_score

# play a round of all players
def play_round(num_players, last_roll, last_score, player_score):
    for player in range(num_players):
        print("== Playing player {}".format(player + 1))
        if last_score > 0 and legal_roll(last_roll):
            yes = input("Do you want to continue on last roll ({} points, {} dice to roll)? ".format(last_score, 6 - len(last_roll)))
            if yes[0] != 'y':
                last_roll = []
                last_score = 0
        last_roll, last_score = player_new_roll(last_roll, last_score)
        player_score[player] += last_score
    return last_roll, last_score

# play the game from beginning
def play_game(num_players, last_roll, last_score, player_score):
    print("Playing with {} players".format(num_players))
    for i in range(num_players):
        player_score.append(0)
    round = 0
    while not any_player_above_10k(player_score):
        round += 1
        print("=== ROUND {} ===".format(round))
        last_roll, last_score = play_round(num_players, last_roll, last_score, player_score)
        print("=== Player scores: {} last score: {}".format(player_score, last_score))

# check which player has most points
def check_winner(scoreboard):
    max_points = 0
    winner_index = -1
    for i in range(0, len(scoreboard)):
        if scoreboard[i] > max_points:
            max_points = scoreboard[i]
            winner_index = i
    return winner_index

player_score_board = []
last_dice_roll = []
last_player_score = 0

number_of_players = input("=== 10000 ===\nHow many players? ")
play_game(int(number_of_players), last_dice_roll, last_player_score, player_score_board)
winner = check_winner(player_score_board)
print("Winner is player {}".format(winner + 1))
