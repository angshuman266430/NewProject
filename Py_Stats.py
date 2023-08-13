import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Function to calculate PBIAS
def pbias(simulated, observed):
    return 100.0 * (np.sum(simulated - observed) / np.sum(observed))

# Function to calculate NSE
def nse(simulated, observed):
    return 1 - np.sum((simulated - observed) ** 2) / np.sum((observed - np.mean(observed)) ** 2)

# Function to calculate RSR
def rsr(simulated, observed):
    return np.sqrt(np.sum((simulated - observed) ** 2)) / np.sqrt(np.sum((observed - np.mean(observed)) ** 2))

# Define performance rating functions for each metric
def get_rating_r2(value):
    if 0.85 < value <= 1.00:
        return 'Very Good'
    elif 0.75 < value <= 0.85:
        return 'Good'
    elif 0.60 < value <= 0.75:
        return 'Satisfactory'
    else:
        return 'Unsatisfactory'

def get_rating_nse(value):
    if 0.80 < value <= 1.00:
        return 'Very Good'
    elif 0.70 < value <= 0.80:
        return 'Good'
    elif 0.50 < value <= 0.70:
        return 'Satisfactory'
    else:
        return 'Unsatisfactory'

def get_rating_rsr(value):
    if 0.00 < value <= 0.50:
        return 'Very Good'
    elif 0.50 < value <= 0.60:
        return 'Good'
    elif 0.60 < value <= 0.70:
        return 'Satisfactory'
    else:
        return 'Unsatisfactory'

def get_rating_pbias(value):
    if abs(value) < 5:
        return 'Very Good'
    elif 5 <= abs(value) <= 10:
        return 'Good'
    elif 10 <= abs(value) <= 15:
        return 'Satisfactory'
    else:
        return 'Unsatisfactory'

# Define color functions for each performance rating
def get_color_rating(value):
    if value == 'Very Good':
        return 'darkgreen'
    elif value == 'Good':
        return 'lightgreen'
    elif value == 'Satisfactory':
        return 'yellow'
    else:
        return 'red'

colors = ['darkgreen', 'lightgreen', 'yellow', 'red', 'blue']
ratings = ['Very Good', 'Good', 'Satisfactory', 'Unsatisfactory', 'Not Rated']
patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, ratings)]

# Load datasets
df_dw = pd.read_csv('Modeled_results.csv')
df_swe = pd.read_csv('Modeled_results_withgate_n_test12Yushi.csv')

# Assuming same column names (stations) and same order
stations = df_dw.columns[1:]

# Replace "@" with "at", replace "_" with " " in the station names
stations = [station.replace("@", "at").replace("_", " ") for station in stations]

metrics_df = pd.DataFrame(index=stations, columns=['PBIAS', 'NSE', 'RSR', 'MAE (ft)', 'RMSE (ft)', 'R\u00b2'])

# Iterate through each station and calculate the metrics
for i, station in enumerate(df_dw.columns[1:]):
    simulated = df_dw[station]
    observed = df_swe[station]

    # Calculating metrics
    pbias_val = pbias(simulated, observed)
    nse_val = nse(simulated, observed)
    rsr_val = rsr(simulated, observed)
    mae_val = mean_absolute_error(simulated, observed)
    rmse_val = np.sqrt(mean_squared_error(simulated, observed))
    r2_val = np.corrcoef(simulated, observed)[0, 1] ** 2

    metrics_df.loc[stations[i]] = [pbias_val, nse_val, rsr_val, mae_val, rmse_val, r2_val]

print(metrics_df)

# Save to csv
metrics_df.to_csv('Py_Stats.csv')

# Create rating columns for each metric
metrics_df['R² Rating'] = metrics_df['R\u00b2'].apply(get_rating_r2)
metrics_df['NSE Rating'] = metrics_df['NSE'].apply(get_rating_nse)
metrics_df['RSR Rating'] = metrics_df['RSR'].apply(get_rating_rsr)
metrics_df['PBIAS Rating'] = metrics_df['PBIAS'].apply(get_rating_pbias)

# Create color columns for each rating
metrics_df['R² Color'] = metrics_df['R² Rating'].apply(get_color_rating)
metrics_df['NSE Color'] = metrics_df['NSE Rating'].apply(get_color_rating)
metrics_df['RSR Color'] = metrics_df['RSR Rating'].apply(get_color_rating)
metrics_df['PBIAS Color'] = metrics_df['PBIAS Rating'].apply(get_color_rating)

# Create color columns for RMSE and MAE
metrics_df['RMSE (ft) Color'] = 'blue'
metrics_df['MAE (ft) Color'] = 'blue'

print(metrics_df)

# Plot metrics with color coding
metrics = ['R\u00b2', 'NSE', 'RSR', 'PBIAS', 'RMSE (ft)', 'MAE (ft)']
for metric in metrics:
    plt.figure(figsize=(10, 5))  # Adjust size according to your needs.
    color = metrics_df[f'{metric} Color']
    plt.barh(metrics_df.index, metrics_df[metric], color=color)
    plt.title(metric)
    plt.xlabel('Value')
    plt.ylabel('Station')

    # Include the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    plt.tight_layout()
    plt.savefig(f'{metric}.png')  # Save each figure with the corresponding metric name
    plt.show()

# Function to create HTML content
def create_html(stations, metrics):
    html_content = "<html><head><title>Results Plots</title></head><body>"
    for metric in metrics:
        html_content += f"<h2>{metric}</h2>"
        html_content += f"<img src='{metric}.png' alt='{metric} plot'>"
    html_content += "</body></html>"
    return html_content

# After plotting the metrics
html_content = create_html(stations, metrics)

# Write the HTML content to a file
with open('results_plots.html', 'w') as file:
    file.write(html_content)
