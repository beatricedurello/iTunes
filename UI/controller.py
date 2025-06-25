import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        dMinTxt = self._view._txtInDurata.value
        if dMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, dato non inserito", color="red"))
            self._view.update_page()
            return

        try:
            dMin = int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore inserito non valido", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(dMin)
        n,e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {n} nodi e {e} archi"))
        self._fillDD(self._model.getAllNodi())
        self._view.update_page()

    def _fillDD(self, listOfNodes):
        listOfOptions = map(lambda x: ft.dropdown.Option(text=x.Title, on_click=self._readDDValue, data=x), listOfNodes)
        self._view._ddAlbum.options = list(listOfOptions)
        self._view.update_page()

    def _readDDValue(self, e):
        if e.control.data is None:
            print("errore in reading dd")
        self._choiceDD = e.control.data


    def getSelectedAlbum(self, e):
        pass

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, album non selezionato", color="red"))
            self._view.update_page()
            return

        size, dTotCC = self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD} "
                                                      f"ha {size} nodi e durata totale di {dTotCC}"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, dato non inserito", color="red"))
            self._view.update_page()
            return
        try:
            soglia = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore inserito non valido", color="red"))
            self._view.update_page()
            return

        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, album non selezionato", color="red"))
            self._view.update_page()
            return

        setOfNodes, sumDurata = self._model.getSetOfNodes(self._choiceDD, soglia)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione {len(setOfNodes)}, durata totale {sumDurata}"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()