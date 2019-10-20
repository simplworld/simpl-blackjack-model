import random


class Model(object):
    """
    The model modifies the game data based on 3 action:
        1. 'deal'
            - creates a new deck
            - shuffles the cars and deals the cards
            - calcualtes the scores for each player
        2. 'hit'
            - adds a new card on the player hand
            - calculates the score for the player
        3. 'stand'
            - adds cards to the dealer hand
            - calculates the score for the player
            - calculates the result of the game
    """

    def __init__(self):
        self.data = {
            "deck": [],
            "player_cards": [],
            "dealer_cards": [],
            "player_score": 0,
            "dealer_score": 0,
            "player_busted": False,
            "dealer_busted": False,
            "push": False,
            "player_done": False,
        }

    def createDeck(self):
        deck = []
        ranks = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        suits = ["H", "S", "C", "D"]

        for rank in ranks:
            for suit in suits:
                deck.append({"rank": rank, "suit": suit})

        random.shuffle(deck)
        return deck

    def calcRankScore(self, rank):
        score = {"hard_total": 0, "soft_total": 0}
        if rank == "A":
            score["hard_total"] += 1
            score["soft_total"] += 1 if ((score["soft_total"] + 11) > 21) else 11
        elif isinstance(rank, str):
            score["hard_total"] += 10
            score["soft_total"] += 10
        else:
            score["hard_total"] += rank
            score["soft_total"] += rank
        return score

    def calcTotal(self, score):
        if score["hard_total"] == 21 or score["soft_total"] == 21:
            return 21
        elif score["soft_total"] > 21:
            return score["hard_total"]
        return score["soft_total"]

    def calcHandScore(self, cards):
        score = 0
        for card in cards:
            score += self.calcTotal(self.calcRankScore(card["rank"]))
        return score

    def isBusted(self, score):
        return score > 21

    def dealerTurn(self, data):
        data["player_done"] = True
        while data["dealer_score"] < 21:
            card = data.get("deck", []).pop()
            data["dealer_cards"].append(card)
            data["dealer_score"] = self.calcHandScore(data["dealer_cards"])
        data["dealer_busted"] = self.isBusted(data["dealer_score"])
        if data["dealer_score"] < data["player_score"]:
            data["player_busted"] = True
        if data["dealer_score"] > data["player_score"]:
            data["dealer_busted"] = True
        if data["dealer_score"] == data["player_score"]:
            data["push"] = True
        return data

    def step(self, action, data=None):
        """
        Parameters:
            action - current period's decision
            data - the game data (cards, scores etc)
        Returns new total
        """
        print("Stepping!")
        print(action)
        print(data)
        if data is None:
            data = {}

        if action == "new":
            return self.data

        if action == "deal":
            deck = self.createDeck()
            deal_data = self.data.copy()
            deal_data["deck"] = deck
            deal_data["player_cards"].append(deck.pop())
            deal_data["dealer_cards"].append(deck.pop())
            deal_data["player_cards"].append(deck.pop())
            deal_data["player_score"] = self.calcHandScore(deal_data["player_cards"])
            deal_data["dealer_score"] = self.calcHandScore(deal_data["dealer_cards"])
            return deal_data

        elif action == "hit":
            card = data.get("deck", []).pop()
            data["player_cards"].append(card)
            data["player_score"] = self.calcHandScore(data["player_cards"])
            data["player_busted"] = self.isBusted(data["player_score"])
            if data["player_busted"]:
                data["player_done"] = True
            if data["player_score"] == 21:
                data = self.dealerTurn(data)
            return data
        elif action == "stand":
            data = self.dealerTurn(data)
            return data
