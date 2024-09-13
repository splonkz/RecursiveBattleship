import random
import pygame

# Define constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = 40
SHIP_TYPES = [('Battleship', 4), ('Destroyer', 3), ('Submarine', 2)]  # (name, length)

# Colors
WATER_COLOR = (0, 0, 255)
SHIP_COLOR = (169, 169, 169)
HIT_COLOR = (255, 0, 0)
MISS_COLOR = (255, 255, 255)

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Battleship Game')
        self.clock = pygame.time.Clock()
        self.player_board = Board()
        self.computer_board = Board()
        self.computer = Player('Computer', self.computer_board, is_computer=True)
        self.player = Player('Player', self.player_board)
        self.current_turn = self.player

    def run(self):
        # Main game loop
        running = True
        while running:
            self.handle_events()
            self.draw()
            self.check_game_over()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_events(self):
        # Handle player inputs and game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_player_turn(event.pos)

    def handle_player_turn(self, pos):
        # Player's turn logic, check clicks, and attack
        if self.current_turn == self.player:
            # Implement player's attack logic
            # Switch turns after the attack
            self.current_turn = self.computer

    def handle_computer_turn(self):
        # Computer's turn logic, randomly attack player's grid
        if self.current_turn == self.computer:
            # Implement computer's attack logic using random choice
            # Switch turns after the attack
            self.current_turn = self.player

    def check_game_over(self):
        # Check if all ships of either player or computer are sunk
        if self.player_board.all_ships_sunk() or self.computer_board.all_ships_sunk():
            # Display the winner and provide options to restart or quit
            print("Game Over")

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Draw boards, ships, hits, and misses
        self.player_board.draw(self.screen, offset=(50, 50), is_player=True)
        self.computer_board.draw(self.screen, offset=(550, 50), is_player=False)

class Board:
    def __init__(self):
        self.grid = [['~' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # '~' for water
        self.ships = []
        self.place_ships()

    def place_ships(self):
        for name, length in SHIP_TYPES:
            self.place_ship_recursively(length)

    def place_ship_recursively(self, ship_length):
        # Recursively try placing a ship
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        orientation = random.choice(['H', 'V'])
        if self.can_place_ship(x, y, ship_length, orientation):
            ship = Ship(ship_length, orientation, (x, y))
            self.ships.append(ship)
            self.mark_ship_on_grid(ship)
        else:
            self.place_ship_recursively(ship_length)

    def can_place_ship(self, x, y, length, orientation):
        if orientation == "H":
            if x + length > GRID_SIZE:  # Ensures the ship fits within the boundaries of the board.
                return False
        else:
            if y + length > GRID_SIZE:
                return False

        return True

    def mark_ship_on_grid(self, ship):
        x, y = ship.start_pos
        for i in range(ship.length):
            if ship.orientation == "H":
                self.grid[y][x + i] = "S"
            else:
                self.grid[y + i][x] = "S"

            
        

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def draw(self, screen, offset, is_player=True):
        # Draw the board with ships, hits, and misses
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Draw each cell based on its state
                rect = pygame.Rect(offset[0] + col * CELL_SIZE, offset[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell_state = self.grid[row][col]

                if cell_state == "~": # Adding in the cell state and colour
                    pygame.draw.rect(screen, WATER_COLOR, rect)
                elif cell_state == "S": # S is for Ship
                    if is_player: # Checking if its the player to ensure the enemy cant see the ships
                        pygame.draw.rect(screen, SHIP_COLOR, rect)
                    else:
                        pygame.draw.rect(screen, WATER_COLOR, rect)
                elif cell_state == "H": # H is for Hit
                    pygame.draw.rect(screen, HIT_COLOR, rect)
                elif cell_state == "M":
                    pygame.draw.rect(screen, MISS_COLOR, rect)
                elif cell_state == "X": # X is for Hit
                    pygame.draw.rect(screen, (0, 0, 0), rect) # Logicc for what color the squares will be depending on the scenario

                pygame.draw.rect(screen, (0, 0, 0), rect, 1) # AI told me I needed to add 1, not sure why

                # Feedback depending on the action. 

                font = pygame.font.Font(None, 24)
                if self.last_hit:
                    text = font.render("Hit!", True, (255, 0, 0))
                elif self.last_miss:
                    text = font.render("Miss!", True, (255, 255, 255))
                elif self.last_sunk:
                    text = font.render(f"You Sunk my {self.last_sunk}!", True, (255, 0, 0))
                else:
                    text = font.render("", True, (0, 0, 0))

                screen.blit(text, (offset[0], offset[1] + GRID_SIZE * CELL_SIZE + 10))







class Ship:
    def __init__(self, length, orientation, start_pos):
        self.length = length
        self.orientation = orientation
        self.start_pos = start_pos
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.length

class Player:
    def __init__(self, name, board, is_computer=False):
        self.name = name
        self.board = board
        self.is_computer = is_computer

    def take_turn(self):
        # Logic for taking a turn (attacking the opponent's board)
        pass

# Main execution
if __name__ == '__main__':
    game = Game()
    game.run()
