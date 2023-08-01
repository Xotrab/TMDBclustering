import torch
import torch.nn as nn
import torch.optim
from tqdm import tqdm
import numpy as np

class VariationalAutoencoder(nn.Module):

    def __init__(self, latent_dim, input_width, input_height, optimizer=None, device="cuda"):
        super(VariationalAutoencoder, self).__init__()

        self.latent_dim = latent_dim
        self.input_width = input_width
        self.input_height = input_height
        self.device = device

        # Encoder
        encoder = self.build_encoder()
        self.sequential_encoder = encoder[0]
        self.mean_layer = encoder[1]
        self.log_var_layer = encoder[2]

        # Decoder
        self.decoder = self.build_decoder()
        self.optimizer = optimizer if optimizer is not None \
            else torch.optim.Adam(self.parameters(), lr=0.0003)
    
    # Create the vector based on the trained mean and variance parameters and the random value from the normal distribution
    def sample_from_distribution(self, args):
        z_mean, z_log_var = args
        epsilon = torch.randn_like(z_mean).to(self.device)
        return z_mean + torch.exp(0.5 * z_log_var) * epsilon

    def build_encoder(self):
        # Define convolution layers
        encoder_sequential = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),   #(128, 112)
            nn.LeakyReLU(0.1),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),  #(64, 56)
            nn.LeakyReLU(0.1),
            nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1),  #(32, 28)
            nn.LeakyReLU(0.1),
            nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1),  #(16, 14)
            nn.LeakyReLU(0.1),
            nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1),  #(8, 7)
            nn.LeakyReLU(0.1),
            nn.Flatten(),
            nn.Linear(8*7*64, self.latent_dim),
            nn.LeakyReLU(0.1)
        ).to(self.device)

        mean_layer = nn.Linear(self.latent_dim, self.latent_dim).to(self.device)
        log_var_layer = nn.Linear(self.latent_dim, self.latent_dim).to(self.device)

        return (encoder_sequential, mean_layer, log_var_layer)

    def build_decoder(self):
        decoder_sequential = nn.Sequential(
            nn.Linear(self.latent_dim, 8*7*64),
            nn.LeakyReLU(0.1),
            nn.Unflatten(1, (64, 8, 7)),
            nn.ConvTranspose2d(64, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.1),
            nn.ConvTranspose2d(64, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.1),
            nn.ConvTranspose2d(64, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.1),
            nn.ConvTranspose2d(64, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.1),
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.1),
            nn.Conv2d(32, 3, kernel_size=3, padding=1),
            nn.Sigmoid()
        ).to(self.device)

        return decoder_sequential
    
    # Forward pass of the model
    def forward(self, x):
        encoder_seq_out = self.sequential_encoder(x)
        z_mean = self.mean_layer(encoder_seq_out)
        z_log_var = self.log_var_layer(encoder_seq_out)
        sample = self.sample_from_distribution((z_mean, z_log_var))
        decoder_out = self.decoder(sample)
        return decoder_out, z_mean, z_log_var
    
    def vae_loss(self, input, output, z_mean, z_log_var):
        reconstruction_loss = nn.functional.binary_cross_entropy(input, output)
        kl_loss = -0.5 * (1 + z_log_var - z_mean.pow(2) - torch.exp(z_log_var)).mean()
        return reconstruction_loss * 1000 + kl_loss
    
    def train(self, data_loader, epochs):
        epoch_avg_train_losses = []
        for epoch in range(epochs):
            batch_train_losses = []
            progress_bar = tqdm(data_loader, desc=f"Epoch {epoch+1}/{epochs}", unit="batch")
            for batch in progress_bar:
                batch = batch.to(self.device)
                self.optimizer.zero_grad()

                decoder_output, z_mean, z_log_var = self.forward(batch)
                loss = self.vae_loss(decoder_output, batch, z_mean, z_log_var)
                loss.backward()
                self.optimizer.step()

                batch_train_losses.append(loss.item())

            epoch_average_train_loss = np.mean(batch_train_losses)
            epoch_avg_train_losses.append(epoch_average_train_loss)

            progress_bar.set_postfix({"Epoch average train loss": epoch_average_train_loss})

            # Close the progress bar after each epoch
            progress_bar.close()

        return epoch_avg_train_losses

    def get_feature_vector(self, input):
        encoder_output = self.sequential_encoder(input)
        return self.mean_layer(encoder_output)
        