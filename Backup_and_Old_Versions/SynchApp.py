
import time

def getInf(i,t):
    time.sleep(t)
    print(f'task {i} done')

def main():

    # times = [1,2,3]
    times = [.5,1,2]
    start = time.time()
    for i,t in enumerate(times):
        getInf(i+1,t)

    end = time.time()
    print(f'Time taken: {end-start}')

if __name__ == '__main__':
    main()
