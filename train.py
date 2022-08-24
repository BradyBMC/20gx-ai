import os
import argparse
import pickle
import dataset_tool
from threading import Thread, Lock

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

    def get_file(files):
        return next(files, None)

    def start_thread(mutex):
        while True:
            mutex.aquire()
            file = get_file()
            mutex.release()
            if file is None:
                break
            # May cause an issue with the adding
            res = dataset_tool.convert_datset(train_path=file, pkl_path=pkl_path, count = i)
            i += res

    assert os.path.isdir(path), 'Illegal path'
    assert os.path.isdir(pkl_path), 'Illegal pkl save destination'

    directory = os.fsencode(path)
    files = os.listdir(directory)
    for i in range(len(files)):
        files[i] = path + '/' + os.fsdecode(files[i])
        assert files[i].endswith('.slp'), 'Training set contains non .slp file' + files[i]

    files = iter(files)
    mutex = Lock()
    threads = []
    i = 0

    for i in range(os.cpu_count()):
        t = Thread(target=start_thread, args=(mutex))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    
#----------------------------------------------------------------------------


parser = argparse.ArgumentParser()

parser.add_argument('-data', help='Training data directory name', type=str)
parser.add_argument('-dest', help='Pickle directory name', type=str)

args = parser.parse_args()

multi_config(args.data, args.dest)

#----------------------------------------------------------------------------

def main():
    print('Hello World')
    
if __name__ == '__main__':
    main()