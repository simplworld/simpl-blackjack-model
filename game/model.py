class Model(object):
    """
    The model adds an operand to the previous total and returns the result.
    """

    def step(self, operand, prev_total=0.0):
        """
        Parameters:
            operand - current period's decision
            prev_total - the calculated total from the previous period
        Returns new total
        """
        return operand + prev_total
