from flask import Flask, request, render_template_string
import pandas as pd
import joblib

app = Flask(__name__)

# Load the saved ensemble model
model_path = r'C:/Users/Innovex/Documents/house_price_prediction/tuned_model_outputs/ensemble_model.pkl'  # path to your saved model
ensemble_model = joblib.load(model_path)

# Load the preprocessor object
preprocessor_path = r'C:/Users/Innovex/Documents/house_price_prediction/model_preprocessor/preprocessor.pkl'  # path to your saved preprocessor
preprocessor = joblib.load(preprocessor_path)  # Load the preprocessor

def preprocess_and_predict(bedrooms, bathrooms, property_type, purchase_type, new_sub_county):
    # Calculate total_rooms
    total_rooms = bedrooms + bathrooms + 2

    # Prepare input data as DataFrame
    data = {
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'property_type': [property_type],
        'purchase_type': [purchase_type],
        'new_sub_county': [new_sub_county],
        'total_rooms': [total_rooms]
    }
    df = pd.DataFrame(data)

    # Apply preprocessor transformations
    df_prepared = preprocessor.transform(df)

    # Predict using the model
    prediction = ensemble_model.predict(df_prepared)[0]

    return prediction

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Predict Cost of Property</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f4f7f6;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                max-width: 700px;
                width: 100%;
            }
            h1 {
                text-align: center;
                font-weight: 500;
            }
            label {
                margin: 10px 0 5px;
                display: block;
                font-weight: 500;
            }
            input[type="text"], select {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }
            button {
                width: 100%;
                padding: 15px;
                background-color: #007BFF;
                border: none;
                border-radius: 4px;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background-color: #0056b3;
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
                background-color: #f4f7f6;
                font-weight: 500;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Predict Cost of Property</h1>
            <form action="{{ url_for('predict')}}" method="post">
                <label for="bedrooms">Integer field</label>
                <input type="text" name="bedrooms" placeholder="Number of Bedrooms" required="required" />
                
                <label for="bathrooms">Integer field</label>
                <input type="text" name="bathrooms" placeholder="Number of Bathrooms" required="required" />

                <label for="property_type">Property Type</label>
                <select name="property_type" required="required">
                    <option value="House">House</option>
                    <option value="Apartment">Apartment</option>
                </select>

                <label for="purchase_type">Purchase Type</label>
                <select name="purchase_type" required="required">
                    <option value="Sale">Sale</option>
                    <option value="Rent">Rent</option>
                </select>

                <label for="new_sub_county">Location</label>
                <select name="new_sub_county" required="required">
                    <option value="Dagoretti North">Dagoretti North</option>
                    <option value="Westlands & Starehe">Westlands & Starehe</option>
                    <option value="Embakasi Areas">Embakasi Areas</option>
                    <option value="Langata & Kibra">Langata & Kibra</option>
                </select>

                <button type="submit">Predict</button>
                
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
                            <td>Langata & Kibra</td>
                            <td>Karen, Nairobi West, Mugumu-Ini, South C, Nyayo Highrise, Nyayo, Ngong, Langata, Ongata Rongai, Rongai, Madaraka, Kiserain, South B, Bomas of Kenya, Golden Estate, Laini Saba, Lindi Makina, Woodley, Kenyatta Golf Course, Sarangombe, Kibra, Jamhuri, Ngumo</td>
                        </tr>
                        <tr>
                            <td>Embakasi Areas</td>
                            <td>Githurai, Kahawa West, Zimmerman, Roysambu, Kahawa Sukari, Kahawa Wendani, Ruiru, Ngecha, Juja, Kenyatta Road, Thika, Ridgeways, Mirema Drive, Garden Estate, Mirema, Tatu City, Umoja I, Umoja One, Umoja 1, Umoja II, Umoja Two, Umoja 2, Umoja, Mowelm, Kariobangi South, Maringo, Hamza, Embakasi West, Donholm, Upper Savannah, Lower Savannah, Savannah, Embakasi, Utawala, Mihango, Embakasi East, Kamulu, Joska, Malaa, Kariobangi North, Dandora, Embakasi North, Imara Daima, Kwa Njenga, Kwa Reuben, Pipeline, Kware, Embakasi South, Kitengela, Syokimau, Mlolongo, Athi River, Mombasa Road, Mombasa Rd, Fedha, Kayole, Kayole North, Kayole South, Kayole Central, Komarock, Matopeni, Spring Valley, Embakasi Central, Clay City, Mwiki, Kasarani, Njiru, Ruai, Saika, Thika Road, Chokaa, Thome, Peponi, Garden City, Thindigua, Viwandani, Harambee, Makongeni, Pumwani, Eastleigh North, Makadara, Buruburu, Jogoo Road, Industrial Area, Eastleigh South, Airbase, California, Ngara, Nairobi Central, Kamukunji, Mabatini, Huruma, Ngei, Mlango Kubwa, Kiamaiko, Mathare, Baba Dogo, Utalii, Matahare North, Lucky Summer, Korogocho, Ruaraka</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])
    property_type = request.form['property_type']
    purchase_type = request.form['purchase_type']
    new_sub_county = request.form['new_sub_county']

    # Predict using the function
    prediction = preprocess_and_predict(
        bedrooms, bathrooms, property_type, purchase_type, new_sub_county
    )

    # Round prediction to 2 decimal places
    prediction = round(prediction, 2)

    # Display prediction
    if purchase_type.lower() == 'rent':
        prediction_text = f"Predicted Monthly Rent (Ksh): {prediction:.2f} (per month)"
    else:
        prediction_text = f"Predicted Price (Ksh): {prediction:.2f}"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Prediction Result</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f4f7f6;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                max-width: 700px;
                width: 100%;
            }
            h1 {
                text-align: center;
                font-weight: 500;
            }
            h2 {
                text-align: center;
                margin-top: 20px;
            }
            .btn {
                display: block;
                width: 100%;
                padding: 15px;
                background-color: #007BFF;
                border: none;
                border-radius: 4px;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
                text-align: center;
                text-decoration: none;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Prediction Result</h1>
            <h2>{{ prediction_text }}</h2>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </body>
    </html>
    ''', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
