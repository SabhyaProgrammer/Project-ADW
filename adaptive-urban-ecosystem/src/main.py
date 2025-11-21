# src/main.py
import os
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Change this import
from simulation import Simulation

# Create simulation with smaller grid for better performance
sim = Simulation(width=40, height=40, seed=42)
sim.populate_random_people(n=60, forage_amount=5, vision=5)

# Enable ML-based decision making
sim.use_ml_decisions = True
sim.learning_rate = 0.01

# Set up figure with advanced layout
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

fig.suptitle('Adaptive Urban Ecosystem - ML Enhanced', fontsize=16, fontweight='bold')

# Create custom colormaps
resource_cmap = LinearSegmentedColormap.from_list('resources', ['#8B4513', '#90EE90', '#228B22'])
traffic_cmap = LinearSegmentedColormap.from_list('traffic', ['#E8F4F8', '#FFD700', '#FF6347'])
env_cmap = LinearSegmentedColormap.from_list('environment', ['#87CEEB', '#FFB6C1', '#8B0000'])
density_cmap = LinearSegmentedColormap.from_list('density', ['white', '#4169E1', '#00008B'])

# ===== ROW 1: Main Simulation Grids =====
# Plot 1: Resources
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(sim.resource_grid, cmap=resource_cmap, vmin=0, vmax=100, animated=True)
ax1.set_title('🌱 Resources', fontweight='bold', fontsize=11)
ax1.set_xticks([])
ax1.set_yticks([])
scatter1 = ax1.scatter([], [], c='black', s=15, marker='o', edgecolors='white', linewidth=0.3, alpha=0.7)
cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar1.set_label('Level', fontsize=8)

# Plot 2: Traffic/Congestion
ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(sim.traffic_grid, cmap=traffic_cmap, vmin=0, vmax=20, animated=True)
ax2.set_title('🚗 Traffic', fontweight='bold', fontsize=11)
ax2.set_xticks([])
ax2.set_yticks([])
scatter2 = ax2.scatter([], [], c='darkblue', s=12, marker='s', alpha=0.6)
cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
cbar2.set_label('Congestion', fontsize=8)

# Plot 3: Environmental Impact
ax3 = fig.add_subplot(gs[0, 2])
im3 = ax3.imshow(sim.environmental_factor_grid, cmap=env_cmap, vmin=0, vmax=100, animated=True)
ax3.set_title('☁️ Pollution', fontweight='bold', fontsize=11)
ax3.set_xticks([])
ax3.set_yticks([])
scatter3 = ax3.scatter([], [], c='lime', s=12, marker='^', alpha=0.7)
cbar3 = plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
cbar3.set_label('Impact', fontsize=8)

# ===== ROW 2: Analysis and Heatmaps =====
# Plot 4: Agent Density Heatmap
ax4 = fig.add_subplot(gs[1, 0])
density_grid = np.zeros((sim.height, sim.width))
im4 = ax4.imshow(density_grid, cmap=density_cmap, vmin=0, vmax=5, animated=True)
ax4.set_title('👥 Population Density', fontweight='bold', fontsize=11)
ax4.set_xticks([])
ax4.set_yticks([])
cbar4 = plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)
cbar4.set_label('Agents', fontsize=8)

# Plot 5: Efficiency Map (Resources/Traffic ratio)
ax5 = fig.add_subplot(gs[1, 1])
efficiency_cmap = LinearSegmentedColormap.from_list('efficiency', ['#FF0000', '#FFFF00', '#00AA00'])
im5 = ax5.imshow(np.zeros((sim.height, sim.width)), cmap=efficiency_cmap, vmin=0, vmax=10, animated=True)
ax5.set_title('⚡ Zone Efficiency', fontweight='bold', fontsize=11)
ax5.set_xticks([])
ax5.set_yticks([])
cbar5 = plt.colorbar(im5, ax=ax5, fraction=0.046, pad=0.04)
cbar5.set_label('Efficiency', fontsize=8)

# Plot 6: Resource Flow Vectors (simplified)
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_title('📊 Sector Health', fontweight='bold', fontsize=11)
ax6.set_xlim(-0.5, 3.5)
ax6.set_ylim(0, 100)
ax6.set_xticks([0, 1, 2, 3])
ax6.set_xticklabels(['North', 'South', 'East', 'West'], fontsize=9)
ax6.set_ylabel('Average Health', fontsize=9)
ax6.grid(True, alpha=0.3, axis='y')
bars = ax6.bar([0, 1, 2, 3], [50, 50, 50, 50], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'], alpha=0.7)

# ===== ROW 3: Metrics and Performance =====
# Plot 7: Key Metrics Over Time
ax7 = fig.add_subplot(gs[2, :2])
ax7.set_title('📈 Ecosystem Metrics', fontweight='bold', fontsize=11)
ax7.set_xlabel('Timestep', fontsize=9)
ax7.set_ylabel('Value', fontsize=9)
ax7.set_xlim(0, 500)
ax7.set_ylim(0, 100)
line_resources, = ax7.plot([], [], label='Avg Resources', color='green', linewidth=2, alpha=0.8)
line_traffic, = ax7.plot([], [], label='Traffic (normalized)', color='red', linewidth=2, alpha=0.8)
line_env, = ax7.plot([], [], label='Avg Pollution', color='purple', linewidth=2, alpha=0.8)
line_health, = ax7.plot([], [], label='System Health', color='blue', linewidth=2, alpha=0.8)
line_satisfaction, = ax7.plot([], [], label='Agent Satisfaction', color='orange', linewidth=2, alpha=0.8)
ax7.legend(loc='upper left', fontsize=9)
ax7.grid(True, alpha=0.3)

# Plot 8: Performance Stats
ax8 = fig.add_subplot(gs[2, 2])
ax8.axis('off')
stats_text = ax8.text(0.05, 0.95, '', transform=ax8.transAxes, fontsize=9,
                      verticalalignment='top', family='monospace',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# History tracking
history = {
    'timesteps': [],
    'resources': [],
    'traffic': [],
    'pollution': [],
    'health': [],
    'satisfaction': [],
    'stress': []
}

def calculate_system_health():
    """Calculate overall system health based on multiple factors"""
    avg_resources = np.mean(sim.resource_grid) / 100
    avg_pollution = 1 - (np.mean(sim.environmental_factor_grid) / 100)
    avg_traffic = 1 - (np.mean(sim.traffic_grid) / 20)
    
    # Weighted health score
    health = (avg_resources * 0.4 + avg_pollution * 0.3 + avg_traffic * 0.3) * 100
    return np.clip(health, 0, 100)

def calculate_sector_health(grid, height, width, num_sectors=4):
    """Divide map into 4 sectors and calculate health"""
    h_half = height // 2
    w_half = width // 2
    
    sectors = [
        grid[:h_half, :w_half],   # North-West
        grid[h_half:, :w_half],   # South-West
        grid[:h_half, w_half:],   # North-East
        grid[h_half:, w_half:]    # South-East
    ]
    
    return [np.mean(s) for s in sectors]

def update_frame(frame):
    sim.step()
    
    # Update resource grid
    resource_snapshot = sim.snapshot_resources()
    im1.set_array(resource_snapshot)
    
    # Get agent positions
    pos = sim.get_agent_positions()
    if pos:
        x_coords = np.array([p[0] for p in pos])
        y_coords = np.array([p[1] for p in pos])
        scatter1.set_offsets(np.c_[x_coords, y_coords])
        scatter2.set_offsets(np.c_[x_coords, y_coords])
        scatter3.set_offsets(np.c_[x_coords, y_coords])
    
    # Update traffic and environment
    traffic_snapshot = sim.snapshot_traffic()
    im2.set_array(traffic_snapshot)
    
    env_snapshot = sim.snapshot_environmental_factors()
    im3.set_array(env_snapshot)
    
    # Calculate and update density heatmap
    density_map = np.zeros((sim.height, sim.width))
    for x, y in pos:
        density_map[y, x] += 1
    im4.set_array(density_map)
    
    # Calculate efficiency map (resources / (traffic + 1))
    efficiency_map = resource_snapshot.astype(float) / (traffic_snapshot.astype(float) + 1)
    im5.set_array(efficiency_map)
    
    # Update sector health bars
    sector_health = calculate_sector_health(resource_snapshot, sim.height, sim.width)
    for bar, health in zip(bars, sector_health):
        bar.set_height(health)
    
    # Update metrics
    avg_resources = np.mean(resource_snapshot)
    total_traffic = np.sum(traffic_snapshot)
    avg_env = np.mean(env_snapshot)
    system_health = calculate_system_health()
    
    # Get satisfaction and stress
    avg_satisfaction = sim.get_agent_satisfaction()
    avg_stress = sim.get_agent_stress()
    
    history['timesteps'].append(sim.t)
    history['resources'].append(avg_resources)
    history['traffic'].append(total_traffic / max(len(sim.agents), 1))
    history['pollution'].append(avg_env)
    history['health'].append(system_health)
    history['satisfaction'].append(avg_satisfaction)
    history['stress'].append(avg_stress)
    
    # Update metrics graph
    if len(history['timesteps']) > 0:
        line_resources.set_data(history['timesteps'], history['resources'])
        line_traffic.set_data(history['timesteps'], history['traffic'])
        line_env.set_data(history['timesteps'], history['pollution'])
        line_health.set_data(history['timesteps'], history['health'])
        line_satisfaction.set_data(history['timesteps'], history['satisfaction'])
        ax7.set_xlim(0, max(500, len(history['timesteps'])))
    
    # Update stats
    stats_text.set_text(
        f'⏱️  Timestep: {sim.t}\n'
        f'👥 Agents: {len(sim.agents)}\n'
        f'🌱 Resources: {avg_resources:.1f}\n'
        f'🚗 Traffic: {int(total_traffic)}\n'
        f'☁️  Pollution: {avg_env:.1f}\n'
        f'💪 System Health: {system_health:.1f}%\n'
        f'😊 Satisfaction: {avg_satisfaction:.1f}%\n'
        f'😟 Stress: {avg_stress:.1f}%\n'
        f'{"─" * 20}\n'
        f'Status: {"🟢 Good" if system_health > 60 else "🟡 Fair" if system_health > 30 else "🔴 Critical"}'
    )
    
    return im1, im2, im3, im4, im5, scatter1, scatter2, scatter3, line_resources, line_traffic, line_env, line_health, line_satisfaction, stats_text

# Create smooth animation with reduced frame rate for performance
anim = FuncAnimation(fig, update_frame, frames=5000, interval=50, blit=True, repeat=False)

plt.show()
