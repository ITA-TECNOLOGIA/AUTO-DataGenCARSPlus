import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


class MF:
    """
    Iterative Recommender system using Matrix Factorization with Stochastic Gradient Descent.

    Original Version: Java (https://github.com/irecsys/CARSKit/)
    """

    def __init__(self, train_df, test_df, num_factors=10, num_interactions=100, init_learning_rate=0.01, max_learning_rate=None, reg=0.02, bold_driver=False, decay=0.95):
        """
        Initialize the iterative recommender system.

        :param train_matrix: Training data as a pandas DataFrame with ['row', 'col', 'value'].
        :param test_matrix: Test data as a pandas DataFrame with ['row', 'col', 'value'].
        :param num_factors: Number of latent factors for users and items.
        :param num_iteractions: Maximum number of iterations.
        :param init_learning_rate: Initial learning rate for gradient descent.
        :param max_learning_rate: Maximum learning rate for bold driver.
        :param reg: Regularization parameter.
        :param bold_driver: Whether to use bold driver for adaptive learning rate.
        :param decay: Decay factor for learning rate.
        """
        # Dataframes (U,I,R): 
        self.train_df = train_df
        self.test_df = test_df

        # Settings:
        self.num_factors = num_factors
        self.num_interactions = num_interactions
        self.learning_rate = init_learning_rate
        self.max_learning_rate = max_learning_rate
        self.reg = reg
        self.bold_driver = bold_driver
        self.decay = decay

        # Satatistics:
        self.num_users = self.train_df['user_id'].max() + 1
        self.num_items = self.train_df['item_id'].max() + 1
        self.global_mean = self.train_df['rating'].mean()

        # Initialize model parameters
        self.P = np.random.normal(0, 0.1, (self.num_users, self.num_factors))
        self.Q = np.random.normal(0, 0.1, (self.num_items, self.num_factors))
        self.user_bias = np.zeros(self.num_users)
        self.item_bias = np.zeros(self.num_items)

        # Convergence variables
        self.loss = 0
        self.last_loss = None
    
    def predict(self, user, item):
        """
        Predict the rating for a given user and item.
        """        
        # print("global_mean: ", self.global_mean)
        # print("user_bias: ", self.user_bias[user])
        # print("item_bias: ", self.item_bias[item])
        # print("PxQ: ", np.dot(self.P[user], self.Q[item]))
        return (self.global_mean + self.user_bias[user] + self.item_bias[item] + np.dot(self.P[user], self.Q[item]))

    def build_model(self):
        """
        Train the recommendation model using Stochastic Gradient Descent.
        """
        for iteration in range(self.num_interactions):
            shuffled_data = self.train_df.sample(frac=1).reset_index(drop=True)

            for _, row in shuffled_data.iterrows():
                user, item, true_rating = int(row['user_id']), int(row['item_id']), row['rating']
                pred_rating = self.predict(user, item)
                error = true_rating - pred_rating

                # Update biases
                self.user_bias[user] += self.learning_rate * (error - self.reg * self.user_bias[user])
                self.item_bias[item] += self.learning_rate * (error - self.reg * self.item_bias[item])

                # Update latent factors
                user_factors = self.P[user].copy()
                self.P[user] += self.learning_rate * (error * self.Q[item] - self.reg * user_factors)
                self.Q[item] += self.learning_rate * (error * user_factors - self.reg * self.Q[item])

            self.loss = self._compute_loss()
            if self.is_converged():
                print(f"Converged at iteration {iteration}")
                break

    def _compute_loss(self):
        """
        Compute the total loss (MSE + regularization).
        """
        loss = 0
        for _, row in self.train_df.iterrows():
            user, item, true_rating = int(row['user_id']), int(row['item_id']), row['rating']
            pred_rating = self.predict(user, item)
            error = true_rating - pred_rating
            loss += error**2

        loss += self.reg * (
            np.sum(self.P**2) + np.sum(self.Q**2) + np.sum(self.user_bias**2) + np.sum(self.item_bias**2)
        )
        return loss

    def is_converged(self):
        """
        Check for convergence based on loss and adjust learning rate if needed.
        """
        if self.last_loss is not None:
            delta_loss = abs(self.last_loss - self.loss)
            if delta_loss < 1e-5:
                return True

            if self.bold_driver:
                if self.loss < self.last_loss:
                    self.learning_rate = min(self.learning_rate * 1.05, self.max_learning_rate or self.learning_rate * 1.05)
                else:
                    self.learning_rate *= 0.5
            else:
                self.learning_rate *= self.decay

        self.last_loss = self.loss
        return False

    def evaluate(self):
        """
        Evaluate the model on the test set using RMSE.
        """
        predictions = []
        ground_truth = []

        for _, row in self.test_df.iterrows():
            user, item, true_rating = int(row['user_id']), int(row['item_id']), row['rating']
            pred_rating = self.predict(user, item)
            predictions.append(pred_rating)
            ground_truth.append(true_rating)
            
        mae = mean_absolute_error(ground_truth, predictions)
        rmse = np.sqrt(mean_squared_error(ground_truth, predictions))        
        return {"MAE": mae, 
                "RMSE": rmse}

    def ranking_metrics(self, ranked_list, ground_truth, n=10):
        """
        Compute ranking-based metrics.

        :param ranked_list: List of ranked item IDs.
        :param ground_truth: List of true item IDs.
        :param n: Cutoff for metrics (e.g., top-N).
        :return: Dictionary with metrics (Precision@N, Recall@N, NDCG@N, MAP@N).
        """
        top_n = ranked_list[:n]
        hits = len(set(top_n) & set(ground_truth))

        precision = hits / len(top_n) if top_n else 0
        recall = hits / len(ground_truth) if ground_truth else 0

        dcg = sum([1 / np.log2(idx + 2) for idx, item in enumerate(top_n) if item in ground_truth])
        idcg = sum([1 / np.log2(idx + 2) for idx in range(min(len(ground_truth), n))])
        ndcg = dcg / idcg if idcg > 0 else 0

        ap = 0
        hit_count = 0
        for idx, item in enumerate(top_n):
            if item in ground_truth:
                hit_count += 1
                ap += hit_count / (idx + 1)
        map_n = ap / len(ground_truth) if ground_truth else 0

        return {
            f"Precision@{n}": precision,
            f"Recall@{n}": recall,
            f"NDCG@{n}": ndcg,
            f"MAP@{n}": map_n
        }


# if __name__ == "__main__":
#     import pandas as pd
    
#     # Load training and testing data from CSV files
#     train_data = pd.read_csv("./resources/sample_data/rating_train_compact.csv")
#     test_data = pd.read_csv("./resources/sample_data/rating_test_compact.csv")

#     # Initialize the Iterative Recommender
#     recommender = MF(train_df=train_data, test_df=test_data, num_factors=10, num_interactions=50, init_learning_rate=0.01, reg=0.02, bold_driver=True, decay=0.95)

#     # Train the model
#     print("Training the model...")
#     recommender.build_model()

#     # Evaluate the model on the test set
#     print("Evaluating the model...")
#     evaluation_metrics = recommender.evaluate()
#     print("Evaluation Metrics:", evaluation_metrics)

#     # Example of ranking metrics for a specific user
#     user_id = 1032  # Replace with an actual user ID from your test data
#     user_test_data = test_data[test_data['user_id'] == user_id]
#     ground_truth = user_test_data['item_id'].tolist()  # List of actual items rated by the user

#     # Predict rankings for all items for the user
#     all_items = train_data['item_id'].unique()  # List of all items in the training data
#     predictions = [(item, recommender.predict(user_id, item)) for item in all_items]
#     ranked_list = [item for item, _ in sorted(predictions, key=lambda x: x[1], reverse=True)]

#     # Compute ranking metrics
#     ranking_metrics = recommender.ranking_metrics(ranked_list, ground_truth, n=5)
#     print(f"Ranking Metrics for user {user_id}:", ranking_metrics)