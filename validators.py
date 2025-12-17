class EnergyTracker:
    def __init__(self, world):
        self.world = world
        self.initial_energy = world.get_total_energy()
        self.measurements = [self.initial_energy]

    def update(self):
        current = self.world.get_total_energy()
        self.measurements.append(current)

    def drift_percent(self):
        if self.initial_energy == 0:
            return 0
        current = self.measurements[-1]
        return abs(current - self.initial_energy) / self.initial_energy * 100

    def check_drift(self, max_percent=1.0):
        drift = self.drift_percent()
        if drift > max_percent:
            pass
           # print(f"WARNING: Energy drift {drift:.2f}%")
            return False
        return True


class MomentumTracker:
    def __init__(self, world):
        self.world = world
        self.initial_momentum = world.get_total_momentum()
        self.measurements = [self.initial_momentum]

    def update(self):
        current = self.world.get_total_momentum()
        self.measurements.append(current)

    def drift_magnitude(self):
        initial_mag = self.initial_momentum.length()
        if initial_mag == 0:
            return 0
        current = self.measurements[-1]
        current_mag = current.length()
        return abs(current_mag - initial_mag)

    def check_drift(self, max_magnitude=1e10):
        drift = self.drift_magnitude()
        if drift > max_magnitude:
            pass
            #print(f"WARNING: Momentum drift {drift:.2e}")
            return False
        return True
