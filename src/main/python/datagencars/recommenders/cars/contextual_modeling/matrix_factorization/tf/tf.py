import numpy as np
from datagencars.recommenders.cars.contextual_modeling.matrix_factorization.mf import MF


class TF(MF):
    """
    Tensor-based recommender system that models user-item-context interactions.
    Extends the FM class to support tensor-based models.
    
    Original Version: Java (https://github.com/irecsys/CARSKit/)
    """

    def __init__(self, train_matrix, test_matrix, num_factors=10, num_interactions=100, init_learning_rate=0.01, reg=0.02):
        super().__init__(train_matrix, test_matrix, num_factors, num_interactions, init_learning_rate, reg)

        # Extract unique context IDs
        self.num_contexts = train_matrix['context_id'].max()

        # Initialize context-specific latent factors
        self.context_factors = np.random.normal(0, 0.1, (self.num_contexts, num_factors))

    def predict(self, user, item, context=None):
        """
        Predict the rating for a given user, item, and context.
        """
        # Note: En el conjunto de datos de prueba (test_data), hay ítems con índices que no están presentes en 
        # los datos de entrenamiento (train_data). En este caso, el modelo no ha aprendido representaciones para 
        # estos ítems, lo que resulta en el error. De ahí, que si no existen, puedes devolver una predicción 
        # predeterminada (por ejemplo, la media global).
        if user >= len(self.user_bias) or item >= len(self.item_bias):
            # Return global mean if user or item is out of bounds
            return self.global_mean
        
        prediction = (
            self.global_mean +
            self.user_bias[user] +
            self.item_bias[item] +
            np.dot(self.P[user], self.Q[item])
        )
        if context is not None and context - 1 < len(self.context_factors):
            prediction += np.dot(self.P[user], self.context_factors[context - 1])  # Adjusted for 1-based indexing
        return prediction

    def build_model(self):
        """
        Train the tensor recommendation model using gradient descent.
        """
        for iteration in range(self.num_interactions):
            shuffled_data = self.train_df.sample(frac=1).reset_index(drop=True)

            for _, row in shuffled_data.iterrows():
                user, item, context = int(row['user_id']), int(row['item_id']), int(row['context_id'])
                true_rating = row['rating']

                if user >= len(self.user_bias) or item >= len(self.item_bias) or context - 1 >= len(self.context_factors):
                    continue

                # Compute prediction and error
                pred_rating = self.predict(user, item, context)
                error = true_rating - pred_rating

                # Update user, item, and context factors
                self.user_bias[user] += self.learning_rate * (error - self.reg * self.user_bias[user])
                self.item_bias[item] += self.learning_rate * (error - self.reg * self.item_bias[item])
                
                user_factors = self.P[user].copy()
                self.P[user] += self.learning_rate * (error * self.Q[item] - self.reg * user_factors)
                self.Q[item] += self.learning_rate * (error * user_factors - self.reg * self.Q[item])
                self.context_factors[context - 1] += self.learning_rate * (error * user_factors - self.reg * self.context_factors[context - 1])

            # Compute loss and check for convergence
            self.loss = self._compute_loss()
            if self.is_converged():
                print(f"Converged at iteration {iteration}")
                break

    def _compute_loss(self):
        """
        Compute the total loss (MSE + regularization) for the tensor model.
        """
        loss = 0
        for _, row in self.train_df.iterrows():
            user, item, context = int(row['user_id']), int(row['item_id']), int(row['context_id'])
            true_rating = row['rating']

            if user >= len(self.user_bias) or item >= len(self.item_bias) or context - 1 >= len(self.context_factors):
                continue

            pred_rating = self.predict(user, item, context)
            error = true_rating - pred_rating
            loss += error**2

        # Add regularization terms
        loss += self.reg * (
            np.sum(self.P**2) +
            np.sum(self.Q**2) +
            np.sum(self.user_bias**2) +
            np.sum(self.item_bias**2) +
            np.sum(self.context_factors**2)
        )
        return loss


# if __name__ == "__main__":
#     import pandas as pd
#     # Load training and testing data    
#     train_data = pd.read_csv("./resources/sample_data/rating_train_compact.csv")
#     test_data = pd.read_csv("./resources/sample_data/rating_test_compact.csv")
#     context_train = pd.read_csv("./resources/sample_data/context_train_compact.csv")
#     context_test = pd.read_csv("./resources/sample_data/context_test_compact.csv")

#     # Merge context data into rating data
#     train_data = train_data.merge(context_train, on="context_id", how="left")
#     test_data = test_data.merge(context_test, on="context_id", how="left")

#     # Initialize TensorRecommender
#     recommender = TF(train_matrix=train_data, test_matrix=test_data, num_factors=10, num_interactions=50, init_learning_rate=0.01, reg=0.02)

#     # Train the model
#     print("Training the model...")
#     recommender.build_model()

#     # Evaluate the model
#     print("Evaluating the model...")
#     evaluation_metrics = recommender.evaluate()
#     print("Evaluation Metrics:", evaluation_metrics)
