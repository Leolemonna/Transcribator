print("Importing libraries ... ")
print("- □□□□□□□ -")
from openai import OpenAI
print("- +□□□□□□ -")
import pygame
print("- ++□□□□□ -")
import render
print("- +++□□□□ -")
import keyboard as kboard
print("- ++++□□□ -")
import pyperclip as pyclip
print("- +++++□□ -")
import concurrent.futures
print("- ++++++□ -")
import pathlib
print("- +++++++ -")
import os
print("Done importing ✓")

#variables init
BUTTON_COLOURS = ((210, 210, 210), (180, 180, 180), (120, 230, 120), (100, 255, 100), (0, 0, 0))       # the last one is the extra color for padding
FILE_BUTTONS_COLOURS = ((235, 235, 235), (220, 230, 225), (120, 230, 120), (100, 255, 100), (120, 120, 120))  # the last one is the extra color for padding
INFIELDS_COLOURS = ((100,100,100), (150,230,150))
SUPPORTED_EXTENSIONS = (".mp3", ".m4a", ".wav", ".mp4", ".mpeg")
ICON = pygame.image.load("icon.png")
SIDEVIEW_POSX: int = 620
TEXT_OFFSETX: int = 12
FILE_BUTTONSX = SIDEVIEW_POSX+TEXT_OFFSETX
SUBMIT_BUTTON_X = 460
SUBMIT_BUTTON_SEPARATION = 30
file_buttons_parameteres = dict(rect_padding=True, font = None, font_colour = (250, 250, 250), font_size = 22, bg_colours = FILE_BUTTONS_COLOURS,
                                      offset = 4, border = 0, width = 30, extra_width = 8, extra_Rectborder = 1)
file_buttons_separator_size: int = 23
current_api_key = None
running = True
openai_inisialised = False

clipboard_text = ''

name_of_the_audios = []
buttons = []
file_buttons = []
file_buttons_selected: list[bool] = []
file_buttons_audio_index: list[int] = []
finished_transcribing_thread = True
files = [f for f in os.listdir() if os.path.isfile(f)]
#variables init end

class extension: 
    def find(text: str):
        name_without_extension = pathlib.Path(text).stem
        extension = pathlib.Path(text).suffix
        
        return [extension, name_without_extension]
    
    def change_extension(self, text: str, new_extension: str):
        '''new_extension must start with a dot'''
        res_text = self.find(text)[1]+new_extension
        
        return res_text


def check_all_buttons_ready(except_buttons: list):
    new_buttons_ready = []
    for index in range(len(buttons_ready)):
        if index in except_buttons:
            continue
        else:
            new_buttons_ready.append(buttons_ready[index])
    
    if all(new_buttons_ready):
        return True
    else:
        return False        

def transcribe():
    def _inner_transcribe(audio_name: str):
        if not openai_inisialised:
            #OpenAI inisialisation
            try:
                print("OpenAI inisialisation")
                client = OpenAI(api_key=current_api_key)
                print("Inisialised succesfuly ✓")
            except:
                print("Client failed to load try running the code again, if the error will remain to pop up, ask Leo to fix the key to the openai ")
                return None
        #Audio file loading with the name of name_of_the_audio
        try:
            audio_file = open(audio_name, "rb")
            print("Audio file loaded succesfuly ✓")
        except FileNotFoundError:
            print("Aduio file wasnt found, there is no file in the folder ")
            return None
        except:
            print("Unknown error while loading file, it was found though :) Just try running the code again ")
            return None
        
        try:
            print("Transcibing...")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            print("Transcribing succesfuly ✓")
        except:
            print("Transcribing failed, check internet avialability or run the code again, possibly the format of your audio is not supported\nIt is advised to use mp3,mp4,mpeg and wav")
            return None
            

        print(transcription)

        text_file = open(extension.change_extension(extension, audio_name, '.txt'),'w')
        text_file.write(transcription.text)
        text_file.close()

        audio_file.close()
        
    target_audio_names = []
    
    for audio_name in name_of_the_audios:
        if audio_name is None:
            continue
        else:
            extension_res = extension.find(audio_name)
            print(extension_res)
            if extension_res[0] in SUPPORTED_EXTENSIONS:
                target_audio_names.append(audio_name)
    if len(target_audio_names) == 0:
        print("nothing to transcribe, all of the files are not supported or no files are selected")
        return -1
    else: 
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(target_audio_names)) as executor:
            executor.map(_inner_transcribe, target_audio_names)

def update_file_menu():
    file_buttons.clear()
    
    file_button_pos = [FILE_BUTTONSX, 5]
    files = [f for f in os.listdir() if os.path.isfile(f)]
    
    for file in files:
        file_button_pos[1] += file_buttons_separator_size
        file_buttons.append(render.FileButton(main_screen, file, 4, position = file_button_pos, **file_buttons_parameteres))
    
    file_buttons_selected = [False for _ in file_buttons]

#Inisialisations of the input fields and buttons and file renderers
main_screen = render.Screen((870, 500), fill = (255, 255, 255))
main_screen.display.set_icon(ICON)
separator_line = pygame.draw.line

api_key_infield = render.InputField(main_screen, position = (10, 33), font = None, font_colour = (0, 0, 0), font_size = 18, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
                                      offset = 5, border = 3, min_width = 50, extra_width = 10)

buttons.append(render.Button(main_screen, position = (SUBMIT_BUTTON_X, 10), rect_padding=True, text='Submit audio name',font = None, font_colour = (0, 0, 0), font_size = 22, bg_colours = BUTTON_COLOURS,      #button 0
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 1))

buttons.append(render.Button(main_screen, position = (SUBMIT_BUTTON_X, SUBMIT_BUTTON_SEPARATION+10), rect_padding=True, text='Submit api_key', font = None, font_colour = (0, 0, 0), font_size = 22, bg_colours = BUTTON_COLOURS, 
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 1))

buttons.append(render.Button(main_screen, position = (255, 400), rect_padding=True, text='Transcribe', font = None, font_colour = (250, 250, 250), font_size = 24, bg_colours = BUTTON_COLOURS,     #button 2
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 1))

buttons.append(render.Button(main_screen, position = (SUBMIT_BUTTON_X, SUBMIT_BUTTON_SEPARATION*2+10), rect_padding=True, text='Reset api_key', font = None, font_colour = (250, 250, 250), font_size = 22, bg_colours = BUTTON_COLOURS,  #button 3
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 1))

refresh_button = render.Button(main_screen, position = (SUBMIT_BUTTON_X, SUBMIT_BUTTON_SEPARATION*3+10), rect_padding=True, text='Refresh file menu', font = None, font_colour = (250, 250, 250), font_size = 22, bg_colours = BUTTON_COLOURS,
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 1)

update_file_menu()

file_text_title = render.Text(main_screen, "Files in your folder: ", position = (SIDEVIEW_POSX+TEXT_OFFSETX, 5), font = None, font_colour = (0,0,0), font_size = 24, bg_colour = None)
api_text_title = render.Text(main_screen, "Your API key: ", position = (TEXT_OFFSETX, 5), font = None, font_colour = (0,0,0), font_size = 24, bg_colour = None)

buttons_ready = [False for _ in buttons]
file_buttons_selected = [False for _ in file_buttons]
name_of_the_audios = [None for _ in file_buttons]

while running:
    main_screen.screen.fill(main_screen.fill)
    number_of_file_buttons = len(file_buttons)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_ready(event)
        for index in range(number_of_file_buttons):
            file_button = file_buttons[index]
            file_button.check_ready(event)
        api_key_infield.check_input(event)
        refresh_button.check_ready(event)
    #file buttons handling audio naming
    for index in range(number_of_file_buttons):
        file_button = file_buttons[index]
        if file_button.selected and not file_buttons_selected[index]:
            file_buttons_selected[index] = True
            name_of_the_audios[index] = file_button.text[:file_button.target_index]
        elif not file_button.selected and file_buttons_selected[index]:
            file_buttons_selected[index] = False
            name_of_the_audios[index] = None
    #keyboard sequences handling
    if kboard.is_pressed('ctrl+v'):
        clipboard_text = pyclip.paste()
        if clipboard_text is not None and api_key_infield.active:
            api_key_infield.text = clipboard_text
    if kboard.is_pressed('ctrl+d'):
        if api_key_infield.active: api_key_infield.text=''
    #displaying all the buttons
    for button in buttons:
        button.display()
    for file_button in file_buttons:
        file_button.display()
    
    refresh_button.display()
    file_text_title.displayText()
    api_text_title.displayText()
    separator_line(main_screen.screen, (0, 0, 0), pygame.math.Vector2(SIDEVIEW_POSX, 0), pygame.math.Vector2(SIDEVIEW_POSX, main_screen.screen.get_height()), width=2)
    api_key_infield.display_input()
    
    
    pygame.display.flip()

    main_screen.clock.tick(60)  # limits FPS to 120
    
    for index in range(len(buttons)):
        if buttons[index].state == 3:
            buttons_ready[index] = True
            #for button 0 the the audio file name will be saved
            if index == 1:
                current_api_key = api_key_infield.text
            elif index == 3:
                openai_inisialised = False
        else:
            #   if the buttons are ready then the buttons ready bool will be assigned true respectfully to their index in buttons list
            #   if the buttons arent ready then the bool will be false
            buttons_ready[index] = False
    
    if refresh_button.state == 3:
        update_file_menu()
        refresh_button.state = 1
    
    if check_all_buttons_ready(except_buttons=[3]):
        
        transcribe()
        
        for button in buttons:
            button.state = 0

pygame.quit()
exit()
# exit





# ----  WASTE ----
# waste that I dont want to delete cause I might need it later:
# input_fields.append(render.InputField(main_screen, position = (10, 10), font = None, font_colour = (0, 0, 0), font_size = 22, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
#                                       offset = 5, border = 3, min_width = 50, extra_width = 10))
# input_fields.append(render.InputField(main_screen, position = (10, 40), font = None, font_colour = (0, 0, 0), font_size = 22, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
#                                       offset = 5, border = 3, min_width = 50, extra_width = 10))

#input_fields = []
#for field in input_fields:
#   field.display_input()
# if kboard.is_pressed('ctrl+v'):
#         clipboard_text = pyclip.paste()
#         if clipboard_text is not None:
#             for field in input_fields:
#                 if field.active:
#                     field.text = clipboard_text
# checking if the buttons are ready or not:
    