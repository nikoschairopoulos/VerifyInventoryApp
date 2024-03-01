<template>
    <div container>
    <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
    <div class="col-6">
        <p><strong>All fields with * are Mandatory</strong></p>       
            <div class="mb-3 mt-3">
                <label for="name" class="form-label">Name*:</label>
                <input type="text" class="form-control" id="name" v-model="name">
            </div>
            <div class="mb-3">
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

            <div class="mb-3">
                <label for="type" class="form-label">Component Type*:</label>
                <input type="text" class="form-control" id="type" v-model="component_type" required>
            </div>

            <div v-if="showSubtype"  class="mb-3">
                <label for="type" class="form-label">Component Subtype*:</label>
                <input type="text" class="form-control" id="type" v-model="component_subtype" required>
            </div>

            <!-- Add Numerics -----------------------------------------------------------------------------> 


            <div class="mb-3">
                <label for="quantity" class="form-label">CAPEX/UGS*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="capex_per_ugs" required min="0" >
            </div>
            
            <div class="mb-3">
                <label for="quantity" class="form-label">OPEX_PER_CAPEX*[%100]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" required min="0" max="100">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Embodied CO2/UGS*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Embodied Pe/UGS*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Component Lifetime[years]*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" required min="0">
            </div>

            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="false">
                <label class="form-check-label" for="isMainInventory">TO ADD AT MAIN INVENTORY*</label>
            </div>


            <button type="submit" class="btn btn-primary">Update Component*</button>

        </div>
        <div class="col-6" id="group2">

            <div class="mb-3">
                <label for="quantity" class="form-label">Pref Cost*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" required min="0">
            </div>
            <div class="mb-3">
                <label for="quantity" class="form-label">Pref Env*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Scale Cost*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Scale Env*:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Major Upgrade Point*[years]</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" required min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Major Upgrade Share*[%100]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" required min="0" max="100">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Anuual Performance Degradation*[%100]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" required min="0" max="100">
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

           
            
            
    </div>
</form>
</div>

</template>
<script>
import { axios } from "@/common/api.service.js";
import {TARGET_IP} from "@/common/request_configs.js"
export default {
  name: 'UpdateComponent',
  props:['header','component'],
  data(){
    return{
        ID: this.component.id,
        name: this.component.name,
        component_type: this.component.component_type,
        component_subtype: this.component.component_subtype,
        capex_per_ugs: this.component.capex_per_ugs,
        opex_per_capex: this.component.opex_per_capex * 100,
        embodied_co2_per_ugs: this.component.embodied_co2_per_ugs,
        embodied_pe_per_ugs: this.component.embodied_pe_per_ugs,
        lifetime: this.component.lifetime,
        pref_cost: this.component.pref_cost,
        pref_env: this.component.pref_env,
        scale_cost: this.component.scale_cost,
        scale_env: this.component.scale_env,
        major_upgrade_point: this.component.major_upgrade_point,
        major_upgrade_share: this.component.major_upgrade_share *100,
        annual_performance_degradation: this.component.annual_performance_degradation *100,
        replace_or_die: this.component.replace_or_die,
        SHEET_TYPE: this.component.SHEET_TYPE,
        IS_MAIN_INVENTORY: this.component.IS_MAIN_INVENTORY,
        bibliography:this.component.bibliography,
        description:this.component.description,
        showSubtype:true
    } 
  },
  mounted(){
    console.log("UPDATE COMPONENT")
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
                //this.$router.push({ name:'ListComponents'}); //here add the router name from router/index.js
                location.reload();
            }catch(error){
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

 
<style >

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

  .mb-3{
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


</style>
