from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a repeated Prisoner's Dilemma. A group of players are randomly matched each cycle. Within each cycle the
  players play an indefinitely repeated prisoners dilemma with a continuation probability.
"""

class Constants(BaseConstants):
    name_in_url = 't7p1'
    players_per_group = 4
    num_rounds = 70
    session_number = 2 # 1,2,3

    instructions_template = 'type_7_p1/Instructions.html'
    
    # Payoff Values
    high_reward = c(29)
    low_reward = c(11)
    effort_cost = c(9)

    # payoff if 1 player defects and the other cooperates
    betray_payoff = high_reward
    betrayed_payoff = low_reward - effort_cost

    # payoff if both players cooperate or both defect
    cooperate_payoff = high_reward - effort_cost
    defect_payoff = low_reward

    # DIE ROLL WAS DETERMINED USING
    # [random.sample(range(1,101),30) for x in range(30)]
    die_dict = {
        1:[[22, 6, 58, 88, 75, 92, 85, 82, 46, 88, 1, 55, 52, 65, 89, 33, 46, 62, 69, 75, 21, 47, 2, 24, 68, 71, 39, 41, 63, 6],
           [31, 33, 67, 85, 26, 90, 100, 99, 50, 88, 20, 6, 66, 32, 31, 77, 94, 24, 26, 9, 98, 32, 100, 39, 39, 59, 31, 18, 38, 4],
           [83, 90, 68, 56, 57, 41, 64, 64, 19, 37, 58, 57, 1, 26, 65, 53, 78, 42, 33, 98, 11, 15, 81, 34, 58, 68, 61, 47, 18, 79],
           [92, 26, 7, 50, 9, 99, 99, 51, 41, 24, 44, 27, 23, 48, 16, 63, 34, 87, 28, 60, 2, 91, 65, 76, 2, 2, 53, 48, 7, 32],
           [70, 29, 1, 4, 34, 75, 95, 23, 90, 17, 16, 73, 60, 17, 58, 1, 15, 3, 41, 94, 18, 92, 75, 56, 61, 47, 19, 12, 74, 90],
           [27, 80, 56, 92, 97, 15, 89, 81, 81, 39, 79, 29, 25, 66, 35, 63, 86, 11, 34, 100, 7, 92, 24, 76, 17, 50, 25, 43, 16, 71],
           [67, 59, 5, 79, 47, 89, 68, 67, 94, 65, 48, 80, 65, 72, 75, 22, 12, 26, 90, 64, 91, 23, 72, 85, 2, 55, 46, 1, 28, 20],
           [91, 42, 88, 69, 7, 52, 98, 73, 93, 49, 12, 51, 91, 19, 7, 56, 49, 88, 14, 79, 13, 3, 72, 93, 85, 62, 21, 85, 35, 42],
           [18, 75, 27, 6, 23, 54, 62, 89, 73, 37, 99, 27, 6, 76, 29, 35, 55, 27, 56, 13, 16, 29, 3, 75, 90, 44, 76, 29, 84, 30],
           [64, 32, 69, 25, 32, 100, 5, 32, 56, 51, 8, 4, 44, 18, 30, 77, 96, 12, 89, 25, 1, 1, 88, 22, 67, 33, 99, 11, 8, 24],
           [20, 71, 52, 41, 48, 87, 10, 74, 63, 26, 11, 43, 41, 10, 92, 73, 26, 7, 50, 17, 9, 44, 81, 95, 33, 45, 58, 8, 6, 79],
           [39, 25, 12, 9, 1, 10, 19, 62, 16, 30, 48, 35, 8, 36, 89, 40, 57, 75, 85, 94, 56, 93, 40, 11, 30, 86, 37, 34, 28, 33],
           [3, 61, 62, 65, 62, 19, 58, 2, 39, 50, 14, 93, 60, 18, 71, 48, 20, 93, 59, 84, 27, 76, 79, 61, 76, 62, 61, 17, 30, 18],
           [30, 3, 43, 33, 1, 92, 61, 70, 65, 67, 55, 56, 64, 19, 45, 61, 43, 4, 8, 59, 72, 52, 19, 22, 70, 74, 50, 91, 12, 80],
           [85, 50, 5, 54, 66, 57, 43, 22, 52, 55, 61, 75, 1, 44, 98, 80, 17, 33, 44, 73, 48, 74, 77, 70, 32, 48, 40, 11, 38, 70],
           [4, 65, 2, 46, 100, 57, 3, 88, 19, 14, 65, 41, 81, 32, 91, 56, 70, 65, 12, 42, 64, 75, 14, 42, 13, 43, 6, 46, 32, 12],
           [76, 79, 44, 78, 17, 83, 17, 99, 83, 66, 76, 83, 70, 83, 55, 28, 58, 79, 94, 83, 35, 75, 46, 9, 46, 56, 17, 57, 51, 58],
           [27, 86, 3, 43, 39, 9, 4, 18, 40, 24, 1, 17, 63, 43, 82, 59, 87, 12, 38, 17, 49, 67, 47, 100, 58, 34, 30, 74, 47, 46],
           [85, 17, 50, 4, 3, 4, 22, 52, 71, 39, 35, 98, 47, 2, 52, 77, 55, 59, 62, 65, 58, 42, 59, 78, 59, 100, 41, 90, 40, 92],
           [74, 73, 64, 9, 92, 54, 34, 21, 18, 66, 21, 74, 61, 94, 26, 34, 2, 86, 19, 37, 61, 1, 6, 42, 21, 76, 91, 22, 88, 56],
           [6, 92, 57, 7, 66, 30, 44, 63, 53, 1, 23, 12, 70, 84, 15, 54, 1, 44, 33, 67, 78, 69, 74, 57, 12, 35, 71, 73, 43, 29],
           [89, 2, 99, 56, 36, 42, 55, 33, 16, 39, 88, 10, 72, 25, 62, 90, 90, 30, 28, 50, 28, 76, 21, 12, 74, 52, 19, 54, 47, 55],
           [60, 85, 37, 85, 7, 38, 24, 67, 40, 79, 96, 85, 19, 20, 96, 82, 27, 19, 30, 8, 12, 61, 3, 43, 77, 43, 42, 89, 72, 72],
           [98, 14, 16, 57, 52, 68, 48, 41, 100, 19, 43, 36, 15, 96, 39, 4, 84, 70, 43, 48, 5, 95, 25, 58, 7, 55, 26, 31, 98, 98],
           [18, 83, 85, 2, 44, 34, 4, 90, 19, 63, 68, 95, 26, 47, 43, 9, 26, 9, 13, 1, 48, 25, 16, 57, 68, 43, 84, 59, 14, 54],
           [92, 16, 55, 47, 25, 65, 1, 47, 59, 8, 60, 95, 22, 2, 34, 79, 72, 58, 61, 75, 24, 61, 68, 12, 66, 54, 41, 1, 88, 59],
           [28, 67, 34, 37, 31, 85, 15, 23, 6, 22, 80, 43, 71, 29, 82, 98, 98, 97, 20, 55, 4, 49, 18, 34, 73, 32, 4, 97, 84, 70],
           [10, 44, 1, 64, 49, 16, 40, 58, 11, 99, 24, 72, 39, 69, 53, 8, 67, 51, 15, 19, 6, 79, 95, 16, 88, 60, 40, 78, 5, 19],
           [48, 47, 92, 49, 13, 82, 74, 24, 11, 5, 15, 43, 56, 75, 86, 33, 74, 32, 78, 82, 16, 69, 73, 64, 97, 51, 16, 76, 62, 46],
           [11, 3, 59, 82, 24, 36, 22, 27, 50, 49, 70, 39, 64, 73, 58, 31, 48, 45, 56, 2, 3, 13, 20, 37, 66, 69, 81, 81, 60, 71]],
        2:[[93, 5, 24, 46, 69, 4, 81, 32, 29, 34, 34, 42, 57, 99, 83, 97, 30, 47, 5, 96, 54, 67, 86, 96, 82, 69, 11, 24, 85, 0], 
           [63, 37, 17, 90, 86, 9, 9, 25, 57, 9, 77, 20, 48, 70, 27, 95, 38, 2, 23, 46, 34, 97, 29, 89, 83, 2, 95, 19, 33, 55], 
           [41, 88, 29, 87, 14, 45, 97, 100, 45, 33, 97, 98, 24, 43, 33, 28, 30, 43, 8, 5, 50, 6, 83, 18, 61, 8, 63, 32, 84, 78], 
           [14, 66, 28, 26, 63, 4, 80, 91, 5, 38, 24, 80, 51, 96, 44, 1, 48, 8, 69, 17, 85, 14, 42, 50, 79, 53, 64, 99, 40, 68], 
           [37, 1, 27, 16, 35, 38, 5, 3, 22, 28, 57, 79, 26, 1, 40, 86, 3, 15, 51, 1, 8, 26, 32, 90, 93, 79, 78, 72, 26, 2], 
           [59, 63, 7, 92, 10, 24, 48, 37, 56, 86, 71, 81, 70, 67, 88, 58, 37, 15, 16, 75, 77, 71, 68, 6, 42, 84, 79, 15, 89, 27], 
           [63, 97, 54, 14, 95, 84, 3, 48, 36, 24, 95, 11, 8, 9, 100, 38, 24, 14, 28, 8, 66, 13, 38, 47, 32, 90, 8, 41, 64, 0], 
           [15, 4, 46, 47, 33, 74, 36, 29, 54, 99, 2, 92, 89, 94, 21, 53, 39, 98, 1, 81, 46, 12, 46, 41, 29, 88, 73, 94, 82, 17], 
           [54, 94, 19, 44, 97, 63, 53, 12, 59, 19, 13, 80, 94, 57, 40, 1, 29, 13, 35, 66, 41, 63, 48, 71, 86, 70, 33, 54, 92, 41], 
           [17, 78, 13, 11, 2, 8, 40, 34, 96, 21, 24, 75, 46, 91, 76, 2, 64, 86, 14, 75, 24, 4, 70, 35, 22, 63, 82, 14, 76, 62], 
           [26, 71, 84, 50, 52, 33, 26, 9, 35, 86, 23, 100, 9, 5, 23, 76, 28, 71, 46, 35, 88, 89, 34, 59, 54, 65, 99, 36, 11, 52], 
           [42, 86, 48, 19, 81, 46, 70, 19, 42, 66, 80, 13, 57, 59, 28, 31, 66, 51, 57, 28, 90, 36, 55, 37, 24, 44, 16, 63, 20, 71], 
           [72, 70, 63, 1, 96, 90, 18, 73, 57, 32, 94, 79, 73, 67, 17, 60, 45, 85, 31, 31, 67, 52, 44, 70, 77, 25, 71, 70, 76, 29], 
           [52, 12, 48, 1, 30, 37, 82, 18, 10, 37, 53, 22, 75, 16, 44, 68, 73, 33, 14, 55, 63, 32, 48, 53, 5, 45, 94, 56, 26, 56], 
           [51, 59, 9, 3, 30, 50, 41, 94, 79, 94, 54, 97, 25, 7, 68, 62, 32, 49, 18, 88, 53, 32, 17, 81, 21, 8, 60, 6, 33, 46], 
           [74, 94, 20, 44, 56, 88, 80, 1, 91, 83, 58, 42, 19, 25, 35, 25, 34, 94, 64, 51, 58, 1, 49, 66, 88, 55, 34, 20, 73, 65], 
           [60, 17, 1, 83, 84, 28, 51, 19, 7, 42, 34, 59, 4, 80, 40, 96, 85, 84, 10, 37, 8, 5, 86, 51, 59, 99, 62, 51, 22, 95], 
           [31, 47, 10, 53, 26, 23, 19, 29, 9, 58, 55, 7, 20, 94, 35, 52, 91, 68, 37, 98, 1, 82, 65, 62, 39, 10, 65, 10, 65, 1], 
           [15, 16, 65, 99, 56, 93, 44, 58, 93, 70, 71, 83, 92, 6, 6, 33, 52, 63, 56, 51, 66, 68, 39, 14, 47, 47, 25, 75, 10, 7], 
           [64, 67, 69, 25, 28, 11, 62, 24, 13, 22, 47, 27, 32, 39, 42, 5, 95, 23, 73, 91, 85, 38, 82, 30, 48, 59, 58, 20, 5, 75], 
           [6, 37, 3, 89, 1, 26, 72, 76, 78, 95, 58, 55, 87, 42, 42, 26, 73, 7, 28, 8, 48, 63, 99, 73, 20, 2, 86, 2, 80, 10], 
           [13, 28, 13, 74, 42, 52, 33, 59, 12, 1, 30, 39, 41, 10, 15, 72, 61, 4, 49, 68, 48, 13, 41, 75, 98, 74, 29, 28, 57, 3], 
           [93, 94, 77, 34, 50, 4, 76, 55, 5, 34, 36, 4, 69, 11, 41, 78, 46, 13, 81, 8, 84, 88, 2, 86, 29, 27, 3, 24, 82, 95], 
           [54, 78, 4, 54, 52, 20, 34, 18, 10, 94, 21, 57, 63, 14, 27, 56, 63, 89, 99, 26, 37, 94, 5, 15, 26, 11, 40, 52, 88, 30], 
           [29, 1, 37, 53, 3, 42, 27, 17, 80, 13, 80, 91, 23, 7, 41, 25, 38, 58, 68, 1, 52, 76, 58, 12, 93, 69, 77, 78, 56, 48], 
           [62, 31, 94, 99, 14, 55, 3, 2, 50, 26, 74, 92, 5, 74, 76, 15, 100, 89, 11, 32, 99, 63, 86, 81, 25, 10, 4, 68, 42, 44], 
           [90, 72, 75, 72, 23, 65, 39, 68, 37, 67, 6, 39, 13, 42, 21, 53, 4, 74, 15, 36, 4, 8, 94, 29, 38, 56, 71, 84, 34, 56], 
           [45, 79, 71, 94, 94, 86, 75, 72, 39, 32, 69, 90, 3, 48, 99, 70, 65, 38, 6, 73, 67, 93, 78, 18, 45, 16, 4, 57, 92, 45], 
           [89, 64, 82, 38, 73, 25, 96, 48, 60, 68, 26, 36, 63, 88, 76, 73, 88, 25, 27, 7, 89, 42, 33, 91, 75, 37, 1, 34, 73, 62], 
           [61, 99, 77, 25, 17, 11, 72, 48, 73, 40, 22, 55, 40, 10, 5, 85, 81, 89, 53, 28, 45, 42, 31, 17, 12, 85, 66, 98, 34, 78]],
        3:[[36, 65, 32, 4, 61, 48, 76, 42, 74, 3, 89, 29, 44, 66, 15, 62, 32, 74, 4, 18, 70, 60, 2, 76, 39, 48, 44, 71, 9, 66], 
           [18, 23, 46, 94, 90, 3, 49, 42, 14, 48, 53, 90, 96, 69, 1, 35, 81, 83, 26, 4, 3, 71, 22, 28, 31, 31, 99, 87, 34, 99], 
           [21, 35, 60, 20, 19, 51, 51, 62, 26, 88, 62, 5, 59, 19, 61, 37, 58, 29, 41, 89, 26, 86, 36, 66, 40, 13, 2, 79, 51, 94], 
           [24, 15, 91, 20, 85, 50, 12, 95, 24, 83, 28, 63, 27, 2, 90, 72, 2, 39, 74, 12, 62, 1, 60, 20, 31, 5, 90, 88, 91, 35], 
           [76, 25, 30, 56, 93, 26, 28, 20, 15, 6, 61, 76, 69, 64, 48, 68, 1, 86, 65, 52, 45, 94, 30, 26, 29, 48, 24, 91, 76, 73], 
           [45, 1, 15, 74, 13, 52, 69, 37, 72, 78, 27, 32, 95, 53, 97, 22, 83, 96, 1, 23, 8, 9, 15, 52, 13, 85, 16, 36, 2, 29], 
           [48, 88, 42, 72, 69, 88, 58, 19, 18, 12, 24, 1, 48, 54, 38, 73, 80, 94, 78, 3, 80, 85, 17, 99, 33, 56, 50, 100, 27, 25], 
           [50, 45, 76, 29, 19, 78, 92, 25, 16, 65, 57, 7, 10, 96, 79, 51, 46, 50, 1, 87, 20, 85, 27, 69, 41, 27, 28, 82, 78, 63], 
           [76, 3, 70, 26, 5, 17, 20, 8, 71, 17, 87, 25, 58, 75, 14, 41, 99, 32, 54, 88, 83, 49, 13, 30, 30, 81, 88, 15, 89, 21], 
           [20, 18, 5, 52, 42, 3, 51, 5, 89, 1, 65, 96, 83, 79, 84, 62, 92, 91, 37, 77, 89, 51, 26, 67, 10, 40, 96, 1, 11, 29], 
           [35, 30, 72, 32, 59, 39, 93, 11, 41, 38, 46, 22, 95, 46, 61, 5, 58, 16, 57, 95, 83, 85, 60, 88, 32, 77, 16, 45, 30, 89], 
           [47, 22, 63, 100, 38, 39, 19, 92, 95, 5, 59, 97, 73, 38, 82, 77, 48, 67, 41, 94, 17, 10, 22, 96, 30, 60, 31, 99, 61, 7], 
           [53, 90, 10, 84, 43, 83, 98, 94, 56, 47, 86, 81, 56, 24, 87, 39, 2, 37, 73, 46, 20, 16, 41, 95, 27, 8, 15, 76, 5, 32], 
           [91, 100, 57, 78, 78, 11, 68, 66, 38, 39, 3, 20, 3, 63, 29, 20, 5, 81, 84, 17, 17, 22, 1, 56, 54, 4, 30, 38, 83, 2], 
           [66, 64, 47, 37, 81, 35, 94, 81, 66, 15, 63, 26, 64, 23, 4, 69, 41, 73, 63, 21, 6, 83, 57, 4, 63, 29, 7, 100, 48, 22], 
           [27, 57, 87, 62, 50, 18, 87, 65, 11, 84, 34, 18, 90, 95, 29, 14, 84, 89, 98, 94, 70, 2, 80, 47, 45, 47, 38, 21, 35, 90], 
           [74, 42, 59, 29, 46, 98, 17, 61, 30, 49, 28, 25, 20, 13, 84, 24, 17, 56, 50, 16, 26, 33, 20, 84, 7, 43, 60, 97, 69, 16], 
           [73, 66, 70, 55, 64, 97, 43, 84, 95, 11, 65, 96, 60, 55, 35, 63, 61, 85, 21, 48, 50, 8, 61, 89, 19, 20, 21, 74, 82, 13], 
           [85, 53, 31, 86, 47, 86, 58, 42, 57, 95, 4, 86, 48, 87, 75, 53, 56, 23, 22, 73, 14, 78, 78, 26, 22, 76, 36, 53, 49, 25], 
           [19, 87, 41, 19, 46, 12, 93, 44, 14, 60, 13, 100, 35, 85, 64, 52, 4, 47, 28, 86, 41, 5, 57, 72, 41, 31, 96, 32, 17, 29], 
           [70, 70, 57, 7, 84, 31, 34, 19, 77, 25, 38, 81, 1, 5, 1, 10, 71, 72, 100, 80, 11, 41, 11, 28, 57, 4, 35, 21, 8, 19], 
           [34, 77, 64, 32, 86, 82, 30, 27, 60, 87, 55, 14, 55, 15, 68, 16, 68, 95, 91, 95, 23, 39, 17, 84, 67, 24, 88, 52, 36, 63], 
           [19, 8, 78, 31, 32, 57, 70, 62, 22, 23, 25, 40, 47, 36, 54, 94, 11, 32, 61, 52, 6, 94, 48, 14, 63, 12, 50, 93, 44, 62], 
           [10, 24, 48, 12, 26, 14, 14, 20, 11, 42, 52, 69, 68, 70, 70, 44, 94, 48, 35, 42, 43, 28, 40, 90, 41, 53, 49, 68, 95, 57], 
           [67, 64, 70, 23, 49, 31, 60, 5, 3, 77, 21, 47, 42, 49, 69, 53, 75, 68, 33, 19, 9, 18, 92, 14, 74, 43, 37, 78, 5, 54], 
           [73, 83, 90, 2, 66, 32, 33, 6, 25, 7, 5, 84, 99, 69, 22, 92, 65, 33, 63, 43, 74, 93, 63, 56, 26, 93, 31, 36, 62, 32], 
           [20, 13, 80, 20, 41, 85, 24, 88, 92, 69, 26, 92, 76, 2, 51, 6, 15, 76, 1, 28, 48, 79, 32, 77, 49, 50, 15, 97, 2, 49], 
           [74, 90, 72, 2, 58, 97, 48, 80, 11, 89, 11, 6, 34, 64, 97, 22, 7, 100, 30, 76, 34, 4, 87, 46, 69, 20, 46, 72, 60, 56], 
           [3, 47, 33, 81, 23, 98, 85, 8, 59, 93, 54, 5, 96, 94, 69, 58, 52, 96, 29, 41, 20, 37, 80, 84, 100, 98, 68, 76, 53, 9], 
           [82, 75, 80, 5, 12, 32, 78, 67, 12, 18, 14, 71, 29, 67, 96, 60, 8, 36, 3, 86, 13, 13, 48, 23, 3, 87, 22, 83, 77, 13]]
    }
    die = die_dict[session_number]

    # GROUPS BY CYCLE IS GENERATED USING
    #def groupcycle(n,g):
    #    groups_by_cycle = []
    #    numbers = random.sample(range(1,n+1),n)
    #    for c in range(11):
    #        random.shuffle(numbers)
    #        groups_by_cycle.append([numbers[i:i+g] for i in range(0,len(numbers),g)])
    #    return groups_by_cycle
    
    groups_by_cycle_dict = {4: [[[4, 1, 2, 3]],
                                [[3, 4, 2, 1]],
                                [[3, 1, 4, 2]],
                                [[3, 4, 2, 1]],
                                [[3, 1, 2, 4]],
                                [[4, 3, 1, 2]],
                                [[1, 3, 2, 4]],
                                [[4, 3, 2, 1]],
                                [[2, 3, 1, 4]],
                                [[3, 2, 4, 1]],
                                [[4, 1, 2, 3]]],
                            16: [[[7, 2, 4, 14], [8, 5, 12, 16], [15, 3, 10, 9], [13, 1, 11, 6]],
                                 [[11, 14, 8, 16], [15, 2, 12, 4], [13, 6, 10, 3], [1, 9, 7, 5]],
                                 [[2, 7, 5, 8], [1, 11, 16, 15], [4, 10, 9, 13], [12, 6, 3, 14]],
                                 [[8, 4, 14, 7], [13, 2, 1, 12], [3, 16, 5, 6], [11, 15, 9, 10]],
                                 [[7, 1, 9, 11], [14, 4, 6, 2], [12, 3, 16, 13], [10, 8, 5, 15]],
                                 [[1, 4, 2, 11], [16, 10, 5, 3], [15, 14, 12, 9], [8, 6, 13, 7]],
                                 [[6, 12, 1, 16], [9, 7, 14, 4], [5, 10, 8, 15], [11, 13, 3, 2]],
                                 [[12, 7, 15, 2], [8, 6, 14, 5], [3, 11, 9, 16], [13, 10, 1, 4]],
                                 [[16, 15, 12, 14], [4, 2, 5, 13], [8, 1, 10, 6], [7, 9, 11, 3]],
                                 [[3, 7, 2, 6], [11, 12, 16, 5], [1, 15, 4, 8], [14, 13, 10, 9]],
                                 [[7, 2, 4, 14], [8, 5, 12, 16], [15, 3, 10, 9], [13, 1, 11, 6]]],
                            20: [[[14, 8, 18, 15], [4, 11, 5, 13], [17, 20, 1, 10], [2, 19, 16, 9], [6, 3, 12, 7]],
                                 [[7, 20, 12, 16], [4, 19, 11, 17], [13, 1, 18, 15], [5, 10, 3, 6], [9, 2, 14, 8]],
                                 [[10, 17, 20, 15], [4, 2, 3, 1], [6, 7, 12, 14], [11, 9, 5, 16], [13, 8, 19, 18]],
                                 [[16, 6, 10, 8], [15, 14, 13, 4], [11, 12, 1, 18], [5, 17, 3, 2], [9, 7, 19, 20]],
                                 [[13, 5, 8, 16], [2, 11, 15, 14], [12, 10, 4, 20], [17, 18, 3, 6], [19, 9, 7, 1]],
                                 [[7, 18, 16, 8], [3, 1, 4, 6], [9, 13, 11, 5], [19, 17, 12, 2], [14, 10, 15, 20]],
                                 [[11, 12, 14, 7], [6, 15, 9, 5], [18, 16, 3, 20], [2, 4, 17, 8], [1, 19, 13, 10]],
                                 [[16, 2, 6, 11], [12, 3, 4, 14], [17, 9, 15, 1], [5, 7, 8, 18], [10, 19, 20, 13]],
                                 [[10, 7, 4, 19], [13, 15, 11, 6], [2, 18, 16, 8], [12, 3, 9, 5], [17, 1, 20, 14]],
                                 [[15, 3, 8, 5], [1, 16, 10, 18], [12, 2, 19, 17], [7, 13, 11, 20], [4, 6, 14, 9]],
                                 [[14, 8, 18, 15], [4, 11, 5, 13], [17, 20, 1, 10], [2, 19, 16, 9], [6, 3, 12, 7]]],
                           24: [[[19, 16, 24, 18], [9, 10, 4, 1], [12, 14, 21, 11], [17, 15, 8, 3], [7, 23, 2, 5], [6, 13, 20, 22]], 
                                [[18, 4, 5, 3], [2, 13, 15, 17], [11, 7, 16, 23], [14, 9, 8, 21], [22, 1, 19, 24], [20, 12, 6, 10]], 
                                [[19, 23, 10, 1], [9, 8, 22, 24], [11, 2, 18, 3], [21, 20, 7, 13], [16, 12, 5, 4], [17, 14, 6, 15]], 
                                [[19, 23, 12, 2], [24, 18, 22, 8], [20, 4, 21, 14], [16, 7, 1, 5], [10, 3, 6, 17], [11, 15, 13, 9]], 
                                [[17, 8, 10, 18], [9, 20, 22, 19], [4, 14, 12, 2], [5, 16, 3, 1], [6, 24, 13, 21], [15, 7, 11, 23]], 
                                [[1, 11, 14, 2], [24, 13, 15, 21], [3, 20, 17, 12], [5, 23, 4, 19], [10, 7, 18, 22], [16, 9, 8, 6]], 
                                [[23, 7, 13, 5], [3, 14, 21, 15], [2, 20, 9, 4], [22, 11, 16, 17], [8, 19, 10, 6], [12, 1, 18, 24]], 
                                [[10, 9, 4, 7], [14, 18, 3, 23], [6, 13, 19, 17], [12, 24, 15, 20], [11, 2, 22, 16], [8, 5, 21, 1]], 
                                [[13, 17, 1, 5], [2, 3, 24, 14], [10, 21, 23, 19], [18, 8, 20, 7], [6, 15, 12, 9], [4, 22, 16, 11]], 
                                [[11, 1, 10, 4], [18, 12, 16, 9], [24, 5, 2, 20], [15, 14, 8, 22], [6, 3, 13, 7], [23, 21, 19, 17]],
                                [[19, 16, 24, 18], [9, 10, 4, 1], [12, 14, 21, 11], [17, 15, 8, 3], [7, 23, 2, 5], [6, 13, 20, 22]]]}
        
    number_of_subjects = 4
    groups_by_cycle = groups_by_cycle_dict[number_of_subjects]

    Cycle_Condition_1 = 50 # Die roll is greater than
    Cycle_Condition_2 = 5 # Round number is greater than
    Cycle_Condition_3 = 10 # Number of cycles

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.session.get_participants():
            p.vars['Cycle_Condition_3'] = Constants.Cycle_Condition_3
            p.vars['p1_round'] = 0
            p.vars['p1_cycle'] = 1
            p.vars['p1_payment_round'] = list([])
            p.vars['p1_payment'] = list([])
            p.vars['payment_part_num'] = random.randint(1,2)
            p.vars['payment_cycle'] = random.randint(1,p.vars['Cycle_Condition_3'])
            p.label = str(random.randint(1000,9999))

class Group(BaseGroup):
    p1_cycle = models.IntegerField(initial=1)

class Player(BasePlayer):
    p1_cycle = models.IntegerField(initial=1)
    p1_round = models.IntegerField(initial=1)
    decision = models.StringField(
        choices=['Green', 'Red'],
        widget=widgets.RadioSelect)
    group_decision = models.StringField()
    die_roll = models.IntegerField()

    def new_cycle(self):
        self.p1_round = 1
        self.participant.vars['p1_round'] = self.p1_round
        self.p1_cycle = self.participant.vars['p1_cycle'] + 1
        self.participant.vars['p1_cycle'] = self.p1_cycle

    def new_round(self):
        self.p1_round = self.participant.vars['p1_round'] + 1
        self.participant.vars['p1_round'] = self.p1_round
        self.p1_cycle = self.participant.vars['p1_cycle']

    def set_payoff(self):
        payoff_matrix = {
            'Green':{'All 3 Green': Constants.cooperate_payoff,
                 'Any of 3 Red': Constants.betrayed_payoff},
            'Red':{'All 3 Green': Constants.betray_payoff,
                 'Any of 3 Red': Constants.defect_payoff}
        }
        self.payoff = payoff_matrix[self.decision][self.group_decision]
        self.die_roll = Constants.die[self.p1_cycle-1][self.participant.vars['p1_round']-1]

    def store_vars(self):
        self.p1_cycle = self.participant.vars['p1_cycle'] + 1
        self.participant.vars['p1_cycle'] = self.p1_cycle
