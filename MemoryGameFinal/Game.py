import sys
import pygame
import Card
import Stack
import Score

# Initialize pygame
pygame.init()
# Screen width and height
WINDOW_X, WINDOW_Y = 1000, 720
# Title of canvas
pygame.display.set_caption("Memory Masters")
# Creating canvas
canvas = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
# Screen layers for layering images
cardLayer = pygame.Surface((WINDOW_X, WINDOW_Y), pygame.SRCALPHA)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load start button image
startImg = pygame.image.load("GameFiles/StartButton.png")
startButton = pygame.transform.scale(startImg, (200, 200))
startButtonRect = startButton.get_rect(center=((WINDOW_X // 2), (WINDOW_Y // 2) - 100))

# Load high score button image
hiScoreImg = pygame.image.load("GameFiles/HiScoreButton.png")
hiScoreButton = pygame.transform.scale(hiScoreImg, (200, 200))
hiScoreButtonRect = hiScoreButton.get_rect(center=((WINDOW_X // 2), (WINDOW_Y // 2) + 100))

# Load back button
backButtonImg = pygame.image.load("GameFiles/BackButton.png")
backButton = pygame.transform.scale(backButtonImg, (100, 100))
backButtonRect = backButton.get_rect(center=(50, 50))
backButtonPressed = False

# Load 4x4 button
button4x4Img = pygame.image.load("GameFiles/Button4x4.png")
button4x4 = pygame.transform.scale(button4x4Img, (100, 100))
button4x4Rect = button4x4.get_rect(center=((WINDOW_X // 2) - 100, (WINDOW_Y // 2) + 150))
button4x4Pressed = False

# Load 4x4 button
button6x6Img = pygame.image.load("GameFiles/Button6x6.png")
button6x6 = pygame.transform.scale(button6x6Img, (100, 100))
button6x6Rect = button6x6.get_rect(center=((WINDOW_X // 2) + 100, (WINDOW_Y // 2) + 150))
button6x6Pressed = False

font = pygame.font.Font(None, 48)
colorStartActive = pygame.Color('white')
colorActive = pygame.Color('black')
color = colorStartActive

# Dictionary of colors for high score screen
scoreColors = {
    1: pygame.Color("#D09900"),
    2: pygame.Color("#BBC4D5"),
    3: pygame.Color("#824C00")
}
text = ''

startActive = False
hiScorePressed = False

# High score and input variables
hiScoreTxtSize = 86
hiScoreTxtFont = pygame.font.Font(None, hiScoreTxtSize)
inputBox = pygame.Rect((WINDOW_X // 2) - 100, (WINDOW_Y // 2) - 25, 200, 50)
inputNameTxt = "Enter Your Username:"
nameTxt = font.render(inputNameTxt, True, BLACK)
hiScoreTxt = "High Scores"
scoreTxt = font.render(inputNameTxt, True, BLACK)
nameTxtWidth, nameTxtHeight = font.size(inputNameTxt)
nameTxtX = (WINDOW_X - nameTxtWidth) // 2
nameTxtY = inputBox.y - nameTxtHeight - 10

# Game mode selection variables
selected4x4 = "Game Mode: 4x4"
selected6x6 = "Game Mode: 6x6"
selected4x4Txt = font.render(selected4x4, True, BLACK)
selected6x6Txt = font.render(selected6x6, True, BLACK)
selectedTxtX = WINDOW_X // 2
selectedTxtY = WINDOW_Y // 2 + 150
selectedTxtRect = selected4x4Txt.get_rect(center=(selectedTxtX, selectedTxtY))

# Card timer variables
CARD_TIMER_EVENT = pygame.USEREVENT + 2
TIMER_DELAY = 1000
CARD_INITIAL_TIME = 2
cardTimeRemaining = CARD_INITIAL_TIME
flippedCount = 0

# Game timer variables
GAME_TIMER_EVENT = pygame.USEREVENT + 1
GAME_INITIAL_TIME_45, GAME_INITIAL_TIME_120 = 45, 120
gameTimeRemaining = GAME_INITIAL_TIME_120

# Game is not started until start button pressed
gameStarted = False

# Initialize array to store matches
matches = []

# Initialize current points to 0
gamePoints = 0
gameScore = Score.Score()
name = "NoName"
score = 0

# Generate cards
cardDeck = Stack.Stack()
cardNums = Card.generateCardNums(6)
cardPos = Card.generateCardPos(6)


# Function to display cards when clicked
def flipCard():
    global flippedCount, card, card1, card2, cardTimeRemaining
    if flippedCount != 0 and flippedCount % 2 == 0:
        return
    for card in cardDeck.cards:
        global cardTimeRemaining
        if card.visible or card in matches:
            continue
        cardRect = card.back.get_rect(topleft=card.position)
        if cardRect.collidepoint(mouseX, mouseY):
            card.visible = True
            flippedCount += 1
            if flippedCount % 2 == 1:
                card1 = card
            if flippedCount % 2 == 0:
                card2 = card
                if not isMatch(card1, card2):
                    cardTimeRemaining = CARD_INITIAL_TIME
                    pygame.time.set_timer(CARD_TIMER_EVENT, TIMER_DELAY)
                else:
                    cardTimeRemaining = 0
                    pygame.time.set_timer(CARD_TIMER_EVENT, 10)


# Method to flip visible cards back
def flipCardBack():
    global card
    for card in cardDeck.cards:
        if card.visible and card not in matches:
            card.visible = False


# Function to check if two cards are a match
def isMatch(cardA, cardB):
    global gamePoints
    if cardA.image == cardB.image:
        matches.append(cardA)
        matches.append(cardB)
        cardA.image = None
        cardB.image = None
        gamePoints += 1
        return True
    return False


# Start running
running = True

while running:
    global card1, card2
    canvas.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse button press
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # If start button pressed set startActive to true
            if startButtonRect and startButtonRect.collidepoint(event.pos):
                startActive = True
                color = colorActive
                canvas.blit(nameTxt, (200, 200))

            # If highScore pressed set highScorePressed to true
            if hiScoreButtonRect and hiScoreButtonRect.collidepoint(event.pos):
                hiScorePressed = True
                backButtonPressed = False

            # If backButton is pressed set backButtonPressed to true
            if (backButton and backButtonRect.collidepoint(event.pos)) and not gameStarted:
                backButtonPressed = True

            # If 4x4 selected, generate board with 16 cards
            if button4x4 and button4x4Rect.collidepoint(event.pos):
                button4x4Pressed = True
                button6x6Pressed = False
                cardDeck = Stack.Stack()
                cardNums = Card.generateCardNums(4)
                cardPos = Card.generateCardPos(4)

                # Fill deck with cards
                for i in range(len(cardNums)):
                    image = Card.numberImages[cardNums[i]]
                    c = Card.Card(cardNums[i], image, Card.cardBack, cardPos[i])
                    cardDeck.push(c)

            # If 6x6 selected, generate board with 36 cards
            if button6x6 and button6x6Rect.collidepoint(event.pos):
                button4x4Pressed = False
                button6x6Pressed = True
                cardDeck = Stack.Stack()
                cardNums = Card.generateCardNums(6)
                cardPos = Card.generateCardPos(6)

                # Fill deck with cards
                for i in range(len(cardNums)):
                    image = Card.numberImages[cardNums[i]]
                    c = Card.Card(cardNums[i], image, Card.cardBack, cardPos[i])
                    cardDeck.push(c)

        # Check if a key is pressed
        elif event.type == pygame.KEYDOWN:
            if startActive:
                # If in start menu and game mode is selected when enter is pressed start game
                if (button4x4Pressed or button6x6Pressed) and event.key == pygame.K_RETURN:
                    if str(text) != '':
                        name = str(text)
                    gameScore.setUserName(name)
                    startActive = False
                    gameStarted = True

                    # Set time depending on game mode
                    if button4x4Pressed:
                        gameTimeRemaining = GAME_INITIAL_TIME_45
                    elif button6x6Pressed:
                        gameTimeRemaining = GAME_INITIAL_TIME_120

                    # Start game timer
                    pygame.time.set_timer(GAME_TIMER_EVENT, 1000)

                # Delete character from name if backspace pressed
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                # Set position of input text box depending on text length
                elif event.unicode.isalpha():
                    textWidth = font.size(text)[0]
                    if textWidth <= 500:
                        text += event.unicode
                        if textWidth >= 200:
                            inputBox.x -= 10

        # Once game is started, if mouse button is clicked call flipCard
        if gameStarted and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            flipCard()

        # Timer handling for flipping cards back
        if event.type == CARD_TIMER_EVENT:
            cardTimeRemaining -= 1

            # Once both cards have been shown for 2 seconds, check if match
            if cardTimeRemaining <= 0:
                # If cards don't match flip them back
                if not isMatch(card1, card2):
                    flipCardBack()

                # Reset amount of flipped cards and card timer
                flippedCount = 0
                pygame.time.set_timer(CARD_TIMER_EVENT, 0)
                cardTimeRemaining = CARD_INITIAL_TIME

        # If game board is cleared, set running to false to stop program
        if (button4x4Pressed and gamePoints == 16) or (button6x6Pressed and gamePoints == 36):
            running = False

        # If time runs out, clear board then set running to false to end program
        if event.type == GAME_TIMER_EVENT:
            gameTimeRemaining -= 1
            if gameTimeRemaining <= 0:

                for i in range((len(cardDeck.cards) * 2)):
                    if not cardDeck.isEmpty():
                        cardDeck.pop()
                running = False

    # Fill background with white
    canvas.fill(WHITE)

    # Blit start button to screen on start
    if not startActive and startButton is not None:
        canvas.blit(startButton, startButtonRect)

    # Blit high score button to screen on start
    if not startActive and hiScoreButton is not None:
        canvas.blit(hiScoreButton, hiScoreButtonRect)

    # If high score button selected, remove unnecessary buttons and display top 3 scores
    if hiScorePressed:
        canvas.fill(WHITE)
        hiScoreButton = None
        hiScoreButtonRect = None
        startButton = None
        startButtonRect = None

        # Reinitialize score variables
        scoreTxt = hiScoreTxtFont.render(hiScoreTxt, True, "black")
        scoreTxtWidth, scoreTextHeight = hiScoreTxtFont.size(hiScoreTxt)
        scoreTxtX = (WINDOW_X - scoreTxtWidth) // 2
        scoreTxtY = 50
        canvas.blit(scoreTxt, (scoreTxtX, scoreTxtY))
        canvas.blit(backButton, backButtonRect)

        # Get scores and set their start pos
        highScores = gameScore.getHighScore()
        highestTextY = scoreTxtY + 75
        scoreCt = 1
        scoreFontSize = 72

        # Get names and scores from high score file

        if not highScores == "No High Scores Yet":
            for name, score in highScores:
                # Determine the color and position based on the rank
                scoreFont = pygame.font.Font(None, scoreFontSize)
                colorRank = min(scoreCt, len(scoreColors))
                scoreColor = scoreColors[colorRank]
                highestTxt = scoreFont.render(f"{name} | {score}", True, scoreColor)
                highestTxtWidth, highestTxtHeight = scoreFont.size(f"{name} - {score}")
                highestTextX = (WINDOW_X - highestTxtWidth) // 2
                canvas.blit(highestTxt, (highestTextX, highestTextY))

                # Update position, rank, and font size
                highestTextY += highestTxtHeight + 25
                scoreCt += 1
                scoreFontSize -= 16
        else:
            noScoresFont = pygame.font.Font(None, scoreFontSize)  # Choose an appropriate font size
            noScoresTxt = noScoresFont.render("No Scores Yet", True, "black")  # White color
            noScoresTxtWidth, noScoresTxtHeight = noScoresFont.size("No Scores Yet")
            noScoresTextX = (WINDOW_X - noScoresTxtWidth) // 2
            canvas.blit(noScoresTxt, (noScoresTextX, highestTextY))

    # If back button pressed, reset start screen
    if backButtonPressed:
        startActive = False
        hiScorePressed = False
        backButtonPressed = False
        startButton = pygame.transform.scale(startImg, (200, 200))
        startButtonRect = startButton.get_rect(center=((WINDOW_X // 2), (WINDOW_Y // 2) - 100))
        hiScoreButton = pygame.transform.scale(hiScoreImg, (200, 200))
        hiScoreButtonRect = hiScoreButton.get_rect(center=((WINDOW_X // 2), (WINDOW_Y // 2) + 100))

    # When start is pressed display game mode selection menu
    if startActive:
        canvas.fill(WHITE)
        startButton = None
        startButtonRect = None
        hiScoreButton = None
        hiScoreButtonRect = None

        # Blit game mode buttons to screen
        canvas.blit(button4x4, button4x4Rect)
        canvas.blit(button6x6, button6x6Rect)
        canvas.blit(backButton, backButtonRect)
        txtSurface = font.render(text, True, color)

        # Display input text box
        textWidth = max(200, txtSurface.get_width() + 10)
        inputBox.w = textWidth
        canvas.blit(txtSurface, (inputBox.x + 5, inputBox.y + 7))
        pygame.draw.rect(canvas, color, inputBox, 2)
        canvas.blit(nameTxt, (nameTxtX, nameTxtY))

    # When 4x4 is selected display game mode selection
    if button4x4Pressed and startActive:
        canvas.blit(selected4x4Txt, (375, 200))

    # When 6x6 is selected display game mode selection
    if button6x6Pressed and startActive:
        canvas.blit(selected6x6Txt, (375, 200))

    # When game is started remove unnecessary buttons and blit cards and game timer
    if gameStarted:
        # Remove game mode buttons
        button4x4 = None
        button6x6 = None

        # Draw all cards
        for i, card in enumerate(cardDeck.cards):
            card.draw(canvas)

        # Display timer
        font = pygame.font.Font(None, 36)
        gameTimerTxt = font.render(f"Game Time Remaining: {gameTimeRemaining} seconds", True, pygame.Color("black"))
        gameTimerTxtWidth, gameTimerTxtHeight = font.size(f"Game Time Remaining: {gameTimeRemaining} seconds")
        gameTimerTxtX = (WINDOW_X - gameTimerTxtWidth) // 2
        canvas.blit(gameTimerTxt, (gameTimerTxtX, 10))

    # Update game screen
    pygame.display.flip()

# Write score to file if greater than 0
if gamePoints > 0:
    if button4x4Pressed:
        # Calculate score base on amt of matches and time left
        gamePoints = gamePoints * (1 + (gameTimeRemaining / GAME_INITIAL_TIME_45))
    elif button6x6Pressed:
        # Calculate score base on amt of matches and time left
        gamePoints = gamePoints * (1 + (gameTimeRemaining / GAME_INITIAL_TIME_120))

    # Set score to calculated final score
    gameScore.setScore(gamePoints)

    # Write name and score to txt file
    gameScore.writeScore()

# Close game
print("Game Over!")
pygame.quit()
sys.exit()
