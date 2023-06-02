import logging
import warnings
import json
from collections import defaultdict
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from surprise import NormalPredictor, KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
import datagencars.evaluation.rs_surprise.surprise_helpers as surprise_helpers
warnings.filterwarnings('ignore')


class RecommenderSIDELARS:
    """
    Class for the Side-LARS (SocIal-Distance prEserving Location-Aware Recommender System). This class handles the creation, 
    management, and updating of recommendations for a user in a virtual world context. The recommendations are trajectory-based, 
    taking into account the user's location, preferences, and contextual variables.
    """

    def __init__(self, df_item, df_context, df_rating, df_behavior):
        """
        :param df_item: Dataframe containing item information.
        :param df_context: Dataframe containing context information.
        :param df_rating: Dataframe containing user rating information.
        :param df_behavior: Dataframe containing user behavior information.
        """
        try:
            self.df_item = df_item
            self.df_context = df_context
            self.df_rating = df_rating
            self.df_behavior = df_behavior

            logging.info('Creating auxiliary data structures...')
            user_counts = self.df_rating['user_id'].value_counts()
            users_with_ratings = user_counts[user_counts > 0].index
            self.df_rating = self.df_rating[self.df_rating['user_id'].isin(users_with_ratings)] # Remove users with no ratings
            self.target_user_list = self.df_rating['user_id'].tolist()
            self.item_list = self.df_item['item_id'].tolist()

        except Exception as e:
            logging.error(e)

    def get_last_position_for_user(self, user_id):
        """
        Retrieves the latest position of the user based on behavior data.
        :param user_id: The ID of the user.
        :return: A list representing the last position of the user or None if no data is available.
        """
        user_data = self.df_behavior[self.df_behavior["user_id"] == user_id]
        user_data = user_data[user_data["object_action"] == "Update"]
        user_data = user_data.sort_values(by="timestamp", ascending=False)
        
        if not user_data.empty:
            last_position = user_data.iloc[0]["user_position"]
            last_position = [float(x) for x in last_position[1:-1].split(',')] # Converting last_position string to a list of float values
            return last_position
        else:
            return None

    def get_top_n(self, predictions, n=10):
        """
        Returns the top-N recommendation for each user from a set of predictions.
        :param predictions: The list of predictions, as returned by the test method of an algorithm.
        :param n: The number of recommendations to output for each user. Default is 10.
        :return: A dict where keys are user (raw) ids and values are lists of tuples [(raw item id, rating estimation), ...] of size n.
        """
        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))
        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
        return top_n

    def get_user_based_recommendation(self, algorithm, trainset, testset, k_recommendations):
        """
        Applies KNN algorithms for user-based collaborative filtering.
        :param algorithm: The KNN algorithm to be used for recommendation.
        :param trainset: The training set.
        :param testset: The test set.
        :param k_recommendations: The number of items to recommend to the user.
        :return: Top k candidate items to be recommended to users.
        """

        # Fitting the algorithm.
        algorithm.fit(trainset)

        # Predicting ratings for all pairs (u,i) that are NOT in the training set.
        predictions = algorithm.test(testset)

        return self.get_top_n(predictions, n=k_recommendations)

    def get_random_recommendation(self, k_recommendations, cold_start_user_list, trainset):
        """
        Provides recommendations using a random prediction algorithm.
        :param k_recommendations: The number of items to recommend to the user.
        :param cold_start_user_list: A list of users with a cold start.
        :param trainset: The training set.
        :return: Top k candidate items to be recommended to cold start users.
        """
        # Building the Random algorithm.
        recommender = NormalPredictor()
        recommender.fit(trainset)
        # Getting all pairs (u,i) that are NOT in the training set.
        fill = trainset.global_mean
        testset = []
        for user in cold_start_user_list:
            for item in self.item_list:
                testset.append((user, item, fill))
        # Predicting ratings for all pairs (u,i) that are NOT in the training set.
        predictions = recommender.test(testset)
        return self.get_top_n(predictions, n=k_recommendations)

    def get_npoi_recommendation(self, k_recommendations, cold_start_user_list):
        """
        Nearest Point of Interest (NPOI) algorithm for cold start users.
        :param k_recommendations: The number of items to recommend to the user.
        :param cold_start_user_list: A list of users with a cold start.
        :return: Top k candidate items to be recommended to cold start users.
        """
        recommendations = defaultdict(list)

        for user in cold_start_user_list:
            user_location = self.get_last_position_for_user(user)

            if user_location is None or len(user_location) != 3:
                continue

            distances = []

            for item in self.item_list:
                df_item_current = self.df_item.loc[self.df_item['item_id'] == item]
                if not df_item_current.empty:
                    item_location = df_item_current['object_position'].iloc[0]
                    item_location = [float(x) for x in item_location[1:-1].split(',')]
                    if len(item_location) == 3:
                        distance = euclidean(user_location, item_location)
                        distances.append((item, distance))

            distances.sort(key=lambda x: x[1])
            recommendations[user] = [(item, None) for item, _ in distances[:k_recommendations]]
        return recommendations

    def apply_social_distance(self, candidate_recommendation_list, min_social_distance):
        """
        Filters recommendation candidates based on a minimum social distance criteria.
        :param candidate_recommendation_list: The candidate list of recommendations.
        :param min_social_distance: The minimum social distance to be maintained.
        :return: A filtered list of recommendations.
        """
        filtered_candidates = {}

        for uid, user_ratings in candidate_recommendation_list.items():
            current_user_location = self.get_last_position_for_user(uid)

            # If there is no location information, add the user to the list
            if current_user_location is None:
                filtered_candidates[uid] = user_ratings
                continue

            too_close = False
            for other_uid, other_user_ratings in filtered_candidates.items():
                other_user_location = self.get_last_position_for_user(other_uid)

                if other_user_location is not None:
                    distance = euclidean(current_user_location, other_user_location)
                    if distance < min_social_distance:
                        too_close = True
                        break

            if not too_close:
                filtered_candidates[uid] = user_ratings

        return filtered_candidates

    def get_trajectory(self, candidate_recommendation_list, apply_social_distancing=False, min_social_distance=2.0):
        """
        Sorts the recommendation list by trajectory, considering the distance between target user and recommended items.
        :param candidate_recommendation_list: The candidate list of recommendations.
        :param apply_social_distancing: Whether to apply social distancing in recommendations. Default is False.
        :param min_social_distance: The minimum social distance to be maintained. Default is 2.0.
        :return: A dictionary with items to recommend per user (sorted by trajectory and social distancing applied).
        """
        recommendation_dict = {}
        # Print the recommended items for each user
        for uid, user_ratings in candidate_recommendation_list.items():
            current_user_location = self.get_last_position_for_user(uid)
            if current_user_location is None:
                continue  # skip this user if their location is not available
            recommended_item_list = []
            explanation_items = []
            for item, rating in user_ratings:
                # Item location:
                df_item_current = self.df_item.loc[self.df_item['item_id'] == item]
                if not df_item_current.empty:
                    item_location = df_item_current['object_position'].iloc[0]
                    item_location = [float(x) for x in item_location[1:-1].split(',')] # Converting item_location string to a list of float values
                    object_type = df_item_current['object_type'].iloc[0]
                    room_id = df_item_current['room_id'].iloc[0]
                    distance = euclidean([current_user_location[0], current_user_location[2]], [item_location[0], item_location[2]])
                    # Adding in dictionary:
                    recommended_item_dict = {}
                    recommended_item_dict['object_id'] = item
                    recommended_item_dict['object_position'] = item_location
                    recommended_item_dict['object_type'] = object_type
                    recommended_item_dict['distance'] = distance
                    recommended_item_dict['room_id'] = room_id
                    recommended_item_list.append(recommended_item_dict)
                    explanation_items.append(f"{object_type} {item} en la habitación {room_id}")
            sorted_recommended_item_list = sorted(recommended_item_list, key=lambda x: x['distance'])
            explanation = "You might be interested in visiting:\n"
            explanation += "\n".join([f"{idx + 1}. {item}" for idx, item in enumerate(explanation_items)])
            explanation += "because many users similar to you have visited it.\n."
            recommendation_dict[uid] = {"recommendations": sorted_recommended_item_list, "explanation": explanation}
        if apply_social_distancing:
            recommendation_dict = self.apply_social_distance(recommendation_dict, min_social_distance)
        return recommendation_dict

    def dynamic_recommendation_pipeline(self, dataset, algorithm, k_recommendations, side_lars, min_social_distance):
        """
        The main pipeline function for dynamic recommendation.
        :param dataset: The dataset to be used for recommendation.
        :param algorithm: The algorithm to be used for recommendation.
        :param k_recommendations: The number of items to recommend to the user.
        :param apply_social_distancing: Whether to apply social distancing in recommendations. Default is False.
        :param min_social_distance: The minimum social distance to be maintained. Default is 2.0.
        :return: A dictionary with items to recommend per user.
        """
        # Generating trainset and testset with the whole dataset:
        logging.info('Generating trainset with the whole dataset...')
        trainset = dataset.build_full_trainset()
        # Getting all pairs (u,i) that are NOT in the training set.
        testset = trainset.build_anti_testset()

        # Getting candidate user-based recommendation list:
        candidate_ub_recommendation_list = self.get_user_based_recommendation(algorithm, trainset, testset, k_recommendations)
        # Sorting recommended items by distance between current user location and recommended item locations:
        ub_recommendation_json = self.get_trajectory(candidate_ub_recommendation_list, side_lars, min_social_distance)
        
        # Filtering recommendation dictionary for target users:
        target_user_cold_start_list = []
        filtered_ub_recommendation_json = {}
        for target_user in self.target_user_list:
            if target_user in ub_recommendation_json:
                filtered_ub_recommendation_json[target_user] = ub_recommendation_json[target_user]
            else:
                target_user_cold_start_list.append(target_user)

        # candidate_random_recommendation_list = self.get_random_recommendation(k_recommendations, target_user_cold_start_list)
        candidate_random_recommendation_list = self.get_npoi_recommendation(k_recommendations, target_user_cold_start_list)
        # Sorting recommended items by distance between current user location and recommended item locations:
        random_recommendation_json = self.get_trajectory(candidate_random_recommendation_list, side_lars, min_social_distance)
        
        return filtered_ub_recommendation_json, random_recommendation_json
    
def default(o):
    if isinstance(o, np.int64): return int(o)  
    return o.__dict__

def main():
    df_item = pd.read_csv(r'resources\dataset_imascono\item.csv')
    df_context = pd.read_csv(r'resources\dataset_imascono\context.csv')
    df_rating = pd.read_csv(r'resources\dataset_imascono\rating.csv')
    df_behavior = pd.read_csv(r'resources\dataset_imascono\behavior.csv')
    dataset = surprise_helpers.convert_to_surprise_dataset(df_rating)
    
    recommender = RecommenderSIDELARS(df_item, df_context, df_rating, df_behavior)

    # Parameter settings of the KNN algorithms.
    k_max_neighbours = 40 # K maximum number of neighbours.
    k_min_neighbours = 1 # K minimum number of neighbours.
    sim_options = {'user_based': True}  # Compute similarities between users
    algorithms = [
        KNNBasic(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options),
        # KNNWithMeans(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options),
        # KNNWithZScore(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options),
        # KNNBaseline(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options)
    ]

    for algorithm in algorithms:
        filtered_ub_recommendation_json, random_recommendation_json = recommender.dynamic_recommendation_pipeline(dataset, algorithm, k_recommendations=3, 
                                                                                                                  side_lars=True, min_social_distance=2.0)
        # print("User-based recommendation json:", filtered_ub_recommendation_json)
        # print("Random recommendation json:", random_recommendation_json)
        
        # Save the JSON data to a file
        with open('filtered_ub_recommendation.json', 'w') as f:
            json.dump(filtered_ub_recommendation_json, f, default=default)

        with open('random_recommendation.json', 'w') as f:
            json.dump(random_recommendation_json, f, default=default)

if __name__ == '__main__':
    main()
