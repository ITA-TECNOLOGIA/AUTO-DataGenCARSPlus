import logging
import warnings
from collections import defaultdict
import pandas as pd
from scipy.spatial.distance import euclidean
from surprise import Dataset, Reader, NormalPredictor, KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
from surprise.model_selection import train_test_split
warnings.filterwarnings('ignore')


class Recommender:

    def __init__(self):
        try:
            # Generating recommendation dataset from virtual_space='Spaceship':
            logging.info('Generating recommendation dataset from virtual_space=Spaceship.')
            # USER: df_user
            self.df_user = pd.read_csv(r'resources\data_schema_imascono\user.csv')
            # ITEM: df_item
            self.df_item = pd.read_csv(r'resources\data_schema_imascono\item.csv')
            # CONTEXT: df_context
            self.df_context = pd.read_csv(r'resources\data_schema_imascono\context.csv')
            # RATING: df_rating
            self.df_rating = pd.read_csv(r'resources\data_schema_imascono\rating.csv')
            # BEHAVIOR: df_behavior
            self.df_behavior = pd.read_csv(r'resources\data_schema_imascono\behavior.csv')

            # Remove users with no ratings
            user_counts = self.df_rating['user_id'].value_counts()
            users_with_ratings = user_counts[user_counts > 0].index
            self.df_rating = self.df_rating[self.df_rating['user_id'].isin(users_with_ratings)]

            # Loading dataset from a df of ratings:
            logging.info('Reading df_rating.')
            if "timestamp" in self.df_rating.columns:
                self.df_rating = self.df_rating.drop("timestamp", axis=1)
            if "context_id" in self.df_rating.columns:
                self.df_rating = self.df_rating.drop("context_id", axis=1)
            reader = Reader(rating_scale=(self.df_rating["rating"].min(), self.df_rating["rating"].max())) #line_format='user item rating', sep=',',
            dataset = Dataset.load_from_df(self.df_rating, reader=reader)

            # Generating trainset with the whole dataset:
            logging.info('Generating trainset and item list.')
            self.trainset = dataset.build_full_trainset()
            self.item_list = self.df_item['item_id'].tolist()

            self.target_user_list = self.df_rating['user_id'].tolist()

        except Exception as e:
            logging.error(e)

    #TODO: Poner esta funcion fuera de la clase de Recommender
    def get_last_position_for_user(self, user_id):
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
        Get the top-N recommendation for each user from a set of predictions.
        :param predictions(list of Prediction objects): The list of predictions, as returned by the test method of an algorithm.
        :param n(int): The number of recommendation to output for each user. Default is 10.
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

    def get_user_based_recommendation(self, k_recommendations, k_max_neighbours, k_min_neighbours):
        """
        KNN algorithms for user-based collaborative filtering.
        :param k_recommendations: K items to recommend to the user.
        :param k_max_neighbours: K maximum number of neighbours.
        :param k_min_neighbours: K minimum number of neighbours.
        :return: K candidate items to be recommended to users.
        """
        # Parameter settings of the KNN algorithms.
        sim_options = {'user_based': True}  # compute similarities between users
        algorithms = [
            KNNBasic(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options, verbose=False),
            KNNWithMeans(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options, verbose=False),
            KNNWithZScore(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options, verbose=False),
            KNNBaseline(k=k_max_neighbours, min_k=k_min_neighbours, sim_options=sim_options, verbose=False)
        ]

        all_predictions = []

        for algorithm in algorithms:
            # Building the algorithm.
            algorithm.fit(self.trainset)

            # Getting all pairs (u,i) that are NOT in the training set.
            testset = self.trainset.build_anti_testset()
            # Predicting ratings for all pairs (u,i) that are NOT in the training set.
            predictions = algorithm.test(testset)


        return self.get_top_n(all_predictions, n=k_recommendations)

    #TODO: esto no es NPOI, esto es aleatorio. Implementar NPOI de verdad.
    def get_random_recommendation(self, k_recommendations, cold_start_user_list):
        '''
        NormalPredictor: it is an algorithm predicts a random rating based on the distribution
        of the training set, which is assumed to be normal. This is one of the most basic
        algorithms that do not do much work.
        :param k_recommendations: K items to recommend to the user.
        :param cold_start_user_list: A list of users with a cold start.
        :return: K candidate items to be recommended to cold start users.
        '''
        # Building the Random algorithm.
        recommender = NormalPredictor()
        recommender.fit(self.trainset)
        # Getting all pairs (u,i) that are NOT in the training set.
        fill = self.trainset.global_mean
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
        :param k_recommendations: K items to recommend to the user.
        :param cold_start_user_list: A list of users with a cold start.
        :return: K candidate items to be recommended to cold start users.
        """
        recommendations = defaultdict(list)

        for user in cold_start_user_list:
            user_location = self.get_last_position_for_user(user)

            if user_location is None:
                continue

            distances = []

            for item in self.item_list:
                df_item_current = self.df_item.loc[self.df_item['item_id'] == item]
                if not df_item_current.empty:
                    item_location = df_item_current['object_position'].iloc[0]
                    item_location = [float(x) for x in item_location[1:-1].split(',')]
                    distance = euclidean(user_location, item_location)
                    distances.append((item, distance))

            distances.sort(key=lambda x: x[1])
            recommendations[user] = [(item, None) for item, _ in distances[:k_recommendations]]

        return recommendations

    def get_trajectory(self, candidate_recommendation_list):
        """
        Sorting the recommendation list by trajectory, by considering the distance between target user and recommended items.
        :param candidate_recommendation_list: Candidate recommendation list.
        :return: A dictionary with items to recommend per user (sorted by trajectory).
        """
        recommendation_dict = {}
        # Print the recommended items for each user
        for uid, user_ratings in candidate_recommendation_list.items():
            current_user_location = self.get_last_position_for_user(uid)
            if current_user_location is None:
                continue  # skip this user if their location is not available
            recommended_item_list = []
            for item, rating in user_ratings:
                # Item location:
                # df_room_current = self.df_room.loc[self.df_room['item_id'] == item]
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
            sorted_recommended_item_list = sorted(recommended_item_list, key=lambda x: x['distance'])
            recommendation_dict[str(uid)] = sorted_recommended_item_list
        return recommendation_dict
        
    def apply_social_distance(self, candidate_recommendation_list, min_social_distance):
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

    def dynamic_recommendation_pipeline(self, k_recommendations, k_max_neighbours, k_min_neighbours, apply_social_distancing, min_social_distance):
        '''
        Dynamic recommendation pipeline.
        :param k_recommendations: K items to recommend to the user.
        :param k_max_neighbours: K maximum number of neighbours.
        :param k_min_neighbours: K minimum number of neighbours.
        :return: Dictionaries resulting from user-based and random recommendations.
        '''
        # Getting candidate user-based recommendation list:
        candidate_ub_recommendation_list = self.get_user_based_recommendation(k_recommendations, k_max_neighbours, k_min_neighbours)
        # Sorting recommended items by distance between current user location and recommended item locations:
        ub_recommendation_json = self.get_trajectory(candidate_ub_recommendation_list)
        if apply_social_distancing:
            candidate_ub_recommendation_list = self.apply_social_distance(candidate_ub_recommendation_list, min_social_distance)
            candidate_random_recommendation_list = self.apply_social_distance(candidate_random_recommendation_list, min_social_distance)
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
        random_recommendation_json = self.get_trajectory(candidate_random_recommendation_list)
        if apply_social_distancing:
            candidate_ub_recommendation_list = self.apply_social_distance(candidate_ub_recommendation_list, min_social_distance)
            candidate_random_recommendation_list = self.apply_social_distance(candidate_random_recommendation_list, min_social_distance)
        return filtered_ub_recommendation_json, random_recommendation_json

def main():
    recommender = Recommender()
    filtered_ub_recommendation_json, random_recommendation_json = recommender.dynamic_recommendation_pipeline(k_recommendations=3, k_max_neighbours=40, 
                                                                                                              k_min_neighbours=1, apply_social_distancing=False, 
                                                                                                              min_social_distance=2.0)

if __name__ == '__main__':
    main()
