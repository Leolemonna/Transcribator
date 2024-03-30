# Transcibator openai-based
This app is developed to transcribe audio files <span style="color:red">**under 25 MB**</span>
## Getting Started
### Requirements:

If you try running main.py you will need pygame, pyperclip and keyboard installed. You dont need to install anything to run main.exe.

### How to use

1. Run main.exe file _or_ python file main.py.
2. Type in audio file name **with** extension _e.g.: very_important_audio<span style="color:yellow">.mp3</span>_.
Make sure that the audio file is in the **same folder** as the main.py. Press d
3. Type in the name of the result text file with audio transcribed.
4. Type in a valid api key.
5. Press **all** Submit buttons and Transcribe button. (Order doesn't matter)
6. The main ui will freeze as long as it is transcribing but you can still see the feedback of the application through the console window. 😄

#### <br/>Extra
> [!IMPORTANT] 
> If you want to switch api keys during usage you can write the new one (or use ctrl+v) **and** preset reset api key because if you don't it will use the previously submitted one.

## Ideas for the new versions
* multi-thread transcribition and ui rendering, it would hopefully solve the ui window freeze since the one thread will be waiting on the response from the server openai and other render the window. <- im working on this right now.
* make the ui just visually pleasing <- that's a hard one. 😄
* loading of the multiple files in the sequence so that itll be easier to use if you need to do multiple files at once.
* show what audio file are the in the folder and to be able to select them in sideview.
* add optional separation of the resulted trascript into different peoples' phrases. Basically speaking, if the resulting text is a dialogue, you could slice it into pieces of phrases according to the people who speak.

## Contributing
Idk yet about that

## License
This software is licensed under [MIT License](https://opensource.org/licenses/MIT)
