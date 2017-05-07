# Trait
A little application to easily translate and learn English words for Lithuanians students.

This application lets people easily translate bulks of English words to Lithuanian and to learn them quickly.

**The prime usage of this application is directed towards Lithuanian schools and their system of learning English.**

**Usage is limited to 1000 words/day by MyMemory api.**

_Often times, many English words are given for students to learn. These words are then accounted by randomly asking ~20% of the words. Students are graded by how many words they managed to translate. While I did primarily call this app a Translator, it is more of a helper for students to learn these large amounts of words._

## Usage:

Usage is simple:
1. Press the "Input" button and paste in the words you need to learn.
2. Translate the words by pressing the "Translate" button.
3. Check the translations
    * Pressing the "Next" button will give you another translation (If it exists).
    * Words can easily be changed and Re-Translated by marking the checkbox near them and pressing "Translate".
    * You can change the translation yourself and it will be added to the valid translations.
    * Don't forget to save or all progress will be lost.
    * **TIP** You can navigate the input fields easily with TAB on your keyboard.
4. Exit the translation view. You can review the words by pressing the "Show" button.
5. Press the "Learn" button when you are ready to learn:
    * You will be given a word. You have to type in the translation without mistakes. Capitalization does not matter, special charcaters are not acounted for.
    * Once you've written your word, you can either press "Check" or ENTER on your keyboard. The word will change color to red if it's wrong or green if it is right.
    * If the word is right it will automatically give you another one in 2 seconds.
    * You can check the spelling of a word by pressing "Show".
    * You can click "Next" at any time to get another word.

## Compiling

I've included the .spec files. You can compile this project by using pyinstaller.
In the project folder do:

`pip install kivy`  
`pip install pyinstaller`  
_If your are not running from project folder: Open Trait.spec or Trait_single.spec and input project location in pathex_
`pyinstaller Trait.spec` or `pyinstaller Trait_single.spec`  
_The single spec compiles to a onefile executable. There are some speed and memory drawbacks to this (For instance, translated words are saved only for one session)_  

**And that should be it. If any issues occur, feel free to contact me**

## Downloads

**Coming soon**