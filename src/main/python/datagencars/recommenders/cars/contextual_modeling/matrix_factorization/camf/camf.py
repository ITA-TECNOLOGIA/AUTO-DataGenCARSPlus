import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datagencars.recommenders.cars.contextual_modeling.matrix_factorization.mf import MF


class CAMF(MF):
    """
    CAMF: Context-Aware Matrix Factorization (CAMF).

    Extends the MF class to include context-aware modeling capabilities with deviation-based models.

    Original Version: Java (https://github.com/irecsys/CARSKit/)
    """

    def __init__(self, train_matrix, test_matrix, context_train, context_test, num_conditions=5, num_factors=10, num_interactions=100, init_learning_rate=0.01, reg=0.02, reg_b=0.1, reg_u=0.1, reg_i=0.1, reg_c=0.1):
        """
        Initialize the CAMF model.

        :param train_matrix: Training data as a pandas DataFrame with ['row', 'col', 'value', 'context'] columns.
        :param test_matrix: Test data as a pandas DataFrame with ['row', 'col', 'value', 'context'] columns.        
        :param num_conditions: Number of possible context conditions (default: 5).
        :param num_factors: Number of latent factors for users and items.
        :param num_iters: Maximum number of iterations.
        :param init_learning_rate: Initial learning rate.
        :param reg: Regularization parameter.
        """
        super().__init__(train_matrix, test_matrix, num_factors, num_interactions, init_learning_rate, reg)

        self.num_conditions = num_conditions
        self.context_train = context_train
        self.context_test = context_test
        
        # Initialize regularization parameters
        self.reg_b = reg_b  # Regularization for biases
        self.reg_u = reg_u  # Regularization for user factors
        self.reg_i = reg_i  # Regularization for item factors
        self.reg_c = reg_c  # Regularization for context factors

        # Initialize context-specific biases and interaction matrices
        self.cond_bias = np.zeros(self.num_conditions)
        self.uc_bias = np.random.normal(0, 0.1, (self.num_users, self.num_conditions))
        self.ic_bias = np.random.normal(0, 0.1, (self.num_items, self.num_conditions))

    def get_conditions(self, context, context_id):
        """
        Retrieve the conditions associated with a given context.

        :param context: Context information as a string (e.g., "1,2,3"), a list of integers, or None.
        :return: List of integers representing the conditions.
        """        
        context_list = context.loc[context['context_id'] == context_id].drop('context_id', axis=1).values.flatten().tolist()           
        return context_list
    
    def evaluate(self):
        """
        Evaluate the CAMF model using RMSE on the test set.
        """
        predictions = []
        ground_truth = []

        for _, row in self.test_df.iterrows():
            user, item = int(row['user_id']), int(row['item_id'])
            true_rating = row['rating']
            context_list = self.get_conditions(context=self.context_test, context_id=row['context_id'])

            pred_rating = self.predict(user, item, context_list)
            predictions.append(pred_rating)
            ground_truth.append(true_rating)

        rmse = np.sqrt(mean_squared_error(ground_truth, predictions))
        mae = mean_absolute_error(ground_truth, predictions)
        return {"RMSE": rmse, "MAE": mae}
    
    def __str__(self):
        """
        Return a string representation of the CAMF model.
        """
        return (
            f"CAMF Model: numFactors={self.num_factors}, "
            f"numInteractions={self.num_interactions}, learningRate={self.learning_rate}, reg={self.reg}, "
            f"numConditions={self.num_conditions}"
        )
