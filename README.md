# Práctica Grafos: Optimización de Recorridos UdeM

Sistema que ayuda a estudiantes, docentes y visitantes a encontrar rutas eficientes dentro del campus de la UdeM, modelando los lugares como vértices de un grafo y los caminos como aristas ponderadas con múltiples atributos.

## Descripción del proyecto

El campus de la UdeM está representado como un grafo con más de 15 vértices que incluyen bloques académicos, laboratorios, biblioteca, cafetería, parqueaderos, teatro, enfermería, zonas deportivas y oficinas administrativas.

Cada camino entre dos lugares tiene los siguientes atributos:

- **Distancia** en metros
- **Tiempo** estimado de recorrido en minutos
- **Nivel de congestión** (1 = baja, 2 = media, 3 = alta)
- **Accesibilidad** para personas con movilidad reducida
- **Estado** del camino: disponible, bloqueado o en mantenimiento

El sistema implementa el algoritmo de Dijkstra adaptado para calcular rutas óptimas según diferentes criterios, ignorando automáticamente los caminos bloqueados o en mantenimiento. También incluye un árbol de expansión mínima (MST) para generar un recorrido guiado que conecte todos los lugares del campus con la menor distancia total.

## Funcionalidades

- Ruta más corta por distancia
- Ruta más rápida por tiempo (ajustada por congestión)
- Ruta con menor nivel de congestión
- Ruta accesible para personas con movilidad reducida
- Recorrido guiado por todos los lugares del campus usando árbol de expansión mínima
- Visualización de la ruta encontrada paso a paso y el costo total

## Cómo ejecutar el proyecto

El proyecto está desarrollado en Python y no requiere librerías externas, solo la librería estándar.

**1. Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd practica-grafos-udem
```

**2. Ejecutar en Google Colab**

Subir el archivo `practica_grafos_udem.py` a Google Colab desde `Archivo > Subir notebook` o pegando el contenido en una celda de código y ejecutando con `Shift + Enter`.

**3. Ejecutar localmente**

```bash
python practica_grafos_udem.py
```

No se necesita instalar nada adicional. El código funciona con Python 3.7 o superior.

## Estructura del código

```
practica-grafos-udem/
│
├── practica_grafos_udem.py   # Código principal
└── README.md
```

El archivo principal contiene:

- `Camino`: clase que representa los atributos de cada arista del grafo
- `GrafoListaCampus`: clase principal con la lista de adyacencia y todos los algoritmos
  - `recorrerEnAnchura()`: BFS
  - `recorrerEnProfundidad()`: DFS
  - `encontrarCaminoMasCorto()`: Dijkstra con soporte para múltiples criterios y restricciones
  - `arbolExpansionMinima()`: MST para el recorrido guiado de visitantes

## Supuestos asumidos

- Los caminos son bidireccionales, es decir, si hay un camino de A hacia B, también existe de B hacia A con los mismos atributos.
- El tiempo de recorrido se ajusta multiplicándolo por el nivel de congestión cuando se optimiza por tiempo, para reflejar que una ruta muy congestionada tarda más en la práctica.
- Los caminos con estado `bloqueado` o `mantenimiento` son ignorados completamente por todos los algoritmos, como si no existieran.
- Para la ruta accesible, se excluyen los caminos cuyo atributo `accesible` es `False`, independientemente de su estado.
- El árbol de expansión mínima se calcula solo sobre caminos disponibles y sin restricción de accesibilidad, ya que los visitantes no tienen restricciones de movilidad.
- Se asume que el grafo es conexo en condiciones normales. Si algún camino bloqueado desconecta el grafo, el sistema informa que no existe ruta disponible.