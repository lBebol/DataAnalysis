import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class HumidityClusterModel:

  def __init__(self, n_clusters=4, random_state=42):

    self.n_clusters = n_clusters
    self.random_state = random_state

    self.features = [
      'PM2.5',
      'O3',
      'NO2',
      'CO',
      'SO2',
      'Temperature_mean',
      'Wind_speed'
    ]

    self.target = 'Humidity'

    self.scaler = StandardScaler()

    self.model = KMeans(
      n_clusters=n_clusters,
      random_state=random_state,
      n_init=10
    )

    self.cluster_humidity = {}
    self.cluster_std = {}

  def fit(self, df):

    X = df[self.features].copy()
    y = df[self.target].copy()

    X_train, _, y_train, _ = train_test_split(
      X,
      y,
      test_size=0.2,
      random_state=self.random_state
    )

    X_scaled = self.scaler.fit_transform(X_train)

    labels = self.model.fit_predict(X_scaled)

    cluster_df = pd.DataFrame({
      'Cluster': labels,
      'Humidity': y_train.values
    })

    self.cluster_humidity = (
      cluster_df.groupby('Cluster')['Humidity']
      .mean()
      .to_dict()
    )

    self.cluster_std = (
      cluster_df.groupby('Cluster')['Humidity']
      .std()
      .to_dict()
    )

    return self

  def predict(self, records):

    if isinstance(records, dict):
      records = [records]

    rows = pd.DataFrame(records)[self.features]

    scaled = self.scaler.transform(rows)

    clusters = self.model.predict(scaled)

    distances = pairwise_distances(
      scaled,
      self.model.cluster_centers_
    )

    predictions = []

    for i, cluster in enumerate(clusters):

      humidity = self.cluster_humidity[cluster]

      std = self.cluster_std.get(cluster, 0)

      confidence = max(
        0,
        100 - (distances[i][cluster] * 12)
      )

      predictions.append({
        'Cluster': int(cluster),
        'Predicted_Humidity': round(humidity, 2),
        'Confidence': round(confidence, 2),
        'Lower_Bound': round(humidity - std, 2),
        'Upper_Bound': round(humidity + std, 2)
      })

    return pd.DataFrame(predictions)

  def save(self, path='humidity_model.pkl'):

    data = {
      'model': self.model,
      'scaler': self.scaler,
      'cluster_humidity': self.cluster_humidity,
      'cluster_std': self.cluster_std,
      'features': self.features
    }

    joblib.dump(data, path)

  @classmethod
  def load(cls, path='humidity_model.pkl'):

    data = joblib.load(path)

    instance = cls()

    instance.model = data['model']
    instance.scaler = data['scaler']
    instance.cluster_humidity = data['cluster_humidity']
    instance.cluster_std = data['cluster_std']
    instance.features = data['features']

    return instance