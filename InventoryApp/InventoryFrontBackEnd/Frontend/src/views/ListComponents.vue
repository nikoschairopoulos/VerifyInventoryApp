<template>
  <div>   
    <div class="tablecontainer">
      <div class="choose_option">
        <h2>Search components by technology <span class="fa fa-search" ></span></h2><br>
        <hr>
      <div class="mb-1">
                <label for="Choose Technology" class="form-label"><strong>Choose Technology</strong>:</label>
                <select id="ChooseTechnology" v-model="SHEET_TYPE" class="custom-select" @change="updateTypeofComponentToRender()">
                    <option value="all types">All Types</option>
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
            <hr style="color: green;">
            
      </div>  
      <div class="table-responsive">
      <table class=" table  table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="col" class="text-center">ID</th>
            <th scope="col" class="text-center">Name</th>
            <th scope="col" class="text-center">Type</th>
            <th scope="col" class="text-center">Subtype</th>
            <th scope="col" class="text-center">replace_or_die</th>
            <th scope="col" class="text-center">SHEET_TYPE</th>
            <th scope="col" class="text-center">IS_MAIN_INVENTORY</th>
            <th scope="col" class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in componentsPerType"  :key="component.id">
                <td class="text-center">{{ component.id }}</td>
                <td class="text-center">{{ component.name }}</td>
                <td class="text-center">{{ component.component_type }}</td>
                <td class="text-center">{{ component.component_subtype }}</td>
                <td class="text-center">{{ component.replace_or_die}}</td>
                <td class="text-center">{{ component.SHEET_TYPE }}</td>
                <td class="text-center">{{ component.IS_MAIN_INVENTORY }}</td>
                <td>
                    <button class="btn btn-primary" style="margin-right:5px;" @click="updateComponent(component.id)">
                        Edit
                    </button>
                <button class="btn btn-danger" style="margin-right:5px;" @click="deleteComponent(component.id)">
                        Delete
                </button>
                <button type="button" class="btn btn-primary" @click="setDetailsAndShowModal(component)" >
                        Info
                </button>
                </td>
          </tr>
        </tbody>
      </table>
    </div>

       <!-- Modal-->
       <div v-if="detailsComp" class="modal" role="document" :class="{ 'is-active': showModal }">
       <div class="modal-background" @click="closeModal"></div>
       <div class="modal-card">
        <header class="modal-card-head">
          <h2 class="modal-card-title">Component Details</h2>
        </header>
            <div class="modal-card-body">
              <div class="group1">
                  
                        <label for="type" class="form-label">Component Type:</label>
                        <input type="text" class="form-control" id="type" v-model="detailsComp.component_type" readonly="true">
                  
                        <label for="type" class="form-label">Component Subtype:</label>
                        <input type="text" class="form-control" id="type" v-model="detailsComp.component_subtype">
              
                        <label for="quantity" class="form-label">CAPEX/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.capex_per_ugs" min="0">
                  
                 
                        <label for="quantity" class="form-label">OPEX_PER_CAPEX[%100]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.opex_per_capex" min="0">
                
                 
                        <label for="quantity" class="form-label">Embodied CO2/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.embodied_co2_per_ugs" min="0">
                
                        <label for="quantity" class="form-label">Embodied Pe/UGS:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.embodied_pe_per_ugs" min="0">
                 
                        <label for="quantity" class="form-label">Component Lifetime[years]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.lifetime" min="0">
               
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
    
                        <label for="quantity" class="form-label">Anuual Performance Degradation[%100]:</label>
                        <input type="text" class="form-control"  id="quantity" v-model="detailsComp.annual_performance_degradation" min="0"> 
             
                  </div>
            </div> 
      </div>
    </div>
      



  </div>
</div>
</template>
  
  

<script>
import { axios} from "@/common/api.service.js";
import {TARGET_IP} from "@/common/request_configs.js"
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
                 showModal:false

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
    components: { UpdateComponent }
} 
</script>




<style scoped>
/* Add styles as needed */
.tablecontainer{}

table {
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #f2f2f2;
}


.table-responsive {
    width: 100%;
    margin: 0 auto;
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
  background: #221ef7;
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
  position: relative;
  left: 0%;
  
}
h2{
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
</style>