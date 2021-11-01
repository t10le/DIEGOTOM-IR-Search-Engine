import ast
import time


print('test.py initiated.\nPlease enter only a single term below; to exit, type \'ZZEND\' and hit enter.')
user = input('> ')


avg_time = 0
count = 0
while user != "ZZEND":
    start = time.time()
    # Enter task below

    end = time.time()

    elapsed = end-start
    avg_time += elapsed
    count += 1
    print(f"Elasped Time to Retrieve: {elapsed}")
    user = input('> ')
print("\ntest.py has been terminated by 'ZZEND'")
print(f"Averaged time of retrieval: {avg_time/count}")
