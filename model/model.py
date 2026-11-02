
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph=nx.Graph()
    def getLocalizations(self):
        return DAO.getLocalizations()

    def buildGraph(self,localization):
        classif = DAO.getClassification(localization)

        # SVUOTO IL GRAFO PRECEDENTE
        self._graph.clear()

        # AGGIUNGO I PILOTI COME NODI
        self._graph.add_nodes_from(classif)

        dMap = {}
        for d in classif:
            dMap[d.GeneID] = d

        # RECUPERO LE COPPIE DI PILOTI E I PESI
        archi = DAO.getArchi(localization)

        # AGGIUNGO GLI ARCHI CON IL LORO PESO
        for g1, g2, peso in archi:
            gene1 = dMap[g1]
            gene2 = dMap[g2]


            self._graph.add_edge(
                gene1,
                gene2,
                weight=peso
            )
        print(archi)

    def getTop3Edges(self):
        # Recupero gli archi con i relativi attributi
        edges = list(self._graph.edges(data=True))

        # Ordino per peso crescente
        edges.sort(key=lambda e: e[2]["weight"])

        # Restituisco i primi tre archi
        return edges

    def getNumNodi(self):
        # RESTITUISCO IL NUMERO DI NODI
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        # RESTITUISCO IL NUMERO DI ARCHI
        return self._graph.number_of_edges()

    def getComponentiConnesse(self):
        # RECUPERO TUTTE LE COMPONENTI CONNESSE
        componenti = list(nx.connected_components(self._graph))

        # CONSIDERO SOLO LE COMPONENTI CON PIU' DI UN NODO
        componenti = [c for c in componenti if len(c) > 1]

        # ORDINO LE COMPONENTI PER DIMENSIONE DECRESCENTE
        componenti.sort(key=len, reverse=True)

        # RESTITUISCO OGNI COMPONENTE (G235468 ───── G237345) considerata come un unico insieme
        #con la sua dimensione

        res = []
        for c in componenti:
            # RECUPERO I GENEID delle coppie di NODI DELLA COMPONENTE
            geneIDs = []
            for nodo in c:
                geneIDs.append(nodo.GeneID)

            # SALVO I GENEID x coppia E LA DIMENSIONE DELLA COMPONENTE
            res.append((geneIDs, len(c)))

        return res



