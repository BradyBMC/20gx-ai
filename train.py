import os
import argparse
import pickle
import dataset_tool



#----------------------------------------------------------------------------

def config(path: str):
    if os.path.isdir(path):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = path + '/' + os.fsdecode(file)
            assert filename.endswith('.slp'), 'Contains non .slp files: ' + filename
            print(filename)
            dataset_tool.convert_dataset(train_dir=filename)
    else:
        raise Exception('Illegal path')
    return None





#----------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-data', help='Training data directory name', type=str)
parser.add_argument('-dest', help='Pickle directory name', type=str)

args = parser.parse_args()

config(args.data)






#----------------------------------------------------------------------------

def main():
    print('Hello World')
    
if __name__ == '__main__':
    main()