
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
  