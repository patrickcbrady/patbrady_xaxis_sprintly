from typing import NamedTuple, List, Dict, Tuple
from collections import Counter, deque
import utils.core.utils as U
DATA_DIR = './'


def read_input_data(filename: str):
    data = open(f'{DATA_DIR}/{filename}', 'r').read()
    return str(data)


class ImageLayer(NamedTuple):
    image: str
    width: int
    height: int

    def render(self):
        table = {
            '0': ' ',
            '1': str('\u2588'),
            '2': '2 '
        }
        res = ''.join([table[char] for char in self.image])
        head = 0
        rows = []
        while head <= len(self.image) - self.width:
            end = head + self.width
            rows.append(res[head:end])
            head = end
        print('\n'.join(rows))


class DSNImage(NamedTuple):
    layers: List[ImageLayer]

    @U.timer
    def flatten(self) -> ImageLayer:
        first_layer = self.layers[0]
        width = first_layer.width
        height = first_layer.height
        num_layers = len(self.layers)
        print(f'Image has {num_layers} layers')
        if num_layers < 2:
            return ImageLayer(first_layer.image, width, height)

        res = list(first_layer.image)
        transparent_positions = deque([idx for idx, char in enumerate(res) if char == '2'])
        for layer_idx in range(1, num_layers):
            pixel_count = len(transparent_positions)
            if pixel_count == 0:
                break
            layer_str = self.layers[layer_idx].image
            for i in range(0, pixel_count):
                pixel_idx = transparent_positions.popleft()
                pixel = layer_str[pixel_idx]
                if pixel == '2':
                    transparent_positions.append(pixel_idx)
                else:
                    res[pixel_idx] = pixel

        return ImageLayer(''.join(res), width, height)


class DSNDecoder:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def decode_image(self, image: str) -> DSNImage:
        img_len = len(image)
        return DSNImage([ImageLayer(image[i:i+self.width*self.height], self.width, self.height)
                         for i in range(0, img_len, self.width*self.height)])


def test_part_1():
    decoder = DSNDecoder(3, 2)
    data = '123456789012'
    image = decoder.decode_image(data)
    for idx, layer in enumerate(image.layers):
        print(f'Layer {idx}: {layer}')


def part_1():
    image_str = read_input_data('day_8_input')
    decoder = DSNDecoder(25, 6)
    image = decoder.decode_image(image_str)
    least_zeroes = None
    min_zeroes = float('inf')
    for idx, layer in enumerate(image.layers):
        num_count = Counter(layer.image)
        prev_min = min_zeroes
        min_zeroes = min(num_count.get('0', 0), min_zeroes)
        if min_zeroes < prev_min:
            least_zeroes = num_count
            print(f'Layer {idx} has the least zeroes so far')

    print(f'number of 1 digits: {least_zeroes["1"]}\nnumber of 2 digits: {least_zeroes["2"]}\n'
          f'product: {least_zeroes["1"] * least_zeroes["2"]}')


def test_part_2():
    data = '0222112222120000'
    DSNDecoder(2, 2).decode_image(data).flatten().render()


def part_2():
    data = read_input_data('day_8_input')
    DSNDecoder(25, 6).decode_image(data).flatten().render()


def __main():
    test_part_1()
    part_1()
    test_part_2()
    part_2()


if __name__ == '__main__':
    __main()
