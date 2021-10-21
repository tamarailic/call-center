class Graph:

    """ Reprezentacija jednostavnog grafa"""

    # ------------------------- Ugnježdena klasa Vertex -------------------------
    class Vertex:
        """ Struktura koja predstavlja čvor grafa."""
        __slots__ = '_element','_popularity','_blocked'

        def __init__(self, x):
            self._element = x
            self._popularity=0
            self._blocked=False

        @property
        def element(self):
            return self._element

        @element.setter
        def element(self, value):
            self._element = value

        @property
        def popularity(self):
            return self._popularity

        @popularity.setter
        def popularity(self,value):
            self._popularity=value

        @property
        def blocked(self):
            return self._blocked

        @blocked.setter
        def blocked(self, value):
            self._blocked = value

        def __hash__(self):         # omogućava da Vertex bude ključ mape
            return hash(id(self))

        def __str__(self):
            return str(self._element)

    # ------------------------- Ugnježdena klasa Edge -------------------------
    class Edge:
        """ Struktura koja predstavlja ivicu grafa """
        __slots__ = '_origin', '_destination', '_data'

        def __init__(self, origin, destination,data=None):
            self._origin = origin
            self._destination = destination
            if data==None:
                self._data = []
            else:
                self._data=[data]

        def endpoints(self):
            """ Vraća torku (u,v) za čvorove u i v."""
            return self._origin, self._destination

        def opposite(self, v):
            """ Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v mora biti instanca klase Vertex')
            if self._destination == v:
                return self._origin
            elif self._origin == v:
                return self._destination
            raise ValueError('v nije čvor ivice')

        # def data(self):
        #     """ Vraća element vezan za ivicu"""
        #     return self._data
        @property
        def origin(self):
            return self._origin

        @origin.setter
        def origin(self, o):
            self._origin = o

        @property
        def destination(self):
            return self._destination

        @destination.setter
        def destination(self, d):
            self._destination=d

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, data):
            self._data.append(data)

        def __hash__(self):         # omogućava da Edge bude ključ mape
            return hash((self._origin, self._destination))



    # ------------------------- Metode klase Graph -------------------------
    def __init__(self, directed=False):
        """ Kreira prazan graf (podrazumevana vrednost je da je neusmeren).

        Ukoliko se opcioni parametar directed postavi na True, kreira se usmereni graf.
        """
        self._outgoing = {}
        # ukoliko je graf usmeren, kreira se pomoćna mapa
        self._incoming = {} if directed else self._outgoing
        self.vertices={}

    def _validate_vertex(self, v):
        """ Proverava da li je v čvor(Vertex) ovog grafa."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Očekivan je objekat klase Vertex')
        # if v not in self._outgoing:
        #     raise ValueError('Vertex ne pripada ovom grafu.')

    def is_directed(self):
        """ Vraća True ako je graf usmeren; False ako je neusmeren."""
        return self._incoming is not self._outgoing  # graf je usmeren ako se mape razlikuju

    def vertex_count(self):
        """ Vraća broj čvorova u grafu."""
        return len(self._outgoing)

    # def vertices(self):
    #     """ Vraća iterator nad svim čvorovima grafa."""
    #     return self._outgoing.keys()

    def edge_count(self):
        """ Vraća broj ivica u grafu."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # ukoliko je graf neusmeren, vodimo računa da ne brojimo čvorove više puta
        return total if self.is_directed() else total // 2

    def edges(self):
        """ Vraća set svih ivica u grafu."""
        result = set()       # pomoću seta osiguravamo da čvorove neusmerenog grafa brojimo samo jednom
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())    # dodavanje ivice u rezultujući set
        return result

    def get_edge(self, u, v):
        """ Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        if u in self._outgoing:
            return self._outgoing[u].get(v)
        else:
            return None

    def degree(self, v, outgoing=True):
        """ Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """ Vraća sve (odlazne) ivice iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        edges=[]
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            edges.append(edge)
        return edges

    def get_neighbor_nodes(self,node,incoming=True):
        if incoming:
            return self._incoming[node].keys()
        else:
            return self._outgoing[node].keys()

    def insert_vertex(self, x=None):
        """ Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}        # mapa različitih vrednosti za dolazne čvorove
        return v

    def insert_edge(self, u, v, x=None):
        """ Ubacuje i vraća novu ivicu (Edge) od u do v sa pomoćnim elementom x.

        Baca ValueError ako u i v nisu čvorovi grafa.
        Baca ValueError ako su u i v već povezani.
        """

        e = self.Edge(u, v,x)
        if u not in self._outgoing:
            self._outgoing[u]={}
        if v not in self._incoming:
            self._incoming[v]={}
        self._outgoing[u][v] = e
        self._incoming[v][u] = e