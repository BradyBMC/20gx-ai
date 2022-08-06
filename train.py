import os
import argparse


def config(path: str):
    # if path == slp load data and return
    # if path == directory load all data and return
    # if neither throw error
    assert os.path.isdir(path)
    return None

parser = argparse.ArgumentParser()

parser.add_argument('-data', '--data', help='Training data', type=str)
parser.add_argument('-s', '--size', help='Size', type=int)

args = parser.parse_args()

config(args.data)

def main():
    print(args.size)
    
if __name__ == '__main__':
    main()