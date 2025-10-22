import pygame
import pandas as pd
import os

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("5K Split Time Entry and Stats")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

# Colors
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# CSV filename
FILE_PATH = "scores.csv"

# Input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789./"
                if event.unicode.lower() in allowed_chars:
                    self.text += event.unicode
            self.txt_surface = font.render(self.text, True, BLACK)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def get_value(self):
        text = self.text.strip().lower()
        if text == "n/a" or text == "na":
            return "N/A"
        try:
            return float(self.text)
        except:
            return None

# Back button for pages
back_button = pygame.Rect(20, 20, 80, 40)

def draw_back_button():
    pygame.draw.rect(screen, COLOR_ACTIVE, back_button)
    label = font.render("Back", True, WHITE)
    screen.blit(label, (back_button.x + 15, back_button.y + 7))

# Menu buttons
menu_buttons = {
    "Top Scores": pygame.Rect(200, 150, 200, 50),
    "Recent Scores": pygame.Rect(200, 220, 200, 50),
    "Average Scores": pygame.Rect(200, 290, 200, 50),
    "Predicted Scores": pygame.Rect(200, 360, 200, 50),
    "Enter Times": pygame.Rect(200, 430, 200, 50),
}

def draw_menu():
    screen.fill(WHITE)
    title = font.render("5K Running Stats Menu", True, BLACK)
    screen.blit(title, (180, 80))
    for text, rect in menu_buttons.items():
        pygame.draw.rect(screen, COLOR_ACTIVE, rect)
        label = font.render(text, True, WHITE)
        screen.blit(label, (rect.x + 30, rect.y + 12))

# Input screen setup
labels = ["5K Total", "Split 1K", "Split 2K", "Split 3K", "Split 4K", "Split 5K"]
input_boxes = [InputBox(250, 150 + i*50, 140, 32) for i in range(len(labels))]

submit_button = pygame.Rect(230, 500, 140, 40)

def draw_input_screen():
    screen.fill(WHITE)
    title = font.render("Enter your times (type N/A if not available)", True, BLACK)
    screen.blit(title, (70, 70))

    for i, box in enumerate(input_boxes):
        label = font.render(labels[i], True, BLACK)
        screen.blit(label, (120, 150 + i*50))
        box.draw(screen)

    pygame.draw.rect(screen, COLOR_ACTIVE, submit_button)
    submit_label = font.render("Submit", True, WHITE)
    screen.blit(submit_label, (submit_button.x + 40, submit_button.y + 8))

    draw_back_button()

def save_to_csv(values):
    df_new = pd.DataFrame([{
        "Total_5k": values[0],
        "Split_1k": values[1],
        "Split_2k": values[2],
        "Split_3k": values[3],
        "Split_4k": values[4],
        "Split_5k": values[5],
    }])
    if os.path.exists(FILE_PATH):
        df_new.to_csv(FILE_PATH, mode='a', header=False, index=False)
    else:
        df_new.to_csv(FILE_PATH, index=False)

def draw_coming_soon(title_text):
    screen.fill(WHITE)
    draw_back_button()
    title = font.render(title_text, True, BLACK)
    screen.blit(title, (180, 250))
    coming = font.render("Coming Soon!", True, BLACK)
    screen.blit(coming, (230, 300))

def draw_top_scores():
    draw_coming_soon("Top Scores")

def draw_recent_scores():
    draw_coming_soon("Recent Scores")

def draw_average_scores():
    draw_coming_soon("Average Scores")

def draw_predicted_scores():
    draw_coming_soon("Predicted Scores")

# Manage which screen to display
current_screen = "menu"

def reset_input_boxes():
    for box in input_boxes:
        box.text = ""
        box.txt_surface = font.render("", True, BLACK)

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for name, rect in menu_buttons.items():
                    if rect.collidepoint(pos):
                        if name == "Top Scores":
                            current_screen = "top_scores"
                        elif name == "Recent Scores":
                            current_screen = "recent_scores"
                        elif name == "Average Scores":
                            current_screen = "average_scores"
                        elif name == "Predicted Scores":
                            current_screen = "predicted_scores"
                        elif name == "Enter Times":
                            current_screen = "input"
                            reset_input_boxes()

        elif current_screen == "input":
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    current_screen = "menu"
                if submit_button.collidepoint(event.pos):
                    values = [box.get_value() for box in input_boxes]
                    # Allow N/A or float, reject None
                    if all(v is not None for v in values):
                        save_to_csv(values)
                        reset_input_boxes()
                    else:
                        print("Please fill all fields with numbers or 'N/A'")

        else:  # On any data screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    current_screen = "menu"

    # Draw current screen
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "input":
        for box in input_boxes:
            box.update()
        draw_input_screen()
    elif current_screen == "top_scores":
        draw_top_scores()
    elif current_screen == "recent_scores":
        draw_recent_scores()
    elif current_screen == "average_scores":
        draw_average_scores()
    elif current_screen == "predicted_scores":
        draw_predicted_scores()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()