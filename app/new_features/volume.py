import os
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_volume_chart(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.png"
    path = os.path.join(out_dir, fname)

    colors = [
        'green' if close >= open_ else 'red'
        for open_, close in zip(df['Open'], df['Close'])
    ]

    plt.figure(figsize=(10, 3))
    plt.bar(df.index, df['Volume'], color=colors)
    plt.title("Daily Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return fname
