import pandas as pd
import random
import authorization # this is the script we created earlier
import numpy as np
from numpy.linalg import norm

df = pd.read_csv("valence_arousal_dataset.csv")
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
sp = authorization.authorize()

def recommend(track_id, ref_df, sp, n_recs = 5):
    
    # Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

def generate_moodvec(mood):
    if (mood == "happy"):
        valence = random.uniform(0.5, 1.0)
        energy = random.uniform(0.5, 1.0)
        return np.array([valence, energy])
    elif(mood == "angry"):
        valence = random.uniform(0.0, 0.5)
        energy = random.uniform(0.5, 1.0)
        return np.array([valence, energy])
    elif(mood == "sad"):
        valence = random.uniform(0.0, 0.5)
        energy = random.uniform(0.0, 0.5)
        return np.array([valence, energy])
    elif(mood == "calm"):
        valence = random.uniform(0.5, 1)
        energy = random.uniform(0.0, 0.5)
        return np.array([valence, energy])

def recommend_from_mood(mood, ref_df, n_recs = 5):
    # Generate Valence and Energy by mood
    track_moodvec = generate_moodvec(mood)
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

mad_world = "3JOVTQ5h8HGFnDdp4VT3MP"
list = recommend(track_id = mad_world, ref_df = df, sp = sp, n_recs = 5)
print(list)
list2 = recommend_from_mood("happy", ref_df=df, n_recs = 5)
print(list2)