
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
  