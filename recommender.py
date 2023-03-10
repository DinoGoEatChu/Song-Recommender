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

def find_recommendations(song_id):
    faves = songs[songs.name.isin([song_id])]
    clust = list(faves['cluster'])
    clustered = {}
    for i in clust:
        clustered[i] = clust.count(i)   
    fave_cluster = [(l, m) for l, m in sorted(clustered.items(), key=lambda item: item[1])][0][0]
    print('Favorite cluster: ', fave_cluster)
    recommendation = songs[songs.cluster == fave_cluster].sort_values('popularity').sample(30).sort_values('popularity', ascending=False)
    return recommendation.head(10)



def display_recommendations():
    song_id = song_entry.get().strip()
    if not song_id:
        messagebox.showerror("Error", "Please enter a song name.")
        return
    
    try:
        recommendations = find_recommendations(song_id)
    except IndexError:
        messagebox.showerror("Error", "Invalid song name. Please try again.")
        return

    recommendations_list.delete(0, tk.END)
    for index, row in recommendations.iterrows():
        song_name = f"{row['name']} by {row['artists']}"
        song_link = row['link']
        song_frame = tk.Frame(recommendations_list)
        song_frame.pack(fill=tk.X)
        tk.Label(song_frame, text=song_name, width=60).pack(side=tk.LEFT)
        tk.Button(song_frame, text="Listen", fg="blue", cursor="hand2", borderwidth=0,
                  command=lambda link=song_link: webbrowser.open(link)).pack(side=tk.RIGHT, padx=5)






# Create the main window and widgets
root = tk.Tk()
root.geometry("700x500")
root.title("Song Recommendation System")



# Create a custom font
custom_font = tkFont.Font(family="Helvetica", size=12)

song_label = tk.Label(root, text="Favorite Song:", font=custom_font)
song_label.place(relx=0.25, rely=0.1, anchor=tk.CENTER)

song_entry = tk.Entry(root, font=custom_font)
song_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

recommendations_button = tk.Button(root, text="Get Recommendations", font=custom_font, command=display_recommendations)
recommendations_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

recommendations_label = tk.Label(root, text="Recommendations:", font=custom_font)
recommendations_label.place(relx=0.25, rely=0.35, anchor=tk.CENTER)

recommendations_list = tk.Listbox(root, height=12, width=75, font=custom_font)
recommendations_list.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Start the event loop
root.mainloop()