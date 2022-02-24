#ask for range for random number, have the user guess until they are correct
import random

start = input('Enter the start of the range: ')
while not start.isdigit():
    print('Please enter a valid number.')
    start = input('Enter the start of the range: ')

end = input('Enter the end of the range: ')
while not end.isdigit() or int(end) < int(start):
    print('Please enter a valid number.')
    end = input('Enter the end of the range: ')

random_number = random.randint(int(start), int(end))

guess = None
attempts = 0

while guess != random_number:
    guessed_number = input("Guess a number: ")
    if not guessed_number.isdigit():
        print("Please enter a valid number.")
        continue
    
    attempts += 1
    guess = int(guessed_number)

suffix = ""
if attempts > 1:
    suffix = "s"

print(f'You guessed the number in {attempts} attempt{suffix}')
