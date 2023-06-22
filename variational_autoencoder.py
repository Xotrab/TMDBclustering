import tensorflow as tf
from keras import layers

class VariationalAutoencoder(tf.Keras.model):

    def __init__(self, latent_dim, input_width, input_height):
        super(VariationalAutoencoder, self).__init__()

        self.latent_dim = latent_dim
        self.input_width = input_width
        self.input_height = input_height

        # Encoder
        self.encoder_input = tf.keras.Input(shape=(self.input_width, self.input_height, 3))
        self.encoder = self.build_encoder()

        # Decoder
        self.decoder_input = tf.keras.Input(shape=(self.latent_dim,))
        self.decoder = self.build_decoder()
    
    def build_encoder(self):
        pass
    
    def build_decoder(self):
        pass

    # Forward pass of the model
    def call(self, input):
        z_mean, z_log_var, z = self.encoder(input)
        return self.decoder(z)
    
    def vae_loss(self):
        pass
    
    def compile_model(self):
        pass

    def train(self):
        pass
        