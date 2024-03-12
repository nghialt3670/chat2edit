BASE_PROGRAM_1 = \
"""
Available functions:
def find(image: Image, prompt: str) -> Entity
def info(image: Image, category: Literal['size', 'color', 'position'], entity: Entity) -> Union[Size, Color, Position]
def generate(category: Literal['image', 'object', 'text'], prompt: str) -> Union[Image, Entity]
def remove(image: Image, target: Entity, fill: bool = True) -> Image
def insert(image: Image, entity: Entity, size: Optional[Size] = None, position: Optional[Position] = None) -> Image
def replace(image: Image, target: Entity, replacement: Entity) -> Image
def move(image: Image, target: Entity, distance: int, direction: Literal['left', 'right', 'up', 'down']) -> Image
def swap(image: Image, entity1: Entity, entity2: Entity) -> Image
def scale(image: Image, category: Literal['brightness', 'contrast', 'smoothness', 'temperature', 'saturation', 'blurness', 'sharpness', 'detail'], factor: float, target: Optional[Entity] = None) -> Image
def rotate(image: Image, angle: float, direction: Literal['clockwise', 'counter-clockwise'] = 'clockwise', target: Optional[Entity] = None) -> Image
def flip(image: Image, direction: Literal['vertical', 'horizontal'] = 'horizontal', target: Optional[Entity] = None) -> Image
def zoom(image: Image, factor: float, target: Optional[Entity] = None) -> Image


Write the function for this instruction: "{instruction}"
def process_image(image: Image) -> Image:
    # Your code here
"""

BASE_PROGRAM_2 = \
"""
class Image:
    def find(self, target: str) -> Entity
    def resize(self, target: Entity, size: Size) -> Image
    def remove(self, target: Entity) -> Image
    def insert(self, entity: Entity) -> Image
    def replace(self, old: Entity, new: Entity) -> Image
    def move(self, target: entity, x_offset: int, y_offset: int) -> None
    def swap(entity1: Entity, entity2: Entity) -> None
    def rotate(angle: float, direction: Literal['cw', 'ccw'], target: Optional[Entity] = None) -> None
    def flip(direction: Literal['vertical', 'horizontal'], target: Optional[Entity] = None) -> None
    def zoom(percent: float, target: Entity) -> None
    def convert(category: Literal['grayscale', 'negative'], target: Optional[Entity] = None) -> Npne


Write the function for this instruction: "{instruction}"
def process_image(image: Image) -> Image:
    # Your code here
     
"""
