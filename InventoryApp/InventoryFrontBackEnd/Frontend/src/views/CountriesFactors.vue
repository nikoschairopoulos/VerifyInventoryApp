<template>
    <div class="input-form" @submit.prevent="handleSubmit">
        <!--<h1 v-if="country && fuel">Update: <span style="color:springgreen">{{fullName}}</span></h1>-->
        <p>1.Choose a Country</p>
        <p>2.Choose a Fuel</p>
        <hr>
        <form class="row g-3 needs-validation" novalidate>
            <div class="col-6">
                <label for="Choose Country" class="form-label">Choose Country:</label>
                <select id="Choose Country" class="form-control" v-model="country" style="background: darkseagreen"
                    required>
                    <option value="Albania">Albania</option>
                    <option value="Andorra">Andorra</option>
                    <option value="Austria">Austria</option>
                    <option value="Belarus">Belarus</option>
                    <option value="Belgium">Belgium</option>
                    <option value="Bosnia and Herzegovina">Bosnia and Herzegovina</option>
                    <option value="Bulgaria">Bulgaria</option>
                    <option value="Croatia">Croatia</option>
                    <option value="Cyprus">Cyprus</option>
                    <option value="Czech Republic">Czech Republic</option>
                    <option value="Denmark">Denmark</option>
                    <option value="Estonia">Estonia</option>
                    <option value="Finland">Finland</option>
                    <option value="France">France</option>
                    <option value="Germany">Germany</option>
                    <option value="Greece">Greece</option>
                    <option value="Hungary">Hungary</option>
                    <option value="Iceland">Iceland</option>
                    <option value="Ireland">Ireland</option>
                    <option value="Italy">Italy</option>
                    <option value="Kosovo">Kosovo</option>
                    <option value="Latvia">Latvia</option>
                    <option value="Liechtenstein">Liechtenstein</option>
                    <option value="Lithuania">Lithuania</option>
                    <option value="Luxembourg">Luxembourg</option>
                    <option value="Malta">Malta</option>
                    <option value="Moldova">Moldova</option>
                    <option value="Monaco">Monaco</option>
                    <option value="Montenegro">Montenegro</option>
                    <option value="Netherlands">Netherlands</option>
                    <option value="Norway">Norway</option>
                    <option value="Poland">Poland</option>
                    <option value="Portugal">Portugal</option>
                    <option value="Romania">Romania</option>
                    <option value="Russia">Russia</option>
                    <option value="San Marino">San Marino</option>
                    <option value="Serbia">Serbia</option>
                    <option value="Slovakia">Slovakia</option>
                    <option value="Slovenia">Slovenia</option>
                    <option value="Spain">Spain</option>
                    <option value="Sweden">Sweden</option>
                    <option value="Switzerland">Switzerland</option>
                    <option value="Ukraine">Ukraine</option>
                    <option value="United Kingdom">United Kingdom</option>
                    <option value="Vatican City">Vatican City</option>
                </select>
                <div class="valid-feedback">
                    pass
                </div>
            </div>

            <div class="col-6">
                <label for="Choose Fuel" class="form-label">Choose Fuel:</label>
                <select id="Choose Fuel" class="form-control" style="background: darkseagreen" v-model="fuel" required>
                    <option value="electricity">Electricity</option>
                    <option value="ngas">Net Gas</option>
                    <option value="diesel">Diesel</option>
                    <option value="biomass">Biomass</option>
                    <option value="biodiesel">Biodiesel</option>
                    <option value="oil">Oil</option>
                    <option value="lpg">LPG</option>
                    <option value="res">RES</option>
                    <option value="hydrogen">Hydrogen</option>
                </select>
                <div class="valid-feedback">
                    pass
                </div>
            </div>



            <!--Output section-->
            <hr>

            <div class="col-6">
                <label for="validationCustom01" class="form-label">Primary Energy Factor [kWh/Fuel kWh]</label>
                <input type="number" step="any" class="form-control" id="validationCustom01" v-model="pef" required
                    min="1">
                <div class="valid-feedback">
                    pass
                </div>
            </div>

            <div class="col-6">
                <label for="validationCustom01" class="form-label">CO2-eq Emission Factor [kg/kWh]</label>
                <input type="number" step="any" class="form-control" id="validationCustom01" v-model="co2" required
                    min="0">
                <div class="valid-feedback">
                    pass
                </div>
            </div>



            <!--add extra fields (comment and source)-->
            <div class="col-6">
                <label for="validationCustom01" class="form-label">Comments</label>
                <textarea class="form-control" id="validationCustom01" v-model="comments" required rows="5"
                    maxlength="50" style="resize: none;">
                    </textarea>
                <div class="valid-feedback">
                    pass
                </div>
            </div>


            <div class="col-6">
                <label for="validationCustom01" class="form-label">Source</label>
                <textarea class="form-control" id="validationCustom01" v-model="source" required rows="5" maxlength="50"
                    style="resize: none;">
                    </textarea>
                <div class="valid-feedback">
                    pass
                </div>
            </div>



            <!--submit button-->

            <div class="col-12">
                <button class="btn btn-primary" type="submit">Update Factors</button>
            </div>
        </form>

        <!-- 
        <hr>
        <h4 style="text-align:center;">CO2 MAP</h4>
        <hr>
        <div v-if='infoObj' id="map">
            <MapChart
                :countryData="this.infoObj"
                highColor="#ff0000"
                lowColor="#aaaaaa"
                countryStrokeColor="#909090"
                defaultCountryFillColor="#dadada"
            />
        </div>
        -->
        <hr>

        <!--Plot element:-->
        <h3>Plot CO2 Hourly Emission Factor per Country:</h3>
        <p v-if="!chartData" style="color:red">{{ errorMessageHourlyFactors }}</p>
        <div v-if='chartData' class="col-2">
            <label for="Choose Monthly or Daily" class="form-label">Choose Monthly or Daily Granularity</label>
            <select id="Choose Monthly or Daily" class="form-control" style="background: darkgray;height: 32px;"
                v-model="yearMonthOption">
                <option value="month">Monthly Average</option>
                <option value="day">Day Average</option>
            </select>
        </div>
        <br>
        <br>

        <div class="plots">
            <div v-if='chartData' class="diagram">
                <Bar :data="chartData" :options="options" />
            </div>

            <div v-if='country' class="diagram">
                <Bar :data="chartDataFossils" :options="options" />
            </div>
        </div>

    </div>







</template>

<script>
import { axios } from "@/common/api.service.js";
import { TARGET_IP } from "@/common/request_configs.js";
import MapChart from 'vue-map-chart';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    BarElement,
    Legend
} from 'chart.js'
import { Scatter, Line, Bar } from 'vue-chartjs'
import chartTrendline from 'chartjs-plugin-trendline';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend
)

ChartJS.register(chartTrendline);

export default {
    name: 'CountriesFactors',
    components: { MapChart, Scatter, Line, Bar },
    data() {
        return {
            id: null,
            pef: null,
            co2: null,
            fuel: null,
            country: null,
            factorsdb: [],
            infoObj: { 'LS': -100 },
            comments: null,
            source: null,
            sample_data: null,
            yearMonthOption: 'month',
            co2SeriesData: null,
            errorMessageHourlyFactors: 'no country selected to plot data',
            chartData: null,
            chartDataFossils:null,
            options: {
                scales: {
                    x: {
                        position: 'bottom',
                        title: {
                            display: true,
                            //text: 'hour of the Year',
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'KgC02/kWh',
                        },
                    },
                },
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: 'KgCO2 Emission per kWh'
                    },
                    tooltip: {
                        enabled: true,  // Tooltips enabled (set to false to hide)
                    },
                },
            }

        }
    },
    //beforeMount(){
    // for testing:
    //    this.yearMonthOption = 'month';
    //},

    mounted() {
        (function () {
            'use strict';
            var forms = document.querySelectorAll('.needs-validation');
            Array.prototype.slice.call(forms).forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        })();

        axios.get(`${TARGET_IP}/api/factor/`)
            .then(response => {
                for (let comp of response.data) {
                    this.factorsdb.push(comp);
                }
                console.log(response.data);
                console.log(this.factorsdb);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });


        //this.currentYear = new Date().getFullYear()
        // Populate the years array with values from 2018 to the current year
        //for (let i = 2018; i <= this.currentYear; i++) {
        //    this.years.push(i);
        //}
        //console.log(this.currentYear)
    },
    beforeUnmount() {
        // *******PROPABLY THERE IS A BUG WITH MAP CHART COMPONENT *****
        try {
            let countryname = this.getCountryCodeOrName(this.country)[1]
            this.infoObj[countryname] = 0;
            //location.reload()
        }
        catch (e) {
            console.log(e)
        }
    },
    created() {

    },
    watch: {
        fullName(newValue) {
            console.log("change at country-fuel combination have been detected")
            this.fillDataofCountry()
        },
        yearMonthOption(newValue) {
            let chartData = {
                        labels: this.takeLabelsforFactorPlot(newValue),
                        datasets: [
                            {
                                label: 'CO2Eq',
                                data: this.takeAveragePerMonthorDay(newValue).map((e) => e.y),  // Use the generated points
                                backgroundColor: 'rgba(0, 123, 255, 0.7)',  // Single color for all bars
                                fill: true,
                                borderColor: 'rgba(255, 255, 0, 1)',
                                barThickness: 10,         // Manually set bar width to control overall layout
                                categoryPercentage: 0.5,  // Use 90% of available category width
                                barPercentage: 0.8,       // Each bar takes up 80% of its category's width
                            }
                        ]
            }
            this.chartData = chartData
            /*
            if (newValue=='month'){
                chartData.datasets[0].trendlineLinear = {
                                    colorMin: "red",
                                    colorMax: "green",
                                    lineStyle: "dotted|solid",
                                    width: 2,
                                    projection: false
                                }
                this.chartData = chartData
            }else if(newValue=='day'){
                chartData.datasets[0].trendlineLinear = {
                                    colorMin: "red",
                                    colorMax: "green",
                                    lineStyle: "dotted|solid",
                                    width: 2,
                                    projection: false
                                }
                this.chartData = chartData
            }
            */
        },
        country(newValue) {
            console.log("i am in country watcher")
            // heare update the the electricity series (for now is for 2023)
            //f"http://192.168.101.31:8003/api/get_electricity_measurements/{country}/{year_to_retrieve_data}

            //Returns promise:
            const tempFunction = async () => {
                try {

                    // take the data
                    let year_to_retrieve_data = 2023 // this is temporary due to we will make it parameter:
                    const response = await axios.get(`${TARGET_IP}/api/get_electricity_measurements/${newValue}/${year_to_retrieve_data}`);
                    let dataFromApi = JSON.parse(response.data);
                    this.co2SeriesData = Object.values(dataFromApi['carbon_intensity_gco2_eq_kwh_direct']);
                    console.log("-----------------")
                    console.log(this.co2SeriesData)
                    //setTimeout(()=>(null),10000000)
                    // update char data:
                    let chartData = {
                        labels: this.takeLabelsforFactorPlot('month'),
                        datasets: [
                            {
                                label: 'CO2Eq Emission Factor Data',
                                data: this.takeAveragePerMonthorDay('month').map((e) => e.y),  // Use the generated points
                                backgroundColor: 'rgba(0, 123, 255, 0.7)',  // Single color for all bars
                                fill: true,
                                borderColor: 'rgba(255, 255, 0, 1)',
                                barThickness: 10,  // Manually set bar width to control overall layout
                                categoryPercentage: 0.5,  // Use 90% of available category width
                                barPercentage: 0.8,  // Each bar takes up 80% of its category's width
                                /*
                                trendlineLinear: {
                                    colorMin: "red",
                                    colorMax: "green",
                                    lineStyle: "dotted|solid",
                                    width: 2,
                                    projection: false
                                }
                                */
                                
                            }
                        ]
                    }
                    return chartData;
                } catch (error) {
                    console.error("Error fetching Data:", error);
                    throw error
                }
            }

            // read the promise using chaining
            tempFunction().then((chartData) => {
                this.chartData = chartData;
            }).catch((e) => {
                console.error("Failed to fetch chart data.");
                this.chartData = null
                this.errorMessageHourlyFactors = 'no hourly electricity data provided for this country'
            });

            // UPDATE fossils for the current country:
            this.updateFossils(newValue)

        }
    },
    methods: {
        updateFossils(newValue){
            // update also data for fossils:
            console.log(this.factorsdb)
            let fossilsData = this.factorsdb.filter((comp)=>comp.country==newValue && comp.fuel!='electricity')
            console.log(`this is chart data:${fossilsData}`)
            let labelsFossils = fossilsData.map((comp)=>comp.fuel)
            let co2Values = []
            for (let fuel of labelsFossils){
                let value = fossilsData.filter((comp)=>comp.fuel==fuel)[0].co2_factor
                co2Values.push(value)
                console.log(fuel)
                console.log(value)
                console.log("--new--")
            }
            console.log(labelsFossils)
            this.chartDataFossils = {
                    labels: labelsFossils,
                    datasets: [
                        {
                            label: 'Non Electricity Fuels CO2Eq Emission Factor Data',
                            data:  co2Values,  // Use the generated points
                            backgroundColor: 'rgba(0, 123, 255, 0.7)',  // Single color for all bars
                            fill: true,
                            borderColor: 'rgba(255, 255, 0, 1)',
                            barThickness: 10,  // Manually set bar width to control overall layout
                            categoryPercentage: 0.5,  // Use 90% of available category width
                            barPercentage: 0.8,  // Each bar takes up 80% of its category's width
                            /*
                            trendlineLinear: {
                                colorMin: "red",
                                colorMax: "green",
                                lineStyle: "dotted|solid",
                                width: 2,
                                projection: false
                            }
                            */            
                        }
                    ]
                }

        },        
        async handleSubmit() {
            try {
                let dataObject = {
                    country: this.country,
                    fuel: this.fuel,
                    co2_factor: this.co2,
                    primary_energy_factor: this.pef,
                    source: this.source,
                    comments: this.comments,
                }
                //returns only one object (there is resriction from the DB)
                let obj = this.factorsdb.filter(comp => comp.country == this.country && comp.fuel == this.fuel)
                console.log("i try to send data at the Backend....", this.$data)
                const { data } = await axios.put(`${TARGET_IP}/api/factor/${obj[0].id}/`, dataObject)
                alert("Success")
                window.location.reload() //here add the router name from router/index.js
            } catch (error) {
                alert("Error")
            }
        },
        fillDataofCountry() {
            try {
                this.infoObj = {}
                let obj = this.factorsdb.filter(comp => comp.country == this.country && comp.fuel == this.fuel)
                console.log(obj[0])
                console.log('--------Inform the attributes--------')
                this.pef = obj[0].primary_energy_factor
                this.co2 = obj[0].co2_factor
                this.id = obj[0].id
                //this.year = obj[0].year
                this.source = obj[0].source
                this.comments = obj[0].comments

                //after updating co2 for the Map:
                console.log("there  data for this country fuel combination")
                let countryname = this.getCountryCodeOrName(this.country)[1]
                this.infoObj[countryname] = this.co2;
                this.infoObj['LS'] = -100;
                console.log("the country name is ==========", this.infoObj)
            } catch (e) {
                console.log(e)
                this.co2 = null;
                this.pef = null;
                this.id = null
                //this.year = null
                this.source = null
                this.comments = null
            }
        },
        getCountryCodeOrName(inputValue) {
            var nameCountries = {
                'Afghanistan': 'AF',
                'Aland Islands': 'AX',
                'Albania': 'AL',
                'Algeria': 'DZ',
                'American Samoa': 'AS',
                'Andorra': 'AD',
                'Angola': 'AO',
                'Anguilla': 'AI',
                'Antarctica': 'AQ',
                'Antigua And Barbuda': 'AG',
                'Argentina': 'AR',
                'Armenia': 'AM',
                'Aruba': 'AW',
                'Australia': 'AU',
                'Austria': 'AT',
                'Azerbaijan': 'AZ',
                'Bahamas': 'BS',
                'Bahrain': 'BH',
                'Bangladesh': 'BD',
                'Barbados': 'BB',
                'Belarus': 'BY',
                'Belgium': 'BE',
                'Belize': 'BZ',
                'Benin': 'BJ',
                'Bermuda': 'BM',
                'Bhutan': 'BT',
                'Bolivia': 'BO',
                'Bosnia And Herzegovina': 'BA',
                'Botswana': 'BW',
                'Bouvet Island': 'BV',
                'Brazil': 'BR',
                'British Indian Ocean Territory': 'IO',
                'Brunei Darussalam': 'BN',
                'Bulgaria': 'BG',
                'Burkina Faso': 'BF',
                'Burundi': 'BI',
                'Cambodia': 'KH',
                'Cameroon': 'CM',
                'Canada': 'CA',
                'Cape Verde': 'CV',
                'Cayman Islands': 'KY',
                'Central African Republic': 'CF',
                'Chad': 'TD',
                'Chile': 'CL',
                'China': 'CN',
                'Christmas Island': 'CX',
                'Cocos (Keeling) Islands': 'CC',
                'Colombia': 'CO',
                'Comoros': 'KM',
                'Congo': 'CG',
                'Congo, Democratic Republic': 'CD',
                'Cook Islands': 'CK',
                'Costa Rica': 'CR',
                'Cote D\'Ivoire': 'CI',
                'Croatia': 'HR',
                'Cuba': 'CU',
                'Cyprus': 'CY',
                'Czech Republic': 'CZ',
                'Denmark': 'DK',
                'Djibouti': 'DJ',
                'Dominica': 'DM',
                'Dominican Republic': 'DO',
                'Ecuador': 'EC',
                'Egypt': 'EG',
                'El Salvador': 'SV',
                'Equatorial Guinea': 'GQ',
                'Eritrea': 'ER',
                'Estonia': 'EE',
                'Ethiopia': 'ET',
                'Falkland Islands (Malvinas)': 'FK',
                'Faroe Islands': 'FO',
                'Fiji': 'FJ',
                'Finland': 'FI',
                'France': 'FR',
                'French Guiana': 'GF',
                'French Polynesia': 'PF',
                'French Southern Territories': 'TF',
                'Gabon': 'GA',
                'Gambia': 'GM',
                'Georgia': 'GE',
                'Germany': 'DE',
                'Ghana': 'GH',
                'Gibraltar': 'GI',
                'Greece': 'GR',
                'Greenland': 'GL',
                'Grenada': 'GD',
                'Guadeloupe': 'GP',
                'Guam': 'GU',
                'Guatemala': 'GT',
                'Guernsey': 'GG',
                'Guinea': 'GN',
                'Guinea-Bissau': 'GW',
                'Guyana': 'GY',
                'Haiti': 'HT',
                'Heard Island & Mcdonald Islands': 'HM',
                'Holy See (Vatican City State)': 'VA',
                'Honduras': 'HN',
                'Hong Kong': 'HK',
                'Hungary': 'HU',
                'Iceland': 'IS',
                'India': 'IN',
                'Indonesia': 'ID',
                'Iran, Islamic Republic Of': 'IR',
                'Iraq': 'IQ',
                'Ireland': 'IE',
                'Isle Of Man': 'IM',
                'Israel': 'IL',
                'Italy': 'IT',
                'Jamaica': 'JM',
                'Japan': 'JP',
                'Jersey': 'JE',
                'Jordan': 'JO',
                'Kazakhstan': 'KZ',
                'Kenya': 'KE',
                'Kiribati': 'KI',
                'Korea': 'KR',
                'Kuwait': 'KW',
                'Kyrgyzstan': 'KG',
                'Lao People\'s Democratic Republic': 'LA',
                'Latvia': 'LV',
                'Lebanon': 'LB',
                'Lesotho': 'LS',
                'Liberia': 'LR',
                'Libyan Arab Jamahiriya': 'LY',
                'Liechtenstein': 'LI',
                'Lithuania': 'LT',
                'Luxembourg': 'LU',
                'Macao': 'MO',
                'Macedonia': 'MK',
                'Madagascar': 'MG',
                'Malawi': 'MW',
                'Malaysia': 'MY',
                'Maldives': 'MV',
                'Mali': 'ML',
                'Malta': 'MT',
                'Marshall Islands': 'MH',
                'Martinique': 'MQ',
                'Mauritania': 'MR',
                'Mauritius': 'MU',
                'Mayotte': 'YT',
                'Mexico': 'MX',
                'Micronesia, Federated States Of': 'FM',
                'Moldova': 'MD',
                'Monaco': 'MC',
                'Mongolia': 'MN',
                'Montenegro': 'ME',
                'Montserrat': 'MS',
                'Morocco': 'MA',
                'Mozambique': 'MZ',
                'Myanmar': 'MM',
                'Namibia': 'NA',
                'Nauru': 'NR',
                'Nepal': 'NP',
                'Netherlands': 'NL',
                'Netherlands Antilles': 'AN',
                'New Caledonia': 'NC',
                'New Zealand': 'NZ',
                'Nicaragua': 'NI',
                'Niger': 'NE',
                'Nigeria': 'NG',
                'Niue': 'NU',
                'Norfolk Island': 'NF',
                'Northern Mariana Islands': 'MP',
                'Norway': 'NO',
                'Oman': 'OM',
                'Pakistan': 'PK',
                'Palau': 'PW',
                'Palestinian Territory, Occupied': 'PS',
                'Panama': 'PA',
                'Papua New Guinea': 'PG',
                'Paraguay': 'PY',
                'Peru': 'PE',
                'Philippines': 'PH',
                'Pitcairn': 'PN',
                'Poland': 'PL',
                'Portugal': 'PT',
                'Puerto Rico': 'PR',
                'Qatar': 'QA',
                'Reunion': 'RE',
                'Romania': 'RO',
                'Russian Federation': 'RU',
                'Rwanda': 'RW',
                'Saint Barthelemy': 'BL',
                'Saint Helena': 'SH',
                'Saint Kitts And Nevis': 'KN',
                'Saint Lucia': 'LC',
                'Saint Martin': 'MF',
                'Saint Pierre And Miquelon': 'PM',
                'Saint Vincent And Grenadines': 'VC',
                'Samoa': 'WS',
                'San Marino': 'SM',
                'Sao Tome And Principe': 'ST',
                'Saudi Arabia': 'SA',
                'Senegal': 'SN',
                'Serbia': 'RS',
                'Seychelles': 'SC',
                'Sierra Leone': 'SL',
                'Singapore': 'SG',
                'Slovakia': 'SK',
                'Slovenia': 'SI',
                'Solomon Islands': 'SB',
                'Somalia': 'SO',
                'South Africa': 'ZA',
                'South Georgia And Sandwich Isl.': 'GS',
                'Spain': 'ES',
                'Sri Lanka': 'LK',
                'Sudan': 'SD',
                'Suriname': 'SR',
                'Svalbard And Jan Mayen': 'SJ',
                'Swaziland': 'SZ',
                'Sweden': 'SE',
                'Switzerland': 'CH',
                'Syrian Arab Republic': 'SY',
                'Taiwan': 'TW',
                'Tajikistan': 'TJ',
                'Tanzania': 'TZ',
                'Thailand': 'TH',
                'Timor-Leste': 'TL',
                'Togo': 'TG',
                'Tokelau': 'TK',
                'Tonga': 'TO',
                'Trinidad And Tobago': 'TT',
                'Tunisia': 'TN',
                'Turkey': 'TR',
                'Turkmenistan': 'TM',
                'Turks And Caicos Islands': 'TC',
                'Tuvalu': 'TV',
                'Uganda': 'UG',
                'Ukraine': 'UA',
                'United Arab Emirates': 'AE',
                'United Kingdom': 'GB',
                'United States': 'US',
                'United States Outlying Islands': 'UM',
                'Uruguay': 'UY',
                'Uzbekistan': 'UZ',
                'Vanuatu': 'VU',
                'Venezuela': 'VE',
                'Viet Nam': 'VN',
                'Virgin Islands, British': 'VG',
                'Virgin Islands, U.S.': 'VI',
                'Wallis And Futuna': 'WF',
                'Western Sahara': 'EH',
                'Yemen': 'YE',
                'Zambia': 'ZM',
                'Zimbabwe': 'ZW'
            }

            var errorCode = "";

            if (inputValue === undefined || Boolean(inputValue.match(/^[^,'& ()-]{1}([a-zA-Z\s',&()-]){0,80}$/)) === false) { errorCode = "5555" }
            var inlength = inputValue.length;
            if (errorCode === "5555") {
                return ["ErrorCode 5555: Unsupported Data, return input value in array 1", inputValue];
            }

            if (inlength === 2) {
                var outValue = inputValue.toUpperCase();
                var countryName = "";
                for (var name in nameCountries) {
                    if (nameCountries[name] === outValue) {
                        countryName = name;
                    }
                }
                switch (true) {
                    case Boolean(countryName === ""):
                        return ["Country code does not match database record: return input value in array 1", inputValue];
                        break;

                    default:
                        return [outValue, countryName];
                        break;
                }

            }

            if (inlength > 2) {
                var outValue = inputValue.toLowerCase();

                switch (true) {
                    case Boolean(outValue.match(/^[Gg][Uu][Ii][Nn][Ee][Aa][-][Bb][Ii][Ss][Ss][Aa][Uu]$/)):
                        outValue = "Guinea-Bissau";
                        break;

                    case Boolean(outValue.match(/^[Hh][Oo][Ll][Yy][ ][Ss][Ee][Ee][ ][(][Vv][Aa][Tt][Ii][Cc][Aa][Nn][ ][Cc][Ii][Tt][Yy][ ][Ss][Tt][Aa][Tt][Ee][)]$/)):
                        outValue = "Holy See (Vatican City State)";
                        break;

                    case Boolean(outValue.match(/[Ff][Aa][Ll][Kk][Ll][Aa][Nn][Dd][ ][Ii][Ss][Ll][Aa][Nn][Dd][Ss][ ][(][Mm][Aa][Ll][Vv][Ii][Nn][Aa][Ss][)]$/)):
                        outValue = "Falkland Islands (Malvinas)";
                        break;

                    case Boolean(outValue.match(/^[Ii][Rr][Aa][Nn]$/)):
                        outValue = "Iran, Islamic Republic Of";
                        break;

                    default:
                        var arrCName = outValue.split(" ");
                        var cNameJoin = "";
                        for (var i in arrCName) {
                            cNameJoin += arrCName[i].charAt(0).toUpperCase() + arrCName[i].slice(1) + " ";
                        }
                        outValue = cNameJoin.trim();
                        break;
                }


                return [
                    (nameCountries.hasOwnProperty(outValue) ? outValue : "Input country doesn't match database: returned input in array 1"),
                    (nameCountries.hasOwnProperty(outValue) ? nameCountries[outValue] : inputValue)
                ];
            }
        },
        takeDaysoftheYear() {
            let daysInMonth = [
                { "month": "January", "days": 31 },
                { "month": "February", "days": 28 },
                { "month": "March", "days": 31 },
                { "month": "April", "days": 30 },
                { "month": "May", "days": 31 },
                { "month": "June", "days": 30 },
                { "month": "July", "days": 31 },
                { "month": "August", "days": 31 },
                { "month": "September", "days": 30 },
                { "month": "October", "days": 31 },
                { "month": "November", "days": 30 },
                { "month": "December", "days": 31 }
            ]
            let res = daysInMonth.map(e => e['days'])
            return res
            // if is a leap year handle here:
            // to do 
        },
        takeAveragePerMonthorDay(option) {
            console.log(` option == ${option}`)
            let step;
            let step_options = {
                month: {
                    step: this.takeDaysoftheYear(),
                    upperStep: 8760
                },
                day: {
                    step: 24,
                    upperStep: 8760
                },
            };
            let arr = this.co2SeriesData;
            let avg = [];
            let i = 0  // is every time sthe start of the slice:
            while (i < step_options[option].upperStep) {
                if (option == 'month') {
                    step = step_options[option].step.shift() * 24
                } else if (option == 'day') {
                    step = step_options[option].step
                }
                //slice:
                console.log(`${i}  ${i + step}`)
                let windowArray = arr.slice(i, i + step);
                //take Average:
                let currentAvg =
                    windowArray.reduce((acc, current) => acc + current) / windowArray.length;
                avg.push({ y: currentAvg });
                i += step
                console.log(`-----------------------`)
                //console.log(currentAvg);
            }
            return avg;
        },
        createSampleData() {
            let arr = [];
            for (let i = 0; i < 8760; i++) {
                arr.push(Math.random(0, 1));
            }
            return arr;
        },
        takeLabelsforFactorPlot(option) {
            if (option == "month") {
                return [
                    'January',
                    'February',
                    'March',
                    'April',
                    'May',
                    'June',
                    'July',
                    'August',
                    'September',
                    'October',
                    'November',
                    'December'
                ];
            } else if (option == "day") {
                return [...Array(365).keys()].map(x => x + 1);
            }
        }
    },

    computed: {
        fullName() {
            return this.country + '-' + this.fuel
        }
    }
}




</script>


<style scoped>
.input-form {
    margin: 0 auto;
    width: 99.5%;
    /*border: solid greenyellow 1px;*/
    padding: 20px;
}

h3 {
    color: cornflowerblue;
}

.plots{
    display: flex;
    justify-content: space-around;
}
.diagram {
    width: 40%;
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
