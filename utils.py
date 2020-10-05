from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from numpy import *
from tqdm import tqdm
from matplotlib.pyplot import subplots

def zscore(x):
    return (x - x.mean())/x.std()

def gen_metrics(dataset, n_clusters):

    random_state = 32313

    results = {
        "silhouette_avg": [],
        "calinski_harabasz": [],
        "davies_bouldin": [],
        "elbow": []
    }

    for clusters in tqdm(n_clusters):
        kmeans = KMeans(n_clusters=clusters)
        cluster_labels = kmeans.fit_predict(dataset)
        
        results["silhouette_avg"].append(
            metrics.silhouette_score(dataset, cluster_labels, metric="euclidean")
        )
        results["calinski_harabasz"].append(
            metrics.calinski_harabasz_score(dataset, cluster_labels)
        )
        results["davies_bouldin"].append(
            metrics.davies_bouldin_score(dataset, cluster_labels)
        )
        results["elbow"].append(
            kmeans.inertia_
        )
    
    return results

def optimal_number_of_clusters(wcss):
    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    
    return distances.index(max(distances)) + 2

def plot_results(data_metrics):

    fig, ((ax0, ax1), (ax2, ax3)) = subplots(2, 2, figsize=(10, 10))
    
    data_metrics.davies_bouldin.plot(ax=ax0, grid=True)
    davies_argmin = data_metrics.davies_bouldin.argmin()+2
    davies_min = data_metrics.davies_bouldin.min()
    ax0.scatter(x=davies_argmin, y=davies_min, s=50, c="red",
               label=f"best: {davies_argmin} ~ {davies_min:.3f}")
    ax0.set_title("davies boudin")
    ax0.legend()
#     annotate(ax0, davies_argmin, davies_min)
    
    
    data_metrics.silhouette_avg.plot(ax=ax1)
    silhouette_argmax = data_metrics.silhouette_avg.argmax()+2
    silhouette_max = data_metrics.silhouette_avg.max()
    ax1.scatter(x=silhouette_argmax, y=silhouette_max, s=50, c="red",
               label=f"best: {silhouette_argmax} ~ {silhouette_max:.3f}")
    ax1.set_title("silhouette avg")
    ax1.legend()
    
#     annotate(ax1, silhouette_argmin, silhouette_min)
    
    data_metrics.calinski_harabasz.plot(ax=ax2)
    calinkski_argmin = data_metrics.calinski_harabasz.argmax()+2
    calinski_min = data_metrics.calinski_harabasz.max()
    ax2.scatter(x=calinkski_argmin, y=calinski_min, s=50, c="red",
               label=f"best: {calinkski_argmin} ~ {calinski_min:.3f}")
                
    ax2.set_title("calinski harabasz")
    ax2.legend()
    
#     annotate(ax1, calinkski_argmin, calinski_min)
    
    
    data_metrics.elbow.plot(ax=ax3)
    elbow_best_x = optimal_number_of_clusters(data_metrics.elbow.to_numpy())
    elbow_best_y = data_metrics.elbow[elbow_best_x]
    ax3.scatter(x=elbow_best_x, y=elbow_best_y, s=50, c="red",
               label=f"best: {elbow_best_x} ~ {elbow_best_y:.3f}")
                
    ax3.set_title("elbow")
    ax3.legend()
    

def plot_views_clusters(dataset, n_clusters, title, ax):

    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(dataset)
    
    pca = PCA(n_components=2)
    trans_data = pca.fit_transform(dataset)
    ax.scatter(x=trans_data[:,0], y=trans_data[:, 1], s=3, c=cluster_labels)
    ax.set_title(title)