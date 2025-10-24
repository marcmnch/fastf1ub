import fastf1
import matplotlib.pyplot as plt
import pandas as pd

fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2025,18,'R')
session.load()
results_list = session.results
pf = pd.DataFrame(results_list)
print(results_list)
positions = pf[['Abbreviation','Points']]

plt.style.use('dark_background')
plt.figure(figsize=(15, 15))
plt.plot(pf['Abbreviation'], pf['Points'], marker='p')
plt.xticks(range(0,20), rotation=45,)
plt.yticks(range(0,26))
plt.grid(True, alpha=0.2)
plt.xlabel('Fahrer')
plt.ylabel('Punlte')
plt.title('Punkteverteilung Singapur GP')
plt.show()