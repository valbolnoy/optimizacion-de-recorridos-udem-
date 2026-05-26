
from typing import Any, List, Dict, Tuple
from collections import deque

class Camino:
    """
    Almacena los atributos de un camino entre dos lugares del campus.
    Se usa como 'peso' dentro de la lista de adyacencia.
    """
    def __init__(self, distancia: int, tiempo: int, congestion: int = 1,
                 accesible: bool = True, estado: str = 'disponible'):
        self.distancia  = distancia   
        self.tiempo     = tiempo      
        self.congestion = congestion  
        self.accesible  = accesible   
        self.estado     = estado     

    def estaDisponible(self):
        return self.estado == 'disponible'
    
    def obtenerPeso(self, factor: str = 'distancia') -> float:
        """
        Retorna el peso del camino según el factor de optimización.
        Si no está disponible retorna infinito (no transitable).
        """
        if not self.estaDisponible():
            return float('inf')
        if factor == 'distancia':
            return self.distancia
        elif factor == 'tiempo':
            return self.tiempo * self.congestion  # tiempo ajustado por congestión
        elif factor == 'congestion':
            return self.congestion
        return self.distancia
    
    def __repr__(self):
        return (f"[dist:{self.distancia}m | tiempo:{self.tiempo}min | "
                f"cong:{self.congestion} | accesible:{self.accesible} | "
                f"estado:{self.estado}]")
 
class GrafoListaCampus:
    def __init__(self):
        self.listaAdy: Dict[Any, List[Tuple[Any, Camino]]] = {}
        self.tamano: int = 0

    def agregarVertice(self, valor: any):
        if valor in self.listaAdy:
            return None
        self.listaAdy[valor] = []
        self.tamano = self.tamano + 1

    def agregarConexion(self, vertice1, vertice2, camino: Camino,
                        dirigido: bool = False):
        if vertice1 not in self.listaAdy:
            self.agregarVertice(vertice1)
        if vertice2 not in self.listaAdy:
            self.agregarVertice(vertice2)
 
        # Verificar si la conexión ya existe en v1
        vecinosV1 = [v for v, c in self.listaAdy[vertice1]]
        if vertice2 not in vecinosV1:
            self.listaAdy[vertice1].append((vertice2, camino))
 
        # Si no es dirigido, crear relación inversa con el mismo Camino
        if not dirigido:
            vecinosV2 = [v for v, c in self.listaAdy[vertice2]]
            if vertice1 not in vecinosV2:
                self.listaAdy[vertice2].append((vertice1, camino))

    def cambiarEstadoCamino(self, vertice1, vertice2, nuevoEstado: str):
        estadosValidos = {'disponible', 'bloqueado', 'mantenimiento'}
        if nuevoEstado not in estadosValidos:
            print(f"Estado invalido. Use: {estadosValidos}")
            return
        for lugar in [vertice1, vertice2]:
            otro = vertice2 if lugar == vertice1 else vertice1
            for vecino, camino in self.listaAdy[lugar]:
                if vecino == otro:
                    camino.estado = nuevoEstado
        print(f"  Estado de '{vertice1} <-> {vertice2}' actualizado a '{nuevoEstado}'")

    def mostrarGrafo(self):
        print("\n" + "="*65)
        print("      MAPA DEL CAMPUS UDeM  -  Lista de Adyacencia")
        print("="*65)
        for lugar in self.listaAdy:
            print(f"\n  {lugar}:")
            if self.listaAdy[lugar]:
                for vecino, camino in self.listaAdy[lugar]:
                    print(f"     --> {vecino}  {camino}")
            else:
                print("     (sin conexiones)")
        print("="*65)
 
    def mostrarCaminosBloqueados(self):
        print("\n  Caminos NO disponibles:")
        encontrado = False
        for origen in self.listaAdy:
            for vecino, camino in self.listaAdy[origen]:
                if not camino.estaDisponible():
                    print(f"    {origen} --> {vecino} [{camino.estado}]")
                    encontrado = True
        if not encontrado:
            print("    Todos los caminos estan disponibles.")

    
    def recorrerEnAnchura(self, verticeInicial: any,
                          soloAccesible: bool = False) -> List[Any]:
        if verticeInicial not in self.listaAdy:
            return []
 
        visitados = []
        cola = deque([verticeInicial])
 
        while cola:
            vertice = cola.popleft()
            if vertice not in visitados:
                visitados.append(vertice)
                for vecino, camino in self.listaAdy[vertice]:
                    if vecino not in visitados:
                        # Restricción: camino disponible y accesible si se pide
                        if camino.estaDisponible():
                            if soloAccesible and not camino.accesible:
                                continue
                            cola.append(vecino)
        return visitados
    

#santi copia aqui 


campus = GrafoListaCampus()

# agregarConexion(origen, destino, Camino(dist, tiempo, cong, accesible, estado))

campus.agregarConexion('Bloque A',    'Bloque B',          Camino(120, 2, 2, True,  'disponible'))
campus.agregarConexion('Bloque A',    'Biblioteca',        Camino(200, 3, 1, True,  'disponible'))
campus.agregarConexion('Bloque A',    'Cafeteria',         Camino(150, 2, 3, True,  'disponible'))
campus.agregarConexion('Bloque A',    'Parqueadero Norte', Camino(300, 4, 1, True,  'disponible'))
campus.agregarConexion('Bloque B',    'Laboratorios',      Camino(100, 2, 1, True,  'disponible'))
campus.agregarConexion('Bloque B',    'Cafeteria',         Camino(180, 3, 2, False, 'disponible'))
campus.agregarConexion('Bloque B',    'Bloque C',          Camino(130, 2, 1, True,  'disponible'))
campus.agregarConexion('Bloque C',    'Teatro',            Camino(250, 4, 1, True,  'disponible'))
campus.agregarConexion('Bloque C',    'Enfermeria',        Camino(170, 3, 1, True,  'disponible'))
campus.agregarConexion('Bloque C',    'Zona Deportiva',    Camino(220, 4, 2, True,  'disponible'))
campus.agregarConexion('Biblioteca',  'Oficinas Admin',    Camino(140, 2, 1, True,  'disponible'))
campus.agregarConexion('Biblioteca',  'Cafeteria',         Camino(160, 3, 3, True,  'disponible'))
campus.agregarConexion('Laboratorios','Bloque A',          Camino(110, 2, 2, False, 'mantenimiento'))
campus.agregarConexion('Laboratorios','Zona Deportiva',    Camino(350, 5, 1, True,  'disponible'))
campus.agregarConexion('Cafeteria',   'Teatro',            Camino(200, 3, 2, True,  'disponible'))
campus.agregarConexion('Cafeteria',   'Parqueadero Sur',   Camino(180, 3, 1, True,  'disponible'))
campus.agregarConexion('Teatro',      'Parqueadero Norte', Camino(300, 4, 1, True,  'bloqueado'))
campus.agregarConexion('Teatro',      'Enfermeria',        Camino(120, 2, 1, True,  'disponible'))
campus.agregarConexion('Enfermeria',  'Oficinas Admin',    Camino(100, 2, 1, True,  'disponible'))
campus.agregarConexion('Enfermeria',  'Parqueadero Sur',   Camino(260, 4, 1, True,  'disponible'))
campus.agregarConexion('Zona Deportiva','Parqueadero Norte',Camino(280, 4, 1, True, 'disponible'))
campus.agregarConexion('Parqueadero Norte','Parqueadero Sur',Camino(500,7, 1, True, 'disponible'))
campus.agregarConexion('Oficinas Admin','Parqueadero Sur',  Camino(230, 3, 1, True, 'disponible'))
    







 