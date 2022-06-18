import pygame
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

width = 1366
height = 768

# opencv code
cap = cv2.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)


# Initialize the pygame
pygame.init()

# Define the screen
screen = pygame.display.set_mode((width, height))

# Title and Icon
pygame.display.set_caption("Mamad Game")
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)

# Player
playerImgCrude = pygame.image.load('images/spaceship.png')
playerImg = pygame.transform.scale(playerImgCrude, (64, 64))

#playerX = 370
#playerY = 480
playerPosition = [370, 480]

def player(playerPosition):
    x = playerPosition[0]
    y = playerPosition[1]
    screen.blit(playerImg, (x, y))


# Game Loop
#running = True
while True:
    # Game code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()


    success, frame = cap.read()
    #print(frame.shape)

    # Mediapipe code for hand detection and Landmarks
    hands, frame = detector.findHands(frame)

    # Landmarks value - (x,y,z) * 21
    if hands:
        #Get the first hand detected
        lmList = hands[0]
        #print(lmList['lmList'])
        #print(lmList['bbox'])
        #print(hands[0])
        positionOfTheHand = lmList['lmList']
        playerPosition[0] = positionOfTheHand[9][0]
        playerPosition[1] = positionOfTheHand[9][1]
    # Opencv Screen
    #frame = cv2.resize(frame, (0, 0), None, 0.3, 0.3)
    cv2.imshow("webcam", frame)

    # Game screen
    screen.fill((50, 10, 100))

    # moving the Player
    player(playerPosition)

    # display update
    pygame.display.update()




