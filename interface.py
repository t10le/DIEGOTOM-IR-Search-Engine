import time
import search as dt
# Greet and process user filter request
dt.welcome_msg()
print('\nREADY!')

# Process user query and use search.py
print('\nEnter your query below; to exit, type \'ZZEND\' and hit enter.')

avg_time = 0
count = 0
while True:
    user = input('> ')
    if user == 'ZZEND':
        break
    start = time.time()
    # --- Enter task below ---
    ranked_list = dt.vector_space_pipeline(dt.pre_process(user))
    print(f'ORIGINAL QUERY: "{user}"')
    # ------------------------
    end = time.time()

    elapsed = end-start
    avg_time += elapsed
    count += 1
    print(f"\nElasped Time to Retrieve: {elapsed}")
print("\ntest.py has been terminated by 'ZZEND'")
if count == 0:
    print(f"Averaged time of retrieval: 0.0")
else:
    print(f"Averaged time of retrieval: {avg_time/count}")
