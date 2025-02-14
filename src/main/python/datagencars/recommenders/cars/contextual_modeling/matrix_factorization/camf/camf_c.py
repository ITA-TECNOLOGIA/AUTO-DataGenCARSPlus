from datagencars.recommenders.cars.contextual_modeling.matrix_factorization.camf.camf import CAMF
import numpy as np


class CAMF_C(CAMF):
    """
    Context-aware Matrix Factorization with Condition Deviations (CAMF_C).
    
    The most general one, we assume that each contextual condition has a global influence on the rat-ings independently from the item. 
    For example, when the contextual factor “weather” is “sunny” one can detect that all the places of interest (POIs), independently 
    from the nature of the particular POI, receive a higher rating. Hence, in this model, which is called CAMF-C, we introduce one
    single parameter for each contextual condition (i.e., value of a contextual factor).
    
    Original Version: Java (https://github.com/irecsys/CARSKit/)
        CAMF_C: Baltrunas, Linas, Bernd Ludwig, and Francesco Ricci. "Matrix factorization techniques for context aware recommendation." Proceedings of the fifth ACM conference on Recommender systems. ACM, 2011.    
        Note: in this algorithm, there is a rating deviation for each context condition                
        @author Yong Zheng    
    """

    def __init__(self, train_matrix, test_matrix, context_train, context_test, num_conditions=5, num_factors=10, num_interactions=100, init_learning_rate=0.01, reg=0.02, reg_b=0.1, reg_u=0.1, reg_i=0.1, reg_c=0.1):
        """
        Initialize the CAMF_C model.

        Args:
            train_matrix (pd.DataFrame): Training data with ['row', 'col', 'value', 'context'] columns.
            test_matrix (pd.DataFrame): Test data with ['row', 'col', 'value', 'context'] columns.
            fold (int): Cross-validation fold index.
        """
        super().__init__(train_matrix, test_matrix, context_train, context_test, num_conditions, num_factors, num_interactions, init_learning_rate, reg, reg_b, reg_u, reg_i, reg_c)
        
        # Initialize biases
        self.user_bias = np.random.normal(0, 0.1, self.num_users)
        self.item_bias = np.random.normal(0, 0.1, self.num_items)
        self.condition_bias = np.random.normal(0, 0.1, self.num_conditions)

        # Initialize latent factors
        self.user_factors = np.random.normal(0, 0.1, (self.num_users, self.num_factors))
        self.item_factors = np.random.normal(0, 0.1, (self.num_items, self.num_factors))
        
        self.algo_name = "CAMF_C"       

    def predict(self, user, item, context_list):
        """
        Predict the rating for a given user-item-context tuple.

        Args:
            user (int): User ID.
            item (int): Item ID.
            context_list (list): Context list.

        Returns:
            float: Predicted rating.
        """
        prediction = (
            self.global_mean +
            self.user_bias[user] +
            self.item_bias[item] +
            np.dot(self.user_factors[user], self.item_factors[item])
        )

        # Add context condition biases        
        for idx, cond in enumerate(context_list):
            prediction += self.condition_bias[idx]
        return prediction

    def build_model(self):
        """
        Train the CAMF_C model using Stochastic Gradient Descent (SGD).
        """
        for iteration in range(1, self.num_interactions + 1):
            self.loss = 0

            # Iterate over training data
            for idx, row in self.train_df.iterrows():
                user = int(row['user_id'])
                item = int(row['item_id'])
                rating = row['rating']                
                
                context_list = self.get_conditions(context=self.context_train, context_id=row['context_id'])
                
                # Compute prediction and error
                prediction = self.predict(user, item, context_list)
                error = rating - prediction

                self.loss += error ** 2

                # Update user and item biases
                self.user_bias[user] += self.learning_rate * (error - self.reg_b * self.user_bias[user])
                self.item_bias[item] += self.learning_rate * (error - self.reg_b * self.item_bias[item])

                # Update context condition biases
                for idx, cond in enumerate(context_list):
                    self.condition_bias[idx] += self.learning_rate * (error - self.reg_c * self.condition_bias[idx])

                # Update latent factors
                for f in range(self.num_factors):
                    user_factor = self.user_factors[user, f]
                    item_factor = self.item_factors[item, f]

                    self.user_factors[user, f] += self.learning_rate * (
                        error * item_factor - self.reg_u * user_factor
                    )
                    self.item_factors[item, f] += self.learning_rate * (
                        error * user_factor - self.reg_i * item_factor
                    )

                    # Add regularization to the loss
                    self.loss += self.reg_u * user_factor ** 2 + self.reg_i * item_factor ** 2

            self.loss *= 0.5

            # Check for convergence
            if self.is_converged():
                print(f"Converged at iteration {iteration}")
                break

    def __str__(self):
        """
        Provide a string representation of the model's parameters.

        Returns:
            str: Description of the model configuration.
        """
        return f"{super().__str__()}, CAMF_C with condition-based deviations"


# # Example usage
# if __name__ == "__main__":
#     import pandas as pd

#     # Load training and testing data
#     train_data = pd.read_csv("./resources/sample_data/rating_train_compact.csv")
#     test_data = pd.read_csv("./resources/sample_data/rating_test_compact.csv")
#     context_train = pd.read_csv("./resources/sample_data/context_train_compact.csv")
#     context_test = pd.read_csv("./resources/sample_data/context_test_compact.csv")
   
#     # Initialize and process data
#     model = CAMF_C(train_data, test_data, context_train, context_test, num_conditions=5, num_factors=10, num_interactions=100, init_learning_rate=0.01, reg=0.02, reg_b=0.1, reg_u=0.1, reg_i=0.1, reg_c=0.1)
#     # Train and evaluate the model
#     print("Training the model...")
#     model.build_model()
#     print("Evaluating the model...")
#     metrics = model.evaluate()
#     print("Evaluation Metrics:", metrics)
