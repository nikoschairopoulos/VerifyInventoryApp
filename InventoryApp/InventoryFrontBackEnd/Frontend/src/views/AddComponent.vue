<template>
    <div container>
    
    <div class="explanation" v-if="explanationMode">
        <h4> explanation </h4>
        <div id="w3review" name="w3review" rows="8" cols="50" readonly="true" >
            {{ explainMessage }}
        </div>
    </div>
    
    <div class="form-photo">
        <div class="directives">
            <br>
            <p><strong>tip:</strong>In case you want to set the <span style="color:darkgreen"><strong>CAPEX, Embodied PE and CO2</strong></span> &nbsp; &nbsp; <br>
            from a Project Inventory, as it is given:<br>
            - set <strong>scale env = 0</strong><br>
            - set <strong>scale cost = 0</strong>
            </p>
            <img id="tech_image" src="../../public/pv.jpg" alt="">
        </div>
        <div class="input-form" @submit.prevent="handleSubmit">
            <form ref="anyName" class="container mt-4 needs-validation" novalidate id="component">
            <div class="col-6"> 
                <p><strong>All fields with * are Mandatory</strong></p>   
                    <div class="mb-2 mt-3">
                        <label for="name" class="form-label">Name*:</label>
                        <input type="text" class="form-control" id="name" v-model="name" required>
                    </div>

                    <div class="mb-2">
                        <label for="Choose Technology" class="form-label">Choose Technology*:</label>
                        <select id="Choose Technology" v-model="SHEET_TYPE" class="custom-select" required>
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

                    <div class="mb-2">
                        <label for="type" class="form-label" @mouseover="explain('type')" @mouseleave="dontExplain">Component Type* :</label>
                        <input type="text" class="form-control" id="type" v-model="component_type" required>
                    </div>

                    <div v-if="showSubtype" class="mb-2">
                        <label for="type" class="form-label" id="subtype_element" @mouseover="explain('subtype')" @mouseleave="dontExplain">Component Subtype* :</label>
                        <input type="text" class="form-control" id="type" v-model="component_subtype" required>
                    </div>

                    <!-- Add Numerics -----------------------------------------------------------------------------> 


                    <div class="mb-2" @mouseover="explain('CAPEX/UGS')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label">CAPEX/UGS*:<strong>[€/{{ ugs_header }}]</strong>:<span v-if="capex_per_ugs<0" class="text-danger"> <br> valid value is non negative</span></label>
                        <input type="number" step="any" class="form-control"  id="validationCustom01" v-model="capex_per_ugs" min="0" required>
                    </div>
                    
                    <div class="mb-2" @mouseover="explain('OPEX_PER_CAPEX')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label">ANNUAL MAINTENANCE* [%CAPEX]: <span v-if="opex_per_capex>100 || opex_per_capex<0" class="text-danger"> <br> valid range is [0,100]</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" min="0" max="100" required>
                    </div>

                    <div class="mb-2" @mouseover="explain('embodied_co2_per_ugs')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label" >Embodied CO2/UGS* <strong>[kgCO2/{{ ugs_header }}]</strong>:<span v-if="embodied_co2_per_ugs<0" class="text-danger"><br> valid value is non negative</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" min="0" required>
                    </div>

                    <div class="mb-2" @mouseover="explain('embodied_pe_per_ugs')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label">Embodied Pe/UGS* <strong>[GJ/{{ ugs_header }}]</strong>:<span v-if="embodied_pe_per_ugs<0" class="text-danger"><br> valid value is non negative</span> </label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" min="0" required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label">Component Lifetime* <strong>[years]</strong>:<span v-if="lifetime<0" class="text-danger"><br> valid value is non negative</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" min="0" required>
                    </div>

                    <div class="mb-2 form-check" @mouseover="explain('MAIN_INVENTORY')" @mouseleave="dontExplain">
                        <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="false" >
                        <label class="form-check-label" for="isMainInventory">TO ADD AT MAIN INVENTORY</label>
                    </div>

                    <button type="submit" class="btn btn-primary">Create Component</button>


            </div>
            <div  id="group2" class="col-6">

                    <div class="mb-2 mt-3" @mouseover="explain('pref_cost')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label">Pref Cost* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" min="0" required>
                    </div>
                    <div class="mb-2" @mouseover="explain('pref_env')" @mouseleave="dontExplain">
                        <label for="quantity" class="form-label">Pref Env* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_env<0" class="text-danger"><br> valid value is non negative</span><br></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" min="0" required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label" @mouseover="explain('scale_cost')" @mouseleave="dontExplain">Scale Cost*:</label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost"  required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label" @mouseover="explain('scale_env')" @mouseleave="dontExplain">Scale Env*:</label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env"  required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label" @mouseover="explain('major_upgrade_point')" @mouseleave="dontExplain">Major Upgrade Point* <strong> [years]</strong>:<span v-if="major_upgrade_point<0" class="text-danger"><br> valid value is non negative</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" min="0" required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label" @mouseover="explain('major_upgrade_share')" @mouseleave="dontExplain">Major Upgrade Share* %:<span v-if="major_upgrade_share>100 || major_upgrade_share<0" class="text-danger"><br>valid range is [0,100]</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" min="0" max="100" required>
                    </div>

                    <div class="mb-2">
                        <label for="quantity" class="form-label" @mouseover="explain('annual_performance_degradation')" @mouseleave="dontExplain">Anuual Performance Degradation* %: <span v-if="annual_performance_degradation>100 || annual_performance_degradation<0" class="text-danger"> <br>  valid range is [0,100]</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" min="0" max="100" required>
                    </div>
                    
                    <!-- ... Sheet Type ... -->
                    <div class="mb-2">
                        <label for="EOL_ACTION" class="form-label">EOL ACTION*:</label>
                        <select id="EOL_ACTION" v-model="replace_or_die" class="custom-select" required>
                            <option value="replace">replace</option>
                            <option value="die">die</option>
                        </select>
                    </div>

                    <!-- ... Repeat the pattern for other form elements ... --> 
                    <div class="mb-2" >
                        <label for="bibliography" style="display:block;">Bibliography:</label>
                        <textarea id="bibliography" v-model="bibliography" rows="2" cols="30" placeholder="Add bibliography links or other sources"></textarea>
                    </div>

                    <div class="mb-2">
                        <label for="description" style="display:block;">Description:</label>
                        <textarea id="description" v-model="description" rows="2" cols="30"  placeholder="fulfill with usefull info about the Component"></textarea>
                    </div>
                    
                
                
                    <!-- ... Repeat the pattern for other form elements ... -->       
            </div>
        </form>
    </div>
    </div>
</div>

</template>

<script>
import { axios } from "@/common/api.service.js";
import {TARGET_IP} from "@/common/request_configs.js"
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
        explanationMode:false,
        showSubtype:true
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
            dataObject.opex_per_capex/=100;
            dataObject.major_upgrade_share/=100;
            dataObject.annual_performance_degradation/=100;
            const {data} = await axios.post(`${TARGET_IP}/api/component/`,dataObject)
                alert("Success")
                this.$router.push({ name:'ListComponents'}); //here add the router name from router/index.js
            }catch(error){
                dataObject.opex_per_capex*=100;
                dataObject.major_upgrade_share*=100;
                dataObject.annual_performance_degradation*=100;
                console.log(error)
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
  mounted(){
    (function() {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
            }, false);
        });
        })();
  },
  watch: {
    SHEET_TYPE(newValue) {
        if( newValue=="El. Generators" || newValue=="Thermal Sources" || newValue=='PCM' || newValue=='Ventilation'){
            this.ugs_header = 'kW'
            this.showSubtype=true;
        }else if(newValue=="Water Storage"){
            this.ugs_header='Litre'
            this.showSubtype=true;
        }
        else if(newValue=='El. Storage'){
            this.ugs_header='kWh'
            this.showSubtype=true;
        }
        else if(newValue=='Insulation'){
            this.ugs_header='m\u00B3'
            this.showSubtype=true;
        }
        else if(newValue=='Glazing'){
            this.ugs_header='m\u00B2'
            this.showSubtype=true;
        }
        else if(newValue=='Other'){
            this.ugs_header='UGS'
            this.showSubtype=true;
        }
        if(newValue=='Ventilation'){
            this.showSubtype=false;
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
    position: relative;
    width: 140%;
    background-color: aliceblue;
    border: 2px solid lightsteelblue;
    display: flex;
    justify-content: space-evenly;
    border-radius: 1%;
    height: 100%;
   
}
/* Apply different styles for smaller viewports */



.explanation{
margin-left: 4%;
position:fixed;
width:20%;
background-color: palegreen;
}

.mb-2{
width: 60%;
}

#w3review{
text-align:left;
}
#group2{
    margin-right: -18%;
  }

#bibliography{
width:100%;
}
#description{
width:100%;
}

.form-photo{
width: 80%;
display: flex;
justify-content: space-around;
}

#tech_image{
width:400px;
}
.directives{
margin-left:50px;
position:relative;
top:400px;
height:50%;
z-index: -1;
}
.directives p{
margin-bottom:0px;
}

@media (max-width: 1000px){
.directives{
    display: none;
}
.form-photo{
    width:70%;
}
#component{
    width:100%;
    position:relative;
    left:28%;
}

}

</style>

    
