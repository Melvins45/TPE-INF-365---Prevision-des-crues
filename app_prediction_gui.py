import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class FloodProbabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prevision de Probabilite d'Inondation - TPE INF 365")
        self.root.geometry("900x900")
        self.root.configure(bg="#f0f0f0")
        
        self.models_dir = "models"
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
        
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_and_train_model()
        
        self.create_widgets()
        
    def load_and_train_model(self):
        try:
            model_path = os.path.join(self.models_dir, "regression_lineaire_model.joblib")
            scaler_path = os.path.join(self.models_dir, "scaler.joblib")
            features_path = os.path.join(self.models_dir, "features.joblib")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(features_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.feature_names = joblib.load(features_path)
            else:
                data_path = os.path.join('datas', 'flood.csv')
                df = pd.read_csv(data_path)
                
                target_col = "FloodProbability"
                X = df.drop(target_col, axis=1)
                y = df[target_col]
                
                self.feature_names = X.columns.tolist()
                
                self.scaler = StandardScaler()
                X_scaled = self.scaler.fit_transform(X)
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.2, random_state=42
                )
                
                self.model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
                self.model.fit(X_train, y_train)
                
                train_score = self.model.score(X_train, y_train)
                test_score = self.model.score(X_test, y_test)
                
                joblib.dump(self.model, model_path)
                joblib.dump(self.scaler, scaler_path)
                joblib.dump(self.feature_names, features_path)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le modèle:\n{str(e)}")
    
    def create_widgets(self):
        
        header_frame = tk.Frame(self.root, bg="#1C2833", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(
            header_frame,
            text="Prevision des Crues",
            font=("Arial", 24, "bold"),
            bg="#1C2833",
            fg="white"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            header_frame,
            text="Predicteur de Probabilite d'Inondation - TPE INF 365, Groupe 24",
            font=("Arial", 10),
            bg="#1C2833",
            fg="#3498db"
        )
        subtitle.pack()
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form_title = tk.Label(
            scrollable_frame,
            text="1. Saisissez les parametres environnementaux",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        )
        form_title.pack(pady=10)
        
        self.input_fields = {}
        
        self.grid_container = tk.Frame(scrollable_frame, bg="#f0f0f0")
        self.grid_container.pack(fill="both", expand=True, padx=10)
        
        self.descriptions = {
            "MonsoonIntensity": "Intensité Mousson (0: Faible | 10: Extrême)",
            "TopographyDrainage": "Drainage Naturel (0: Excellent | 10: Nul)",
            "RiverManagement": "Gestion Rivières (0: Parfaite | 10: Absente)",
            "Deforestation": "Déforestation (0: Nulle | 10: Totale)",
            "Urbanization": "Urbanisation (0: Rurale | 10: Intense)",
            "ClimateChange": "Climat (0: Stable | 10: Critique)",
            "DamsQuality": "Qualité Barrages (0: Robustes | 10: Fragiles)",
            "Siltation": "Sédimentation (0: Nulle | 10: Grave)",
            "AgriculturalPractices": "Pratiques Agricoles (0: Durables | 10: Risquées)",
            "Encroachments": "Empiétements (0: Aucun | 10: Massifs)",
            "IneffectiveDisasterPreparedness": "Gestion Catastrophes (0: Prêt | 10: Imprévu)",
            "DrainageSystems": "Systèmes Drainage (0: Modernes | 10: Obsolètes)",
            "CoastalVulnerability": "Zones Côtières (0: Protégées | 10: Exposées)",
            "Landslides": "Glissements Terrain (0: Stables | 10: Fréquents)",
            "Watersheds": "Bassins Versants (0: Sains | 10: Dégradés)",
            "DeterioratingInfrastructure": "Infrastructures (0: Neuves | 10: Vétustes)",
            "PopulationScore": "Densité Population (0: Faible | 10: Critique)",
            "WetlandLoss": "Perte Zones Humides (0: Aucune | 10: Totale)",
            "InadequatePlanning": "Planification (0: Rigoureuse | 10: Nulle)",
            "PoliticalFactors": "Facteurs Politiques (0: Stables | 10: Instables)"
        }
        
        self.create_responsive_grid()
        
        self.root.bind("<Configure>", self.on_window_resize)
        
        self.bind_mouse_wheel(canvas)
        
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10, fill=tk.X, padx=10)
        
        predict_btn = tk.Button(
            button_frame,
            text="2. Predire la Probabilite d'Inondation",
            command=self.predict,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        predict_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            button_frame,
            text="Reinitialiser",
            command=self.reset_fields,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.result_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, bd=2)
        self.result_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="3. Resultat: Entrez les parametres et cliquez sur 'Predire' pour obtenir le resultat",
            font=("Arial", 11),
            bg="white",
            fg="#7f8c8d",
            wraplength=800,
            justify=tk.LEFT
        )
        self.result_label.pack(pady=15, padx=15)
    
    def bind_mouse_wheel(self, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.create_responsive_grid()

    def create_responsive_grid(self):
        for widget in self.grid_container.winfo_children():
            widget.grid_forget()

        width = self.root.winfo_width()
        if width < 100: width = 900 
        
        num_cols = max(1, width // 280)
        
        for i, feature in enumerate(self.feature_names):
            row = i // num_cols
            col = i % num_cols
            
            if feature not in self.input_fields:
                feature_frame = tk.Frame(self.grid_container, bg="white", relief=tk.RAISED, bd=1)
                
                description = self.descriptions.get(feature, feature)
                label = tk.Label(
                    feature_frame,
                    text=description,
                    font=("Arial", 9, "bold"),
                    bg="white",
                    fg="#2C3E50"
                )
                label.pack(padx=10, pady=(5, 0), anchor="center")
                
                scale = tk.Scale(
                    feature_frame,
                    from_=0,
                    to=10,
                    orient=tk.HORIZONTAL,
                    bg="white",
                    fg="#3498db",
                    length=220,
                    resolution=0.1,
                    command=lambda val, f=feature: self.update_entry(f, val)
                )
                scale.set(5.0)
                scale.pack(padx=10, pady=0, fill=tk.X)
                
                entry = tk.Entry(feature_frame, width=8, font=("Arial", 10), justify='center')
                entry.pack(padx=10, pady=(0, 5), anchor="center")
                entry.insert(0, "5.0")
                entry.bind('<KeyRelease>', lambda e, f=feature: self.update_scale(f))
                
                self.input_fields[feature] = {"scale": scale, "entry": entry, "frame": feature_frame}
            
            self.input_fields[feature]["frame"].grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        for c in range(num_cols):
            self.grid_container.grid_columnconfigure(c, weight=1)

    def update_entry(self, feature, value):
        entry = self.input_fields[feature]["entry"]
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

    def update_scale(self, feature):
        try:
            val = float(self.input_fields[feature]["entry"].get())
            if 0 <= val <= 10:
                self.input_fields[feature]["scale"].set(val)
        except ValueError:
            pass

    def predict(self):
        try:
            input_data = []
            for feature in self.feature_names:
                try:
                    value = float(self.input_fields[feature]["entry"].get())
                    if not (0 <= value <= 10):
                        messagebox.showwarning(
                            "Attention",
                            f"{feature} doit être entre 0 et 10"
                        )
                        return
                    input_data.append(value)
                except ValueError:
                    messagebox.showerror(
                        "Erreur",
                        f"Veuillez entrer une valeur numérique pour {feature}"
                    )
                    return
            
            X_input = np.array([input_data])
            
            X_input_scaled = self.scaler.transform(X_input)
            
            probability = self.model.predict(X_input_scaled)[0]
            
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
            elif hasattr(self.model, 'coef_'):
                importances = np.abs(self.model.coef_)
            else:
                importances = np.ones(len(self.feature_names))
                
            impact_scores = []
            for i, feat in enumerate(self.feature_names):
                score = X_input_scaled[0][i] * importances[i]
                impact_scores.append((feat, score))
            
            impact_scores.sort(key=lambda x: x[1], reverse=True)
            top_factors = impact_scores[:3] 
            
            self.display_result(probability, top_factors)
            
        except Exception as e:
            messagebox.showerror("Erreur de prédiction", str(e))
    
    def display_result(self, probability, top_factors):
        probability = max(0, min(1, probability))
        
        if probability < 0.3:
            risk_level = "FAIBLE"
            color = "#27ae60"
        elif probability < 0.6:
            risk_level = "MOYEN"
            color = "#f39c12"
        else:
            risk_level = "ELEVE"
            color = "#e74c3c"
        
        names_map = {
            "MonsoonIntensity": "Mousson excessive",
            "TopographyDrainage": "Défaut de drainage topographique",
            "RiverManagement": "Mauvaise gestion des cours d'eau",
            "Deforestation": "Déforestation massive",
            "Urbanization": "Urbanisation galopante",
            "ClimateChange": "Impact du changement climatique",
            "DamsQuality": "Fragilité structurelle des barrages",
            "Siltation": "Sédimentation des lits",
            "AgriculturalPractices": "Pratiques agricoles inadaptées",
            "Encroachments": "Empiétement sur les zones inondables",
            "IneffectiveDisasterPreparedness": "Préparation aux secours insuffisante",
            "DrainageSystems": "Réseaux de drainage obsolètes",
            "CoastalVulnerability": "Vulnérabilité des côtes",
            "Landslides": "Risques de glissements de terrain",
            "Watersheds": "Dégradation des bassins versants",
            "DeterioratingInfrastructure": "Infrastructures vieillissantes",
            "PopulationScore": "Forte densité de population exposée",
            "WetlandLoss": "Destruction des zones humides",
            "InadequatePlanning": "Défaut d'urbanisme préventif",
            "PoliticalFactors": "Instabilité des politiques de gestion"
        }
        
        top_str = "\n".join([f"  • {names_map.get(f, f)}" for f, s in top_factors])

        result_text = f"PROBABILITÉ D'INONDATION : {probability*100:.2f}%\n"
        result_text += f"NIVEAU DE RISQUE : {risk_level}\n\n"
        result_text += f"FACTEURS AGGRAVANTS MAJEURS :\n{top_str}\n\n"
        
        if probability < 0.3:
            result_text += "Recommandation : Risque faible. Vigilance habituelle."
        elif probability < 0.6:
            result_text += "Recommandation : Risque modéré. Prévoir des dispositifs d'évacuation."
        else:
            result_text += "Recommandation : RISQUE CRITIQUE ! Alerte maximale et évacuation immédiate."
        
        if not hasattr(self, 'result_text_area'):
            self.result_label.pack_forget()
            self.result_text_area = tk.Text(
                self.result_frame, 
                height=8, 
                font=("Arial", 11), 
                bg="white", 
                relief=tk.FLAT,
                padx=10,
                pady=10
            )
            res_scroll = tk.Scrollbar(self.result_frame, command=self.result_text_area.yview)
            res_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.result_text_area.configure(yscrollcommand=res_scroll.set)
            self.result_text_area.pack(fill=tk.BOTH, expand=True)

        self.result_text_area.configure(state=tk.NORMAL)
        self.result_text_area.delete('1.0', tk.END)
        self.result_text_area.insert(tk.END, result_text)
        
        self.result_text_area.tag_add("risk", "2.0", "2.end")
        self.result_text_area.tag_config("risk", foreground=color, font=("Arial", 11, "bold"))
        self.result_text_area.configure(state=tk.DISABLED)
    
    def reset_fields(self):
        for feature in self.feature_names:
            self.input_fields[feature]["scale"].set(5)
            self.input_fields[feature]["entry"].delete(0, tk.END)
            self.input_fields[feature]["entry"].insert(0, "5.0")
        
        if hasattr(self, 'result_text_area'):
            self.result_text_area.configure(state=tk.NORMAL)
            self.result_text_area.delete('1.0', tk.END)
            self.result_text_area.insert(tk.END, "3. Resultat: Entrez les parametres et cliquez sur 'Predire' pour obtenir le resultat")
            self.result_text_area.configure(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = FloodProbabilityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
