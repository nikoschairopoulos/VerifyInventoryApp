<template>
    <div container>
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
                <label for="type" class="form-label">Component Type:</label>
                <input type="text" class="form-control" id="type" v-model="component_type">
            </div>

            <div class="mb-3">
                <label for="type" class="form-label">Component Subtype:</label>
                <input type="text" class="form-control" id="type" v-model="component_subtype">
            </div>

            <!-- Add Numerics -----------------------------------------------------------------------------> 

            <div class="mb-3">
                <label for="quantity" class="form-label">installed_ugs: <strong>{{ ugs_header }}</strong></label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="installed_ugs" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">CAPEX/UGS:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="capex_per_ugs" min="0">
            </div>
            
            <div class="mb-3">
                <label for="quantity" class="form-label">OPEX_PER_CAPEX[%100]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Embodied CO2/UGS:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Embodied Pe/UGS:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Component Lifetime[years]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" min="0">
            </div>

            <button type="submit" class="btn btn-primary">Update Component</button>

        </div>
        <div class="group2">

            <div class="mb-3">
                <label for="quantity" class="form-label">Pref Cost:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" min="0">
            </div>
            <div class="mb-3">
                <label for="quantity" class="form-label">Pref Env:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Scale Cost:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Scale Env:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Major Upgrade Point[years]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Major Upgrade Share[%100]:</label>
                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" min="0">
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">Anuual Performance Degradation[%100]:</label>
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

            <div class="mb-3 form-check">
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
  name: 'UpdateComponent',
  props:['header','component'],
  data(){
    return{
        ID: this.component.id,
        name: this.component.name,
        component_type: this.component.component_type,
        component_subtype: this.component.component_subtype,
        installed_ugs: this.component.installed_ugs,
        capex_per_ugs: this.component.capex_per_ugs,
        opex_per_capex: this.component.opex_per_capex,
        embodied_co2_per_ugs: this.component.embodied_co2_per_ugs,
        embodied_pe_per_ugs: this.component.embodied_pe_per_ugs,
        lifetime: this.component.lifetime,
        pref_cost: this.component.pref_cost,
        pref_env: this.component.pref_env,
        scale_cost: this.component.scale_cost,
        scale_env: this.component.scale_env,
        major_upgrade_point: this.component.major_upgrade_point,
        major_upgrade_share: this.component.major_upgrade_share,
        annual_performance_degradation: this.component.annual_performance_degradation,
        replace_or_die: this.component.replace_or_die,
        SHEET_TYPE: this.component.SHEET_TYPE,
        IS_MAIN_INVENTORY: this.component.IS_MAIN_INVENTORY,
        bibliography:this.component.bibliography,
        description:this.component.description
    } 
  },
  mounting(){
        console.log("inside:",this.component)
    },
  methods:{
    async handleSubmit(){ 
        const dataObject = this.$data;
        try{
            const {data} = await axios.put(`http://127.0.0.1:8000/api/component/${this.ID}/`,dataObject)
                alert("Success")
                this.$router.push({ name:'Home'}); //here add the router name from router/index.js
            }catch(error){
                console.log(error)
                alert("Error")
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
        border-radius: 2%;
    
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
  </style>


    
