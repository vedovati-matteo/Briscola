import pygame
import sys

from deck.card_sprite import CardSprite, Rank, Suit

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
CARD_WIDTH = 100
CARD_HEIGHT = int(CARD_WIDTH * 1.5)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (27,94,32)
FPS = 10

font = pygame.font.Font("fonts/Monda-Bold.ttf", 36)
fontSmall = pygame.font.Font("fonts/Monda-Bold.ttf", 20) 

def draw_hand(hand: list, screen: pygame.Surface):
    w, h = screen.get_size()
    hand_size = len(hand)
    
    start = w / 2 - (hand_size / 2) * CARD_WIDTH
    for card in hand:
        card.draw(start, h - CARD_HEIGHT, screen)
        start += CARD_WIDTH
    
def onclick_hand_card(card: CardSprite):
    print(str(card) + " clicked")

def render_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    
    for i, p in enumerate(player_position):
        text_surface = fontSmall.render("str(adsdasdsaadasdai)", True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = p
        screen.blit(text_surface, text_rect)
    

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game")

# Load the entire spritesheet image
spritesheet = pygame.image.load("img/napoletane.bmp")

# Create a card
card1 = CardSprite(Rank["KNAVE"], Suit.CUPS, CARD_WIDTH, CARD_HEIGHT, spritesheet)
card2 = CardSprite(Rank.TWO, Suit.SWORDS, CARD_WIDTH, CARD_HEIGHT, spritesheet)
card3 = CardSprite(Rank.ACE, Suit.CLUBS, CARD_WIDTH, CARD_HEIGHT, spritesheet)
card4 = CardSprite(Rank.SEVEN, Suit.COINS, CARD_WIDTH, CARD_HEIGHT, spritesheet)
card5 = CardSprite(Rank.FOUR, Suit.CUPS, CARD_WIDTH, CARD_HEIGHT, spritesheet)

hand = [card1, card2, card3, card4, card5]
player_position = [(WIDTH - 140, 400), (WIDTH - 140, 150), (140, 150), (140, 400)]
# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check for left mouse button click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse clicked at", mouse_x, mouse_y)
                for card in hand:
                    if card.inside(mouse_x, mouse_y):
                        onclick_hand_card(card)
                        
    
    # Clear the screen
    screen.fill(GREEN)

    draw_hand(hand, screen)
    render_text("Card Game", 10, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

