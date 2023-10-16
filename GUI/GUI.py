import pygame
import sys
import multiprocessing

from GUI.constants import *
from deck.card_sprite import CardSprite, Rank, Suit

class GUI:
    def __init__(self, request_queue, response_queue) -> None:
        # Queues for communication with the client
        self.request_queue = request_queue
        self.response_queue = response_queue
        
        # Initialize pygame
        pygame.init()
        self.font = pygame.font.Font(FONT, 36)
        self.font_small = pygame.font.Font(FONT, 20)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Briscola")
        
        # Load the entire spritesheet image
        self.spritesheet = pygame.image.load(CARDS_SPRITESHEET)
        
        # position of the other players on the screen
        self.players_position = [(WIDTH - 140, 400), (WIDTH - 140, 160), (140, 160), (140, 400)]
        
        # game state varaibles
        self.game_state = None
        self.player_bid = False         # True if it's the player's turn to bid
        self.player_select_card = False # True if it's the player's turn to select a card
        self.game_over = False          # True if the game is over
        
        # bid choice variables
        self.bid = None                 # bid rank chosen
        self.suit = None                # bid suit chosen
        # lists for bid choice
        self.bid_choise_list = None     # list of bid choices
        self.suit_choise_list = None    # list of suit choices
        
    
    # Main game loop
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            try:
                self.handle_client_message()
            except multiprocessing.queues.Empty: # If there are no messages fom the client, continue
                self.handle_events()
                
                # Draw the screen
                self.screen.fill(GREEN)
                self.draw(self.screen)
                
                pygame.display.flip()
                clock.tick(FPS)

        pygame.quit()
        sys.exit()
    
    # ==> EVENT HANDLING <==
    # Handle events from the user
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Check for left mouse button click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.bid_choise_list:
                        print("Have to bid")
                        self.handle_bid_choice(mouse_x, mouse_y)
                    elif self.suit_choise_list:
                        self.handle_suit_choice(mouse_x, mouse_y)
                    elif self.player_select_card:
                        self.handle_card_choice(mouse_x, mouse_y)
    
    # Handle messages from the client
    def handle_client_message(self):
        request_type, data = self.request_queue.get(timeout=1)
        self.game_state = data
        if request_type == "game_state":
            pass
        elif request_type == "bid":
            self.player_bid = True
        elif request_type == "play_card":
            self.player_select_card = True
        elif request_type == "game_over":
            self.game_over = True
    
    # Check if the player clicked on a bid rank choice
    def handle_bid_choice(self, x: int, y: int):
        for i, b_view in enumerate(self.bid_choise_list):
            b = b_view[0]
            r = b_view[1]
            if r.collidepoint(x, y):
                self.bid = b # get the bid rank
                self.bid_choise_list = None # remove the bid choice list
                if self.bid == 'PASS': # if the player passed, send the bid directly, otherwise ask for the suit
                    self.send_bid()
    
    # Check if the player clicked on a bid suit choice
    def handle_suit_choice(self, x: int, y: int):
        for i, s_view in enumerate(self.suit_choise_list):
            s = s_view[0]
            r = s_view[1]
            if r.collidepoint(x, y):
                self.suit = s # get the bid suit
                self.suit_choise_list = None # remove the suit choice list
                self.send_bid() # send the bid
    
    # Check if the player clicked on a card
    def handle_card_choice(self, x: int, y: int):
        for i, c in enumerate(self.hand):
            if c.inside(x, y):
                self.send_card(c) # send the card chosen
    
    # ==> DRAWING <==
    # Main draw function
    def draw(self, screen: pygame.Surface):
        if self.game_state is None:
            return
        self.phase = self.game_state['current_phase'] # get the current phase
        
        if "briscola" in self.game_state:
            self.draw_briscola(screen)
        
        self.render_text(screen)
        self.draw_hand(screen)
        if self.phase == 'bidding':
            self.render_bid(screen)
        if self.phase == 'game':
            self.render_play(screen)
        if self.phase == 'end':
            self.render_game_over(screen)
    
    # render the phase text and the players' names
    def render_text(self, screen: pygame.Surface):
        self.players = [ p['name'] for p in self.game_state['players'] ]
        self.player = self.game_state['player']
        self.current_player = self.game_state['current_player'] 
        
        if self.current_player is not None:
            # print phase
            phase_text = self.font.render(self.phase + " phase: " + self.players[self.current_player] + "'s turn", True, WHITE)
            screen.blit(phase_text, (10, 10))
        else:
            # print phase
            p_won = self.player_won()
            if p_won:
                phase_text = self.font.render(self.phase + " phase", True, WHITE)
                screen.blit(phase_text, (10, 10))
                if self.phase == 'bidding':
                    s = self.players[p_won] + " won the bid"
                    self.render_text_center(s, screen)
                elif self.phase == 'game':
                    s = self.players[p_won] + " won the round"
                    self.render_text_center(s, screen)
                
        
        # print players
        for i, p in enumerate(self.players):
            if i == self.player: # user player
                if 'bidder' in self.game_state and self.player == self.game_state['bidder']:
                    text_surface = self.font_small.render("You are the bidder", True, RED)
                    text_rect = text_surface.get_rect()
                    text_rect.bottomleft = (10, HEIGHT - 10)
                    screen.blit(text_surface, text_rect)
                elif ('partner' in self.game_state and self.player == self.game_state['partner']) or self.briscola_in_hand():
                    text_surface = self.font_small.render("You are the partner", True, ORANGE)
                    text_rect = text_surface.get_rect()
                    text_rect.bottomleft = (10, HEIGHT - 10)
                    screen.blit(text_surface, text_rect)
            else: # other players
                if 'bidder' in self.game_state and i == self.game_state['bidder']:
                    text_surface = self.font_small.render(p, True, RED)
                elif 'partner' in self.game_state and i == self.game_state['partner']:
                    text_surface = self.font_small.render(p, True, ORANGE)
                else:
                    text_surface = self.font_small.render(p, True, WHITE)
                index = (i - self.player) % len(self.players) - 1
                text_rect = text_surface.get_rect()
                text_rect.center = self.players_position[index]
                screen.blit(text_surface, text_rect)
    
    # draw the player's hand
    def draw_hand(self, screen: pygame.Surface):
        self.hand = [ self.set_card(c) for c in self.game_state['hand'] ]
        
        w, h = screen.get_size()
        hand_size = len(self.hand)
    
        start = w / 2 - (hand_size / 2) * CARD_WIDTH
        for card in self.hand:
            card.draw(start, h - CARD_HEIGHT, screen)
            start += CARD_WIDTH
    
    # draw the latest bid of each player
    def render_bid(self, screen: pygame.Surface):
        for i, p in enumerate(self.players): # for each player
            if self.player_bid and i == self.player: # if it's the player's turn to bid
                if self.bid is None:
                    self.draw_bid_choise(screen)
                elif self.suit is None:
                    self.draw_suite_choise(screen)
                
            else: # if it's not the player's turn to bid
                bid = self.latest_bid(i) # get the latest bid of the player
                if bid: # if the player has bidden in the past, render the latest bid
                    text_surface = self.font_small.render(bid, True, WHITE)
                    text_rect = text_surface.get_rect()
                    if i == self.player:
                        center = (WIDTH // 2, HEIGHT - CARD_HEIGHT - 50)
                    else:
                        index = (i - self.player) % len(self.players) - 1
                        center = (self.players_position[index][0], self.players_position[index][1] + 50)
                    text_rect.center = center
                    screen.blit(text_surface, text_rect)
    
    # draw the bid rank choices
    def draw_bid_choise(self, screen: pygame.Surface):
        max_bid = self.biggest_bid() # get the biggest bid done so far
        if max_bid is None:
            possible_bids = [r.name for r in Rank] # get all the possible bids
        else:
            max_bid_rank = Rank[max_bid]
            possible_bids = [r.name for r in Rank if r < max_bid_rank] # get the possible bids left
        possible_bids.append('PASS')
        
        # render the possible bids
        length = len(possible_bids) * 90
        start = WIDTH / 2 - length / 2
        center_start = start + 45
        self.bid_choise_list = []
        for i, b in enumerate(possible_bids):
            text_surface = self.font_small.render(b, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (center_start, HEIGHT - CARD_HEIGHT - 50)
            screen.blit(text_surface, text_rect)
            self.bid_choise_list.append([b, text_rect])
            center_start += 90
    
    # draw the suit choices
    def draw_suite_choise(self, screen: pygame.Surface):
        possible_suite = [s.name for s in Suit] # get the possible suits
        
        # render the possible suits
        length = len(possible_suite) * 90
        start = WIDTH / 2 - length / 2
        center_start = start + 45
        self.suit_choise_list = []
        for i, s in enumerate(possible_suite):
            text_surface = self.font_small.render(s, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (center_start, HEIGHT - CARD_HEIGHT - 50)
            screen.blit(text_surface, text_rect)
            self.suit_choise_list.append([s, text_rect])
            center_start += 90
            
    # draw the cards played in the current round
    def render_play(self, screen: pygame.Surface):
        round_num = str(self.game_state['current_round'])
        round = self.game_state["rounds"][round_num]
        for i, p in enumerate(self.players): # for each player
            if self.player_select_card and i == self.player: # if it's the player's turn to play
                text_surface = self.font_small.render("Select a card", True, WHITE)
                text_rect = text_surface.get_rect()
                text_rect.center = (WIDTH // 2, HEIGHT - CARD_HEIGHT - 50)
                screen.blit(text_surface, text_rect)
            else:
                played_card = round[str(i)]
                if played_card["played"]:
                    card = self.set_card(played_card)
                    if i == self.player:
                        card.draw(WIDTH // 2 - CARD_WIDTH // 2, HEIGHT - 2 * CARD_HEIGHT - 50, screen)
                    else:
                        index = (i - self.player) % len(self.players) - 1
                        card.draw(self.players_position[index][0] - CARD_WIDTH // 2, self.players_position[index][1] + 30, screen)
    
    # draw the briscola card
    def draw_briscola(self, screen: pygame.Surface):
        b = self.game_state['bidder']
        bidder_text = self.font_small.render("Bidder: " + self.players[b], True, WHITE)
        bidder_rect = bidder_text.get_rect()
        bidder_rect.topright = (WIDTH - 10, 5)
        screen.blit(bidder_text, bidder_rect)
        
        briscola_text = self.font_small.render("Briscola:", True, WHITE)
        briscola_rect = briscola_text.get_rect()
        briscola_rect.topright = (int(WIDTH - CARD_WIDTH / 1.5 - 20), 40)
        screen.blit(briscola_text, briscola_rect)
        
        briscola = self.set_card(self.game_state['briscola'], int(CARD_WIDTH / 1.5), int(CARD_HEIGHT / 1.5))
        briscola.draw(int(WIDTH - CARD_WIDTH / 1.5 - 10), 40, screen)
    
    # draw the game over screen
    def render_game_over(self, screen: pygame.Surface):
        # points for each player
        for i, p in enumerate(self.players):
            points = self.game_state['points'][str(i)]
            if i != self.game_state['bidder'] and i != self.game_state['partner']:
                color = WHITE
            elif i == self.game_state['bidder']:
                color = RED
            elif i == self.game_state['partner']:
                color = ORANGE
            points_surface = self.font.render(str(points), True, color)
            points_rect = points_surface.get_rect()
            if i == self.player:
                points_rect.center = (WIDTH // 2, HEIGHT - CARD_HEIGHT - 50)
            else:
                pos = self.players_position[(i - self.player) % len(self.players) - 1]
                points_rect.center = (pos[0], pos[1] + 50)
            screen.blit(points_surface, points_rect)
        
        # winner text
        if self.game_state['winner'] is None: # it's a TIE
            s = "It's a TIE!"
        else: # there is a winner
            s = "The team composed of\n"
            for i in self.game_state['winner']:
                s += self.players[i] + "\n"
            s += "won the game!"
            
        self.render_text_center(s, screen)
    
    def render_text_center(self, text: str, screen: pygame.Surface):
        lines = text.split('\n')
        
        start = HEIGHT // 2 - len(lines) * 40 // 2 - 20
        for line in lines:
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (WIDTH // 2, start)
            screen.blit(text_surface, text_rect)
            start += 40
    
    # ==> SENDING MESSAGES TO THE CLIENT <==
    # send the bid chosen to the client
    def send_bid(self):
        self.player_bid = False # the player has bidden
        if self.bid == 'PASS':
            data = {
                "pass": True
            }
        else:
            data = {
                "pass": False,
                "card": {
                    "rank": self.bid,
                    "suit": self.suit
                }
            }
        self.response_queue.put(data)
        # reset bid variables
        self.bid = None
        self.suit = None
        
    # send the card chosen to the client
    def send_card(self, card: CardSprite):
        self.player_select_card = False # the player has chosen a card
        data = {
            "card": card.get_card_state()
        }
        self.response_queue.put(data)
        # remove the card from the player's hand
        self.hand.remove(card)
    
    # ==> HELPER FUNCTIONS <==
    def set_card(self, c: dict, c_width: int = CARD_WIDTH, c_height: int = CARD_HEIGHT):
        return CardSprite(Rank[c['rank']], Suit[c['suit']], c_width, c_height, self.spritesheet)
    
    def latest_bid(self, index: int):
        for item in reversed(self.game_state['bid_history']):
            if item['player'] == index:
                return item['bid']
        return None

    def biggest_bid(self):
        for item in reversed(self.game_state['bid_history']):
            if item['bid'] != 'PASS':
                return item['bid']
        return None
    
    def player_won(self):
        if self.phase == 'bidding':
            for item in reversed(self.game_state['bid_history']):
                if item['bid'] != 'PASS':
                    return item['player']
        elif self.phase == 'game':
            curr_round = self.game_state['current_round']
            winner = self.game_state['rounds'][str(curr_round)]['winner']
            return winner
        
        return None
    
    def briscola_in_hand(self):
        if 'briscola' in self.game_state:
            for c in self.hand:
                if c.rank == self.game_state['briscola']['rank'] and c.suit == self.game_state['briscola']['suit']:
                    return True
        return False