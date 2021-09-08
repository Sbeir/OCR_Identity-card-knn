import detect
import recognition_letters
import knn

def main():
    #detect
    detect.transform_image()
    recognition_letters.run_letters()
    nome_html, cognome_html = knn.run_knn()
    return nome_html, cognome_html

main()