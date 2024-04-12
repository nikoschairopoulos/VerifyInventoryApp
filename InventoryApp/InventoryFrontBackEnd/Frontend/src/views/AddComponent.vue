<template>

    <div container>
    
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
                <div class="container">

                    <div class="row mt-1">
                        <div class="col-6">
                            <div class="mb-1">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" title="It is Important to give a formated name e.g: for the Rehouse Project at Greek Demo, a heatpump named Psyctotherm would named: Rehouse_Greek_Heatpump_Psyctotherm "></i>
                                <label for="name" class="form-label">Name*:</label>
                                <input type="text" class="form-control" id="name" v-model="name" placeholder="format: Project_Demo_Building_Name" required>
                            </div>
                        </div>


                        <div class="col-6">
                            <div class="mb-1">
                               
                                <label for="quantity" class="form-label"> <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['pref_cost']"></i> 
                                Pref Cost* <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_cost<0" class="text-danger"><br> valid value is non negative</span><br></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_cost" min="0" required>
                            </div>
                        </div>
                    </div>


                    <div class="row">
                        <div class="col-6">
                            <div class="mb-1">
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
                        </select>
                    </div>
                        </div>

                            <div class="col-6">
                                <div class="mb-1">
                                    <label for="quantity" class="form-label">
                                        <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['pref_env']"></i> Pref Env*
                                         <strong> [{{ ugs_header }}]</strong>:<span v-if="pref_env<0" class="text-danger"><br> valid value is non negative</span><br></label>
                                    <input type="number" step="any" class="form-control"  id="quantity" v-model="pref_env" min="0" required>
                                </div>
                            </div>
                        </div>


                        <div class="row">
                        <div class="col-6">
                           <!--Add types-----------------------------------------------------------------------------> 
                                <div id="options" v-if="SHEET_TYPE==null">
                                    <label for="type" class="form-label">
                                        Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                    </select>
                                </div>
                                <div class="mb-1" id="options">
                                    <div id="options" v-if="SHEET_TYPE=='Thermal Sources'">
                                        <label for="type" class="form-label">
                                            Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="boiler">boiler</option>
                                        <option value="heat_pump">heatpump</option>
                                        <option value="air_conditioning">aircondition</option>
                                        <option value="solar">solar thermal panel</option>
                                        <option value="district_heating">district heating </option>
                                        <option value="geo">geo thermal</option>
                                        <option value="fan">fan coil </option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='El. Generators'">
                                        <label for="type">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="pv">photovoltaic panel</option>
                                        <option value="wind">wind turbine</option>
                                    </select>
                                    </div>

                                    <div id="options" v-if="SHEET_TYPE=='Insulation'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="building_insulation">building insulation</option>
                                        <option value="dhw_insulation">water tank insulation</option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='PCM'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="pcm">phase change material standard</option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='Water Storage'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="hot_water">water storage tank</option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='El. Storage'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="li_ion">battery Li-ion </option>
                                        <option value="lead_acid">battery lead acid</option>
                                        <option value="flow">battery flow</option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='Glazing'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="frame"> frame </option>
                                        <option value="glass"> glass </option>
                                    </select>
                                    </div>
                                    <div id="options" v-if="SHEET_TYPE=='Ventilation'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="mixing_ventilation"> mixing ventilation </option>
                                        <option value="displacement_ventilation"> displacement ventilation </option>
                                        <option value="stratum_ventilation"> stratum ventilation </option>
                                        <option value="natural_ventilation"> natural ventilation </option>
                                        <option value="micro_ventilation">micro ventilation</option>
                                        </select>
                                    </div>
                                </div>
                        </div>
                        <div class="col-6">
                            <div class="mb-1"> 
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['scale_env']"></i>
                                    Scale Env*:</label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_env"  required>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-6">
                            <div id="options" class="mb-1" v-if="showSubtype && component_type=='boiler' && SHEET_TYPE=='Thermal Sources' "> 
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" title="this is a test"></i>
                            <label for="type" class="form-label" id="subtype_element">Component Subtype (Fuel) :</label><br>
                            <select  id="type" v-model="component_subtype" required>
                            <option value="ngas">  natural gas </option>
                            <option value="diesel"> diesel  </option>
                            <option value="biomass"> biomass </option>
                            <option value="oil"> oil  </option>
                            <option value="lpg"> lpg </option>
                        </select>
                        </div>
                        <div  v-else-if="!showSubtype" class="mb-1">
                            <label for="type" class="form-label" id="subtype_element">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['subtype']"></i>
                                Component Subtype*:</label>
                            <input style="background-color: gray;" type="text" class="form-control" id="type" v-model="component_subtype" required readonly placeholder="not required">
                        </div>  
                        <div  v-else-if="showSubtype" class="mb-1">
                            <label for="type" class="form-label" id="subtype_element">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['subtype']"></i>
                                Component Subtype*:</label>
                            <input type="text" class="form-control" id="type" v-model="component_subtype" required>
                        </div>
                    
                        </div>
                        <div class="col-6">
                            <div class="mb-1">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['scale_cost']"></i>
                                <label for="quantity" class="form-label">Scale Cost*:</label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="scale_cost"  required>
                            </div>
                        </div>
                    </div>


                    <div class="row mb-1" v-if="SHEET_TYPE=='Insulation'">
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


                    <div class="row">
                        <div class="col">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">Component Lifetime* <strong>[Years]:</strong><span v-if="lifetime<0" class="text-danger"><br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" min="0" required>
                            </div>
                        </div>
                        <div class="col">    
                            <div class="mb-1">
                            
                            <label for="quantity" class="form-label">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['major_upgrade_point']"></i>
                                Major Upgrade Point* <strong> 
                                [Years]:</strong><span v-if="major_upgrade_point<0" class="text-danger"><br> valid value is non negative</span></label>
                            <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_point" min="0" required>
                        </div>
                        </div>

                        <div class="col">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['major_upgrade_share']"></i>
                                    Major Upgrade Share* <strong>[CAPEX%]:</strong> <span v-if="major_upgrade_share>100 || major_upgrade_share<0" class="text-danger"><br>valid range is [0,100]</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="major_upgrade_share" min="0" max="100" required>
                        </div>
                        </div>

                    </div>

                    <div v-if="SHEET_TYPE=='Glazing'" class="row mb-2">
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


                    <div class="row">
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['CAPEX/UGS']"></i>
                                    CAPEX/UGS*<strong>[€/{{ ugs_header }}]</strong>:<span v-if="capex_per_ugs<0" class="text-danger"> <br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control"  id="validationCustom01" v-model="capex_per_ugs" min="0" required>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['annual_performance_degradation']"></i>
                                    Annual Performance Degradation[%]*: <span v-if="annual_performance_degradation>100 || annual_performance_degradation<0" class="text-danger"> <br>  valid range is [0,100]</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="annual_performance_degradation" min="0" max="100" required>
                            </div>
                        </div>
                    </div>


                    <div class="row">
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['OPEX_PER_CAPEX']"></i>
                                    Annual Maintenance <strong>[CAPEX%]:</strong> <span v-if="opex_per_capex>100 || opex_per_capex<0" class="text-danger"> <br> valid range is [0,100]</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="opex_per_capex" min="0" max="100" required>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="EOL_ACTION" class="form-label">EOL ACTION*:</label>
                                <select id="EOL_ACTION" v-model="replace_or_die" class="custom-select" required>
                                    <option value="replace">replace</option>
                                    <option value="die">die</option>
                                </select>
                            </div>
                        </div>
                    </div>


                    <div class="row">
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="quantity" class="form-label" >
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['embodied_co2_per_ugs']"></i>
                                    Embodied CO2/UGS* <strong>[kgCO2/{{ ugs_header }}]</strong>:</label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_co2_per_ugs" required>
                            </div>
                        </div>
                        <div class="col-6">     
                            <div class="mb-1">
                                <label for="description" style="display:block;">Description:</label>
                                <textarea id="description" v-model="description" rows="2" cols="30"  placeholder="fulfill with usefull info about the Component"></textarea>
                            </div>
                        </div>
                    </div>


                    <div class="row">
                        <div class="col-6">
                            <div class="mb-1">
                                <label for="quantity" class="form-label">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['embodied_pe_per_ugs']"></i>
                                    Embodied Pe/UGS* <strong>[GJ/{{ ugs_header }}]</strong>:<span v-if="embodied_pe_per_ugs<0" class="text-danger"><br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="embodied_pe_per_ugs" min="0" required>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="mb-1" >
                                <label for="bibliography" style="display:block;">Bibliography:</label>
                                <textarea id="bibliography" v-model="bibliography" rows="2" cols="30" placeholder="Add bibliography links or other sources"></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-2 mt-2">
                            <button type="submit" id="sumbit-button" class="btn btn-primary mb-2">Create Component</button>
                        </div>
                        <p  id='mandatory' class="col-10 mt-2"><strong>All fields with * are Mandatory</strong></p>
                    </div>  
               
                   

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
        conductivity:null,
        density:null,
        capacity:null,
        uvalue:null,
        gvalue:null,
        ugs_header:null,
        explainMessage:null,
        explanationMode:false,
        showSubtype:true,
        explain_dict:{
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

        if(this.SHEET_TYPE=='Insulation'){
            dataObject['thermal_properties'] = {'conductivity':this.conductivity,
                                                'density':this.density,
                                                'capacity':this.capacity}
        } 

        if(this.SHEET_TYPE=='Glazing'){
            dataObject['thermal_properties'] = {'uvalue':this.uvalue,
                                                'gvalue':this.gvalue}
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
            return this.explainMessage
        }
        if(explainHeader==='subtype'){
            this.explainMessage = 'Is the Components subtype e.g. for a Heatpump a subtype would be: water to water'
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='installed_ugs'){
            this.explainMessage = 'Is the Components installed Nominal Magnitude e.g. for Heatpump is the nominal power to kwh '
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='CAPEX/UGS'){
            this.explainMessage = 'This parameter is the ratio of a the CAPEX/UGS for the reference component that is considered for this analysis e.g. Heatpumps cost=100 € and nominal power (installed UGS) = 10kW ==>  CAPEX/UGS=10[€/kW]'              
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='OPEX_PER_CAPEX'){
            this.explainMessage = 'This parameter gives the ratio of components yearly maintenance according to its CAPEX. e.g. if this ratio=10% then considering that Heatpump costs 100€ every year maintenance cost is 10€ '              
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='embodied_co2_per_ugs'){
            this.explainMessage = 'This parameter gives the ratio of embodied CO2[kg]/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied CO2=100 kg and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[kgCO2/kWh] '              
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='embodied_pe_per_ugs'){
            this.explainMessage = 'This parameter gives the ratio of embodied Primary/UGS for the reference component that is considered for this analysis, e.g. Heatpumps embodied Pe=100 GJ and the Nominal Power (installed UGS) is 10 kWh then the ratio=10[GJ/kWh] '              
            this.explanationMode=true
            return this.explainMessage
            
        }
        if(explainHeader==='scale_cost'){
            this.explainMessage = 'exponent for power-scaling the input values to match the size of the user-input(monetery). '              
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='scale_env'){
            this.explainMessage = 'exponent for power-scaling the input values to match the size of the user-input (environmental).'              
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='major_upgrade_point'){
            this.explainMessage ='Is time interval that major upgrades for the component occur, e.g. for a heatpump if the major upgrade point is 5 years, every 5 years major upgrade occur for this component.'
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='major_upgrade_share'){
            this.explainMessage = 'Is the % Percentage of CAPEX to calculate the cost of a major upgrade.'
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='annual_performance_degradation'){
            this.explainMessage = 'Annual drop of performance'
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='pref_env'){
            this.explainMessage = 'is the nominal installed UGS for the reference component of the analysis(environmental) e.g for a heatpump would be 10[kW]'
            this.explanationMode=true
            return this.explainMessage
        }
        if(explainHeader==='pref_cost'){
            this.explainMessage = 'is the nominal installed UGS for the reference component of the analysis(monetery) e.g for a heatpump would be 8[kW]'
            this.explanationMode=true
            return this.explainMessage
        }
        if (explainHeader=='MAIN_INVENTORY'){
            this.explainMessage = 'When a component is not project specific is added at main inventory e.g. there is need to have a generalized Heatpump water to water at Verify inventory.'
            this.explanationMode=true
            return this.explainMessage

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
        if( newValue=="El. Generators" || newValue=="Thermal Sources" || newValue=='PCM'){
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
#component {
    position: relative;
    width: 120%;
    background-color: aliceblue;
    border: 2px solid lightsteelblue;
    display: flex;
    justify-content: space-evenly;
    border-radius: 1%;
    height: 98%;
   
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

</style>
