from bs4 import BeautifulSoup
import requests
import csv
import re

# Fonction pour formatter l'URL de recherche en fonction des critères spécifiés.
def url_nav(page):
    
    # Formatage de l'URL
    url = """https://www.barreaudenice.com/annuaire/avocats/?fwp_paged={page}""".format(page=page)
    return url



# Fonction pour scraper le barreau de Nice, les informations sur les avocats et les stocker dans un fichier CSV
def main():

    annuaire = []
    
    # SCRAPING de la page 1 à 50 de résultat de recherche pour extraire les informations sur les avocats

    for page in range(1, 50):
        url = url_nav(page)

        requete = requests.get(url)

        soup = BeautifulSoup(requete.text, 'html.parser')

        avocats = soup.find_all('div', class_='callout secondary annuaire-single')
        
        if not avocats:
            annuaire.append([f'Page {page} : L\'annuaire recherché est introuvable', 'no_data', 'no_data', 'no_data', 'no_data', 'no_data'])
            print(f"{url} : l'annuaire recherché est introuvable")

        # Extraire les informations de chaque avocat de la page.

        for avocat in avocats:
            nom = avocat.find('h3').text.strip()
            serment = avocat.find('span', class_='date').text.strip()
            adresse = avocat.find('span', class_='adresse').text.strip()
            # nettoyage de l'adresse avec un regex
            adresse_regex = re.sub(r"\s+", " ", adresse)
            
            try:
                telephone = avocat.find('span', class_='telephone').text.strip()
            except AttributeError as e:
                telephone = "telephone indisponible"  
                  
            try:    
                email = avocat.find('span', class_='email').a.text.strip()
            except AttributeError as e:
                email = "email indisponible"   


            if avocat:
                print("Nom :", nom, "Date de Serment  :", serment, "Adresse :", adresse_regex, '\n',
                      "Telephone :", telephone, '\n', "Adresse mail :", email,)

                annuaire.append([nom, serment, adresse_regex, telephone, email])   
                

    
    # Récolte des données récupérées dans un fichier CSV
    with open("annuaire.csv", "a", newline="") as fd:
        writer = csv.writer(fd)
        writer.writerow(
            ["Nom", "Date de Serment", "Adresse", "Telephone", "Adresse mail",])
        for row in annuaire:
            writer.writerow(row)

# bloc d'exécution conditionnelle (plus sécurisé)
if __name__ == "__main__":
    main()

    