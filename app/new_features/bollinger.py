import os
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_bollinger_chart(df, out_dir, window=20, num_std=2):
    os.makedirs(out_dir, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.png"
    path = os.path.join(out_dir, fname)

    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std  = df['Close'].rolling(window=window).std()
    upper_band   = rolling_mean + (rolling_std * num_std)
    lower_band   = rolling_mean - (rolling_std * num_std)

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(rolling_mean, label=f'{window}-Day MA')
    plt.plot(upper_band, label='Upper Band')
    plt.plot(lower_band, label='Lower Band')
    plt.fill_between(df.index, lower_band, upper_band, color='lightgray', alpha=0.5)
    plt.title(f"Bollinger Bands ({window}-Day)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return fname
