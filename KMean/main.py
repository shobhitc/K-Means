from KMeansMain import KMeans

if __name__ == "__main__":
    file_name = "cardaten/car.data"
    attributes = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    target = 'acceptability'

    # initialize a KMeans object with the file, attributes, and target attribute
    #k = 4
    k = input("Enter Number of Clusters: ")
    k = int(k)
    kMeans = KMeans(file_name, attributes, target, k, max_iterations = 20)
    kMeans.execute()



