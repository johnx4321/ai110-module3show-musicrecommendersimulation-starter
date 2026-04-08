graph TD
    A["📥 INPUT: User Preferences"] --> A1["User Profile:<br/>- favorite_genre<br/>- favorite_mood<br/>- target_energy<br/>- preferred_valence<br/>- preferred_acousticness"]
    A --> A2["Favorite Song ID"]
    
    A1 --> B["📂 Load Songs CSV"]
    A2 --> B
    B --> B1["songs.csv<br/>18 songs with attributes:<br/>genre, mood, energy,<br/>valence, acousticness, etc."]
    
    B1 --> C["🔁 PROCESS: Score Each Song"]
    
    C --> C1["Filter: Exclude<br/>Favorite Song"]
    C1 --> C2["Initialize<br/>Scored_Songs = []"]
    
    C2 --> D["🎵 FOR EACH Candidate Song"]
    
    D --> D1["Calculate Scores"]
    D1 --> D1a["Genre Match<br/>+2 if match, +0 else"]
    D1 --> D1b["Mood Match<br/>+1 if match, +0 else"]
    D1 --> D1c["Energy Distance<br/>0-3 points based<br/>on proximity"]
    D1 --> D1d["Valence Check<br/>+1 if preference match"]
    D1 --> D1e["Acousticness Check<br/>+0.5 if preference match"]
    
    D1a --> D2["Sum All Scores"]
    D1b --> D2
    D1c --> D2
    D1d --> D2
    D1e --> D2
    
    D2 --> D3["Total Score<br/>for Song"]
    
    D3 --> D4["Add to List:<br/>Song + Score"]
    D4 --> D5["More Songs?"]
    
    D5 -->|YES| D["🎵 FOR EACH Candidate Song"]
    D5 -->|NO| E["📊 RANKING: Sort & Select"]
    
    E --> E1["Sort by Score<br/>Descending"]
    E1 --> E2["Select Top K<br/>Default K=3"]
    E2 --> E3["Apply Diversity<br/>Filter Optional"]
    
    E3 --> F["📤 OUTPUT: Top K Recommendations"]
    F --> F1["Recommendation 1<br/>Song Title + Score"]
    F --> F2["Recommendation 2<br/>Song Title + Score"]
    F --> F3["Recommendation 3<br/>Song Title + Score"]
    
    F1 --> G["Display to User"]
    F2 --> G
    F3 --> G
    
    style A fill:#e1f5ff
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#c8e6c9