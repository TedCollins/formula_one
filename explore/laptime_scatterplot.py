import seaborn as sns
from matplotlib import pyplot as plt

import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

race = fastf1.get_session(2023, "Azerbaijan", 'R')
race.load()

driver_laps = race.laps.pick_driver("VER").pick_quicklaps().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))

sns.scatterplot(data=driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.COMPOUND_COLORS,
                s=80,
                linewidth=0,
                legend='auto')


ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

# The y-axis increases from bottom to top by default
# Since we are plotting time, it makes sense to invert the axis
ax.invert_yaxis()
plt.suptitle("Laptimes in the 2023 Azerbaijan Grand Prix")

# Turn on major grid lines
plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()
