import pandas as pd
from fastf1.ergast import Ergast
import fastf1
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache')

ergast = Ergast()
drivers_wins = {}

for runde in range(1, 20):
    results = ergast.get_race_results(season=2025, round=runde)
    results_list = results.content[0]
    pf = pd.DataFrame(results_list)
    
    winner = pf[pf['position'] == 1]['driverId'].values[0]
    

    for driver in set(pf['driverId']):
        if driver not in drivers_wins:
            drivers_wins[driver] = [0] * 19
        if runde > 1:
            drivers_wins[driver][runde-1] = drivers_wins[driver][runde-2]
        if driver == winner:
            drivers_wins[driver][runde-1] += 1


plt.style.use('dark_background')
plt.figure(figsize=(15, 8))

winning_drivers = {d: w for d, w in drivers_wins.items() if max(w) > 0}

colors = ['orange','blue','yellow','cyan']
for idx, (driver, wins) in enumerate(winning_drivers.items()):
    plt.plot(range(1, 20), wins, label=driver, color=colors[idx % len(colors)], marker='o')

plt.xticks(range(1, 20), rotation=45)
plt.xlabel('Grand Prix')
plt.ylabel('Anzahl Siege')
plt.title('F1 Rennsiege pro Fahrer 2025')
plt.grid(True, alpha=0.2)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

