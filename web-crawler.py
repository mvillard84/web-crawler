import requests
from bs4 import BeautifulSoup
import csv
import sys


def web_crawler(url, output_file="output.csv"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hay errores en la solicitud
        html_content = response.text

        # Analizar el contenido
        soup = BeautifulSoup(html_content, 'html.parser')

        # Guardar los links en un archivo CSV
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:  # Si el archivo está vacío, escribe la cabecera
                writer.writeheader()

            # Obtiene los headers (h1 a h6) y sus links
            for i in range(1, 7):
                titles = soup.find_all(f'h{i}')
                for title in titles:
                    title_text = title.text.strip()
                    link = title.find('a')
                    link_url = link.get('href') if link else "No link available"

                    # Imprimir en pantalla y guarda el resultado en un archivo CSV
                    print(f"Title: {title_text}")
                    print(f"URL: {link_url}")
                    writer.writerow({'Title': title_text, 'URL': link_url})

            # Obtiene los links del sitio y los rastrea en forma recursiva
            links = soup.find_all('a')
            for link in links:
                new_url = link.get('href')
                if new_url and new_url.startswith('http'):
                    web_crawler(new_url, output_file)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Verificar si se proporciona la URL y output como argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 web-crawler.py <target-url> <output-csv>")
        sys.exit(1)

    # Llamar a la función del web crawler
    web_crawler(sys.argv[1], sys.argv[2])
