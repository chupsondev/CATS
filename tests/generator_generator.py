import random
def generate():
    passing: bool = random.randint(1, 100) < 70
    return ('4', '5') if passing else ('10', '20')
