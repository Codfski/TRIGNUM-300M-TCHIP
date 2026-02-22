from typing import Any

import matplotlib.pyplot as plt


def plot_confusion_matrix(tp: int, fp: int, tn: int, fn: int):
    matrix = [[tp, fp], [fn, tn]]
    plt.imshow(matrix, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.colorbar()
    plt.show()

def display_illogics(sample: Any):
    # Placeholder: print or visualize detected illogics
    print("Illogics found:", getattr(sample, "illogics_found", []))
