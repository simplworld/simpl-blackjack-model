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
            'deck': [],
            'player_cards': [],
            'dealer_cards': [],
            'player_score': 0,
            'dealer_score': 0,
            'player_busted': False,
            'dealer_busted': False,
            'push': False,
            'player_done': False
        }

    def createDeck(self):
        deck = []
        ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        suits = ['H', 'S', 'C', 'D']

        for rank in ranks:
            for suit in suits:
                deck.append({
                        'rank': rank,
                        'suit': suit
                    })

        random.shuffle(deck)
        return deck

    def calcRankScore(self, rank):
        score = {
            'hard_total': 0,
            'soft_total': 0
        }
        if (rank == 'A'):
            score['hard_total'] += 1
            score['soft_total'] += 1 if ((score['soft_total'] + 11) > 21) else 11
        elif isinstance(rank, str):
            score['hard_total'] += 10
            score['soft_total'] += 10
        else:
            score['hard_total'] += rank
            score['soft_total'] += rank
        return score

    def calcTotal(self, score):
        if score['hard_total'] == 21 or score['soft_total'] == 21:
            return 21
        elif score['soft_total'] > 21:
            return score['hard_total']
        return score['soft_total']

    def calcHandScore(self, cards):
        score = 0
        for card in cards:
            score += self.calcTotal(self.calcRankScore(card['rank']))
        return score

    def isBusted(self, score):
        return score > 21

    def step(self, action, data={}):
        """
        Parameters:
            action - current period's decision
            prev_total - the calculated total from the previous period
        Returns new total
        """
        if action == 'deal':
            deck = self.createDeck()
            self.data['deck'] = deck
            self.data['player_cards'].append(deck.pop())
            self.data['dealer_cards'].append(deck.pop())
            self.data['player_cards'].append(deck.pop())
            self.data['player_score'] = self.calcHandScore(self.data['player_cards'])
            self.data['dealer_score'] = self.calcHandScore(self.data['dealer_cards'])
            return self.data

        elif action == 'hit':
            card = data.get('deck', []).pop()
            data['player_cards'].append(card)
            data['player_score'] = self.calcHandScore(data['player_cards'])
            data['player_busted'] = self.isBusted(data['player_score'])
            if data['player_busted']:
                data['player_done'] = True
            return data
        elif action == 'stand':
            data['player_done'] = True
            while data['dealer_score'] < 19:
                card = data.get('deck', []).pop()
                data['dealer_cards'].append(card)
                data['dealer_score'] = self.calcHandScore(data['dealer_cards'])
            data['dealer_busted'] = self.isBusted(data['dealer_score'])
            if data['dealer_score'] == data['player_score']:
                data['push'] = True
            if data['dealer_score'] < data['player_score']:
                data['player_busted'] = True
            if data['dealer_score'] > data['player_score']:
                data['dealer_busted'] = True
            if data['dealer_score'] == data['player_score']:
                data['push'] = True
            return data
