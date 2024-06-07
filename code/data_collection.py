import pygame
import time
import pandas as pd

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
font = pygame.font.Font(None, 36)
input_text = ""
target_password = "inetum"
attempts = 50
completed_attempts = 0
start_time = None
key_data = []

running = True
while running and completed_attempts < attempts:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not start_time:
                start_time = time.time()
            key_data.append({
                'key': pygame.key.name(event.key),
                'timestamp': time.time(),
                'event': 'keydown',
                'attempt': completed_attempts,
                'correct': None  # Will be set later based on attempt outcome
            })
            input_text += pygame.key.name(event.key)
        elif event.type == pygame.KEYUP:
            key_data.append({
                'key': pygame.key.name(event.key),
                'timestamp': time.time(),
                'event': 'keyup',
                'attempt': completed_attempts,
                'correct': None  # Will be set later based on attempt outcome
            })

    screen.fill((255, 255, 255))
    text = font.render(input_text, True, (0, 0, 0))
    screen.blit(text, (20, 20))
    pygame.display.flip()

    # Check if the password is typed
    if len(input_text) >= len(target_password):
        if input_text == target_password:
            # Mark all keystrokes in this attempt as correct
            for record in key_data:
                if record['attempt'] == completed_attempts:
                    record['correct'] = True
            completed_attempts += 1
            print(f"Attempt {completed_attempts}/{attempts} complete.")
        else:
            # Mark all keystrokes in this attempt as incorrect
            for record in key_data:
                if record['attempt'] == completed_attempts:
                    record['correct'] = False
            print("Incorrect password. Please try again.")

        # Reset input text for the next attempt
        input_text = ""
        start_time = None  # Reset start time for the next attempt

pygame.quit()

# Save the collected data to a CSV file
df = pd.DataFrame(key_data)
df.to_csv('keystroke_data.csv', index=False)
print("Data collection complete. Data saved to keystroke_data.csv")