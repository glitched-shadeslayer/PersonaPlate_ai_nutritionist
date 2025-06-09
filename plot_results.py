import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file with two tabs and multi-level headers
file = 'Results-DeepGen - Hypertension.xlsx'
df_hypertension = pd.read_excel(file, sheet_name='Hypertension', header=[0, 1])
df_obesity = pd.read_excel(file, sheet_name='Obesity', header=[0, 1])

# Create two separate figures
fig1, ax1 = plt.subplots(figsize=(10, 6))  # Hypertension plot
fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(20, 6))  # Obesity plots (Calories and Fat)

# Function to create subplot for Hypertension
def create_hypertension_subplot(ax, df, title, ylabel):
    # Store original data with missing values
    original_normal = df[('Normal', 550)].copy()
    original_optimized = df[('Optimized (MAS)', 1500)].copy()

    # Interpolate missing values
    normal = original_normal.interpolate(method='linear')
    optimized = original_optimized.interpolate(method='linear')

    # Create x-axis values (profile numbers)
    x = np.arange(1, len(df) + 1)

    # Plot the constant lines (example values, adjust as needed)
    ax.axhline(y=2300, color='r', linestyle='--', label='Normal Adult Baseline (2300)')
    ax.axhline(y=1500, color='g', linestyle='--', label='Hypertension Baseline (1500)')

    # Plot the interpolated lines
    ax.plot(x, normal, 'b-', label='Normal', marker='o', markersize=4)
    ax.plot(x, optimized, color='black', label='Optimized MAS', marker='s', markersize=4)

    # Highlight missing values
    missing_normal = x[original_normal.isna()]
    missing_optimized = x[original_optimized.isna()]

    # Plot markers for missing values
    if len(missing_normal) > 0:
        ax.scatter(missing_normal, normal.loc[missing_normal-1], color='blue', s=100, zorder=5, label='No Output - Normal')
    if len(missing_optimized) > 0:
        ax.scatter(missing_optimized, optimized.loc[missing_optimized-1], color='black', s=100, zorder=5, label='No Output - Optimized MAS')

    # Customize the subplot
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Profile Number', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)

# Function to create subplot for Obesity (Calories)
def create_obesity_calories_subplot(ax, df, title, ylabel):
    # Store original data with missing values
    original_normal = df[('Calories', 'Normal')].copy()
    original_optimized = df[('Calories', 'Optimized (MAS)')].copy()

    # Interpolate missing values
    normal = original_normal.interpolate(method='linear')
    optimized = original_optimized.interpolate(method='linear')

    # Create x-axis values (profile numbers)
    x = np.arange(1, len(df) + 1)

    # Plot the constant lines (example values, adjust as needed)
    ax.axhline(y=2000, color='r', linestyle='--', label='Normal Adult Baseline (2000)')
    # ax.axhline(y=1500, color='g', linestyle='--', label='Obesity Baseline (1500)')

    # Plot the interpolated lines
    ax.plot(x, normal, 'b-', label='Normal', marker='o', markersize=4)
    ax.plot(x, optimized, color='black', label='Optimized MAS', marker='s', markersize=4)

    # Highlight missing values
    missing_normal = x[original_normal.isna()]
    missing_optimized = x[original_optimized.isna()]

    # Plot markers for missing values
    if len(missing_normal) > 0:
        ax.scatter(missing_normal, normal.loc[missing_normal-1], color='blue', s=100, zorder=5, label='No Output - Normal')
    if len(missing_optimized) > 0:
        ax.scatter(missing_optimized, optimized.loc[missing_optimized-1], color='black', s=100, zorder=5, label='No Output - Optimized MAS')

    # Customize the subplot
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Profile Number', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)

# Function to create subplot for Obesity (Fat)
def create_obesity_fat_subplot(ax, df, title, ylabel):
    # Store original data with missing values
    original_normal = df[('FAT', 'Normal')].copy()
    original_optimized = df[('FAT', 'Optimized (MAS)')].copy()

    # Interpolate missing values
    normal = original_normal.interpolate(method='linear')
    optimized = original_optimized.interpolate(method='linear')

    # Create x-axis values (profile numbers)
    x = np.arange(1, len(df) + 1)

    # Plot the constant lines (example values, adjust as needed)
    ax.axhline(y=78, color='r', linestyle='--', label='Normal Adult Baseline Max (78g)')
    ax.axhline(y=45, color='r', linestyle='--', label='Normal Adult Baseline Min (45g)')

    # Plot the interpolated lines
    ax.plot(x, normal, 'b-', label='Normal', marker='o', markersize=4)
    ax.plot(x, optimized, color='black', label='Optimized MAS', marker='s', markersize=4)

    # Highlight missing values
    missing_normal = x[original_normal.isna()]
    missing_optimized = x[original_optimized.isna()]

    # Plot markers for missing values
    if len(missing_normal) > 0:
        ax.scatter(missing_normal, normal.loc[missing_normal-1], color='blue', s=100, zorder=5, label='No Output - Normal')
    if len(missing_optimized) > 0:
        ax.scatter(missing_optimized, optimized.loc[missing_optimized-1], color='black', s=100, zorder=5, label='No Output - Optimized MAS')

    # Customize the subplot
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Profile Number', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)

# Create the plots
create_hypertension_subplot(ax1, df_hypertension, 'Users with Hypertension - Sodium Comparison', 'Daily Sodium Intake (mg)')
create_obesity_calories_subplot(ax2, df_obesity, 'Users with Obesity - Calories Comparison', 'Daily Calories Intake (kcal)')
create_obesity_fat_subplot(ax3, df_obesity, 'Users with Obesity - Fat Comparison', 'Daily Fat Intake (g)')

# Adjust layout and save both figures
fig1.tight_layout()
fig2.tight_layout()
fig1.savefig('hypertension_plot.png', dpi=300, bbox_inches='tight')
fig2.savefig('obesity_plots.png', dpi=300, bbox_inches='tight')
plt.close('all') 