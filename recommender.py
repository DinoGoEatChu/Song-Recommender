import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import random
import webbrowser

# Load songs dataframe
songs = pd.read_csv("songs_w_links.csv")

from fuzzywuzzy import fuzz

def find_recommendations(song_title, artist):
    faves = songs[(songs['name'].str.lower().str.contains(song_title.lower())) & (songs['artists'].str.lower().str.contains(artist.lower()))]
    if faves.empty:
        return None
    clust = list(faves['cluster'])
    clustered = {}
    for i in clust:
        clustered[i] = clust.count(i)   
    fave_cluster = [(l, m) for l, m in sorted(clustered.items(), key=lambda item: item[1])][0][0]
    print('Favorite cluster: ', fave_cluster)
    recommendation = songs[(songs.cluster == fave_cluster) & (~songs['name'].str.lower().str.contains(song_title.lower()))].sort_values('popularity').sample(30).sort_values('popularity', ascending=False)
    return fave_cluster, recommendation.head(10)


def display_recommendations():
    song_id = song_entry.get().strip()
    artist_id = artist_entry.get().strip()
    fave_cluster_id = fave_cluster_entry.get().strip()
    
    if not song_id and not artist_id and not fave_cluster_id:
        messagebox.showerror("Error", "Please enter a song name or artist name or favorite cluster.")
        return
    
    if fave_cluster_id:
        try:
            fave_cluster = int(fave_cluster_id)
            recommendations = find_recommendations_by_cluster(fave_cluster).head(10)
        except ValueError:
            messagebox.showerror("Error", "Favorite cluster number must be an integer. Please try again.")
            return
        except KeyError:
            messagebox.showerror("Error", "Invalid favorite cluster number. Please try again.")
            return
    else:
        try:
            fave_cluster, recommendations = find_recommendations(song_id, artist_id)
        except IndexError:
            messagebox.showerror("Error", "Invalid song or artist name. Please try again.")
            return
    
    fave_cluster_label.config(text=f"Favorite Cluster: {fave_cluster}")

    # Remove the previous recommendations
    for widget in recommendations_list.winfo_children():
        widget.destroy()

    # Create a list to keep track of the song frames
    song_frames = []

    # Create a song frame for each recommendation
    for index, row in recommendations.iterrows():
        song_name = f"{row['name']} by {row['artists']}"
        song_link = row['link']
        song_frame = tk.Frame(recommendations_list)
        song_frame.pack(fill=tk.X)
        tk.Label(song_frame, text=song_name, width=85).pack(side=tk.LEFT)
        tk.Button(song_frame, text="Listen", fg="blue", cursor="hand2", borderwidth=0,
                  command=lambda link=song_link: webbrowser.open(link)).pack(side=tk.RIGHT, padx=5)
        song_frames.append(song_frame)

    # Pack the song frames into the recommendations list
    for song_frame in song_frames:
        recommendations_list.pack_slaves()


    # Pack the favorite cluster label into the window
    fave_cluster_label.pack()

def find_recommendations_by_cluster(fave_cluster):
    recommendations = songs[(songs.cluster == fave_cluster)].sort_values('popularity').sample(30).sort_values('popularity', ascending=False)
    return recommendations


# Create the main window and widgets
root = tk.Tk()
root.geometry("800x500")
root.title("Song Recommendation System")

# Create a custom font
custom_font = tkFont.Font(family="Helvetica", size=12)

fave_cluster_label = tk.Label(root, text="", font=custom_font)
fave_cluster_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

song_label = tk.Label(root, text="Favorite Song:", font=custom_font)
song_label.place(relx=0.25, rely=0.1, anchor=tk.CENTER)

song_entry = tk.Entry(root, font=custom_font)
song_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

artist_label = tk.Label(root, text="Artist:", font=custom_font)
artist_label.place(relx=0.25, rely=0.15, anchor=tk.CENTER)

artist_entry = tk.Entry(root, font=custom_font)
artist_entry.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

fave_cluster_entry = tk.Entry(root, font=custom_font)
fave_cluster_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

favorite_label = tk.Label(root, text="Favorite Cluster: ", font=custom_font)
favorite_label.place(relx=0.25, rely=0.2, anchor=tk.CENTER)



recommendations_button = tk.Button(root, text="Get Recommendations", font=custom_font, command=display_recommendations)
recommendations_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

recommendations_label = tk.Label(root, text="Recommendations: ", font=custom_font)
recommendations_label.place(relx=0.25, rely=0.35, anchor=tk.CENTER)

recommendations_list = tk.Listbox(root, height=12, width=75, font=custom_font)
recommendations_list.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


# Start the event loop
root.mainloop()