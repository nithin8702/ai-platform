""" Mushroom Classifier Model Training """
import pickle
import pandas as pd
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class MushroomClassifier:
    def load_data(self):
        """ Load the dataset and encode the columns """
        data = pd.read_csv("train_dataset.csv")
        labelencoder=LabelEncoder()
        for col in data.columns:
            data[col] = labelencoder.fit_transform(data[col])
        return data
    def split(self, df):
        """ To split dataset into train and test by some ratio """
        y, x = df.type, df.drop(columns=['type'])
        self.x_train, self.x_test, self.y_train, self.y_test \
            = train_test_split(x, y, test_size=0.3, random_state = 0)
    def build_model(self, name):
        """ To build 2 models - SVC and LogisticRegression """
        if name == 'SVC':
            model = SVC()
            model.fit(self.x_train, self.y_train)
        elif name == 'LR':
            model = LogisticRegression(max_iter=1000)
            model.fit(self.x_train, self.y_train)
        return model
    def save_model(self, model, name):
        """ To save the model into pickle format for model prediction """
        with open(name + '.pkl', 'wb') as model_pkl:
            pickle.dump(model, model_pkl, protocol=2)
if __name__ == '__main__':
    clf = MushroomClassifier()
    df = clf.load_data()
    clf.split(df)
    class_names = ['edible', 'poisonous']
    svc = clf.build_model('SVC')
    clf.save_model(svc, 'svc_model')
    lr = clf.build_model('LR')
    clf.save_model(lr, 'lr_model')
