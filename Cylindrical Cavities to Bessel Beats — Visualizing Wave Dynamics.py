import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.special import jv, jn_zeros
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import os

# ========== অ্যানিমে ভাইবের জন্য কালারম্যাপ ==========
colors = ['#0a0a2a', '#1a1a4a', '#ff4d4d', '#ff9e4d', '#ffe64d', '#4dff4d', '#4dd2ff', '#bf4dff']
anime_cmap = LinearSegmentedColormap.from_list('anime_vibe', colors, N=256)

# ========== প্যারামিটার সেটআপ ==========
radius = 1.0
freq_factor = 0.8
frames = 200
interval = 50

# ========== মোড সিলেক্ট ==========
modes_to_show = [
    (0, 1, "Mode (0,1) - Pure Radial", '#ff4d4d'),
    (1, 1, "Mode (1,1) - Dipole", '#4dff4d'),
    (2, 1, "Mode (2,1) - Quadrupole", '#4dd2ff'),
    (0, 2, "Mode (0,2) - 2nd Radial", '#ff9e4d'),
]

# গ্রিড তৈরি
r = np.linspace(0, radius, 150)
theta = np.linspace(0, 2*np.pi, 200)
R, Theta = np.meshgrid(r, theta)
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# ========== ফিগার সেটআপ ==========
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('⚡ CYLINDRICAL MODE VIBRATION ⚡\nBessel Beats | Anime Vibe Mode ON', 
             fontsize=16, fontweight='bold', color='#ff4d4d')
fig.patch.set_facecolor('#0a0a2a')

for ax in axes.flat:
    ax.set_facecolor('#0a0a2a')
    ax.set_xlim(-radius*1.1, radius*1.1)
    ax.set_ylim(-radius*1.1, radius*1.1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#ff4d4d')
        spine.set_linewidth(1.5)
    ax.grid(True, alpha=0.15, color='#4dd2ff', linestyle='--', linewidth=0.5)

# ========== অ্যানিমেশন ফাংশন ==========
def animate(frame):
    t = frame / frames * 2 * np.pi
    plots = []
    
    for ax, (m, n, title, color) in zip(axes.flat, modes_to_show):
        ax.clear()
        
        x_mn = jn_zeros(m, n)[-1]
        k_r = x_mn / radius
        
        radial_pattern = jv(m, k_r * R)
        azimuthal_pattern = np.cos(m * Theta - t * freq_factor * 2)
        time_variation = np.cos(t * freq_factor * 3)
        
        mode_strength = radial_pattern * azimuthal_pattern * time_variation
        mode_strength = mode_strength / np.max(np.abs(mode_strength)) * 0.8
        
        im = ax.pcolormesh(X, Y, mode_strength, cmap=anime_cmap, 
                           shading='auto', alpha=0.95)
        
        circle = patches.Circle((0, 0), radius, fill=False, 
                                 edgecolor=color, linewidth=3, alpha=0.8)
        ax.add_patch(circle)
        
        ax.axhline(0, color=color, alpha=0.3, linewidth=0.8)
        ax.axvline(0, color=color, alpha=0.3, linewidth=0.8)
        
        ax.set_title(f'{title}\n⏱️ t = {t/(2*np.pi)*100:.1f}% cycle', 
                    color=color, fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#0a0a2a', 
                             edgecolor=color, alpha=0.7))
        
        ax.text(0.05, 0.95, f'⚡ m={m} n={n} ⚡', transform=ax.transAxes,
               color=color, fontsize=9, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='#0a0a2a', alpha=0.8))
        
        plots.append(im)
    
    return plots

# অ্যানিমেশন তৈরি
anim = FuncAnimation(fig, animate, frames=frames, interval=interval, blit=False, repeat=True)

# ========== ভিডিও সেভ ==========
print("🎬 রেন্ডারিং শুরু...")

# GIF সেভ
gif_filename = 'cylindrical_modes_anime.gif'
anim.save(gif_filename, writer=PillowWriter(fps=20), dpi=100)
print(f"✅ GIF সেভ হয়েছে: {os.path.abspath(gif_filename)}")

# MP4 চেষ্টা
try:
    mp4_filename = 'cylindrical_modes_anime.mp4'
    anim.save(mp4_filename, writer='ffmpeg', fps=20, dpi=100, bitrate=2000)
    print(f"✅ MP4 সেভ হয়েছে: {os.path.abspath(mp4_filename)}")
except Exception as e:
    print(f"⚠️ MP4 সেভ হয়নি: {e}")
    print("   টিপ: 'pip install ffmpeg-python' রান করো অথবা FFmpeg ইনস্টল করো")

plt.tight_layout()
plt.show()

print("\n✨ সম্পন্ন! ফাইল চেক করো ✨")