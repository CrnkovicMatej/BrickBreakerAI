# BrickBreakerAI

Ovaj projekat implementira neuronsku mrežu koja igra igru Brick Breaker, kopiju popularne
Atari igre 'Breakout' koristeći NEAT algoritam.

# Zahtjevi

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
