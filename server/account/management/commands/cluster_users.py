from django.core.management import BaseCommand

import keys
from account.models import User
from polls.models import UserInput

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np


class Command(BaseCommand):
    help = 'Command to cluster users based on their opinions'

    def handle(self, *args, **options):
        if not hasattr(self, 'clusterer'):
            self.clusterer = Clusterer(  # pylint: disable=attribute-defined-outside-init
                n_components=2, n_clusters='auto')

        user_input_json = list()
        user_inputs = UserInput.objects.all()
        for user_input in user_inputs:
            temp_json = {}
            temp_json["question"] = user_input.question_id
            temp_json["user"] = user_input.user_id
            temp_json["statement_shown_to_user"] = user_input.statement_id
            input = 0
            if user_input.input == keys.AGREE:
                input = 1
            if user_input.input == keys.DISAGREE:
                input = -1
            temp_json["input"] = input
            user_input_json.append(temp_json)

        print("user_input_json", user_input_json)
        user_input_json = [
            {
                "question": 1,
                "user": 1,
                "statement_shown_to_user": "some statement shown to the user",
                "input": 1,
                "answer": "users answer that he described in detail",
            },
            {
                "question": 1,
                "user": 2,
                "statement_shown_to_user": "some statement shown to the user",
                "input": 0,
                "answer": "users answer that he described in detail",
            },
            {
                "question": 1,
                "user": 3,
                "statement_shown_to_user": "some statement shown to the user",
                "input": 1,
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 1,
                "statement_shown_to_user": "some statement shown to the user",
                "input": 1,
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 2,
                "statement_shown_to_user": "some statement shown to the user",
                "input": -1,
                "answer": "users answer that he described in detail",
            },
            {
                "question": 2,
                "user": 3,
                "statement_shown_to_user": "some statement shown to the user",
                "input": 0,
                "answer": "users answer that he described in detail",
            },
        ]

        # 1 user, 101 statements, 10 questions.

        # user_input_json = [{'user': 1, 'statement_shown_to_user': 1, 'input': 1},
        #                    {'user': 1, 'statement_shown_to_user': 2, 'input': -1}]

        # Convert json to ndarray
        ndarray = JSONHandler.json_to_ndarray(
            user_input_json, 'user', {'question': 'input'})
        cluster_labels = self.clusterer.fit_predict(ndarray)
        cluster_labels_json = JSONHandler.ndarray_to_json(
            cluster_labels[:, None], 'user', {'cluster': cluster_labels})
        print("cluster_labels_json", cluster_labels_json)
        return


class JSONHandler:
    """Class to convert JSON lists to ndarray and viceversa"""

    @staticmethod
    def json_to_ndarray(json_list, row_name, col_name):
        """Converts a list of dictionaries to a ndarray using row_name and col_names
        Args:
            json_list: list of dictionaries
            row_name: name of the key in the dictionary to be used as row index
            col_names: dictionary of key-value pair to be used as column index and value
        """
        rows = max([json[row_name] for json in json_list]) + 1
        cols = max([json[col] for json in json_list for col in col_name]) + 1
        ndarray = np.zeros((rows, cols), dtype=np.float32)

        for json in json_list:
            for col, val in col_name.items():
                ndarray[json[row_name], json[col]] = json[val]

        return ndarray

    @staticmethod
    def ndarray_to_json(ndarray, row_name, col_names):
        """Converts a ndarray to a list of dictionaries using row_name and col_names"""
        json_list = []

        for i, row in enumerate(ndarray):
            json = {row_name: i}
            for j, col in enumerate(col_names):
                json[col] = row[j]
            json_list.append(json)

        return json_list


class Clusterer:
    """Class to run PCA and KMeans clustering on an ndarray"""

    def __init__(self, n_components=2, n_clusters='auto'):
        self.n_clusters = n_clusters
        self.n_components = n_components
        self.pca = PCA(n_components=self.n_components)

        if n_clusters != 'auto':
            self.kmeans = KMeans(n_clusters=n_clusters)

    def fit(self, ndarray):
        """Fits the PCA and KMeans models to the ndarray."""
        self.pca.fit(ndarray)
        self.pca_ndarray = self.pca.transform(ndarray)  # pylint: disable=attribute-defined-outside-init

        if self.n_clusters == 'auto':
            self.kmeans = self._auto_cluster(self.pca_ndarray)
        else:
            self.kmeans.fit(self.pca_ndarray)

    def predict(self, ndarray):
        """Predicts the cluster labels for the ndarray"""
        pca_ndarray = self.pca.transform(ndarray)
        return self.kmeans.predict(pca_ndarray)

    def fit_predict(self, ndarray):
        """Fits the PCA and KMeans models to the ndarray and returns the cluster labels"""
        self.fit(ndarray)
        return self.predict(ndarray)

    def _auto_cluster(self, ndarray, max_clusters=7):
        """Finds the optimal number of clusters for the ndarray and
        returns a trained KMeans model with that number of clusters"""
        best_silhouette_avg = -2
        best_kmeans = None

        for n_clusters in range(2, min(max_clusters + 1, len(ndarray))):
            print(n_clusters)
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(ndarray)
            cluster_labels = kmeans.predict(ndarray)
            silhouette_avg = silhouette_score(ndarray, cluster_labels)

            if silhouette_avg > best_silhouette_avg:
                best_silhouette_avg = silhouette_avg
                best_kmeans = kmeans

        return best_kmeans
