import time
def example(seconds):
    print('starying task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('Task complited')