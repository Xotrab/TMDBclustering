import tensorflow as tf
from keras import layers

class VariationalAutoencoder(tf.Keras.model):

    def __init__(self, latent_dim, input_width, input_height):
        super(VariationalAutoencoder, self).__init__()

        self.latent_dim = latent_dim
        self.input_width = input_width
        self.input_height = input_height

        # Encoder
        self.encoder_input = tf.keras.Input(shape=(self.input_width, self.input_height, 3), name='encoder_input')
        self.encoder = self.build_encoder()

        # Decoder
        self.decoder_input = tf.keras.Input(shape=(self.latent_dim,), name='decoder_input')
        self.decoder = self.build_decoder()
    
    # Create the vector based on the trained mean and variance parameters and the random value from the normal distribution
    def sample_from_distribution(self, args):
        z_mean, z_log_var = args

        distribution_shape = (tf.keras.backend.shape(z_mean)[0], self.latent_dim)
        epsilon = tf.keras.backend.random_normal(shape=distribution_shape, mean=0.0, stddev=1.0)

        return z_mean + tf.keras.backend.exp(0.5 * z_log_var) * epsilon

    def build_encoder(self):
        # Define convolution layers
        x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(self.encoder_input)
        x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)

        # Flatten the output and pass it throught the dense layer
        x = layers.Flatten()(x)
        x = layers.Dense(16, activation="relu")(x)

        # Define the mean and variance vectors
        z_mean = layers.Dense(self.latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self.latent_dim, name="z_log_var")(x)

        # Define the latent space sampling layer
        z = layers.Lambda(self.sample_from_distribution, output_shape=(self.latent_dim,))([z_mean, z_log_var])

        # Instantiate and return the encoder model
        return tf.keras.Model(self.encoder_input, [z_mean, z_log_var, z], name="encoder")
    
    def build_decoder(self):
        pass

    # Forward pass of the model
    def call(self, input):
        _, _, z = self.encoder(input)
        return self.decoder(z)
    
    def vae_loss(self):
        pass
    
    def compile_model(self):
        pass

    def train(self):
        pass

    def get_feature_vector(self, input):
        _, _, z = self.encoder(input)
        return z
        