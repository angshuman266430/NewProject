import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# Data
data = {'Task': ['Developing the research goals', 'Data collection and literature review',
                 'Development of full methodology for machine learning',
                 'Development of project timeline and deliverable deadlines', 'Administrative needs'],
        'Start': ['2023-05-08', '2023-06-01', '2023-06-20', '2023-07-25', '2023-05-02'],
        'Finish': ['2023-06-06', '2023-07-10', '2023-07-25', '2023-08-30', '2023-08-30'],
        'Budget': ['$1,644', '$3,496', '$4,951', '$3,426', '$1,461'],
        'Hours': ['10 hours', '25 hours', '36 hours', '22.5 hours', '9.5 hours']}

# Create DataFrame
df = pd.DataFrame(data)

# Convert 'Start' and 'Finish' into datetime
df['Start'] = pd.to_datetime(df['Start'])
df['Finish'] = pd.to_datetime(df['Finish'])

# Plotting
fig, ax = plt.subplots(figsize=(10,6))

# Create a plot for each task
for i in range(len(df)):
    ax.barh(df['Task'][i], df['Finish'][i] - df['Start'][i], left = df['Start'][i], color = 'blue')
    mid_date = df['Start'][i] + (df['Finish'][i] - df['Start'][i]) / 2
    ax.text(mid_date, df['Task'][i], f"{df['Budget'][i]} ({df['Hours'][i]})", color='white', va='center', ha='center')

# Set the date format
date_form = DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Set the date ticks interval
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY, interval=2))

# Set x-axis limits
ax.set_xlim([pd.to_datetime('2023-05-01'), pd.to_datetime('2023-08-30') + pd.Timedelta(days=1)])

# Set labels and title with increased font size
plt.xlabel('Date', fontsize=12)
plt.ylabel('Task', fontsize=12)
plt.title('Gantt Chart for $15,000 Budget')

# Rotate date labels
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
