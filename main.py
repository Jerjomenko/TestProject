from flask import Flask, render_template, request
from flask.views import View
from flask_cors import CORS
import json
from dateutil import parser


app = Flask(__name__)
CORS(app)
class IndexView(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):
        info_dict = {
            "10k": ("1.212.120", 40000),
            "15k": ("2.727.270", 90000),
            "20k": ("4.545.450", 150000),
            "25k": ("5.000.000", 165000),
            "30k": ("5.454.550", 180000),
            "35k": ("5.909.090", 195000),
            "40k": ("6.363.640", 210000),
            "50k": ("8.181.820", 270000)
        }

        if request.method == "POST":
            self.plz_value = request.json.get("plzValue")
            atvVal = request.json.get("atvVal")
            youtubeVal = request.json.get("youtubeVal")
            freeveeVal = request.json.get("freeveeVal")
            options = {"pg": 25, "cross": 20, "searchintent": -50, "finecastkids": -91,
                       "gamblalkohol": -50, "longvideo": 1, "youtube": youtubeVal,
                       "freevee": freeveeVal, "atv": atvVal, "netflix": 20, "disney": 10}
            updateAmount = 0
            self.activeOptions = []
            with open("data.json", "r") as file:
                data = json.load(file)
            baseImpressions = data[self.plz_value]
            for k, v in options.items():
                if request.json.get(k):
                    updateAmount += baseImpressions * int(v) / 100
                    self.activeOptions.append(k)


            self.impresions = int(data[self.plz_value] + updateAmount)
            tkp = int(request.json.get("tkpValue"))
            price = request.json.get("priceValue")
            price = float(price)
            if tkp == 1000:
                self.budget_day = round((self.impresions * price) / tkp, -2)
            else:
                self.budget_day = round((self.impresions * price) * 930 / 1000, -2)

            start_date_str = request.json.get("startDate")
            end_date_str = request.json.get("endDate")

            # Verwende dateutil.parser.parse, um verschiedene Datumsformate zu akzeptieren weil Json hat format ISO
            start_date = parser.parse(start_date_str)
            end_date = parser.parse(end_date_str)
            date_interval = end_date - start_date
            days = date_interval.days + 1

            self.laufzeit_impressions = self.impresions * days
            self.laufzeit_price = self.budget_day * days

            calculations = {
                "plzValue": self.plz_value,
                "activeOptions": self.activeOptions,
                "startDate": str(start_date).split()[0],
                "endDate": str(end_date).split()[0],
                "Interval": days,
                "tkpValue": tkp,
                "priceValue": price,
                "impressions": self.impresions,
                "budgetDay": self.budget_day,
                "impressoinsLaufzeit": self.laufzeit_impressions,
                "budgetLaufzeit": self.laufzeit_price
            }
            with open("saved_calculations.txt", "a") as file:
                file.write(json.dumps(calculations) + '\n')

        return render_template('index.html', info_dict=info_dict)

# Weise die IndexView-Klasse der Route '/' zu
app.add_url_rule('/', view_func=IndexView.as_view('index'))


if __name__ == '__main__':
    app.run(debug=True)
