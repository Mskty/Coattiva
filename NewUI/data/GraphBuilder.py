import itertools

import matplotlib.pyplot as plt
import numpy as np

class GraphBuilder:

    def plot_roc_curve(self,true_positive, false_positive, label=None):
        # fa comparire il grafico della roc_curve

        print(true_positive)
        plt.plot(true_positive, false_positive, linewidth=2, label=label)
        plt.plot([0, 1], [0, 1], 'k--', label="coin toss")
        plt.axis([0, 1, 0, 1])
        plt.legend(loc="lower right")
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')

    def plot_precision_recall(self, precision, recall):
        # fa comparire il grafico della precision vs recall con threshold della decision function (default 0)

        plt.plot(recall, precision, "b-", label="Precision")
        plt.axis([0, 1, 0, 1])
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.legend(loc="upper left")

    def plot_confusion_matrix(self, cm,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        Stampa in un grafico 2d la confusion matrix
        si può scegliere di normalizzare i risultati tra 0 e 1 passando True al parametro normalize.
        :param cm: confusion matrix da metodo di AlgorithmPipeline
        :param normalize:
        :param title:
        :param cmap:
        :return:
        """
        classes= ["Positiva", "Negativa"]

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=0)
        plt.yticks(tick_marks, classes)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            # print("Normalized confusion matrix")
        else:
            True  # print('Confusion matrix, without normalization')

        # print(cm)

        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, cm[i, j],
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')