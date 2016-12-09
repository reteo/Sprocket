#!/usr/bin/python

# sprocket-advanced.py:
#              A configuration generator for the Custom Ore Generation:
#              First Revival add-on for Minecraft.  The program reads
#              the mod's name and list of ores from a simple file, and
#              then generates the xml configuration file that can be
#              inserted into COG for play.  Keep in mind that the
#              generated file is *basic*, this was designed to make
#              clean files for further refinement without all the
#              tedious searching for missing brackets or broken 
#              elements.

# UPDATE - 8/15/2015 - Script rewritten from the ground up for maximum
#                      Flexibility and compatibility with COG

import random
import ConfigParser
import sys
import os
import textwrap
import string



# ------ Basic Functions ----- #

# Generates a random hexadecimal number of specified length.
def randomHexNumber(length):
    return ''.join([random.choice('0123456789ABCDEF') for x in range(length)])
    
# Returns the first element in a list.
def firstListItem(currentList):
    return firstListItem[0]
    
# Removes spaces from the string.
def spaceRemove(currentItem):
    newItem = currentItem.replace(" ", "")
    return newItem
    
# Removes a hash mark (#) from a string.  Useful for web color codes.
def hashRemove(currentItem):
    newItem = currentItem.replace("#", "")
    return newItem
    
# Removes XML-invalid characters from the string.
def xmlInvalidRemove(currentItem):
    preNewItem1 = currentItem.replace("\'", "")  # Remove Apostrophes
    preNewItem2 = preNewItem1.replace(":", "")  # Remove Colons
    preNewItem3 = preNewItem2.replace("|", "")  # Remove Vertical Bar
    preNewItem4 = preNewItem3.replace("<", "")  # Remove Less-Than
    preNewItem5 = preNewItem4.replace(">", "")  # Remove Greater-Than
    preNewItem6 = preNewItem5.replace("\"", "")     # Remove Quotes
    newItem = preNewItem6.replace(" ", "")
    return newItem

# Takes a list of text items, and turns it into a grammatically-correct
# list, depending on the number of items in the list.  Useful for
# generating lists for comments.
def grammaticalList(textList):    
    if len(textList) > 2:
        return ", and ".join([", ".join(textList[:-1]),textList[-1]])
    elif len(textList) == 2:
        return " and ".join(textList)
    else:
        return textList[0]

# --- End of Basic Functions --- #







# ------------- Option Extraction commands ------------ #

# Makes a list of characters into a spaceless, comma-separated list.
def extractList(currentList):
    newList = []
    intList = currentList.split(',')
    for item in range (0, len(intList)):
        newList.append(intList[item].replace(" ", ""))
    return newList

# Before we try to pull any information from an option, we want to make
# sure it actually has information to be pulled.  If the information is
# either -2.0 (that's negative two-point-zero) or "MISSING", then there
# is no need to extract it.


# Makes a list of characters into a comma-separated list.
def extractPreservedList(currentList):
    newList = []
    intList = currentList.split(',')
    for item in range (0, len(intList)):
        newList.append(intList[item].lstrip())        
    return newList

# Before we try to pull any information from an option, we want to make
# sure it actually has information to be pulled.  If the information is
# either -2.0 (that's negative two-point-zero) or "MISSING", then there
# is no need to extract it.

# This is the list version.
def checkOption(option):
    if spaceRemove(option[0]) == -2.0 or spaceRemove(option[0]) == -2 or spaceRemove(option[0]) == "MISSING":
        return False
    else:
        return True

# This is the single-variable version.
def checkCurrentOption(option):
    if option == -2.0 or option == -2 or spaceRemove(option) == "MISSING":
        return False
    else:
        return True

# A lot of the options come in the form "average, range, selection
# type, scaling" so it stands to reason we need special commands to
# extract the correct information from those options.

def extractAverage(option): # Extracts the average number
    if checkOption(option):    
        return option[0]
    else:
        return ""


def extractRange(option): # Extracts the deviation range  
    if checkOption(option):    
        return option[1]
    else:
        return ""


def extractRule(option): # Extracts the distribution rule  
    if checkOption(option):    
        return spaceRemove(option[2])
    else:
        return ""


def extractScale(option): # Extracts the height scaling method
    if checkOption(option):    
        return spaceRemove(option[3])
    else:
        return ""
    
# There are also compound options that have a minimum and maximum value.
# Let's make sure those are extractable as well.

def extractMinimum(option): # Extracts minimum value.
    if checkOption(option):    
        return spaceRemove(option[0])
    else:
        return ""

def extractMaximum(option): # Extracts minimum value.
    if checkOption(option):    
        return spaceRemove(option[1])
    else:
        return ""

# Finally, let's make sure we can get the first block from a list of blocks.
def extractFirstBlock(option):    
    if checkOption(option):    
        return spaceRemove(option[0])
    else:
        return ""

# ------------------------------------------- #









# ------------- Global Variables ------------ #

# [Mod] Section
modName=""                  # Mod name component for variable names
modPrefix=""                # Comes before the ore name in variable names
modDetect=""                # ModID identifier for mod
modHandle=""                # By default, COG will handle the mod's oregen.
modDescription=""           # Custom description for the Mod

# Variables for distribution configuration.
blockName=[]                # Name for block's section.
blockConfigName=[]          # The XML-valid name
blockSettingName=[]         # Block's configuration name with prefix.

# Block ID and Weight Lists
mainBlocks=[]               # List of unlocalized main block names.
mainBlockWeights=[]         # List of weights for main blocks.
altBlocks=[]                # List of unlocalized alternate block names.
altBlockWeights=[]          # List of weights for alternate blocks.
repBlocks=[]                # List of unlocalized replacement block names.
repBlockWeights=[]          # List of weights for replacement blocks.

# Locations
biomeNames=[]               # List of biome names
biomeTypes=[]               # List of biome dictionary keywords
biomeAvoidNames=[]          # List of biome names for main blocks to avoid.
biomeAvoidTypes=[]          # List of biome dictionary keywords for main blocks to avoid.
biomePreferNames=[]         # List of biome names for main blocks to prefer.
biomePreferTypes=[]         # List of biome dictionary keywords for main blocks to prefer.
biomeRainfall=[]            # Minimum and maximum rainfall to select biomes.
biomeTmperature=[]          # Minimum and maximum temperature to select biomes.
                    
# Adjacency
placeAbove=[]               # List of blocks to place main blocks above.
placeBeside=[]              # List of blocks to place main blocks next to.
placeBelow=[]               # List of blocks to place main blocks beneath.

# Debugging Values
wireframeActive=[]          # Enable wireframe in debugging mode?
wireframeColor=[]           # Web color code for wireframe.
boundBoxActive=[]           # Enable bounding box in debugging mode?
boundBoxColor=[]            # Web color code for bounding box.

# General Distribution Options
dimensionList=[]            # List of dimensions for block to spawn in.
presetList=[]               # List of distribution presets to use.
blockSeed=[]                # Hexadecimal seed for the RNG
distActive=[]               # If not active, the default distribution is "none"
distHint=[]                 # Do we want to use hint veins?  (Clouds only)
distSize=[]                 # General distribution size.
distFreq=[]                 # General distribution frequency.
distHeight=[]               # Y level of distribution
distDensity=[]              # Density of ores in distribution.
distParentRange=[]          # Range of child distribution from parent.
initSubAll=[]               # Initialize oregen by wiping any blocks at all? (Default: yes)
initSubMain=[]              # Initialize oregen by wiping main block? (Default: yes)
initSubAlt=[]               # Initialize oregen by wiping alternate block? (Default: no)
clampRange=[]               # Two comma-separated numbers, stating min and max Y levels for clamping ore distribution.
heightScaling=[]            # Height Scaling Option

# Substitution Settings
subHeightRange=[]           # Two comma-separated numbers stating min and max Y level for substitution.

# Standard Generation (Vanilla-Simulation) Distribution Options
stdHeight=[]                # Y level for standard generator.
stdFreq=[]                  # Frequency multiplier for standard generator.
stdSize=[]                  # Size multiplier for standard generator.
stdParentRange=[]           # Range of child distribution from parent.
stdHeightRange=[]           # Two comma-separated numbers stating min and max Y level for substitution.

# Cloud Generation Distribution Options
cloudFreq=[]                # Frequency Multiplier
cloudParentRange=[]         # Range of child distribution from parent.
cloudRadius=[]              # Horizontal Size of cloud.
cloudThickness=[]           # Vertical Size of cloud.
cloudNoise=[]               # Smoothness (or lack thereof) of cloud sides.
cloudHeight=[]              # Y levels of cloud distribution
cloudInclination=[]         # Tilt of the cloud from XZ, in radians.
cloudDensity=[]             # Density multiplier
cloudNoiseCutoff=[]         # Per-block internal density noise cutoff.
cloudRadiusMult=[]          # Per-block multiplier of max radius for clouds.
cloudHeightRange=[]         # Two comma-separated numbers stating min and max Y level for substitution.

# Vein Generation Distribution Options
# Motherlode settings
veinMotherlodeFreq=[]       # Vein motherlode frequency multiplier.
veinMotherlodeRangeLimit=[] # Range of child distribution from parent.
veinMotherlodeSize=[]       # Size multiplier of motherlode.
veinMotherlodeHeight=[]     # Y levels of motherlodes.
# Full branch settings
veinBranchType=[]           # Ellipsoid or Bezier
veinBranchFreq=[]           # Number of branches per motherlode.
veinBranchInclination=[]    # Angle from XZ plane that branch leaves motherlode.
veinBranchLength=[]         # Maximum length of branch if stretched out.
veinBranchHeightLimit=[]    # Limits how far up or down branches will turn.
# Branch segment settings
veinSegmentForkFreq=[]      # How frequently segments will fork from branch.
veinSegmentForkLength=[]    # Multiplier to remaining branch length to a fork.
veinSegmentLength=[]        # Length of each straight branch segment.
veinSegmentAngle=[]         # Angle of diversion from one segment to next.
veinSegmentPitch=[]         # 
veinSegmentRadius=[]        # Width multiplier to widest point in segment.
veinOreDensity=[]           # Per-block density multiplier
veinOreRadiusMult=[]        # Multiplier to maximum radius (for both segments and motherlodes)
# Miscellaneous vein distribution settings
veinHeightRange=[]          # Two comma-separated numbers stating min and max Y level for substitution.

oreList = ""
indentLine=0 # This is the value that tracks indentation for XML

# ------------------------------------------- #






# --- Error Checking and File Preparation --- #

# We want to make sure that errors are tracked by this program, and
# when one occurs, nothing gets written to disk.  This prevents mistakes
# from destroying a previously-working configuration.

errorCondition = "" # No errors are detected by default.

# First step, make sure the INI file is actually there.  If not,
# just shut down.
try:
    if not os.path.isfile(sys.argv[1]):
        sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": No such file or directory")
        
except IndexError:
	print "\n  Sprocket is designed to take an INI file and convert it into an"
	print "  XML file in the current directory.\n"
	print "USAGE:"
	print os.path.basename(sys.argv[0])+" <oregen file>\n"
	print "       or\n"
	print "python "+os.path.basename(sys.argv[0])+" <oregen file> \n"
	errorCondition=1
	sys.exit()
	
# At this point, we've passed the test.  Let's prepare the file for
# loading.
configFile = sys.argv[1]

# Open a configuration file for reading, and prepare defaults.
Config = ConfigParser.SafeConfigParser(
    defaults={  'Blocks':'MISSING',
                'Block Weights':'MISSING',
                'Alternate Blocks':'minecraft:stone',
                'Alternate Block Weights':'MISSING',
                'Replaces':'minecraft:stone',
                'Replacement Weights':'MISSING',
                'Dimensions':'Overworld',
                'Need Biomes':'.*',
                'Need Biome Types':'MISSING',
                'Avoid Biomes':'MISSING',
                'Avoid Biome Types':'MISSING',
                'Prefer Biomes':'MISSING',
                'Prefer Biome Types':'MISSING',
                'Biome Rainfall Range':'MISSING',
                'Biome Temperature Range':'MISSING',
                'Place Below':'MISSING',
                'Place Beside':'MISSING',
                'Place Above':'MISSING',
                'Wireframe':'yes',
                'Bounding Box':'no',
                'Wireframe Color':"MISSING",
                'Bounding Box Color':"MISSING",
                'Seed':"MISSING",
                'Active':'yes',
                'Hint Veins':'yes',
                'Size':'_default_, _default_, normal, base',
                'Frequency':'_default_, _default_, normal, base',
                'Height':'_default_, _default_, normal, base',
                'Density':'_default_, _default_, normal, base',
                'Parent Range Limit':'_default_, _default_, normal, base',
                'Use Cleanup':'yes',
                'Main Block Cleanup':'yes',
                'Alternate Block Cleanup':'no',
                'Distribution Presets':'Vanilla',
                'Height Clamp Range':'MISSING',
                'Height Scaling':'base',
                'Substitution Height Clamp Range':'MISSING',
                'Standard Size':'MISSING',
                'Standard Frequency':'MISSING',
                'Standard Height':'MISSING',
                'Standard Parent Range Limit':'MISSING',
                'Standard Height Clamp Range':'MISSING',
                'Cloud Frequency':'MISSING',
                'Cloud Parent Range Limit':'MISSING',
                'Cloud Radius':'MISSING',
                'Cloud Thickness':'MISSING',
                'Cloud Noise':'_default_, _default_, normal, base',
                'Cloud Height':'MISSING',
                'Cloud Inclination':'_default_, _default_, normal, base',
                'Cloud Density':'MISSING',
                'Cloud Noise Cutoff':'_default_, _default_, normal, base',
                'Cloud Radius Multiplier':'_default_, _default_, normal, base',
                'Cloud Height Clamp Range':'MISSING',
                'Vein Motherlode Frequency':'MISSING',
                'Vein Motherlode Range Limit':'MISSING',
                'Vein Motherlode Size':'MISSING',
                'Vein Motherlode Height':'MISSING',
                'Vein Branch Type':'Bezier',
                'Vein Branch Frequency':'_default_, _default_, normal, base',
                'Vein Branch Inclination':'_default_, _default_, normal, base',
                'Vein Branch Length':'_default_, _default_, normal, base',
                'Vein Branch Height Limit':'_default_, _default_, normal, base',
                'Vein Segment Fork Frequency':'_default_, _default_, normal, base',
                'Vein Segment Fork Length Multiplier':'_default_, _default_, normal, base',
                'Vein Segment Length':'_default_, _default_, normal, base',
                'Vein Segment Angle':'_default_, _default_, normal, base',
                'Vein Segment Pitch':'_default_, _default_, normal, base',
                'Vein Segment Radius':'_default_, _default_, normal, base',
                'Vein Ore Density':'MISSING',
                'Vein Ore Radius Multiplier':'_default_, _default_, normal, base',
                'Vein Height Clamp Range':'MISSING'
    })
Config.read(configFile)

# Let's get the name of the mod from the configuration.
try:
    modName = Config.get('Mod', 'Name')  # "My Mod 2"
except ConfigParser.NoSectionError:
	print "No [Mod] section found."
	errorCondition=1
	sys.exit(""+os.path.basename(sys.argv[1])+": nothing written due to errors\n")
except ConfigParser.NoOptionError:
    print "No mod name found."
    errorCondition=1

# Variables cannot have spaces.  Let's remove spaces and XML-invalid
# characters from the Mod's name so we can use it in variable names.

modPreConfigName1=spaceRemove(modName)
modConfigName=xmlInvalidRemove(modPreConfigName1)


# The prefix is important in making XML name attributes.
try:
    modPrefix = Config.get('Mod', 'Prefix') # "mmd2"
except ConfigParser.NoOptionError:
    print "No mod prefix found."
    errorCondition=1

# This is for detecting the mod based on its ModID name.
try:
    modDetect = Config.get('Mod', 'Detect') # "MyMod"
except ConfigParser.NoOptionError:
    print "No ModID to detect was found."
    errorCondition=1

# If errors occurred at this point, don't go any further.
if errorCondition:
    sys.exit(os.path.basename(sys.argv[0])+": "+sys.argv[1]+": nothing written due to errors\n")

# Otherwise, let's see if we can get a description.

try:
    modDescription = Config.get('Mod', 'Description') # "This is a mod I like...?"
except ConfigParser.NoOptionError:
    print "You don't need a mod description, but one might be nice..."

# Also, let's see how we want to handle ores by default
try:
    modHandle = Config.get('Mod', 'Enable') # Enable COG generation of this mod by default?
except ConfigParser.NoOptionError:
    modHandle = "yes"

print "Generating configuration for "+modName+"." # Yup, we can now proceed.

blockName = Config.sections()
blockName.pop(0)  # The first section is not an ore, it's the mod's
                # default settings.  It's not needed here, but will
                # still apply when needed.

blockCount = 0    # Start the count at the first ore.

# Creating a set of matrices for the options; memory access is always
# faster than disk access.

for currentBlock in blockName:
    blockConfigName.append(xmlInvalidRemove(blockName[blockCount]))
    blockSettingName.append(modPrefix+blockConfigName[blockCount])
    mainBlocks.append(extractPreservedList(Config.get(currentBlock, 'Blocks')))
    mainBlockWeights.append(extractList(Config.get(currentBlock, 'Block Weights')))
    altBlocks.append(extractPreservedList(Config.get(currentBlock, 'Alternate Blocks')))
    altBlockWeights.append(extractList(Config.get(currentBlock, 'Alternate Block Weights')))
    repBlocks.append(extractPreservedList(Config.get(currentBlock, 'Replaces')))
    repBlockWeights.append(extractList(Config.get(currentBlock, 'Replacement Weights')))
    dimensionList.append(extractList(Config.get(currentBlock, 'Dimensions')))
    biomeNames.append(extractPreservedList(Config.get(currentBlock, 'Need Biomes')))
    biomeTypes.append(extractPreservedList(Config.get(currentBlock, 'Need Biome Types')))
    biomeAvoidNames.append(extractPreservedList(Config.get(currentBlock, 'Avoid Biomes')))
    biomeAvoidTypes.append(extractPreservedList(Config.get(currentBlock, 'Avoid Biome Types')))
    biomePreferNames.append(extractPreservedList(Config.get(currentBlock, 'Prefer Biomes')))
    biomePreferTypes.append(extractPreservedList(Config.get(currentBlock, 'Prefer Biome Types')))
    biomeRainfall.append(extractList(Config.get(currentBlock, 'Biome Rainfall Range')))
    biomeTmperature.append(extractList(Config.get(currentBlock, 'Biome Temperature Range')))
    placeBelow.append(extractList(Config.get(currentBlock, 'Place Below')))
    placeBeside.append(extractList(Config.get(currentBlock, 'Place Beside')))
    placeAbove.append(extractList(Config.get(currentBlock, 'Place Above')))
    wireframeActive.append(extractList(Config.get(currentBlock, 'Wireframe')))
    wireframeColor.append(extractList(Config.get(currentBlock, 'Wireframe Color')))
    boundBoxActive.append(extractList(Config.get(currentBlock, 'Bounding Box')))
    boundBoxColor.append(extractList(Config.get(currentBlock, 'Bounding Box Color')))
    presetList.append(extractList(Config.get(currentBlock, 'Distribution Presets')))
    blockSeed.append(extractList(Config.get(currentBlock, 'Seed')))
    distActive.append(extractList(Config.get(currentBlock, 'Active')))
    distHint.append(extractList(Config.get(currentBlock, 'Hint Veins')))
    distSize.append(extractPreservedList(Config.get(currentBlock, 'Size')))
    distFreq.append(extractPreservedList(Config.get(currentBlock, 'Frequency')))
    distHeight.append(extractPreservedList(Config.get(currentBlock, 'Height')))
    distDensity.append(extractPreservedList(Config.get(currentBlock, 'Density')))
    distParentRange.append(extractPreservedList(Config.get(currentBlock, 'Parent Range Limit')))
    initSubAll.append(extractList(Config.get(currentBlock, 'Use Cleanup')))
    initSubMain.append(extractList(Config.get(currentBlock, 'Main Block Cleanup')))
    initSubAlt.append(extractList(Config.get(currentBlock, 'Alternate Block Cleanup')))
    clampRange.append(extractList(Config.get(currentBlock, 'Height Clamp Range')))
    subHeightRange.append(extractList(Config.get(currentBlock, 'Substitution Height Clamp Range')))
    stdHeight.append(extractPreservedList(Config.get(currentBlock, 'Standard Height')))
    stdFreq.append(extractPreservedList(Config.get(currentBlock, 'Standard Frequency')))
    stdSize.append(extractPreservedList(Config.get(currentBlock, 'Standard Size')))
    stdParentRange.append(extractPreservedList(Config.get(currentBlock, 'Standard Parent Range Limit')))
    stdHeightRange.append(extractList(Config.get(currentBlock, 'Standard Height Clamp Range')))
    cloudFreq.append(extractPreservedList(Config.get(currentBlock, 'Cloud Frequency')))
    cloudParentRange.append(extractPreservedList(Config.get(currentBlock, 'Cloud Parent Range Limit')))
    cloudRadius.append(extractPreservedList(Config.get(currentBlock, 'Cloud Radius')))
    cloudThickness.append(extractPreservedList(Config.get(currentBlock, 'Cloud Thickness')))
    cloudNoise.append(extractPreservedList(Config.get(currentBlock, 'Cloud Noise')))
    cloudHeight.append(extractPreservedList(Config.get(currentBlock, 'Cloud Height')))
    cloudInclination.append(extractPreservedList(Config.get(currentBlock, 'Cloud Inclination')))
    cloudDensity.append(extractPreservedList(Config.get(currentBlock, 'Cloud Density')))
    cloudNoiseCutoff.append(extractPreservedList(Config.get(currentBlock, 'Cloud Noise Cutoff')))
    cloudRadiusMult.append(extractPreservedList(Config.get(currentBlock, 'Cloud Radius Multiplier')))
    cloudHeightRange.append(extractList(Config.get(currentBlock, 'Cloud Height Clamp Range')))
    veinMotherlodeFreq.append(extractPreservedList(Config.get(currentBlock, 'Vein Motherlode Frequency')))
    veinMotherlodeRangeLimit.append(extractPreservedList(Config.get(currentBlock, 'Vein Motherlode Range Limit')))
    veinMotherlodeSize.append(extractPreservedList(Config.get(currentBlock, 'Vein Motherlode Size')))
    veinMotherlodeHeight.append(extractPreservedList(Config.get(currentBlock, 'Vein Motherlode Height')))
    veinBranchType.append(extractPreservedList(Config.get(currentBlock, 'Vein Branch Type')))
    veinBranchFreq.append(extractPreservedList(Config.get(currentBlock, 'Vein Branch Frequency')))
    veinBranchInclination.append(extractPreservedList(Config.get(currentBlock, 'Vein Branch Inclination')))
    veinBranchLength.append(extractPreservedList(Config.get(currentBlock, 'Vein Branch Length')))
    veinBranchHeightLimit.append(extractPreservedList(Config.get(currentBlock, 'Vein Branch Height Limit')))
    veinSegmentForkFreq.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Fork Frequency')))
    veinSegmentForkLength.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Fork Length Multiplier')))
    veinSegmentLength.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Length')))
    veinSegmentAngle.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Angle')))
    veinSegmentPitch.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Pitch')))
    veinSegmentRadius.append(extractPreservedList(Config.get(currentBlock, 'Vein Segment Radius')))
    veinOreDensity.append(extractPreservedList(Config.get(currentBlock, 'Vein Ore Density')))
    veinOreRadiusMult.append(extractPreservedList(Config.get(currentBlock, 'Vein Ore Radius Multiplier')))
    veinHeightRange.append(extractList(Config.get(currentBlock, 'Vein Height Clamp Range')))
    
    # There MUST be a main block value; all others are negotiable or
    # have default values already assigned.  If the block is missing,
    # Then we'll just stop the program with an error; there's no point
    # continuing.
    #if checkOption(Config.get(currentBlock, 'Blocks')):
    #    print('Error: The \'['+currentBlock+']\' section *must* have at least one block ID assigned.')
    #    errorCondition = 'T'

    # Okay, we got this section of the configuration, let's move onto the next.
    blockCount += 1
    
# Now, we need to assign individual random numbers to seeds and wireframes that are missing them.
for blockIndex in range(0, len(blockName)):
    if blockSeed[blockIndex][0] == "MISSING":
        blockSeed[blockIndex][0] = str(randomHexNumber(4))
    if wireframeColor[blockIndex][0] == "MISSING":
        wireframeColor[blockIndex][0] = str(randomHexNumber(6))
    if boundBoxColor[blockIndex][0] == "MISSING":
        boundBoxColor[blockIndex][0] = str(randomHexNumber(6))
        
# ------------------------------------------- #









                    

# ---- Configuration Formatting Commands ---- #

# XML convention is to indent items within an XML space.
cogIndentLevel = 0

# Returns space equal to two spaces per indent level.
def cogIndentSpace():
    cogSpace = ""
    global cogIndentLevel
    
    for count in range(0, cogIndentLevel):
        cogSpace += "  "
        
    return cogSpace
 
# Changes the indent level.
def cogIndent(cogIndentValue):
    global cogIndentLevel
    
    cogIndentLevel += cogIndentValue

    return ""
   
# Adds a new line to the configuration.
def cogFormatLine(cogLine):

    return cogIndentSpace()+cogLine+"\n"

# This adds a wrapped version of the cogFormatLine command.
def cogWrappedLine(cogComment):
    global cogIndentLevel
    wrappedComment = "\r\n".join(textwrap.wrap(cogComment, (65-(cogIndentLevel*4))))
    finalComment = textwrap.fill(wrappedComment, initial_indent=cogIndentSpace(), subsequent_indent=cogIndentSpace())+"\n"
    
    return finalComment

# Adds a new comment to the configuration.
# This comment is automatically wrapped and
# indented as needed.
def cogFormatComment(cogComment):
    global cogIndentLevel
    wrappedComment = "\r\n".join(textwrap.wrap(cogComment, (65-(cogIndentLevel*4))))
    finalComment = textwrap.fill(wrappedComment, initial_indent=cogIndentSpace()+"<!-- ", subsequent_indent=cogIndentSpace()+"     ")+" -->\n"
    
    return finalComment

# A boxed comment for extra-special comments.
def cogFormatBoxComment(cogComment):
    currentLine = ""
    wrappedComment = "\r\n".join(textwrap.wrap(cogComment, (65-(cogIndentLevel*4))))
    for lineSegment in range(0, (65-(cogIndentLevel*4))):
        currentLine += "="
        
    firstLine = cogIndentSpace()+"<!-- "+currentLine+"\n"
    mainLine  = textwrap.fill(wrappedComment, initial_indent=cogIndentSpace()+"     ", subsequent_indent=cogIndentSpace()+"     ")+"\n"
    lastLine  = cogIndentSpace()+"     "+currentLine+" -->\n"
    
    finalComment = firstLine+mainLine+lastLine
    
    return finalComment
    
# ------------------------------------------- #








    











# -------------- Main Commands ------------- #



### Block Command ###

def blockCommand(command, currentBlock, currentWeight):
    if checkCurrentOption(currentBlock):
        if checkCurrentOption(currentWeight):
            return "<"+command+" block='"+currentBlock+"' weight='"+currentWeight+"' />"
        else: 
            return "<"+command+" block='"+currentBlock+"' />"
    else:
        return ""
    
    
    #if checkCurrentOption(currentBlock):
    #    if checkCurrentOption(currentWeight):
    #        return "<"+command+" block='"+currentBlock+"' weight='"+currentWeight+"' />"
    #    else:
    #        return "<"+command+" block='"+currentBlock+"' />"
    #else:
    #    return ""

     
### Biome Commands ###

# Refine by rainfall and/or temperature.
def biomeClimate(currentRainfall, currentTemperature):
    maxRainfall = maxTemperature = minRainfall = minTemperature = -2.0
    climateAttributes = ""
    
    # Make sure the values exist, and then assign them.
       
    if checkOption(currentRainfall):
        if checkCurrentOption(extractMinimum(currentRainfall)):
            minRainfall=extractMinimum(currentRainfall)
        if checkCurrentOption(extractMaximum(currentRainfall)):
            maxRainfall=extractMaximum(currentRainfall)
        
    if checkOption(currentTemperature):
        if checkCurrentOption(extractMinimum(currentTemperature)):
            minTemperature=extractMinimum(currentTemperature)
        if checkCurrentOption(extractMaximum(currentTemperature)):
            maxTemperature=extractMaximum(currentTemperature)
           
    if minRainfall != -2.0:
        climateAttributes += " minRainfall='"+extractMinimum(currentRainfall)+"'"
        
    if maxRainfall != -2.0:
        climateAttributes += " maxRainfall='"+extractMaximum(currentRainfall)+"'"
            
    if minTemperature != -2.0:
        climateAttributes += " minTemperature='"+extractMinimum(currentTemperature)+"'"
        
    if minTemperature != -2.0:
        climateAttributes += " maxTemperature='"+extractMaximum(currentTemperature)+"'"
        
    return climateAttributes

# Selects biomes to populate.
def biomeSelect(command, currentBiome, currentRainfall, currentTemperature):  
    if checkOption(currentBiome):
        return "<"+command+" name='"+currentBiome+"' "+biomeClimate(currentRainfall, currentTemperature)+" />"
    else:
        return ""
    
# Selects biomes to ignore.
def biomeIgnore(command, currentBiome, currentRainfall, currentTemperature):   
    if checkOption(currentBiome):
        return "<"+command+" name='"+currentBiome+"' "+biomeClimate(currentRainfall, currentTemperature)+" weight='-1' />"
    else:
        return ""

   


### Adjacency Placement
   
def placeNear(direction, blockId):
    return "<Places"+direction+" "+blockId+" />"





### Debugging Values
    
# Wireframes
def setWireframe(active, color):
    if active == "yes":
        return "drawWireframe=':= drawWireframes' wireframeColor='0x60"+hashRemove(color)+"'"
    else:
        return "drawWireframe='false' wireframeColor='0x60"+hashRemove(color)+"'"
    
# Bounding boxes
def setBoundingBox(active, color):
    if active == "yes":
        return "drawBoundBox='true' boundBoxColor='0x60"+boundBoxColor(color)+"'"
    else:
        return "drawBoundBox='false' boundBoxColor='0x60"+hashRemove(color)+"'"





### Dimension Options
   
def dimensionName(dimensionCode):
    if spaceRemove(dimensionCode.lower()) == "overworld":
        return "Overworld"
    elif spaceRemove(dimensionCode.lower()) == "nether":
        return "Nether"
    elif spaceRemove(dimensionCode.lower()) == "end":
        return "End"
    elif spaceRemove(dimensionCode.lower()) == "twilightforest":
        return "Twilight Forest"
    elif spaceRemove(dimensionCode.lower()) == "aether":
        return "Aether"
    elif spaceRemove(dimensionCode.lower()) == "dungeon" or spaceRemove(dimensionCode.lower()) == "dungeons" or spaceRemove(dimensionCode.lower()) == "dungeondimension" or spaceRemove(dimensionCode.lower()) == "aetherdungeon" or spaceRemove(dimensionCode.lower()) == "aetherdungeons":
        return "Aether Dungeons"
    elif spaceRemove(dimensionCode.lower()) == "outerlands" or spaceRemove(dimensionCode.lower()) == "theouterlands":
        return "Outer Lands"
    elif spaceRemove(dimensionCode.lower()) == "bedrock" or spaceRemove(dimensionCode.lower()) == "bedrockdimension":
        return "Bedrock Dimension"
    elif spaceRemove(dimensionCode.lower()) == "mining" or spaceRemove(dimensionCode.lower()) == "miningworld":
        return "Aroma1997s Mining World"
    elif spaceRemove(dimensionCode.lower()) == "space" or spaceRemove(dimensionCode.lower()) == "galacticraftspace":
        return "GalactiCraft Space"
    elif spaceRemove(dimensionCode.lower()) == "moon" or spaceRemove(dimensionCode.lower()) == "galacticraftmoon":
        return "GalactiCraft Moon"
    elif spaceRemove(dimensionCode.lower()) == "orbit" or spaceRemove(dimensionCode.lower()) == "galacticraftorbit":
        return "GalactiCraft Orbit"
    elif spaceRemove(dimensionCode.lower()) == "mars" or spaceRemove(dimensionCode.lower()) == "galacticraftmars":
        return "GalactiCraft Mars"
    elif spaceRemove(dimensionCode.lower()) == "asteroids" or spaceRemove(dimensionCode.lower()) == "galacticraftasteroids":
        return "GalactiCraft Asteroids"
    elif spaceRemove(dimensionCode.lower()) == "rftools":
        return "RFTools"
    elif spaceRemove(dimensionCode.lower()) == "mystcraft":
        return "MystCraft"
    else:
        return "MISSING"
    
def dimensionCheck(dimList, dimName):
    confirm = False
    
    for dimCount in range(0, len(dimList)):
        if dimensionName(dimList[dimCount]) == dimName:
            confirm = True
    
    return confirm


### Preset Options

def presetInherit(preset):
    # Presets provided by Custom Ore Generation.
    if preset.lower()=="substitution":
        return ""
    if preset.lower()=="vanilla":
        return "inherits='PresetStandardGen'"
    if preset.lower()=="layeredveins":
        return "inherits='PresetLayeredVeins'"
    if preset.lower()=="verticalveins":
        return "inherits='PresetVerticalVeins'"
    if preset.lower()=="smalldeposits":
        return "inherits='PresetSmallDeposits'"
    if preset.lower()=="hugeveins":
        return "inherits='PresetHugeVeins'"
    if preset.lower()=="hintveins":
        return "inherits='PresetHintVeins'"
    if preset.lower()=="sparseveins":
        return "inherits='PresetSparseVeins'"
    if preset.lower()=="pipeveins":
        return "inherits='PresetPipeVeins'"
    if preset.lower()=="cloud" or preset.lower()=="strategicclouds":
        return "inherits='PresetStrategicCloud'"
    if preset.lower()=="strata" or preset.lower()=="stratumclouds":
        return "inherits='PresetStratum'"
    # Presets added by Sprocket.
    if preset.lower()=="geode":
        return "inherits='PresetSmallDeposits'"
    if preset.lower()=="compoundveins":
        return "inherits='PresetLayeredVeins'"
    # Preset for a non-preset distribution; useful for completely custom distributions.
    if preset.lower()=="customcloud":
        return ""
    if preset.lower()=="customveins":
        return ""
    if preset.lower()=="null":
        return ""
    else:
        print "Invalid Distribution Preset: \""+preset+"\""
        return ""
    
def presetName(preset):
    # Presets provided by Custom Ore Generation.
    if preset.lower()=="substitution":
        return "Substitution"
    if preset.lower()=="vanilla":
        return "Vanilla"
    if preset.lower()=="layeredveins":
        return "Layered Veins"
    if preset.lower()=="verticalveins":
        return "Vertical Veins"
    if preset.lower()=="smalldeposits":
        return "Small Deposits"
    if preset.lower()=="hugeveins":
        return "Huge Veins"
    if preset.lower()=="hintveins":
        return "Hint Veins"
    if preset.lower()=="sparseveins":
        return "Sparse Veins"
    if preset.lower()=="pipeveins":
        return "Pipe Veins"
    if preset.lower()=="cloud" or preset.lower()=="strategicclouds":
        return "Strategic Clouds"
    if preset.lower()=="strata" or preset.lower()=="stratumclouds":
        return "Strata"
    # Presets added by Sprocket.
    if preset.lower()=="geode":
        return "Geode"
    if preset.lower()=="compoundveins":
        return "Compound Veins"
    # Preset for a non-preset distribution; useful for completely custom distributions.
    if preset.lower()=="customcloud":
        return "Custom Cloud"
    if preset.lower()=="customveins":
        return "Custom Veins"
    if preset.lower()=="null":
        return "Blank"
    else:
        print "Invalid Distribution Preset: \""+preset+"\""
        return ""
    
def presetDescription(preset):
    # Presets provided by Custom Ore Generation.
    if preset.lower()=="substitution":
        return "This is a global replacement of one block with another.  Height clamping is needed to keep the substitution from being universal."
    if preset.lower()=="vanilla":
        return "A master preset for standardgen ore distributions."
    if preset.lower()=="layeredveins":
        return "Small, fairly rare motherlodes with 2-4 horizontal veins each."
    if preset.lower()=="verticalveins":
        return "Single vertical veins that occur with no motherlodes."
    if preset.lower()=="smalldeposits":
        return "Small motherlodes without any branches.  Similar to the deposits produced by StandardGen distributions."
    if preset.lower()=="hugeveins":
        return "Very large, extremely rare motherlodes.  Each motherlode has many long slender branches---so thin that parts of the branch won't contain any ore at all.  This, combined with the incredible length of the branches, makes them more challenging to follow underground.  Once found, however, a motherlode contains enough ore to keep a player supplied for a very long time.  The rarity of these veins might be too frustrating in a single-player setting.  In SMP, though, teamwork could make finding them much easier and the motherlodes are big enough to supply several people without shortage.  This might be a good way to add challenge to multiplayer worlds.  Credit: based on feedback by dyrewulf from the MC forums."
    if preset.lower()=="hintveins":
        return "Single blocks, generously scattered through all heights (density is about that of vanilla iron ore). They will replace dirt and sandstone (but not grass or sand), so they can be found nearer to the surface than most ores.  Intened to be used as a child distribution for large, rare strategic deposits that would otherwise be very difficult to find.  Note that the frequency is multiplied by ground level to maintain a constant density, but not by ore frequency because it is assumed that the frequency of the parent distribution will already be scaled by that."
    if preset.lower()=="sparseveins":
        return "Large veins filled very lightly with ore.  Because they contain less ore per volume, these veins are relatively wide and long.  Mining the ore from them is time consuming compared to solid ore veins.  They are also more difficult to follow, since it is harder to get an idea of their direction while mining."
    if preset.lower()=="pipeveins":
        return "Short sparsely filled veins sloping up from near the bottom of the map."
    if preset.lower()=="cloud" or preset.lower()=="strategicclouds":
        return "Large irregular clouds filled lightly with ore.  These are huge, spanning several adjacent chunks, and consequently rather rare.  They contain a sizeable amount of ore, but it takes some time and effort to mine due to low density. The intent for strategic clouds is that the player will need to actively search for one and then set up a semi-permanent mining base and spend some time actually mining the ore."
    if preset.lower()=="stratum" or preset.lower()=="stratumclouds":
        return "Wide, thin, and flat disks of ore.  Primarily, this distribution is meant to provide realistic distribution of stone in a strata formation."
    # Presets added by Sprocket.
    if preset.lower()=="geode":
        return "Multi-layered deposit.  On the outside is a shell, usually made of some form of stone.  Within this shell is sprinkled ores.  Inside both is an air pocket from which the enterprising miner can look for the contained ores."
    if preset.lower()=="compoundveins":
        return "Similar to pipe veins, except that the motherlode and veins are a solid vein containing another, smaller solid vein."
    # Preset for a non-preset distribution; useful for completely custom distributions.
    if preset.lower()=="customcloud":
        return "A completely custom cloud design.  It is recommended to change this text to appropriately describe the distribution."
    if preset.lower()=="customveins":
        return "A completely custom veins design.  It is recommended to change this text to appropriately describe the distribution."
    if preset.lower()=="null":
        return "MISSING"
    else:
        print "Invalid Distribution Preset: \""+preset+"\""
        return ""
    
def presetLiteDescription(preset):
    # Presets provided by Custom Ore Generation.
    if preset.lower()=="substitution":
        return "Universal Block Replacement."
    if preset.lower()=="vanilla":
        return "Simulates Vanilla Minecraft."
    if preset.lower()=="layeredveins":
        return "Small, fairly rare motherlodes with 2-4 horizontal veins each."
    if preset.lower()=="verticalveins":
        return "Single vertical veins that occur with no motherlodes."
    if preset.lower()=="smalldeposits":
        return "Small motherlodes without any branches."
    if preset.lower()=="hugeveins":
        return "Very large, extremely rare motherlodes with long, thin tendrils."
    if preset.lower()=="hintveins":
        return "Single blocks, scattered through all heights, replacing dirt and sandstone only."
    if preset.lower()=="sparseveins":
        return "Large veins filled very lightly with ore."
    if preset.lower()=="pipeveins":
        return "Short and sparsely filled compound veins containing one material inside another."
    if preset.lower()=="cloud" or preset.lower()=="strategicclouds":
        return "Large irregular clouds filled lightly with ore."
    if preset.lower()=="stratum" or preset.lower()=="stratumclouds":
        return "Wide, thin, and flat disks of ore."
    # Presets added by Sprocket.
    if preset.lower()=="geode":
        return "Multi-layered deposit in a spherical shape."
    if preset.lower()=="compoundveins":
        return "Veins containing another vein."
    # Preset for a non-preset distribution; useful for completely custom distributions.
    if preset.lower()=="customcloud":
        return "Custom cloud; update this description."
    if preset.lower()=="customveins":
        return "Custom vein; update this description."
    if preset.lower()=="null":
        return "MISSING"
    else:
        print "Invalid Distribution Preset: \""+preset+"\""
        return ""




### Random Number Generator options.

def seedAttribute(seed):
    return "seed='0x"+seed+"'"




### Height Range Commands

def distHeightRange(preferredOption, globalOption):
    
    attributes = ""
        
    # First, we'll see if the distribution's own clamps are set.
    if checkOption(preferredOption):
        if checkCurrentOption(extractMinimum(preferredOption)):
            attributes += " minHeight='"+extractMinimum(preferredOption)+"' "        
        if checkCurrentOption(extractMaximum(preferredOption)):
            attributes += " maxHeight='"+extractMaximum(preferredOption)+"' "
    elif checkOption(globalOption): # It's not here, so now we check for global clamps.
        if checkCurrentOption(extractMinimum(globalOption)):
            attributes += " minHeight='"+extractMinimum(globalOption)+"' "
        if checkCurrentOption(extractMaximum(globalOption)):
            attributes += " maxHeight='"+extractMaximum(globalOption)+"' "        
        
    return attributes




# If the distribution is not active, than the default should be set to "none."

def ifDistActive(option):
    activeOption = option[0]
    if activeOption.lower() == "no":
        return " default='none' "
    else:
        return " "



    
### 3-option settings (avg, range, type)

# NOTE: configName should be set to the appropriate blockSettingName[]

def mainSetting(settingName, preferredOption, globalOption, configName, sliderOption, multiplier):
    valAverage = valRange = ruleType = ""
     
    # Next, we'll see if the distribution's own settings are set.
    if checkOption(preferredOption):
        if checkCurrentOption(extractAverage(preferredOption)):
            numAverage = str(extractAverage(preferredOption))
        if checkCurrentOption(extractRange(preferredOption)):
            numRange = str(extractRange(preferredOption))
        if checkCurrentOption(extractRule(preferredOption)):
            ruleType = str(extractRule(preferredOption))
                
    else: # The preferred options weren't set, let's use globals.
        if checkCurrentOption(extractAverage(globalOption)):
            numAverage = str(extractAverage(globalOption))
        if checkCurrentOption(extractRange(globalOption)):
            numRange = str(extractRange(globalOption))
        if checkCurrentOption(extractRule(globalOption)):
            ruleType = str(extractRule(globalOption))
    
    sliderName = ""
    if checkCurrentOption(sliderOption):
        sliderName = " * "+configName+sliderOption
        
    if multiplier == "1":
        multiplierString = ""
    else:
        multiplierString = " * "+multiplier+" "
    
    return "<Setting name='"+settingName+"' avg=':= "+numAverage+sliderName+" "+multiplierString+"' range=':= "+numRange+sliderName+" "+multiplierString+"' type='"+ruleType+"' />"





### 4-option settings (avg, range, type, scale)

# NOTE: configName should be set to the appropriate blockSettingName[]

def extSetting(settingName, preferredOption, globalOption, configName, sliderOption, multiplier):
    numAverage = numRange = ruleType = scale = ""
        
    # First, we'll see if the distribution's own settings are set.
    if checkOption(preferredOption):
        if checkCurrentOption(extractAverage(preferredOption)):
            numAverage = str(extractAverage(preferredOption))
        if checkCurrentOption(extractRange(preferredOption)):
            numRange = str(extractRange(preferredOption))
        if checkCurrentOption(extractRule(preferredOption)):
            ruleType = extractRule(preferredOption)
        if checkCurrentOption(extractScale(preferredOption)):
            scale = extractScale(preferredOption)
                
    else: # The preferred options weren't set, let's use globals.
        if checkCurrentOption(extractAverage(globalOption)):
            numAverage = str(extractAverage(globalOption))
        if checkCurrentOption(extractRange(globalOption)):
            numRange = str(extractRange(globalOption))
        if checkCurrentOption(extractRule(globalOption)):
            ruleType = extractRule(globalOption)
        if checkCurrentOption(extractScale(globalOption)):
            scale = extractScale(globalOption)
    
    sliderName = ""
    if checkCurrentOption(sliderOption):
        sliderName = " * "+configName+sliderOption
        
    if multiplier == "1":
        multiplierString = ""
    else:
        multiplierString = " * "+multiplier+" "
      
    return "<Setting name='"+settingName+"' avg=':= "+numAverage+sliderName+" "+multiplierString+"' range=':= "+numRange+sliderName+" "+multiplierString+"' type='"+ruleType+"' scaleTo='"+scale+"' />"


### Vein Type options (Ellipsoid/Bezier)
def setVeinType(veinType):
    veinTypeOption = ""
    veinTypeLower = veinType.lower()
    
    if veinTypeLower.startswith("e"):
        veinTypeOption = "Ellipsoid"
    elif veinTypeLower.startswith("b"):
        veinTypeOption = "Bezier"
    return "branchType='"+veinTypeOption+"'"
    



# ----------------------------------------------------------------------------- #






# ---------------------------- Preset Classes --------------------------------- #
  

# Substitute Preset is the most basic.  It simply replaces one block with another.
# There is little configuration beyond height clamping, and choices of biomes and
# blocks.

class substitutePreset:
    # 'basePreset' is a class containing methods used by all classes, including
    # block, biome, and clamping values.

    # This is required for each class to have its own copy of _presetScript.
    def __init__(self):
        self._presetScript = ""
 
    # Method for adding a list of "main block" 
    def addMainBlocksList(self, blockIndex):
        
        weightDefined = False
        blockWeight = 0.0
        
        # If no weights were assigned to the blocks, we want the blocks to be evenly distributed.
        if spaceRemove(mainBlockWeights[blockIndex][0]) == "MISSING":
            blockWeight = 1.0 / float(len(mainBlocks[blockIndex]))
        else:
            weightDefined = True
            
        for blockSelect in range(0, len(mainBlocks[blockIndex])):
            if weightDefined:
                blockWeight = mainBlockWeights[blockIndex][blockSelect]
            self._presetScript += cogFormatLine(blockCommand("OreBlock", mainBlocks[blockIndex][blockSelect], str(blockWeight)))
    
        return
 
    
    def addAltBlocksList(self, blockIndex):
        
        weightDefined = False
        blockWeight = 0.0
        
        # If no weights were assigned to the blocks, we want the blocks to be evenly distributed.
        if spaceRemove(altBlockWeights[blockIndex][0]) == "MISSING":
            blockWeight = 1.0 / float(len(altBlocks[blockIndex]))
        else:
            weightDefined = True
            
        for blockSelect in range(0, len(altBlocks[blockIndex])):
            if weightDefined:
                blockWeight = altBlockWeights[blockIndex][blockSelect]
            self._presetScript += cogFormatLine(blockCommand("OreBlock", altBlocks[blockIndex][blockSelect], str(blockWeight)))
    
        return
 
    
    def addRepBlocksList(self, blockIndex):
        # Replaces blocks by name.
        weightDefined = False
        blockWeight = 0.0
        
        # If no weights were assigned to the blocks, we want the blocks to be evenly distributed.
        if not checkOption(repBlockWeights[blockIndex]):
            blockWeight = 1.0
        else:
            weightDefined = True
        
        for blockSelect in range(0, len(repBlocks[blockIndex])):
        
            if weightDefined:
                blockWeight = repBlockWeights[blockIndex][blockSelect]
                
            # Certain blocks should use their ore dictionary entries for replacement.
            if repBlocks[blockIndex][blockSelect]=="minecraft:stone":
                self._presetScript += cogFormatLine(blockCommand("ReplacesOre", "stone", str(blockWeight)))
            elif repBlocks[blockIndex][blockSelect]=="minecraft:sand":
                self._presetScript += cogFormatLine(blockCommand("ReplacesOre", "sand", str(blockWeight)))
            else:
                self._presetScript += cogFormatLine(blockCommand("Replaces", repBlocks[blockIndex][blockSelect], str(blockWeight)))
    
        return
    
    def addBiomesList(self, biomeIndex):
        if checkOption(biomeNames[biomeIndex]):
            for biomeStep in range(0, len(biomeNames[biomeIndex])):
                self._presetScript += cogFormatLine(biomeSelect("Biome", biomeNames[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
    
    def addBiomeTypesList(self, biomeIndex):
        if checkOption(biomeTypes[biomeIndex]):
            for biomeStep in range(0, len(biomeTypes[biomeIndex])):
                self._presetScript += cogFormatLine(biomeSelect("BiomeType", biomeTypes[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
    
    def addAvoidBiomesList(self, biomeIndex):
        if checkOption(biomeAvoidTypes[biomeIndex]):
            for biomeStep in range(0, len(biomeAvoidNames[biomeIndex])):
                self._presetScript += cogFormatLine(biomeIgnore("Biome", biomeAvoidNames[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
    
    def addAvoidBiomeTypesList(self, biomeIndex):
        if checkOption(biomeAvoidNames[biomeIndex]):
            for biomeStep in range(0, len(biomeAvoidTypes[biomeIndex])):
                self._presetScript += cogFormatLine(biomeIgnore("BiomeType", biomeAvoidTypes[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
        
    def addPreferredBiomesList(self, biomeIndex):
        if checkOption(biomePreferNames[biomeIndex]):
            for biomeStep in range(0, len(biomePreferNames[biomeIndex])):
                self._presetScript += cogFormatLine(biomeSelect("Biome", biomePreferNames[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
        
    def addPreferredBiomeTypesList(self, biomeIndex):
        if checkOption(biomePreferTypes[biomeIndex]):
            for biomeStep in range(0, len(biomePreferTypes[biomeIndex])):
                self._presetScript += cogFormatLine(biomeSelect("BiomeType", biomePreferTypes[biomeIndex][biomeStep], biomeRainfall[biomeIndex], biomeTmperature[biomeIndex]))
            
        return
    
    def addCogIndent(self, indentValue):
        cogIndent(indentValue)
        
        return
    
    def addBlankLine(self):
        self._presetScript += "\n"
        
        return
        
    def addComment(self, comment):
        self._presetScript += cogFormatComment(comment)
        
        return 
        
    def addBoxComment(self, comment):
        self._presetScript += cogFormatBoxComment(comment)
        
        return 
        
    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<Substitute name='"+blockSettingName[blockIndex]+"Substitute' "+distHeightRange(subHeightRange[blockIndex], clampRange[blockIndex])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Substitute>")
    
    def getPresetScript(self):
        return self._presetScript
        

# This is a blank preset for those wanting a blank XML Canvas to design
# their configurations.
class nullPreset(substitutePreset):

    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<NULL name='"+blockSettingName[blockIndex]+"NULL'>")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self._presetScript += "\n\n"
        self._presetScript += cogFormatLine("<!-- Enter your distribution code here -->")
        self._presetScript += "\n\n"
        cogIndent(-1)
        self._presetScript += cogFormatLine("</NULL>")

# The Vanilla preset is designed to mimic classic minecraft orespawn.
# Doing this will require a few extra commands.
        
class vanillaPreset(substitutePreset):
    def addSizeSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("Size", stdSize[blockIndex], distSize[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
    
    def addFreqSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("Frequency", stdFreq[blockIndex], distFreq[blockIndex], blockSettingName[blockIndex], "Freq", multiplier))
    
        return
    
    def addHeightSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("Height", stdHeight[blockIndex], distHeight[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addParentRangeSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("ParentRangeLimit", stdParentRange[blockIndex], distParentRange[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<StandardGen name='"+blockSettingName[blockIndex]+"Standard' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addSizeSetting(blockIndex, "1")
        self.addFreqSetting(blockIndex, "1")
        self.addHeightSetting(blockIndex, "1")
        self.addParentRangeSetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</StandardGen>")
        
        

# The Cloud preset provides a large, strategic deposit.
        
class cloudPreset(substitutePreset):
    def addRadiusSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("CloudRadius", cloudRadius[blockIndex], distSize[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
        
    def addThicknessSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("CloudThickness", cloudThickness[blockIndex], distSize[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
    
    def addFreqSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("DistributionFrequency", cloudFreq[blockIndex], distFreq[blockIndex], blockSettingName[blockIndex], "Freq", multiplier))
    
        return
    
    def addHeightSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("CloudHeight", cloudHeight[blockIndex], distHeight[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addParentRangeSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("ParentRangeLimit", cloudParentRange[blockIndex], distParentRange[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
        
    def addNoiseSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("CloudSizeNoise", cloudNoise[blockIndex], cloudNoise[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addInclinationSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("CloudInclination", cloudInclination[blockIndex], cloudInclination[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addDensitySetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("OreDensity", cloudDensity[blockIndex], distDensity[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addVolumeNoiseCutoffSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("OreVolumeNoiseCutoff", cloudNoiseCutoff[blockIndex], cloudNoiseCutoff[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addRadiusMultSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("OreRadiusMult", cloudRadiusMult[blockIndex], cloudRadiusMult[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<Cloud name='"+blockSettingName[blockIndex]+"Cloud' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addRadiusSetting(blockIndex, "1")
        self.addThicknessSetting(blockIndex, "1")
        self.addFreqSetting(blockIndex, "1")
        self.addHeightSetting(blockIndex, "1")
        self.addParentRangeSetting(blockIndex, "1")
        self.addNoiseSetting(blockIndex, "1")
        self.addInclinationSetting(blockIndex, "1")
        self.addDensitySetting(blockIndex, "1")
        self.addVolumeNoiseCutoffSetting(blockIndex, "1")
        self.addRadiusMultSetting(blockIndex, "1")
        if distHint[blockIndex][0] == "yes":
            # The next step is to set up hint veins to make the deposits findable.
            currentPreset = veinHintPreset()
            currentPreset.setPresetScript(blockIndex, "HintVeins")
            cogIndent(1)
            self._presetScript += currentPreset.getPresetScript()
            cogIndent(-1)
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Cloud>")
        # Now to repeat the step for preferred biomes, essentially tripling the distributions in those biomes.
        
        if checkOption(biomePreferNames[blockIndex]) or checkOption(biomePreferTypes[blockIndex]):
            self._presetScript += "\n"
            self._presetScript += cogFormatComment("Beginning \"Preferred\" configuration.")
            self._presetScript += cogFormatLine("<Cloud name='"+blockSettingName[blockIndex]+"PreferredCloud' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine("Ore generation is doubled in preferred biomes.")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addMainBlocksList(blockIndex)
            self.addRepBlocksList(blockIndex)
            self.addPreferredBiomesList(blockIndex)
            self.addPreferredBiomeTypesList(blockIndex)
            self.addAvoidBiomesList(blockIndex)
            self.addAvoidBiomeTypesList(blockIndex)
            self.addRadiusSetting(blockIndex, "1")
            self.addThicknessSetting(blockIndex, "1")
            self.addFreqSetting(blockIndex, "1")
            self.addHeightSetting(blockIndex, "1")
            self.addParentRangeSetting(blockIndex, "1")
            self.addNoiseSetting(blockIndex, "1")
            self.addInclinationSetting(blockIndex, "1")
            self.addDensitySetting(blockIndex, "1")
            self.addVolumeNoiseCutoffSetting(blockIndex, "1")
            self.addRadiusMultSetting(blockIndex, "1")
            # The next step is to set up hint veins to make the deposits findable.
            if distHint[blockIndex][0] == "yes":
               currentPreset = veinHintPreset()        
               currentPreset.setPresetPreferredScript(blockIndex, "HintVeins")
               cogIndent(1)
               self._presetScript += currentPreset.getPresetScript()
               cogIndent(-1)
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Cloud>")
            self._presetScript += cogFormatComment("\"Preferred\" configuration complete.")
            self._presetScript += "\n"
            
# The stratum preset produces a wide, thin, and flat, disk of ore.
class cloudStratumPreset (cloudPreset): 
    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<Cloud name='"+blockSettingName[blockIndex]+"Cloud' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addRadiusSetting(blockIndex, "1")
        self.addThicknessSetting(blockIndex, "1")
        self.addFreqSetting(blockIndex, "1")
        self.addHeightSetting(blockIndex, "1")
        self.addParentRangeSetting(blockIndex, "1")
        self.addNoiseSetting(blockIndex, "1")
        self.addInclinationSetting(blockIndex, "1")
        self.addDensitySetting(blockIndex, "1")
        self.addVolumeNoiseCutoffSetting(blockIndex, "1")
        self.addRadiusMultSetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Cloud>")
        # Now to repeat the step for preferred biomes, essentially tripling the distributions in those biomes.
        
        if checkOption(biomePreferNames[blockIndex]) or checkOption(biomePreferTypes[blockIndex]):
            self._presetScript += "\n"
            self._presetScript += cogFormatComment("Beginning \"Preferred\" configuration.")
            self._presetScript += cogFormatLine("<Cloud name='"+blockSettingName[blockIndex]+"PreferredCloud' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine("Ore generation is doubled in preferred biomes.")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addMainBlocksList(blockIndex)
            self.addRepBlocksList(blockIndex)
            self.addPreferredBiomesList(blockIndex)
            self.addPreferredBiomeTypesList(blockIndex)
            self.addAvoidBiomesList(blockIndex)
            self.addAvoidBiomeTypesList(blockIndex)
            self.addRadiusSetting(blockIndex, "1")
            self.addThicknessSetting(blockIndex, "1")
            self.addFreqSetting(blockIndex, "1")
            self.addHeightSetting(blockIndex, "1")
            self.addParentRangeSetting(blockIndex, "1")
            self.addNoiseSetting(blockIndex, "1")
            self.addInclinationSetting(blockIndex, "1")
            self.addDensitySetting(blockIndex, "1")
            self.addVolumeNoiseCutoffSetting(blockIndex, "1")
            self.addRadiusMultSetting(blockIndex, "1")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Cloud>")
            self._presetScript += cogFormatComment("\"Preferred\" configuration complete.")
            self._presetScript += "\n"
    
# The Vein preset provides a large motherlode with multiple branches.
        
class veinPreset(substitutePreset):
    def addMotherlodeFrequencySetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("MotherlodeFrequency", veinMotherlodeFreq[blockIndex], distFreq[blockIndex], blockSettingName[blockIndex], "Freq", multiplier))
    
        return
        
    def addMotherlodeSizeSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("MotherlodeSize", veinMotherlodeSize[blockIndex], distSize[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
    
    def addMotherlodeHeightSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("MotherlodeHeight", veinMotherlodeHeight[blockIndex], distHeight[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addMotherlodeRangeLimitSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("MotherlodeRangeLimit", veinMotherlodeRangeLimit[blockIndex], distParentRange[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addBranchFrequencySetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("BranchFrequency", veinBranchFreq[blockIndex], veinBranchFreq[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
        
    def addBranchInclinationSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("BranchInclination", veinBranchInclination[blockIndex], veinBranchInclination[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addBranchLengthSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("BranchLength", veinBranchLength[blockIndex], veinBranchLength[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addBranchHeightLimitSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(extSetting("BranchHeightLimit", veinBranchHeightLimit[blockIndex], veinBranchHeightLimit[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addSegmentForkFrequencySetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentForkFrequency", veinSegmentForkFreq[blockIndex], veinSegmentForkFreq[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addSegmentForkLengthMultSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentForkLengthMult", veinSegmentForkLength[blockIndex], veinSegmentForkLength[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addSegmentLengthSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentLength", veinSegmentLength[blockIndex], veinSegmentLength[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
    
    def addSegmentAngleSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentAngle", veinSegmentAngle[blockIndex], veinSegmentAngle[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addSegmentPitchSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentPitch", veinSegmentPitch[blockIndex], veinSegmentPitch[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addSegmentRadiusSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("SegmentRadius", veinSegmentRadius[blockIndex], veinSegmentRadius[blockIndex], blockSettingName[blockIndex], "Size", multiplier))
    
        return
    
    def addOreDensitySetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("OreDensity", veinOreDensity[blockIndex], distDensity[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def addOreRadiusMultSetting(self, blockIndex, multiplier):
        self._presetScript += cogFormatLine(mainSetting("OreRadiusMult", veinOreRadiusMult[blockIndex], veinOreRadiusMult[blockIndex], blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
    
    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"Veins' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setVeinType(veinBranchType[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addMotherlodeFrequencySetting(blockIndex, "1")
        self.addMotherlodeSizeSetting(blockIndex, "1")
        self.addMotherlodeHeightSetting(blockIndex, "1")
        self.addMotherlodeRangeLimitSetting(blockIndex, "1")
        self.addBranchFrequencySetting(blockIndex, "1")
        self.addBranchInclinationSetting(blockIndex, "1")
        self.addBranchLengthSetting(blockIndex, "1")
        self.addBranchHeightLimitSetting(blockIndex, "1")
        self.addSegmentForkFrequencySetting(blockIndex, "1")
        self.addSegmentForkLengthMultSetting(blockIndex, "1")
        self.addSegmentLengthSetting(blockIndex, "1")
        self.addSegmentAngleSetting(blockIndex, "1")
        self.addSegmentPitchSetting(blockIndex, "1")
        self.addSegmentRadiusSetting(blockIndex, "1")
        self.addOreDensitySetting(blockIndex, "1")
        self.addOreRadiusMultSetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        # Now to repeat the step for preferred biomes, essentially tripling the distributions in those biomes.
        
        if checkOption(biomePreferNames[blockIndex]) or checkOption(biomePreferTypes[blockIndex]):
            self._presetScript += "\n"
            self._presetScript += cogFormatComment("Beginning \"Preferred\" configuration.")
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"PreferredVeins' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setVeinType(veinBranchType[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine("Ore generation is doubled in preferred biomes.")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addMainBlocksList(blockIndex)
            self.addRepBlocksList(blockIndex)
            self.addPreferredBiomesList(blockIndex)
            self.addPreferredBiomeTypesList(blockIndex)
            self.addAvoidBiomesList(blockIndex)
            self.addAvoidBiomeTypesList(blockIndex)
            self.addMotherlodeFrequencySetting(blockIndex, "1")
            self.addMotherlodeSizeSetting(blockIndex, "1")
            self.addMotherlodeHeightSetting(blockIndex, "1")
            self.addMotherlodeRangeLimitSetting(blockIndex, "1")
            self.addBranchFrequencySetting(blockIndex, "1")
            self.addBranchInclinationSetting(blockIndex, "1")
            self.addBranchLengthSetting(blockIndex, "1")
            self.addBranchHeightLimitSetting(blockIndex, "1")
            self.addSegmentForkFrequencySetting(blockIndex, "1")
            self.addSegmentForkLengthMultSetting(blockIndex, "1")
            self.addSegmentLengthSetting(blockIndex, "1")
            self.addSegmentAngleSetting(blockIndex, "1")
            self.addSegmentPitchSetting(blockIndex, "1")
            self.addSegmentRadiusSetting(blockIndex, "1")
            self.addOreDensitySetting(blockIndex, "1")
            self.addOreRadiusMultSetting(blockIndex, "1")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
            self._presetScript += cogFormatComment("\"Preferred\" configuration complete.")
            self._presetScript += "\n"

# The Compound Vein preset inherits the veins, and adds a second distribution
# within the first.  This obviously covers the pipe vein preset, but can be
# applied to any configuration of main and alternate ores.
        
class veinCompoundPreset(veinPreset):    
    def addInvRepBlocksList(self, blockIndex):
        for blockSelect in range(0, len(mainBlocks[blockIndex])):
            self._presetScript += cogFormatLine(blockCommand("Replaces", mainBlocks[blockIndex][blockSelect], "1.0"))
    
        return
        
    def addPipeVeinCoreDensity(self, blockIndex, multiplier):
        coreDensity = []
        
        coreDensity.append("1.0")
        coreDensity.append("0")
        coreDensity.append("normal")
     
        self._presetScript += cogFormatLine(mainSetting("OreDensity", coreDensity, coreDensity, blockSettingName[blockIndex], "MISSING", multiplier))
    
        return
                

    def setPresetScript(self, blockIndex, preset):
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"Veins' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addMotherlodeFrequencySetting(blockIndex, "1")
        self.addMotherlodeSizeSetting(blockIndex, "1")
        self.addMotherlodeHeightSetting(blockIndex, "1")
        self.addMotherlodeRangeLimitSetting(blockIndex, "1")
        self.addBranchFrequencySetting(blockIndex, "1")
        self.addBranchInclinationSetting(blockIndex, "1")
        self.addBranchLengthSetting(blockIndex, "1")
        self.addBranchHeightLimitSetting(blockIndex, "1")
        self.addSegmentForkFrequencySetting(blockIndex, "1")
        self.addSegmentForkLengthMultSetting(blockIndex, "1")
        self.addSegmentLengthSetting(blockIndex, "1")
        self.addSegmentAngleSetting(blockIndex, "1")
        self.addSegmentPitchSetting(blockIndex, "1")
        self.addSegmentRadiusSetting(blockIndex, "1")
        self.addOreDensitySetting(blockIndex, "1")
        self.addOreRadiusMultSetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        self._presetScript += "\n"
        self._presetScript += cogFormatComment("Configuring contained material.")
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"VeinsPipe' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"Veins' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)        
        self.addAltBlocksList(blockIndex)
        self.addRepBlocksList(blockIndex)
        self.addInvRepBlocksList(blockIndex)
        self.addMotherlodeSizeSetting(blockIndex, "0.5")
        self.addSegmentRadiusSetting(blockIndex, "0.5")
        if presetName(preset) == "Pipe Veins":
            self.addPipeVeinCoreDensity(blockIndex, "1")
        else:
            self.addOreDensitySetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        # Now to repeat the step for preferred biomes, essentially tripling the distributions in those biomes.
        
        if checkOption(biomePreferNames[blockIndex]) or checkOption(biomePreferTypes[blockIndex]):
            self._presetScript += "\n"
            self._presetScript += cogFormatComment("Beginning \"Preferred\" configuration.")
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"VeinsPrefer' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine("Ore generation is doubled in preferred biomes.")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addMainBlocksList(blockIndex)
            self.addRepBlocksList(blockIndex)
            self.addPreferredBiomesList(blockIndex)
            self.addPreferredBiomeTypesList(blockIndex)
            self.addAvoidBiomesList(blockIndex)
            self.addAvoidBiomeTypesList(blockIndex)
            self.addMotherlodeFrequencySetting(blockIndex, "1")
            self.addMotherlodeSizeSetting(blockIndex, "1")
            self.addMotherlodeHeightSetting(blockIndex, "1")
            self.addMotherlodeRangeLimitSetting(blockIndex, "1")
            self.addBranchFrequencySetting(blockIndex, "1")
            self.addBranchInclinationSetting(blockIndex, "1")
            self.addBranchLengthSetting(blockIndex, "1")
            self.addBranchHeightLimitSetting(blockIndex, "1")
            self.addSegmentForkFrequencySetting(blockIndex, "1")
            self.addSegmentForkLengthMultSetting(blockIndex, "1")
            self.addSegmentLengthSetting(blockIndex, "1")
            self.addSegmentAngleSetting(blockIndex, "1")
            self.addSegmentPitchSetting(blockIndex, "1")
            self.addSegmentRadiusSetting(blockIndex, "1")
            self.addOreDensitySetting(blockIndex, "1")
            self.addOreRadiusMultSetting(blockIndex, "1")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
            self._presetScript += "\n"
            self._presetScript += cogFormatComment("Contained Material for Preferred Distributions.")
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"VeinsPreferPipe' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"VeinsPrefer' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)        
            self.addAltBlocksList(blockIndex)
            self.addInvRepBlocksList(blockIndex)
            self.addRepBlocksList(blockIndex)
            self.addMotherlodeSizeSetting(blockIndex, "0.5")
            self.addSegmentRadiusSetting(blockIndex, "0.5")
            if presetName(preset) == "Pipe Veins":
                self.addPipeVeinCoreDensity(blockIndex, "1")
            else:
                self.addOreDensitySetting(blockIndex, "1")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
            self._presetScript += cogFormatComment("\"Preferred\" configuration complete.")
            self._presetScript += "\n"
    
    
class veinGeodePreset(veinPreset):  

    # The center of any geode is a bubble of air.  The center will not have any other material.
    def addAirBlock(self, blockIndex):
        self._presetScript += cogFormatLine(blockCommand("OreBlock", "minecraft:air", "1.0"))
        return

    # The bubble must be able to replace both shell and ore materials.
    def addRepBubbleBlocksList(self, blockIndex):
        for blockSelect in range(0, len(altBlocks[blockIndex])):
            self._presetScript += cogFormatLine(blockCommand("Replaces", altBlocks[blockIndex][blockSelect], "1.0"))
        
        for blockSelect in range(0, len(mainBlocks[blockIndex])):
            self._presetScript += cogFormatLine(blockCommand("Replaces", mainBlocks[blockIndex][blockSelect], "1.0"))
    
        return
 
    # At the same time, the ore layer should always be able to replace the outer shell's material.
    def addRepShellBlocksList(self, blockIndex):
        for blockSelect in range(0, len(altBlocks[blockIndex])):
            self._presetScript += cogFormatLine(blockCommand("Replaces", altBlocks[blockIndex][blockSelect], "1.0"))
    
        return
    
    # A custom motherlode size is necessary for inner shells to avoid extraneous imports.
    def addGeodeSubMotherlodeSizeSetting(self, ruleType):
        self._presetScript += cogFormatLine("<Setting name='MotherlodeSize' avg=':= _default_ * 0.5' range=':= _default_ * 0.5' type='"+ruleType+"' />")
      
        return
    
    
    def setPresetScript(self, blockIndex, preset):
        # First, we have the outer shell layer.
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeShell' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setVeinType(veinBranchType[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addAltBlocksList(blockIndex) # Shell material
        self.addRepBlocksList(blockIndex) # Normal replacement material
        self.addBiomesList(blockIndex)
        self.addBiomeTypesList(blockIndex)
        self.addAvoidBiomesList(blockIndex)
        self.addAvoidBiomeTypesList(blockIndex)
        self.addMotherlodeFrequencySetting(blockIndex, "1")
        self.addMotherlodeSizeSetting(blockIndex, "1")
        self.addMotherlodeHeightSetting(blockIndex, "1")
        self.addMotherlodeRangeLimitSetting(blockIndex, "1")
        self.addOreDensitySetting(blockIndex, "1")
        self.addOreRadiusMultSetting(blockIndex, "1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        # Next, the inner ore layer.
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeOre' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"GeodeShell' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex) # Ore layer
        self.addRepBlocksList(blockIndex) # Normal replacement material
        self.addRepShellBlocksList(blockIndex) # Shell material
        self.addGeodeSubMotherlodeSizeSetting("uniform")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        # Finally, the central air bubble.
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeBubble' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"GeodeOre' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addAirBlock(blockIndex) # Air Bubble
        self.addRepBubbleBlocksList(blockIndex) # Shell material
        self.addRepBlocksList(blockIndex) # Normal replacement material
        self.addGeodeSubMotherlodeSizeSetting("uniform")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
        # Now to repeat the step for preferred biomes, essentially tripling the distributions in those biomes.
        self._presetScript += "\n"
        self._presetScript += cogFormatComment("Beginning \"Preferred\" configuration.")
        
        if checkOption(biomePreferNames[blockIndex]) or checkOption(biomePreferTypes[blockIndex]):
            
            # First, we have the outer shell layer.
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeShell' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine(presetDescription(preset))
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addAltBlocksList(blockIndex) # Shell material
            self.addRepBlocksList(blockIndex) # Normal replacement material
            self.addPreferredBiomesList(blockIndex)
            self.addPreferredBiomeTypesList(blockIndex)
            self.addAvoidBiomesList(blockIndex)
            self.addAvoidBiomeTypesList(blockIndex)
            self.addMotherlodeFrequencySetting(blockIndex, "1")
            self.addMotherlodeSizeSetting(blockIndex, "1")
            self.addMotherlodeHeightSetting(blockIndex, "1")
            self.addMotherlodeRangeLimitSetting(blockIndex, "1")
            self.addOreDensitySetting(blockIndex, "1")
            self.addOreRadiusMultSetting(blockIndex, "1")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
            # Next, the inner ore layer.
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeOre' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"GeodeShell' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine(presetDescription(preset))
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addMainBlocksList(blockIndex) # Ore layer
            self.addRepShellBlocksList(blockIndex) # Shell material
            self.addGeodeSubMotherlodeSizeSetting("uniform")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
            # Finally, the central air bubble.
            self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"GeodeBubble' "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" inherits='"+blockSettingName[blockIndex]+"GeodeOre' "+setVeinType(veinBranchType[blockIndex][0])+" "+seedAttribute(blockSeed[blockIndex][0])+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
            cogIndent(1)
            self._presetScript += cogFormatLine("<Description>")
            cogIndent(1)
            self._presetScript += cogWrappedLine(presetDescription(preset))
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Description>")
            self.addAirBlock(blockIndex) # Air Bubble
            self.addRepBubbleBlocksList(blockIndex) # Shell material
            self.addGeodeSubMotherlodeSizeSetting("uniform")
            cogIndent(-1)
            self._presetScript += cogFormatLine("</Veins>")
        
            
# Hint Veins have a different purpose than most.  They scatter ores in 
# stone and other materials to hint at the presence of a vein.
        
class veinHintPreset(veinPreset):   
    def addHintRepBlocksList(self):
        hintReplace = []
        hintReplace.append("minecraft:dirt")
        hintReplace.append("minecraft:sandstone")
        hintReplace.append("minecraft:stone")
        hintReplace.append("minecraft:gravel")
        
        for blockSelect in range(0, len(hintReplace)):
            if hintReplace[blockSelect]=="minecraft:stone":
                self._presetScript += cogFormatLine(blockCommand("ReplacesOre", "stone", "1.0"))
            elif hintReplace[blockSelect]=="minecraft:sand":
                self._presetScript += cogFormatLine(blockCommand("ReplacesOre", "sand", "1.0"))
            else:
                self._presetScript += cogFormatLine(blockCommand("Replaces", hintReplace[blockSelect], "1.0"))
    
        return

    def setPresetScript(self, blockIndex, preset):        
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"HintVeins' "+setVeinType(veinBranchType[blockIndex][0])+" "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine(presetDescription(preset))
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addHintRepBlocksList()
        self.addMotherlodeFrequencySetting(blockIndex, "0.1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")
    
    def setPresetPreferredScript(self, blockIndex, preset):        
        self._presetScript += cogFormatLine("<Veins name='"+blockSettingName[blockIndex]+"PreferredHintVeins' "+setVeinType(veinBranchType[blockIndex][0])+" "+distHeightRange(stdHeightRange[blockIndex], clampRange[blockIndex])+" "+presetInherit(preset)+" "+setWireframe(wireframeActive[blockIndex][0], wireframeColor[blockIndex][0])+" "+setBoundingBox(boundBoxActive[blockIndex][0], boundBoxColor[blockIndex][0])+">")
        cogIndent(1)
        self._presetScript += cogFormatLine("<Description>")
        cogIndent(1)
        self._presetScript += cogWrappedLine("Ore generation is doubled in preferred biomes.")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Description>")
        self.addMainBlocksList(blockIndex)
        self.addHintRepBlocksList()
        self.addMotherlodeFrequencySetting(blockIndex, "0.1")
        cogIndent(-1)
        self._presetScript += cogFormatLine("</Veins>")     

# ----------------------------------------------------------------------------- #






# -------------------- Process Support Commands ------------------------------- #

### Assemble a list of replacement blocks for the current world.
def replacementSectionList(dimName):
    replacementBlockList = []
    
    # Make a list of replacement blocks for the specified dimension.
    for mainBlockSelect in range(0, len(mainBlocks)):
        if dimensionCheck(dimensionList[mainBlockSelect], dimName) and checkOption(repBlocks[mainBlockSelect]):
            for replacementBlockSelect in range(0, len(repBlocks[mainBlockSelect])):
                replacementBlockList.append(spaceRemove(repBlocks[mainBlockSelect][replacementBlockSelect]))
    
    # Remove duplicate entries from the list.
    replacementFinalBlockList = list(set(replacementBlockList))
    replacementFinalBlockList.sort()
       
    return replacementFinalBlockList
    
def chosenBlockList(replacementBlock, dimName):
    cleanupBlockList = []
    
    # We will start by collecting all the substitutable main blocks.
    for mainBlockSelect in range(0, len(mainBlocks)):
        if dimensionCheck(dimensionList[mainBlockSelect], dimName) and initSubMain[mainBlockSelect][0] == "yes" and extractFirstBlock(repBlocks[mainBlockSelect]) == replacementBlock:
            for cleanupBlockSelect in range(0, len(mainBlocks[mainBlockSelect])):
                cleanupBlockList.append(spaceRemove(mainBlocks[mainBlockSelect][cleanupBlockSelect]))
    
    # Next, we will collect the substitutable alternate blocks.
    for altBlockSelect in range(0, len(altBlocks)):
        if dimensionCheck(dimensionList[altBlockSelect], dimName)  and initSubAlt[altBlockSelect][0]   == "yes" and extractFirstBlock(repBlocks[altBlockSelect]) == replacementBlock:
            for cleanupBlockSelect in range(0, len(altBlocks[mainBlockSelect])):
                cleanupBlockList.append(spaceRemove(altBlocks[altBlockSelect][cleanupBlockSelect]))
    
    # Remove all duplicate entries from the combined list.
    cleanupFinalBlockList = list(set(cleanupBlockList))
    cleanupFinalBlockList.sort()
            
    return cleanupFinalBlockList

### Make a list of "?blockExists()" conditions, separated by an OR statement ("|")
def blockExistList(blockIndex):
    blockChecklist = []
    altChecklist = []
    blockCheckString = "("

    for blockSelect in range(0, len(mainBlocks[blockIndex])):
        blockChecklist.append("?blockExists(\""+mainBlocks[blockIndex][blockSelect]+"\")")
            
    for blockCheckCount in range(0, len(blockChecklist)):
        if blockCheckCount > 0:
            blockCheckString += "  &amp; "
        blockCheckString += blockChecklist[blockCheckCount]
    
    for blockSelect in range(0, len(altBlocks[blockIndex])):
        if altBlocks[blockIndex][blockSelect] != "minecraft:stone":
            altChecklist.append("?blockExists(\""+altBlocks[blockIndex][blockSelect]+"\")")
          
    if len(altBlocks[blockIndex]) > 0 and altBlocks[blockIndex][0] != "minecraft:stone":
        blockCheckString += ") &amp; ("
            
    for blockCheckCount in range(0, len(altChecklist)):
        if blockCheckCount > 0:
            blockCheckString += "  &amp; "            
        blockCheckString += altChecklist[blockCheckCount]
        
    blockCheckString += ")"
    
    return(blockCheckString)
    
def presetSelection(blockIndex, presetSelect):
    distOutput = ""
    
    distOutput += cogFormatLine("<IfCondition condition=':= "+blockExistList(blockIndex)+" '>\n")
    distOutput += cogFormatLine("<Choice value='"+presetList[blockIndex][presetSelect]+"' displayValue='"+presetName(presetList[blockIndex][presetSelect])+"'>")
    cogIndent(1)
    distOutput += cogFormatLine("<Description>")
    cogIndent(1)
    distOutput += cogFormatLine(presetLiteDescription(presetList[blockIndex][presetSelect]))
    cogIndent(-1)
    distOutput += cogFormatLine("</Description>")
    cogIndent(-1)
    distOutput += cogFormatLine("</Choice>")
    distOutput += cogFormatLine("</IfCondition>\n")
    
    
    return distOutput
    
def modHandleState():
    if modHandle.lower() == "yes":
        return "true"
    else:
        return "false"
    
def modCleanupState():
    if modHandle.lower() == "yes":
        return "true"
    else:
        return "false"
    

# ----------------------------------------------------------------------------- #
    
    

# ----------------------------------------------------------------------------- #

def controlsSetup(blockIndex):    
    controlsOutput = ""

    controlsOutput += cogFormatLine("<OptionChoice name='"+blockSettingName[blockIndex]+"Dist'"+ifDistActive(distActive[blockIndex])+" displayState=':= if(?enable"+modConfigName+", \"shown\", \"hidden\")' displayGroup='group"+modConfigName+"'>")
    cogIndent(1)
    controlsOutput += cogFormatLine("<Description> Controls how "+blockName[blockIndex]+" is generated </Description>")
    controlsOutput += cogFormatLine("<DisplayName>"+modName+" "+blockName[blockIndex]+"</DisplayName>")
    
    for selectPreset in range(0, len(presetList[blockIndex])):
        controlsOutput += presetSelection(blockIndex, selectPreset)
    
    controlsOutput += cogFormatLine("<Choice value='none' displayValue='None' description='"+blockName[blockIndex]+" is not generated in the world.'/>")
    
    cogIndent(-1)
    controlsOutput += cogFormatLine("</OptionChoice>")
    controlsOutput += cogFormatLine("<OptionNumeric name='"+blockSettingName[blockIndex]+"Freq' default='1'  min='0' max='5' displayState=':= if(?enable"+modConfigName+", if(?advOptions, \"shown\", \"hidden\"), \"hidden\")' displayGroup='group"+modConfigName+"'>")

    cogIndent(1)
    controlsOutput += cogFormatLine("<Description> Frequency multiplier for "+modName+" "+blockName[blockIndex]+" distributions </Description>")
    controlsOutput += cogFormatLine("<DisplayName>"+modName+" "+blockName[blockIndex]+" Freq.</DisplayName>")
    cogIndent(-1)
    controlsOutput += cogFormatLine("</OptionNumeric>")
    controlsOutput += cogFormatLine("<OptionNumeric name='"+blockSettingName[blockIndex]+"Size' default='1'  min='0' max='5' displayState=':= if(?enable"+modConfigName+", if(?advOptions, \"shown\", \"hidden\"), \"hidden\")' displayGroup='group"+modConfigName+"'>")
    cogIndent(1)
    controlsOutput += cogFormatLine("<Description> Size multiplier for "+modName+" "+blockName[blockIndex]+" distributions </Description>")
    controlsOutput += cogFormatLine("<DisplayName>"+modName+" "+blockName[blockIndex]+" Size</DisplayName>")
    cogIndent(-1)
    controlsOutput += cogFormatLine("</OptionNumeric>")

    return controlsOutput

def distributionSetup(blockIndex, dimension):
    # Start with empty script.
    distOutput = ""
    
    for presetSelect in range (0, len(presetList[blockIndex])):
        if presetName(presetList[blockIndex][presetSelect]) == "Substitution":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = substitutePreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Vanilla":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = vanillaPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Strategic Clouds" or presetName(presetList[blockIndex][presetSelect]) == "Custom Cloud":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = cloudPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Strata":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = cloudStratumPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Layered Veins" or presetName(presetList[blockIndex][presetSelect]) == "Vertical Veins" or presetName(presetList[blockIndex][presetSelect]) == "Small Deposits" or presetName(presetList[blockIndex][presetSelect]) == "Huge Veins" or presetName(presetList[blockIndex][presetSelect]) == "Sparse Veins" or presetName(presetList[blockIndex][presetSelect]) == "Custom Veins":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = veinPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Compound Veins" or presetName(presetList[blockIndex][presetSelect]) == "Pipe Veins":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = veinCompoundPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Geode":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = veinGeodePreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
        elif presetName(presetList[blockIndex][presetSelect]) == "Blank":
            distOutput += "\n"
            distOutput += cogFormatComment("Starting "+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+".")
            distOutput += cogFormatLine("<ConfigSection>")
            cogIndent(1)
            distOutput += cogFormatLine("<IfCondition condition=':= "+blockSettingName[blockIndex]+"Dist = \""+presetList[blockIndex][presetSelect]+"\"'>")
            cogIndent(1)
            currentPreset = nullPreset()
            currentPreset.setPresetScript(blockIndex, presetList[blockIndex][presetSelect])
            distOutput += currentPreset.getPresetScript()
            cogIndent(-1)
            distOutput += cogFormatLine("</IfCondition>")
            cogIndent(-1)
            distOutput += cogFormatLine("</ConfigSection>")
            distOutput += cogFormatComment(""+presetList[blockIndex][presetSelect]+" Preset for "+blockName[blockIndex]+" is complete.")
            distOutput += "\n"
                    
    return distOutput

### Remove all previously-placed blocks.
def initCleanup(dimName):
    cleanupOutput = ""
    
    # First, we need a list of replacement block sections to populate.
    uniqueSections = replacementSectionList(dimName)
        
    # Now, we need to create the sections, and apply the substitution of
    # the replacement blocks to the main/alternate blocks.
    
    cleanupOutput += "\n" 
    cleanupOutput += cogFormatComment("Starting Original \""+dimName+"\" Block Removal")
    
    for sectionSelect in range(0, len(uniqueSections)):
        cleanupSubOutput = ""
        cleanupSubUse = 0
        
        # Next, we need a list of main and alternate blocks to clean out.
        chosenBlocks = chosenBlockList(uniqueSections[sectionSelect],dimName)
        
        cleanupSubOutput += "\n"
        if (modDetect.lower() != "minecraft") and (modDetect.lower() != "none"):
          cleanupSubOutput += cogFormatLine("<IfCondition condition=':= ?cleanUp"+modConfigName+"'>")
          cogIndent(1)
        cleanupSubOutput += cogFormatLine("<IfCondition condition=':= ?blockExists(\""+uniqueSections[sectionSelect]+"\")'>")
        cogIndent(1)
        cleanupSubOutput += cogFormatLine("<Substitute name='"+modPrefix+spaceRemove(dimName)+"BlockSubstitute"+str(sectionSelect)+"' block='"+uniqueSections[sectionSelect]+"'>")
        cogIndent(1)
        cleanupSubOutput += cogFormatLine("<Description>")
        cogIndent(1)
        cleanupSubOutput += cogFormatLine("Replace vanilla-generated ore clusters.")
        cogIndent(-1)
        cleanupSubOutput += cogFormatLine("</Description>")
        cleanupSubOutput += cogFormatLine("<Comment>")
        cogIndent(1)
        cleanupSubOutput += cogWrappedLine("The global option deferredPopulationRange must be large enough to catch all ore clusters (>= 32).")
        cogIndent(-1)
        cleanupSubOutput += cogFormatLine("</Comment>")
                
        for blockSelect in range(0, len(chosenBlocks)):
            cleanupSubOutput += cogFormatLine(blockCommand("Replaces", chosenBlocks[blockSelect], "1.0"))
            cleanupSubUse = 1
                
        cogIndent(-1)
        cleanupSubOutput += cogFormatLine("</Substitute>")
        cogIndent(-1)
        cleanupSubOutput += cogFormatLine("</IfCondition>")
        if (modDetect.lower() != "minecraft") and (modDetect.lower() != "none"):
          cogIndent(-1)
          cleanupSubOutput += cogFormatLine("</IfCondition>")
        cleanupSubOutput += "\n"
                
        if cleanupSubUse:
            cleanupOutput += cleanupSubOutput
        
    cleanupOutput += cogFormatComment("Original \""+dimName+"\" Block Removal Complete")
    
    return cleanupOutput


### Minecraft Setup Screen Configuration.

def configSetupSection():
    
    setupOutput = ""
    
    setupOutput += "\n\n\n\n" 
    setupOutput += cogFormatComment("Setup Screen Configuration")
    setupOutput += cogFormatLine("<ConfigSection>")
    cogIndent(1)
    setupOutput += cogFormatLine("<OptionDisplayGroup name='group"+modConfigName+"' displayName='"+modName+"' displayState='shown'>")
    cogIndent(1)
    setupOutput += cogFormatLine("<Description>")
    cogIndent(1)
    setupOutput += cogFormatLine("Distribution options for "+modName+" Ores.")
    cogIndent(-1)
    setupOutput += cogFormatLine("</Description>")
    cogIndent(-1)
    setupOutput += cogFormatLine("</OptionDisplayGroup>")
    
    if modName.lower() == "vanilla":
        setupOutput += cogFormatLine("<OptionDisplayGroup name='vanillaHiddenAssignments' displayName='"+modName+"' displayState='hidden'>")
        cogIndent(1)
        setupOutput += cogFormatLine("<Description>")
        cogIndent(1)
        setupOutput += cogFormatLine("Hidden options solely for variable assignment.")
        cogIndent(-1)
        setupOutput += cogFormatLine("</Description>")
        cogIndent(-1)
        setupOutput += cogFormatLine("</OptionDisplayGroup>")

    
    # New option, designed to allow the player to bypass specific mods in favor of others.  By default, always enabled.
    setupOutput += cogFormatLine("<OptionChoice name='enable"+modConfigName+"' displayName='Handle "+modName+" Setup?' default='"+modHandleState()+"' displayState='shown_dynamic' displayGroup='group"+modConfigName+"'>")
    cogIndent(1)    
    setupOutput += cogFormatLine("<Description> Should Custom Ore Generation handle "+modName+" ore generation? </Description>")
    setupOutput += cogFormatLine("<Choice value=':= ?true' displayValue='Yes' description='Use Custom Ore Generation to handle "+modName+" ores.'/>")
    setupOutput += cogFormatLine("<Choice value=':= ?false' displayValue='No' description='"+modName+" ores will be handled by Minecraft directly.'/>")
    cogIndent(-1)
    setupOutput += cogFormatLine("</OptionChoice>")
    
    if modName.lower() == "vanilla":
        setupOutput += cogFormatLine("<!-- This is hidden, and is for internal configuration only. -->")
        setupOutput += cogFormatLine("<OptionChoice name='vanillaOreGen' displayName='Allow Vanilla Ore Generation?' default=':= !?enable"+modConfigName+"' displayState='hidden' displayGroup='vanillaHiddenAssignments'>")
        cogIndent(1)    
        setupOutput += cogFormatLine("<Description> Should Custom Ore Generation handle "+modName+" ore generation? </Description>")
        setupOutput += cogFormatLine("<Choice value=':= ?true' displayValue='Yes' description='Keep the vanilla oregen disabled.'/>")
        setupOutput += cogFormatLine("<Choice value=':= ?false' displayValue='No' description='"+modName+" ores will be handled by Minecraft directly.'/>")
        cogIndent(-1)
        setupOutput += cogFormatLine("</OptionChoice>")
    
    setupOutput += cogFormatLine("<OptionChoice name='cleanUp"+modConfigName+"' displayName='Use "+modName+" Cleanup?' default='"+modCleanupState()+"' displayState=':= if(?enable"+modConfigName+", \"shown\", \"hidden\")' displayGroup='group"+modConfigName+"'>")
    cogIndent(1)    
    setupOutput += cogFormatLine("<Description> Should Custom Ore Generation use the Substitution Pass to remove all instances of "+modName+" ore from the world?  If the mod's oregen can be turned off in its configuration, then it's recommended to do so, as the substitution pass can slow the game significantly.  If this option is disabled without disabling the mod's own ore generation, you'll end up with two oregens working at once, flooding the world with ore.  Enabled by default to ensure the ores are completely removed. </Description>")
    setupOutput += cogFormatLine("<Choice value=':= ?true' displayValue='Yes' description='Use the substitution pass to clean up "+modName+" ores.'/>")
    setupOutput += cogFormatLine("<Choice value=':= ?false' displayValue='No' description='"+modName+" ores do not need to be cleaned up by a substitution pass.'/>")
    cogIndent(-1)
    setupOutput += cogFormatLine("</OptionChoice>")
    
    for blockSelect in range(0, len(blockName)):
        setupOutput += "\n"
        setupOutput += cogFormatComment(blockName[blockSelect]+" Configuration UI Starting")
        setupOutput += cogFormatLine("<ConfigSection>")
        cogIndent(1)
        setupOutput += controlsSetup(blockSelect)
        cogIndent(-1)
        setupOutput += cogFormatLine("</ConfigSection>")
        setupOutput += cogFormatComment(blockName[blockSelect]+" Configuration UI Complete")
        setupOutput += "\n"
    
    cogIndent(-1)
    setupOutput += cogFormatLine("</ConfigSection>")
    setupOutput += cogFormatComment("Setup Screen Complete")

    return setupOutput

### Dimension configuration

def dimensionSetup(dimName, dimClass):
    blockCount=0 # We start with the first block.
    worldOutput = ""
    
    worldOutput += "\n\n\n\n" 
    worldOutput += cogFormatComment(dimName+" Setup Beginning")
    worldOutput += "\n"
    
    if dimName == "Overworld":
        worldOutput += cogFormatLine("<IfCondition condition=':= ?COGActive'>")
    else:
        worldOutput += cogFormatLine("<IfCondition condition=':= dimension.generator.class = \""+dimClass+"\"'>")
    
    cogIndent(1)
    worldOutput += initCleanup(dimName)
    worldOutput += "\n"
    worldOutput += cogFormatComment("Adding blocks")
    
    for blockSelect in range(0,len(blockName)):
        if dimensionCheck(dimensionList[blockSelect], dimName):
            blockCount += 1
            worldOutput += "\n"
            worldOutput += cogFormatComment("Begin "+blockName[blockSelect]+" Generation")
            worldOutput += distributionSetup(blockSelect, dimName) # Pass the list index, not block name.
            worldOutput += cogFormatComment("End "+blockName[blockSelect]+" Generation")
            worldOutput += "\n"
     
    worldOutput += cogFormatComment("Finished adding blocks")
    cogIndent(-1)
    worldOutput += "\n"
    worldOutput += cogFormatLine("</IfCondition>")
    worldOutput += cogFormatComment(dimName+" Setup Complete")
    worldOutput += "\n"
    
    if blockCount == 0:
        return ""
    else:
        return worldOutput
            
### Whole configuration setting
# This is where the main structure is established, and the various sections are
# launched for generation.

def mainConfigStructure():
    configOutput = "" # create the output configuration
    
    # First, we want the opening comments to describe the mod and its ores.
    blockNameList = grammaticalList([element.lower() for element in blockName])

    configOutput += cogFormatBoxComment("Custom Ore Generation \""+modName+"\" Module: This configuration covers "+blockNameList+".")
    configOutput += "\n\n"
    if modDescription:
        configOutput += cogFormatComment(modDescription)
    
    configOutput += "\n\n\n\n" 
        
    if (modDetect.lower() != "minecraft") and (modDetect.lower() != "none"): # Vanilla minecraft, or self-contained configurations need not be checked.
        configOutput += cogFormatComment("Is the \""+modName+"\" mod on the system?  Let's find out!")
        configOutput += cogFormatLine("<IfModInstalled name=\""+modDetect+"\">")
        configOutput += "\n"
        cogIndent(1)
      
    configOutput += cogFormatComment("Starting Configuration for Custom Ore Generation.")
    configOutput += cogFormatLine("<ConfigSection>")
    configOutput += "\n"    
    cogIndent(1)
    
    # At this point, we pass the configuration onto sub-functions.
    # First, the Setup Screen Configuration...
    configOutput += configSetupSection()
    configOutput += "\n"    
    
    # Now, let's make sure we want to do this... a new option was added in the menu to bypass COG for specific mods.
    configOutput += cogFormatLine("<IfCondition condition=':= ?enable"+modConfigName+"'>")
    cogIndent(1)
    
    # Next, let's get the worlds prepared.  For now, we're limited to the
    # Overworld, Nether, and End, but as new generators can be detected, we can
    # Expand Sprocket's ability to create configurations for additional dimensions.
    configOutput += dimensionSetup("Overworld", "COGActive")
    configOutput += dimensionSetup("Nether", "ChunkProviderHell")
    configOutput += dimensionSetup("End", "ChunkProviderEnd")
    configOutput += dimensionSetup("Flat", "ChunkProviderFlat")
    configOutput += dimensionSetup("Twilight Forest", "ChunkProviderTwilightForest")
    configOutput += dimensionSetup("Aether", "ChunkProviderAether")
    configOutput += dimensionSetup("Aether Dungeons", "ChunkProviderDungeons")
    configOutput += dimensionSetup("Outer Lands", "ChunkProviderOuter")
    configOutput += dimensionSetup("Bedrock Dimension", "ChunkProviderBedrock")
    configOutput += dimensionSetup("Aroma1997s Mining World", "ChunkProviderMining")
    configOutput += dimensionSetup("Galacticraft Space", "ChunkProviderSpace")
    configOutput += dimensionSetup("Galacticraft Orbit", "ChunkProviderOrbit")
    configOutput += dimensionSetup("Galacticraft Moon", "ChunkProviderMoon")
    configOutput += dimensionSetup("Galacticraft Mars", "ChunkProviderMars")
    configOutput += dimensionSetup("Galacticraft Asteroids", "ChunkProviderAsteroids")
    configOutput += dimensionSetup("RFTools", "GenericChunkProvider")
    configOutput += dimensionSetup("MystCraft", "ChunkProviderMyst")
        
    cogIndent(-1)
    configOutput += cogFormatLine("</IfCondition>")
        
    cogIndent(-1)
    configOutput += "\n"
    configOutput += cogFormatLine("</ConfigSection>")
    configOutput += cogFormatComment("Configuration for Custom Ore Generation Complete!")
            
    if (modDetect.lower() != "minecraft") and (modDetect.lower() != "none"): # Don't use a detect line for vanilla minecraft or self-contained configurations.
        cogIndent(-1)
        configOutput += "\n"
        configOutput += cogFormatLine("</IfModInstalled>")
        configOutput += cogFormatComment("The \""+modName+"\" mod is now configured.")
        configOutput += "\n"
    
    configOutput += "\n\n\n\n"
    configOutput += cogFormatBoxComment("This file was made using the Sprocket Advanced Configuration Generator.  If you wish to make your own configurations for a mod not currently supported by Custom Ore Generation, and you don't want the hassle of writing XML, you can find the generator script at its GitHub page: http://https://github.com/reteo/Sprocket")
    
    return configOutput

#print mainConfigStructure()

### Write XML File
# At this point, we can confirm that the configuration is completely assembled
# and there has been no logic errors in the script.  Time to create/open the
# file and write the new configuration to it.

xmlConfigFile = open('./'+modConfigName+'.xml', 'w+')
xmlConfigFile.write(mainConfigStructure())

print "Configuration complete for "+modName+"!\n"
