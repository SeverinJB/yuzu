# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

startCapital = 5000
endCapital = startCapital
dailyWin = 0.01

for day in range(22):
    endCapital += endCapital * dailyWin

print(f'Value is {startCapital}\nEnd capital: {endCapital}\nMultiplier: {endCapital/startCapital}')