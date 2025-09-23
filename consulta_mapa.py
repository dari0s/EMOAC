import pandas as pd
import folium
import json
from geopy.distance import geodesic

# === Cargar datos ===

# Cargar GeoJSON del contorno de Chile
with open("chile_geo.geojson", "r", encoding="utf-8") as f:
    chile_geojson = json.load(f)

# Cargar Excel de subestaciones
df = pd.read_excel("placemarks.xlsx")

# === Funciones auxiliares ===

def extraer_coordenadas(coord_str):
    try:
        parts = coord_str.split(",")
        if len(parts) != 2:
            return None, None
        lon = float(parts[0].strip())
        lat = float(parts[1].strip())
        if lon > 0:
            lon = -lon
        if lat > 0:
            lat = -lat
        return lat, lon
    except:
        return None, None

def obtener_subestacion_por_codigo(codigo):
    resultado = df[df['Nombre'].str.startswith(str(codigo) + "_")]
    if resultado.empty:
        raise ValueError(f"No se encontró subestación con código {codigo}")
    return resultado.iloc[0]

# Extraer coordenadas del Excel
df[['Latitud', 'Longitud']] = df['Coordenadas'].apply(lambda x: pd.Series(extraer_coordenadas(x)))
df = df.dropna(subset=['Latitud', 'Longitud'])

# === Menú de opciones ===
print("Seleccione una opción:")
print("1. Ingresar un punto y encontrar la subestación más cercana")
print("2. Ingresar dos subestaciones y calcular la distancia entre ellas")
opcion = input("Ingrese 1 o 2: ").strip()

# === Crear mapa SIN fondo, centrado en Chile ===
mapa = folium.Map(location=[-35.5, -71.5], zoom_start=6, tiles=None)

# === Agregar SOLO el contorno de Chile (relleno blanco) ===
folium.GeoJson(
    chile_geojson,
    name="Chile",
    style_function=lambda feature: {
        "fillColor": "white",    # Relleno blanco
        "color": "black",        # Borde negro
        "weight": 1,
        "fillOpacity": 1.0       # Totalmente opaco
    }
).add_to(mapa)

# === Lógica según opción seleccionada ===

if opcion == "1":
    # Punto de consulta
    lat_usuario = float(input("Ingrese latitud del punto de consulta (ej: -35.5): "))
    lon_usuario = float(input("Ingrese longitud del punto de consulta (ej: -71.5): "))
    if lon_usuario > 0:
        lon_usuario = -lon_usuario
    if lat_usuario > 0:
        lat_usuario = -lat_usuario

    punto_usuario = [lat_usuario, lon_usuario]

    # Calcular subestación más cercana
    df['Distancia_al_usuario_km'] = df.apply(
        lambda row: geodesic(punto_usuario, (row['Latitud'], row['Longitud'])).km,
        axis=1
    )
    sub_mas_cercana = df.loc[df['Distancia_al_usuario_km'].idxmin()]
    coord_cercana = [sub_mas_cercana['Latitud'], sub_mas_cercana['Longitud']]
    distancia_usuario_km = df['Distancia_al_usuario_km'].min()

    print(f"Subestación más cercana: {sub_mas_cercana['Nombre']} ({distancia_usuario_km:.2f} km)")

    # Marcadores y línea
    folium.Marker(
        location=punto_usuario,
        popup="Punto consulta",
        tooltip="Punto consulta",
        icon=folium.Icon(color="green", icon="map-marker")
    ).add_to(mapa)

    folium.Marker(
        location=coord_cercana,
        popup=sub_mas_cercana['Nombre'],
        tooltip="Más cercana: " + sub_mas_cercana['Nombre'],
        icon=folium.Icon(color="orange", icon="bolt", prefix="fa")
    ).add_to(mapa)

    folium.PolyLine([punto_usuario, coord_cercana], color="purple", weight=2, dash_array="5").add_to(mapa)

    mid_usuario = [(punto_usuario[0] + coord_cercana[0]) / 2, (punto_usuario[1] + coord_cercana[1]) / 2]
    folium.Marker(
        location=mid_usuario,
        icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: purple;">{distancia_usuario_km:.2f} km</div>')
    ).add_to(mapa)

    mapa.fit_bounds([punto_usuario, coord_cercana])

elif opcion == "2":
    # Comparar subestaciones
    codigo1 = input("Ingrese el código de la primera subestación (ej: 238): ").strip()
    codigo2 = input("Ingrese el código de la segunda subestación (ej: 575): ").strip()

    try:
        sub1 = obtener_subestacion_por_codigo(codigo1)
        sub2 = obtener_subestacion_por_codigo(codigo2)
    except ValueError as e:
        print(e)
        exit()

    coord1 = [sub1['Latitud'], sub1['Longitud']]
    coord2 = [sub2['Latitud'], sub2['Longitud']]

    distancia_subs_km = geodesic(coord1, coord2).km
    print(f"Distancia entre {sub1['Nombre']} y {sub2['Nombre']}: {distancia_subs_km:.2f} km")

    folium.Marker(
        location=coord1,
        popup=sub1['Nombre'],
        tooltip=sub1['Nombre'],
        icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
    ).add_to(mapa)

    folium.Marker(
        location=coord2,
        popup=sub2['Nombre'],
        tooltip=sub2['Nombre'],
        icon=folium.Icon(color="blue", icon="bolt", prefix="fa")
    ).add_to(mapa)

    folium.PolyLine([coord1, coord2], color="red", weight=3).add_to(mapa)

    mid_subs = [(coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2]
    folium.Marker(
        location=mid_subs,
        icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: red;">{distancia_subs_km:.2f} km</div>')
    ).add_to(mapa)

    mapa.fit_bounds([coord1, coord2])

else:
    print("Opción no válida.")
    exit()

# === Guardar mapa ===
mapa.save("mapa_subestaciones.html")
print("Mapa generado y guardado como mapa_subestaciones.html")
