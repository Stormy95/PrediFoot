import T00_cons

import numpy as np
import json
import tensorflow as tf

def normalise_features_per_fifa(column):
    assert isinstance(column, np.ndarray)

    dmin = column.min()
    dmax = column.max()

    return ((column - dmin) / (dmax - dmin)).clip(min=0,max=1)

class NeuralNet:
    def __init__(self, hidden_nodes=8, keep_prob=1.0, learning_rate=0.001):
        self.hidden_nodes = hidden_nodes
        self.keep_prob_value = keep_prob
        self.learning_rate = learning_rate

        self.graph = tf.Graph()
        self.input = None
        self.keep_prob = None
        self.target = None
        self.loss = None
        self.train = None
        self.output = None
        self.training_summary = None
        self.validation_summary = None

        self.build_model()

    def build_model(self):
        with self.graph.as_default():
            self.input = tf.placeholder(tf.float32, shape=[None, 6], name='input')
            self.target = tf.placeholder(tf.float32, shape=[None, 3], name='target')
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            hidden_layer = tf.layers.dense(self.input, 16, activation=tf.nn.relu, name="hidden_layer")
            hidden_layer2 = tf.layers.dense(hidden_layer, 8, activation=tf.nn.relu, name="hidden_layer2")
            self.output = tf.layers.dense(hidden_layer2, 3, name="output")
            self.output = tf.nn.softmax(self.output, name='softmax')

            with tf.name_scope('losses') as scope:
                self.loss = tf.losses.absolute_difference(self.target, self.output)

                self.train = tf.train.MomentumOptimizer(self.learning_rate, 0.99).minimize(self.loss)

            self.training_summary = tf.summary.scalar("training_accuracy", self.loss)
            self.validation_summary = tf.summary.scalar("validation_accuracy", self.loss)

    @staticmethod
    def init_saver(sess):
        writer = tf.summary.FileWriter('./tf-log-SP1/', sess.graph)
        saver = tf.train.Saver(max_to_keep=1)
        return writer, saver

    def train_model(self, X, y, X_val, y_val, model_name):

        best_val_loss = 0.30

        with tf.Session(graph=self.graph) as sess:

            writer, saver = self.init_saver(sess)

            sess.run(tf.global_variables_initializer())

            for i in range(40000): #40000

                feed_dict = {self.input: X, self.target: y, self.keep_prob: 0.8}

                _, current_loss, train_sum = sess.run([self.train, self.loss, self.training_summary],
                                                      feed_dict=feed_dict)

                if i % 1000 == 0:
                    val_loss, val_sum = sess.run([self.loss, self.validation_summary],
                                                 feed_dict={self.input: X_val, self.target: y_val, self.keep_prob: 1.0})
                    writer.add_summary(val_sum, i)
                    writer.add_summary(train_sum, i)

                    print(i, current_loss, val_loss)
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        saver.save(sess, model_name)

    def predict(self, X, model_name):

        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(model_name + '.meta')
            saver.restore(sess, model_name)
            graph = tf.get_default_graph()
            input = graph.get_tensor_by_name('input:0')
            keep_prob = graph.get_tensor_by_name('keep_prob:0')
            output = graph.get_tensor_by_name('softmax:0')
            feed_dict = {input: X, keep_prob: 1.0}
            predictions = sess.run(output, feed_dict=feed_dict)

        return predictions

##################################################################

league = T00_cons.league
seasonV = T00_cons.seasonV

##################################################################

if __name__ == '__main__':
    tf.set_random_seed(8)
    np.random.seed(8)

    season = 18

    path = './data/' + league + '/vectors/'
    in_i = path + 'in_season_'
    out_i = path + 'out_odds_season_'
    # out_i = path + 'out_result_season_'
    ext = '.txt'

    in_14 = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(in_i + '14' + ext, dtype=float))
    in_15 = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(in_i + '15' + ext, dtype=float))
    in_16 = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(in_i + '16' + ext, dtype=float))
    in_17 = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(in_i + '17' + ext, dtype=float))
    in_18 = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(in_i + '18' + ext, dtype=float))

    out_14 = np.loadtxt(out_i + '14' + ext, dtype=float)
    out_15 = np.loadtxt(out_i + '15' + ext, dtype=float)
    out_16 = np.loadtxt(out_i + '16' + ext, dtype=float)
    out_17 = np.loadtxt(out_i + '17' + ext, dtype=float)
    out_18 = np.loadtxt(out_i + '18' + ext, dtype=float)

    c = 20
    in_18_train = in_18[:-60-c]
    out_18_train = out_18[:-60-c]

    validation_in = in_18[-60-c:-10-c]
    validation_out = out_18[-60-c:-10-c]

    train_in = np.vstack((#in_14,
                        in_15,
                        in_16,
                        in_17,
                        in_18_train ))

    train_out = np.vstack((#out_14,
                         out_15,
                         out_16,
                         out_17,
                         out_18_train  ))



    # HEY HEY HEY: If odds output !!!!!
    train_out = 1 / train_out
    validation_out = 1 / validation_out
    ##################################################################

    net = NeuralNet()
    path_model = './data/' + league + '/model/'
    m_name = path_model + 'TF_chris'

    net.train_model(train_in, train_out, validation_in, validation_out, model_name= m_name)

    net = NeuralNet()
