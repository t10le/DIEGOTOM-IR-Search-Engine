import time
import search as dt

metadata_tuple = dt.read_metadata()
authors_dict = metadata_tuple[0]
titles_dict = metadata_tuple[1]

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
    query_decon = dt.pre_process(user)
    ranked_list = dt.vector_space_pipeline(query_decon)
    print(f'{query_decon}\n')
    # print(ranked_list)
    for i in range(len(ranked_list)):
        score = ranked_list[i][1]
        ID = ranked_list[i][0]
        author = ' '.join(authors_dict[ID])
        title = ' '.join(titles_dict[ID])
        print(
            f'Rank: {i+1}\nDocument ID:\t {ID}\nTitle:\t\t {title}\nAuthor(s):\t {author}\nRelevance Score: {score}\n\n')
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
