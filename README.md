# proceditor
procedual video editing for blender. first time addon developer, expect shitty code


What follows is a bunch of rambling about how the addon could work

## TODO

alert when template is not found
add menu for markup clips
offset markup clips when stacked

metaclip support for modifying templates

ability to freeze compiled clip for manual editing

adjustkeyframes beginning keyframes

### clip naming scheme

template:keyword

template is a metaclip
parameter:keyword:number clips get altered by markup

options;yourclipname gets modifiers applied to it
for instance, adjustkeyframes for clips that aren't parameters

parameter:keyword:number


insert image from keyword

### templates

- color
  - syntax: c
  - parameter 1 is color
  - can be hex code or selection from colorscheme

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
