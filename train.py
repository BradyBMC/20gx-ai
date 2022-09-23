import os
import argparse
import pickle
import dataset_tool
from threading import Thread, Lock
from multiprocessing import Process

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
            res = dataset_tool.convert_dataset(train_path=filename, pkl_path=pkl_path, count=i)
            i += res
    else:
        raise Exception('Illegal path')
    return None

#----------------------------------------------------------------------------

def multi_config(
    path: str,
    pkl_path: str
):
    global COUNT
    COUNT = 0
    
    def get_file():
        return next(files, None)
    
    def gf(i):
        if i == 0:
            return next(f1, None)
        else:
            return next(f2, None)
    
    def start_thread(x):
        while True:
            global COUNT
            file = gf(x)
            # mutex.acquire()
            # file = get_file()
            # mutex.release()
            if file is None:
                break
            # May cause an issue with the adding
            res = dataset_tool.convert_dataset(train_path=file, pkl_path=pkl_path, count = COUNT)
            COUNT = COUNT + res

    assert os.path.isdir(path), 'Illegal path'
    assert os.path.isdir(pkl_path), 'Illegal pkl save destination'

    directory = os.fsencode(path)
    files = os.listdir(directory)
    for j in range(len(files)):
        files[j] = path + '/' + os.fsdecode(files[j])
        assert files[j].endswith('.slp'), 'Training set contains non .slp file' + files[j]

    f1 = files[:int(len(files)/2)]
    f2 = files[int(len(files)/2):]
    f1 = iter(f1)
    f2 = iter(f2)
        
    files = iter(files)
    mutex = Lock()
    threads = []

    # for k in range(os.cpu_count()):
    for x in range(2):
        # t = Thread(target=start_thread)
        t = Process(target=start_thread,args=0)
        t = Process(target=start_thread,args=1)
        threads.append(t)
        t.start()
        break

    for t in threads:
        t.join()

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