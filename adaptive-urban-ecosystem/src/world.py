# src/world.py
import os
import csv
import random
from typing import Tuple, List

import numpy as np  # we installed this already

class World:
    def __init__(self, width: int = 500, height: int = 500, seed: int | None = None):
        self.width = width
        self.height = height
        self.rng = np.random.default_rng(seed)
        # resource grid: integer levels 0..100
        self.resources = self.rng.integers(low=20, high=101, size=(height, width)).astype(int)
        self.timestep = 0
        self.log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "world_log.csv")
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        # create CSV header
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestep", "avg_resource", "min_resource", "max_resource"])

    def step(self, decay_rate: float = 0.02, regen_chance: float = 0.2, regen_amount: Tuple[int,int]=(5,20)):
        """
        Advance the world by one timestep.
        - decay_rate: fraction of resource to remove per tick (applied multiplicatively)
        - regen_chance: probability per cell to regenerate some amount
        - regen_amount: (min,max) integer to add when regen happens
        """
        self.timestep += 1

        # decays: multiplicative decay then floor to int
        decay_factor = 1.0 - decay_rate
        self.resources = np.floor(self.resources * decay_factor).astype(int)

        # random regeneration events
        # create boolean mask of cells that regenerate this tick
        regen_mask = self.rng.random(self.resources.shape) < regen_chance
        if regen_mask.any():
            # sample integer regeneration amounts
            regen_vals = self.rng.integers(regen_amount[0], regen_amount[1] + 1, size=self.resources.shape)
            self.resources = np.where(regen_mask, self.resources + regen_vals, self.resources)

        # clamp between 0 and 100
        np.clip(self.resources, 0, 100, out=self.resources)

        # log summary
        avg_r = float(self.resources.mean())
        min_r = int(self.resources.min())
        max_r = int(self.resources.max())
        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.timestep, f"{avg_r:.3f}", min_r, max_r])

        return {"timestep": self.timestep, "avg": avg_r, "min": min_r, "max": max_r}

    def get_snapshot(self) -> List[List[int]]:
        """Return a nested list snapshot of the resource grid (for visualization)."""
        return self.resources.tolist()

    def save_grid_png(self, path: str):
        """Save a quick heatmap PNG (requires matplotlib)."""
        import matplotlib.pyplot as plt

        plt.imshow(self.resources, vmin=0, vmax=100)
        plt.colorbar(label="Resource level")
        plt.title(f"World resources @ t={self.timestep}")
        plt.tight_layout()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()
