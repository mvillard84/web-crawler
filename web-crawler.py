import requests
from bs4 import BeautifulSoup
import csv


def simple_crawler(url, output_file="links.csv"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hay errores en la solicitud
        html_content = response.text

        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Guardar los enlaces en un archivo CSV
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:  # Si el archivo está vacío, escribir encabezados
                writer.writeheader()

            # Obtener títulos (h1 a h6) y enlaces
            for i in range(1, 7):
                titles = soup.find_all(f'h{i}')
                for title in titles:
                    title_text = title.text.strip()
                    link = title.find('a')
                    link_url = link.get('href') if link else "No link available"

                    # Imprimir y guardar en el archivo CSV
                    print(f"Title: {title_text}")
                    print(f"URL: {link_url}")
                    writer.writerow({'Title': title_text, 'URL': link_url})

            # Obtener enlaces y rastrear recursivamente
            links = soup.find_all('a')
            for link in links:
                new_url = link.get('href')
                if new_url and new_url.startswith('http'):
                    simple_crawler(new_url, output_file)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


start_url = "[SITE-URL]"
output_file = "links.csv"

simple_crawler(start_url, output_file)
