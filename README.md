# PCBS_Project: The Attentional Blink in Visual Perception
## Table of Contents 
  * [Background](#background)
  * [Aim](#aim)
  * [Procedure Outline](#procedure-outline)
  * [User’s Guide to the Code](#user-s-guide-to-the-code)
  * [Program Highlights](#program-highlights)
  * [References](#references)

## Background 
The role of attention and how it acts as a filter for visual perception has long been a topic of interest in psychology. Previous experiments showed effects such as inattentional blindness, whereby a stimulus or a change in the stimulus are not perceived in moments of inattention, suggest attention is necessary for perception. Subsequent experiments investigating how attention modulates perception reported periods of inattention in Rapid Serial Visual Presentation (RSVP), as detection of a second target was poor if it is presented within a certain time interval following the first target, a phenomenon which the research group coined “attentional blink” (Raymond, Shapiro & Arnell, 1992). This suggests the presence of a refractory period after presentation of a target, during which we are blind to any new targets presented. This experiment is adapted from a paper by Kristjansson and Nakayama, where they design a paradigm to investigate the attentional blink (Kristjánsson & Nakayama, 2002). They made an experiment to look at time and also spatial relationships between the targets. The space variable in perception is interesting as visual attention is often referred to as “spotlight-like”, meaning a gaussian curve applies to focus and resolution, which is maximal at the centre and falls in the edges of visual attention. 

## Aim 
Understanding the relationship between attention and perception, specifically the temporal and spatial properties of the attentional blink (AB) in visual perception.

## Methods
(This section refers to default setting values, but these can easily be modified in the code.)
The paradigm used is an RSVP task. Each frame presents seven streams of upper-case letters (distractors) equally spaced in a circle around a central fixation cross, on a black square background. 

![Image of stimulus](exampleFrame.png)

### Collecting Participant Information
The experiment starts by obtaining participant consent to the terms and conditions, following by collecting some personal information (age, gender, education level...). Error messages appear if the inputs are incomplete (*consentCheck* & *errorCheck*). Various functions are defined to enable navigation between pages
```python
def nextPage():  # incrementally increases page number
    currentPage = ui.swPages.currentIndex()
    ui.swPages.setCurrentIndex(currentPage + 1)


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
```


### Create stimuli
Stimuli consist of distractors (capital letters) and targets (numbers 2-9). 
```python 
ui.alphabetList = []
    for letter in range(65, 91):
        ui.alphabetList.append(chr(letter))

ui.numberList = list(range(2, 10))
```
### Stimuli Presentation
Distractors (letters) are randomly selected from the alphabet using the *pickDistractors* function and change every 140ms but the positions of the streams of letters remained the same within the same trial. 

```python
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
```

For each trial, 30 frames are presented, within which two integers (targets), T1 and T2, are randomly chosen from 2-9, using the *pickTargets* function and their position is arbitrarily determined every time (1 is omitted due to its resemblance to the letter I).
The targets appear between frames 10 and 25 (so that they are flanked by frames showing distractors only). The time gap between T1 one T2 varies from 1 to 6 frames (149-840ms, *showStimuli*), and their relative positions change every trial (*getDistance*), to measure the effect of temporal and spatial properties on the attentional blink effect.

```python
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


def showStimuli():
    ui.framesTimer = QTimer()
    ui.framesTimer.start(ui.interval)
    ui.framesTimer.timeout.connect(pickDistractors)  # changes letters each frame
    ui.framesTimer.timeout.connect(endTrial)  # checks if max frame has been reached
    ui.framesTimer.timeout.connect(showTarget)


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
```

### Defining a Trial
At the start of each trial, the randomised variables need to be reset using *startTrial*, and the 

```python
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
```


### Participant Response 
In each trial, the participant is shown 30 frames, and once the sequence presentation is over, the computer asks them to type in the two digits that appeared in the previous trial. The answers are displayed on the screen (*showAnswer*) giving them feedback after both answers have been inputted (*checkAnswer*), by coloring the answer red if incorrect and green if correct. They were prompted to guess when unsure but press “0” if they did not want to guess. The accuracy of answers is stored under ui.result1/2 (*getAnswer).

```python
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
```

## User’s Guide to the Code
This code requires the PyQt library to run. PyQt was chosen because it is very powerful in creating user interfaces and can allow for a simpler and more natural interaction between the participant and the computer task. Instructions on how to install PyQt can be found [here](https://doc.bccnsoft.com/docs/PyQt5/installation.html).
The folder PCBS_Project contains all the necessary elements to run the experiment. “FunModule.py” contains all the functions, and the code the experimenter needs to run is called “RunExperiment.py”. "DesignerCode.py" contains the python code for all the settings established in Designer, and "DesignerFile.ui" is the file used to directly edit the user interface in Designer (a what you see is what you get UI editor). 

In RunExperiment.py, the code begins by importing all the relevant modules used later on.

```python
from uiStuff import *  # settings required for displaying UI
from FunModule import *  # all functions are stored here
from random import *
from math import *
```

All the experimental settings can be found at the beginning of this file and can be modified to the experimenter’s preferences, without needing any changes in the rest of the code. 

```python
# VARIABLES
# Initialised all modifiable parameters so the experiment is easier to customise, 'ui.' prefix makes them accessible
ui.streams = 7      # number of sides of the polygon = number of stimuli presented simultaneously
ui.radius = 180     # size of polygon, distance from fixation cross
ui.interval = 140   # time (milliseconds) between each frame
ui.framesMax = 30   # number of frames per trial
ui.trialMax = 7     # number of trials per block

# Set practice trials
ui.practiceTrial = True     # set to True if you want practice trials, and False if not
ui.practiceNumber = 1       # set number of practice trials

# Set stimuli
ui.distractors = ui.alphabetList
ui.targets = ui.numberList
```

The raw data is stored in a file named “data.csv”, located in the same folder as the programme. The format is one line per trial, and the conditions, difference in time (milliseconds) and position of the targets (in terms of number of polygon sides between the targets and absolute distance in Qt Designer units), which were randomly selected by the computer, will be specified, along with the accuracy of the participant’s answers (0 for incorrect and 1 for correct).


```python
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
```


The advantage of the programme is it allows for different numbers of streams to appear on screen. The createPoly function uses methods from the math module to automatically create coordinates for the vertices for a polygon along a circle of custom radius, and allowing for random degree of rotation at each trial (so that the vertices can be randomly placed along the circle and there is not always a label on the Y axis, for example. 

```python
def createPoly(n, r, s):  # creates list with coordinates for a polygon of n sides, radius r and shift s
    coordinates = []               # adapted from https://stackoverflow.com/questions/35316781/drawing-a-polygon-in-pyqt
    w = 360/n                      # angle per step
    for i in range(n):
        t = w*i + s
        x = r*math.cos(math.radians(t))
        y = r*math.sin(math.radians(t))
        coordinates.append([y, x])  # stores x and y coordinates in a list of lists
    return coordinates
```
This adds a lot of flexibility to the experiment, as the experimenter might be interested in the effect of changing visual load on the attentional blink. By changing one variable, ui.streams (the number of streams hence the number of sides to the polygon), the code adapts by creating that exact number of labels to then hold the distractors and targets. A set of variables initialised at the beginning of the program, to allow for flexible modifications such as the speed of the frames, the number of frames per trial, and the number of trials. There is also the option to add any number of practice trials. The stimuli (currently capital letters from the whole alphabet and numbers 2-9) can also be changed by creating new lists. There is no need to press buttons once the experiment has started, automatic page chances following timers and keypresses. 

Randomisation occurs on 3 levels: the rotation of the polygon on the circle, the time delay between the two targets appearing and physical distance between the two targets. The conditions are sampled evenly (so all conditions occur if number of trials = number of conditions) so even if the number of trials isn’t an exact multiple of the number of conditions, the same condition isn’t repeated until all conditions have been tested.

## Future Directions
Given more time, it would have been interesting to allow the experimenter to define blocks of trials with different settings (milliseconds interval between stimuli, size of stimuli, number of stimuli) as the experiment is currently fixed on one set of variables every time it is run. Furthermore, the data is now simply stored in a .csv file, but an additional step would have been to write a script to analyse the data using statistical tests.

## References
Kristjánsson, Á. and Nakayama, K., 2002. The attentional blink in space and time. Vision research, 42(17), pp.2039-2050.
Raymond, J.E., Shapiro, K.L. and Arnell, K.M., 1992. Temporary suppression of visual processing in an RSVP task: An attentional blink?. Journal of experimental psychology: Human perception and performance, 18(3), p.849.
