from lite_models import *
from  sqlalchemy.sql.expression import func
import sys
import igraph
from igraph import *

def load_from_file (filename):
    g = Graph.Read_Pickle(filename)
    return g

def save_to_file (filename, g):
    f = open(filename, "w+")
    Graph.write_pickle(g, filename)
    #Graph.write_gml(g,filename)
    f.close()

def print_dif_layout(g,i):
    layout = g.layout_kamada_kawai()
    filename = str(i)+"kamada_kawai.png"
    plot(g, filename,
         layout=layout, directed=True,
         bbox=(2400, 1600), margin=100)
    layout= g.layout_fruchterman_reingold()
    filename = str(i) + "fruchterman_reingold.png"
    plot(g, filename,
         layout=layout, directed=True,
         bbox=(2400, 1600), margin=100)
    layout = g.layout_grid()
    filename = str(i) + "grid.png"
    plot(g, filename,
         layout=layout, directed=True,
         bbox=(2400, 1600), margin=100)
    layout = g.layout_lgl()
    filename = str(i) + "lgl.png"
    plot(g, filename,
         layout=layout, directed=True,
         bbox=(2400, 1600), margin=100)
    layout = g.layout_reingold_tilford()
    filename = str(i) + "reingold_tilford.png"
    plot(g, filename,
         layout=layout, directed=True,
         bbox=(2400, 1600), margin=100)


def print_dif_centralities(g,i):
    g.vs["size"] = g.betweenness(directed=True,weights="width")
    listb =  g.vs["size"]
    for v in g.vs:
        v["size"] = (v["size"]+35)*2
    plot(g, str(i)+"betweenness.png",
         layout=g.layout_kamada_kawai(), directed=True,
         bbox=(2400, 1600), margin=100)
    g.vs["size"] = g.hub_score(weights="width")
    for v in g.vs:
        v["size"] = (v["size"] + 35) * 2
    plot(g, str(i) + "hub_score.png",
         layout=g.layout_kamada_kawai(), directed=True,
         bbox=(2400, 1600), margin=100)
    g.vs["size"] = g.authority_score()#weights="width")
    for v in g.vs:
        v["size"] = (v["size"] + 35) * 2
    plot(g, str(i) + "authority_score.png",
         layout=g.layout_kamada_kawai(), directed=True,
         bbox=(2400, 1600), margin=100)
    #g.vs["size"] = listb
    # g.assortativity_degree()#("size")  # weights="width")


def print_g_values(g,filename):
    f = open(filename, "w+")
    f.write("Assortativity Degree: " + str(g.assortativity_degree())+"\n")
    #f.write("Assortativity: " + str(g.assortativity()) + "\n")
    f.close()

def small_print(g):
    g.vs["size"] = g.betweenness(directed=True,weights="width")
    for v in g.vs:
        v["size"] = (v["size"]+35)*2
    plot(g, str(i)+"betweenness_width.png",
         layout=g.layout_kamada_kawai(), directed=True,
         bbox=(2400, 1600), margin=100)

    g.vs["size"] = g.betweenness(directed=True)
    for v in g.vs:
        v["size"] = (v["size"]+35)*2
    plot(g, str(i)+"betweenness.png",
         layout=g.layout_kamada_kawai(), directed=True,
         bbox=(2400, 1600), margin=100)

    pro = sum(g.vs["spotify"])
    for v in g.vs:
        v["size"] = ((v["spotify"] * 100 / pro)+35)*2
    plot(g, str(i) + "aufrufe.png",
         layout=g.layout("kk"), directed=True,
         bbox=(2400, 1600), margin=100)

def cleanup(g):
    g.delete_vertices({0,1,2,3,4})
    save_to_file(i+".graph",g)

def add_info(g):
    g.vs["spotify"] = [0, 9949734, 18520457, 19790796, 7146906,
                       580123, 404702, 442, 27657, 0, 2814, 9173, 2316064, 0, 32930]
    g.vs["type"] = ["u", "g", "a", "a", "a", "a", "a", "a", "a",
                    "u", "a", "a", "a", "a", "a"]
    # g.vs["type"] = {"unknown", "group" , "artist", "artist", "artist", "artist", "artist", "artist",  }
    g.vs["genre"] = ["unknown", "hip hop", "rap", "rap", "rap", "rap",
                     "rap", "rap", "rap", "unknown", "rap", "rap", "soul", "rap", "r&p"]
    save_to_file(str(i) + "info.graph", g)

if __name__ == "__main__":
#def ifail():
    i = "test11"
    g = load_from_file(str(i)+"info.graph")
    plot(g, str(i) + ".png",
        layout=g.layout("kk"), directed=True,
        bbox=(2400, 1600), margin=100)
    small_print(g)
    #print_dif_centralities(g1,i)
    #print_g_values(g,str(i)+"info.txt")
    #g2 = load_from_file("4.graph")
    #g3 = load_from_file("10.graph")
    #layout = g.layout("kk")

