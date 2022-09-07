import time
import random
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import tkinter as tk

root = Tk()
root.title("TypingGame v3.0")

# Discards the min/max window option
root.resizable(0,0)


# Specifies tkinter to open a window in the middle of the screen
w = 800
h = 700

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()


x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x ,y))


# Creates frame for tkinter window
frm = ttk.Frame(root, padding=20)
frm.grid()


# Function that separates a string into lines automatically so each line can be called easier
def lineSplicer(line):
    storyCopy = line
    CONST_CHAR_PER_LINE = 72
    newLine = ""

    while (len(storyCopy) >= CONST_CHAR_PER_LINE):
        currLine = storyCopy[:CONST_CHAR_PER_LINE]
        storyCopy = storyCopy[CONST_CHAR_PER_LINE:]
        carryWord = ""

        # Check to see if currLine ends mid-word, if it does, run the if statement
        if(currLine[CONST_CHAR_PER_LINE -1].isalpha()):
            # Remove the word and add it to the next line until the last character in the string is not an alpha character
            endIndexTracker = CONST_CHAR_PER_LINE - 1
            while(currLine[endIndexTracker].isalpha()):
                carryWord = currLine[endIndexTracker] + carryWord
                currLine = currLine[:-1]
                endIndexTracker -= 1

        # Add the carryWord back to the storyCopy
        storyCopy = carryWord + storyCopy

        # Make sure that storyCopy != 0 before calling the if statement below
        if(len(storyCopy) != 0):
        # Check to see if the line starts with a space, if it does, remove the space
            if storyCopy[0] == " ":
                storyCopy = storyCopy[1:]

        # Add the currLine to the newLine which will be returned later
        newLine = newLine + currLine + "\n"

    # Add the last line of the story to the returned string
    newLine = newLine + storyCopy
    return newLine


# Creates the text box for the main text paragraph and the actual contents within the text box + the initial setup for highlighting text
storyText = Text(frm, fg='black')
fontStyle = tkFont.Font(family="Times New Roman", size=17,)
storyText.grid(column=0, row=2, padx=(20, 20), pady=(50, 20), columnspan=6)
# Configure the font, height, width
storyText.configure(font=fontStyle, height=13, width=65)


# WPM, TIME, ACCURACY, STATUS, and DIFFICULTY labels
dataFontStyle = tkFont.Font(family="Times New Roman", size=14)

wpmLabel = ttk.Label(frm, width=20, text="WPM: N/A", )
wpmLabel.grid(column=0, row=3, padx=(20,0), pady=(5, 5))
wpmLabel.configure(font=dataFontStyle)

timeLabel = ttk.Label(frm, width=20, text="Time: N/A", )
timeLabel.grid(column=0, row=4, padx=(20,0), pady=(5,5))
timeLabel.configure(font=dataFontStyle)

accuracyLabel = ttk.Label(frm, width=20, text="Accuracy: N/A", )
accuracyLabel.grid(column=0, row=5, padx=(20,0), pady=(5,5))
accuracyLabel.configure(font=dataFontStyle)

statusLabel = ttk.Label(frm, width=20, text="Status: N/A", )
statusLabel.grid(column=0, row=6, padx=(20,0), pady=(5,5))
statusLabel.configure(font=dataFontStyle)

difficultyLabelFont = tkFont.Font(family="Times New Roman", size=11)
difficultyLabel = ttk.Label(frm, width=20, text="Difficulty:")
difficultyLabel.grid(column=5, row=5, padx=(85, 0), pady=(5, 5))
difficultyLabel.configure(font=difficultyLabelFont)


# Function that restarts the game and resets the highlighted text
# Part 1 - Actual function
def restart(event):
    global sessionStarted
    global sessionEnded
    global wrongEntriesCounter
    global totalCharactersCounter
    global startTime
    global endTime
    global elapsedTime
    global textIndexTracker
    global textLineTracker
    global textCharTracker

    sessionStarted = False
    sessionEnded = True
    wrongEntriesCounter = 0
    totalCharactersCounter = 0
    startTime = 0
    endTime = 0
    elapsedTime = 0
    textIndexTracker = 0
    textLineTracker = 1
    textCharTracker = 0

    wpmLabel.configure(text="WPM: N/A")
    timeLabel.configure(text="Time: N/A")
    accuracyLabel.configure(text="Accuracy: N/A")
    statusLabel.configure(text="Status: N/A")

    storyText.configure(fg='black')
    storyText.tag_delete('currLetterHi')
    storyText.tag_add('currLetterHi', '1.0')
    storyText.tag_configure('currLetterHi', background='SkyBlue', foreground='white')
    storyText.tag_delete('highlight')

# Part 2 - Event listener that triggers function call when clicked on
restartButton = ttk.Button(frm, width=10, text="Restart")
restartButton.grid(column=5, row=3, padx=(0,0), pady=(5,5))
restartButton.bind('<ButtonPress>', restart)


# Dropdown menu that allows you to choose which difficulty you want to play on
options = StringVar()
options.set("Select difficulty")
drop = OptionMenu(frm, options, "Easy", "Medium", "Hard")
drop.grid(column=5, row=6, padx=(10,0), pady=(5,5))

# Function that shuffles/adds story text to the screen if there is or isn't a previous story
# Part 0 - Helper function that chooses a random story
# Variable that helps the function pick a new story by keeping track of the index of the previous one
lastStoryFirstIndex = -1
lastStorySecondIndex = -1
def shuffleOrAddStoriesHelper(event):
    global lastStoryFirstIndex
    global lastStorySecondIndex
    global drop

    # 2D that stores story and their difficulty
    # Easy stories
    storyAEasy = "A boy turned off his buzzing alarm. He got out of bed and went outside and got his cloak on and became a superhero, saving people that were in trouble."
    storyBEasy = "I was sick to my stomach. \"I know how you feel.\" my boss sarcastically said. Following a straight punch to his gut I added, \"Now you do.\""
    storyCEasy = "She lifted the curtain to let in the sun, a beautiful day had begun. The clock was ticking but time stood still in her little house up on the hill."

    # Medium stories
    storyAMedium = "For every week the war goes on, I plant a row of sunflower seeds. Before long, two rows turn into a dozen. After a while, blooming" \
                   "begins. Soon, golden yellow sunflowers are everywhere. Whenever someone asks how many sunflowers have bloomed, I shake my head and say, Far too many."

    storyBMedium = "My eyes still ache. My eyes are the ocean. Pale water swirls in my irises. It's what I miss, what I crave. " \
                   "Church at 7:00 AM. Sticky petticoats, stifling dresses, sickly sweet incense. " \
                   "Home for toast and tea. Then all seven in the wagon. To merge with the silken sea."

    storyCMedium = "\"What shall we do on holiday?\" Charlie asked Marge. \"Trekking with Sherpas? Camping with the Berbers?\"" \
                   "\"Kayaking with Inuits?\" suggested Marge.Charlie and Marge loved cultural adventure; meeting strangers, making friends." \
                   "\"The house will be empty. Better tell the next door neighbour,\" warned Charlie. \"I wonder what his name is?\""

    # Hard stories
    storyAHard = "They arrived silently, swiftly during the night and stood present by morning. They flocked the fields, parking lots, and manmade" \
                 " suburban ponds. They were big. All at least three and a half feet tall, the size of an average kindergartener. Threatening. So many." \
                 " No one suspected it would be them. Their peaceful stature, impressing the image of grace and elegance in citizens' minds year after year, migration after migration." \
                 " No one suspected their teeth would grow; their eyes would turn crimson; their tempers would ascend. No one suspected that of all the potential apocalypse catalysts-it would be the geese."
    storyBHard = "Her mother never wore a sari, my mother never did not. Her mother drove a Mustang, my mother walked everywhere, even though I hated " \
                 "being picked up last. Her mother never packed her lunches, my mother packed feasts, even though I wanted greasy, stale pizza from the " \
                 "cafeteria like everyone else. Her mother allowed sleepovers, my mother trusted no one, not even friends. Her mother went on business trips," \
                 " my mother was... my mother, nothing else."
    storyCHard = "Lost rain wandering parking lots and highways in search of the earth. Down-on-its-luck rain watering plastic petunias on a twentieth-floor balcony." \
                 " Angry rain condemned to storm sewers, denied rivers. Rebellious rain. Tried to rally ducks and frogs to rise up when their marsh was bulldozed for bungalows. Didn't work. Tired rain." \
                 " Here, old neighbor rain. Fickle friend rain. Trickling deep to farmers who've become dirt, white finger bones point and skulls grumble: \"Where were you, prayed-for rain?\" Regretful rain, " \
                 "that corn withered, cattle and children went thirsty. Sorrowful, as if a downpour would help now. Dying rain, mossy and misty-eyed."


    # Make a 2D array with the index of the original array as a list of stories from easy to hard
    storyList = [[storyAEasy, storyBEasy, storyCEasy], [storyAMedium, storyBMedium, storyCMedium],
                 [storyAHard, storyBHard, storyCHard]]


    # Get the first index based on which difficulty the user selected, or random if a user has not selected a difficulty
    selectedDifficulty = drop.cget("text")

    if(selectedDifficulty == "Easy"):
        firstIndex = 0
    elif(selectedDifficulty == "Medium"):
        firstIndex = 1
    elif(selectedDifficulty == "Hard"):
        firstIndex = 2
    else:
        firstIndex = (random.randint(0, len(storyList) - 1))


    secondIndex = (random.randint(0, len(storyList[firstIndex]) - 1))

    # Loop until an index that is not equal to the last one is picked so a new story can be shown
    while(firstIndex == lastStoryFirstIndex and secondIndex == lastStorySecondIndex):
        if(selectedDifficulty != "Easy" and selectedDifficulty != "Medium" and selectedDifficulty != "Hard"):
            firstIndex = (random.randint(0, len(storyList) - 1))
        secondIndex = (random.randint(0, len(storyList[firstIndex]) - 1))

    # Helps keep track of the current story by assigning the last story to the story that will be shown on the screen, used to compare for the next event
    lastStoryFirstIndex = firstIndex
    lastStorySecondIndex = secondIndex

    shuffleOrAddStories(storyList[firstIndex][secondIndex])


# Part 1 - The actual function that shuffles/adds the story
def shuffleOrAddStories(story):
    global storyText
    storyText.configure(state=NORMAL)
    storyText.delete("1.0", "end")
    storyText.insert(tk.END, lineSplicer(story))
    restart('<ButtonPress>')
    storyText.configure(state=DISABLED)

# Add the initial story text
what = "a;lsdjfka;sl"
shuffleOrAddStoriesHelper(what)

# Part 2 - Event listener that trigger function call when clicked on
shuffleButton = ttk.Button(frm, width=10, text="New Story")
shuffleButton.grid(column=5, row=4, padx=(0,0), pady=(5,5))
shuffleButton.bind('<ButtonPress>', shuffleOrAddStoriesHelper)


# Game title label
label = ttk.Label(frm, width=20, text="TypeGamer")
label.grid(column=1, row=0, padx=5, pady=0, columnspan=6)
labelFontStyle = tkFont.Font(family="Times New Roman", size=40)
label.configure(font=labelFontStyle)


# Helper variables for the functions below ----------------------
# Global variables that keep track of there is or isn't a session happening
sessionStarted = False
sessionEnded = True
# Global variables that keep track of the number of wrong entries inputted and total characters
wrongEntriesCounter = 0
totalCharactersCounter = 0
# Global variables that  keep track of time elapsed
startTime = 0
endTime = 0
elapsedTime = 0
# Global variable that keeps track of which index we are on
textIndexTracker = 0
# Global variables that keeps track of the line number and character number
textLineTracker = 1
textCharTracker = 0




# Function that triggers when the user starts typing letters (store all letters for accuracy comparison, keep track of the time started)
def typingStart():
    global startTime
    global wrongEntriesCounter
    global totalCharactersCounter
    global sessionEnded
    global statusLabel
    global keepCalculating
    sessionEnded = False
    startTime = time.time()
    # Set wrongEntries and totalCharacters counter to 0 to grab fresh data from when the correct letter is typed first (aka, game is started)
    wrongEntriesCounter = 0
    totalCharactersCounter = 0
    # Set status label to typing
    statusLabel.configure(text="Status: Typing...")


# Function that triggers when the user finishes the story text (updates WPM, TIME, ACCURACY labels respectively
def typingEnd():
    global endTime
    global elsapedTime
    global wrongEntriesCounter
    global sessionEnded

    sessionEnded = True

    # Calculate and update the time
    endTime = time.time()
    elapsedTime = endTime - startTime
    timeLabel.configure(text="Time: " + "{:.2f}".format(elapsedTime) + " seconds")

    # Calculate and update the accuracy
    accuracy = "{:.2f}%".format(100 * float(totalCharactersCounter / (totalCharactersCounter + wrongEntriesCounter)))
    accuracyLabel.configure(text="Accuracy: " + accuracy)

    # Calculate and update gross WPM
    # 5 characters is used as a standard word
    wordsPerMinute = "{:.2f}".format(float(float(totalCharactersCounter / 5) / float(elapsedTime / 60)))
    wpmLabel.configure(text="WPM: " + wordsPerMinute)

    # Set status label to typing finished
    statusLabel.configure(text="Status: Finished")


# Highlighter function that updates the highlighter tags so that the next character is highlighted if the input character is correct
def highlighter(event):
    global storyText
    global textIndexTracker
    global textCharTracker
    global textLineTracker
    global sessionStarted
    global sessionEnded
    global totalCharactersCounter
    global wrongEntriesCounter

    lineStart = str(textLineTracker) + ".0"
    lineEnd = str(textLineTracker) + "." + str(textCharTracker) + " lineend"
    currLine = (storyText.get(lineStart, lineEnd))

    # Updates the auto-highlighter so that the next character in the current sentence is highlighted if the input character matches the highlighted character
    if(textIndexTracker != len(currLine)):
        currLetter = currLine[textIndexTracker]

        # Check and see if the current letter in the entry form matches the current letter of the text box
        if(event.char == currLetter):
            if(sessionStarted == False):
                typingStart()
                sessionStarted = True
            textIndexTracker += 1
            textCharTracker += 1
            lineAndChar = str(textLineTracker) + "." + str(textCharTracker)

            # Delete the red highlighter tag if there is one
            storyText.tag_delete('redHighlighter')

            # Replace the previous highlight tag with the new one
            storyText.tag_delete('highlight')
            storyText.tag_add('highlight', '1.0', lineAndChar)
            storyText.tag_config('highlight', foreground='gray')

            # Replace the current character highlighter tag with the new one
            storyText.tag_delete('currLetterHi')
            storyText.tag_add('currLetterHi', str(textLineTracker) + "." + str(textCharTracker))
            storyText.tag_configure('currLetterHi', background='SkyBlue', foreground='white')

            # Update the total character count of the story
            totalCharactersCounter += 1

        # If the input character does not match the current letter of the text box, add a red highlighter to the current letter in the story
        else:
            # Add a red highlighter tag since the user typed the wrong character
            storyText.tag_add('redHighlighter', str(textLineTracker) + "." + str(textCharTracker))
            storyText.tag_configure('redHighlighter', background='Red')

            # Update the number of wrong entries typed to help calculate the User's accuracy
            wrongEntriesCounter += 1

    # Automatically set the text to the next line if the user reaches the end of the sentences
    lineStart = str(textLineTracker) + ".0"
    lineEnd = str(textLineTracker) + "." + str(textCharTracker) + " lineend"
    currLine = (storyText.get(lineStart, lineEnd))
    if(textCharTracker == len(currLine)):
        textIndexTracker = 0
        textLineTracker += 1
        textCharTracker = 0

        # Replace the current character highlighter tag with the new one
        storyText.tag_delete('currLetterHi')
        lineStart = str(textLineTracker) + ".0"
        lineEnd = str(textLineTracker) + "." + str(textCharTracker) + " lineend"
        currLine = (storyText.get(lineStart, lineEnd))
        # Does not highlight the next line if there are no contents to be highlighted
        if (len(currLine) != 0):
            storyText.tag_add('currLetterHi', str(textLineTracker) + "." + str(textCharTracker))
            storyText.tag_configure('currLetterHi', background='SkyBlue', foreground='white')


    # Check to see if there are any more texts left in the story
    if(sessionEnded == False):
        lineStart = str(textLineTracker) + ".0"
        lineEnd = str(textLineTracker) + "." + str(textCharTracker) + " lineend"
        currLine = (storyText.get(lineStart, lineEnd))
        if(len(currLine) == 0):
            typingEnd()


capsLk_On = False

# bind_all is used when you want the event listener to be binded to the root. (bind is used when you want the event listener to be binded to the widget
storyText.bind_all('<Key>', highlighter)

root.mainloop()
