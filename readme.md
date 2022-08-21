# worldReader

I was interested to try my hand at decoding the data contained in minecraft region files, so I took a crack at it and came up with this in about 4-6 hours. I'm sort of disappointed with how long it took considering I was 99% of the way there for about 2-3 hours, my brain was just too much so in 1am mode to realize I was reading the contents of long array's as floating points values instead of longs. I'm pretty sure I would have caught that a little easier if I just let myself rest and come back to it tomorrow 😅, instead I let my tired brain waste some time haha.

Here are a list of the websites I used to aid in the creation of this:

- https://hexed.it/ - Served as a very capable browser based binary file viewer.
- https://minecraft.fandom.com/wiki/Region_file_format - Describes the structure of region files.
- https://minecraft.fandom.com/wiki/NBT_format - Describes the structure of the nbt data within region files.

This repo demonstrates reading the nbt data out of a region file without any extra help of any non-standard dependencies. This should work on any fresh full installation of python 3.10+ without any additional setup.

I wrote this putting time efficiency over everything (I was set on finishing this tonight), so if I where to spend more time on this (which I may do in the future) there are a few structural changes I'd make.

Overall though, I was surprised how easy this was. If it weren't for my one trip up, this would have taken me nearly half the time. The whole codebase behind this is only 171 lines long. The majority of my time was spent on sleepy ineffective debugging and researching the structure of region files.