### NOTE: This branch is for a complete rewrite of the 1.7.10 version.

# Sprocket
Configuration Utility for Custom Ore Gen: First Revival mod
(http://tinyurl.com/qdpekog)

    The Custom Ore Generation mod for Minecraft is one of the best
    discoveries I've made to this point.
    
    However, it is apparent that the XML files it requires are a
    particularly tricky thing to deal with; to properly configure COG,
    you need to spend a lot of time writing a large XML file with a lot
    of sections and options, just to get it to work with one or two
    ores.  On the other hand, if you have a mod with a lot of ores, such
    as Metallurgy or Nether Ores, this can turn into a major hassle in a
    hurry... especially when you spend the better part of a week simply
    hunting down a missing angle bracket or misspelled element!
    
    Enter Sprocket.  With Sprocket, you can get a baseline XML file
    built in a short time, just by making an INI file with the key
    information for each ore and the mod.  Then, by running Sprocket on
    the config file, a fully-valid, basic XML file is generated,
    essentially giving you a shortcut to the point where you simply need
    to tweak the file for the needed settings.

# Using the Program

Sprocket is a command-line program.  It requires that you have Python 2.7
installed on your system.  You can pick up Python 2.7 from www.python.org

To run the program, you have one of two options:
        
        `sprocket.py name-of-file.ini`

or 

        `python sprocket.py name-of-file.ini`

If Sprocket works correctly, you should either see it start a long chain
of progress messages, starting with the ore's name, or else an error
message stating (in English) what you need to do to correct the INI file.

It will always create the XML file in the folder you are currently in, and
it will name the configuration based on the mod name in the INI file.

## INI Format

The INI file will have at least 3 parts, the mod definition section, the defaults section, and at least one block definition section.  The file is formatted as follows:

```
[Section]
Option Name: Option 1, Option 2, Option 3, ... Final Option
```

### Mod Definition

The `[Mod]` section provides key information for the mod, including its name, XML prefix, Mod ID, and A description of the mod or the configuration.

* The mod name is just that; this is what a player will see in the "Custom Ore Generation" setup screen, both before the ore name, and the mod tab.  Do not use special characters, other than spaces.  Example: `Name: Pams Harvestcraft`
* The mod's prefix is used in the XML.  This ensures that all variables are different to prevent conflicts.  For example, Copper exists in a large number of mods, so any configuration of copper in one mod would conflict with the copper in another mod, unless the configuration variables include something specific to that mod.  The full name (minus spaces) could be used, but shortened versions of the mod name tend to be easier to read in what might already be a long name.  Example: `Prefix: hvst`
* The mod's "detect" name is used in the XML to check and see if a mod is installed.  Otherwise, if you are to remove a mod without removing its Custom Ore Generation configuration, the Custom Ore Generation mod will crash upon starting the game.  Example: `Detect: harvestcraft`
* The description is where you can add custom information into the XML file.  This is a perfect place to add a basic description of the mod, your name and email address (as the configuration designer), and any other information you wish to include.

So, an example using the above three examples would be:

```
[Mod]
Name: Pams HarvestCraft
Prefix: hvst
Detect: harvestcraft
Description: A mod centered around the farming and collection of crops, and the extensive arrays of edible recipes you can make from them.  Oregen is for salt. Configuration by Reteo.
```

### Defaults Section

Some options are shared among all block definition sections.  In this case, there is no reason that the shared options need to be repeated over and over.  That's where the `[DEFAULTS]` section comes in.  It doesn't need to be included, but if you want to set an option that everything will use (such as enabling wireframes, or choosing distribution presets), you simply add those options to this section, and they won't need to be added to other sections.

Keep in mind that this sets defaults.  These defaults can easily be overridden by simply adding an altered form of the option to a specific block section (for example, setting layered veins as a default distribution preset, but configuring a specific ore to use sparse or pipe veins instead).

Example:

```
[DEFAULT]
Wireframe: yes
Bounding Box: no
Distribution presets: Sparse Veins, Cloud, Vanilla
```

### Block Definitions Sections

The block definition sections always start with the distribution's name; for example: `[Salt]`.  This will be shown in the list of blocks in the Custom Ore Generation Setup screen during game setup (in the example's case, as "Pams Harvestcraft Salt").

Following the name are a list of distribution options.  The options will be explained in more detail in the following sections.

For now, however, here's an example of a block definition section, using the Pam's HarvestCraft example we've already used so far:

```
[Salt]
Wireframe Color: 90927C
Bounding Box Color: 90927C
Blocks: harvestcraft:salt
Height: 67, 61, uniform, base
Standard Size: 2.500, 2.500, normal, base
Standard Frequency: 15.000, 15.000, normal, base
Vein Motherlode Frequency: 3.751 * _default_, 3.751 * _default_, normal, base
Vein Motherlode Size: 0 * _default_, 0 * _default_, normal, base
Vein Branch Length: 1.937 * _default_, 1.937 * _default_, normal, base
Vein Segment Radius: 1.392 * _default_, 1.392 * _default_, normal, base
Cloud Frequency: 1.341 * _default_, 1.341 * _default_, normal, base
Cloud Radius: 1.158 * _default_, 1.158 * _default_, normal, base
Cloud Thickness: 1.158 * _default_, 1.158 * _default_, normal, base
```

## Distribution Presets

Before we get into the options, it seems like a good idea to cover the different distribution options available in Sprocket Advanced.

Custom Ore Generation comes with several built-in presets, and Sprocket adds some more complex presets to the table.

### Custom Ore Generation Presets

* **Substitution**: The simplest of the distribution options.  The substitution distribution simply replaces all of one type of block with a block of a second type.  Constraints can be added to limit the changes to specific Y layers in the ground.
* **Vanilla**: Actually, the name of this distribution is "StandardGen", but Sprocket uses "Vanilla" to clarify the function of this distribution.  In essence, this distribution works like the vanilla oregen, sprinkling small veins of ore throughout the Y layers its assigned.
* **Cloud**: The cloud distribution is a large sphere of ore.  This sphere is sparse by default, meaning that all the blocks in the cloud are spread apart, making the process of mining the whole cloud tricky and time-consuming.  The shape of the cloud is configurable, as its vertical and horizontal sizes can be independently changed, and the whole distribution can be tilted.  The cloud distribution also generates hint veins around it (see below).
    * **Strata**: This cloud distribution is a huge thin disc of ore or stone.  It is best used to provide stratafied stone distributions for mods containing their own special stone blocks.  This preset is not available in version &lt;1.2.25 of Custom Ore Generation.
* **Motherlode and Veins**:  Note, unlike the previous options, this is not a preset; this is a class of preset.  The vein distribution is easily the most complex distribution of the group.  The first part of the vein distribution is the *motherlode*, a sphere of ore that functions as the center of the distribution.  The second part is the *vein*, a string of ore which leaves the motherlode, and goes outward in random directions, smoothly twisting and turning on its path, and sometimes splitting into multiple branches.  Key terms to know in the vein distribution are *branches*, which is essentially the entire length of the vein from the point at which it spawned (whether it's at a motherlode, or at a point where another branch split), and *segments*, which are the different curved sections of the vein.
    * **Layered Veins**:  This preset is the basic motherlode-and-veins ore distribution.
    * **Vertical Veins**: This preset is nothing but a branch of ore starting at one location, and travelling downwards by default.  The branch does still split on its way down, however.
    * **Small Deposits**: This preset is nothing but a motherlode.  By default, it can be quite small... about the size of a vanilla vein.
    * **Huge Veins**:  This distribution consists of both motherlode and vein distributions, like the layered veins.  However, the motherlode is enormous by comparison, and the veins are thin, but extremely long.  This is meant to be a strategic option; players have to search for the ore, and once they encounter the vein, they have to follow it back to the motherlode, at which point, they will have ore for a long time to come.
    * **Sparse Veins**:  This preset is nothing but a branch of ore.  The branch is extremely wide, and extremely long.  However, the vein is a sparse one.  Following a sparse vein is tricky, since the player has to keep looking to find the next ore block, rather than just mining as blocks become visible.
    * **Pipe Veins**:  This preset is a two-vein distribution with no motherlode.  The outer vein is a sparse vein, while the smaller inner vein is solid.  This is used to mix valuable ore with a hazard of some kind, such as lava or monster eggs.
    * **Hint Veins**:  This preset is usually not used on its own, instead functioning as a way to alert a player that a strategic deposit is close by.  It sprinkles the area with one-block veins of ore.
    * **Compound Veins**:  This preset is identical to the layered veins distribution, except that it is a distribution containing a distribution, similar to the pipe vein distribution.
    * **Geode**: The geode distribution is identical to the small deposits distribution, except it contains a second distribution, which itself surrounds an air pocket.  In essence, This distribution arranges blocks to simulate actual geodes.
* **Custom Distributions**: The following are distributions to use when you know what you're doing, and you have something specific in mind.  These distributions will not include a preset value.
    * **Custom Veins**: This will produce an un-preset vein distribution.  You can use all vein-related options in this distribution.
    * **Custom Cloud**: This will produce an un-preset cloud distribution.  You can use all cloud-related options in this distribution.
    * **Null**: This will produce only the absolute basic XML configuration; The settings options will all be there, the distribution configuration section will be empty, and all distribution-specific names and values will include the word "NULL".  This is meant to be a blank canvas on which a configuration writer can make their custom-designed XML code without needing to worry about arganizing the main file.

## Option Types

* **List**: A comma-separated list of items.  Can also use regular expressions.
* **Boolean**: A simple "yes" or "no" will suffice.
* **Statistical Variation**: This option consists of four values.
    * The *statistical average*.
    * The *statistical deviation*.
    * Preference, consisting of *one of the following*:
        * **normal** (prefers to stay closer to the average)
        * **inverse** (prefers to stay closer to the deviation)
        * **uniform** (no preference, completely random)
    * *Scaling option* (see COG's documentation for more details), usually defaults to "base".
    
**NOTE**:  in the case of Statistical Variation options, you can refer to the preset's default values by using the `_default_` value.  Make sure this is the word "default" with an underline before and after it.

If you want the negative version of the default value, you can use the negative operator before the value (`-_default_`).  The negative version can be useful in some cases, such as reversing the direction of a vertical vein (`Vein Branch Inclination: -_default_, -_default_, normal, base`), making it go from the bottom up, instead of the top down.
    
## Example Options

### Example List

```
Blocks: minecraft:stone, minecraft:dirt, minecraft:sand
```

### Example Boolean

```
Active: yes
```

### Example Statistical Variation

```
Vein Motherlode Height: 16, 8, normal, base
```
    

## Distribution Meta Options

These options apply, regardless of the preset, and are useful in adding special logic to the XML that apply in specific circumstances.  They also include some universal values that can be applied if not overridden by distribution-specific options.

### Distribution Presets (List)

This is a list of all distributions presets available for this distribution.  (List of available distribution presets are a work in progress)

     Default: Vanilla

### Seed (Value)

The seed value is used to synchronize the random number generator between two or more distributions; this is useful when placing distributions inside other distributions.

     Default: MISSING

### Active (Boolean)

If Active is set to "no," then the default distribution is set to "none."  Otherwise, the default distribution is the first option in the distribution presets list.

     Default: yes
     
### Use Cleanup (Boolean)

If set to "yes," then the configuration will undergo a "cleaning" pass before beginning to generate any block distributions.  This is a computationally-expensive step that can cause a game to lag when generating new chunks.

If set to "no," the cleanup pass is skipped.  However, if the mod does not have oregen disabled in its own configuration, you will end up with both Custom Ore Generation distributions, as well as the mod's own oregen.

This option is not available for "minecraft" (non-modded) configurations.

    Default: yes

### Main Block Cleanup (Boolean)

If set to "yes," then the configuration will first undergo a "cleaning" step, in which all existing blocks in the "Blocks" list will be replaced by the first block in the "Replaces" list.  This removes ores generated by other mods in order to prepare the way for the new generation.

Setting this to "no" is recommended if the mod has configuration options that can disable its own oregen, as this can improve new chunk generation performance.

     Default: yes

### Alternate Block Cleanup (Boolean)

If set to "yes," then the configuration will first undergo a "cleaning" step, in which all existing blocks in the "Alternate Blocks" list will be replaced by the first block in the "Replaces" list.  This removes ores generated by other mods in order to prepare the way for the new generation.

Setting this to "no" is recommended if the mod has configuration options that can disable its own oregen, as this can improve new chunk generation performance.

     Default: no
     
## Shared Options

These options are applied to all distributions that do not have their own configurations.

### Size (Statistical Variation)

This is the size range.

     Default: _default_, _default_, normal, base

### Frequency (Statistical Variation)

This is the frequency range.

     Default: _default_, _default_, normal, base

### Height (Statistical Variation)

This is the Y level range.

     Default: _default_, _default_, normal, base

### Density (Statistical Variation)

This is a Density multiplier; 0 means no blocks, 1 means a solid shape, anything inbetween means that the ores will be spread out.

     Default: _default_, _default_, normal, base

### Height Clamp Range (List)

Two numbers, indicating the minimum and maximum Y level that the distribution will place blocks on.

     Default: MISSING


### Parent Range Limit (Statistical Variation)

This identifies how far away a child distribution can be from the parent.

     Default: _default_, _default_, normal, base
     
## Block Lists

### Blocks (List)

List of block IDs that will be placed in the distribution.  This option *must be supplied*.

     Default: MISSING

### Alternate Blocks (List)

List of block IDs that will be placed in special locations in the distribution.  This option is only useful in complex distributions like pipes (it fills the pipe with the alternate blocks), compound veins, and geodes (both compound vein and geode are surrounded by the alternate blocks in a custom shell).

     Default: minecraft:stone

### Replaces (List)

The blocks that get replaced with the "Blocks" blocks.

     Default: minecraft:stone

### Block Weights (List)

Adjusts the weight values of the blocks in the "Blocks" list.  Must always be the same number of values as the "Blocks" list, and must always total 1 or less.

     Default: MISSING

### Alternate Block Weights (List)

Adjusts the weight values of the blocks in the "Alternate Blocks" list.  Must always be the same number of values as the "Alternate Blocks" list, and must always total 1 or less.

     Default: MISSING

### Replacement Weights (List)

Adjusts the weight values of the blocks in the "Replaces" list.  Must always be the same number of values as the "Alternate Blocks" list.  Unlike the previous two, the numbers do not have any specific total requirements.  However, a value of "1" means that the block is *always* replaced, and a value of "-1" means that the block is *never* replaced.

     Default: MISSING

## Location Options

### Dimensions (List)

List of dimensions for the current distribution.  This list has been heavily expanded, and includes quite a few mods' dimensions.  The current options are:
 
* Overworld
* Nether
* End
* Twilight Forest
* Aether
* Aether Dungeons
* Outer Lands
* Bedrock Dimension (or just "Bedrock")
* Mining World (or just "Mining")
* GalactiCraft Space (or just "Space")
* GalactiCraft Orbit (or just "Orbit")
* GalactiCraft Moon (or just "Moon")
* GalactiCraft Mars (or just "Mars")
* GalactiCraft Asteroids (or just "Asteroids")
* RFTools
* Mystcraft

     Default: Overworld

### Need Biomes (List)

List of biomes; these are the only biomes the distribution will work for.

     Default: .*

### Need Biome Types (List)

List of Forge biome dictionary types; these are the only biome types the distribution will work for.

     Default: MISSING

### Avoid Biomes (List)

List of biomes; these are the biomes the distribution will *not* work for.

     Default: MISSING

### Avoid Biome Types (List)

List of Forge biome dictionary types; these are the biome types the distribution will *not* work for.

     Default: MISSING

### Prefer Biomes (List)

List of biomes; the distribution will add an extra distributions for these biomes.

     Default: MISSING

### Prefer Biome Types (List)

List of Forge biome dictionary types; the distribution will add extra distributions for these biome types.

     Default: MISSING

### Biome Rainfall Range (List)

Two numeric values indicate the minimum and maximum rainfall required for the biome to qualify for the distribution.

     Default: MISSING

### Biome Temperature Range (List)

Two numeric values indicate the minimum and maximum temperature required for the biome to qualify for the distribution.

     Default: MISSING

### Place Below (List)

List of block IDs.  Block will only be placed if it is connected to the bottom surface of one of these blocks.

     Default: MISSING

### Place Beside (List)

List of block IDs.  Block will only be placed if it is connected to the side surface of one of these blocks.

     Default: MISSING

### Place Above (List)

List of block IDs.  Block will only be placed if it is connected to the top surface of one of these blocks.

     Default: MISSING
     
# Substitution Distribution Options

### Substitution Height Clamp Range (List)

Two numbers, indicating the minimum and maximum Y level that the distribution will substitute blocks on.

     Default: MISSING

## Standard Distribution Options

### Standard Size (Statistical Variation)

The vein size.

     Default: MISSING

### Standard Frequency (Statistical Variation)

The number of veins per chunk.

     Default: MISSING

### Standard Height (Statistical Variation)

The range of Y levels the ore spawns at.

     Default: MISSING

### Standard Parent Range Limit (Statistical Variation)

The range from the parent distribution that children distributions spawn.

     Default: MISSING

### Standard Height Clamp Range (List)

Two numbers, indicating the minimum and maximum Y level that the distribution will substitute blocks on.

     Default: MISSING
     
## Cloud Distribution Options

### Cloud Frequency (Statistical Variation)

The number of clouds per chunk.

     Default: MISSING

### Cloud Parent Range Limit (Statistical Variation)

The range from the parent distribution that children distributions spawn.

     Default: MISSING

### Cloud Radius (Statistical Variation)

The horizontal range from the center of the cloud to its edge.

     Default: MISSING

### Cloud Thickness (Statistical Variation)

The vertical range from the center of the cloud to its edge.

     Default: MISSING

### Cloud Noise (Statistical Variation)

How random the blocks spawn in the cloud.  If the value is 0, and the cloud is sparse, then the blocks spawn at regular intervals.

     Default: _default_, _default_, normal, base

### Cloud Height (Statistical Variation)

The range of Y levels the clouds spawn at.

     Default: MISSING

### Cloud Inclination (Statistical Variation)

The vertical angle of the cloud (allows for "slanting" clouds).

     Default: _default_, _default_, normal, base

### Cloud Density (Statistical Variation)

Density multiplier; 0 means no blocks, 1 means a solid sphere, anything inbetween means that the ores will be spread out.

     Default: MISSING

### Cloud Noise Cutoff (Statistical Variation)

TBD

     Default: _default_, _default_, normal, base

### Cloud Radius Multiplier (Statistical Variation)

TBD

     Default: _default_, _default_, normal, base

### Cloud Height Clamp Range (List)

Two numbers, indicating the minimum and maximum Y level that the distribution will substitute blocks on.

     Default: MISSING
     
## Vein Distribution Options

### Vein Motherlode Frequency (Statistical Variation)

The number of motherlodes per chunk.

     Default: MISSING

### Vein Motherlode Range Limit (Statistical Variation)

The range from the parent motherlode that children distributions spawn.

     Default: MISSING

### Vein Motherlode Size (Statistical Variation)

The size of the motherlode's diameter.

     Default: MISSING

### Vein Motherlode Height (Statistical Variation)

The range of Y levels the motherlode spawns at.

     Default: MISSING
     
### Vein Branch Type (List)

A single option describing the type of curves in the branches.  The choices are *Ellipsoid*, in which curves are somewhat circular, and more regular, and *Bezier*, in which the vein's curves are smoother and more complex.

    Default: Bezier

### Vein Branch Frequency (Statistical Variation)

The number of branches per motherlode.

     Default: _default_, _default_, normal, base

### Vein Branch Inclination (Statistical Variation)

Adjusts the vertical angle of branches as they leave the motherlode.

     Default: _default_, _default_, normal, base

### Vein Branch Length (Statistical Variation)

The total length of the branch (and all segments within it) from the motherlode to its farthest tip.

     Default: _default_, _default_, normal, base

### Vein Branch Height Limit (Statistical Variation)

The maximum Y levels the branches can wander away from the motherlode.

     Default: _default_, _default_, normal, base

### Vein Segment Fork Frequency (Statistical Variation)

How likely a given segment will split into two branches.

     Default: _default_, _default_, normal, base

### Vein Segment Fork Length Multiplier (Statistical Variation)

Multiplier to each fork to reduce the total branch length.  Values must be from 0-1.

     Default: _default_, _default_, normal, base

### Vein Segment Length (Statistical Variation)

The length of each segment of the branch.

     Default: _default_, _default_, normal, base

### Vein Segment Angle (Statistical Variation)

The horizontal angle from which a segment diverges from the branch.

     Default: _default_, _default_, normal, base
     
### Vein Segment Pitch (Statistical Variation)

The vertical angle from which a segment diverges from the branch.

     Default: _default_, _default_, normal, base

### Vein Segment Radius (Statistical Variation)

The width of the segments at their thickest point.  In essence, the width of the branch.

     Default: _default_, _default_, normal, base

### Vein Ore Density (Statistical Variation)

Density multiplier; 0 means no blocks, 1 means a solid sphere and solid veins, anything inbetween means that the ores will be spread out.

     Default: MISSING

### Vein Ore Radius Multiplier (Statistical Variation)

TBD

     Default: _default_, _default_, normal, base

### Vein Height Clamp Range (List)

Two numbers, indicating the minimum and maximum Y level that the distribution will substitute blocks on.

     Default: MISSING

## Debugging Options

### Wireframe (Boolean)

When in debugging mode, do you want to see wireframes?

     Default: yes

### Bounding Box (Boolean)

When in debugging mode, do you want to see bounding boxes?

     Default: no

### Wireframe Color (Value)

The color, in web color code, of the wireframes for this distribution.  Sprocket Advanced can handle the hash mark (#), but the XML can't.

     Default: MISSING

### Bounding Box Color (Value)


The color, in web color code, of the bounding box for this distribution.  Sprocket Advanced can handle the hash mark (#), but the XML can't.

     Default: MISSING
     
