class TrieNode():
    __slots__ = '_value','_num','_children','_blocked'
    def __init__(self,value):
        self._value=value
        self._num=[]
        self._children={}
        self._blocked = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,v):
        self._value=v

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self,n):
        self._num.append(n)

    @property
    def children(self):
        return self._children

    def add_child(self,child):
        self._children[child.value]=child

class Trie():

    def __init__(self):
        self._root=TrieNode('')
        self._leaf_nodes=[]
        self.sugg=[]


    def insert_word(self,word,num):

        node=self._root
        for char in word:
            if char in node.children:
                node=node.children[char]
            else:
                new_node=TrieNode(char)
                node.add_child(new_node)
                node=new_node

        node.num.append(num)

    def valid_prefix(self,prefix):
        prefix = prefix.lower()
        node = self._root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                raise KeyError
        return node,prefix

    def find_last_node(self,prefix):
        self._leaf_nodes=[]
        node,prefix=self.valid_prefix(prefix)
        if node.num!=[]:
            self._leaf_nodes.append(node)
        else:
            for child in node.children:
                self.search_results(node.children[child])

    def search_results(self,node):
        if node.num!=[]:
            self._leaf_nodes.append(node)
        else:
            for child in node.children:
                self.search_results(node.children[child])

    def find_users(self,prefix, phonebook):
        users=[]
        self.find_last_node(prefix)
        for result in self._leaf_nodes:
            for num in result.num:
                users.append(phonebook[num]+[num])
        return users

    def find_user(self,prefix):
        self.find_last_node(prefix)
        return self._leaf_nodes[0].num

    def find_match(self,node,prefix):
        if node.num!=[]:
             self.sugg.append(prefix)
        else:
            for child in node.children:
                self.find_match(node.children[child],prefix+child)


    def find_suggestions(self,prefix):
        self.sugg=[]
        node,prefix=self.valid_prefix(prefix)
        if node.children=={}:
            if not node._blocked:
                self.sugg.append(prefix)
        else:
            for child in node.children:
               self.find_match(node.children[child],prefix+child)



