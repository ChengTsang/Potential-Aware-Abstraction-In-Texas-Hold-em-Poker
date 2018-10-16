""" Script that drives the kmean algorithm after parsing the user parameters.

The user inputed parameters are used to customize the kmean algorithm's
parameters. The progress of the convergence of the optimal clustering is shown
in each iteration using pyplot.
"""
import numpy
#matplotlib.use('GTKAgg') # For linux gtk
from pyemd import emd

userArgs = None

class Clustering():

    """Class that solves the problem of clustering a set of random data points
    into k clusters.

    The process is iterative and visually shown how the clusters convergence on
    the optimal solution.
    """

    def __init__(self):
        """Default constructor.
        """
        pass

    def points_best_cluster(self, centroids, dataPoint):
        """Takes the dataPoint and find the centroid index that it is closest too.

        Args:
          centroids: The list of centroids
          dataPoint: The dataPoint that is going to be determined which centroid it
            is closest too
        """
        closestCentroid = None
        leastDistance = None
        matrix = numpy.array([[0,1/3.0,2/3.0],[1/3.0,0,1/3.0],[2/3.0,1/3.0,0]])

        for i in range(len(centroids)):
            distance = emd(numpy.array(dataPoint),numpy.array(centroids[i]),matrix)
            #print(distance)
            if (leastDistance == None or distance < leastDistance ):
                closestCentroid = i
                leastDistance = distance

        return closestCentroid

    def new_centroid(self, cluster):
        """Finds the new centroid location given the cluster of data points. The
        mean of all the data points is the new location of the centroid.

        Args:
          cluster: A single cluster of data points, used to find the new centroid
        """
        #print(cluster)
        return numpy.mean(cluster, axis = 0)

    def configure_clusters(self, centroids, dataPoints):
        """Creates a new configuration of clusters for the given set of dataPoints
        and centroids.

        Args:
          centroids: The list of centroids
          dataPoints: The set of random data points to be clustered

        Return:
            The set of new cluster configurations around the centroids
        """
        # Create the empty clusters
        clusters = []
        for i in range(len(centroids)):
            cluster = []
            clusters.append(cluster)

        # For all the dataPoints, place them in initial clusters
        for i in range(len(dataPoints)):
            idealCluster = self.points_best_cluster(centroids, dataPoints[i])
            clusters[idealCluster].append(dataPoints[i])
        #NOTE:it is dangerous
        max = 0
        blank = []
        for i in range(len(clusters)):
            if len(clusters[i]) > max:
                max = i
            if len(clusters[i]) == 0:
                blank.append(i)
        for i in range(len(blank)):
            clusters[blank[i]].append(clusters[max].pop())
        return clusters

    def get_cluster_RSS(self, cluster, centroid):
        """Calculates the cluster's Residual Sum of Squares (RSS)

        Args:
          cluster: The list of data points of one cluster
          centroid: The centroid point of the corresponding cluster
        """
        sumRSS = 0
        matrix = numpy.array([[0, 1 / 3.0, 2 / 3.0], [1 / 3.0, 0, 1 / 3.0], [2 / 3.0, 1 / 3.0, 0]])

        for i in range(len(cluster)):
            sumRSS += pow(abs(emd(numpy.array(cluster[i]), numpy.array(centroid),matrix)), 2)

        return sumRSS

    def solve(self, dataPoints, k):
        """Iteratively clusters the dataPoints into the most appropriate cluster
        based on the centroid's distance. Each centroid's position is updated to
        the new mean of the cluster on each iteration. When the RSS doesn't change
        anymore then the best cluster configuration is found.

        Args:
          dataPoints: The set of random data points to be clustered
          k: The number of clusters
        """
        # Create the initial centroids and clusters
        l = len(dataPoints[0])
        centroids = dataPoints[0:k]
        print(centroids)
        clusters = self.configure_clusters(centroids, dataPoints)

        # Loop till algorithm is done
        allRSS = []
        notDone = True
        lastRSS = 0
        while (notDone):
            # Find Residual Sum of Squares of the clusters
            clustersRSS = []
            for i in range(len(clusters)):
                clustersRSS.append(self.get_cluster_RSS(clusters[i], centroids[i]) / len(dataPoints))
            currentRSS = sum(clustersRSS)
            allRSS.append(currentRSS)
            print("RSS", currentRSS)

            # See if the kmean algorithm has converged
            if (currentRSS == lastRSS):
                notDone = False
            else:
                lastRSS = currentRSS

            # Update each of the centroids to the new mean location
            for i in range(len(centroids)):
                centroids[i] = self.new_centroid(clusters[i])

            # Reconfigure the clusters to the new centroids
            clusters = self.configure_clusters(centroids, dataPoints)
        #print(centroids)
        with open("centroids.csv",'w') as file:
            for i in centroids:
                file.write(str(i.tolist()[0])+','+str(i.tolist()[1])+','+str(i.tolist()[2])+'\n')

def main():
    """Generate the random points and starts the kmean clustering algorithm.
    """
    # Generate random points
    dataPoints = []
    with open("data.csv") as file:
        for line in file:
            string_line = line.split(",")
            line_1,line_2,line_3 = float(string_line[0]), float(string_line[1]), float(string_line[2])
            dataPoint = [line_1, line_2, line_3]
            #print(dataPoint)
            dataPoints.append(dataPoint)

    kmean = Clustering()
    kmean.solve(dataPoints, 5)

# If this module is ran as main
if __name__ == '__main__':
    main()
