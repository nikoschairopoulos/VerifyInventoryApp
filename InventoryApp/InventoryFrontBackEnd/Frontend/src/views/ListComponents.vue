<template>
  <div>   
    <div class="tablecontainer">
      <div class="choose_option">
        <div style="display: flex; justify-content: space-between;">
        <h2>Search components by technology <span class="fa fa-search" ></span></h2><br>
        
          <download-excel 
             class="btn btn-info download-btn"
             :data="deepCopyComps"
              type="xlsx"
             name="verify_components.xlsx">
             download components
          </download-excel>
        </div>
        <hr>
      <div class="mb-1 ml-2" id="filter">
                <label for="Choose Technology" class="form-label"><strong>Choose Technology</strong>:</label>
                <select id="ChooseTechnology" v-model="SHEET_TYPE" class="custom-select" @change="updateTypeofComponentToRender()">
                  <optgroup label="Building Level Components">
                      <option value="all types">All Types</option>
                      <option value="El. Generators">Electrical Generators</option>
                      <option value="Thermal Sources">Thermal Sources</option>
                      <option value="Glazing">Glazing</option>
                      <option value="Insulation">Insulation</option>
                      <option value="Ventilation">Ventilation</option>
                      <option value="PCM">PCM</option>
                      <option value="Water Storage">Water Storage</option>
                      <option value="El. Storage">El. Storage (ESS)</option>
                      <option value="B_Batteries">Batteries</option>
                  </optgroup>
                  <optgroup label="District Level Components">
                      <option value="Plants">Plants</option>
                      <option value="Public">Public</option>
                      <option value="Transport">Transport</option>
                      <option value="D_Batteries">Batteries + ESS </option>
                  </optgroup>
                  <!--<option value="Other">Other</option>--> 
                   
                </select>

                <div class="mb-2 ml-2 " >
                  <label class="form-check-label" for="isMainInventory"><strong>No Main Inventory  </strong></label>
                        <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="NotMainInventory" @change="updateTypeofComponentToRender()"  value="false" >
                    </div>
            </div>
            <hr style="color: green;">
            
      </div>  
      <div class="responsive">
      <div class="table-responsive">
      <table class=" table  table-hover">
          <tr style="background-color:#054673;color:#F7F7F7;">
            <th id="id_element" scope="col" class="text-center">ID</th>
            <th scope="col" class="text-center">Name</th>
            <th scope="col" class="text-center">Type</th>
            <th scope="col" class="text-center">Subtype</th>
            <th id="actions_element" scope="col" class="text-center">Actions</th>
          </tr>
        <tbody>
          <tr v-for="component in componentsPerType"  :key="component.id">
                <td class="text-center">{{ component.id }}</td>
                <td class="text-center">{{ component.name }}</td>
                <td class="text-center">{{ component.component_type }}</td>
                <td class="text-center">{{ component.component_subtype }}</td>
                <td>

              
                  
                  <span @click="setDetailsAndShowModal(component)"  class="fa-stack">
										<i class="fa fa-square fa-stack-2x"></i>
										<i  style="color: white;" class="fa fa-edit fa-stack-1x fa-inverse"></i>
									</span>


                  <span @click="updateComponent(component.id)"  class="fa-stack" >
										<i class="fa fa-square fa-stack-2x" ></i>
										<i style="color: yellow;" class="fa fa-pencil fa-stack-1x fa-inverse"></i>
									</span>
                

									<span @click="deleteComponent(component.id)"  class="fa-stack">
										<i class="fa fa-square fa-stack-2x"></i>
										<i style="color: red;" class="fa fa-trash-o fa-stack-1x fa-inverse"></i>
									</span>

							

                </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>

       <!-- Component Info Modal-->
       <div v-if="detailsComp" class="modal" role="document" :class="{ 'is-active': showModal }">
       <div class="modal-background" @click="closeModal"></div>
       <div class="modal-card">
        <header class="modal-card-head">
          <h4 class="modal-card-title"><strong>{{ detailsComp.name }}</strong></h4>
        </header>
        <hr style="size:60px;" class="mt-4">
            <div class="modal-card-body">
              <div class="group1">
                  
                        <label for="type" class="form-label">Component Type:</label>
                        <input type="text" class="form-control" id="type" v-model="detailsComp.component_type" readonly="true">
                  
                        <label for="type" class="form-label">Component Subtype:</label>
                        <input type="text" class="form-control" id="type" v-model="detailsComp.component_subtype">
              
                        <label for="quantity" class="form-label">CAPEX/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.capex_per_ugs" min="0">
                  
                 
                        <label for="quantity" class="form-label">ANNUAL MAINTENANCE[%CAPEX]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.opex_per_capex" min="0">
                
                 
                        <label for="quantity" class="form-label">Embodied CO2/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.embodied_co2_per_ugs" min="0">
                
                        <label for="quantity" class="form-label">Embodied Pe/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.embodied_pe_per_ugs" min="0">
                 
                        <label for="quantity" class="form-label">Component Lifetime[years]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.lifetime" min="0">

                        <label for="quantity" class="form-label">EoL CO2 Cost[KgCO2]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.eol_co2_cost" min="0"> 

                        <hr>
                        <div v-if="detailsComp.SHEET_TYPE=='Insulation'">
                          <label for="quantity" class="form-label">Density<strong>[Kg/m&sup3;]</strong>:</label>
                          <input type="text" class="form-control"  id="quantity" v-model="detailsComp.thermal_properties.density" min="0">
                        </div>

                        <div v-if="detailsComp.SHEET_TYPE=='Insulation'">
                          <label for="quantity" class="form-label">Specific Heat Capacity:<strong>[J/(Kg&middot;K)]</strong></label>
                          <input type="text" class="form-control"  id="quantity" v-model="detailsComp.thermal_properties.capacity" min="0">
                        </div>

                        <div v-if="detailsComp.SHEET_TYPE=='Glazing'">
                            <label for="quantity" class="form-label">U value:</label>
                            <input type="text" class="form-control"  id="quantity" v-model="detailsComp.thermal_properties.uvalue" min="0">
                          </div>
            </div>
            <div class="group2">
                
                        <label for="quantity" class="form-label">Pref Cost:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.pref_cost" min="0">
                 
                        <label for="quantity" class="form-label">Pref Env:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.pref_env" min="0">
                  
                        <label for="quantity" class="form-label">Scale Cost:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.scale_cost" min="0">
                  
                        <label for="quantity" class="form-label">Scale Env:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.scale_env" min="0">
                  
                        <label for="quantity" class="form-label">Major Upgrade Point[years]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.major_upgrade_point" min="0">
                
                        <label for="quantity" class="form-label">Major Upgrade Share[%100]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.major_upgrade_share" min="0">
    
                        <label for="quantity" class="form-label">Annual Performance Degradation[%]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.annual_performance_degradation" min="0"> 

                        <label for="quantity" class="form-label">EoL primary energy cost[Gj]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.eol_pe_cost" min="0"> 

                        <hr>
                        <div v-if="detailsComp.SHEET_TYPE=='Insulation'">
                            <label for="quantity" class="form-label">Thermal Conductivity<strong>[W/(m&middot;K)]:</strong></label>
                            <input type="text" class="form-control"  id="quantity" v-model="detailsComp.thermal_properties.conductivity" min="0">
                          </div>

                        <div v-if="detailsComp.SHEET_TYPE=='Insulation'">
                          <label for="quantity" class="form-label">U value<strong>[W/(m&sup2;K)]</strong>:</label>
                          <input style="background-color: gray;" type="text" class="form-control"  id="quantity" value="not defined" min="0">
                        </div>

                        <div v-if="detailsComp.SHEET_TYPE=='Glazing'">
                            <label for="quantity" class="form-label">G value:</label>
                            <input type="text" class="form-control"  id="quantity" v-model="detailsComp.thermal_properties.gvalue" min="0">
                          </div>
             
                  </div>
            </div> 
      </div>
    </div>
    
    <!--Deletion Modal-->
    <div v-if="showDeleteModal"   class="modal"  tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true" :class="{ 'is-active':showDeleteModal}" >
        <div class="modal-background" @click="closeDeleteModal" >
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" style="background-color: cornflowerblue;">Warnings of Deletion Procedure</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>{{this.deletion_warnings}}</p>
            </div>
            <div class="modal-footer">
              <!-- <button type="button" class="btn btn-primary">Save changes</button> -->
               <p>will not be performed deletion</p>
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
    </div>
  </div>

</div>
</template>
  
  

<script>
import { axios } from "@/common/api.service.js";
import { TARGET_IP } from "@/common/request_configs.js";
import JsonExcel from 'vue-json-excel3';
import UpdateComponent from './UpdateComponent.vue';
export default {
    name:"ListComponents",

    data() {
        return { components: [],
                 updateComponentMode: false,
                 EditedComponent:null,
                 componentsPerType:[],
                 SHEET_TYPE:"all types",
                 detailsComp:null,
                 toShow:false,
                 showModal:false,
                 NotMainInventory:false,
                 deletion_warnings:[],
                 showDeleteModal:false,
                 deepCopyComps:[]

        };
    },
    mounted() {
        console.log(`${TARGET_IP}/api/component/`,'------------------------------')
        axios.get(`${TARGET_IP}/api/component/`)
            .then(response => {
            for (let comp of response.data) {
                this.components.push(comp);
            }
            this.componentsPerType=this.components
            this.componentsPerType.sort((a, b) => a.id - b.id);
            console.log(response.data);
            console.log(this.components)
            this.componentTableForExcell();
        })
            .catch(error => {
            console.error('Error fetching data:', error);
        });
    },

    methods: {
        updateTypeofComponentToRender(){
          if(this.SHEET_TYPE==="all types"){this.componentsPerType=this.components}
          else{this.componentsPerType=this.components.filter(comp=>comp.SHEET_TYPE==this.SHEET_TYPE)}

          if(this.NotMainInventory){
            this.componentsPerType=this.componentsPerType.filter(comp=>!comp.IS_MAIN_INVENTORY)
          }

          //sort by id the components per type:
          this.componentsPerType.sort((a, b) => a.id - b.id);
        },
        componentTableForExcell(){
          console.log(this.components[0]);
          this.deepCopyComps = this.components.map((comp) => JSON.parse(JSON.stringify(comp)));
          // change column names Dict:
          let namesDict = {
            'capex_per_ugs':'Capex Per Functional Unit [Euro/Functional Unit]',
            'embodied_co2_per_ugs':'Embodied Co2 Per Functional Unit [KgCo2/Functionl Unit]',
            'embodied_pe_per_ugs':'Embodied Primary Energy Per Functional Unit [Gj/Functional Unit]',
            'major_upgrade_point':'Major Upgrade Point [years]',
            'lifetime':'Lifetime [years]',
            'opex_per_capex':'Annual Maintenance [%Capex]',
            'replace_or_die':'replace (or) end of life',
            'pref_env':'Pref_env [Functional Unit]',
            'pref_cost':'Pref_cost [Functional Unit]'
          }
          function renameKey(obj, old_key, new_key) {
            // Check if old key = new key
            if (old_key !== new_key) {
              // Modify old key
              Object.defineProperty(obj, new_key,
              Object.getOwnPropertyDescriptor(obj, old_key));
              //delete old key:
              delete obj[old_key];
            }
          }
          for (let comp of this.deepCopyComps){
            if (comp.hasOwnProperty('thermal_properties') && comp.SHEET_TYPE=='Insulation' && comp['thermal_properties']!= null){
                comp['thermal_properties'] = JSON.stringify(comp['thermal_properties']);
            }
            //round:
            comp['embodied_co2_per_ugs'] = Math.round(comp['embodied_co2_per_ugs'] * 1000) / 1000;
            comp['embodied_pe_per_ugs'] = Math.round(comp['embodied_pe_per_ugs'] * 1000) / 1000;
            comp['capex_per_ugs'] = Math.round(comp['capex_per_ugs']*1000)/1000;

            for(let key in namesDict){
              if (key == 'opex_per_capex'){
                comp[key]*=100
              }
              renameKey(comp,key,namesDict[key])
            }
            // Add the correct Functional Units:
            let newValue = comp['SHEET_TYPE']
            // initialize to None:
            comp['Functional Unit'] = null
            if( newValue=="El. Generators" || newValue=="Thermal Sources" || newValue=='PCM' || newValue=='Plants'){
              comp['Functional Unit'] = 'Kw'
            }else if(newValue=="Water Storage"){
              comp['Functional Unit']='Litre'
            }
            else if(newValue=='El. Storage' ||newValue=='B_Batteries' || newValue=='D_Battteries'){
              comp['Functional Unit']='KWh'
            }
            else if(newValue=='Insulation'){
              comp['Functional Unit']='m\u00B3'
            }
            else if(newValue=='Glazing'){
              comp['Functional Unit']='m\u00B2'
            }
            else if(newValue=='Other'){
              comp['Functional Unit']='UGS'
            }
            else if(newValue=='Ventilation'){
              comp['Functional Unit'] = 'Kw'
            }
            else if(newValue=='Public' && comp['component_type']=='charging_station'){
              comp['Functional Unit'] = 'Kw'
            }
            else if(newValue=='Public' && comp['component_type']=='transformer'){
              comp['Functional Unit'] = 'KVA'
            }
            else if(newValue=='Public' && comp['component_type']=='lighting'){
              comp['Functional Unit'] = 'KVA'
            }
            else if(newValue=='Transport'){
              comp['Functional Unit'] = 'vehicle'
            }
          
          }

          //********sort the components**********
          this.deepCopyComps.sort((a, b) => a.id - b.id);

          // ***************filter components*****************:
          //filter (1)
          //this.deepCopyComps = this.deepCopyComps.filter((comp)=>comp.IS_B_COMPONENT)
          //filter (2)
          this.deepCopyComps = this.deepCopyComps.filter((comp)=>comp['IS_MAIN_INVENTORY'])
          //***************************************************

          //delete some attributes:
          this.deepCopyComps = this.deepCopyComps.map((comp) =>{ 
            delete comp['IS_MAIN_INVENTORY']
            delete comp['IS_B_COMPONENT']
            return comp
          })
          console.log(this.deepCopyComps)
        },
        refreshlist(id) {
            this.components = this.components.filter(comp => comp.id != id);
            this.updateTypeofComponentToRender()
        },
        
        async deleteComponent(componentId) {
            let comp = this.components.filter(comp => comp.id === componentId);
            let check = window.prompt(`Please Enter "y" if you want to delete the component (Name:${comp[0].name})  else press "n":`, "");
            if (check === "y") {
                await axios
                    .delete(`${TARGET_IP}/api/component/${componentId}/`)
                    .then(()=>this.refreshlist(componentId))
                    .catch(error => {
                            if (error.response) {
                            // The request was made and the server responded with a status code
                            // that falls out of the range of 2xx
                            console.log('Error response data:', error.response.data);
                            console.log('Error response status:', error.response.status);
                            console.log('Error response headers:', error.response.headers);
                            // Show the error message to the user
                            this.deletion_warnings = JSON.stringify(error.response.data, null, 2);
                            this. showDeleteModal = true
                            console.log('delete:',this.deleteComponentModal)
                            //alert(`Error: ${errorMessage}`);
                            } else if (error.request) {
                            // The request was made but no response was received
                            console.log('Error request:', error.request);
                            alert('Error: No response received from the server.');
                            } else {
                            // Something happened in setting up the request that triggered an Error
                            console.log('Error message:', error.message);
                            alert(`Error: ${error.message}`);
                            }
                          })
                        }},
        
        updateComponent(componentId) {
            // find the component from its Id:
            //this.EditedComponent = this.components.filter(comp=>comp.id===componentId)[0]
            
            //make the request to the router with query paramas: id 
            console.log("i will update this component ",componentId)
            this.$router.push({ name:'Update Component',
                                params:{id:componentId}});   
        },
        dontshowDetails(){
          this.toShow=false;
        },
        closeModal() {
          this.showModal = false;
        },
        closeDeleteModal(){
          console.log('i will close warnings modals .....')
          this.showDeleteModal=false;
        },
        setDetailsAndShowModal(component) {
          this.detailsComp = JSON.parse(JSON.stringify(component));
          this.detailsComp.opex_per_capex*=100;
          this.detailsComp.annual_performance_degradation*=100;
          this.detailsComp.major_upgrade_share*=100

          console.log(this.detailsComp)
          this.showModal = true;
  }
},
    computed: {
  },
    components: { UpdateComponent ,downloadExcel:JsonExcel }
} 
</script>




<style scoped>
/* Add styles as needed */
.tablecontainer{}

.responsive{
  margin: 0 auto;
  width:99%;
}

table {
  border-collapse: collapse;
}


.infocart{
  box-sizing: content-box;
  position: fixed;
  bottom: 20%;
  left:10%;
  border:green solid 2px;
  margin-top: 5%;
  display:flex;
  justify-content: space-around;
  background-color: aliceblue;
}

.group2{
  margin-right: 10px;
  max-height: 70%;
}

.group1{
  margin-left: 10px;
  max-height: 70%;
}

.modal {
  display: none;
}

.modal.is-active {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}


.modal-card {
  width: 50%;
  background-color:aliceblue;
  border-radius: 5px;
}

.modal-card-head {
            color: #fff;
            font-size: 20px;
            text-align: center;
}

.modal-card-body {
  display: flex;
  justify-content: space-between;
  padding: 20px; 
}

.choose_option{
  margin-left:10px;
  
}
h4{
  padding-top: 10px;
  margin-bottom: -25px;
  color: seagreen;
}


#ChooseTechnology{
  padding: 8px;
  background-color: hwb;
  border-radius: 24px;
  border: solid 2px darkgreen;
}

th, td {
  border: 1px solid #ddd;
  padding: 6px;
  text-align: center;
  text-overflow: ellipsis;
  white-space: normal;
  font-size: medium;
  word-wrap: break-word;
  width:200px;
  max-width: 200px;
}

#buttons{
width:50%;
}

.table thead > tr > th > p span {
	color: green
}

.table p.table-link {
	color:green;
	margin: 0 5px;
	font-size: 1.125em;
}
.table p.table-link:hover {
	text-decoration: none;
	color: #2aa493;
}
.table p.table-link.danger {
	color: #fe635f;
}
.table p.table-link.danger:hover {
	color: #dd504c;
}

span > i:hover {
    cursor: pointer;
    color: #2bb6a3;
	border-color: #2bb6a3;
}

span{
  color: green;
}

.table-responsive{
  display: contents;
}
h2{
  padding-top: 10px;
  margin-bottom: -25px;
  color: seagreen;
}

.download-btn{
  margin-top: 7px;
  margin-right: 1%;
  border: dashed 0.5px
}

#id_element{
  width: 5%;
}
#actions_element{
  width:10%;
}

.form-label{
  margin-bottom: 0px;
}

</style>