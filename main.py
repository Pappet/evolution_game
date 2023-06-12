import random
import time
import keyboard


class World:
    def __init__(self, width, height):
        self.organisms = []
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]

    def is_empty(self, x, y):
        return not any(organism.x == x and organism.y == y for organism in self.organisms)

    def get_empty_neighbors(self, x, y):
        neighbors = [(nx, ny) for nx in range(x-1, x+2) for ny in range(y-1, y+2)
                     if 0 <= nx < self.width and 0 <= ny < self.height and not (nx == x and ny == y)]
        return [(nx, ny) for (nx, ny) in neighbors if self.is_empty(nx, ny)]

    def add_organism(self, organism):
        self.organisms.append(organism)

    def remove_organism(self, organism):
        self.organisms.remove(organism)

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                for organism in self.organisms:
                    if organism.x == x and organism.y == y:
                        if isinstance(organism, Herbivore):
                            print('H', end=' ')
                        elif isinstance(organism, Carnivore):
                            print('C', end=' ')
                        break
                else:
                    print('.', end=' ')
            print()
        print()

    def move_organisms(self):
        for organism in self.organisms:
            organism.move(self)

    def reproduce_organisms(self):
        new_organisms = [organism.reproduce(self)
                         for organism in self.organisms]
        self.organisms.extend(
            new_organism for new_organism in new_organisms if new_organism is not None)

    def remove_dead_organisms(self):
        self.organisms = [
            organism for organism in self.organisms if organism.age < organism.lifespan]

    def evolve_organisms(self):
        # Define rules for evolution and mutation
        pass


class Organism:
    def __init__(self, health, speed, strength, reproduction_rate, lifespan, x, y):
        self.health = health
        self.speed = speed
        self.strength = strength
        self.reproduction_rate = reproduction_rate
        self.lifespan = lifespan
        self.x = x
        self.y = y
        self.age = 0

    def move(self, world):
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        new_x = max(0, min(self.x + dx, world.width - 1))
        new_y = max(0, min(self.y + dy, world.height - 1))
        if world.is_empty(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def age_one_step(self):
        self.age += 1

    def eat(self, world):
        # Code to determine how the organism eats
        pass

    def reproduce(self, world):
        if random.random() < self.reproduction_rate:
            empty_neighbors = world.get_empty_neighbors(self.x, self.y)
            if empty_neighbors:
                new_x, new_y = random.choice(empty_neighbors)
                return self.__class__(self.health, self.speed, self.strength, self.reproduction_rate, self.lifespan, new_x, new_y, self.hunger_decrement)
        return None


class Carnivore(Organism):
    def __init__(self, health, speed, strength, reproduction_rate, lifespan, x, y, hunger_decrement):
        super().__init__(health, speed, strength, reproduction_rate, lifespan, x, y)
        self.hunger_decrement = hunger_decrement

    def eat(self, world):
        prey = [organism for organism in world.organisms if isinstance(
            organism, Herbivore)]
        nearby_prey = [organism for organism in prey
                       if abs(organism.x - self.x) <= self.speed and abs(organism.y - self.y) <= self.speed]

        if nearby_prey:
            victim = random.choice(nearby_prey)
            world.organisms.remove(victim)
            self.health += victim.health
        else:
            self.health -= self.hunger_decrement


class Herbivore(Organism):
    def __init__(self, health, speed, strength, reproduction_rate, lifespan, x, y, hunger_decrement):
        super().__init__(health, speed, strength, reproduction_rate, lifespan, x, y)
        self.hunger_decrement = hunger_decrement


class Simulation:
    def __init__(self, world):
        self.world = world
        self.running = True
        self.paused = False
        self.step = False

        # Press 'p' to pause/unpause
        keyboard.add_hotkey('p', self.toggle_pause)
        # Press 's' to step
        keyboard.add_hotkey('s', self.do_step)

    def toggle_pause(self):
        self.paused = not self.paused

    def do_step(self):
        self.step = True

    def run(self):
        while self.running:
            if not self.paused or self.step:
                for organism in self.world.organisms:
                    organism.age_one_step()
                    organism.eat(self.world)
                self.world.remove_dead_organisms()
                self.world.reproduce_organisms()
                self.world.move_organisms()
                self.world.display()
                self.step = False  # Reset step flag
            time.sleep(0.5)


def main():
    world = World(10, 10)
    world.add_organism(Herbivore(10, 1, 2, 0.1, 20, 10, 10, 0.2))
    world.add_organism(Carnivore(15, 2, 3, 0.05, 15, 0, 0, 0.2))

    simulation = Simulation(world)
    simulation.run()


if __name__ == "__main__":
    main()
