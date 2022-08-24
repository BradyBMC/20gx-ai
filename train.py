import os
import argparse
import pickle
import dataset_tool

#----------------------------------------------------------------------------

def config(
    path: str, 
    pkl_path: str
):
    assert os.path.isdir(pkl_path), 'Illegal pkl save destination'

    if os.path.isdir(path):
        directory = os.fsencode(path)
        i = 0
        for file in os.listdir(directory):
            filename = path + '/' + os.fsdecode(file)
            assert filename.endswith('.slp'), 'Contains non .slp files: ' + filename
            dataset_tool.convert_dataset(train_path=filename, pkl_path=pkl_path, count=i)
            i+=1
    else:
        raise Exception('Illegal path')
    return None





#----------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-data', help='Training data directory name', type=str)
parser.add_argument('-dest', help='Pickle directory name', type=str)

args = parser.parse_args()

config(args.data, args.dest)






#----------------------------------------------------------------------------

def main():
    print('Hello World')
    
if __name__ == '__main__':
    main()