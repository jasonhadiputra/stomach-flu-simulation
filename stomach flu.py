import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

def init_env(probSusceptible, probInfectious):
    """
    Menginisialisasi matriks 25x25 yang berisikan angka status orang tersebut.
    Perhatikan bahwa peluang seseorang bersifat Immune di awal
    simulasi adalah `probImmune = 1 - probSusceptible - probInfectious`.
    \n\t`0`: Susceptible
    \n\t`1-2`: Infectious
    \n\t`3-7`: Immune

    Parameters
    ----------
    probSusceptible : float
        Peluang seseorang bersifat Susceptible di awal.
    probInfectious : float
        Peluang seseorang bersifat Infectious di awal.

    Returns
    -------
    env : 25x25 matrix
        Kondisi awal dari simulasi.

    """
    # Kalau jumlah peluangnya lebih dari 1, bubar
    if probSusceptible + probInfectious > 1:
        return("Error")
    
    # Inisialisasi matriks 25x25
    env = [[0 for i in range(25)] for j in range(25)]
    
    # Mengisi matriks
    for i in range(25):
        for j in range(25):
            
            # Random dan isi sesuai hasil random dan peluangnya
            rand = random.random()
            if rand < probSusceptible:
                env[i][j] = 0
            elif rand < probSusceptible + probInfectious:
                env[i][j] = random.randint(1,2)
            else:
                env[i][j] = random.randint(3,7)
                
    return env

def extend(env):
    """
    Menambahkan absorbing boundary yang berisikan orang-orang Immune (`7`).

    Parameters
    ----------
    env : 25x25 matrix
        Matriks awal.

    Returns
    -------
    extEnv : 27x27 matrix
        Matriks awal yang sudah diperluas.

    """
    # Inisialisasi matriks berisi orang Immune
    extEnv = [[7 for i in range(27)] for j in range(27)]
    
    # Salin env ke extEnv
    for i in range(1,26):
        for j in range(1,26):
            extEnv[i][j] = env[i-1][j-1]
    
    return extEnv

def spread(coordinates, extEnv):
    """
    Menyebarkan penyakit ke sekitar seseorang di `coordinates` dari `extEnv`
    secara Von Neumann. Sebagai penanda bahwa sel tersebut sudah diperbaharui,
    nilainya negatif dari yang seharusnya.

    Parameters
    ----------
    coordinates : array of 2 integers
        Koordinat dari seseorang yang sakit di iterasi sebelumnya di `extEnv`.
    extEnv : 27x27 matrix
        Matriks tempat penyebaran penyakit terjadi.

    Returns
    -------
    extEnv : 27x27 matrix
        Matriks tempat penyebaran penyakit terjadi setelah penyebaran penyakit.

    """
    # Kalau orang tersebut Infectious,
    if 1 <= extEnv[coordinates[0]][coordinates[1]] <= 2:
        
        # Untuk setiap tetangga Von Neumann-nya
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 or j == 0:
                    
                    # Cek apakah tetangganya Susceptible
                    if extEnv[coordinates[0] + i][coordinates[1] + j] == 0:
                        # Kalau susceptible, jadikan Infectious tapi updated (-1)
                        extEnv[coordinates[0] + i][coordinates[1] + j] = -1
                    
    return extEnv

def iterate(env):
    """
    Melakukan satu kali iterasi sesuai aturan yang diberikan.

    Parameters
    ----------
    env : 25x25 matrix
        Matriks tempat iterasi terjadi.

    Returns
    -------
    objective : 25x25 matrix
        Matriks hasil iterasi.

    """
    # Perluas
    extEnv = extend(env)
    
    # Inisiasi lingkungan setelah iterasi
    objective = [[0 for i in range(25)] for j in range(25)]
    
    # Data lokasi Infectious
    coordinatesInfectious = []
    for i in range(1,26):
        for j in range(1,26):
            
            # Kalau Infectious, simpan koordinatnya
            if 1 <= extEnv[i][j] <= 2:
                coordinatesInfectious.append([i,j])
    
    # Sebar penyakitnya
    for coordinates in coordinatesInfectious:
        extEnv = spread(coordinates, extEnv)
        
    # Finalisasi extEnv dan simpan hasil
    for i in range(1,26):
        for j in range(1,26):
            
            # Kalau nilai selnya lebih dari 0 dan belum update, update
            if extEnv[i][j] > 0:
                extEnv[i][j] = (extEnv[i][j] + 1) % 8
            # Kalau sudah update (-1), jadikan nilai yang seharusnya (1)
            elif extEnv[i][j] < 0:
                extEnv[i][j] = abs(extEnv[i][j])
                
            # Simpan hasil ke objective
            objective[i-1][j-1] = extEnv[i][j]
            
    return objective

def someone_is_not_susceptible(env):
    """
    Mengecek apakah ada seseorang yang tidak Susceptible di `env`.
    
    Parameters
    ----------
    env : 25x25 matrix
        Tempat pengecekan dilakukan

    Returns
    -------
    bool
        Nilai kebenaran keadaan seseorang yang tidak Susceptible.

    """
    # Untuk setiap sel di env
    for i in range(25):
        for j in range(25):
            
            # Kalau ada yang tidak Susceptible, True
            if env[i][j] != 0:
                return True
            
    # Kalau setelah cek semua tidak ada, False
    else:
        return False

def simulate(probSusceptible, probInfectious, maxIter = 30):
    """
    Melakukan simulasi dan menghasilkan daftar lingkungan.

    Parameters
    ----------
    probSusceptible : float
        Peluang seseorang bersifat Susceptible di awal.
    probInfectious : float
        Peluang seseorang bersifat Infectious di awal.
    maxIter : int, default: 30
        Banyak simulasi maksimal.

    Returns
    -------
    listEnv : 25x25x? matrix
        Daftar `env` dari awal hingga akhir simulasi

    """
    # Inisialisasi
    listEnv = []
    listEnv.append(init_env(probSusceptible,probInfectious))
    numberSim = 1
    
    # Simulasikan selama masih ada yang bisa berubah dan
    # jumlah simulasi belum sama dengan maxIter
    while someone_is_not_susceptible(listEnv[-1]) and numberSim < maxIter:
        listEnv.append(iterate(listEnv[-1]))
        numberSim += 1
        
    return listEnv

# Jumlah iterasi maksimal
maxIter = 60

# Set colormap yang sesuai
# Hari 0   / Susceptible: hijau
# Hari 1-2 / Infectious : biru
# Hari 3-7 / Immune     : merah
cmap_flu = ListedColormap(["forestgreen",
                           "deepskyblue", "skyblue",
                           "maroon", "firebrick", "indianred", "lightcoral", "mistyrose"])

# Jangan tunjukkan plot
plt.ioff()

for probSusceptible in np.linspace(0.1, 0.9, 9):
    for probInfectious in np.linspace(0.1, 1-probSusceptible, round(10 * (1-probSusceptible))):
        
        # Antisipasi rounding error
        probSusceptible = round(probSusceptible, 1)
        probInfectious = round(probInfectious, 1)
        
        # Tentukan probImmune dan hasil simulasinya
        probImmune = abs(round(1 - probInfectious - probSusceptible, 1))
        listEnv = simulate(probSusceptible, probInfectious, maxIter)
        
        # Buat figure dan axis matplotlib
        fig, ax = plt.subplots()
        
        # Buat figure-nya kotak ukuran 5x5 inci
        fig.set_size_inches(5,5)

        # Buat judul
        image = ax.set_title(
            f"Probability: Sus = {probSusceptible}, Inf = {probInfectious}, Imm = {probImmune}")
            
        # Fungsi update frame
        def update(frame):
            # Buat gambar
            image = ax.imshow(listEnv[frame], cmap_flu, vmin = 0, vmax = 7)
            
            return [image]
        
        # Fungsi animasi
        ani = FuncAnimation(fig, update, frames=np.arange(len(listEnv)), interval = 2000)
        
        # Hilangkan spine dan tick dari axis
        plt.axis("off")
        
        # Save
        ani.save(f"C:/Users/jason/Google Drive/Sikomat/Stomach Flu Videos/s{probSusceptible} i{probInfectious}.gif")

