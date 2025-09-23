# 🗺️ Mapa SEN Consulta

El presente script muestra de forma interactiva elementos del SEN bajo el siguiente menú de opciones.

- La distancia entre dos subestaciones (barras) seleccionadas.
- La subestación más cercana a un punto ingresado por el usuario en coordenadas (LAT/LONG).

El mapa se genera en formato HTML y muestra únicamente el territorio nacional con una capa construida por medio de un archivo geojson, ocultando por completo cualquier otro detalle cartográfico.

---

### 📦 Instalación de Librerias / Dependencias

Las dependencias o librerias necesarias son:

```bash
pip install pandas folium geopy shapely geopandas openpyxl


⚠️ Importante: En Windows, la instalación de geopandas puede requerir tener GDAL o fiona correctamente configurados.

---

## 📁 Archivos requeridos

- `placemarks.xlsx`: archivo Excel con una columna llamada `Coordenadas`, en formato `"longitud, latitud"`, y una columna `Nombre`.
- `chile_geo.geojson`: archivo GeoJSON que contiene el contorno del territorio nacional de Chile (MultiPolygon o Polygon).

---

## 🚀 Ejecución

Ejecuta el script principal en la terminal:

```bash
python mapa_subestaciones.py

--- 

## 🚀 Funciones Principales

| Función                            | Descripción                                                         | Detalles técnicos                                           |
| ---------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------- |
| `extraer_coordenadas()`            | Convierte una cadena `"lon, lat"` a coordenadas (latitud, longitud) | Corrige signos para asegurar que los valores estén en Chile |
| `obtener_subestacion_por_codigo()` | Busca una subestación cuyo nombre comience con un código específico | Devuelve la primera coincidencia con el prefijo             |
| `geodesic()` (de `geopy.distance`) | Calcula distancia geográfica entre dos coordenadas                  | Retorna distancia en kilómetros                             |
| `folium.Map()`                     | Crea el mapa de Folium                                              | `tiles=None` para eliminar fondo cartográfico               |
| `folium.GeoJson()`                 | Agrega el contorno de Chile al mapa                                 | Chile se muestra en blanco con borde negro                  |
| `folium.Marker()`                  | Agrega marcadores al mapa                                           | Representa subestaciones, puntos de usuario, etiquetas      |
| `folium.PolyLine()`                | Dibuja líneas entre puntos seleccionados                            | Usa colores para diferenciar conexiones                     |
| `mapa.fit_bounds()`                | Ajusta la vista del mapa a los puntos relevantes                    | Se usa para enfocar el área de interés                      |
