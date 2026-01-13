import requests
import csv
import os

class sentence1:
    def __init__(self):
        self.base_url = "https://api.deezer.com"
        # ID de México en Deezer es 196. usar 0 para el Top Global.
        self.region_id = "0" 

    def get_top_tracks(self):
        """Obtiene el top de canciones de la región seleccionada."""
        url = f"{self.base_url}/chart/{self.region_id}/tracks"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"Error al conectar con Deezer: {response.status_code}")
            return []

    def get_genre_name(self, album_id):
        """Obtiene el género principal de un álbum específico."""
        url = f"{self.base_url}/album/{album_id}"
        response = requests.get(url)
        if response.status_code == 200:
            genres = response.json().get('genres', {}).get('data', [])
            return genres[0]['name'] if genres else "Unknown"
        return "Unknown"

    def process_and_save(self):
        print(f"Iniciando extracción para región ID: {self.region_id}...")
        tracks = self.get_top_tracks()
        
        # Diccionario para agrupar canciones por género
        # { 'Rock': [cancion1, cancion2], 'Pop': [...] }
        genre_map = {}

        for track in tracks:
            print(f"Procesando: {track['title']} - {track['artist']['name']}")
            
            # Deezer no da el género en el track, hay que consultarlo vía el álbum
            genre = self.get_genre_name(track['album']['id'])
            
            if genre not in genre_map:
                genre_map[genre] = []
            
            genre_map[genre].append({
                'Rank': track['position'],
                'Title': track['title'],
                'Artist': track['artist']['name'],
                'Album': track['album']['title'],
                'Link': track['link']
            })

        # Crear archivos CSV por cada género
        if not os.path.exists('output'):
            os.makedirs('output')

        for genre, data in genre_map.items():
            filename = f"output/top_{genre.lower().replace(' ', '_')}.csv"
            keys = data[0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            
            print(f"Archivo generado: {filename} con {len(data)} canciones.")

if __name__ == "__main__":
    reto = sentence1()
    reto.process_and_save()