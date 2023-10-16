from deck.card import Card, Rank, Suit

import pygame

class CardSprite(Card):
    def __init__(self, rank: Rank, suit: Suit, WIDTH: int, HEIGHT: int, spritesheet: pygame.Surface):
        super().__init__(rank, suit)
        # Define the card section rectangle
        spritesheet_width, spritesheet_height = spritesheet.get_size()
        card_section_width = spritesheet_width / 13
        card_section_height = spritesheet_height / 5
        card_section_rect = pygame.Rect(card_section_width * rank.value[2], card_section_height * suit.value[1], card_section_width, card_section_height)
        # Create a card by extracting the card section
        self.image = spritesheet.subsurface(card_section_rect)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        
        self.rect = self.image.get_rect()
    
    def draw(self, x: int, y: int, screen: pygame.Surface):
        w, h = screen.get_size()
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)
        
    def inside(self, x: int, y: int):
        return self.rect.collidepoint(x, y)