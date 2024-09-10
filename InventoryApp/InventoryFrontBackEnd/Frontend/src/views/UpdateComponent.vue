<template>

    <div class="container">
    
    <div class="form-photo">

        <!--
            <div class="col-12">
                <h3>Find a Good Header ..</h3>
            </div>
        <hr>
        -->

        <div  @submit.prevent="handleSubmit">
            <form class="input-form row mt-4 needs-validation myform" ref="anyName" novalidate> 

                        <div class="mt-3">
                            <h5><b>1. Add the basic attributes to update the component:</b></h5>
                        </div>
                        
                        <div v-if="is_admin"  class="row">
                            <div class="col">
                                <label class="form-label" for="isMainInventory">Is Default Component</label>
                                <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="false">
                            </div>
                        </div>

                        <!-- Add Name -->
                        <div class="col-12" style="margin: 0 auto;">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" title="It is Important to give a formated name e.g: for the Rehouse Project at Greek Demo, a heatpump named Psyctotherm would named: Rehouse_Greek_Heatpump_Psyctotherm "></i>
                                <label for="name" class="form-label">Name*:</label>
                                <input type="text" class="form-control" id="name" v-model="name" placeholder="format: Project_Demo_Building_Name" required>
                        </div>
                        
                                              
<!-- common section  -->
                    <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3">
                            <h5><b>2. Add common fields:</b></h5>
                    </div>

                    <div class="row">
                        <div class="col-4">
                                <label for="quantity" class="form-label">Component Lifetime* <strong>[Years]:</strong><span v-if="lifetime<0" class="text-danger"><br> valid value is non negative</span></label>
                                <input type="number" step="1" class="form-control"  id="quantity" v-model="lifetime" oninput="this.value|=0"  min="0" required>
                        </div>

                        <div class="col-4">    
                            <label for="quantity" class="form-label">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['major_upgrade_point']"></i>
                                Major Upgrade Point* <strong> 
                                [Years]:</strong><span v-if="major_upgrade_point<0" class="text-danger"><br> valid value is non negative</span></label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" min="0" placeholder="For No Replacement put : 1000" required>
                        </div>

                        <div class="col-4">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['major_upgrade_share']"></i>
                                    Major Upgrade Share* <strong>[CAPEX%]:</strong> <span v-if="major_upgrade_share>100 || major_upgrade_share<0" class="text-danger"><br>valid range is [0,100]</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" min="0" max="100" required >
                        </div>
                    </div>

                    <div class="col-4 mt-3">
                        <label for="quantity" class="form-label">
                        <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['annual_performance_degradation']"></i>
                                    Annual Performance Degradation[%]*: <span v-if="annual_performance_degradation>100 || annual_performance_degradation<0" class="text-danger"> <br>  valid range is [0,100]</span></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" min="0" max="100" required>
                    </div>

                    <div class="col-4 mt-3">
                        <label for="quantity" class="form-label">
                            <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['OPEX_PER_CAPEX']"></i>
                                    Annual Maintenance <strong>[CAPEX%]:</strong> <span v-if="opex_per_capex>100 || opex_per_capex<0" class="text-danger"> <br> valid range is [0,100]</span></label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" min="0" max="100" required>
                    </div>


<!--sources section-->
                    <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3">
                            <h5><b>3. Add Description and Sources:</b></h5>
                    </div>

                        <div class="col-6">     
                                <label for="description" style="display:block;">Description:</label>
                                <textarea id="description" v-model="description" rows="2" cols="30"  placeholder="fulfill with usefull info about the Component"></textarea>
                        </div>

                        <div class="col-6">
                            <label for="bibliography" style="display:block;">Bibliography:</label>
                            <textarea id="bibliography" v-model="bibliography" rows="2" cols="30" placeholder="Add bibliography links or other sources"></textarea>
                        </div>

<!--add related components with Capex - embodied CO2 - embodied Pe -->
                    
                    <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3">
                        <h5 v-if="IS_MAIN_INVENTORY"><b>4. Add  CAPEX - Embodied CO2 per FU - Embodied Primary Energy per FU:</b></h5>
                        <h5 v-else><b>4. Add  Embodied CO2 - Embodied Primary Energy:</b></h5>
                     
                        
                        <ul v-if="IS_MAIN_INVENTORY">
                          <li>CAPEX of the component divided by overall installed magnituded </li>
                          <li>Embodied CO2 of the component divided by overall installed magnituded</li>
                          <li>Embodied Primary Energy of the component divided by overall installed magnituded</li>
                        </ul>
                        <ul v-else>
                          <li>Embodied CO2 of the component</li>
                          <li>Embodied Primary Energy of the component</li>
                        </ul>  
                    
                    </div>

                       
                        <div v-if="IS_MAIN_INVENTORY" class="col-6 mt-3">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['CAPEX/UGS']"></i>
                                    CAPEX/UGS*<strong>[€/{{ ugs_header }}]</strong>:<span v-if="capex_per_ugs<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control"  id="validationCustom01" v-model="capex_per_ugs" min="0" required>
                        </div>
                        

                        
                        <div class="col-6">
                                <label for="quantity" class="form-label mt-3" >
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['embodied_co2_per_ugs']"></i>
                                    <span v-if="IS_MAIN_INVENTORY">
                                    Embodied CO2/UGS* <strong>[kgCO2/{{ ugs_header }}]</strong>:
                                    </span>
                                    <span v-else>
                                    Embodied CO2* <strong>[kgCO2]</strong>:
                                    </span>
                                </label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" required>
                        </div>


                        <div class="col-6">
                            <label for="quantity" class="form-label mt-3">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['embodied_pe_per_ugs']"></i>
                                <span v-if="IS_MAIN_INVENTORY">
                                Embodied Pe/UGS* <strong>[GJ/{{ ugs_header }}]</strong>:
                                </span>
                                <span v-else>
                                Embodied Pe* <strong>[GJ]</strong>:
                                </span>
                                <span v-if="embodied_pe_per_ugs<0" class="text-danger"><br> valid value is non negative</span>
                            </label>
                            <input type="number" step="any" class="form-control" id="quantity" v-model="embodied_pe_per_ugs" min="0" required>
                        </div>

<!--add eol attributes-->
                        <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                        <div class="mt-3">
                            <h5><b>5. Add environmental end of life attributes:</b></h5>
                            <p>-In this section attributes about EoL are added for the component,<br>
                            </p>
                        </div>
                        <div class="col-4 mt-3">
                            <label for="quantity" class="form-label"> <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['eol_co2_cost']"></i> 
                            EoL CO2 cost* <strong> [KgCO2] </strong>:<span v-if="eol_co2_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="eol_co2_cost" min="0" required>
                        </div>

                            <div class="col-4 mt-3">
                            <label for="quantity" class="form-label"> <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['eol_pe_cost']"></i> 
                            EoL Primary Energy cost* <strong> [Gj] </strong>:<span v-if="eol_pe_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="eol_pe_cost" min="0" required>
                        </div>

                        <div class="col-4 mt-3">
                        <label for="EOL_ACTION" class="form-label">EoL Action*:</label>
                        <select id="EOL_ACTION" v-model="replace_or_die" class="custom-select" required>
                            <option value="replace">replace</option>
                            <option value="die">die</option>
                        </select>
                    </div>

<!--add regression attributes if is a default component-->

                <div v-if="IS_MAIN_INVENTORY" class="regression">
                <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3" >
                        <h5><b>6. Add Regression Attributes:</b></h5>
                        <p>-In this section attributes are added for Default components,<br>
                            that have been calculated for many values with SimaPro or another source and will be used using scaling</p>
                    </div>
                    <div class="row">
                    <div class="col-3">
                        <label for="quantity" class="form-label"> <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['pref_cost']"></i> 
                        Pref Cost* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" min="0" required>
                    </div>

                    <div class="col-3">
                            <label for="quantity" class="form-label">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['pref_env']"></i> Pref Env*
                                <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_env<0" class="text-danger"><br> valid value is non negative</span><br></label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" min="0" required>
                    </div>

                    <div class="col-3">
                        <label for="quantity" class="form-label">
                            <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['scale_env']"></i>
                            Scale Env*:</label>
                        <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env"  required>
                    </div>

                    <div class="col-3">
                        <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['scale_cost']"></i>
                            <label for="quantity" class="form-label">Scale Cost*:</label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost"  required>
                        </div>
                    </div> <!--end row-->
                    </div>

         

<!-- add extra element which are non common-->

                    <!--for glazing-->
                    <div v-if="SHEET_TYPE=='Glazing'" class="row mb-2">
                        
                        <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                        <div class="mt-3">
                            <h5><b>Add some extra attributes which are not common to all components (technology specific):</b></h5>
                        </div>

                            <div v-if="component_type=='glass' ||component_type=='frame' " class="col-6">
                                <label for="quantity" class="form-label thermals">U-value <strong>[W/(m&sup2;K)]</strong>:<span v-if="uvalue<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control thermals"  id="validationCustom01" v-model="uvalue" min="0" required>
                            </div>
                            <div v-if="component_type=='glass'" class="col-6">
                                <label for="quantity" class="form-label thermals">G-value :<span v-if="gvalue<0 || gvalue>1" class="text-danger"> <br> valid range is (0,1)</span></label>
                                <input type="number" step="any" class="form-control thermals"  id="validationCustom01" v-model="gvalue" min="0" required>
                            </div>
                            <div v-else-if="component_type=='frame'"  class="col-6">
                                <label for="quantity" class="form-label thermals">G-value :<span v-if="gvalue<0 || gvalue>1" class="text-danger"> <br> valid range is (0,1)</span></label>
                                <input type="number" step="any" class="form-control thermals"  style="background-color:grey" id="validationCustom01" value="not required"  readonly placeholder="not required">
                            </div>
                    </div>

                    <!--for insulation-->
                    <div class="row mb-1" v-if="SHEET_TYPE=='Insulation'">
                        <div class="mt-3">
                            <h5><b>Add some extra attributes which are not common to all components (technology specific):</b></h5>
                        </div>
                            <div class="col-4">
                                <label for="quantity" class="form-label thermals">Density<strong>[Kg/m&sup3;]</strong>:<span v-if="density<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control thermals"  id="validationCustom01" v-model="density" min="0">
                            </div>
                            <div class="col-4">
                                <label for="quantity" class="form-label thermals">Specific Heat Capacity<strong>[J/(Kg&middot;K)]</strong>:<span v-if="capacity<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control thermals"  id="validationCustom01" v-model="capacity" min="0">
                            </div>
                            <div class="col-4">
                                <label for="quantity" class="form-label thermals">Thermal Conductivity<strong>[W/(m&middot;K)]</strong>:<span v-if="conductivity<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control thermals"  id="validationCustom01" v-model="conductivity" min="0">
                            </div>
                    </div>

<!--sumbit button-->

                    <div class="col-2 mt-2">
                        <button type="submit" id="sumbit-button" class="btn btn-primary mb-2">Update Component</button>
                    </div>


                      
            </form>
        </div>
    </div>
</div>

</template>
<script>
import { axios } from "@/common/api.service.js";
import { TARGET_IP } from "@/common/request_configs.js";
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
        density:null,
        capacity:null,
        conductivity:null,
        uvalue:null,
        gvalue:null,
        IS_B_COMPONENT:null,
        eol_pe_cost:null,
        eol_co2_cost:null,
        component:{}, explain_dict:{
            "type":'Is the Components type e.g.  Heatpump',
            "subtype":'Is the Components subtype e.g. for a Heatpump a subtype would be: water to water',
            "installed_ugs":'Is the Components installed Nominal Magnitude e.g. for Heatpump is the nominal power to kwh ',
            "CAPEX/UGS":'This parameter is the ratio of a the CAPEX/UGS for the reference component that is considered for this analysis e.g. Heatpumps cost=100 € and nominal power (installed UGS) = 10kW ==>  CAPEX/UGS=10[€/kW]',
            'OPEX_PER_CAPEX':'This parameter gives the ratio of components yearly maintenance according to its CAPEX. e.g. if this ratio=10% then considering that Heatpump costs 100€ every year maintenance cost is 10€ ',
            'embodied_co2_per_ugs':'This parameter gives the ratio of embodied CO2[kg]/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied CO2=100 kg and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[kgCO2/kWh] ',
            'embodied_pe_per_ugs':'This parameter gives the ratio of embodied Primary/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied Pe=100 GJ and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[GJ/kWh] ',
            'scale_cost':'exponent for power-scaling the input values to match the size of the user-input(monetery). ',
            'scale_env':'exponent for power-scaling the input values to match the size of the user-input (environmental).',
            'major_upgrade_point':'Is time interval that major upgrades for the component occur, e.g. for a heatpump if the major upgrade point is 5 years, every 5 years major upgrade occur for this component.',
            'major_upgrade_share':'Is the % Percentage of CAPEX to calculate the cost of a major upgrade.',
            'annual_performance_degradation':'Annual drop of performance',
            'pref_env':'is the nominal installed UGS for the reference component of the analysis(environmental) e.g for a heatpump would be 10[kW]',
            'pref_cost':'is the nominal installed UGS for the reference component of the analysis(monetery) e.g for a heatpump would be 8[kW]',
            'MAIN_INVENTORY':'When a component is not project specific is added at main inventory e.g. there is need to have a generalized Heatpump water to water at Verify inventory.'
        }
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
    this.IS_B_COMPONENT = this.component.IS_B_COMPONENT
    this.eol_co2_cost = this.component.eol_co2_cost
    this.eol_pe_cost = this.component.eol_pe_cost

    
    if(this.component.thermal_properties!=null  && this.component.thermal_properties.hasOwnProperty("conductivity")){
        this.capacity = this.component.thermal_properties.capacity
        this.density  = this.component.thermal_properties.density
        this.conductivity = this.component.thermal_properties.conductivity
    }

    if(this.component.thermal_properties!=null && this.component.thermal_properties.hasOwnProperty("gvalue")){
        this.gvalue = this.component.thermal_properties.gvalue
    }

    if(this.component.thermal_properties!=null && this.component.thermal_properties.hasOwnProperty("uvalue")){
        this.uvalue = this.component.thermal_properties.uvalue
    }

    if(this.component.SHEET_TYPE==='Ventilation'){
        this.showSubtype=false;
    }
    console.log("inside:",this.component)
  },
  methods:{
    async handleSubmit(){ 
        const dataObject = this.$data;
        try{

            if(this.SHEET_TYPE==='Insulation'){
                dataObject['thermal_properties'] = {'conductivity':this.conductivity,
                                                    'density':this.density,
                                                    'capacity':this.capacity}
            }

            if(this.SHEET_TYPE=='Glazing'){
                dataObject['thermal_properties'] = {'uvalue':this.uvalue,
                                                    'gvalue':this.gvalue}
            }
          

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
            this.showSubtype=false;
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

/* Apply different styles for smaller viewports */



.explanation{
margin-left: 4%;
position:fixed;
width:20%;
background-color: #1089ff;
color:#F7F7F7;
display:none;
}



#w3review{
text-align:left;
}


#bibliography{
width:100%;
}
#description{
width:100%;
}

.container{}

.form-photo{
    margin:0 auto;
    width:90%;
}


.directives{
margin-left:50px;
position:relative;
top:400px;
height:50%;
}
.directives p{
    margin-bottom:0px;
}


#sumbit-button{
    position: relative;
    bottom: -5%;
}

#type{
    width:100%
}

.custom-select{
    width: 100%;
}

.thermals{
}
.thermals-properties{
    width:50%;
}

label{
    
}

input{
    
}

#mandatory{
    display: flex;
    justify-content: end;
}

#tooltip-explain{
    size: 15px;
}

.myform{
    border: solid 0.75px lavender;
}

hr{
    height: 5px;
}


input, select, textarea {
  background-color: #ffffff; /* White input background */
  border: 1px solid #ced4da; /* Medium gray border */
}

#sumbit-button:hover {
  background-color: #0b5ed7; /* Darkened primary color for hover */
}

h5{
    color:cornflowerblue;
}



</style>
