import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodi = None
        self._grafo = nx.Graph()
        self._idMap = {}

    def getAnni(self):
        return DAO.getAllYears()
    def get_numnodi(self):
        return len(self._grafo.nodes())
    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self, ai, af):
        self._grafo.clear()
        self._idMap = {}
        self._nodi = DAO.getAllNodes(ai, af)
        for n in self._nodi:
            self._grafo.add_node(n)
            self._idMap[n.driverId] = n
        self.addEdges(ai, af)

    def addEdges(self, ai, af):
        edges = DAO.getAllEdges(ai, af)
        for e in edges:
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            self._grafo.add_edge(n1, n2, weight=e[2])

    def get_top3_archi(self):
        archi = []
        for u, v, data in self._grafo.edges(data=True):
            archi.append((u, v, data["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:3]

    def getInfoCompConnessa(self):
        if self._grafo.number_of_nodes() == 0:
            return 0, set()
        numero = nx.number_connected_components(self._grafo)
        piu_grande = max(nx.connected_components(self._grafo), key=len)
        piu_grande_ordinata = sorted(piu_grande, key=lambda x: self._grafo.degree(x), reverse=True)
        return numero, piu_grande_ordinata

