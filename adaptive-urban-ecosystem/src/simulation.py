import numpy as np
import random
from agents import AdvancedAgent

class Simulation:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        self.t = 0
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        self.resource_grid = np.random.randint(0, 101, size=(height, width), dtype=np.int32)
        self.MAX_RESOURCE_CAPACITY = 100

        self.general_resource_grid = np.full((height, width), 50, dtype=np.int32)

        self.traffic_grid = np.zeros((height, width), dtype=np.int32)
        self.MAX_TRAFFIC_CAPACITY = 20
        self.traffic_decay_rate = 0.1

        self.environmental_factor_grid = np.zeros((height, width), dtype=np.int32)
        self.MAX_ENVIRONMENTAL_FACTOR_CAPACITY = 100
        self.environmental_decay_rate = 0.05

        self.agents = []

        self.resource_history = []
        self.traffic_history = []
        self.environmental_history = []
        self.satisfaction_history = []
        self.stress_history = []

        self.use_ml_decisions = True
        self.learning_rate = 0.01

    def populate_random_people(self, n, forage_amount, vision):
        for i in range(n):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.agents.append(AdvancedAgent(x, y, forage_amount, vision, agent_id=i))

    def _update_resources_depletion_and_dilation(self):
        new_resource_grid = self.resource_grid.copy()
        dilation_rate = 0.07

        for y in range(self.height):
            for x in range(self.width):
                current_resources = self.resource_grid[y, x]
                if current_resources > 0:
                    dilated_amount = int(current_resources * dilation_rate)
                    if dilated_amount == 0 and current_resources > 0:
                        dilated_amount = 1

                    new_resource_grid[y, x] -= dilated_amount

                    neighbors = []
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = (x + dx) % self.width, (y + dy) % self.height
                            neighbors.append((ny, nx))

                    if neighbors:
                        per_neighbor_dilation = dilated_amount // len(neighbors)
                        for ny, nx in neighbors:
                            new_resource_grid[ny, nx] = min(self.MAX_RESOURCE_CAPACITY, new_resource_grid[ny, nx] + per_neighbor_dilation)

        self.resource_grid = new_resource_grid

    def _regenerate_resources(self):
        regeneration_amount = 1
        for y in range(self.height):
            for x in range(self.width):
                self.resource_grid[y, x] = min(self.MAX_RESOURCE_CAPACITY, self.resource_grid[y, x] + regeneration_amount)

    def _update_traffic_dynamics(self):
        self.traffic_grid = (self.traffic_grid * (1 - self.traffic_decay_rate)).astype(np.int32)
        self.traffic_grid = np.clip(self.traffic_grid, 0, self.MAX_TRAFFIC_CAPACITY)

    def _update_environmental_factors(self):
        agent_density_effect = np.zeros_like(self.environmental_factor_grid, dtype=np.int32)
        for agent in self.agents:
            agent_density_effect[agent.y, agent.x] += 1

        self.environmental_factor_grid = self.environmental_factor_grid + agent_density_effect
        self.environmental_factor_grid = (self.environmental_factor_grid * (1 - self.environmental_decay_rate)).astype(np.int32)
        self.environmental_factor_grid = np.clip(self.environmental_factor_grid, 0, self.MAX_ENVIRONMENTAL_FACTOR_CAPACITY)

    def get_agent_positions(self):
        """Return list of (x, y) positions for all agents"""
        return [(agent.x, agent.y) for agent in self.agents]

    def get_agent_satisfaction(self):
        """Return average satisfaction"""
        return np.mean([agent.satisfaction for agent in self.agents]) if self.agents else 0

    def get_agent_stress(self):
        """Return average stress"""
        return np.mean([agent.stress_level for agent in self.agents]) if self.agents else 0

    def step(self):
        traffic_perception_grid = self.traffic_grid.copy()

        for agent in self.agents:
            if self.resource_grid[agent.y, agent.x] > 0:
                consumption = min(agent.forage_amount, self.resource_grid[agent.y, agent.x])
                agent.resources += consumption
                self.resource_grid[agent.y, agent.x] -= consumption

            target_x, target_y = agent.choose_next_move(
                self.resource_grid,
                traffic_perception_grid,
                self.environmental_factor_grid,
                self.width,
                self.height
            )

            agent.move_to(target_x, target_y)
            self.traffic_grid[agent.y, agent.x] += 1

        self._update_resources_depletion_and_dilation()
        self._regenerate_resources()
        self._update_traffic_dynamics()
        self._update_environmental_factors()

        # Agents learn from their experiences
        if self.use_ml_decisions:
            self._apply_ml_feedback()

        self.resource_history.append(np.mean(self.resource_grid))
        self.traffic_history.append(np.sum(self.traffic_grid))
        self.environmental_history.append(np.mean(self.environmental_factor_grid))
        self.satisfaction_history.append(self.get_agent_satisfaction())
        self.stress_history.append(self.get_agent_stress())

        self.t += 1

    def _apply_ml_feedback(self):
        """Apply reinforcement learning to improve agent behavior"""
        for agent in self.agents:
            # Calculate reward based on satisfaction and resource acquisition
            reward = agent.satisfaction - agent.stress_level + (agent.resources * 0.05)
            
            # Adapt agent preferences
            agent.adapt_preferences(reward)

    def snapshot_resources(self):
        return self.resource_grid.copy()

    def snapshot_traffic(self):
        return self.traffic_grid.copy()

    def snapshot_environmental_factors(self):
        return self.environmental_factor_grid.copy()
