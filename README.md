## Experimental chess position evaluation project

The goal of this project is to evaluate chess position with machine learning

Current code in repository transforms PGN files into tensors of size ```6x8x8``` and ```12x8x8```, ```8x8``` represents board itself while    ```6``` and ```12``` represent depth of tensor. For ```depth = 6``` each piece is placed in one of 6 dimensions (as we have 6 types of pieces) with values ```1``` or ```-1``` indicating the piece color. In case of ```depth = 12``` each piece is placed in one of 12 dimensions (6 black + 6 white pieces) with one value = ```1```.

In other words every piece on ```8x8``` board is represented by vector of dimensionality ```6``` or ```12``` (depending what board representation is chosen) in a 'bag of words' fashion.


Requirements:
```
numpy>=1.12.0
python-chess>=0.22.0
torch>=0.3.0.post4
torchvision>=0.2.0
pytest>=3.3.1
```

To install requirements run:
```bash
pip install -r requirements.txt
```

To translate PGN file into tensor-like data (coordinates and values of non-zero tensor entries + game metadata):

```python
from common.readers import PgnReader as data_reader
from common.io import FileSystemDataSaverWithShuffling as data_saver

with data_reader("data.pgn") as reader, data_saver('output', chunk_size = 8000) as saver:
    for position in iter(reader):
        black_to_move = position['current'].black_to_move
        current_tensor = position['current'].get_tensor(flip = black_to_move)
        prev_tensors = [prev.get_tensor(flip = black_to_move) for prev in position['prev']]
        saver.insert_next({'current': current_tensor, 'prev_positions': prev_tensors})
```


To later use tensor-like data in pytorch you can start with:
```python
from common.io import TensorPositionReader as tensor_reader
t = tensor_reader("output", number_of_files_in_memory = 10, batch_size = 100)
for position in iter(t):
    do_something_with(position['X'], position['Y'])
    # position holds training data now
    # shape of position['X'] (observations) is 100 x 6 x 6 x 8
    # length of position['Y'] (labels) is 100
```
To run tests try:

```bash
py.test -v tests/
```
