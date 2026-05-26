# Sistema de Rutas - Campus UdeM

Aplicación que ayuda a estudiantes, docentes y visitantes a encontrar rutas eficientes dentro del campus universitario, usando algoritmos de grafos con restricciones del mundo real.

---

## Descripción del proyecto

El campus se modela como un grafo no dirigido donde cada **vértice** representa un lugar (bloques académicos, laboratorios, biblioteca, cafetería, parqueaderos, teatro, enfermería, zona deportiva, admisiones y entrada principal) y cada **arista** representa un camino entre dos lugares.

Cada camino tiene cinco atributos:

| Atributo     | Descripción                                              |
|--------------|----------------------------------------------------------|
| `distancia`  | Metros entre los dos lugares                             |
| `tiempo`     | Minutos estimados de recorrido                           |
| `congestion` | Nivel de tráfico del 1 (libre) al 5 (muy congestionado) |
| `accesible`  | Si el camino permite movilidad reducida                  |
| `estado`     | `disponible`, `bloqueado` o `mantenimiento`              |

El sistema implementa dos algoritmos:

- **Dijkstra** con criterio seleccionable: calcula la ruta óptima entre dos puntos según distancia, tiempo, congestión o accesibilidad. Ignora automáticamente los caminos bloqueados o en mantenimiento.
- **Prim (Árbol de Expansión Mínima)**: genera el recorrido de menor distancia total que conecta todos los lugares del campus, pensado para guías de visitantes.

---

## Cómo ejecutar el proyecto

**Requisitos:** Python 3.x (sin dependencias externas).

```bash
# Clonar el repositorio
git clone https://github.com/valbolnoy/optimizacion-de-recorridos-udem-.git
cd optimizacion-de-recorridos-udem-

# Ejecutar
python codigo-principal.py 
```

El script imprime en consola:
1. La ruta óptima entre `Entrada` y `Deportes` según cada uno de los 4 criterios disponibles, con el detalle de cada tramo.
2. El árbol de expansión mínima para el recorrido de visitantes, con la distancia total.

Para cambiar el origen, el destino o el criterio, modificar las llamadas al final del archivo:

```python
campus.mostrarRuta("Entrada", "Biblioteca", "tiempo")
campus.mostrarRuta("Parqueadero1", "Teatro", "accesible")