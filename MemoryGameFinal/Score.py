class Score:

    def __init__(self):
        # Array to store tuples with score and name
        self.scores = []

        # Score and name variables
        self.gamePoints = 0
        self.userName = "NoName"

    # Selection sort used to order scores in descending order
    def selectionSort(self):
        if not isFileEmpty():
            scores = self.scores
            for i in range(len(scores)):
                max_index = i
                for j in range(i + 1, len(scores)):
                    # Find index of the highest score
                    if scores[j][1] > scores[max_index][1]:
                        max_index = j
                # Swap scores to achieve proper order
                scores[i], scores[max_index] = scores[max_index], scores[i]

    # Getters and Setters
    def setScore(self, score):
        self.gamePoints = score

    def getScore(self):
        return self.gamePoints

    def setUserName(self, name):
        self.userName = name

    def getUserName(self):
        return self.userName

    # Function to write scores to file
    def writeScore(self):
        with open("GameFiles/Scores.txt", 'a') as file:
            score = format(self.getScore(), '.2f')
            playerName = self.getUserName()
            file.write(f"{playerName}, {score}\n")

            # Append score and name tuple to scores array
            self.scores.append((playerName, float(score)))

    # Function to read then rewrite score file in descending order
    def rewriteScores(self):
        if not isFileEmpty():
            self.scores = []
            with open("GameFiles/Scores.txt", 'r') as file:
                SEPARATOR = ","
                for line in file:
                    line = line.strip()
                    if line:
                        name_score = line.split(SEPARATOR)
                        player_name = name_score[0]
                        score = float(name_score[1])
                        self.scores.append((player_name, score))

            # Apply selection sort to the scores array
            self.selectionSort()

            # Rewrite the file in the sorted order
            with open("GameFiles/Scores.txt", 'w') as file:
                for player_name, score in self.scores:
                    file.write(f"{player_name}, {score}\n")

    # Function used to retrieve top 3 scores
    def getHighScore(self):
        self.rewriteScores()
        # Return top 3 scores from class variable scores
        return self.scores[:3] if self.scores else "No High Scores Yet"


# Function to check if file is empty
def isFileEmpty():
    with open("GameFiles/Scores.txt", 'r') as file:
        line = file.readline()
        if line.strip() == "":
            return True
        else:
            return False
