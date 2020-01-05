""" This module contains all the functions necessary to run the Attentional Blink experiment."""

from uiStuff import *
from random import *
import math
import time


def nextPage():  # incrementally increases page number
    currentPage = ui.swPages.currentIndex()
    ui.swPages.setCurrentIndex(currentPage + 1)


def labelHide():  # hide all streams before experiment begins
    for label in ui.labelsList:
        label.hide()


def delayTimer(milliseconds, change):  # call a function after a custom delay period
    ui.oneTimer = QTimer()
    ui.oneTimer.singleShot(milliseconds, change)


def createPoly(n, r, s):  # creates list with coordinates for a polygon of n sides, radius r and shift s
    coordinates = []               # adapted from https://stackoverflow.com/questions/35316781/drawing-a-polygon-in-pyqt
    w = 360/n                      # angle per step
    for i in range(n):
        t = w*i + s
        x = r*math.cos(math.radians(t))
        y = r*math.sin(math.radians(t))
        coordinates.append([y, x])  # stores x and y coordinates in a list of lists
    return coordinates


def consentCheck():  # displays error message if terms and conditions aren't accepted
    if ui.chbAgree.isChecked():
        nextPage()
    else:
        ui.lblError0.show()


def errorCheck():  # displays specific error message for each field in the form
    demogCount = 0
    if ui.leName.text() == "":
        ui.lblErrorName.show()
    else:
        ui.lblErrorName.hide()
        demogCount += 1

    if ui.sbAge.value() == 0:
        ui.lblErrorAge.show()
    elif ui.sbAge.value() < 18:
        ui.lblErrorAge.setText("You must be at least 18 years old")
        ui.lblErrorAge.show()
    else:
        ui.lblErrorAge.hide()
        demogCount += 1

    if ui.cbEducation.currentIndex() == 0:
        ui.lblErrorEduc.show()
    else:
        ui.lblErrorEduc.hide()
        demogCount += 1

    if not (ui.rbtnWoman.isChecked() or ui.rbtnMan.isChecked() or ui.rbtnOther.isChecked()):  # returns integers
        ui.lblErrorGender.show()
    else:
        ui.lblErrorGender.hide()
        demogCount += 1

    if ui.leEmail.text() == "":
        ui.lblErrorEmail.show()
    elif '@' not in ui.leEmail.text():
        ui.lblErrorEmail.setText("Please enter a valid email address")
        ui.lblErrorEmail.show()
    else:
        ui.lblErrorEmail.hide()
        demogCount += 1

    window.repaint()  # mac issue

    if demogCount == 5:  # counter makes sure all fields are filled and accepted
        nextPage()


def pickTarget():  # picks targets and assigns frame numbers
    ui.targetsChosen = []               # empty out list of chosen targets (for checking answers later on)
    ui.targetList = ui.targets.copy()   # create a copy of the original stimuli list otherwise it also becomes modified
    ui.T1 = choice(ui.targetList)
    ui.targetsChosen.append(ui.T1)
    ui.targetList.remove(ui.T1)         # deletes chosen item so targets are different
    ui.T2 = choice(ui.targetList)
    ui.targetsChosen.append(ui.T2)

    framesT1List = list(range(10,25))   # digits were only presented from frame 13-25
    ui.frameT1 = choice(framesT1List)
    ui.frameT2 = ui.frameT1 + randint(1,6)      # difference between T1 and T2 limited to 1-6frames
    if ui.frameT2 > 25:                 # cannot go above frame 25
        ui.frameT2 = 25

    ui.diffFrame = ui.frameT2 - ui.frameT1  # calculate frame difference in order to sample

    if len(ui.lagList) == 6:  # empty list of frame differences when all possibilities have been sampled
        ui.lagList = []

    if ui.diffFrame in ui.lagList:  # chooses frames again (limited to 13-25, so if T1 is 24 T2 can only be 25)
        pickTarget()
    else:
        ui.lagList.append(ui.diffFrame)


def showTarget():  # displays target numbers on a randomly selected frame and position
    if ui.frameCount == ui.frameT1:
        ui.labelT1 = choice(ui.labelsList)
        ui.index1 = ui.labelsList.index(ui.labelT1)
        ui.labelT1.setText(str(ui.T1))
        ui.labelT1.setStyleSheet('color: white')  # brightness of targets is higher than distractors
    elif ui.frameCount == ui.frameT2:
        ui.diffPosition = randint(0,len(ui.labelsList))  # randomise position by choosing an index
        if len(ui.positionList) == len(ui.labelsList):  # if all the positions have been sampled, empty list, start over
            ui.positionList = []

        ui.positionList.append(ui.diffPosition)
        ui.index2 = ui.index1 + ui.diffPosition

        if ui.index2 > len(ui.labelsList)-1:  # if index becomes out of range, start counting from 0 again
            ui.index2 = ui.index2 - len(ui.labelsList)-1

        ui.labelT2 = ui.labelsList[ui.index2]
        ui.labelT2.setText(str(ui.T2))
        ui.labelT2.setStyleSheet('color: white')


def pickDistractors():  # (iterations, list), randomly selects letter from alphabet as a distractor stimulus
    ui.frameCount += 1
    ui.distractorList = ui.distractors.copy()  # create a copy of the original list otherwise it also becomes modified

    for i in range(ui.streams):  # randomly selects letter from alphabet for each stream
        distractor = choice(ui.distractorList)
        if ui.frameCount > 1:
            while distractor == ui.previousList[(ui.frameCount-2) * ui.streams + i]:  # cant be in the same position 2x
                distractor = choice(ui.distractorList)
        ui.labelsList[i].setText(distractor)
        ui.labelsList[i].setStyleSheet('color: lightGray')
        ui.labelsList[i].show()
        labelGeometry = QRect(ui.pageCentreWidth + ui.vertices[i][0] - ui.lblWidth/2,
                              ui.pageHeight/2 - ui.vertices[i][1] - ui.lblHeight/2, ui.lblWidth, ui.lblHeight)
        ui.labelsList[i].setGeometry(labelGeometry)  # applying the equidistant geometry
        ui.previousList.append(distractor)
        ui.distractorList.remove(distractor)


def getDistance():  # Calculates distance in terms of number of sides between T1 and T2 and absolute distance in units
    indexT1 = ui.labelsList.index(ui.labelT1)
    indexT2 = ui.labelsList.index(ui.labelT2)
    if indexT1 < indexT2:
        diffIndex = indexT2 - indexT1
        diffAdjust = indexT2 +ui.streams -indexT1
        listIndex = [diffIndex,diffAdjust]
        ui.distanceIndex = min(listIndex)
    else:
        diffIndex = indexT1 - indexT2
        diffAdjust = indexT1 + ui.streams - indexT2
        listIndex = [diffIndex, diffAdjust]
        ui.distanceIndex = min(listIndex)  # actual distance (in sides) once circularity and symmetry taken into account
    ui.distanceUnits = ui.lengths[ui.distanceIndex]  # fetches previously calculated distance in pyqt units


def endTrial():  # stops showing stimuli once sequence of frames is over
    if ui.frameCount == ui.framesMax:
        ui.framesTimer.stop()
        delayTimer(ui.interval, labelHide)  # back to fixation cross
        delayTimer(1500, nextPage)          # flip to answer page
        ui.time1 = time.time()
        ui.myWidget.show()
        ui.myWidget.setFocus()  # reset focus whenever answer page is displayed otherwise keyPressEvent won’t be called
        getDistance()


def startTrial():  # reset counters for frames, pick digits again in new trial
    ui.positionList = []  # empty out list of positions otherwise run out of memory
    # List of equidistant labels positioned in a circle around the fixation point
    ui.shift = randint(0, 360)  # selects random float, representing shift degree
    ui.vertices = createPoly(ui.streams, ui.radius, ui.shift)  # choose number of sides, radius, and angle of rotation

    if ui.practiceTrial is True and ui.trialCount < ui.practiceNumber:  # indicates if the trial is a practice one
        ui.lblPractice.show()
        ui.lblPractice2.show()
    else:
        ui.lblPractice.hide()
        ui.lblPractice2.hide()
    pickTarget()
    ui.frameCount = 0
    ui.trialCount += 1
    ui.answerCount = 0
    ui.lblEntry1.hide()
    ui.lblEntry2.hide()
    delayTimer(1000, showStimuli)


def showStimuli():
    ui.framesTimer = QTimer()
    ui.framesTimer.start(ui.interval)
    ui.framesTimer.timeout.connect(pickDistractors)  # changes letters each frame
    ui.framesTimer.timeout.connect(endTrial)  # checks if max frame has been reached
    ui.framesTimer.timeout.connect(showTarget)


def newTrial():  # essentially loops over experiment until trial number has been reached
    if ui.practiceTrial is True:
        if ui.trialCount - ui.practiceNumber < ui.trialMax:
            labelHide()
            ui.swPages.setCurrentIndex(3)
            startTrial()  # automatically starts without needing to press buttons
        else:
            ui.swPages.setCurrentIndex(5)
    else:
        if ui.trialCount < ui.trialMax:  # displays stimuli until previously defined number of trials
            labelHide()
            ui.swPages.setCurrentIndex(3)
            startTrial()  # automatically starts without needing to press buttons
        else:
            ui.swPages.setCurrentIndex(5)


def showAnswer(key, index):  # displays answer on screen
    labelAnswer = ui.entriesList[index]
    labelAnswer.setStyleSheet("color: black")
    labelAnswer.setText(key)
    labelAnswer.show()
    if index == 1:
        delayTimer(1000,checkAnswer)  # did not want immediate feedback to prevent distractions
        delayTimer(3000, newTrial)


def checkAnswer():  # provides feedback on correct/incorrect
    ui.outcomeList = []  # stores accuracy of answers
    for answer in ui.entriesList:
        index = ui.entriesList.index(answer)
        if answer.text() == str(ui.targetsChosen[index]):
            ui.outcomeList.append(1)  # correct = 1
            answer.setStyleSheet("color: green")
        else:
            ui.outcomeList.append(0)  # incorrect = 0
            answer.setStyleSheet("color:red")


def getAnswer(key):  # obtains identity of key pressed, and link it to functions
    if not key.isdigit():
        ui.lblErrorDigit.show()
    else:
        ui.lblErrorDigit.hide()
        ui.answerCount += 1           # prevent proceeding onto next step if key pressed != integer
        ui.time2 = time.time()
        if ui.answerCount == 1:
            showAnswer(key, 0)
        elif ui.answerCount == 2:
            showAnswer(key, 1)
            ui.myWidget.hide()  # take away focus so the button can be clicked
            if (ui.practiceTrial is True) and (ui.trialCount <= ui.practiceNumber):
                pass
            else:
                storeData()


def storeData():  # stores variables in a list per participant every trial
    ui.name = ui.leName.text()
    ui.age = ui.sbAge.value()
    ui.education = ui.cbEducation.currentText()
    ui.email = ui.leEmail.text()
    if ui.rbtnWoman.isChecked():
        ui.gender = 0
    else:
        ui.gender = 1
    ui.diffTime = (ui.diffFrame * ui.interval)/1000  # convert frame to timer difference in seconds

    ui.result1 = ui.outcomeList[0]
    ui.result2 = ui.outcomeList[1]
    if ui.practiceTrial is True:
        ui.trialNo = ui.trialCount-ui.practiceNumber
    ui.dataList = [ui.name, str(ui.age), str(ui.gender), ui.education, ui.email, str(ui.trialNo), str(ui.diffTime),
                   str(ui.distanceIndex), str(ui.distanceUnits), str(ui.result1), str(ui.result2)]
    writeCsv()


def writeCsv():  # writes new line for each participant
    newLine = ','.join(ui.dataList)
    ui.data.write(newLine + '\n')
