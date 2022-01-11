import threading
import time


def load_data(name):
    print('Downloading...')
    time.sleep(2)
    print(f'{name} download!')


start = time.perf_counter()
print('Start proccess')

thread1 = threading.Thread(target=load_data, args=['data1'])
thread2 = threading.Thread(target=load_data, args=['data2'])
thread3 = threading.Thread(target=load_data, args=['data3'])
thread4 = threading.Thread(target=load_data, args=['data4'])
thread1.start()
thread2.start()
thread3.start()
thread4.start()
# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()

finish = time.perf_counter()
print('Elapsed time:', finish - start)
print('End proccess')
