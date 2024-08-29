from flask import Flask, request, render_template_string
import pandas as pd
import joblib

app = Flask(__name__)

# Load the saved ensemble model
model_path = r'C:/Users/Innovex/Documents/house_price_prediction/tuned_model_outputs/ensemble_model.pkl'
ensemble_model = joblib.load(model_path)

# Load the preprocessor object
preprocessor_path = r'C:/Users/Innovex/Documents/house_price_prediction/model_preprocessor/preprocessor.pkl'
preprocessor = joblib.load(preprocessor_path)

def preprocess_and_predict(bedrooms, bathrooms, property_type, purchase_type, new_sub_county):
    total_rooms = bedrooms + bathrooms + 2

    data = {
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'property_type': [property_type],
        'purchase_type': [purchase_type],
        'new_sub_county': [new_sub_county],
        'total_rooms': [total_rooms]
    }
    df = pd.DataFrame(data)
    df_prepared = preprocessor.transform(df)
    prediction = ensemble_model.predict(df_prepared)[0]
    return prediction

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    if request.method == 'POST':
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        property_type = request.form['property_type']
        purchase_type = request.form['purchase_type']
        new_sub_county = request.form['new_sub_county']

        prediction = preprocess_and_predict(bedrooms, bathrooms, property_type, purchase_type, new_sub_county)
        prediction = round(prediction, 2)

        if purchase_type.lower() == 'rent':
            prediction_text = f"Predicted Monthly Rent (Ksh): {prediction:.2f} (per month)"
        else:
            prediction_text = f"Predicted Price (Ksh): {prediction:.2f}"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Nairobi Property Price Prediction</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #e0f7fa;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                max-width: 750px;
                width: 100%;
            }
            h1 {
                text-align: center;
                font-weight: 600;
                color: #00796b;
            }
            label {
                margin: 10px 0 5px;
                display: block;
                font-weight: 500;
            }
            input[type="text"], select {
                width: 100%;
                padding: 12px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 16px;
            }
            button {
                width: 100%;
                padding: 15px;
                background-color: #00796b;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #004d40;
            }
            .prediction-box {
                background-color: #b2dfdb;
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
                font-size: 20px;
                color: #004d40;
                font-weight: 600;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #b2ebf2;
                font-weight: 500;
            }
            tr:nth-child(even) {
                background-color: #f1f8e9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Nairobi County Property Price Prediction Model</h1>
            <form method="post">
                <label for="bedrooms">Integer field</label>
                <input type="text" name="bedrooms" placeholder="Number of Bedrooms" required />

                <label for="bathrooms">Integer field</label>
                <input type="text" name="bathrooms" placeholder="Number of Bathrooms" required />

                <label for="property_type">Property Type</label>
                <select name="property_type" required>
                    <option value="House">House</option>
                    <option value="Apartment">Apartment</option>
                </select>

                <label for="purchase_type">Purchase Type</label>
                <select name="purchase_type" required>
                    <option value="Sale">Sale</option>
                    <option value="Rent">Rent</option>
                </select>

                <label for="new_sub_county">Location</label>
                <select name="new_sub_county" required>
                    <option value="Dagoretti North">Dagoretti North</option>
                    <option value="Westlands & Starehe">Westlands & Starehe</option>
                    <option value="Embakasi Areas">Embakasi Areas</option>
                    <option value="Langata & Kibra">Langata & Kibra</option>
                </select>

                <button type="submit">Predict</button>
            </form>
            {% if prediction_text %}
            <div class="prediction-box">{{ prediction_text }}</div>
            {% endif %}
            <h2>Sublocations</h2>
            <table>
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Sublocations</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Dagoretti North</td>
                        <td>Kilimani, Kawangware, Gatina, Kileleshwa, Kabiro, Dagoretti North, Dagoretti Corner, Lavington, Valley Arcade, Riruta, Naivasaha Road, Riaira, Riara Road, Mutu-Ini, Ngando, Riruta, Uthiru, Ruthimitu, Waithaka, Dagoretti South, Kikuyu Town, Kikuyu</td>
                    </tr>
                    <tr>
                        <td>Westlands & Starehe</td>
                        <td>Kitisuru, Parklands, Highridge, Karura, Kangemi, Mountain View, Muthaiga, Westlands, Limuru, Redhill, Kiambu Road, Ruaka, Banana, Parkland, Hurlingham, Upper Hill, Brookside, Kyuna, Museum Hill, Muthangari, Nyari, Tigoni, Lower Kabete, Gigiri, Runda, Loresho, Rosslyn, Riverside, Thigiri, Pangani, Ziwani, Kariokor, Landimawe, Nairobi South, Hospital, Starehe</td>
                    </tr>
                    <tr>
                        <td>Embakasi Areas</td>
                        <td>Githurai, Kahawa West, Zimmerman, Roysambu, Kahawa Sukari, Kahawa Wendani, Ruiru, Ngecha, Juja, Kenyatta Road, Thika, Ridgeways, Mirema Drive, Garden Estate, Mirema, Tatu City, Umoja I, Umoja One, Umoja 1, Umoja II, Umoja Two, Umoja 2, Umoja, Mowelm, Kariobangi South, Maringo, Hamza, Embakasi West, Donholm, Upper Savannah, Lower Savannah, Savannah, Embakasi, Utawala, Mihango, Embakasi East, Kamulu, Joska, Malaa, Kariobangi North, Dandora, Embakasi North, Imara Daima, Kwa Njenga, Kwa Reuben, Pipeline, Kware, Embakasi South, Kitengela, Syokimau, Mlolongo, Athi River, Mombasa Road, Mombasa Rd, Fedha, Kayole, Kayole North, Kayole South, Kayole Central, Komarock, Matopeni, Spring Valley, Embakasi Central, Clay City, Mwiki, Kasarani, Njiru, Ruai, Saika, Thika Road, Chokaa, Thome, Peponi, Garden City, Thindigua, Viwandani, Harambee, Makongeni, Pumwani, Eastleigh North, Makadara, Buruburu, Jogoo Road, Industrial Area, Eastleigh South, Airbase, California, Ngara, Nairobi Central, Kamukunji, Mabatini, Huruma, Ngei, Mlango Kubwa, Kiamaiko, Mathare, Baba Dogo, Utalii, Matahare North, Lucky Summer, Korogocho, Ruaraka</td>
                    </tr>
                    <tr>
                        <td>Langata & Kibra</td>
                        <td>Karen, Nairobi West, Mugumu-Ini, South C, Nyayo Highrise, Nyayo, Ngong, Langata, Ongata Rongai, Rongai, Madaraka, Kiserain, South B, Bomas of Kenya, Golden Estate, Laini Saba, Lindi Makina, Woodley, Kenyatta Golf Course, Sarangombe, Kibra, Jamhuri, Ngumo</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    ''', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
