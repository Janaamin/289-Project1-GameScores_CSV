import csv

# Processes disqualifications depedning on  scores of each player
def process_disqualifications(scores):
    disqualified_rounds = []
    for i, score in enumerate(scores):
        if score == -1:
            disqualified_rounds.append(i+1)  # i+1 because rounds are 1-indexed
    return disqualified_rounds

# To Open and read the CSV file: 'r'
players = []
with open('tournament_results.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        name = row[1] + ' ' + row[0]  # Combine first and last names
        scores = [int(x) for x in row[2:]]  # Convert string scores to integers
        disqualified_rounds = process_disqualifications(scores)
        # Storing players information in a tuple
        players.append((name, scores, disqualified_rounds))

# Initialzing variables for calculating statistics and storing disqualified players
total_scores = []
disqualified_players_info = []

# Initializing list to store valid scores for each round
round_valid_scores = [[] for _ in range(4)]  # There are 4 rounds


# Processing each player to separate disqualified players from those who will be included in the statistics
for player in players:
    name, scores, disqualified_rounds = player
    if disqualified_rounds:
        disqualified_players_info.append((name, disqualified_rounds))
        total_score = sum(score for score in scores if score != -1)  # Exclude disqualified scores
    else:
        total_score = sum(scores)
        # Store valid scores for each round
        for i, score in enumerate(scores):
            if score != -1:
                round_valid_scores[i].append(score)
    total_scores.append((name, total_score))

# Calculating the highest and lowest scores
highest_score = max(total_scores, key=lambda x: x[1])
lowest_score = min(total_scores, key=lambda x: x[1])

# Output highest and lowest scores
print(highest_score[0] + ' has the highest score with ' + str(highest_score[1]))
print(lowest_score[0] + ' has the lowest score with ' + str(lowest_score[1]))

# Calculating mean and median scores for the qualified participants
qualified_scores = [score for name, score in total_scores if score > -1]
average_score = sum(qualified_scores) / len(qualified_scores)  # Mean score
sorted_scores = sorted(qualified_scores)
mid = len(sorted_scores) // 2
median_score = (sorted_scores[mid] + sorted_scores[-mid-1]) / 2  # Median score

# mean and median scores
print("Mean score: " + str(round(average_score, 1)))
print("Median score: " + str(round(median_score, 1)))

# Calculating mean score for each round using valid scores
mean_scores_rounds = [sum(scores) / len(scores) if scores else 0 for scores in round_valid_scores]
for i, mean_score in enumerate(mean_scores_rounds, 1):
    print("Round " + str(i) + " mean score: " + str(round(mean_score, 1)))

# Writing the disqualified players info to a file
with open('disqualified_players.txt', 'w') as output_file:
    for info in disqualified_players_info:
        rounds = ', '.join(str(round_num) for round_num in info[1])
        output_file.write(info[0] + " did not participate in round " + rounds + "\n")

# Sorting players by their total score for final output
total_scores.sort(key=lambda x: (-x[1], x[0]))  # Sort by score descending, then by name
with open('participant_scores.txt', 'w') as output_file:
    for entry in total_scores:
        output_file.write(entry[0] + ', ' + str(entry[1]) + "\n")