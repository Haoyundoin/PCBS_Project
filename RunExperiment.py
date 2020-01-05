# PCBS Project Haoyun LIU

""" Attentional Blinking in Space and Time: This code reproduces and extends the experiment from
(Kristjánsson & Nakayama, 2002). It is a visual detection task and requires Qt Designer to run.
The experimental data is stored in a separate .csv file located in the same folder. Each participant corresponds
to a single line. """


from uiStuff import *
from FunModule import *
from random import *
from math import *

# Create stimuli
ui.alphabetList = []
# Alphabet letters, reinitialise every run as letters are deleted when picked
for letter in range(65, 91):
    ui.alphabetList.append(chr(letter))

ui.numberList = list(range(2, 10))  # Selects numbers from 2 to 9 as targets


########################################################################################################################

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

########################################################################################################################

# Initialise lists to keep track of conditions and store variables
ui.positionList = []    # record of difference in position between the two targets
ui.previousList = []    # previously chosen letters to avoid same letter in the same position two frames in a row
ui.lagList = []         # record of differences in frame number between targets
ui.labelsList = []      # list of labels created
ui.dataList = []        # list of results per participant
ui.lengths = []         # list of distances between streams of stimuli in units


# Counters
ui.trialCount = 0
ui.frameCount = 0
ui.answerCount = 0

# Set full screen
window.showFullScreen()
ui.swPages.setCurrentIndex(0)


# LAYOUT
# Get window and page dimensions
ui.pageCentreWidth = ui.swPages.width()/2
ui.pageHeight = ui.swPages.height()
windowWidthC = window.width()/2
windowHeightC = window.height()/2

# Centre widgets
# Pages
pagesGeometry = QRect(windowWidthC - ui.pageCentreWidth, windowHeightC-ui.pageHeight/2, ui.pageCentreWidth*2, ui.pageHeight)
ui.swPages.setGeometry(pagesGeometry)

# Black background box of frames
boxWidth = ui.radius * 3  # size of box varies with radius
boxHeight = ui.radius * 3
boxGeometry = QRect(ui.pageCentreWidth-boxWidth/2, ui.pageHeight/2-boxHeight/2, boxWidth, boxHeight)
ui.lblBox.setGeometry(boxGeometry)
ui.lblBox.show()

# Fixation Point
ui.sizeFont = QFont()
ui.sizeFont.setPointSize(36)
ui.lblFixPoint.setFont(ui.sizeFont)  # Setting font to size 36
ui.lblFixPoint.setAlignment(Qt.AlignCenter)
fixWidth = 31
fixHeight = 41
fixXaxis = ui.pageCentreWidth - fixWidth/2
fixYaxis = ui.pageHeight/2 - fixHeight/2
fixGeometry = QRect(fixXaxis, fixYaxis, fixWidth, fixHeight)
ui.lblFixPoint.setGeometry(fixGeometry)

# Title centre top
titleWidth = 121
titleHeight = 16
titleX = ui.pageCentreWidth - titleWidth/2
titleY = titleHeight
titleGeometry = QRect(titleX, titleY, titleWidth, titleHeight)
ui.lblConsent.setGeometry(titleGeometry)
ui.lblDemographics.setGeometry(titleGeometry)
ui.lblInstructions.setGeometry(titleGeometry)
ui.lblDebrief.setGeometry(titleGeometry)

ui.lblPractice.move(titleX, ui.lblBox.y()-25)  # use move method if no need to resize
ui.lblPractice2.move(titleX, ui.lblBox.y()-25)

# Buttons bottom right
btnGeometry = QRect(600, 450, 90, 30)
ui.btnConfirm.setGeometry(btnGeometry)
ui.btnSubmit.setGeometry(btnGeometry)
ui.btnNext.setGeometry(btnGeometry)


# Textboxes centre
textWidth = 600
textHeight = 200
textX = (ui.swPages.width()-textWidth)/2
textY = titleHeight*2 + 10
textGeometry = QRect(textX, textY, textWidth, textHeight)
ui.lblTandC.setGeometry(textGeometry)
ui.wgForm.setGeometry(QRect(textX + ui.swPages.x()/2, textY, textWidth, textHeight))
ui.lblDescription.setGeometry(textGeometry)
ui.lblExample.setGeometry(QRect((ui.swPages.width()-180)/2, ui.lblDescription.y()+textHeight+10, 180, 180))
ui.lblQuestion.setGeometry(textGeometry)
ui.lblThanks.setGeometry(textGeometry)

# Place answer labels
answerX = 200
ui.lblAnswer1.setGeometry(QRect(answerX,ui.pageHeight/2,titleWidth, titleHeight))  # set relative to page leftx and page right x
ui.lblErrorDigit.move(answerX+titleWidth, ui.pageHeight/2-titleHeight)
ui.lblEntry1.setGeometry(QRect(answerX,ui.pageHeight/2+titleHeight,titleWidth, titleHeight))
ui.lblAnswer2.setGeometry(QRect(ui.swPages.width()-answerX-titleWidth, ui.pageHeight/2, titleWidth, titleHeight))
positionX=ui.swPages.width()-answerX-titleWidth
ui.lblEntry2.setGeometry(QRect(positionX, ui.pageHeight/2+titleHeight, titleWidth, titleHeight))


#############
# FUNCTIONAL
# create .csv summary file in the append mode so previous data entries remain
ui.data = open('attentionalBlink.csv', 'a')
readData = open('attentionalBlink.csv', 'r')
listData = readData.readlines()

# Write column names
if len(listData) == 0:
    ui.data.write('Name, Age, Gender, Education, Email, Trial no, Time(s), Distance(sides), Distance(ui units), '
                  'Outcome 1, Outcome 2,\n')


# List of equidistant labels positioned in a circle around the fixation point
ui.shift = randint(0, 360)  # selects random float, representing shift degree in radians
ui.vertices = createPoly(ui.streams, ui.radius, ui.shift)  # choose number of sides, radius, and angle of rotation


# Create labels
for i in range(ui.streams):
    name = "lbl" + str(i)
    ui.name = QLabel(ui.pgExperiment)
    ui.name.setFont(ui.sizeFont)
    ui.name.resize(31, 31)
    ui.lblHeight = ui.name.height()
    ui.lblWidth = ui.name.width()
    ui.name.setAlignment(Qt.AlignCenter)
    ui.name.show()
    ui.labelsList.append(ui.name)  # list of labels so they are accessible


# List of numbers to choose targets and frames where they appear from


# CONSENT
# Ensures the conditions are clear and understood before experiment begins
ui.btnConfirm.clicked.connect(consentCheck)


# HIDING and SHOWING
# Hide all stimuli
labelHide()

# Display practice title depending on boolean
ui.lblPractice.hide()
ui.lblPractice2.hide()



# Hide all specific error labels
ui.lblErrorName.hide()
ui.lblErrorGender.hide()
ui.lblErrorEduc.hide()
ui.lblErrorAge.hide()
ui.lblErrorEmail.hide()
ui.lblErrorDigit.hide()
ui.lblError0.hide()


# DEMOGRAPHICS
ui.btnSubmit.clicked.connect(errorCheck)


# INSTRUCTIONS
# Adapt on screen instructions to the particular conditions of the experiment
description = "In each trial, you will be shown {0} consecutive frames with {1} elements " \
              "placed in a circle around the fixation dot, as seen in the image below:\n\n" \
              "In every trial, there will be 2 random frames which contain one number. " \
              "The aim is for you to remember the numbers hidden among the letters " \
              "and input them at the end of each trial."

# Append practice trial instructions if they are happening
if ui.practiceTrial is True:
    pracDescription = "\nYou will get {2} practice trial(s) at the beginning, where your results will not be recorded"
    description += pracDescription
    ui.lblDescription.setText(description.format(ui.framesMax, ui.streams, ui.practiceNumber))
else:
    ui.lblDescription.setText(description.format(ui.framesMax, ui.streams))

ui.btnNext.clicked.connect(nextPage)


# EXPERIMENT
ui.btnNext.clicked.connect(startTrial)  # triggers connected functions which run the whole experiment


# ANSWERS
ui.entriesList = [ui.lblEntry1, ui.lblEntry2]

ui.lblEntry1.hide()
ui.lblEntry2.hide()


# Create widget that is keyboard-sensitive for participant to type in answer
class KeyboardWidget (QWidget):
    keyPressed = pyqtSignal(str)

    def keyPressEvent(self, keyEvent):
        self.keyPressed.emit(keyEvent.text())


ui.myWidget = KeyboardWidget(ui.pgAnswer)
ui.myWidget.setGeometry(40, 40, 500, 500)
ui.myWidget.keyPressed.connect(getAnswer)


# DATA COLLECTION
# Calculate distance between vertice 0 and all the remaining vertices in the polygon
for i in range(len(ui.vertices)):
    x0 = ui.vertices[0][0]
    y0 = ui.vertices[0][1]
    xi = ui.vertices[i][0]
    yi = ui.vertices[i][1]
    length = hypot(xi-x0, yi-y0)    # distance is the hypotenuse between positions
    ui.lengths.append(length)       # stores the lengths between all vertices


# displays UI window
window.show()

sys.exit(app.exec_())