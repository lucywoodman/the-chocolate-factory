# The Chocolate Factory Importance/Feasibility chart

I opted to use the `matplotlib` Python library to create the chart in this project. On my last project, I used Figma to map everything out, but having recently learned more about this library, I opted to use code this time. It allows for quicker updating of the data without having to redraw the chart every time.

If you'd like to give this a try locally:
- Create a new project folder and open it up in [VSCode](https://code.visualstudio.com/download). Open the terminal in VSCode.
- Create a Python virtual environment and activate. I use `python -m venv env` and `. env/bin/activate`.
- Install `numpy`* and `matplotlib` in your environment. * `numpy` is not required, as you can use standard lists instead of numpy arrays.
- Create a new Jupyter notebook in VSCode and make sure it's using your environment for Python so it can access the installed libraries.
- Copy and paste the code below into the notebook and run it. The chart will pop up at the bottom.

```
import numpy as np
import matplotlib.pyplot as plt

# data
feasibility = np.array([22, 18, 6, 21, 3, 2, 23, 20, 19, 14, 13, 12, 11, 5, 9, 8, 7, 4, 10, 17, 16, 15, 1])
importance = np.array([22, 21, 20, 4, 5, 6, 7, 23, 13, 12, 9, 17, 8, 3, 16, 18, 19, 1, 10, 15, 14, 11, 2])

#plot
fig, ax = plt.subplots(1, figsize=(10,10))
ax.add_artist(plt.Circle((24, 24), 12, color='#D6A11E', alpha=0.5))
ax.add_artist(plt.Circle((24, 24), 21, color='#F0BB39', alpha=0.5))
plt.scatter(feasibility, importance, marker="o", s=1000, c='black')
plt.xlim(0, 24)
plt.ylim(0, 24)

# set aspect
ax.set_aspect('equal')
ax.plot()   # causes an autoscale update.

# remove spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# grid
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.3)
ax.xaxis.grid(color='gray', linestyle='dashed', alpha=0.3)

# title, axis labels
plt.title('The Chocolate Factory Feasibility Chart', fontsize=18, pad=20)
plt.xlabel('Feasibility/Viability', fontsize=14, labelpad=10)
plt.ylabel('Importance', fontsize=14, labelpad=10)

# ticks
plt.xticks(np.arange(min(feasibility)-1, max(feasibility)+1, 2.0))
plt.yticks(np.arange(min(importance)-1, max(importance)+1, 2.0))

# annotation
for i in range(len(feasibility)):
    plt.annotate(i + 1, (feasibility[i], importance[i]), size=14, color='white', ha='center', va='center')
```