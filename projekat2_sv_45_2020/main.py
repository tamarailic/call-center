import time
from helper_funcs import menu,upload_data

if __name__ == '__main__':
    time1=time.time()
    phonebook, nums_trie, names_trie, surnames_trie, nums_graph=upload_data()
    print(time.time()-time1)
    menu(phonebook, nums_trie, names_trie, surnames_trie, nums_graph)