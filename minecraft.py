from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# A list to store all our block entities
blocks = []

class Brick(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.lime,
        )
    
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                # Spawn a new block adjacent to the clicked face
                new_brick = Brick(position=self.position + mouse.normal)
                blocks.append(new_brick)
                
            if key == 'left mouse down':
                # Remove the clicked block
                blocks.remove(self)
                destroy(self)

# Generate a small flat floor of blocks
for z in range(10):
    for x in range(10):
        brick = Brick(position=(x, 0, z))
        blocks.append(brick)

# Add a first-person character (WASD to move, Space to jump, Mouse to look)
player = FirstPersonController()

app.run()