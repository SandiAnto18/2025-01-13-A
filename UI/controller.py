import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillLocalizations(self):
        luoghi= self._model.getLocalizations()
        # Inserisco gli anni in entrambi i menu
        # Popolo i due menu a tendina
        for loc in luoghi:
            self._view.dd_localization.options.append(ft.dropdown.Option(loc))


        self._view.update_page()

    def handle_graph(self, e):
        # Leggo da VIEW gli anni selezionati
        local= self._view.dd_localization.value

        # costruisco il grafo sugli anni selezionati (da ,a)
        self._model.buildGraph(local)

        # Pulisco i risultati precedenti
        self._view.txt_result.controls.clear()

        # Visualizzo il numero di nodi e archi
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )

        # Recupero e stampo i tre archi di peso maggiore
        topEdges = self._model.getTop3Edges()

        self._view.txt_result.controls.append(
            ft.Text("archi:")
        )

        for i, (c1, c2, data) in enumerate(topEdges, start=1):
            self._view.txt_result.controls.append(
                ft.Text(
                    f"{i}. {c1.GeneID} <--> {c2.GeneID}: "
                    f"(peso {data['weight']})"
                )
            )

        # Aggiorno la pagina
        self._view.update_page()


    def analyze_graph(self, e):

            # RECUPERO LE COMPONENTI CONNESSE
            result = self._model.getComponentiConnesse()

            # PULISCO I RISULTATI PRECEDENTI
            self._view.txt_result.controls.clear()

            # SCORRO LE DIVERSE COMPONENTI CONNESSE
            for geneIDs,dimensione in result:
                    self._view.txt_result.controls.append(
                        ft.Text(f"{geneIDs} | Dimensione {dimensione}")
                    )

            # AGGIORNO LA PAGINA
            self._view.update_page()
    def handle_path(self, e):
        pass

