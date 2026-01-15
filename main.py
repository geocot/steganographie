#Martin Couture https://github.com/geocot
#Janvier 2026
#Explication : https://youtu.be/MRve3jIFudI

from PIL import Image
image = "imageBase.jpg"
message = "Bonjour à tous!"

def formatageBinaire(valeur):
    return valeur[2:].rjust(8, '0')

def texteBinaire(texte):
    #Retourne une chaine de binaire
    chaineBinaire = ""
    for lettre in texte:
        chaineBinaire += formatageBinaire(bin(ord(lettre)))
    return chaineBinaire

def encodageBinaire(message, image):
    if len(message) < 256:
        # Traduction du message en binaire
        messageBinaire = texteBinaire(message)
        print("Le message en binaire est :", messageBinaire)
        # Calcul de la longueur du message en binaire
        longueurBinaire = formatageBinaire(bin(len(message)))
        print("La longueur en binaire :", longueurBinaire)
        # Ajout de la longueur au message
        binaireAEncoder = longueurBinaire + messageBinaire;
        print("Le binaire en encoder :", binaireAEncoder)

        # Ouverture de l'image
        im = Image.open(image)
        # Hauteur et largeur de l'image du tuple
        largeur, hauteur = im.size
        # On suppose que l'on a une image en RGB que l'on divise en 3
        r, g, b = im.split()
        # On va encoder dans une des trois bandes. Dans ce cas-ci, la première.
        canalRougeValeur = list(r.getdata())

        for j in range(len(binaireAEncoder)):
            canalRougeValeur[j] = 2 * int(canalRougeValeur[j] // 2) + int(binaireAEncoder[j])

        #Recréation du canal rouge de l'image
        nouveauRougeBinaire = Image.new("L", (largeur, hauteur))
        nouveauRougeBinaire.putdata(canalRougeValeur)

        #Assemblage du RGB
        nouvelleImage = Image.merge('RGB', (nouveauRougeBinaire, g, b))

        a,b,c = nouvelleImage.split()
        test = list(a.getdata())

        return nouvelleImage
    else:
        raise ValueError("Message trop long")

def decodageMessage(image):
    # Ouverture de l'image
    im = Image.open(image)
    # Hauteur et largeur de l'image du tuple
    largeur, hauteur = im.size
    # On suppose que l'on a une image en RGB que l'on divise en 3
    r, g, b = im.split()
    # On va encoder dans une des trois bandes. Dans ce cas-ci, la première.
    canalRougevaleur = list(r.getdata())
    #Longueur de la chaine dans le premier octet
    longueurBinaire = ""
    for j in range(8):
        longueurBinaire += str(canalRougevaleur[j]%2)
    longueurMessage = int(longueurBinaire,2)
    print(f"La longueur du message est de {longueurMessage} caractères" )
    #Lecture du message
    octet = ""
    message = ""
    for j in range(8,(longueurMessage+2)*8):
        if len(octet) < 8:
            octet += str(canalRougevaleur[j]%2)
        else:
            message += chr(int(octet, 2))
            octet = str(canalRougevaleur[j]%2)
    return message

#Encodage
nouvelleImage = encodageBinaire(message, image)
nouvelleImage.save("imageBaseEncode.png")

#Décodage
print(decodageMessage("imageBaseEncode.png"))



