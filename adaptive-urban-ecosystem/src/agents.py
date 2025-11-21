# src/agents.py
from __future__ import annotations
import random
from typing import Tuple, List, Any, Dict
import numpy as np
from collections import deque

class Agent:
    """Base agent: has position, id, and a simple step() interface."""
    _next_id = 1

    def __init__(self, x: int, y: int):
        self.id = Agent._next_id
        Agent._next_id += 1
        self.x = x
        self.y = y

    def step(self, world) -> None:
        """Override in subclasses to implement behavior each tick."""
        raise NotImplementedError

    def pos(self) -> Tuple[int,int]:
        return (self.x, self.y)


class Person(Agent):
    """
    Simple mobile agent:
    - Moves to a random neighbor cell (von Neumann or 8-neighbors if you prefer).
    - Forages: eats a small amount of resource on current cell.
    - If resource is zero, moves more aggressively.
    """
    def __init__(self, x:int, y:int, forage_amount:int=5, vision:int=1):
        super().__init__(x,y)
        self.forage_amount = forage_amount
        self.vision = vision  # look range for resource bias

    def step(self, world) -> None:
        h, w = world.height, world.width

        # Look for best neighbor within vision (simple greedy)
        best = (self.x, self.y)
        best_val = world.resources[self.y, self.x]

        # explore neighbor cells in square of radius = vision
        for dy in range(-self.vision, self.vision + 1):
            for dx in range(-self.vision, self.vision + 1):
                nx, ny = self.x + dx, self.y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h:
                    continue
                val = world.resources[ny, nx]
                # small random jitter to break ties & add variability
                val += random.random() * 0.001
                if val > best_val:
                    best_val = val
                    best = (nx, ny)

        # move towards chosen cell (may be current cell)
        self.x, self.y = best

        # forage: reduce resource at current location
        # ensure we don't go negative
        current = int(world.resources[self.y, self.x])
        taken = min(self.forage_amount, current)
        world.resources[self.y, self.x] = current - taken

        # Optionally: when starving (no resources around) randomly teleport small chance
        if best_val <= 0 and random.random() < 0.01:
            self.x = random.randint(0, w - 1)
            self.y = random.randint(0, h - 1)


class AdvancedAgent:
    """Enhanced agent with memory, learning, and adaptive behavior"""

    def __init__(self, x, y, forage_amount, vision, agent_id=0):
        self.x = x
        self.y = y
        self.resources = 0
        self.forage_amount = forage_amount
        self.vision = vision
        self.agent_id = agent_id

        # Memory and learning
        self.memory = deque(maxlen=50)  # Recent experiences
        self.preference_weights = {
            'resources': 1.0,
            'traffic': -2.0,
            'pollution': -0.5,
            'comfort': 0.3,  # Prefer less crowded areas
            'familiarity': 0.2  # Learn preferred routes
        }

        # Personality traits (vary per agent)
        self.personality = {
            'risk_tolerance': random.uniform(0.3, 1.0),      # 0.3 = cautious, 1.0 = adventurous
            'exploration': random.uniform(0.2, 1.0),          # 0.2 = routine, 1.0 = explorer
            'social': random.uniform(0.1, 1.0),               # 0.1 = loner, 1.0 = social
            'efficiency': random.uniform(0.3, 1.0),           # 0.3 = lazy, 1.0 = efficient
        }

        # Goal and state
        self.current_goal = None
        self.goal_memory = {}  # Remember successful locations
        self.energy = 100
        self.max_energy = 100
        self.stress_level = 0
        self.satisfaction = 50

        # Movement history for pattern learning
        self.visited_cells = deque(maxlen=100)
        self.move_count = 0

    def add_memory(self, location, resource_level, traffic_level, outcome):
        """Store experience in memory"""
        self.memory.append({
            'location': location,
            'resources': resource_level,
            'traffic': traffic_level,
            'outcome': outcome,
            'timestep': self.move_count
        })

        # Update goal memory if good outcome
        if outcome > 50:
            if location not in self.goal_memory:
                self.goal_memory[location] = 0
            self.goal_memory[location] += 1

    def _get_vision_neighborhood(self, x, y, resource_grid, traffic_grid, env_grid, width, height):
        """Get all cells within vision range"""
        candidates = []

        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                nx = (x + dx) % width
                ny = (y + dy) % height

                distance = np.sqrt(dx**2 + dy**2)
                if distance <= self.vision:
                    candidates.append({
                        'pos': (nx, ny),
                        'distance': distance,
                        'resources': resource_grid[ny, nx],
                        'traffic': traffic_grid[ny, nx],
                        'pollution': env_grid[ny, nx]
                    })

        return candidates

    def choose_next_move(self, resource_grid, traffic_grid, environmental_grid, width, height):
        """Advanced decision-making with learning and personality"""

        # Get visible candidates
        candidates = self._get_vision_neighborhood(
            self.x, self.y, resource_grid, traffic_grid, environmental_grid, width, height
        )

        best_score = -np.inf
        best_moves = []

        for candidate in candidates:
            nx, ny = candidate['pos']

            # Calculate multi-factor score based on personality
            score = self._calculate_move_score(
                candidate,
                (nx, ny),
                self.personality,
                self.preference_weights
            )

            if score > best_score:
                best_score = score
                best_moves = [(nx, ny)]
            elif score == best_score:
                best_moves.append((nx, ny))

        # Apply exploration behavior
        if random.random() < self.personality['exploration'] * 0.1:
            target = random.choice(candidates)['pos']
        else:
            target = random.choice(best_moves)

        # Update energy and stress
        self._update_internal_state(resource_grid[target[1], target[0]],
                                   traffic_grid[target[1], target[0]])

        return target

    def _calculate_move_score(self, candidate, target_pos, personality, weights):
        """Calculate score with personality modulation"""

        resources = candidate['resources']
        traffic = candidate['traffic']
        pollution = candidate['pollution']
        distance = candidate['distance']

        # Base scoring
        score = 0
        score += resources * weights['resources']
        score -= traffic * weights['traffic'] * personality['risk_tolerance']
        score -= pollution * weights['pollution']
        score -= distance * 0.5  # Prefer closer moves

        # Social preference (avoid/seek crowding)
        if personality['social'] > 0.6:
            score -= traffic * 0.1  # Less penalty for traffic (likes crowds)
        else:
            score -= traffic * 0.5  # More penalty for traffic (avoids crowds)

        # Familiarity bonus
        if target_pos in self.goal_memory:
            score += self.goal_memory[target_pos] * weights['familiarity']

        # Efficiency bonus
        if resources > 0:
            efficiency_boost = personality['efficiency'] * resources
            score += efficiency_boost

        return score

    def _update_internal_state(self, resources_at_location, traffic_at_location):
        """Update agent's internal state"""

        # Energy management
        self.energy -= traffic_at_location * 0.1  # Traffic drains energy
        self.energy = max(0, min(self.max_energy, self.energy))

        # Stress from congestion
        self.stress_level += traffic_at_location * 0.05
        self.stress_level = max(0, min(100, self.stress_level))

        # Satisfaction from resources
        if resources_at_location > 0:
            self.satisfaction = min(100, self.satisfaction + resources_at_location * 0.1)
        else:
            self.satisfaction = max(0, self.satisfaction - 2)

        # Stress recovery in quiet areas
        if traffic_at_location < 5:
            self.stress_level = max(0, self.stress_level - 1)

    def move_to(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.visited_cells.append((new_x, new_y))
        self.move_count += 1

    def adapt_preferences(self, reward):
        """Learn from success/failure"""
        learning_rate = 0.01

        if reward > 0:
            # Increase successful strategy weights
            self.preference_weights['resources'] += learning_rate
            self.preference_weights['traffic'] -= learning_rate * 0.5
            self.personality['efficiency'] = min(1.0, self.personality['efficiency'] + learning_rate * 0.5)
        else:
            # Decrease unsuccessful weights
            self.preference_weights['resources'] -= learning_rate * 0.5
            self.personality['risk_tolerance'] = max(0.3, self.personality['risk_tolerance'] - learning_rate)
