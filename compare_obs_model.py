import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import plotly.subplots as sp

# File paths
obs_file = 'Z:\\Greenbelt\\RAS_Model_Working\\Observation\\Observed_data_CPPJ_May2021_Interpolated_UTC_adjusted.csv'
model_file = 'Z:\\Greenbelt\\RAS_Model_Working\\Observation\\Modeled_results.csv'
obs_station_file = 'Z:\\Greenbelt\\RAS_Model_Working\\Observation\\Observed_data_StationID_UTC.csv'
model_station_file = 'Z:\\Greenbelt\\RAS_Model_Working\\Observation\\Modeled_results_StationID.txt'

# Reading the data
obs_value_table = pd.read_csv(obs_file)
model_table = pd.read_csv(model_file)
obs_station_table = pd.read_csv(obs_station_file)
model_station = pd.read_csv(model_station_file, header=None).values.flatten()

obs_station = obs_station_table.iloc[:, 0].values
obs_correctors = obs_station_table.iloc[:, 1].values

# Get matched station names for titles
matched_titles = []
for i in range(len(obs_station)):
    for j in range(len(model_station)):
        if obs_station[i].lower() == model_station[j].lower():
            matched_titles.append(obs_station[i].replace('@', 'at').replace('_', ' '))

# Create a subplot for interactive plots
fig = sp.make_subplots(rows=len(matched_titles), cols=1, vertical_spacing=0.02, subplot_titles=matched_titles)

# Index for subplot row
row_index = 1

for i in range(len(obs_station)):
    matched = False
    for j in range(len(model_station)):
        if obs_station[i].lower() == model_station[j].lower():
            matched = True
            model_date = pd.to_datetime(model_table.iloc[:, 0])
            model_value = model_table.iloc[:, j + 1]
            obs_date = pd.to_datetime(obs_value_table.iloc[:, 0])
            obs_value = obs_value_table.iloc[:, i + 1]
            obs_value_corrected = obs_value + obs_correctors[i]

            # Static plot
            plt.plot(model_date, model_value, label='Modeled', color='b')
            plt.plot(obs_date, obs_value_corrected, label='Observed', color='r', linestyle='--')
            plt.xlim([pd.Timestamp('05/16/2021'), pd.Timestamp('06/01/2021')])
            title_name = obs_station[i].replace('@', 'at').replace('_', ' ')
            plt.title(title_name, fontsize=14)
            plt.legend()
            plt.ylabel('Water Level (ft)', fontweight='bold')
            plt.xlabel('Date', fontweight='bold')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
            plt.gcf().autofmt_xdate()
            plt.tick_params(axis='both', direction='in', length=6, width=1)  # Add tick marks
            figure_name = f'Z:\\Greenbelt\\RAS_Model_Working\\Observation\\{obs_station[i]}.png'
            figure_name = figure_name.replace('@', 'at')
            plt.savefig(figure_name, dpi=300, bbox_inches='tight')  # High resolution
            plt.close()

            # Interactive plot
            show_legend = True if row_index == 1 else False
            fig.add_trace(go.Scatter(x=model_date, y=model_value, name='Modeled', line=dict(color='blue'), showlegend=show_legend), row=row_index, col=1)
            fig.add_trace(go.Scatter(x=obs_date, y=obs_value_corrected, name='Observed', line=dict(color='red', dash='dot'), showlegend=show_legend), row=row_index, col=1)
            row_index += 1

    if not matched:
        print(f"No match found for station: {obs_station[i]}")

# Style interactive plots
fig.update_layout(height=300 * len(matched_titles))
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Water Level (ft)")
fig.write_html('Z:\\Greenbelt\\RAS_Model_Working\\Observation\\interactive_plots.html')
