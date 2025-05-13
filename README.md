# BrickBreakerAI

This project implements a neural network that plays Brick Breaker, a clone of the popular Atari game 'Breakout', using the NEAT algorithm.

![alt text](https://raw.githubusercontent.com/CrnkovicMatej/BrickBreakerAI/main/Videos/bricks.jpg)

## Requirements

To run this project successfully, you need Python and the following packages installed:  
- `pygame`  
- `neat-python`  

All dependencies are listed in `requirements.txt`.

### Install Packages

You can install the packages using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pygame
pip install neat-python
```

## Playing the Game

For AI training, a custom Brick Breaker game is implemented and placed within the BrickBreaker Python package.

If you'd like to play the game manually, run the playGame.py file.

To adjust the game speed, change the clock.tick() value in line 12 of playGame.py:
```python
clock.tick(100)
```

## Quick Demo of AI Training and Gameplay
To preview AI training and gameplay, two videos are included in the repository:

treniranje.mp4 – showcases the AI bot learning process across generations

best AI playing.mp4 – shows the final trained AI playing the game

## Running the AI
The file winner.pkl contains the genome of the best-performing agent trained using the NEAT algorithm.

To see it in action, simply run: test_best_ai.py 

To test a different genome pickle, replace the filename in line 39 of test_best_ai.py:
```python
# Replace 'winner.pkl' with your own pickle file
winner_path = os.path.join(local_dir, "winner.pkl")
```
## Training the AI from Scratch

To retrain the AI, run:
```python
python main.py
```

Training uses NEAT checkpointing. If interrupted, you can resume from a specific checkpoint by adjusting lines 119–120 in main.py:


```python
#pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
pop = neat.Population(config)
```

# BrickBreakerAI (HR)

Ovaj projekat implementira neuronsku mrežu koja igra igru Brick Breaker, kopiju popularne
Atari igre 'Breakout' koristeći NEAT algoritam.

![alt text](https://raw.githubusercontent.com/CrnkovicMatej/BrickBreakerAI/main/Videos/bricks.jpg)


## Zahtjevi

Kako bi uspješno pokretali ove programe potrebno je imati instaliran python 
te programske pakete pygame i neat-python.

Zahtjevi su navedeni u requirements.txt.


## Instalacija paketa

Možete koristiti [pip](https://pip.pypa.io/en/stable/) za instalaciju paketa.

```bash
pip install pygame
pip install neat-python

```

## Igranje igre

Za potrebe treniranja AI unutar ovog projekta zasebno je implementirana igra Brick Breaker i
većinski smještena u novi python paket BrickBreaker.

Oni koji žele mogu se samostalno okušati u igranju igre pokretanjem datoteke playGame.py.

Brzina igre može se prilagoditi povećavanjem ili smajnivanjem tick-a u 12. liniji iste datoteke:
```python
clock.tick(100)
```

## Brzi pregled treniranja i igranja AI

Za one koji žele samo pogledati kako je tekao trening AI i kako je on na kraju 
igrao igru u repozitoriju postoje dva videa:

treniranje.mp4 - koji prikazuje proces treniranja AI bota kroz generacije

best AI playing.mp4 - koji prikazuje kako istrenirani AI igra igru

## Pokretanje AI 

U datoteci winner.pkl sačuvan je genom kojeg je NEAT algoritam izbacio kao najboljeg.

Ukoliko samostalno želite provjeriti kako taj genom igra igru možete jednostavno pokrenuti 
datoteku test_best_ai.py 

Ukoliko želite testirati neki drugi pickle potrebno ga je eksplicitno zadati u 39. liniji datototeke test_best_ai.py

```python
#Umjesto winner.pkl odabrati svoj pickle
winner_path = os.path.join(local_dir, "winner.pkl")
```

## Novo treniranje AI

Ukoliko želite iznova trenirati AI možete to učiniti uz jednostavno pokretanje datoteke
main.py. Kako je u trenutačnoj implementaciji omogućeno stvaranje takozvanih checkpoint-a
ukoliko se odlučite u nekom trenutku prekinuti trening, a kasnije ga nastaviti možete to učiniti tako da odkomentirate prvu liniju
idućeg snippeta i zakomentirate drugu uz napomenu da odaberete checkpoint od kojeg želite nastaviti (ovdje je to checkpoint 4).
Idući snippet nalazi se u 119 i 120 liniji datoteke main.py

```python
#pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
pop = neat.Population(config)
```
