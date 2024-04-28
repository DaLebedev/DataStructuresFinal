import random
import pygame

# Screen width and height
WINDOW_X, WINDOW_Y = 1000, 720

CARD_SIZE = (100, 100)

cardBack = pygame.image.load("GameFiles/CardBack.png")

# Define color names and corresponding file paths
colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]
shapes = ["Circle", "Pentagon", "Rhombus", "Square", "Star", "Triangle"]
file_path = "GameFiles/"

# Load images using loops
images = {}
for color in colors:
    for shape in shapes:
        file_name = color + shape + ".png"
        images[color + shape] = pygame.image.load(file_path + file_name)

# Create dictionary for card images
numberImages = {
    1: images["RedCircle"], 2: images["RedPentagon"], 3: images["RedRhombus"], 4: images["RedSquare"],
    5: images["RedStar"], 6: images["RedTriangle"], 7: images["OrangeCircle"], 8: images["OrangePentagon"],
    9: images["OrangeRhombus"], 10: images["OrangeSquare"], 11: images["OrangeStar"], 12: images["OrangeTriangle"],
    13: images["YellowCircle"], 14: images["YellowPentagon"], 15: images["YellowRhombus"], 16: images["YellowSquare"],
    17: images["YellowStar"], 18: images["YellowTriangle"], 19: images["GreenCircle"], 20: images["GreenPentagon"],
    21: images["GreenRhombus"], 22: images["GreenSquare"], 23: images["GreenStar"], 24: images["GreenTriangle"],
    25: images["BlueCircle"], 26: images["BluePentagon"], 27: images["BlueRhombus"], 28: images["BlueSquare"],
    29: images["BlueStar"], 30: images["BlueTriangle"], 31: images["PurpleCircle"], 32: images["PurplePentagon"],
    33: images["PurpleRhombus"], 34: images["PurpleSquare"], 35: images["PurpleStar"], 36: images["PurpleTriangle"],
}

# Load image for backs of cards
cardBack = pygame.transform.scale(cardBack, CARD_SIZE)

# Load card images
for key, image in numberImages.items():
    numberImages[key] = pygame.transform.scale(image, CARD_SIZE)


class Card:
    def __init__(self, value, cardImg, back, position):
        # Card object variables
        self.value = value
        self.image = cardImg
        self.back = back
        self.position = position
        self.visible = False

    # Function to draw cards on screen
    def draw(self, surface):
        if self.image is not None:
            if self.visible:
                surface.blit(self.image, self.position)
            else:
                surface.blit(self.back, self.position)
        else:
            return

    # Card to string for testing
    def __str__(self):
        return f"{self.value},{self.position}"


# Generates a single random card off-screen
def generateSingleCard():
    value = random.randint(0, 36)
    cardImg = numberImages[random.randint(1, 36)]
    back = cardBack
    position = -10000, -10000
    return Card(value, cardImg, back, position)


# Function for generating random card values each with a match
def generateCardNums(boardSize=6):
    finalCards = []
    arr = [num for num in range(1, boardSize*boardSize)]
    random.shuffle(arr)
    for n in range(int(pow(boardSize, 2) / 2)):
        finalCards.append(arr[n])
    finalCards *= 2
    random.shuffle(finalCards)
    return finalCards


# Generates the position of all cards so they are centered
def generateCardPos(boardSize=6):
    cardPositions = []
    startX = 0
    startY = 0
    numRows = 0
    # Calculate the center of the screen
    centerX = WINDOW_X // 2
    centerY = WINDOW_Y // 2
    # Set positions for 4x4 game mode
    if boardSize == 4:
        startX = centerX - ((boardSize/2) * 100)
        startY = centerY - ((boardSize/2) * 100)
        numRows = 4
    # Set positions for 6x6 game mode
    elif boardSize == 6:
        startX = centerX - ((boardSize / 2) * 100)
        startY = centerY - ((boardSize / 2) * 100)
        numRows = 6

    xpos = startX
    ypos = startY

    for i in range(numRows):  # Outer loop for rows
        for u in range(numRows):  # Inner loop for columns
            cardPositions.append((xpos, ypos))
            xpos += 110  # Move to the next column
        xpos = startX  # Reset xpos for the next row
        ypos += 110  # Move to the next row

    return cardPositions
