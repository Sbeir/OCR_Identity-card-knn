from os import listdir
from PIL import Image
import numpy as np


def knn_func():
    global scaler, classifier
    
    letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    X = []
    y = []
    for dir in listdir('train_set'):
        i = 0
        for filename in listdir('train_set/' + dir):
            img_data = Image.open(f'train_set/{dir}/{filename}')
            img_resized = img_data.resize((64,64))
            img_vector = np.array(img_resized).flatten()
            X.append(img_vector)
            y.append(letter[i])
            i += 1

    #KNN

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors = 3)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    #from sklearn import metrics
    #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    cognome_lett = []
    for x in listdir('img-process/letters_cognome'):
        x = Image.open('img-process/letters_cognome/' + x)
        x = x.resize((64, 64))
        x = np.array(x).flatten()
        cognome_lett.append(x)

    nome_lett = []
    for x in listdir('img-process/letters_nome'):
        x = Image.open('img-process/letters_nome/' + x)
        x = x.resize((64, 64))
        x = np.array(x).flatten()
        nome_lett.append(x)
        
    return nome_lett, cognome_lett


def test(prova):
    X_test = prova
    X_test = scaler.transform(X_test)
    y_pred = classifier.predict(X_test)
    #print("MY y_pred", y_pred)
    return y_pred

def result(nome, cognome):   
    nome_html = ''.join(test(nome)).capitalize()
    cognome_html = ''.join(test(cognome)).capitalize()
    #print(nome_html, cognome_html)
    return nome_html, cognome_html

def run_knn():
    nome_lett, cognome_lett = knn_func()
    nome_html, cognome_html = result(nome_lett, cognome_lett)
    return nome_html, cognome_html
 
 