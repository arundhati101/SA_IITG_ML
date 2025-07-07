import pandas as pd

# Load the dataset
df = pd.read_csv('dataset.csv')

# Display shape and first few rows
print("Dataset Shape:", df.shape)
df.head()

# Check column names and types
df.info()

# Quick summary of numerical columns
df.describe()

import numpy as np

# Step 1: Combine Date and Time into a Timestamp (with correct date format)
df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'], dayfirst=True)

# Step 2: Sort the data by Parking Lot and Time
df.sort_values(by=['SystemCodeNumber', 'Timestamp'], inplace=True)

# Step 3: Encode 'VehicleType' and 'TrafficConditionNearby'
vehicle_map = {'car': 1.0, 'bike': 0.5, 'truck': 1.5}
traffic_map = {'low': 1.0, 'medium': 2.0, 'high': 3.0}

df['VehicleWeight'] = df['VehicleType'].map(vehicle_map)
df['TrafficLevel'] = df['TrafficConditionNearby'].map(traffic_map)

# Reset index
df.reset_index(drop=True, inplace=True)

# View the cleaned data
df[['SystemCodeNumber', 'Timestamp', 'Occupancy', 'Capacity', 'QueueLength', 'VehicleWeight', 'TrafficLevel']].head()

# Initialize model parameters
alpha = 2.0
base_price = 10
min_price, max_price = 5, 20

# Create a price column initialized with base price
df['Price_Model1'] = base_price

# Apply the baseline pricing logic
for i in range(1, len(df)):
    if df.loc[i, 'SystemCodeNumber'] == df.loc[i-1, 'SystemCodeNumber']:
        prev_price = df.loc[i-1, 'Price_Model1']
        occupancy_ratio = df.loc[i, 'Occupancy'] / df.loc[i, 'Capacity']
        new_price = prev_price + alpha * occupancy_ratio
        new_price = min(max(new_price, min_price), max_price)
        df.loc[i, 'Price_Model1'] = new_price
    else:
        df.loc[i, 'Price_Model1'] = base_price  # reset for new lot

# View results
df[['SystemCodeNumber', 'Timestamp', 'Occupancy', 'Capacity', 'Price_Model1']].head(15)

# Apply the baseline pricing logic (with capped increments)
df['Price_Model1'] = base_price

for i in range(1, len(df)):
    if df.loc[i, 'SystemCodeNumber'] == df.loc[i-1, 'SystemCodeNumber']:
        prev_price = df.loc[i-1, 'Price_Model1']
        occ_ratio = df.loc[i, 'Occupancy'] / df.loc[i, 'Capacity']
        
        # Limit change based on normalized increment
        delta = alpha * (occ_ratio - 0.5)  # center around 0.5 utilization
        new_price = prev_price + delta
        new_price = min(max(new_price, min_price), max_price)
        
        df.loc[i, 'Price_Model1'] = new_price
    else:
        df.loc[i, 'Price_Model1'] = base_price  # reset

from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10

output_notebook()

# Filter data for one lot
lot_id = "BHMBCCMKT01"  # You can change this ID to try different lots
df_lot = df[df['SystemCodeNumber'] == lot_id]

# Create Bokeh data source
source = ColumnDataSource(df_lot)

# Create the figure using 'height' and 'width'
p = figure(x_axis_type='datetime',
           title=f"Model 1 Pricing Over Time for Lot {lot_id}",
           height=350, width=800)

# Add price line
p.line(x='Timestamp', y='Price_Model1', source=source,
       line_width=2, color=Category10[10][0], legend_label="Price")

# Add hover tool
p.add_tools(HoverTool(
    tooltips=[
        ("Time", "@Timestamp{%F %H:%M}"),
        ("Price", "@Price_Model1{$0.00}"),
        ("Occupancy", "@Occupancy"),
        ("Queue", "@QueueLength"),
    ],
    formatters={'@Timestamp': 'datetime'},
    mode='vline'
))

# Labels
p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Price ($)"
p.legend.location = "top_left"
p.legend.click_policy = "hide"

# Display the plot
show(p)

from sklearn.preprocessing import MinMaxScaler

# Define weights (you can tune them)
alpha, beta, gamma, delta, epsilon = 1.5, 0.8, 1.2, 2.0, 1.0
lambda_ = 0.7  # how aggressively price reacts to demand
base_price = 10

# Compute raw demand score
df['RawDemand'] = (
    alpha * (df['Occupancy'] / df['Capacity']) +
    beta * df['QueueLength'] -
    gamma * df['TrafficLevel'] +
    delta * df['IsSpecialDay'] +
    epsilon * df['VehicleWeight']
)

# Normalize demand to 0–1
scaler = MinMaxScaler()
df['NormalizedDemand'] = scaler.fit_transform(df[['RawDemand']])

# Calculate Model 2 price (bounded between 5 and 20)
df['Price_Model2'] = base_price * (1 + lambda_ * df['NormalizedDemand'])
df['Price_Model2'] = df['Price_Model2'].clip(lower=5, upper=20)

# Show sample
df[['SystemCodeNumber', 'Timestamp', 'Occupancy', 'QueueLength', 'TrafficLevel', 'Price_Model2']].head(10)


from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10

output_notebook()

# Filter data for one lot
lot_id = "BHMBCCMKT01"  # You can change this ID to try different lots
df_lot = df[df['SystemCodeNumber'] == lot_id]

# Create Bokeh data source
source = ColumnDataSource(df_lot)

# Create the figure using 'height' and 'width'
p = figure(x_axis_type='datetime',
           title=f"Model 2 Pricing Over Time for Lot {lot_id}",
           height=350, width=800)

p.line(x='Timestamp', y='Price_Model2', source=ColumnDataSource(df_lot),
       line_width=2, color=Category10[10][1], legend_label="Model 2 Price")

# Add hover tool
p.add_tools(HoverTool(
    tooltips=[
        ("Time", "@Timestamp{%F %H:%M}"),
        ("Price", "@Price_Model1{$0.00}"),
        ("Occupancy", "@Occupancy"),
        ("Queue", "@QueueLength"),
    ],
    formatters={'@Timestamp': 'datetime'},
    mode='vline'
))

# Labels
p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Price ($)"
p.legend.location = "top_left"
p.legend.click_policy = "hide"

# Display the plot
show(p)

# Just change y='Price_Model1' to Price_Model2

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show
from bokeh.palettes import Category10

# Filter data again for the lot
df_lot = df[df['SystemCodeNumber'] == lot_id]
source = ColumnDataSource(df_lot)

# Create a figure
p = figure(x_axis_type='datetime',
           title=f"Model 1 vs Model 2 Pricing for Lot {lot_id}",
           height=400, width=850)

# Model 1 Line
p.line(x='Timestamp', y='Price_Model1', source=source,
       line_width=2, color=Category10[10][0], legend_label="Model 1")

# Model 2 Line
p.line(x='Timestamp', y='Price_Model2', source=source,
       line_width=2, color=Category10[10][1], legend_label="Model 2")

# Hover tool
p.add_tools(HoverTool(
    tooltips=[
        ("Time", "@Timestamp{%F %H:%M}"),
        ("Model 1", "@Price_Model1{$0.00}"),
        ("Model 2", "@Price_Model2{$0.00}"),
        ("Occupancy", "@Occupancy"),
        ("Queue", "@QueueLength"),
    ],
    formatters={'@Timestamp': 'datetime'},
    mode='vline'
))

# Labels
p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Price ($)"
p.legend.location = "top_left"
p.legend.click_policy = "hide"

# Show plot
show(p)
