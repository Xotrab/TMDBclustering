import tensorflow as tf
from keras import layers
from tqdm import tqdm
import numpy as np

class VariationalAutoencoder(tf.keras.Model):

    def __init__(self, latent_dim, input_width, input_height, optimizer=tf.keras.optimizers.Adam()):
        super(VariationalAutoencoder, self).__init__()

        self.latent_dim = latent_dim
        self.input_width = input_width
        self.input_height = input_height
        self.optimizer = optimizer

        # Encoder
        self.encoder_input = tf.keras.Input(shape=(self.input_width, self.input_height, 3), name='input')

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
        x = layers.Conv2D(128, 3, activation="relu", strides=2, padding="same")(x)

        # Flatten the output and pass it throught the dense layer
        x = layers.Flatten()(x)
        x = layers.Dense(self.latent_dim, activation="relu")(x)

        # Define the mean and variance vectors
        z_mean = layers.Dense(self.latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self.latent_dim, name="z_log_var")(x)

        # Define the latent space sampling layer
        z = layers.Lambda(self.sample_from_distribution, output_shape=(self.latent_dim,))([z_mean, z_log_var])

        # Instantiate and return the encoder model
        return tf.keras.Model(self.encoder_input, [z_mean, z_log_var, z], name="encoder")
    
    def build_decoder(self):
        x = layers.Dense(self.input_width // 8 * self.input_height // 8 * 128, activation="relu")(self.decoder_input)
        x = layers.Reshape((self.input_width // 8, self.input_height // 8, 128))(x)
        x = layers.Conv2DTranspose(128, 3, activation="relu", strides=2, padding="same")(x)
        x = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
        x = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
        decoder_output = layers.Conv2DTranspose(3, 3, activation="sigmoid", padding="same")(x)

        # Instantiate and return the decoder model
        return tf.keras.Model(self.decoder_input, decoder_output, name="decoder")

    # Forward pass of the model
    def call(self, input):
        z_mean, z_log_var, z = self.encoder(input)
        decoder_output = self.decoder(z)

        return decoder_output, z_mean, z_log_var, z
    
    def vae_loss(self, input, output, z_mean, z_log_var):
        # Calculate the reconstruction loss using the binary crossentropy
        reconstruction_loss = tf.keras.losses.binary_crossentropy(input, output) #Maybe should use MSE instead?

        # Reduce the loss by taking the mean across all dimensions but the batch dimension
        reconstruction_loss = tf.reduce_mean(reconstruction_loss, axis=(1, 2))
        
        # Calcualte the KL divergence loss
        kl_loss = -0.5 * tf.reduce_sum(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var), axis=-1)
        
        return reconstruction_loss + kl_loss
    
    def compile_model(self):
        self.compile(optimizer=self.optimizer)

    def train(self, data_loader, epochs):
        # x_train, x_test = data_loader.get_train_test_data()
        # self.fit(x_train, x_train, batch_size=data_loader.batch_size, epochs=epochs, validation_data=(x_test, x_test))
        # self.fit(data_loader, epochs=epochs)
         for epoch in range(epochs):

            progress_bar = tqdm(data_loader, desc=f"Epoch {epoch+1}/{epochs}", unit="batch")

            for batch in progress_bar:
                
                with tf.GradientTape() as tape:
                    decoder_output, z_mean, z_log_var, z = self.call(batch)
                    loss = self.vae_loss(batch, decoder_output, z_mean, z_log_var)
                
                gradients = tape.gradient(loss, self.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))

                # Update the progress bar description with the current loss
                progress_bar.set_postfix({"Loss": loss.numpy()})

            # Close the progress bar after each epoch
            progress_bar.close()

    def get_feature_vector(self, input):
        z_mean, _, _ = self.encoder(input)
        return z_mean
        