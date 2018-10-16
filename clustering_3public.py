""" Script that drives the cluster algorithm for 2 hands and 3 public

"""
import numpy
#matplotlib.use('GTKAgg') # For linux gtk
import EMD_org
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
        #matrix = numpy.array([[0,1/3.0,2/3.0],[1/3.0,0,1/3.0],[2/3.0,1/3.0,0]])
        matrix = [[0]*10]*10
        for i in range(10):
            for j in range(10):
                matrix[i][j] = 1/10*abs(i-j)
        matrix = numpy.array(matrix)

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
            #print(i)
            cluster = []
            clusters.append(cluster)

        # For all the dataPoints, place them in initial clusters
        #print(len(dataPoints))
        for i in range(len(dataPoints)):
            idealCluster = self.points_best_cluster(centroids, dataPoints[i])
            clusters[idealCluster].append(dataPoints[i])
        #NOTE:it is dangerous
        max = 0
        max_index = 0
        blank = []
        for i in range(len(clusters)):
            if len(clusters[i]) > max:
                max = len(clusters[i])
                max_index = i
            if len(clusters[i]) == 0:
                blank.append(i)
        print(blank)
        for i in range(len(blank)):
            for _ in range(3):
                clusters[blank[i]].append(clusters[max_index].pop())

        return clusters

    def get_cluster_RSS(self, cluster, centroid):
        """Calculates the cluster's Residual Sum of Squares (RSS)

        Args:
          cluster: The list of data points of one cluster
          centroid: The centroid point of the corresponding cluster
        """
        sumRSS = 0
        #matrix = numpy.array([[0, 1 / 3.0, 2 / 3.0], [1 / 3.0, 0, 1 / 3.0], [2 / 3.0, 1 / 3.0, 0]])
        matrix = [[0] * 10] * 10
        for i in range(10):
            for j in range(10):
                matrix[i][j] = 1 / 10 * abs(i - j)
        matrix = numpy.array(matrix)
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
        centroids = dataPoints[100:k+100]
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
        #(centroids)
        with open("centroids_3.csv",'w') as file:
            for i in centroids:
                file.write(str(i.tolist()[0])+','+str(i.tolist()[1])+','+str(i.tolist()[2])+','+str(i.tolist()[3])+','+str(i.tolist()[4])+','+ str(i.tolist()[5])+','+str(i.tolist()[6])+','+str(i.tolist()[7])+','+str(i.tolist()[8])+','+str(i.tolist()[9])+'\n')


  def main():
      """Generate the random points and starts the kmean clustering algorithm.
      """
      # Generate random points
      dataPoints = []
      with open("data_3.csv") as file:
          for line in file:
              string_line = line.strip().split(",")[:10]
              #print(type(string_line))
              dataPoint = list(map(float, string_line))
              dataPoints.append(dataPoint)
      print(len(dataPoints))
      kmean = Clustering()
      kmean.solve(dataPoints, 20)

# If this module is ran as main
if __name__ == '__main__':
  main()
