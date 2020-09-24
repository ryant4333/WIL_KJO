import sys
import matplotlib.pyplot as plt

sys.path.insert(1, "./src/")
import plot_graph

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise AttributeError("Missing directory to objective log")
    f = sys.argv[1]

    if len(sys.argv) < 3:
        title = None
    else:
        title = sys.argv[2]
    
    plot_graph.graph(f, title)
    plt.show()

    
    