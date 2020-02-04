import sys
import warnings

from Data_Loader import *
from Pulizia.Storic_PF_Cleaner import *
from Pulizia.Storic_PG_Cleaner import *
from Preprocessamento.PF_Prepare import *
from Preprocessamento.PG_Prepare import *
from Preprocessamento.Train_Test_Splitter import *
from Preprocessamento.Data_Scaler import *
from Preprocessamento.Data_Undersampler import *
from Modellazione.Model_Trainer import *

"""
Script principale da cui runna la shell
"""
# Ignore all warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Variabili globali placeholdeer
trainset, testset, currentdf = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
limiteinput = 10
print("INIZIO ESECUZIONE SHELL \n")

# Caricamento dati storici
print("Carica il file contenente i dati storici in formato csv...")
dfPF, dfPG = load_storic_data()
print("File csv caricato correttamente! \n")

# Pulizia dati storici
print("Ora i dati storici contenenti i titoli di persone fisiche e giuridiche verranno preparati...")
dfPFclean = clean_storic_pf(dfPF)
dfPGclean = clean_storic_pg(dfPG)
print("Pulizia dati storici completata! \n")

# Preparazione dati storici
print("Ora i dati storici verranno preparati per l'elaborazione...")
dfPFprepared = prepare_pf(dfPFclean)
dfPGprepared = prepare_pg(dfPGclean)
print("Preparazione dati storici completata! \n")

# scelta pf o pg
typepfpg = "PF"
inp = ''
dialog = ''
counter = 0
while inp != "1" and inp != "2" and counter < limiteinput:
    counter += 1
    inp = input("Ora i 2 dataset sono pronti per l'elaborazione, con quale vuoi continuare? \n 1: Persone Fisiche \n 2: Persone Giuridiche")

if inp == "1":
    typepfpg = "PF"
    currentdf = dfPFprepared
elif inp == "2":
    typepfpg = "PG"
    currentdf = dfPGprepared
else:
    print("ERRORE")
    sys.exit()
    # TODO ERRORE E BREAKPOINT
if typepfpg == "PF":
    dialog = "Persone Fische"
else:
    dialog = "Persone Giuridiche"
print("Stai utilizzando i dati riguardanti " + dialog + "\n")

# train test splitter
choices = train_test_splitter_possibilities(currentdf)
inprange = list(map(str, list(range(1, len(choices) + 1))))
inp = ''
dialog = "Selezione esempi che faranno parte del training set: \n"
counter = 0
# generazione messaggio per l'input
for i in inprange:
    dialog = dialog + i + ": fino a ruolo :" + str(choices.iloc[int(i) - 1].ruolo) \
             + " esempi training: " + str(choices.iloc[int(i) - 1].nesempi) + " di cui buoni pagatori: " \
             + str(choices.iloc[int(i) - 1].true)
    dialog = dialog + "\n"
while not (inp in inprange) and counter < limiteinput:
    counter += 1
    inp = input(dialog)

if inp in inprange:
    # Suddivido training e testset come desiderato dall'utente
    # Seleziono le righe con iloc, devo selezionare le prime x righe dove x è l'input dell'utente
    train_dates = list()
    for i in range(0, int(inp)):
        train_dates.append(str(choices.iloc[i].ruolo))
    # Ottengo trainset e testset
    trainset, testset = train_test_splitter(currentdf, train_dates, typepfpg)
else:
    print("ERRORE")
    sys.exit()
    # TODO ERRORE E BREAKPOINT
print("Suddivisione training set e test set completata! \n")

# Salvo il testset originale nel caso voglia essere salvato e venga trasformato con scaling per l'elaborazione
original_testset = testset.copy()

# Selezione algoritmo di apprendimento, utilizzando gli iperparametri di default di scikit-learn 0.22
inp = ''
counter = 0
classifier = None
while inp != "1" and inp != "2" and inp != "3" and inp != "4" and inp != "5" and counter < limiteinput:
    counter += 1
    inp = input("Seleziona l'algoritmo di apprendimento: \n 1: Logistic Regression \n "
                "2: Support Vector Machine \n 3: Decision Tree \n 4: Random Forest \n 5: XgBoost")
if inp == "1":
    classifier = skl.linear_model.LogisticRegression(solver="lbfgs", max_iter=10000)
elif inp == "2":
    classifier = svm.SVC(kernel="rbf", gamma="scale")
elif inp == "3":
    classifier = skl.tree.DecisionTreeClassifier()
elif inp == "4":
    classifier = RandomForestClassifier(n_estimators=100)
elif inp == "5":
    classifier = xgb.XGBClassifier()
else:
    print("ERRORE")
    sys.exit()
    # TODO ERRORE E BREAKPOINT
print("Modello di tipo " + classifier.__class__.__name__ + " istanziato con successo!\n")

# Selezione undersampling o no
inp = ''
counter = 0
undersampling = None  # di default nessuno scaler

while inp != "1" and inp != "2" and counter < limiteinput:
    counter += 1
    inp = input("Vuoi effettuare undersampling sui dati di training? \n 1: No \n 2: Si ")

if inp == "1":
    print("Non è stato applicato undersampling \n")
elif inp == "2":
    trainset = data_undersample(trainset)
    print("Training set trasformato attraverso undersampling con successo!\n")
else:
    print("ERRORE")
    sys.exit()
    # TODO ERRORE E BREAKPOINT

# Selezione tipo scaling (addestrato su training set e poi lo applica su test set se presente)
inp = ''
counter = 0
scaler = None  # di default nessuno scaler

while inp != "1" and inp != "2" and inp != "3" and counter < limiteinput:
    counter += 1
    inp = input("Seleziona il tipo di normalizzazione da applicare sui dati: \n 1: Nessuna \n 2: Standard Scaler \n "
                "3: MinMax Scaler")
if inp == "1":
    print("Non è stato applicato nessuno scaling \n")
elif inp == "2":
    trainset, testset, scaler = feature_scaling(trainset, testset, minmax=False, tipo=typepfpg)
    print("Operazione di scaling dei dati avvenuta con successo!\n")
elif inp == "3":
    trainset, testset, scaler = feature_scaling(trainset, testset, minmax=True, tipo=typepfpg)
    print("Operazione di scaling dei dati avvenuta con successo!\n")
else:
    print("ERRORE")
    sys.exit()
    # TODO ERRORE E BREAKPOINT

# addestramento modello e riporto risultati su test set se presente
print("Ora il modello verrà addestrato sul training set...")
classifier = train(classifier, trainset)
print("Addestramento del modello completato! \n")

if not testset.empty:
    print("Ecco i risultati sul test set: \n")
    predictions_test=report_test(classifier, testset)
    # richiesta salvataggio su file di test set
    inp = ''
    counter = 0
    while inp != "1" and inp != "2" and counter < limiteinput:
        counter += 1
        inp = input("Vuoi salvare le predizioni sul test set per visionarle su file? \n 1: No \n 2: Si ")
    if inp == "1":
        print("Le previsioni su test set non saranno salvate \n")
    elif inp == "2":
        # salvataggio test set su file con predizioni
        print("Seleziona dove salvare in formato csv i risultati: \n")
        original_testset["Predizioni"] = predictions_test
        save_data(original_testset)
        print("Le predizioni per il test set sono state salvate su file con successo! \n")
else:
    print("Non è stato selezionato un test set, procedi con il caricamento di un file esterno su cui effettuare le previsioni \n")


# caricamento file csv out of sample per effettuare predizioni
if typepfpg == "PF":
    dialog = "Persone Fische"
else:
    dialog = "Persone Giuridiche"

print("Carica il file .csv esterno su cui effettuare delle predizioni, deve contenere dei dati riferiti a " + dialog + "...")
external_df = load_new_data()
print("Caricamento del file avvenuto con successo! \n")

# DEBUG se voglio utilizzare un dataset che contiene anche una label di classe (es out of sample da dati storici)
labelpresent = False
labels = None
if "label" in external_df.columns:
    labelpresent=True
    labels=external_df["label"]
    external_df.drop(columns="label",inplace=True)

# preparazione dei dati su file caricato
print("Ora i dati ottenuti dal file verrano preparati e classificati...")
if typepfpg == "PF":
    external_dfprepared = prepare_pf(external_df)
else:
    external_dfprepared = prepare_pg(external_df)

# ho ottenuto il dataset preparato pronto per essere utilizzato nella classificazione (i dati esterni non devono avere nè label nè DataCaricoTitolo)
if scaler is not None:
    # se ho utilizato uno scaler per normalizzare devo utilizzarlo anche sui nuovi dati
    external_dfprepared = use_scaler(external_dfprepared, scaler)
# ottengo le predizioni:
predictions = classifier.predict(external_dfprepared.to_numpy())

print("Operazione completata! di " + str(len(predictions)) + " crediti ne sono stati classificati come positivi "
      + str(np.count_nonzero(predictions)) + " e come negativi " + str(len(predictions) - np.count_nonzero(predictions)) + "!")

# attacco le predizioni al dataset originale per esportarlo in formato csv
external_df["Predizioni"] = predictions

# DEBUG ri-attacco le labels se erano presenti:
if labelpresent is True:
    external_df["label"] = labels

print("Seleziona dove salvare in formato csv i risultati: \n")
save_data(external_df)

print("Operazione completata! il file csv conterrà i dati originali con aggregata una nuova colonna 'Predizioni' "
      "che conterrà i valori: \n 1 se il credito è stato classificato come positivo  "
      "\n 0 se il credito è stato classificato come negativo")

