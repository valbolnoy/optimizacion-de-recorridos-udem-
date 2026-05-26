
class GrafoLista:

    def __init__(self):
        self.listaAdy: dict[any, list[any]] = {}
        self.tamano: int = 0

    def agregarVertice(self, valor: any):
        if valor in self.listaAdy:
            return None
        self.listaAdy[valor] = []
        self.tamano = self.tamano + 1

    def agregarConexion(self, vertice1, vertice2, dirigido=False, peso=1):
        if vertice1 not in self.listaAdy:
            self.agregarVertice(vertice1)
        if vertice2 not in self.listaAdy:
            self.agregarVertice(vertice2)

        vecinosVertice1 = []
        for vertice in self.listaAdy[vertice1]:
            vecinosVertice1.append(vertice[0])

        if vertice2 not in vecinosVertice1:
            self.listaAdy[vertice1].append((vertice2, peso))

        if not dirigido:
            vecinosVertice2 = []
            for vertice in self.listaAdy[vertice2]:
                vecinosVertice2.append(vertice[0])

            if vertice1 not in vecinosVertice2:
                self.listaAdy[vertice2].append((vertice1, peso))

    def agregarConexionCampus(self, vertice1, vertice2,
                               distancia: float,
                               tiempo: float,
                               congestion: int,
                               accesible: bool,
                               estado: str,
                               dirigido=False):

        if vertice1 not in self.listaAdy:
            self.agregarVertice(vertice1)
        if vertice2 not in self.listaAdy:
            self.agregarVertice(vertice2)

        atributos = {
            "distancia":  distancia,
            "tiempo":     tiempo,
            "congestion": congestion,
            "accesible":  accesible,
            "estado":     estado
        }

        vecinosV1 = [v[0] for v in self.listaAdy[vertice1]]
        if vertice2 not in vecinosV1:
            self.listaAdy[vertice1].append((vertice2, atributos))

        if not dirigido:
            vecinosV2 = [v[0] for v in self.listaAdy[vertice2]]
            if vertice1 not in vecinosV2:
                self.listaAdy[vertice2].append((vertice1, atributos))


    def dijkstraCampus(self, verticeInicial: any, verticeFinal: any,
                        criterio: str = "distancia") -> tuple:

        criteriosValidos = ["distancia", "tiempo", "congestion", "accesible"]
        if criterio not in criteriosValidos:
            return (float('inf'), [], f"Criterio '{criterio}' no válido. Use: {criteriosValidos}")

        if verticeInicial not in self.listaAdy or verticeFinal not in self.listaAdy:
            return (float('inf'), [], "Uno o ambos vértices no existen en el grafo.")

        # Inicializar todas las distancias en infinito
        distancias   = {v: float('inf') for v in self.listaAdy}
        predecesores = {v: None         for v in self.listaAdy}
        visitados    = []

        distancias[verticeInicial] = 0
        verticeActual = verticeInicial

        while verticeActual is not None and verticeActual != verticeFinal:

            for vecino, atributos in self.listaAdy[verticeActual]:
                if atributos["estado"] in ("bloqueado", "mantenimiento"):
                    continue

                if criterio == "accesible" and not atributos["accesible"]:
                    continue

                if vecino in visitados:
                    continue

                if criterio == "accesible":
                    peso = atributos["tiempo"]
                else:
                    peso = atributos[criterio]

                nuevaDistancia = distancias[verticeActual] + peso

                if nuevaDistancia < distancias[vecino]:
                    distancias[vecino]   = nuevaDistancia
                    predecesores[vecino] = verticeActual

            visitados.append(verticeActual)

            distanciaMenor = float('inf')
            verticeMenor   = None

            for vertice in distancias:
                if vertice not in visitados and distancias[vertice] < distanciaMenor:
                    distanciaMenor = distancias[vertice]
                    verticeMenor   = vertice

            verticeActual = verticeMenor

        if distancias[verticeFinal] == float('inf'):
            return (float('inf'), [], "No existe ruta disponible entre los vértices dados.")

        camino     = []
        pasoActual = verticeFinal
        while pasoActual is not None:
            camino.insert(0, pasoActual)
            pasoActual = predecesores[pasoActual]
        costo = distancias[verticeFinal]
        if criterio == "distancia":
            explicacion = (f"Ruta más corta por distancia: {costo:.0f} metros. "
                           f"Se eligió minimizando el total de metros recorridos, "
                           f"ignorando caminos bloqueados o en mantenimiento.")
        elif criterio == "tiempo":
            explicacion = (f"Ruta más rápida: {costo:.1f} minutos. "
                           f"Se eligió minimizando el tiempo de recorrido, "
                           f"ignorando caminos bloqueados o en mantenimiento.")
        elif criterio == "congestion":
            explicacion = (f"Ruta con menor congestión: nivel acumulado {costo}. "
                           f"Se eligió la ruta con menos tráfico en cada tramo, "
                           f"ignorando caminos bloqueados o en mantenimiento.")
        elif criterio == "accesible":
            explicacion = (f"Ruta accesible más rápida: {costo:.1f} minutos. "
                           f"Solo se consideraron caminos accesibles para personas con "
                           f"movilidad reducida, ignorando los demás.")

        return (costo, camino, explicacion)

    def arbolExpansionMinima(self, verticeInicial: any) -> tuple:

        if verticeInicial not in self.listaAdy:
            return (float('inf'), [])

        incluidos  = [verticeInicial]   
        aristas    = []               
        distanciaTotal = 0


        while len(incluidos) < len(self.listaAdy):

            mejorDistancia = float('inf')
            mejorArista    = None      


            for vertice in incluidos:
                for vecino, atributos in self.listaAdy[vertice]:


                    if atributos["estado"] in ("bloqueado", "mantenimiento"):
                        continue

                    if vecino in incluidos:
                        continue

                    if atributos["distancia"] < mejorDistancia:
                        mejorDistancia = atributos["distancia"]
                        mejorArista    = (vertice, vecino, atributos["distancia"])

            if mejorArista is None:
                break

            origen, destino, dist = mejorArista
            incluidos.append(destino)
            aristas.append(mejorArista)
            distanciaTotal += dist

        return (distanciaTotal, aristas)


    def mostrarRuta(self, verticeInicial: any, verticeFinal: any,
                    criterio: str = "distancia"):

        costo, camino, explicacion = self.dijkstraCampus(
            verticeInicial, verticeFinal, criterio
        )

        print("\n" + "=" * 60)
        print(f"  RUTA: {verticeInicial}  →  {verticeFinal}")
        print(f"  Criterio de búsqueda: {criterio.upper()}")
        print("=" * 60)

        if not camino:
            print(f"  ✗ {explicacion}")
            return

        print(f"\n  Recorrido ({len(camino) - 1} tramos):")

        for i in range(len(camino) - 1):
            origen  = camino[i]
            destino = camino[i + 1]

            atributos = None
            for vecino, attrs in self.listaAdy[origen]:
                if vecino == destino:
                    atributos = attrs
                    break

            if atributos:
                accesible_txt = "Sí" if atributos["accesible"] else "No"
                print(f"  {i+1}. {origen:15} → {destino:15} | "
                      f"{atributos['distancia']:>4.0f}m  "
                      f"{atributos['tiempo']:>4.1f}min  "
                      f"congestión:{atributos['congestion']}  "
                      f"accesible:{accesible_txt}")
            else:
                print(f"  {i+1}. {origen} → {destino}")

        print(f"\n  Costo total ({criterio}): {costo}")
        print(f"\n  ¿Por qué esta ruta?")
        print(f"  {explicacion}")
        print("=" * 60)




campus = GrafoLista()

campus.agregarConexionCampus("Entrada",      "BloqueA",      distancia=120, tiempo=2,   congestion=3, accesible=True,  estado="bloqueado")
campus.agregarConexionCampus("Entrada",      "Parqueadero1", distancia=80,  tiempo=1,   congestion=4, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Entrada",      "Admisiones",   distancia=150, tiempo=2.5, congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueA",      "BloqueB",      distancia=90,  tiempo=1.5, congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueA",      "Cafeteria",    distancia=110, tiempo=2,   congestion=5, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueA",      "Lab1",         distancia=60,  tiempo=1,   congestion=1, accesible=False, estado="disponible")
campus.agregarConexionCampus("BloqueB",      "BloqueC",      distancia=70,  tiempo=1,   congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueB",      "Biblioteca",   distancia=100, tiempo=1.5, congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueB",      "Lab2",         distancia=55,  tiempo=1,   congestion=1, accesible=False, estado="mantenimiento")
campus.agregarConexionCampus("BloqueC",      "BloqueD",      distancia=80,  tiempo=1.5, congestion=3, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueC",      "Teatro",       distancia=130, tiempo=2,   congestion=1, accesible=True,  estado="disponible")
campus.agregarConexionCampus("BloqueD",      "Deportes",     distancia=200, tiempo=3,   congestion=2, accesible=False, estado="disponible")
campus.agregarConexionCampus("BloqueD",      "Enfermeria",   distancia=95,  tiempo=1.5, congestion=1, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Lab1",         "Lab2",         distancia=40,  tiempo=0.5, congestion=1, accesible=False, estado="disponible")
campus.agregarConexionCampus("Lab1",         "Biblioteca",   distancia=140, tiempo=2,   congestion=2, accesible=False, estado="disponible")
campus.agregarConexionCampus("Biblioteca",   "Cafeteria",    distancia=85,  tiempo=1.5, congestion=3, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Cafeteria",    "Teatro",       distancia=160, tiempo=2.5, congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Cafeteria",    "Parqueadero2", distancia=120, tiempo=2,   congestion=3, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Parqueadero1", "Admisiones",   distancia=100, tiempo=1.5, congestion=1, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Parqueadero2", "Deportes",     distancia=180, tiempo=2.5, congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Teatro",       "Enfermeria",   distancia=110, tiempo=2,   congestion=1, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Admisiones",   "BloqueA",      distancia=130, tiempo=2,   congestion=2, accesible=True,  estado="disponible")
campus.agregarConexionCampus("Enfermeria",   "Deportes",     distancia=150, tiempo=2.5, congestion=1, accesible=True,  estado="disponible")



for criterio in ["distancia", "tiempo", "congestion", "accesible"]:
    campus.mostrarRuta("Entrada", "Deportes", criterio)



print("  RECORRIDO DE VISITANTES — ÁRBOL DE EXPANSIÓN MÍNIMA (Prim)")
distanciaTotal, aristas = campus.arbolExpansionMinima("Entrada")

print(f"\n  Tramos del recorrido ({len(aristas)} conexiones):")
for i, (origen, destino, dist) in enumerate(aristas, 1):
    print(f"  {i:>2}. {origen:15} → {destino:15} | {dist:>4.0f}m")

print(f"\n  Distancia total del recorrido: {distanciaTotal:.0f} metros")
print(f"  Lugares cubiertos: {len(aristas) + 1} de {campus.tamano}")


campus.mostrarRuta("Entrada", "Capilla", "distancia")
 