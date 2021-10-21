import pickle
import graph1
import datetime
from main import popularity
import trie
def graph_from_file(graph,phonebook,calls):

    for num in phonebook:
        v=graph1.Graph.Vertex(num)
        graph.vertices[num]=v

    file_calls = open(calls,'r')
    for line in file_calls:
        tokens=line.strip('\n').split(',')
        caller=graph.vertices[tokens[0].replace('-','').replace(' ','')]
        calling=graph.vertices[tokens[1].replace('-','').replace(' ','')]
        date=datetime.datetime.strptime(tokens[2],' %d.%m.%Y %H:%M:%S')
        duration=datetime.datetime.strptime(tokens[3],' %H:%M:%S')
        edge=graph.get_edge(caller,calling)
        if edge==None:
            nums_graph.insert_edge(caller, calling,[date,duration])
        else:
            edge.data.append([date,duration])
    file_calls.close()
if __name__ == '__main__':
    phonebook = {}
    file_phones = open('phones.txt', 'r')
    for line in file_phones:
        tokens = line.strip('\n').split(',')
        name, surname = tokens[0].split(' ')
        number = tokens[1].replace('-', '').replace(' ', '')
        phonebook[number] = [name, surname]
    file_phones.close()


    names_trie = trie.Trie()
    surnames_trie = trie.Trie()
    nums_trie = trie.Trie()
    for num in phonebook:
        names_trie.insert_word(phonebook[num][0].lower(), num)
        surnames_trie.insert_word(phonebook[num][1].lower(), num)
        nums_trie.insert_word(num, num)

    nums_graph = graph1.Graph(directed=True)
    graph_from_file(nums_graph, phonebook, 'calls.txt')
    for node in nums_graph.vertices:
        popularity(nums_graph.vertices[node], nums_graph)

    blocked_files = open('blocked.txt', 'r')
    for line in blocked_files:
        blocked_num = line.strip('\n').replace('-', '').replace(' ', '')
        nums_graph.vertices[blocked_num].blocked=True
        nums_trie.find_last_node(blocked_num)
        nums_trie._leaf_nodes[0]._blocked = True
    blocked_files.close()

    pickle_graph_file=open('graph.pickle','wb')
    pickle.dump(nums_graph,pickle_graph_file)
    pickle_graph_file.close()

    pickle_nums_file = open('nums_trie.pickle', 'wb')
    pickle.dump(nums_trie, pickle_nums_file)
    pickle_nums_file.close()

    pickle_names_file = open('names_trie.pickle', 'wb')
    pickle.dump(names_trie, pickle_names_file)
    pickle_names_file.close()

    pickle_surnames_file = open('surnames_trie.pickle', 'wb')
    pickle.dump(surnames_trie, pickle_surnames_file)
    pickle_surnames_file.close()

    pickle_phonebook_file = open('phonebook.pickle', 'wb')
    pickle.dump(phonebook, pickle_phonebook_file)
    pickle_phonebook_file.close()

