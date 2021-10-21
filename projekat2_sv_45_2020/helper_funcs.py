import datetime
import graph1
import pickle
import difflib
import sys


class BlockedNumberError(Exception):
    pass


def menu(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    options = {1: live_call,
               2: file_call,
               3: two_num_history,
               4: one_num_history,
               5: search_options}
    while True:
        print(
            '1)Live call\n2)File call\n3)History of two numbers\n4)History of one number\n5)Phonebook search\n6)Close')
        option = input('Select option: ')
        try:
            if option == '6':
                break
            else:
                print('\n')
                options[int(option)](phonebook, nums_trie, names_trie, surnames_trie, nums_graph)
        except:
            print('Wrong input.')
            print('\n')
    sys.exit(0)


def live_call(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    while True:
        try:
            print('Put "*" on the end of input for autocomplete suggestions')
            calling = input('Number calling: ').replace('-', '').replace(' ', '')
            if calling[-1] == '*':
                valid_num(calling[:-1])
                person_callig = nums_graph.vertices[autocomplete(calling[:-1], nums_trie)[0]]
                if person_callig.blocked == True:
                    raise BlockedNumberError
            else:
                valid_num(calling)
                person_callig = nums_graph.vertices[calling]
                if person_callig.blocked == True:
                    raise BlockedNumberError
            break
        except ValueError:
            print('Wrong number input. Try again')
        except BlockedNumberError:
            print('This number is blocked. Try again')
        except KeyError:
            person_callig = did_you_mean(calling, phonebook.keys(), nums_graph)
            break

    while True:
        try:
            calls = input('Number called:').replace('-', '').replace(' ', '')
            if calls[-1] == '*':
                valid_num(calls[:-1])
                person_called = nums_graph.vertices[autocomplete(calls[:-1], nums_trie)[0]]
                if person_called.blocked == True:
                    raise BlockedNumberError
            else:
                valid_num(calls)
                person_called = nums_graph.vertices[calls]
                if person_called.blocked == True:
                    raise BlockedNumberError
            break
        except ValueError:
            print('Wrong number input. Try again')
        except BlockedNumberError:
            print('This number is blocked. Try again')
        except KeyError:
            person_called = did_you_mean(calls, phonebook.keys(), nums_graph)
            break

    # treba naci broj u trie
    begin = datetime.datetime.now()
    time_elapsed = 0
    time_elapsed1 = 0
    end = input('x)End call')
    if end == 'x':
        time_elapsed1 = datetime.datetime.now() - begin
        seconds = time_elapsed1.seconds
        hours = seconds // 36000
        seconds = seconds - hours * 36000
        minutes = seconds // 60
        seconds = seconds - 60 * minutes
        time_elapsed = datetime.datetime(1900, 1, 1, hours, minutes, seconds)

    edge = nums_graph.get_edge(person_callig, person_called)
    if edge == None:
        nums_graph.insert_edge(person_callig, person_called, [begin, time_elapsed])
    else:
        edge.data.append([begin, time_elapsed])
    popularity(person_callig, nums_graph)
    popularity(person_called, nums_graph)
    # posle poziva azurirati graf popularnosti
    print('Caller:', calling, '\nCalled:', calls, '\nDate and start of call:', begin, '\nDuration:', time_elapsed1)


def autocomplete(prefix, trie):
    trie.find_suggestions(prefix)
    suggs = trie.sugg
    sugg_dict = {}
    for i in range(len(suggs)):
        sugg_dict[str(i + 1)] = suggs[i]
        print((i + 1), '.', suggs[i])

    while True:
        try:
            option = input('Enter option that you want to pick:')
            answer = trie.find_user(sugg_dict[option])
            break
        except:
            print('Wrong option input')
    return answer


def did_you_mean(num, strings, nums_graph):
    print('Did you mean?')
    suggs = difflib.get_close_matches(num, strings)
    sugg_dict = {}
    for i in range(len(suggs)):
        sugg_dict[str(i + 1)] = suggs[i]
        print((i + 1), '.', suggs[i])

    while True:
        try:
            option = input('Enter option that you want to pick.')
            answer = nums_graph.vertices[sugg_dict[option]]
            break
        except:
            print('Wrong option input')
    return answer


def valid_num(num):
    pattern = '1234567890'
    for char in num:
        if char not in pattern:
            raise ValueError


def file_call(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    try:
        file_name = input('Enter file name:')
        print('-' * 37, 'File Calls', '-' * 37)
        print('|{:25}|{:25}|{:21}|{:10}|'.format('caller', 'called', 'date and time', 'duration'))
        print('-' * 86)
        file = open(file_name, 'r')
        for line in file:
            tokens = line.strip('\n').split(',')
            caller = nums_graph.vertices[tokens[0].replace('-', '').replace(' ', '')]
            calling = nums_graph.vertices[tokens[1].replace('-', '').replace(' ', '')]
            date = datetime.datetime.strptime(tokens[2], ' %d.%m.%Y %H:%M:%S')
            duration = datetime.datetime.strptime(tokens[3], ' %H:%M:%S')
            edge = nums_graph.get_edge(caller, calling)
            if edge == None:
                nums_graph.insert_edge(caller, calling, [date, duration])
            else:
                edge.data.append([date, duration])
            popularity(caller, nums_graph)
            popularity(calling, nums_graph)
            print_call(tokens)
            print('-' * 86)
    except:
        print('Wrong file input.')


def print_call(tokens):
    print('|{:25}|{:25}|{:21}|{:10}|'.format(tokens[0], tokens[1], tokens[2], tokens[3]))


def two_num_history(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    while True:
        try:
            print('Put "*" on the end of input for autocomplete suggestions')
            calling = input('First number: ').replace('-', '').replace(' ', '')
            if calling[-1] == '*':
                valid_num(calling[:-1])
                person_callig = nums_graph.vertices[autocomplete(calling[:-1], nums_trie)[0]]
                if person_callig.blocked == True:
                    raise BlockedNumberError
            else:
                valid_num(calling)
                person_callig = nums_graph.vertices[calling]
                if person_callig.blocked == True:
                    raise BlockedNumberError
            break
        except ValueError:
            print('Wrong number input. Try again')
        except BlockedNumberError:
            print('This number is blocked. Try again')
        except KeyError:
            person_callig = did_you_mean(calling, phonebook.keys(), nums_graph)
            break

    while True:
        try:
            calls = input('Second number:').replace('-', '').replace(' ', '')
            if calls[-1] == '*':
                valid_num(calls[:-1])
                person_called = nums_graph.vertices[autocomplete(calls[:-1], nums_trie)[0]]
                if person_called.blocked == True:
                    raise BlockedNumberError
            else:
                valid_num(calls)
                person_called = nums_graph.vertices[calls]
                if person_called.blocked == True:
                    raise BlockedNumberError
            break
        except ValueError:
            print('Wrong number input. Try again')
        except BlockedNumberError:
            print('This number is blocked. Try again')
        except KeyError:
            person_called = did_you_mean(calls, phonebook.keys(), nums_graph)
            break
    edge1 = nums_graph.get_edge(person_callig, person_called)
    edge2 = nums_graph.get_edge(person_called, person_callig)
    if edge1 == None and edge2 == None:
        print('Numbers have no history.')
    else:
        results = []
        if edge1 != None:
            for inp in edge1.data:
                results.append(inp + [calling] + [calls])
        if edge2 != None:
            for inp in edge2.data:
                results.append(inp + [calls] + [calling])
        results.sort(key=lambda input: input[0])
        print('-' * 43, 'History', '-' * 43)
        print('|{:25}|{:25}|{:21}|{:21}|'.format('date and time', 'duration', 'caller', 'called'))
        print('-' * 95)
        for r in results:
            print_two_history(r)
            print('-' * 95)


def print_two_history(input):
    print('|{:25}|{:25}|{:21}|{:21}|'.format(input[0].strftime(' %d.%m.%Y %H:%M:%S'), input[1].strftime(' %H:%M:%S'),
                                             input[2], input[3]))


def one_num_history(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    while True:
        try:
            print('Put "*" on the end of input for autocomplete suggestions')
            number = input('Number: ').replace('-', '').replace(' ', '')
            if number[-1] == '*':
                valid_num(number[:-1])
                person = nums_graph.vertices[autocomplete(number[:-1], nums_trie)[0]]
                if person.blocked == True:
                    raise BlockedNumberError
            else:
                valid_num(number)
                person = nums_graph.vertices[number]
                if person.blocked == True:
                    raise BlockedNumberError
            break
        except ValueError:
            print('Wrong number input. Try again')
        except BlockedNumberError:
            print('This number is blocked. Try again')
        except KeyError:
            person = did_you_mean(number, phonebook.keys(), nums_graph)
            break
    results = []
    edges_out = nums_graph.incident_edges(person, outgoing=True)
    if edges_out != []:
        for e in edges_out:
            for inp in e.data:
                results.append(inp + [person] + [e.destination])
    edges_in = nums_graph.incident_edges(person, outgoing=False)
    if edges_in != []:
        for e in edges_in:
            for inp in e.data:
                results.append(inp + [e.origin] + [person])
    results.sort(key=lambda inp: inp[3].popularity)
    print('-' * 43, 'History', '-' * 43)
    print('|{:25}|{:25}|{:21}|{:21}|'.format('date and time', 'duration', 'caller', 'called'))
    print('-' * 95)
    for r in results:
        print_one_history(r)
        print('-' * 95)


def print_one_history(input):
    print('|{:25}|{:25}|{:21}|{:21}|'.format(input[0].strftime(' %d.%m.%Y %H:%M:%S'), input[1].strftime(' %H:%M:%S'),
                                             input[2].element, input[3].element))


def search_options(phonebook, nums_trie, names_trie, surnames_trie, nums_graph):
    print('1)Name\n2)Surname\n3)Phone number')
    tries = {
        1: names_trie,
        2: surnames_trie,
        3: nums_trie
    }

    option = input('Enter one option: ')
    try:
        trie = tries[int(option)]
        search_trie(trie, phonebook, nums_graph)
    except:
        print('Wrong option input.')


def search_trie(trie, phonebook, nums_graph):
    try:
        print('Put "*" on the end of input for autocomplete suggestions')
        prefix = input('Search: ')
        if prefix[-1] == '*':
            nums = autocomplete(prefix[:-1], trie)
            users = []
            for num in nums:
                users.append(phonebook[num] + [num])
            print_users(users, nums_graph)
        else:
            print_users(trie.find_users(prefix, phonebook), nums_graph)
    except KeyError:
        print('Wrong searching value.')


def print_users(users, nums_graph):
    if users == []:
        print('No results.')
    else:
        print('{:15}|{:15}|{:15}|{:15}'.format('ime', 'prezime', 'broj', 'popularnost'))
        print('-' * 60)
        sort_by_popularity(users, nums_graph)
        for user in users:
            print('{:15}|{:15}|{:15}|{:15}'.format(user[0], user[1], user[2], nums_graph.vertices[user[2]].popularity))
            print('-' * 60)


def sort_by_popularity(users, nums_graph):
    return users.sort(key=lambda user: nums_graph.vertices[user[2]].popularity)


def upload_data():
    pickle_phonebook_file = open('phonebook.pickle', 'rb')
    phonebook = pickle.load(pickle_phonebook_file)
    pickle_phonebook_file.close()

    pickle_nums_file = open('nums_trie.pickle', 'rb')
    nums_trie = pickle.load(pickle_nums_file)
    pickle_nums_file.close()

    pickle_names_file = open('names_trie.pickle', 'rb')
    names_trie = pickle.load(pickle_names_file)
    pickle_names_file.close()

    pickle_surnames_file = open('surnames_trie.pickle', 'rb')
    surnames_trie = pickle.load(pickle_surnames_file)
    pickle_surnames_file.close()

    pickle_graph_file = open('graph.pickle', 'rb')
    nums_graph = pickle.load(pickle_graph_file)
    pickle_graph_file.close()

    return phonebook, nums_trie, names_trie, surnames_trie, nums_graph


def graph_from_file(graph, phonebook, calls, nums_graph):
    for num in phonebook:
        v = graph1.Graph.Vertex(num)
        graph.vertices[num] = v

    file_calls = open(calls, 'r')
    for line in file_calls:
        tokens = line.strip('\n').split(',')
        caller = graph.vertices[tokens[0].replace('-', '').replace(' ', '')]
        calling = graph.vertices[tokens[1].replace('-', '').replace(' ', '')]
        date = datetime.datetime.strptime(tokens[2], ' %d.%m.%Y %H:%M:%S')
        duration = datetime.datetime.strptime(tokens[3], ' %H:%M:%S')
        edge = graph.get_edge(caller, calling)
        if edge == None:
            nums_graph.insert_edge(caller, calling, [date, duration])
        else:
            edge.data.append([date, duration])
    file_calls.close()


def popularity(node, nums_graph):
    received_calls = 0
    duration = 0
    caller_calls = 0

    edges = nums_graph.incident_edges(node, outgoing=False)

    for e in edges:
        received_calls += len(e.data)
        for input in e.data:
            duration += (input[1] - datetime.datetime(1900, 1, 1)).total_seconds()

    for n in nums_graph.get_neighbor_nodes(node):
        caller_calls += num_received_calls(n, nums_graph)

    pop = int(received_calls + caller_calls + duration * 0.001)
    node.popularity = pop


def num_received_calls(node, nums_graph):
    received_calls = 0
    edges = nums_graph.incident_edges(node, outgoing=False)
    for e in edges:
        received_calls += len(e.data)
    return received_calls