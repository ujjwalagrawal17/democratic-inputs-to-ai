import numpy as np

from typing import List


def get_group_vote_probability(vote_matrix: np.ndarray, users_in_group: np.ndarray, vote: int) -> np.ndarray:
    """Calculates the probability of a group of users voting for a given vote
    
    Args:
        vote_matrix (np.ndarray): A matrix of votes, where each row is a user and each column is a statement
        users_in_group (List[int]): A list of user ids that are in the group
        vote (int): The vote to calculate the probability for (1 or -1)

    Returns:
        np.ndarray: The probability of the group of users voting for the given vote for all statements
    """
        
    # Calculate in-group statistics
    num_group_users_voted_for = np.sum(vote_matrix[users_in_group] == vote, axis=0)
    num_group_users_voted = np.sum(vote_matrix[users_in_group] != 0, axis=0)
    probability_group_vote_for = (1 + num_group_users_voted_for) / (2 + num_group_users_voted)

    return probability_group_vote_for


def get_responsiveness(vote_matrix: np.ndarray, users_in_group: np.ndarray, vote: int) -> float:
    """Calculates the responsiveness score of a group of users for a given vote
    
    Args:
        vote_matrix (np.ndarray): A matrix of votes, where each row is a user and each column is a statement
        users_in_group (List[int]): A list of user ids that are in the group
        vote (int): The vote to calculate the responsiveness for (1 or -1)

    Returns:
        float: The responsiveness score of the group of users for the given vote for all statements
    """
    
    # Calculate in-group statistics
    probability_group_vote_for = get_group_vote_probability(vote_matrix, users_in_group, vote)

    # calculate out-group statistics
    users_out_group = np.setdiff1d(np.arange(vote_matrix.shape[0]), users_in_group)
    probability_out_group_vote_for = get_group_vote_probability(vote_matrix, users_out_group, vote)

    # calculate responsiveness
    responsiveness = probability_group_vote_for / probability_out_group_vote_for
    return responsiveness


def get_concensus_metric(vote_matrix: np.ndarray, user_groups: List[np.ndarray], vote: int) -> float:
    """Calculates the concensus metric for a given vote
    
    Args:
        vote_matrix (np.ndarray): A matrix of votes, where each row is a user and each column is a statement
        user_groups (List[np.ndarray]): A list of arrays of user ids that are in each group
        vote (int): The vote to calculate the concensus metric for (1 or -1)

    Returns:
        float: The concensus metric for the given vote
    """

    group_vote_probabilities = [get_group_vote_probability(vote_matrix, group, vote) for group in user_groups]
    concensus_metric = np.prod(group_vote_probabilities)
    return concensus_metric

