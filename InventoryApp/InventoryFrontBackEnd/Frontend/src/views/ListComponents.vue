<template>
  <div>   
    <div class="tablecontainer">
      <div class="choose_option">
        <div style="display: flex; justify-content: space-between;">
        <h2>Search components by technology <span class="fa fa-search" ></span></h2><br>
        
          <download-excel 
             class="btn btn-info download-btn"
             :data="components"
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
            <th scope="col" class="text-center">ID</th>
            <th scope="col" class="text-center">Name</th>
            <th scope="col" class="text-center">Type</th>
            <th scope="col" class="text-center">Subtype</th>
            <th scope="col" class="text-center">Actions</th>
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

       <!-- Modal-->
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
                 NotMainInventory:false

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
            console.log(response.data);
            console.log(this.components);
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
                          console.error('Error fetching data:', error)})}},
        
        updateComponent(componentId) {
            // find the component from its Id:
            //this.EditedComponent = this.components.filter(comp=>comp.id===componentId)[0]
            
            //make the request to the router with query paramas: id 
            console.log("i will update this component ",componentId)
            this.$router.push({ name:'Update Component',
                                params:{id:componentId}});   
        },
        dontshowDetails(){
          this.toShow=false
        },
        closeModal() {
          this.showModal = false;
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

</style>