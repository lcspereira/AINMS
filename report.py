#!/usr/bin/python3
import pandas
import sys
import numpy as np
import matplotlib.pyplot as plt, mpld3

from sklearn.metrics import confusion_matrix, classification_report

test_file = sys.argv[1]
#train_file = '/etc/ainms/if_train.csv'
#test_file = 'if_test_data.csv'

dataset = pandas.read_csv (test_file)
test, truth = dataset.iloc[:,-2], dataset.iloc[:,-1]
data_graph = dataset.iloc[:,:-2]
res_graph = (test, truth)

print (confusion_matrix(truth, test, labels=[0, 1, 2, 3]))
print (classification_report (truth, test, target_names=['0', '1', '2', '3']))

try:
    fig, axes = plt.subplots (nrows=2, ncols=1, figsize=(20,6))
    #data_graph.plot.bar(ax=axes[0], width=2)
    data_graph.plot(ax=axes[0])
    axes[0].set_title("Visualização dos dados de teste")
    axes[0].set_ylabel ("%")
    #axes[0].axes.get_xaxis().set_visible (False)

    test.plot (ax=axes[1])
    truth.plot (ax=axes[1])
    axes[1].set_title("Predição X Verdade")
    axes[1].set_ylabel ("Código de saída")
    axes[1].legend()
    plt.show()
    with open("report.html", 'w') as html_chart: 
        html_chart.write (mpld3.fig_to_html (fig))
except Exception as ex:
    raise (ex)