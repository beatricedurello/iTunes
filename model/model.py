import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._maxLen = None
        self._bestSet = None
        self._grafo = nx.Graph()
        self._idMapAlbum = {}

    def getSetOfNodes(self, a1, soglia):
        self._bestSet = {}
        self._maxLen = 0

        parziale = {a1}
        cc = nx.node_connected_component(self._grafo, a1)

        cc.remove(a1)  # mi fa risparmiare un'iterazione del ciclo

        for n in cc:
            # richiamo la mia ricorsione
            parziale.add(n)  # add e non append perchè è un set
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia)
            parziale.remove(n)  # backtracking
            cc.add(n)

        return self._bestSet, self.getDurataTot(self._bestSet)  # getDurataTot deve essere un valore inferiore a quello di soglia

    def _ricorsione(self, parziale, rimanenti, soglia):
        # i rimanenti sono tutti i nodi della componente connessa tranne quelli che ho già aggiunto
        # 1) verifico che parziale sia una soluzione ammissibile, ovvero se viola i vincoli
        if self.getDurataTot(parziale) > soglia:
            return

        # 2) se parziale soddisfa i criteri allor averifico se è migliore di bestSet
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)

        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n)


    def buildGraph(self, durataMin):
        self._grafo.clear()
        self.allNodi = DAO.getAllAlbums(durataMin)
        self._grafo.add_nodes_from(self.allNodi)

        self._idMapAlbum = {n.AlbumId: n for n in self.allNodi}

        self.allEdges = DAO.getAllEdges(self._idMapAlbum)

        self._grafo.add_edges_from(self.allEdges)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodi(self):
        return list(self._grafo.nodes)

    def getDurataTot(self, cc):
        sum = 0
        for n in cc:
            sum += n.Durata
        return sum

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._grafo, a1)
        return len(cc), self.getDurataTot(cc)

