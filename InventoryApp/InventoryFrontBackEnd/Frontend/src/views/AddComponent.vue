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
                            <h5><b>1. Add the basic attributes to define the component:</b></h5>
                        </div>
                        
                        <div v-if="is_admin"  class="row">
                            <div class="col">
                                <label class="form-label" for="isMainInventory">Is Default Component</label>
                                <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="IS_MAIN_INVENTORY" value="false">
                            </div>
                        </div>

                        <!-- Add Name -->
                        <div class="col-6">
                                <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" title="It is Important to give a formated name e.g: for the Rehouse Project at Greek Demo, a heatpump named Psyctotherm would named: Rehouse_Greek_Heatpump_Psyctotherm "></i>
                                <label for="name" class="form-label">Name*:</label>
                                <input type="text" class="form-control" id="name" v-model="name" placeholder="format: Project_Demo_Building_Name" required>
                        </div>
                        
<!-- Add technology Key -->
                        <div class="col-6">
                            <label for="Choose Technology" class="form-label">Choose Technology*:</label>
                            <select id="Choose Technology" v-model="SHEET_TYPE" class="custom-select" required>
                            <optgroup label="Building Level Components">
                                <option value="El. Generators">Electrical Generators</option>
                                <option value="Thermal Sources">Thermal Sources</option>
                                <option value="Glazing">Glazing</option>
                                <option value="Insulation">Insulation</option>
                                <option value="Ventilation">Ventilation</option>
                                <option value="PCM">PCM</option>
                                <option value="Water Storage">Water Storage</option>
                                <option value="El. Storage">Electrical Storage (ESS)</option>
                                <option value="B_Batteries"> Batteries (Buildings)</option>
                            </optgroup>
                            <!--D COMPONENTS:-->
                            <optgroup label="District Level Components">
                                <option value="Plants">Plants</option>
                                <option value="Public">Public</option>
                                <option value="Transport">Transport</option>
                                <option value="D_Batteries">Batteries + ESS </option>
                            </optgroup>
                        </select>
                        </div>
                      
<!--Add types-----------------------------------------------------------------------------> 
                        <div class="col-6 mt-3">
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

                                    <div id="options" v-if="SHEET_TYPE=='B_Batteries'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="battery_li_ion">battery Li-ion </option>
                                        <option value="lead_acid">battery lead acid</option>
                                        <option value="flow">battery flow</option>
                                    </select>
                                    </div>

                                    <div id="options" v-if="SHEET_TYPE == 'D_Batteries'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="battery_li_ion">battery Li-ion </option>
                                        <option value="lead_acid">battery lead acid</option>
                                        <option value="flow">battery flow</option>
                                        <option value="flywheel">flywheel </option>
                                    </select>
                                    </div>

                                    <div id="options" v-if="SHEET_TYPE=='El. Storage' ">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                        <option value="flywheel">flywheel </option>
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
                                                            <!--D COMPONENT TYPES-->
                                    <div id="optionsD" v-if="SHEET_TYPE=='Plants'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                            <option value="power_plant"> Power Plant </option>
                                            <option value="geothermal_hydro_plant"> Geothermal / Hydro Plant </option>
                                            <option value="incineration_plant">Incineration Plant</option>
                                            <option value="tidal_device_plant">Tidal Plant</option>
                                            <option value="fuel_cell_plant">Fuel Cell Plant</option>
                                            <option value="solar_park">Solar Park</option>
                                            <option value="wind_park"> Wind Park</option>
                                        </select>
                                    </div>

                                    <div id="optionsD" v-if="SHEET_TYPE=='Transport'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                            <option value="electric_vehicle"> Electric Vehicle </option>
                                        </select>
                                        </div>
                                    
                                    
                                    <div id="optionsD" v-if="SHEET_TYPE=='Public'">
                                        <label for="type" class="form-label">Component Type* :</label><br>
                                        <select id="type" v-model="component_type" required>
                                            <option value="charging_station"> Charging Station </option>
                                            <option value="transformer"> Transformer </option>
                                            <option value="lighting"> Lighting </option>
                                            <option value="interconnection"> Interconnection </option>
                                        </select>
                                    </div>
                                </div>
                        </div>
<!--Add subtypes-->

                        <div class="col-6 mt-3">
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
                            <div  v-else-if="!showSubtype">
                                <label for="type" class="form-label" id="subtype_element">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['subtype']"></i>
                                    Component Subtype*:</label>
                                <input style="background-color: gray;" type="text" class="form-control" id="type" v-model="component_subtype" required readonly placeholder="not required">
                            </div>  
                            <div  v-else-if="showSubtype">
                                <label for="type" class="form-label" id="subtype_element">
                                    <i id='tooltip-explain' class="fa fa-question-circle" data-toggle="tooltip" data-placement="left" :title="explain_dict['subtype']"></i>
                                    Component Subtype*:</label>
                                <input type="text" class="form-control" id="type" v-model="component_subtype" required>
                            </div>
                        </div>
                        
<!-- common section  -->
                    <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3">
                            <h5><b>2. Add common fields:</b></h5>
                    </div>

                    <div class="row">
                        <div class="col-4">
                                <label for="quantity" class="form-label">Component Lifetime* <strong>[Years]:</strong><span v-if="lifetime<0" class="text-danger"><br> valid value is non negative</span></label>
                                <input type="number" step="any" class="form-control"  id="quantity" v-model="lifetime" oninput="this.value|=0" min="0" required>
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


<!--sources section AND  LCA information--> 
                    <hr class="mt-3 mb-3" style="width: 98%; margin: 0 auto;">
                    <div class="mt-3">
                            <h5><b>3. Add Description and Sources:</b></h5>
                    </div>

                    <div class="col-12 mt-3">
                            <label for="simapro_version" style="display:block;">Simapro Version:</label>
                            <input class="form-control" type="text" v-model="simapro_version">
                    </div>

                        <!--Add Description and Bibliography-->
                        <div class="col-12 mt-3">     
                                <label for="description" style="display:block;">Description:</label>
                                <textarea id="description" v-model="description" rows="4" cols="30"  placeholder="fulfill with usefull info about the Component"></textarea>
                        </div>

                        <div class="col-12 mt-3">
                            <label for="bibliography" style="display:block;">Bibliography:</label>
                            <textarea id="bibliography" v-model="bibliography" rows="4" cols="30" placeholder="Add bibliography links or other sources"></textarea>
                        </div>

                           <!-- Add some new element about LCA info-->
                           <div class="col-6 mt-3">
                            <label for="ia_method_ghg" style="display:block;">Impact Assessment Method (GHG emissions):</label>
                            <input class="form-control" type="text" v-model="ia_method_ghg">
                        </div>


                        <div class="col-6 mt-3">
                            <label for="ia_method_pe" style="display:block;">Impact Assessment Method (Primary Energy Demand):</label>
                            <input class="form-control" type="text" v-model="ia_method_pe">
                        </div>

                        <div class="col-6 mt-3">
                            <label for="lca_db" style="display:block;">Life Cycle Analysis Database:</label>
                            <input class="form-control" type="text" id="lca_db" v-model="lca_db">
                        </div>

                        <div class="col-6 mt-3">
                            <label for="custom" style="display:block;">Functional Unit:</label>
                            <input id="custom" class="form-control" type="text"  v-model="functional_unit">
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
                        <button type="submit" id="sumbit-button" class="btn btn-primary mb-2">Create Component</button>
                    </div>


                      
            </form>
        </div>
    </div>
</div>

</template>

<script>
import { axios } from "@/common/api.service.js";
import { TARGET_IP } from "@/common/request_configs.js";
import readXlsxFile from 'read-excel-file';
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
        pref_cost:1,
        pref_env:1,
        scale_cost:1,
        scale_env:1,
        capex_per_ugs:1,
        major_upgrade_point:null,
        major_upgrade_share:null,
        annual_performance_degradation:null,
        replace_or_die:null,
        SHEET_TYPE:null,
        IS_MAIN_INVENTORY:false,
        description:null,
        bibliography:null,
        ia_method_ghg:null,
        ia_method_pe:null,
        lca_db:null,
        simapro_version:null,
        functional_unit:null,
        conductivity:null,
        density:null,
        capacity:null,
        uvalue:null,
        gvalue:null,
        ugs_header:null,
        explainMessage:null,
        explanationMode:false,
        showSubtype:true,
        file :null,
        eol_pe_cost:null,
        eol_co2_cost:null,
        is_admin:false,
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
        console.log("i submit..")
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
        console.log("SHEET_TYPE:", this.SHEET_TYPE);
        if(this.SHEET_TYPE=='Insulation'){
            dataObject['thermal_properties'] = {'conductivity':this.conductivity,
                                                'density':this.density,
                                                'capacity':this.capacity}
        } 

        if(this.SHEET_TYPE=='Glazing'){
            dataObject['thermal_properties'] = {'uvalue':this.uvalue,
                                                'gvalue':this.gvalue}
        }

        // tag the component as B or D 
        if(this.SHEET_TYPE=="Plants" || this.SHEET_TYPE=="Public" || this.SHEET_TYPE=='Transport' ||this.SHEET_TYPE=='D_Batteries'){
            dataObject["IS_B_COMPONENT"] = false
            console.log("D COMPONENT")
        }else{
            dataObject["IS_B_COMPONENT"] = true
            console.log("B COMPONENT")
        }

        try{
            console.log("i submit..")
            dataObject.opex_per_capex/=100;
            dataObject.major_upgrade_share/=100;
            dataObject.annual_performance_degradation/=100;
            const {data} = await axios.post(`${TARGET_IP}/api/component/`,dataObject)
                console.log(dataObject)
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


    async onFileChange(event) {
        let xlsxfile = event.target.files ? event.target.files[0] : null;
        readXlsxFile(xlsxfile).then((rows) => {
        
            console.log("rows:", rows)
            let parameter_labels = rows[0]
            // is the Array of all objects will be created
            let excellComponent = []
            //(initialization)create n emtpy objects for n rows of component values
            for(let i=0;i<rows.length-1;i++){
                excellComponent.push({})
           }
            console.log("rows= ",rows.length)
            // iterate over rows (components)
            for(let i=1 ; i<rows.length ;i++){
                let sheetType = rows[i][15] // is its position at the form, will be changed
                console.log( "iteration = ",i," SHEET-TYPE = ",sheetType)
                if(sheetType==='Glazing' || sheetType==='Insulation'){
                    console.log("add thermal properties before create insulation")
                    excellComponent[i-1]['thermal_properties'] = {}
                }
                for(let j = 0; j < parameter_labels.length; j++){
                    let jsonKey = rows[0][j]
                    if (jsonKey!='conductivity' && jsonKey!='capacity' && jsonKey!='density' && jsonKey!="gvalue" && jsonKey!="uvalue"){ 
                        excellComponent[i-1][jsonKey] = rows[i][j]
                    }else if(sheetType==='Insulation' && (jsonKey=='density'||jsonKey=='conductivity'||jsonKey=='capacity')){
                        console.log('Insulation in')
                        excellComponent[i-1]['thermal_properties'][jsonKey] = rows[i][j]
                    }else if(sheetType==='Glazing' && (jsonKey=='uvalue'||jsonKey=='gvalue')){
                        console.log('Glazing in')
                        excellComponent[i-1]['thermal_properties'][jsonKey] = rows[i][j]
                    }
                }
                if (!('thermal_properties' in excellComponent[i-1])){
                    excellComponent[i-1].thermal_properties = null
                }
            }

            console.log("----------test----------------")
            console.log(excellComponent)
            console.log(excellComponent[0])
            console.log(excellComponent[1])
            console.log(excellComponent[2])

            // to handle them properly - now is for proof of concept:
            /*
            excellComponent["bibliography"] = null
            excellComponent["description"] = null 
            excellComponent["thermal_properties"] = null
            console.log(excellComponent)
            */
            console.log("excellComponent data:", excellComponent);


            //let excellComponentBody = JSON.stringify({excellComponent})
            axios.post(`${TARGET_IP}/api/excell_create`,excellComponent, {
                headers: {'Content-Type': 'application/json'},}) 
                .then(()=>{
                alert("Success")
                this.$router.push({ name:'ListComponents'}); //here add the router name from router/index.js
            }).catch(error => {
                let error_message = "errors \n"
                for(let i=0;i<error.response.data.length;i++){
                    if(Object.keys(error.response.data[i]).length===0){
                        error_message+=`${excellComponent[i].name} : pass \n`
                    }else{
                        console.log(error.response.data[i])
                        for(let prop in error.response.data[i])
                        error_message+=`${excellComponent[i].name} : ${error.response.data[i][prop][0]} \n`
                    }
                }
               alert(error_message)
               console.error('Error fetching data:', error.response.data)})
            } 
  )}},

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

        //check if you are the admin user:
        axios.get(`${TARGET_IP}/api/is_admin_user`).
        then(response=>{
          this.is_admin = response.data.is_admin
          console.log(`is the user admin: ${this.is_admin}`)
        })
  },
  watch: {
    SHEET_TYPE(newValue) {
        // at every change of sheet type make it null:
        this.ugs_header = null
        
         if( newValue=="El. Generators" || newValue=="Thermal Sources" || newValue=='Ventilation' || newValue=='PCM' || newValue=='Plants'){
            console.log(this.ugs_header)
            this.ugs_header = 'kW'
            this.showSubtype=true;
        }else if(newValue=="Water Storage"){
            this.ugs_header='Litre'
            this.showSubtype=true;
        }
        else if(newValue=='El. Storage' ||newValue=='B_Batteries' || newValue=='D_Batteries'){
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
        else if(newValue=='Other' || newValue=='Transport'){
            this.ugs_header='FU'
            this.showSubtype=true;
        }
    },
    typeSubtypeCombination(newValue){
        if(this.SHEET_TYPE=='Public'){
            if(newValue=='Public transformer'){

                this.ugs_header='kVA'
                this.showSubtype=true;

            }else if (newValue=='Public interconnection'){
                this.ugs_header='FU'
                this.showSubtype=true;
            }else{
                this.ugs_header='kW'
                this.showSubtype=true;
            }
        }
    },
    IS_MAIN_INVENTORY(newValue){
        if(newValue==true){
            this.scale_cost=null
            this.scale_env=null
            this.pref_cost=null
            this.pref_env=null
            this.capex_per_ugs=null
        }
    }
  },
  computed: {
    typeSubtypeCombination() {
      return `${this.SHEET_TYPE} ${this.component_type}`
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
