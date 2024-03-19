<template>
    <div container>
    <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
    <div class="col-6">
        <p><strong>All fields with * are Mandatory</strong></p>       
            <div class="mb-2 mt-3">
                <label for="name" class="form-label">Name*:</label>
                <input type="text" class="form-control" id="name" v-model="name">
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
                    <option value="El. Storage">Electrical Storage</option>
                    <option value="Other">Other</option>
                </select>
            </div>

                           <!-- Add types -----------------------------------------------------------------------------> 
                           <div class="mb-1" id="options">
                        <div id="options" v-if="SHEET_TYPE=='Thermal Sources'">
                            <label for="type" class="form-label">Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="boiler">boiler</option>
                            <option value="heatpump">heatpump</option>
                            <option value="air_conditioning">aircondition</option>
                            <option value="solar">solar thermal panel</option>
                            <option value="district_heating">district heating </option>
                            <option value="geo">geo thermal</option>
                            <option value="fan">fan coil </option>

                        </select>
                        </div>

                        <div id="options" v-if="SHEET_TYPE=='El. Generators'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="pv">photovoltaic panel</option>
                            <option value="wind">wind turbine</option>
                        </select>
                        </div>


                        <div id="options" v-if="SHEET_TYPE=='Insulation'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="building_insulation">building insulation</option>
                            <option value="dhw_insulation">water tank insulation</option>
                        </select>
                        </div>

                        <div id="options" v-if="SHEET_TYPE=='PCM'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="pcm">phase change material standard</option>
                        </select>
                        </div>

                        <div id="options" v-if="SHEET_TYPE=='Water Storage'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="hot_water">water storage tank</option>
                        </select>
                        </div>

                        <div id="options" v-if="SHEET_TYPE=='El. Storage'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="li_on">battery Li-ion </option>
                            <option value="lead_acid">battery lead acid</option>
                            <option value="flow">battery flow</option>
                        </select>
                        </div>

                        <div id="options" v-if="SHEET_TYPE=='Glazing'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="frame"> frame </option>
                            <option value="glass"> glass </option>
                        </select>
                        </div>


                        <div id="options" v-if="SHEET_TYPE=='Ventilation'">
                            <label for="type" class="form-label" >Component Type* :</label><br>
                            <select id="type" v-model="component_type" required>
                            <option value="mixing_ventilation"> mixing ventilation </option>
                            <option value="displacement_ventilation"> displacement ventilation </option>
                            <option value="stratum_ventilation"> stratum ventilation </option>
                            <option value="natural_ventilation"> natural ventilation </option>
                            <option value="micro_ventilation">micro ventilation</option>
                            </select>
                        </div>


                    </div>

                    <!-- subtypes -->
                    <div id="options" class="mb-1" v-if="showSubtype && component_type=='boiler' && SHEET_TYPE=='Thermal Sources' "> 
                        <label for="type" class="form-label" id="subtype_element" >Fuel :</label><br>
                        <select  id="type" v-model="component_subtype" required>
                            <option value="ngas">  natural gas </option>
                            <option value="diesel"> diesel  </option>
                            <option value="biomass"> biomass </option>
                            <option value="oil"> oil  </option>
                            <option value="lpg"> lpg </option>
                            </select>
                    </div>  
                    <div  v-else-if="showSubtype" class="mb-1">
                        <label for="type" class="form-label" id="subtype_element">Component Subtype* :</label>
                        <input type="text" class="form-control" id="type" v-model="component_subtype" required>
                    </div>

            <!-- Add Numerics -----------------------------------------------------------------------------> 


            <div class="mb-2">
                <label for="quantity" class="form-label">CAPEX/UGS*:<strong>[€/{{ ugs_header }}]</strong>:<span v-if="capex_per_ugs<0" class="text-danger"> <br> valid value is non negative</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="capex_per_ugs" required min="0" >
            </div>
            
            <div class="mb-2">
                <label for="quantity" class="form-label"><span>ANNUAL MAINTENANCE[%CAPEX]*:</span>  <span v-if="opex_per_capex>100 || opex_per_capex<0" class="text-danger"> <br> valid range is [0,100]</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" required min="0" max="100">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Embodied CO2/UGS* <strong>[kgCO2/{{ ugs_header }}]</strong>:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" required min="0">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Embodied Pe/UGS* <strong>[GJ/{{ ugs_header }}]</strong>:<span v-if="embodied_pe_per_ugs<0" class="text-danger"><br> valid value is non negative</span> </label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" required min="0">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Component Lifetime[years]*:<span v-if="lifetime<0" class="text-danger"><br> valid value is non negative</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" required min="0">
            </div>

            <div class="mb-2 form-check">
                <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="false">
                <label class="form-check-label" for="isMainInventory">TO ADD AT MAIN INVENTORY*</label>
            </div>


            <button type="submit" id="submitbtn" class="btn btn-primary">Update Component*</button>

        </div>
        <div class="col-6" id="group2">

            <div class="mb-2">
                <label for="quantity" class="form-label">Pref Cost* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" required min="0">
            </div>
            <div class="mb-2">
                <label for="quantity" class="form-label">Pref Env* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_env<0" class="text-danger"><br> valid value is non negative</span><br></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" required min="0">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Scale Cost*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Scale Env*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Major Upgrade Point*[years]:<span v-if="major_upgrade_point<0" class="text-danger"><br> valid value is non negative</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" required min="0">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Major Upgrade Share*[%100]: <span v-if="major_upgrade_share>100 || major_upgrade_share <0" class="text-danger"> <br> valid range is [0,100]</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" required min="0" max="100">
            </div>

            <div class="mb-2">
                <label for="quantity" class="form-label">Anuual Performance Degradation*[%100]: <span v-if="annual_performance_degradation>100 || annual_performance_degradation<0" class="text-danger"> <br> valid range is [0,100]</span></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" required min="0" max="100">
            </div>
            
            <!-- ... Sheet Type ... -->
            <div class="mb-2">
                <label for="EOL_ACTION" class="form-label">EOL ACTION:</label>
                <select id="EOL_ACTION" v-model="replace_or_die" class="custom-select">
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

</template>
<script>
import { axios } from "@/common/api.service.js";
import {TARGET_IP} from "@/common/request_configs.js"
export default {
  name: 'UpdateComponent',
  data(){
    return{
        ID: null,
        name:null,
        component_type:null, 
        component_subtype:null, 
        capex_per_ugs:null,
        opex_per_capex:null, 
        embodied_co2_per_ugs:null, 
        embodied_pe_per_ugs:null, 
        lifetime: null,
        pref_cost: null,
        pref_env: null,
        scale_cost:null, 
        scale_env: null,
        major_upgrade_point:null, 
        major_upgrade_share:null, 
        annual_performance_degradation:null, 
        replace_or_die:null, 
        SHEET_TYPE:null, 
        IS_MAIN_INVENTORY:null, 
        bibliography:null,
        description:null,
        showSubtype:true,
        ugs_header:null,
        component:{}
    } 
  },
  async created(){

    try {
            console.log("inside created")
            let response = await axios.get(`${TARGET_IP}/api/component/${this.$route.params.id}/`);
            console.log("inside created after axios request")
            this.component = response.data;
            console.log("successfully fetched", response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }

    this.ID = this.component.id
    this.name = this.component.name
    this.component_type =  this.component.component_type
    this.component_subtype =  this.component.component_subtype
    this.capex_per_ugs =  this.component.capex_per_ugs
    this.opex_per_capex =  this.component.opex_per_capex * 100
    this.embodied_co2_per_ugs =  this.component.embodied_co2_per_ugs
    this.embodied_pe_per_ugs = this.component.embodied_pe_per_ugs
    this.lifetime =  this.component.lifetime
    this.pref_cost =  this.component.pref_cost
    this.pref_env =  this.component.pref_env
    this.scale_cost =  this.component.scale_cost
    this.scale_env =  this.component.scale_env
    this.major_upgrade_point =  this.component.major_upgrade_point
    this.major_upgrade_share =  this.component.major_upgrade_share *100
    this.annual_performance_degradation =  this.component.annual_performance_degradation *100
    this.replace_or_die =  this.component.replace_or_die
    this.SHEET_TYPE =  this.component.SHEET_TYPE
    this.IS_MAIN_INVENTORY =  this.component.IS_MAIN_INVENTORY
    this.bibliography = this.component.bibliography
    this.description = this.component.description
    if(this.component.SHEET_TYPE==='Ventilation'){
        this.showSubtype=false;
    }
    console.log("inside:",this.component)
  },
  methods:{
    async handleSubmit(){ 
        const dataObject = this.$data;
        try{
            dataObject.opex_per_capex/=100
            dataObject.annual_performance_degradation/=100
            dataObject.major_upgrade_share/=100
            const {data} = await axios.put(`${TARGET_IP}/api/component/${this.ID}/`,dataObject)
                alert("Success")
                this.$router.push({ name:'ListComponents'}); //here add the router name from router/index.js
            }catch(error){
                dataObject.opex_per_capex*=100;
                dataObject.major_upgrade_share*=100;
                dataObject.annual_performance_degradation*=100;
                console.log(error)
                alert("Error")
        }
        
    }
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

 
<style scoped >

h1{
        text-align: center;
    }
    #component {
        width: 50%;
        background-color: aliceblue;
        border: 2px solid lightsteelblue;
        display: flex;
        justify-content: space-evenly;
        border-radius: 1%;
    
    }
    /* Apply different styles for smaller viewports */
  @media (max-width: 1000px) { 
  }
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

  #submitbtn{
    margin-bottom: 4px;
  }

  #type{
    width:60%
}

.custom-select{
    width: 100%;
}


</style>
