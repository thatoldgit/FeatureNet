from lite_models import *
from  sqlalchemy.sql.expression import func
import sys
import igraph
from igraph import *

def create_test_data_set(s, size, file = sys.stdout):
    """ s: session
        size: stop when min size artists are reached."""

    artists = list()
    _artists = list()

    # provide enough artists (some may be skipped due to zero collaborations)
    artists_iterator = iter(s.query(Artist).order_by(func.random()).limit(size*10).all())

    while (len(artists) < size or len(_artists)>0):
        if len(_artists) == 0:
            # start with random artist
            while (True):
                try:
                    artist = next(artists_iterator)
                    break
                except StopIteration:
                    artists_iterator = iter(s.query(Artist).order_by(func.random()).limit(size*2).all())

            artists.append(artist)
        else:
            # start with artist that has already been encountered but not followed up upon
            artist =_artists.pop(0)


        for a in artist.collaborators:
            if a not in artists and a not in _artists and len(artists) < size:
                artists.append(a)
                _artists.append(a)

    return artists

def artists_to_edges_file (artists, file=sys.stdout):
   # f= open(filename, "w+")
    for a1 in artists:
        for c in a1.left_cs:
            a2 = c.right
            #f.write('"{}" "{}"\n'.format(a1.name, a2.name))
            print('"{}" "{}"'.format(a1.name, a2.name), file=file)

def load_from_file (filename):
    #g = Graph.Read_GraphML(filename)
    g = Graph.Read_Pickle(filename)
    return g

def save_to_file (filename, g):
    f = open(filename, "w+")
    Graph.write_pickle(g, filename)
    #Graph.write_gml(g,filename)
    f.close()

def artists_to_graph (artists):
    g = Graph()
    g.add_vertices (len(artists))

    names = list()
    e_colors = list()

    for a1 in artists:
        # set name
        names.append(a1.name)

        # add eges
        for c in a1.left_cs:
            a2 = c.right
            if not a2 in artists:
                continue

            e = g.get_eid(artists.index(a1), artists.index(a2), error=False)
            # returns valueerror if not found
            if e == -1:
                if artists.index(a1) == artists.index(a2):
                    continue
                g.add_edge(artists.index(a1), artists.index(a2), width=1)
                # g.add_edges([(artists.index(a1), artists.index(a2))])
                if c.is_feature:
                    e_colors.append("blue")
                else:
                    e_colors.append("black")

            else:
                e = g.es[e]
                e["width"] += 0.5
    g.vs["label"] = names
    g.vs["color"] = ["white"]*len(artists)
    g.vs["size"] = [60]*len(artists)
    g.es["color"] = e_colors
    #g.simplify(combine_edges=sum)
    return g


if __name__ == "__main__":
#def old():
    Session = sessionmaker(bind=db)
    s = Session()
    num_artists = s.query(Artist).count()
    print ("{} artists in database.".format(num_artists))

    #track = s.query(Track).order_by(func.random()).first()
    #print (track.name)
    #for artist in track.artists:
    #    print(artist.name)
    for e in range(1):
    #print("Creating test data.")
        artists = create_test_data_set(s, 90000)
        artists_to_edges_file(artists)

    #print("Creating graph from test data.")
        g = artists_to_graph(artists)
        g.to_directed()
        save_to_file("test"+str(e)+".graph",g)
    #gra = load_from_file("2.graph")

    #print(g.vcount())

    #print ("Rendering graph.")

        layout = g.layout("kk")
    #for v in g.vs:
    #    print(v)
    #for e in g.es.select(lambda edge: edge["width"] > 1):
    #    print(e["width"])
    #    print(g.vs(e.source)["label"])
    #    print(g.vs(e.target)["label"])
    #   print("\n")
        plot(g, "test"+str(e)+".png",
            layout = layout, directed=True,
            bbox = (2400, 1600), margin = 100)


    print ("Done.")