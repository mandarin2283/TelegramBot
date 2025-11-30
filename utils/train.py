class Train:

    def __init__(self,date,train_type,approaches):
        self.date = date
        self.train_type = train_type
        self.approaches = self.parse_approaches(approaches)

    def __str__(self):
        return f"{self.date},{self.train_type}"

    @classmethod
    def create(cls,data):
        date,type_of_train,approaches = data.split(';')
        return cls(date,type_of_train,approaches)

    @staticmethod
    def parse_approaches(approaches):
        train = dict()
        for approach in approaches.split('/'):
            exercise,repeats = approach.split('х')
            exercise,weight = exercise.split(',')
            repeats = repeats.split(',')
            train[exercise] = (weight,repeats)
        return train

    def get_data(self):
        return (self.date,self.train_type,self.approaches)

