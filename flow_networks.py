import sys
import csv
import glob

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.residual_edge = None

    def __repr__(self):
        return f"<Edge start:{self.start} end:{self.end} capacity:{self.capacity}>"

    def __str__(self):
        return f"{self.start},{self.end}"


class flow_networks:

    # Constructor
    def __init__(self):
        self.adjacency = {}
        self.flow = {}


    def add_edge(self, start, end, capacity : int):
        """
        Add edge to flow network

        Precondition: start != end and capacity > 0

        Parameters
        ----------
        start : str
            Start vertex of edge
        end : str
            End vertex of edge
        capacity : int
            Max capacity of edge

        Postcondition: Edge is added to adjacency list and flow list
        """
        edge = Edge(start,end,capacity)
        residual_edge = Edge(start,end,0)

        edge.residual_edge = residual_edge
        residual_edge.residual_edge = edge

        self.adjacency[start].append(edge)
        self.adjacency[end].append(residual_edge)

        self.flow[edge] = 0
        self.flow[residual_edge] = 0


    ''' Reads input file and stores as adjacency matrix with accompanying dictionary for node index '''
    def parse_file(self,file):
        with open(file, mode= 'r') as file:
            csvFile = csv.reader(file)

            # Populate adjacency list
            for line in csvFile:
                if line[0] not in self.adjacency:
                    self.adjacency[line[0]] = []
                if line[1] not in self.adjacency:
                    self.adjacency[line[1]] = []
                self.add_edge(line[0],line[1],int(line[2]))

    def find_path(self, source, sink, path):
        queue = [(source, path)]
        while queue:
            (source, path) = queue.pop(0)
            for edge in self.adjacency[source]:
                residual = edge.capacity - self.flow[edge]
                if residual > 0 and edge not in path and edge.residual_edge not in path:
                    if edge.end == sink:
                        return path + [edge]
                    else:
                        queue.append((edge.end, path + [edge]))


    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            print('path', path)
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.residual_edge] -= flow
            path = self.find_path(source, sink, [])
            # print 'flow', self.flow
        return sum(self.flow[edge] for edge in self.adjacency[source])


if len(sys.argv) == 1:
    files = glob.glob('network*.txt')
else:
    files = sys.argv[1:]

for file in files:
    # reading input file
    n = flow_networks()
    n.parse_file(file)

    # run Ford-Fulkerson algorithm on network
    max_flow = (n.max_flow('s','t'))

    # Output to file
    with open(file[:-4]+"_output.txt", 'w') as f:
        # printing out input file
        print(f'Input File: {file}\n', file=f)
        print("Input:", file=f)
        with open(file, 'r') as input:
            print(input.read(), file=f)

        # printing out network flow
        print("\nNetwork Flow:", file=f)
        for i in n.flow.items():
            if i[0].capacity != 0:
                print(f"{i[0]}\t flow:  {i[1]}/{i[0].capacity}", file=f)
        print(f"\nMax flow in this network is {max_flow}", file=f)