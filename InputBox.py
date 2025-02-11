#-*- coding: UTF-8 -*-
import pygame
from pygame import*

inactive_color = (147, 173, 172)
active_color = (205, 247, 245)
font = pygame.font.Font(None, 32)

class InputBox:
    """
    Classe to build an input box
    ...
    Attributes
    ----------
    rect : pygame rect object
    color : tuple
    text : str
    txt_surface : Surface
    active : bool
    message : str

    Methods
    -------
    handle_event():
        checks if the input bar is hoovered, clicked or if the user presses a key on its keyboard
    update():
        udpates the inputbox with the user input
    draw():
        displays the inputbox on the pygame window
    """
    def __init__(self, text=''):
        """
        Constructs all the necessary attributes for the inputbox object
        :param text: str
        """
        self.rect = pygame.Rect(180, 660, 400, 70)
        self.color = inactive_color
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.message = ''

    def handle_event(self, event, window):
        """
        checks if the input bar is hoovered, clicked or if the user presses a key on its keyboard
        :param event: key
        :param window: object
        :return: self.message
        :rtype: str
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = active_color if self.active else inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.message = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)
        return self.message

    def update(self):
        """
        udpates the inputbox with the user input
        :return: None
        """
        # Resize the box if the text is too long.
        width = max(400, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, window):
        """
        displays the inputbox on the pygame window
        :param window:
        :return: None
        """
        # Blit the text.
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, 2, border_radius=6)