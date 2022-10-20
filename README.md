# proceditor

procedual video editing for blender. first time addon developer, expect shitty
code


What follows is a bunch of rambling about how the addon could work


## Dependencies

**only runs on unix like systems**

youtube_dl
ddgimcli
ffmpeg
npm
xclip


## TODO

alert when template is not found
add menu for markup clips
offset markup clips when stacked

metaclip support for modifying templates

ability to freeze compiled clip for manual editing

adjustkeyframes beginning keyframes


## Templates

Templates are metaclips which take parameters that alter their contents. 
To create a template, create a metaclip (ctrl + g with a strip selected) and name it
`template_keyword`

example

```
template_text
```

## Placeholders

Placeholders are clips inside templates that have their contents replaced by the
template parameters. Their naming scheme is `:parameter_index:`. The most
simple example is a text clip with the name `:0:` (Parameters start at 0). This
text clip will take the first parameter passed to the template as the text
content. 

## Markup Clips

Markup clips are text clips which have contents matching a simple markup
language. The markup contains a template name along with some parameters.
Proceditor can replace these with a copy of the specified template and apply
the parameters from the text to the template. 

The syntax for markup clips is
```
;templatename;parameter1;parameter2
```
Example
```
;title;This is the content of a title
```

### template ideas


- twitter
  - syntax: tw
  - parameter 1 is link to tweet

- reddit
  - syntax: re
  - parameter 1 is link to post

- quote
  - syntax: q
  - parameter 1 is name
  - parameter 2 is content

- stinger transition
  - syntax: s

- square hover
  - syntax:h
  - normal hover

- square hmm
  - syntax:hm
  - rotating lots of squares
  - adjustkeyframes

- square angry
  - syntax:hm
  - red square noice modifier
  - adjustkeyframes

- website
  - syntax:w
  - give link, get scrolling screenshot

- music
  - syntax: m
  - give link, download music with youtube-dl, insert

- youtube video
  - give in/out parameter to download specific portion of video

## Placeholder ideas

- color clip
  - parameter is color
  - can be hex code or selection from colorscheme


## mrkp - Non-verbose markup language. Doesn't need autocomplete to be usable

options without separator;semicolon.objecttype:content1::content2::content3

## TODO for the far future

metaclip templates via name
- layout templates
  - everything inside metaclip gets autoarranged
  - things can appear with time offset
  - examples
    - grid
    - splitscreen

telegram sticker template

parameter, template etc markup abbreviations

define custom templates in blend file

multithreaded compilation

## old documentation stuff, please rework

parameter:keyword:number clips get altered by markup

options;yourclipname gets modifiers applied to it
for instance, adjustkeyframes for clips that aren't parameters

parameter:keyword:number


insert image from keyword

