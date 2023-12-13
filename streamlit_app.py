import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Titel
st.title('ABC-Analyse')

# Diagramm für die Klassenverteilung
def plot_class_distribution(data):
    fig = px.bar(data, x='Class', y='Count', color='Class',
                 title='Verteilung der ABC-Klassen')
    st.plotly_chart(fig)


# Diagramm für die Gesamteinnahmen pro Kategorie
def plot_total_earnings(data):
    fig = px.bar(data, x=data.index, y='Total_2022',
                 title='Gesamteinnahmen pro Kategorie')
    st.plotly_chart(fig)

# Erstellen des Pareto-Diagramms
def plot_pareto_chart(data):
    fig = go.Figure()

    # Hinzufügen des Balkendiagramms für die kumulativen Prozentwerte
    fig.add_trace(go.Bar(
        x=data.index, 
        y=data['Cumulative_Percentage'],
        text=data['Class'],  # Dies zeigt die Klasse jeder Kategorie an
        marker_color=data['Class'].map({'A': 'green', 'B': 'blue', 'C': 'red'}),  # Farben nach Klasse
        name='Kumulativer Anteil'
    ))

    # Hinzufügen der horizontalen Linien für die Klassengrenzen
    fig.add_hline(y=80, line_dash="dot",
                  annotation_text="Klasse A bis 80%)", 
                  annotation_position="bottom left")

    fig.add_hline(y=95, line_dash="dot",
                  annotation_text="Klasse B bis 95%", 
                  annotation_position="bottom left")

    fig.add_hline(y=100, line_dash="dot",
                  annotation_text="Klasse C bis 100%", 
                  annotation_position="top left")

    # Layout-Einstellungen
    fig.update_layout(
        title='Pareto-Diagramm: Kumulativer Anteil pro Kategorie',
        xaxis=dict(title='Kategorien', tickangle=-45),
        yaxis=dict(title='Kumulativer Anteil in Prozent', ticksuffix="%"),
        showlegend=False,
        hovermode="x unified"
    )

    # Anzeigen des Diagramms in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Erstellen des Pareto-Diagramms
def plot_pareto_chart2(data):
    fig = go.Figure()

    # Hinzufügen des Balkendiagramms für die kumulativen Prozentwerte
    fig.add_trace(go.Bar(
        x=data["parent_name"], 
        y=data['Cumulative_Percentage'],
        text=data['Class'],  # Dies zeigt die Klasse jeder Kategorie an
        marker_color=data['Class'].map({'A': 'green', 'B': 'blue', 'C': 'red'}),  # Farben nach Klasse
        name='Kumulativer Anteil'
    ))

    # Hinzufügen der horizontalen Linien für die Klassengrenzen
    fig.add_hline(y=80, line_dash="dot",
                  annotation_text="Klasse A bis 80%)", 
                  annotation_position="bottom left")

    fig.add_hline(y=95, line_dash="dot",
                  annotation_text="Klasse B bis 95%", 
                  annotation_position="bottom left")

    fig.add_hline(y=100, line_dash="dot",
                  annotation_text="Klasse C bis 100%", 
                  annotation_position="top left")

    # Layout-Einstellungen
    fig.update_layout(
        title='Pareto-Diagramm: Kumulativer Anteil pro Inventar',
        xaxis=dict(title='Kategorien', tickangle=-45),
        yaxis=dict(title='Kumulativer Anteil in Prozent', ticksuffix="%"),
        showlegend=False,
        hovermode="x unified"
    )

    # Anzeigen des Diagramms in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Erstellen eines Balkendiagramms mit Plotly
def plot_inventory_class_distribution(data):
    fig = px.bar(data, barmode='stack',
                 labels={'value': 'Anzahl der Kategorien', 'parent_name': 'Inventarbereich'},
                 title='Verteilung der ABC-Klassen in den Inventarbereichen')
    st.plotly_chart(fig)

# Erstellen des Plotly Diagramms
def plot_monthly_earnings(data):
    fig = px.bar(data, x='Monat', y='Gesamteinnahmen', color='parent_name',
                 title='Monatliche Einnahmen 2022 pro Inventarbereich',
                 labels={'Gesamteinnahmen': 'Einnahmen', 'parent_name': 'Inventarbereich'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

def plot_annual_earnings_pie_chart(data):
    fig = px.pie(data, names='Inventarbereich', values='Gesamteinnahmen',
                 title='Jahresgesamteinnahmen pro Inventarbereich')
    st.plotly_chart(fig)

def plot_monthly_growth_streamlit(monthly_growth_melted):
    # Erstellen eines Liniendiagramms mit Plotly Express
    fig = px.line(monthly_growth_melted, x='Monat', y='Wachstumsrate', color='parent_name', markers=True,
                  title='Monatliches Wachstum der Inventarbereiche')

    # Anzeigen des Diagramms in Streamlit
    st.plotly_chart(fig)

def classify_monthly(data, earning_columns):
    monthly_classification = pd.DataFrame()

    for month in earning_columns:
        # Monatliche Einnahmen und kumulative Prozentsätze berechnen
        monthly_earnings = data.groupby('name')[month].sum()
        total_earnings = monthly_earnings.sum()
        monthly_earnings = monthly_earnings.sort_values(ascending=False)
        cumulative_percentage = monthly_earnings.cumsum() / total_earnings

        # Klassifizierung in A, B, C
        classification = pd.cut(cumulative_percentage, bins=[0, 0.8, 0.95, 1], labels=['A', 'B', 'C'], right=False)
        monthly_classification[month] = classification

    return monthly_classification

def count_class_changes(classification):
    changes = classification.apply(lambda row: (row != row.shift()).cumsum(), axis=1)
    change_counts = changes.apply(lambda row: len(row.unique()) - 1, axis=1)
    return change_counts


def plot_top_10_changes(top_10):
    fig = px.bar(top_10, x=top_10.index, y=top_10.values, labels={'y': 'Anzahl der Klassenwechsel', 'index': 'Kategorie'},
                 title='Top 10 Kategorien mit den häufigsten Klassenwechseln')
    st.plotly_chart(fig)
# ----------------------------------------------------------------------------------------------------------------------------------

# Datei-Upload-Widgets
uploaded_file_categories = st.file_uploader("categories.csv hochladen", type=["csv"])
uploaded_file_earnings = st.file_uploader("earnings.csv hochladen", type=["csv"])

# Überprüfen, ob beide Dateien hochgeladen wurden
if uploaded_file_categories is not None and uploaded_file_earnings is not None:
    
    # Laden der Daten in DataFrames
    csv1 = pd.read_csv(uploaded_file_categories)
    csv2 = pd.read_csv(uploaded_file_earnings)

    # Ausgabe der einzelnen CSV als df in streamlit
    #st.write("Categories:")
    #st.dataframe(csv1)

    #st.write("Earnings:")
    #st.dataframe(csv2)

    # Mergen der beiden DataFrames
    merged_data = pd.merge(csv2, csv1, how='left', left_on='category_id', right_on='id')

    # Anzeigen der gemergten Daten
    st.write("Left-merge anhand der category_id (product_earnings.csv) und der id (categories.csv)")
    st.write("Merged Data:")
    st.dataframe(merged_data)

    st.subheader("Bestimme sinnvolle Bucketgrößen und weise den Kategorien Klassen zu")

    # Aggregieren der monatlichen Einnahmen pro Kategorie
    category_earnings = merged_data.groupby('name').sum() # name ist name der kategorie

    # Berechnen der Gesamteinnahmen pro Kategorie für das Jahr 2022
    earning_columns = ['Januar 2022', 'Februar 2022', 'März 2022', 'April 2022', 'Mai 2022', 'Juni 2022', 'Juli 2022', 'August 2022', 'September 2022', 'Oktober 2022', 'November 2022', 'Dezember 2022']
    category_earnings = merged_data.groupby('name')[earning_columns].sum()

    category_earnings['Total_2022'] = category_earnings.sum(axis=1)
    # Sortieren der Kategorien nach Gesamteinnahmen
    sorted_categories = category_earnings.sort_values(by='Total_2022', ascending=False)
    
    print(sorted_categories[['Total_2022']])


    # Plotten der Verteilung der Gesamteinnahmen
    plot_total_earnings(sorted_categories)

    # Berechnen der kumulativen Prozentanteile

    sorted_categories['Cumulative_Percentage'] = 100 * (sorted_categories['Total_2022'].cumsum() / sorted_categories['Total_2022'].sum())

    # Zuweisung der Kategorien zu den Buckets A, B, C
    # bucketgröße: A: 80%, B: 95%, C: 100% (in die jeweiligen Klassen fallen alle Kategorien, die zwischen diese Werte fallen -> in A sind alle Kategorien, die 60% des Umsatzes ausmachen)
    sorted_categories['Class'] = 'C'  # default alle als C einstufen
    sorted_categories.loc[sorted_categories['Cumulative_Percentage'] < 95, 'Class'] = 'B'
    sorted_categories.loc[sorted_categories['Cumulative_Percentage'] < 80, 'Class'] = 'A'

    # Sortieren der Kategorien nach kumulativem Prozentsatz für die Darstellung
    sorted_categories = sorted_categories.sort_values(by='Cumulative_Percentage')

    print(sorted_categories[['Total_2022', 'Cumulative_Percentage', 'Class']])

       # --------------- nach inventar ------------
    # Umwandlung in einen DataFrame für die weitere Verarbeitung
    # Aggregieren der Gesamteinnahmen pro Inventarbereich für das Jahr 2022
    total_earnings_by_inventory = merged_data.groupby('parent_name')[earning_columns].sum().sum(axis=1)

    sorted_inventories = total_earnings_by_inventory.reset_index()
    sorted_inventories.columns = ['parent_name', 'Total_2022']
    print(sorted_inventories.head())

    # Berechnen der kumulativen Prozentsätze
    total_earnings = sorted_inventories['Total_2022'].sum()
    sorted_inventories['Cumulative_Percentage'] = 100 * sorted_inventories['Total_2022'].cumsum() / total_earnings

    # Einteilung in ABC-Klassen
    sorted_inventories['Class'] = 'C'
    sorted_inventories.loc[sorted_inventories['Cumulative_Percentage'] < 95, 'Class'] = 'B'
    sorted_inventories.loc[sorted_inventories['Cumulative_Percentage'] < 80, 'Class'] = 'A'

    # Sortieren der Inventarbereiche nach kumulativem Prozentsatz
    sorted_inventories = sorted_inventories.sort_values(by='Cumulative_Percentage')
    print(sorted_inventories.head())

    st.write("Nach dem Pareto-Prinzip generieren 20% des Sortiments 80% der Einnahmen. Aufgrund dessen werden die Klassengrenzen für die kumulierten Prozenanteile des Umsatzes für A bei 80%, für B bei 95% und der Rest in C eingeteilt.")


    ################ Aufgabe 2
    st.subheader("Welche Verteilung der Klassen zeigt sich über den gesamten Katalog bzw. in den unterschiedlichen Inventarbereichen?")
    
    # Vorbereiten der Daten für die Visualisierung
    class_distribution = sorted_categories['Class'].value_counts().reset_index()
    class_distribution.columns = ['Class', 'Count']

    # Aggregieren der Gesamteinnahmen pro Klasse
    class_earnings = sorted_categories.groupby('Class')['Total_2022'].sum().reindex(['A', 'B', 'C'])

    cumulative_percentage = class_earnings.cumsum() / class_earnings.sum() * 100
    cumulative_percentage = cumulative_percentage.reset_index()
    cumulative_percentage.columns = ['Class', 'Cumulative_Percentage']

    plot_class_distribution(class_distribution)
    
    # Berechnen der Anzahl der Kategorien pro Klasse
    class_counts = sorted_categories['Class'].value_counts()

    # Zuweisung der Anzahlen zu Variablen
    count_class_a = class_counts.get('A', 0) # Falls keine Kategorie in Klasse A, setze 0
    count_class_b = class_counts.get('B', 0) 
    count_class_c = class_counts.get('C', 0) 

    # Gesamtanzahl der Kategorien
    total_categories = len(sorted_categories)

    # Prozentualen Anteil jeder Klasse berechnen
    percentage_class_a = (count_class_a / total_categories) * 100 if total_categories > 0 else 0
    percentage_class_b = (count_class_b / total_categories) * 100 if total_categories > 0 else 0
    percentage_class_c = (count_class_c / total_categories) * 100 if total_categories > 0 else 0

    st.write(f"Bei einer Gesamtzahl von {total_categories} Kategorien, ergeben sich für jede Klasse folgende Anteile:")
    st.write(f"Anzahl der Kategorien in Klasse A: {count_class_a} / {percentage_class_a:.2f}%")
    st.write(f"Anzahl der Kategorien in Klasse B: {count_class_b} / {percentage_class_b:.2f}%")
    st.write(f"Anzahl der Kategorien in Klasse C: {count_class_c} / {percentage_class_c:.2f}%")

    plot_pareto_chart(sorted_categories)
    st.write(f"Nach dem oben genannten Pareto-Prinzip sollten etwa 20% zu 80% der Einnahmen beitragen. Die Lorenzkurve zeigt, dass die Einnahmen eher gleichverteilt sind. Insgesamt tragen {percentage_class_a:.2f}% der Kategorien zu 80% der Einnahmen bei (Klasse A).")

    plot_pareto_chart2(sorted_inventories)
    st.write("Auch eine Einteilung nach Inventar zeigt, dass das Pareto-Prinzip nicht zutrifft.")
    # Zusammenführen der klassifizierten Daten mit den Inventarbereichen
    full_data = pd.merge(sorted_categories, csv1, left_index=True, right_on='name', how='left')
    
    # Gruppieren nach Inventarbereich und Klasse
    inventory_class_distribution = full_data.groupby(['parent_name', 'Class']).size().unstack().fillna(0) # enthält die anzahl der kategorien pro klasse der inventarbereiche
    print(inventory_class_distribution.head())

    # Gruppieren nach Inventarbereich und Klasse
    plot_inventory_class_distribution(inventory_class_distribution)
    st.write("Es ist zu sehen, dass Klasse A immer den größten Teil aller Inventarbereiche einnimmt.")
    ############## Aufgabe 3

    st.subheader("Welche saisonalen Schwerpunkte würdest Du Content Management empfehlen?")
    
    # Aggregieren der monatlichen Einnahmen pro Inventarbereich
    monthly_earnings_by_inventory = merged_data.groupby('parent_name')[earning_columns].sum()
    print(monthly_earnings_by_inventory.head())
    # Umwandeln der Daten in ein für Plotly geeignetes Format
    monthly_earnings_melted = monthly_earnings_by_inventory.reset_index().melt(id_vars='parent_name', var_name='Monat', value_name='Gesamteinnahmen')

    plot_monthly_earnings(monthly_earnings_melted)
    
    st.write("Man sieht, dass vor die monatlichen Einnahmen mit Jahresverlauf zunehmen.")

    # Aggregieren der Jahresgesamteinnahmen pro Inventarbereich
    annual_earnings_by_inventory = merged_data.groupby('parent_name')[earning_columns].sum().sum(axis=1).reset_index()
    annual_earnings_by_inventory.columns = ['Inventarbereich', 'Gesamteinnahmen']

    # Sortieren der Inventarbereiche absteigend nach Gesamteinnahmen
    sorted_annual_earnings = annual_earnings_by_inventory.sort_values(by='Gesamteinnahmen', ascending=False)

    # Visualisierung der Jahresgesamteinnahmen pro Inventarbereich als Tortendiagramm
    plot_annual_earnings_pie_chart(sorted_annual_earnings)

    st.write("Inventarbereiche absteigend nach Gesamteinnahmen:")
    st.write(sorted_annual_earnings[['Inventarbereich', 'Gesamteinnahmen']])

    # Sortieren der Spalten basierend auf dem Datum, um sicherzustellen, dass die Reihenfolge korrekt ist
    #monthly_earnings_by_inventory = monthly_earnings_by_inventory.reindex(sorted(monthly_earnings_by_inventory.columns), axis=1)

    # Berechnung des monatlichen Wachstums pro Inventarbereich
    monthly_growth = monthly_earnings_by_inventory.pct_change(axis=1)

    # Zurücksetzen des Index, um 'parent_name' als normale Spalte zu haben
    monthly_growth = monthly_growth.reset_index()
    print(monthly_growth)
    # Transformieren der Daten für die Visualisierung
    monthly_growth_melted = monthly_growth.melt(id_vars='parent_name', var_name='Monat', value_name='Wachstumsrate')

    plot_monthly_growth_streamlit(monthly_growth_melted)
    st.write("Von Februar auf März findet eine über 70% Erhöhung der Einnahmen je Inventarbereich statt. Solange die Wachstumsrate im positiven Bereich ist, wächst der Umsatz. Fällt die Wachstumsrate in den negativen Bereich, verringerte sicher der Umsatz im Vergleich zum Vormonat.")
    st.write("""
    Von September auf Oktober ist beispielsweise zu sehen, dass die Einnahmen in allen Bereichen, außer der für **Baby&Kind** steigen.
    Generell könnte man versuchen die Wachstumsrate positiv zu halten. Speziell für das Beispiel des Inventares **Baby&Kind** kann man Marketing Strategien entwickeln, um einen Rückgang des Umsatzes zu vermeiden.
    """)
    st.subheader("Kann man darstellen, welche Kategorien in Zukunft voraussichtlich in eine andere Klasse wechseln?")
    monthly_classification = classify_monthly(merged_data, earning_columns)
    st.write("Die Kategorien aus dem **merged_data**-Dataframe wird auf monatlicher Basis in die Klassen A,B,C eingeteilt. Anschließend werden die Wechsel der Klassen gezählt.")
    st.write("Monatliche Klasseneinteilung jeder Kategorie:")
    st.dataframe(monthly_classification)
    class_change_counts = count_class_changes(monthly_classification)
    top_10_changes = class_change_counts.sort_values(ascending=False).head(10)
    st.write("Dargestellt sind die 10 Kategorien mit den meisten Klassenwechseln im Jahr 2022. Diese Anzahl der Wechsel aller Kategorien könnte man nutzen, um zukünftige Kategoriewechsel vorherzusagen. Beispielsweise könnte man mit historischen Daten vergleichen, an welchen Monaten ein Klassenwechsel einer bestimmten Kategorie stattfindet und ein Muster zu beobachten ist.")

    plot_top_10_changes(top_10_changes)
    st.subheader("Was sind die Vor- und Nachteile der ABC-Analyse für diese Fragestellung? Würdest Du einen anderen Ansatz bevorzugen und warum?")

    # Vorzüge der ABC-Analyse
    st.write("""
    Vorteile:

    - **Effizienzsteigerung**: Sie hilft dabei, sich auf die wichtigsten Artikel zu konzentrieren, anhand der man entsprechende Maßnahmen vornehmen kann.
    - **Priorisierung**: Sie ermöglicht eine Priorisierung der Produkte basierend auf den Beitrag zum Gesamtumsatz.
    """)

    # Nachteile der ABC-Analyse
    st.write("""
    Nachteile:

    - **Gleichverteilung der Umsätze**: Wenn alle Produkte ähnlich zum Gesamtumsatz beitragen, bietet die ABC-Analyse wenig Einblick, da keine klare Trennung nach ihrer Wichtigkeit besteht.
   """)

    st.write("Für die gegeben Daten hat sich die ABC-Analyse allerdings für unpassend erwiesen, da die Einnahmesumme aller Produkte in etwa gleich ist. Es gibt also keine Produkte die hauptsächlich zum Umsatz beitragen.")

    # Alternative Ansätze
    st.subheader("Alternative Ansätze")

    st.write("""
    Hier wurde ChatGPT zur Hilfe genommen, um andere Möglichkeiten Analysemöglichkeiten zu finden.
    Das sind die Vorschläge:
             
Wenn die ABC-Analyse gleichverteilte Umsätze ergibt, was bedeutet, dass alle Artikel annähernd gleich wichtig sind, könnte es sinnvoll sein, alternative Analysemethoden in Betracht zu ziehen, die unterschiedliche Aspekte des Inventars oder der Verkaufsdaten hervorheben. Hier sind einige Methoden, die in einem solchen Szenario nützlich sein könnten:

1. **XYZ-Analyse**: Diese Methode fokussiert sich auf die Vorhersagbarkeit des Verbrauchs der Artikel. Artikel werden in X, Y und Z Kategorien eingeteilt, wobei X für konstante, Y für schwankende und Z für unregelmäßige Nachfragemuster steht.

2. **FMEA (Failure Mode and Effects Analysis)**: Diese Methode eignet sich zur Identifikation von Risikofaktoren in Prozessen. Sie kann hilfreich sein, um zu verstehen, welche Artikel aufgrund potenzieller Ausfälle oder Fehler kritisch sein könnten.

3. **Kundenwertanalyse (Customer Value Analysis, CVA)**: Hierbei wird der Fokus auf die Kunden und deren Wertigkeit gelegt. Diese Analyse kann aufdecken, welche Produkte für bestimmte Kundensegmente am wertvollsten sind.

4. **RFM-Analyse (Recency, Frequency, Monetary)**: Diese Methode betrachtet, wie kürzlich und wie oft ein Kunde gekauft hat, sowie den Geldwert der Käufe. Sie könnte nützlich sein, um zu verstehen, welche Produkte regelmäßig nachgefragt werden.

5. **Pareto-Analyse**: Obwohl ähnlich zur ABC-Analyse, könnte eine detailliertere Pareto-Analyse helfen, feinere Unterschiede in der Wichtigkeit der Artikel zu identifizieren.

6. **Multivariate Analysemethoden**: Techniken wie Clusteranalyse oder Hauptkomponentenanalyse können genutzt werden, um Muster und Beziehungen zwischen verschiedenen Produkten oder Verkaufsdaten zu identifizieren.

7. **Prozesskostenrechnung (Activity-Based Costing, ABC)**: Diese Methode konzentriert sich darauf, die tatsächlichen Kosten der Produktbereitstellung zu verstehen, was helfen kann, Prioritäten in Bezug auf Effizienz und Profitabilität zu setzen.

Die Auswahl der geeigneten Methode hängt von den spezifischen Zielen und dem Kontext Ihres Unternehmens ab. Es ist oft hilfreich, mehrere dieser Methoden zu kombinieren, um ein umfassendes Bild der Situation zu erhalten.
    """)

    st.write("ChatGPT wurde verwendet, um Plots mit der Library Plotly umzusetzen und um die letzte Teilaufgabe der Challenge zu lösen. Es wurden keine Daten hochgeladen, sondern lediglich die Spaltentypen angegeben!")
else:
    st.write("Bitte lade beide CSV-Dateien hoch, um fortzufahren.")
