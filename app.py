import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# =======================
# Chargement des données
# =======================

df = pd.read_csv("supermarket_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%Y-%U")  # Semaine


# ============================
# Initialisation de l'application
# ============================

app = dash.Dash(__name__)
server = app.server  # test
app.title = "Tableau de bord des ventes"


# =======================
# Définition des couleurs
# =======================

COLOR_BG = "#2c3e50"
COLOR_HEADER = "#1b2838"
COLOR_CARD = "#34495e"
COLOR_TEXT = "#ecf0f1"
COLOR_ACCENT = "#1abc9c"
COLOR_GRAPH = "#e67e22"


# ============================
# Mise en page de l'application
# ============================

app.layout = html.Div(
    [
        # En-tête et filtres alignés horizontalement
        html.Div(
            [
                html.H1(
                    "Tableau de bord des ventes",
                    style={
                        "color": COLOR_TEXT,
                        "margin": "0",
                        "padding": "10px",
                        "fontSize": "34px",
                    },
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="city-filter",
                            options=[{"label": "Tout sélectionner", "value": "all"}]
                            + [
                                {"label": city, "value": city}
                                for city in df["City"].unique()
                            ],
                            placeholder="Sélectionner la ville",
                            multi=True,
                        )
                    ],
                    style={"width": "30%", "display": "inline-block", "padding": "5px"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="gender-filter",
                            options=[{"label": "Tout sélectionner", "value": "all"}]
                            + [
                                {"label": gender, "value": gender}
                                for gender in df["Gender"].unique()
                            ],
                            placeholder="Sélectionner le genre",
                            multi=True,
                        )
                    ],
                    style={"width": "30%", "display": "inline-block", "padding": "5px"},
                ),
                html.Span(
                    "?",
                    title="Projet de Python-Dash / M1 ECAP 2024-2025 / DAËRON Djayan / Enseignant :  SANE Abdoul Razac",
                    style={
                        "color": COLOR_TEXT,
                        "fontSize": "24px",
                        "cursor": "help",
                        "marginLeft": "20px",
                        "padding": "10px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "backgroundColor": COLOR_HEADER,
                "padding": "10px",
            },
        ),
        # Indicateurs
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            id="total-sales",
                            style={
                                "fontSize": "50px",
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "color": COLOR_ACCENT,
                                "margin": "25px 0",
                            },
                        ),
                        html.H3(
                            "Montant total des achats",
                            style={
                                "fontSize": "24px",
                                "textAlign": "center",
                                "color": COLOR_TEXT,
                            },
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "backgroundColor": COLOR_CARD,
                        "margin": "5px",
                    },
                ),
                html.Div(
                    [
                        html.P(
                            id="total-invoices",
                            style={
                                "fontSize": "50px",
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "color": COLOR_ACCENT,
                                "margin": "25px 0",
                            },
                        ),
                        html.H3(
                            "Nombre total d'achats (factures)",
                            style={
                                "fontSize": "24px",
                                "textAlign": "center",
                                "color": COLOR_TEXT,
                            },
                        ),
                    ],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "backgroundColor": COLOR_CARD,
                        "margin": "5px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "10px",
            },
        ),
        # Graphiques
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="hist-total-sales")],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "backgroundColor": COLOR_CARD,
                        "margin": "5px",
                    },
                ),
                html.Div(
                    [dcc.Graph(id="bar-total-invoices")],
                    style={
                        "width": "48%",
                        "display": "inline-block",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "backgroundColor": COLOR_CARD,
                        "margin": "5px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "marginBottom": "10px",
            },
        ),
        html.Div(
            [dcc.Graph(id="line-month-sales", style={"width": "100%"})],
            style={
                "width": "98%",
                "padding": "10px",
                "borderRadius": "10px",
                "backgroundColor": COLOR_CARD,
                "margin": "20px auto",
                "display": "flex",
                "justifyContent": "center",
            },
        ),
    ],
    style={"backgroundColor": "#1e3a5f", "minHeight": "100vh", "padding": "0px"},
)


# ============================
# Callbacks pour les mises à jour
# ============================

"""
    Update the dashboard figures and metrics based on selected filters for cities and genders.
    This callback function updates the following components:
    1. Total sales (formatted as a string with currency).
    2. Total number of unique invoices.
    3. Histogram of total sales distribution.
    4. Bar chart of total invoices.
    5. Line chart showing monthly sales trends.
    Parameters:
    -----------
    selected_cities : list of str
        List of selected cities. If empty or contains "all", all cities are considered.
    selected_genders : list of str
        List of selected genders. If empty or contains "all", all genders are considered.
    Returns:
    --------
    tuple
        A tuple containing:
        - total_sales (str): Total sales formatted as a string with currency (e.g., "1 234.56 USD").
        - total_invoices (str): Total number of unique invoices formatted as a string.
        - hist_fig (plotly.graph_objects.Figure): Histogram figure showing the distribution of total sales.
        - bar_fig (plotly.graph_objects.Figure): Bar chart figure showing the total number of invoices.
        - line_fig (plotly.graph_objects.Figure): Line chart figure showing the monthly sales trends.
    Notes:
    ------
    - If "all" is selected for both cities and genders, the histogram bars are displayed in a single color.
    - The bar chart and line chart adapt dynamically based on the selected filters.
    - The function uses predefined color maps for cities and genders to ensure consistent visualization.
    """

@app.callback(
    [
        Output("total-sales", "children"),
        Output("total-invoices", "children"),
        Output("hist-total-sales", "figure"),
        Output("bar-total-invoices", "figure"),
        Output("line-month-sales", "figure"),
    ],
    [Input("city-filter", "value"), Input("gender-filter", "value")],
)
def update_dashboard(selected_cities, selected_genders):
    # Gestion des villes : si vide, on considère toutes les villes
    if not selected_cities:
        filtered_cities = df["City"].unique().tolist()
        show_city_distinction = True
    elif "all" in selected_cities:
        filtered_cities = df["City"].unique().tolist()
        show_city_distinction = False
    else:
        filtered_cities = selected_cities
        show_city_distinction = True

    # Gestion des genres : si vide, on considère tous les genres
    if not selected_genders:
        filtered_genders = df["Gender"].unique().tolist()
        show_gender_distinction = True
    elif "all" in selected_genders:
        filtered_genders = df["Gender"].unique().tolist()
        show_gender_distinction = False
    else:
        filtered_genders = selected_genders
        show_gender_distinction = True

    filtered_df = df[
        (df["City"].isin(filtered_cities)) & (df["Gender"].isin(filtered_genders))
    ]

    # Calculs des indicateurs
    total_sales = f"{filtered_df['Total'].sum():,.2f}".replace(",", " ") + " USD"
    total_invoices = f"{filtered_df['Invoice ID'].nunique():,.0f}".replace(",", " ")

    # Déterminer si on doit colorer par Genre ou Ville
    color_var = None
    pattern_var = None

    if show_gender_distinction and show_city_distinction:
        color_var = "Gender"
        pattern_var = "City"
    elif show_city_distinction:
        pattern_var = "City"  # Toujours en pattern si distinction de ville
        color_var = None  # Pas de couleur si uniquement distinction par ville
    elif show_gender_distinction:
        color_var = "Gender"
        pattern_var = None  # Pas de pattern si uniquement distinction par genre

    # Titres dynamiques
    gender_translation = {"Male": "hommes", "Female": "femmes"}
    gender_title = ""
    if show_gender_distinction:
        translated_genders = [gender_translation.get(g, g) for g in selected_genders]
        if len(translated_genders) == 1:
            gender_title = f" pour les {translated_genders[0]}"
        else:
            gender_title = " par genre"

    city_title = ""
    if show_city_distinction:
        if len(selected_cities) == 1:
            city_title = f" à {selected_cities[0]}"
        else:
            city_title = " par ville"

    # Générer l'histogramme en fonction des filtres
    gender_color_map = {
        "Female": "#1abc9c",  # Vert
        "Male": "#3498db",  # Bleu
        "All": "#f1c40f",  # Jaune
    }

    city_color_map = {
        "Yangon": "#27ae60",  # Vert bien visible
        "Naypyitaw": "#2980b9",  # Bleu foncé
        "Mandalay": "#5dade2",  # Bleu clair, mais pas trop
        "Moyenne des villes sélectionnées": "#f1c40f",  # Jaune doré pour bien ressortir
        "Somme des 3 villes": "#000000",  # Noir pour un contraste maximal
    }

    # Création du graphique avec couleurs selon le genre et motifs selon la ville
    hist_fig = px.histogram(
        filtered_df,
        x="Total",
        color=(
            color_var if color_var else None
        ),  # Couleurs par genre si pas "Tout sélectionner"
        pattern_shape=(
            pattern_var if pattern_var else None
        ),  # Motifs par ville si activé
        title=f"Répartition des montants totaux des achats{gender_title}{city_title}",
        barmode="stack",
        color_discrete_map=gender_color_map,  # Utilisation des couleurs définies pour les genres
        labels={
            "Gender": "Genre",
            "City": "Ville",
            "Total": "Montant total des achats (USD)",
        },
    )

    hist_fig.update_layout(yaxis_title="Nombre d'achats (factures)")
    hist_fig.update_layout(legend_traceorder="reversed")

    # 1. Si "Tout sélectionner" est activé pour le genre ET pour la ville → tout devient jaune
    if "all" in selected_genders and "all" in selected_cities:
        hist_fig.update_traces(
            marker=dict(
                color=city_color_map["Moyenne des villes sélectionnées"],
                pattern_shape=None,  # Suppression des motifs
            )
        )

    # 2. Si "Tout sélectionner" est activé uniquement pour le genre → chaque barre a la couleur des villes
    elif "all" in selected_genders:
        hist_fig.for_each_trace(
            lambda trace: trace.update(
                marker=dict(
                    color=city_color_map.get(
                        trace.name, "#000000"
                    ),  # Appliquer la couleur de la ville
                    pattern_shape=None,  # Suppression des motifs
                )
            )
        )

    # 3. Si "Tout sélectionner" est activé uniquement pour la ville → couleurs du genre, mais sans motifs
    elif "all" in selected_cities:
        hist_fig.for_each_trace(
            lambda trace: trace.update(
                marker=dict(
                    color=gender_color_map.get(trace.name, "#000000"),
                    pattern_shape=None,  # Suppression des motifs
                )
            )
        )

    # Barre des achats totaux (Empilement : Sexe → Ville)
    # Reclasser pour que "Male" soit en bas et "Female" en haut

    # Vérification si "Tout sélectionner" est activé pour Genre
    if "all" in selected_genders:
        bar_fig = px.bar(
            filtered_df.groupby(["City"])["Invoice ID"].count().reset_index(),
            x="City",
            y="Invoice ID",
            color="City",
            title=f"Nombre total d'achats (factures) {city_title}",
            barmode="stack",
            labels={"Invoice ID": "Nombre d'achats (factures)", "City": "Ville"},
            color_discrete_map=city_color_map,  # Utilisation des couleurs des villes
        )
    else:

        if show_city_distinction and show_gender_distinction:
            bar_fig = px.bar(
                filtered_df.groupby(["City", "Gender"])["Invoice ID"]
                .count()
                .reset_index(),
                x="City",
                y="Invoice ID",
                color="Gender",
                title=f"Nombre total d'achats (factures){gender_title}{city_title}",
                barmode="stack",
                labels={
                    "Invoice ID": "Nombre d'achats (factures)",
                    "City": "Ville",
                    "Gender": "Genre",
                },
                color_discrete_map=gender_color_map,  # Utilisation des couleurs des genres
            )
        elif show_city_distinction:
            bar_fig = px.bar(
                filtered_df.groupby(["City"])["Invoice ID"].count().reset_index(),
                x="City",
                y="Invoice ID",
                color="City",
                title=f"Nombre total d'achats (factures) {city_title}",
                barmode="stack",
                labels={"Invoice ID": "Nombre d'achats (factures)", "City": "Ville"},
                color_discrete_map=city_color_map,  # Utilisation des couleurs des villes
            )
        elif show_gender_distinction:
            bar_fig = px.bar(
                filtered_df.groupby(["City", "Gender"])["Invoice ID"]
                .count()
                .reset_index(),
                x="City",
                y="Invoice ID",
                color="Gender",
                title=f"Nombre total d'achats (factures){gender_title}",
                barmode="stack",
                labels={
                    "Invoice ID": "Nombre d'achats (factures)",
                    "City": "Ville",
                    "Gender": "Genre",
                },
                color_discrete_map=gender_color_map,  # Utilisation des couleurs des genres
            )
        else:
            bar_fig = px.bar(
                filtered_df.groupby("City")["Invoice ID"].count().reset_index(),
                x="City",
                y="Invoice ID",
                title="Nombre total d'achats (factures)",
                labels={"Invoice ID": "Nombre d'achats (factures)", "City": "Ville"},
                color_discrete_map=city_color_map,  # Utilisation des couleurs des villes par défaut
            )

    # Réorganiser la légende pour que "Male" soit en bas et "Female" en haut
    bar_fig.update_layout(legend_traceorder="reversed")

    # Graphique de l'évolution des achats par mois)
    # Définition des couleurs avec plus de contraste

    # Regrouper par mois et ville
    month_sales = filtered_df.groupby(["Month", "City"])["Total"].sum().reset_index()

    # Vérifier si "Tout sélectionner" est activé
    if "all" in selected_cities:
        # Afficher uniquement la somme des 3 villes
        month_sum = month_sales.groupby("Month")["Total"].sum().reset_index()
        month_sum["City"] = "Somme des 3 villes"
        month_sales = month_sum
    else:
        num_selected_cities = len(filtered_cities)

        # Ajouter la moyenne des villes sélectionnées si au moins 2 villes sont sélectionnées
        if num_selected_cities > 1:
            month_avg = month_sales.groupby("Month")["Total"].mean().reset_index()
            month_avg["City"] = "Moyenne des villes sélectionnées"
            month_sales = pd.concat([month_sales, month_avg])

    # Création du graphique avec des couleurs contrastées et des lignes épaisses
    line_fig = px.line(
        month_sales,
        x="Month",
        y="Total",
        color="City",
        title=f"Évolution des achats par mois{city_title}",
        color_discrete_map=city_color_map,
        labels={
            "Month": "Temps (Mois-Année)",
            "Total": "Montant total des achats (USD)",
            "City": "Ville",
        },
        line_shape="linear",
    )

    # Rendre les lignes plus épaisses et visibles
    line_fig.update_traces(line=dict(width=5))

    return total_sales, total_invoices, hist_fig, bar_fig, line_fig


# Gestion du filtre "Tout sélectionner" (exclusif)
@app.callback(
    Output("city-filter", "value"),
    Input("city-filter", "value"),
)
def update_city_filter(selected_cities):
    if not selected_cities:
        return []  # Affiche "Sélectionner ..." mais prend toutes les villes

    if "all" in selected_cities and len(selected_cities) > 1:
        return ["all"]  # Si "Tout sélectionner" est activé, il reste seul

    return selected_cities


@app.callback(
    Output("gender-filter", "value"),
    Input("gender-filter", "value"),
)
def update_gender_filter(selected_genders):
    if not selected_genders:
        return []  # Affiche "Sélectionner ..." mais prend tous les genres

    if "all" in selected_genders and len(selected_genders) > 1:
        return ["all"]  # Si "Tout sélectionner" est activé, il reste seul

    return selected_genders


# ============================
# Lancement de l'application
# ============================

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)
