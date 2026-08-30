import matplotlib.pyplot as plt
import numpy as np
import os

def generate_burndown():
    days = list(range(0, 11))
    
    # Total Sprint Points = 42 (Stories 1 to 10)
    ideal_burndown = [42 - (42 / 10.0) * i for i in days]
    
    # Actual story points remaining across 10 sprint days
    actual_burndown = [42, 42, 39, 34, 26, 21, 16, 13, 10, 5, 0]
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Plot lines
    ax.plot(days, ideal_burndown, label='Ideal Burndown Trend', color='#888888', linestyle='--', linewidth=2.5, marker='o', markersize=6)
    ax.plot(days, actual_burndown, label='Actual Sprint Burndown', color='#1E88E5', linewidth=3.5, marker='s', markersize=8)
    
    # Fill under actual curve
    ax.fill_between(days, actual_burndown, color='#1E88E5', alpha=0.15)
    
    # Annotations & styling
    ax.set_title('Sprint 1 Burndown Chart - Foundation & Core Architecture', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Sprint Days (Day 0 - Day 10)', fontsize=12, labelpad=10)
    ax.set_ylabel('Remaining Story Points', fontsize=12, labelpad=10)
    
    ax.set_xticks(days)
    ax.set_xticklabels([f'Day {d}' for d in days], fontsize=10)
    ax.set_ylim(-1, 46)
    
    # Highlight milestone values
    for d, val in zip(days, actual_burndown):
        ax.annotate(f'{val} pts', (d, val), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, fontweight='bold', color='#0D47A1')
        
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    
    # Save image to root and docs/
    os.makedirs('docs', exist_ok=True)
    plt.savefig('burndown_chart.png', dpi=300)
    plt.savefig('docs/burndown_chart.png', dpi=300)
    plt.close()
    
    print("Burndown chart PNG generated successfully at burndown_chart.png and docs/burndown_chart.png")

if __name__ == '__main__':
    generate_burndown()
