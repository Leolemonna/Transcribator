import pygame

SPECIAL_CHATACTERS = (pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_SPACE)

VERSION = "v0.4b"

class Screen:
    def __init__(self, size: list, caption = "Transcribator " + VERSION, fill = (250,250,250)):
        pygame.init()
        self.display = pygame.display
        self.screen = self.display.set_mode(size)
        self.display.set_caption(caption)
        self.fill = fill
        self.screen.fill(fill)
        
        self.clock = pygame.time.Clock()

class Text:
    """This is a class for writing text in the pygame window"""
    def __init__(self, screen: Screen, text, **kwargs) -> None:
        self.text = text
        self.screen = screen
        
        self.pos         = kwargs["position"]
        self.font        = kwargs["font"]
        self.font_colour = kwargs["font_colour"]
        self.font_size   = kwargs["font_size"]
        self.bg_colour  = kwargs["bg_colour"]
        
        self.surface_font = pygame.font.Font(self.font, self.font_size)
        
        self.img = self.surface_font.render(self.text, True, self.font_colour)
    
    def displayText(self):
        self.img = self.surface_font.render(self.text, True, self.font_colour)
        self.screen.screen.blit(self.img, (self.pos[0], self.pos[1]))
        if self.bg_colour == None:
            pass
        else:
            pass # Ill do rect later

class InputField (Text):
    def __init__(self, screen: Screen, **kwargs):
        self.screen = screen
        
        self.text = ''
        self.active = False
        
        self.pos         = kwargs["position"]
        self.font        = kwargs["font"]
        self.font_colour = kwargs["font_colour"]
        self.font_size   = kwargs["font_size"]
        self.bg_colour_active  = kwargs["bg_colour1"]
        self.bg_colour_passive = kwargs["bg_colour2"]
        self.offset      = kwargs["offset"]
        self.border      = kwargs["border"]
        self.min_width   = kwargs["min_width"]
        self.extra_width = kwargs["extra_width"]

        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, self.font_size+self.offset)

        super().__init__(self.screen,self.text, position = (self.rect.x+self.offset, self.rect.y+self.offset),font = self.font, font_size = self.font_size, font_colour = (0, 0, 0), bg_colour = None)
        
        self.display_input()

    def display_input(self):
        if self.active:
            pygame.draw.rect(self.screen.screen, self.bg_colour_active, self.rect, self.border)
        else:
            pygame.draw.rect(self.screen.screen, self.bg_colour_passive, self.rect, self.border)
            
        self.displayText()
        self.rect.w = max(self.min_width, self.img.get_width()+self.extra_width)

    def check_input(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.active = True
            else:
                self.active = False
            
        elif self.active:
            if event.type == pygame.KEYDOWN or event.type == pygame.TEXTINPUT:
                try:
                    if event.key in SPECIAL_CHATACTERS:
                        for special_char in SPECIAL_CHATACTERS:
                            if event.key == special_char and special_char == pygame.K_BACKSPACE:
                                self.text = self.text[:-1]
                            elif event.key == special_char and special_char == pygame.K_RETURN:
                                self.active = False
                            elif event.key == special_char and special_char == pygame.K_SPACE:
                                pass
                except:
                    self.text += event.text

class Button (Text):   
    def __init__(self, screen: Screen, text = 'Submit', rect_padding: bool = False, **kwargs):
        self.screen = screen

        #   states:
        #   0 - inactive
        #   1 - mouse on the button
        #   2 - mouse down on the button
        #   3 - mouse up after down on the button
        
        self.text = text
        self.state = 0
        self.rect_padding_bool = rect_padding
        
        self.pos         = kwargs["position"]
        self.font        = kwargs["font"]
        self.font_colour = kwargs["font_colour"]
        self.font_size   = kwargs["font_size"]
        self.bg_colours  = kwargs["bg_colours"]
        self.offset      = kwargs["offset"]
        self.border      = kwargs["border"]
        self.width       = kwargs["width"]
        self.extra_width = kwargs["extra_width"]
        self.extra_Rectboder = kwargs["extra_Rectborder"]

        if self.rect_padding_bool:
            self.rect_padding = pygame.Rect(self.pos[0], self.pos[1], self.width, self.font_size)
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.font_size)

        super().__init__(self.screen,self.text, position = (self.rect.x+self.offset, self.rect.y+self.offset),font = self.font, font_size = self.font_size, font_colour = (0, 0, 0), bg_colour = None)
        
    def display(self):
        self.rect.w = max(self.width, self.img.get_width()+self.extra_width)
        
        pygame.draw.rect(self.screen.screen, self.bg_colours[self.state], self.rect, self.border)
        if self.rect_padding_bool:
            self.rect_padding.w = max(self.width, self.img.get_width()+self.extra_width)
            # if self.state == 0: I used to do it this way but it seems to look better with static colour for the frame
            pygame.draw.rect(self.screen.screen, self.bg_colours[4], self.rect_padding, self.extra_Rectboder)
            # else:
                # pygame.draw.rect(self.screen.screen, self.bg_colours[self.state-1], self.rect_padding, self.extra_Rectboder)
        self.displayText()
    
    def check_ready(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos[0], event.pos[1]) and self.state != 3:
                if self.state == 0:
                    self.state = 1
            elif self.state != 3:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos[0], event.pos[1]):
            if self.state != 3:
                self.state = 2
            else:
                self.state = 1
        elif self.state == 2:
            if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.state = 3
                
class FileButton(Button):
    def __init__(self, screen: Screen, text, line_len: int, rect_padding: bool = False, line_colour: tuple = (140,140,140),**kwargs):
        super().__init__(screen, text, rect_padding, **kwargs)
        
        self.line_len = line_len
        self.line_colour = line_colour
        self.selected = False
    
    def display(self):
        super().display()
        pygame.draw.line(self.screen.screen, self.line_colour, (self.rect.x-3, self.rect.y+self.rect.h//2), (self.rect.x-self.line_len-3, self.rect.y+self.rect.h//2))
        
    def check_ready(self, event: pygame.event.Event):
        super().check_ready(event)
        
        if self.state == 3 and not self.selected:
            self.selected = True
            self.target_index = len(self.text)
            self.text += " - selected"
        
        elif self.state != 3 and self.selected == True:
            self.selected = False
            self.text = self.text[:self.target_index]
    
    def find_extension(self):        
        tmp = 0
        self.extension = ''
        
        for index in range(len(self.text)):
            char = self.text[index]
            
            if (char != " " or char != '.') and tmp == 0:
                continue
            elif char == '.':
                tmp = 1
                continue
            elif char != '.' and tmp == 1 and char != ' ':
                self.extension += char
                continue
            elif char == ' ' and tmp != 0:
                break