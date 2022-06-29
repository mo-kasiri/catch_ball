import pygame
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
import random
from pygame import mixer

width = 1366
height = 768

# opencv code
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Initialize the pygame
pygame.init()

# background sounds
mixer.music.load('music/background.mp3')
mixer.music.play(loops=-1)

closedHand_sound = mixer.Sound('music/slap.mp3')
catching_sound = mixer.Sound('music/catching_sound.wav')

# Define the screen
screen = pygame.display.set_mode((width, height))

# Timer
clock = pygame.time.Clock()
currentTime = 1

# Title and Icon
pygame.display.set_caption("Catch Ball")
icon = pygame.image.load('images/ball_32.png').convert_alpha()
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load('images/tennisBack.png').convert()

# Player
playerPosition = [370, 480]
playerMovement = [0, 0]
x = width/2 - 64
y = height/2 - 64
openHandImg = pygame.image.load('images/openHand.png').convert_alpha()
openHandImg = pygame.transform.scale(openHandImg, (128, 128))
openHand_rect = openHandImg.get_rect(topleft=(x, y))

closedHandImg = pygame.image.load('images/closedHand.png').convert_alpha()
closedHandImg = pygame.transform.scale(closedHandImg, (128, 128))
closedHand_rect = closedHandImg.get_rect(topleft=(x, y))

# Insects
InsectImg = []
InsectX = []
InsectY = []
insect_rect = []
insectMoveX = []
insectMoveY = []
numberOfInsects = 10
for i in range(numberOfInsects):
    InsectX.append(random.randint(0, 1366))
    InsectY.append(random.randint(0, 768))
    InsectImg.append(pygame.image.load('images/ball_32.png').convert_alpha())
    #InsectImg.append(pygame.transform.scale(InsectImg, (32, 32)))
    insect_rect.append(InsectImg[i].get_rect(topleft=(InsectX[i], InsectY[i])))
    insectMoveX.append(10)
    insectMoveY.append(8)

## Game Texts
 # Score Text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
gameOver_font = pygame.font.Font('freesansbold.ttf', 100)
textX = 10
textY = 10
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_timer():
    if currentTime/1000 >= 80:
        timer = font.render("Time: " + str(int(101 - currentTime / 1000)), True, (255, 0, 0))
    else:
        timer = font.render("Time: " + str(int(101 - currentTime/1000)), True, (255, 255, 255))
    screen.blit(timer, (1210, 10))
    if currentTime / 1000 >= 100:
        gameOver = gameOver_font.render("Game Over!", True, (255, 0, 0))
        screen.blit(gameOver, (width/2 - 300, height/2 - 30))


indexes_for_closed_fingers = [8, 12, 16, 20]
################################################################################################## Game Loop
catch_insect_with_openHand = False
fingers = [0, 0, 0, 0]
while True:
    # Game code
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    # opencv code
    success, frame = cap.read()
    # Mediapipe code for hand detection and Landmarks
    hands, frame = detector.findHands(frame)

    # Landmarks value - (x,y,z) * 21
    if hands:
        #Get the first hand detected
        lmList = hands[0]
        positionOfTheHand = lmList['lmList']
        openHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
        openHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
        closedHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
        closedHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5

        ## open or closed hand
        hand_is_closed = 0 #for playing the sound once when hand is closed
        for index in range(0, 4):
            if positionOfTheHand[indexes_for_closed_fingers[index]][1] > positionOfTheHand[indexes_for_closed_fingers[index] - 2][1]:
                fingers[index] = 1
            else:
                fingers[index] = 0
            if fingers[0]*fingers[1]*fingers[2]*fingers[3]:
                # playing close hand sound
                if hand_is_closed and catch_insect_with_openHand == False:
                    closedHand_sound.play()
                hand_is_closed = 0
                screen.blit(closedHandImg, closedHand_rect)
                # detect catching
                for iteration in range(numberOfInsects):
                    if openHand_rect.colliderect(insect_rect[iteration]) and catch_insect_with_openHand:
                        score_value += 1
                        catching_sound.play()
                        catch_insect_with_openHand = False
                        insect_rect[iteration] = InsectImg[iteration].get_rect(topleft=(random.randint(0, 1366), random.randint(0, 768)))

                catch_insect_with_openHand = False
            else:
                screen.blit(openHandImg, openHand_rect)
                hand_is_closed = 1
                for iterate in range(numberOfInsects):
                    if openHand_rect.colliderect(insect_rect[iterate]):
                        catch_insect_with_openHand = True





    # Opencv Screen
    #frame = cv2.resize(frame, (0, 0), None, 0.3, 0.3)
    cv2.imshow("webcam", frame)

    # Game screen
    ## placing Insects

    ## moving Insects
    for i in range(numberOfInsects):
            # moving X
        insect_rect[i].right += insectMoveX[i]
        if insect_rect[i].right <= 16:
            insectMoveX[i] += 10
        elif insect_rect[i].right >= width:
            insectMoveX[i] -= 10

            # moving Y
        insect_rect[i].top += insectMoveY[i]
        if insect_rect[i].top <= 0:
            insectMoveY[i] += 8
        elif insect_rect[i].top >= height-32:
            insectMoveY[i] -= 8
        screen.blit(InsectImg[i], insect_rect[i])

    # showing texts
    show_score(textX, textY)
    currentTime = pygame.time.get_ticks()
    show_timer()

    # display update
    pygame.display.update()
    clock.tick(60)




