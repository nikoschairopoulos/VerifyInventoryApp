<template>
    <div container>
    
    <div class="explanation" v-if="explanationMode">
        <h4> explanation </h4>
        <div id="w3review" name="w3review" rows="8" cols="50" readonly="true" >
            {{ explainMessage }}
        </div>
    </div>
    
    <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
    <div class="group1">    
            <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input type="text" class="form-control" id="name" v-model="name">
            </div>

            <div class="mb-3">
                <label for="Choose Technology" class="form-label">Choose Technology:</label>
                <select id="Choose Technology" v-model="SHEET_TYPE" class="custom-select">
                    <option value="El. Generators">Electrical Generators</option>
                    <option value="Thermal Sources">Thermal Sources</option>
                    <option value="Glazing">Glazing</option>
                    <option value="Insulation">Insulation</option>
                    <option value="Ventilation">Ventilation</option>
                    <option value="PCM">PCM</option>
                    <option value="Water Storage">Water Storage</option>
                    <option value="El. Storage">El. Storage</option>
                    <option value="Other">Other</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="type" class="form-label" @mouseover="explain('type')" @mouseleave="dontExplain">Component Type:</label>
                <input type="text" class="form-control" id="type" v-model="component_type">
            </div>

            <div class="mb-3">
                <label for="type" class="form-label" @mouseover="explain('subtype')" @mouseleave="dontExplain">Component Subtype:</label>
                <input type="text" class="form-control" id="type" v-model="component_subtype">
            </div>

            <!-- Add Numerics -----------------------------------------------------------------------------> 


            <div class="mb-3" @mouseover="explain('CAPEX/UGS')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label">CAPEX/UGS <strong>[€/{{ ugs_header }}]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="capex_per_ugs" min="0">
            </div>
            
            <div class="mb-3" @mouseover="explain('OPEX_PER_CAPEX')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label">OPEX_PER_CAPEX %100:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" min="0">
            </div>

            <div class="mb-3" @mouseover="explain('embodied_co2_per_ugs')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label" >Embodied CO2/UGS<strong>[kgCO2/{{ ugs_header }}]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" min="0">
            </div>

            <div class="mb-3" @mouseover="explain('embodied_pe_per_ugs')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label">Embodied Pe/UGS <strong>[GJ/{{ ugs_header }}]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Component Lifetime <strong>[years]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" min="0">
            </div>

            <button type="submit" class="btn btn-primary">Create Component</button>

        </div>
        <div class="group2">

            <div class="mb-3" @mouseover="explain('pref_cost')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label">Pref Cost <strong>[{{ ugs_header }}]</strong> :</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" min="0">
            </div>
            <div class="mb-3" @mouseover="explain('pref_env')" @mouseleave="dontExplain">
                <label for="quantity" class="form-label">Pref Env <strong>[{{ ugs_header }}]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label" @mouseover="explain('scale_cost')" @mouseleave="dontExplain">Scale Cost:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label" @mouseover="explain('scale_env')" @mouseleave="dontExplain">Scale Env:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label" @mouseover="explain('major_upgrade_point')" @mouseleave="dontExplain">Major Upgrade Point<strong> [years]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label" @mouseover="explain('major_upgrade_share')" @mouseleave="dontExplain">Major Upgrade Share %:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label" @mouseover="explain('annual_performance_degradation')" @mouseleave="dontExplain">Anuual Performance Degradation %:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" min="0">
            </div>
            
            <!-- ... Sheet Type ... -->
            <div class="mb-3">
                <label for="EOL_ACTION" class="form-label">EOL ACTION:</label>
                <select id="EOL_ACTION" v-model="replace_or_die" class="custom-select">
                    <option value="replace">replace</option>
                    <option value="die">die</option>
                </select>
            </div>

            <!-- ... Repeat the pattern for other form elements ... --> 
            <div class="mb-3" >
                <label for="bibliography" style="display:block;">Bibliography:</label>
                <textarea id="bibliography" v-model="bibliography" rows="2" cols="30" placeholder="Add bibliography links or other sources"></textarea>
            </div>

            <div class="mb-3">
                <label for="description" style="display:block;">Description:</label>
                <textarea id="description" v-model="description" rows="2" cols="30"  placeholder="fulfill with usefull info about the Component"></textarea>
            </div>
        
           
            <!-- ... Repeat the pattern for other form elements ... -->

            <div class="mb-3 form-check" @mouseover="explain('MAIN_INVENTORY')" @mouseleave="dontExplain">
                <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="true">
                <label class="form-check-label" for="isMainInventory">TO ADD AT MAIN INVENTORY</label>
            </div>

            
            
    </div>
</form>
</div>

</template>

<script>
import { axios } from "@/common/api.service.js";
export default {
  name: 'AddComponentForm',
  props:['header','componentValues','EditMode'],
  data(){
    return{
        name:null,
        component_type:null,
        component_subtype:null,
        capex_per_ugs:null,
        opex_per_capex:null,
        embodied_co2_per_ugs:null,
        embodied_pe_per_ugs:null,
        lifetime:null,
        pref_cost:null,
        pref_env:null,
        scale_cost:null,
        scale_env:null,
        major_upgrade_point:null,
        major_upgrade_share:null,
        annual_performance_degradation:null,
        replace_or_die:null,
        SHEET_TYPE:null,
        IS_MAIN_INVENTORY:false,
        description:null,
        bibliography:null,
        ugs_header:null,
        explainMessage:null,
        explanationMode:false
    } 
  },
  methods:{
    async handleSubmit(){ 
        const dataObject = this.$data;
        // remove some no need properties: 
        try{
            delete dataObject['ugs_header']
        }catch(error){
            console.log(error)
        }
        try{
        delete dataObject['explainMessage']
        }catch(error){
            console.log(error)
        }
        try{
        delete dataObject['explanationMode']
        }catch(error){
            console.log(error)
        }

        try{
            const {data} = await axios.post('http://127.0.0.1:8000/api/component/',dataObject)
                //this.$refs.anyName.reset();
                for (let elem in this.$data) {this[elem] = null;}
                alert("Success")
                this.IS_MAIN_INVENTORY = false
                this.$router.push({ name:'Home'}); //here add the router name from router/index.js
            }catch(error){
                console.log(error)
                this.$refs.anyName.reset();
                //for (let elem in this.$data) {this[elem] = null;}
                this.IS_MAIN_INVENTORY = false
                alert("Error")
        }        
    },
    explain(explainHeader){
        if(explainHeader==='type'){
            this.explainMessage = 'Is the Components type e.g.  Heatpump'
            this.explanationMode=true
        }
        if(explainHeader==='subtype'){
            this.explainMessage = 'Is the Components subtype e.g. for a Heatpump a subtype would be: water to water'
            this.explanationMode=true
        }
        if(explainHeader==='installed_ugs'){
            this.explainMessage = 'Is the Components installed Nominal Magnitude e.g. for Heatpump is the nominal power to kwh '
            this.explanationMode=true
        }
        if(explainHeader==='CAPEX/UGS'){
            this.explainMessage = 'This parameter is the ratio of a the CAPEX/UGS for the reference component that is considered for this analysis e.g. Heatpumps cost=100 € and nominal power (installed UGS) = 10kW ==>  CAPEX/UGS=10[€/kW]'              
            this.explanationMode=true
        }
        if(explainHeader==='OPEX_PER_CAPEX'){
            this.explainMessage = 'This parameter gives the ratio of components yearly maintenance according to its CAPEX. e.g. if this ratio=10% then considering that Heatpump costs 100€ every year maintenance cost is 10€ '              
            this.explanationMode=true
        }
        if(explainHeader==='embodied_co2_per_ugs'){
            this.explainMessage = 'This parameter gives the ratio of embodied CO2[kg]/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied CO2=100 kg and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[kgCO2/kWh] '              
            this.explanationMode=true
        }
        if(explainHeader==='embodied_pe_per_ugs'){
            this.explainMessage = 'This parameter gives the ratio of embodied Primary/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied Pe=100 GJ and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[GJ/kWh] '              
            this.explanationMode=true
        }
        if(explainHeader==='scale_cost'){
            this.explainMessage = 'exponent for power-scaling the input values to match the size of the user-input(monetery). '              
            this.explanationMode=true
        }
        if(explainHeader==='scale_env'){
            this.explainMessage = 'exponent for power-scaling the input values to match the size of the user-input (environmental).'              
            this.explanationMode=true
        }
        if(explainHeader==='major_upgrade_point'){
            this.explainMessage ='Is time interval that major upgrades for the component occur, e.g. for a heatpump if the major upgrade point is 5 years, every 5 years major upgrade occur for this component.'
            this.explanationMode=true
        }
        if(explainHeader==='major_upgrade_share'){
            this.explainMessage = 'Is the % Percentage of CAPEX to calculate the cost of a major upgrade.'
            this.explanationMode=true
        }
        if(explainHeader==='annual_performance_degradation'){
            this.explainMessage = 'Annual drop of performance'
            this.explanationMode=true
        }
        if(explainHeader==='pref_env'){
            this.explainMessage = 'is the nominal installed UGS for the reference component of the analysis(environmental) e.g for a heatpump would be 10[kW]'
            this.explanationMode=true
        }
        if(explainHeader==='pref_cost'){
            this.explainMessage = 'is the nominal installed UGS for the reference component of the analysis(monetery) e.g for a heatpump would be 8[kW]'
            this.explanationMode=true
        }
        if (explainHeader=='MAIN_INVENTORY'){
            this.explainMessage = 'When a component is not project specific is added at main inventory e.g. there is need to have a generalized Heatpump water to water at Verify inventory.'
            this.explanationMode=true

        }

    },
    dontExplain(){
        this.explanationMode=false
    }
  },
  watch: {
    SHEET_TYPE(newValue) {
        if( newValue=="El. Generators" || newValue=="Thermal Sources" || newValue=='PCM' || newValue=='Ventilation'){
            this.ugs_header = 'kW'
        }else if(newValue=="Water Storage"){
            this.ugs_header='Litre'
        }
        else if(newValue=='El. Storage'){
            this.ugs_header='kWh'
        }
        else if(newValue=='Insulation'){
            this.ugs_header='m\u00B3'
        }
        else if(newValue=='Glazing'){
            this.ugs_header='m\u00B2'
        }
        else if(newValue=='Other'){
            this.ugs_header='UGS'
        }
    }
  }
}

</script>

  <style scoped>

    h1{
        text-align: center;
    }
    #component {
        width: 50%;
        background-color:aliceblue;
        border: 1px solid lightsteelblue;
        display: flex;
        justify-content: space-evenly;
        border-radius: 1%;
    
    }
    /* Apply different styles for smaller viewports */
  @media (max-width: 768px) {
    #component {
        width: 80%;  /* Adjust the width for smaller screens */
    }

    .mb-3 {
        width: 100%;             /* Make each form element take full width on smaller screens */
        box-sizing: border-box;  /* Include padding and border in the width */
        margin-bottom: 10px;     /* Adjust the margin between form elements */
    }

 
  }
  .explanation{
    margin-left: 4%;
    position:fixed;
    width:20%;
    background-color: palegreen;
  }

  #w3review{
    text-align:left;
  }

  </style>


    
