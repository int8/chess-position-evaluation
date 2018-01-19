## Experimental chess position evaluation project

The goal of this project is to evaluate chess position with machine learning

Current code in repository transforms PGN files into
- tensors of size ```6x8x8``` and ```12x8x8```, ```8x8``` represents board itself while    ```6``` and ```12``` represent depth of tensor. For ```depth = 6``` each piece is placed in one of 6 dimensions (as we have 6 types of pieces) with values ```1``` or ```-1``` indicating the piece color. In case of ```depth = 12``` each piece is placed in one of 12 dimensions (6 black + 6 white pieces) with one value = ```1```.
In other words every piece on ```8x8``` board is represented by vector of dimensionality ```6``` or ```12``` (depending what board representation is chosen) in a 'bag of words' fashion.


- flat vectors of size ```384 (6*8*8)``` and ```768 (12*8*8)``` being flattened versions of tensor described above

- position metadata (result, number_of_moves, castlings potential) is inlcuded

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
from common.readers import PgnReader as reader
from common.io import FileSystemDataSaverWithShuffling as saver
from common.transformations import DataSpecs

# memory_size indicates how many prev moves to keep
with reader("data.pgn", memory_size = 5) as r, saver('output', chunk_size = 5000, number_of_buckets=50) as s:
    for position in iter(r):
        # if you don't want to include draws in your dataset
        if position['current'].draw():
            continue
        black_to_move = position['current'].black_to_move
        # flipping board instead of encoding who moves next - board always seen from white perspective
        current_data = position['current'].get_training_data(DataSpecs.vector12x8x8_flat, flip = black_to_move)
        prev_data = [prev.get_training_data(flip = black_to_move) for prev in position['prev']]
        s.insert_next({'current': current_data, 'prev_positions': prev_data})
```


To later use tensor-like data to train chess value network:
```python
from common.io import FlatVector6x8x8PositionReader
from common.models import FeedForwardNetwork
from training.trainers import ValueNetworkTrainer
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

# training data reader - reads previously created data files
training_data_reader = FlatVector6x8x8PositionReader("data_dir", number_of_files_in_memory = 10, batch_size = 1000)

# create dense feed forward neural network
network = FeedForwardNetwork(
    layers_shapes = [(6*8*8, 5000), (5000,500), (500,50), (50, 1)],
    activations = [F.leaky_relu, F.leaky_relu, F.leaky_relu, F.sigmoid]
)

optimizer = optim.Adam(network.parameters(), lr=0.0001)

trainer = ValueNetworkTrainer(
    training_data_reader = training_data_reader,
    model = network, # network itself
    loss_function = F.mse_loss, # mean square error loss
    x_tensorize_f = lambda x : Variable(x), # in case you need additional transformation
    y_tensorize_f = lambda x : Variable(x), # in case you need additional transformation
    optimizer = optimizer, # adam optimizer
    use_cuda = False # set to true to run on CUDA
)

# train 10 epochs
for epoch in range(0,10):    
    trainer.train_single_epoch()
    # save after each epoch
    trainer.save_model_state(prefix = 'epoch_' + str(epoch) + '_')
```
To run tests try:

```bash
py.test -v tests/
```
