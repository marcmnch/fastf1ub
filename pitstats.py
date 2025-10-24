import fastf1
import pandas as pd
from fastf1.ergast import Ergast
import matplotlib.pyplot as plt
import matplotlib.cm as cm

fastf1.Cache.enable_cache('cache')
ergast = Ergast()

total_points = {}
standings_history = []

for runde in range(1, 20):
    pitstops = ergast.get_pit_stops(season=2025, round=runde)
    pitstops_df = pd.DataFrame(pitstops.content[0])
    if pitstops_df.empty:
        standings_history.append(total_points.copy())
        continue


    mean_durations = pitstops_df.groupby('driverId')['duration'].mean()
    sorted_drivers = mean_durations.sort_values()

    for idx, (driver, duration) in enumerate(sorted_drivers.items()):
        points = 20 - idx
        if points < 1:
            points = 1
        total_points[driver] = total_points.get(driver, 0) + points

    standings_history.append(total_points.copy())

standings_df = pd.DataFrame(standings_history).fillna(0)

top_drivers = standings_df.iloc[-1].sort_values(ascending=False).head(5).index


# Farben generieren
num_drivers = len(standings_df.columns)
colors = cm.get_cmap('tab20', num_drivers)

# Fahrer nach Endstand sortieren und Label mit Punkten
final_points = standings_df.iloc[-1]
sorted_drivers = final_points.sort_values(ascending=False).index

plt.style.use('dark_background')
plt.figure(figsize=(15, 8))

handles = []
labels = []
for idx, driver in enumerate(sorted_drivers):
    label = f"{driver} ({int(final_points[driver])} P)"
    line, = plt.plot(range(1, 20), standings_df[driver], label=label, color=colors(idx), marker='o')
    handles.append(line)
    labels.append(label)

plt.xlabel('Rennwochenende')
plt.ylabel('Gesamtpunkte')
plt.xticks(range(0,20))
plt.title('Pitstop-Standings Entwicklung 2025 (Alle Fahrer, sortierte Legende)')
plt.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.show()
