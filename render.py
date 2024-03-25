import pygame

SPECIAL_CHATACTERS = (pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_SPACE)

VERSION = "v0.2a"


class Screen:
    def __init__(self, size: list, caption = "Trinscribe for mama " + VERSION, fill = (250,250,250)):
        pygame.init()
        self.display = pygame.display
        self.screen = self.display.set_mode(size)
        self.display.set_caption(caption)
        self.fill = fill
        self.screen.fill(fill)
        
        self.clock = pygame.time.Clock()


class InputField:
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

        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, self.font_size)

        self.surface_font = pygame.font.Font(self.font,self.font_size)
        self.display_input()
        self.rect.w = max(self.min_width, self.img.get_width())  # starting width ONLY

    def display_input(self):
        self._draw_text()
        if self.active:
            pygame.draw.rect(self.screen.screen, self.bg_colour_active, self.rect, self.border)
        else:
            pygame.draw.rect(self.screen.screen, self.bg_colour_passive, self.rect, self.border)
        self.rect.w = max(self.min_width, self.img.get_width()+self.extra_width)

    def _draw_text(self):
        self.img = self.surface_font.render(self.text, True, self.font_colour)
        self.screen.screen.blit(self.img, (self.rect.x+self.offset, self.rect.y+self.offset))

    def check_input(self, event):
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


class Button:   
    def __init__(self, screen: Screen, text = 'Submit',rect_padding: bool = False, **kwargs):
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
            self.rect_padding = pygame.Rect(self.pos[0]-1, self.pos[1]-1, self.width, self.font_size)
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.font_size)

        self.surface_font = pygame.font.Font(self.font,self.font_size)
        
    def display(self):
        pygame.draw.rect(self.screen.screen, self.bg_colours[self.state], self.rect, self.border)
        self._draw_text()
        self.rect.w = max(self.width, self.img.get_width()+self.extra_width)
    
    def _draw_text(self):
        self.img = self.surface_font.render(self.text, True, self.font_colour)
        self.screen.screen.blit(self.img, (self.rect.x+self.offset, self.rect.y+self.offset))
    
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