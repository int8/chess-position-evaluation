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
```

To install requirements run:
```
pip install -r requirements.txt
```

Simple example of how to use the code:

```
i = iter(PgnReader("data/yourpgnfile.pgn"))
try:
    with DataSaverWithShuffling(output_dir='output') as saver:        
        while(True):
            position = next(i)
            transformer = Position2SparseRepresentation()
            obj = transformer.transform_position_with_context(position)
            saver.insert_next(obj)            
except StopIteration as error:
    pass
```
