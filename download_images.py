# Uso
# python download_images.py --urls urls.txt --output Imagens/PapaiNoel

# Importar os pacotes necessários
from imutils import paths
import argparse
import requests
import cv2
import os

# Pega os argumentos da chamada do comando
# Analisa os argumentos e valida
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())

# Pega as linhas da lista de URLs do arquivo de entrada e inicaliza
rows = open(args["urls"]).read().strip().split("\n")
# total = número total de imagens baixadas
total = 0

# loop URLs
for url in rows:
	try:
		#Tenta baixar a imagem
		r = requests.get(url, timeout=60)

		#Salva a imagem no disco
		p = os.path.sep.join([args["output"], "{}.jpg".format(
			str(total).zfill(8))])
		f = open(p, "wb")
		f.write(r.content)
		f.close()

		# Atualiza o contador
		print("[INFO] downloaded: {}".format(p))
		total += 1

	#Manipula se deu algo errado durante o processo de download
	except:
		print("[INFO] error downloading {}...skipping".format(p))

# Loop nas imagens para ver se tem arquivo corrompido
for imagePath in paths.list_images(args["output"]):
	# Auxiliar para deletar ou não a imagem
	delete = False

	# Tenta carregar a imagem
	try:
		image = cv2.imread(imagePath)

		#Se a imagem for "None", não é possivel carregá-la
		#Então deleta
		if image is None:
			print("None")
			delete = True

	#Se o OpenCV não puder carregar a imagem
	#É que pode estar corrompida então, deleta
	except:
		print("Except")
		delete = True

	# Checa se a imagem deve ser excluida
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)
