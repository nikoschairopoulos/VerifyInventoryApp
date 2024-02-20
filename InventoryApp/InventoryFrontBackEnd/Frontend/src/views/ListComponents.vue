<template>
    <div class="tablecontainer">

      <div class="mb-3" v-if="!updateComponentMode">
                <label for="Choose Technology" class="form-label">Choose Technology:</label>
                <select id="Choose Technology" v-model="SHEET_TYPE" class="custom-select" @change="updateTypeofComponentToRender()">
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


      <UpdateComponent v-if="updateComponentMode" header="Update Component" :component="EditedComponent" />

     
     
      <table class="table-responsive" v-if="!updateComponentMode">
        <thead class="thead-dark">
          <tr>
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
                <td class="text-center">{{ component.name }}</td>
                <td class="text-center">{{ component.component_type }}</td>
                <td class="text-center">{{ component.component_subtype }}</td>
                <td class="text-center">{{ component.replace_or_die}}</td>
                <td class="text-center">{{ component.SHEET_TYPE }}</td>
                <td class="text-center">{{ component.IS_MAIN_INVENTORY }}</td>
                <td>
                    <button class="btn btn-primary" style="margin-right:2px;" @click="updateComponent(component.id)">
                        Edit
                    </button>
                <button class="btn btn-danger" style="margin-right:2px;" @click="deleteComponent(component.id)">
                        Delete
                </button>
                <button class="btn btn-info" @mouseover="showDetails(component)" @mouseleave="dontshowDetails">
                        Info
                </button>
                </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="toShow" class="infocart">
        <div class="group1">
          <strong>name</strong>:{{detailsComp.name}} <br>
          <strong>component_type</strong>:{{detailsComp.component_type}}  <br>
          <strong>component_subtype</strong>:{{detailsComp.component_subtype}}<br>
          <strong>capex_per_ugs</strong>:{{detailsComp.capex_per_ugs}}  <br>
          <strong>opex_per_capex</strong>:{{detailsComp.opex_per_capex}}  <br>
          <strong>embodied_co2_per_ugs</strong>:{{detailsComp.embodied_co2_per_ugs}}  <br> 
          <strong>embodied_pe_per_ugs</strong>:{{detailsComp.embodied_pe_per_ugs}}  <br>
          <strong>lifetime</strong>:{{detailsComp.lifetime}}  <br> 
          <strong>pref_cost</strong>:{{detailsComp.pref_cost}}  <br>
          <strong>Bibliography</strong>:{{detailsComp.bibliography}}  <br>
        </div>
        <div class="group2">
        <strong>pref_env</strong>:{{detailsComp.pref_env}}  <br>
        <strong>scale_cost</strong>:{{detailsComp.scale_cost}}  <br>
        <strong>scale_env</strong>:{{detailsComp.scale_env}}  <br>
        <strong>major_upgrade_point</strong>:{{detailsComp.major_upgrade_point}}  <br>
        <strong>major_upgrade_share</strong>:{{detailsComp.major_upgrade_share}}  <br>
        <strong>annual_performance_degradation</strong>:{{detailsComp.annual_performance_degradation}}<br>
        <strong>replace_or_die</strong>:{{detailsComp.replace_or_die}}<br>
        <strong>SHEET_TYPE</strong>:{{detailsComp.SHEET_TYPE}}<br>
        <strong>IS_MAIN_INVENTORY</strong>:{{detailsComp.IS_MAIN_INVENTORY}}  <br>
        <strong>Description</strong>:{{detailsComp.description}}<br>
        </div>
      </div>

    </div>
  </template>
  
  

<script>
import { axios } from "@/common/api.service.js";
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
                 toShow:false

        };
    },
    mounted() {
        axios.get('http://127.0.0.1:8000/api/component/')
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
                    .delete(`http://127.0.0.1:8000/api/component/${componentId}/`)
                    .then(()=>this.refreshlist(componentId))
                    .catch(error => {
                          console.error('Error fetching data:', error)})}},
        
        updateComponent(componentId) {
            this.updateComponentMode = true;
            this.EditedComponent = this.components.filter(comp=>comp.id===componentId)[0]   
        },
        showDetails(component){
          this.toShow=true
          this.detailsComp=component
          
        },
        dontshowDetails(){
          this.toShow=false
        }
    },
    components: { UpdateComponent }
} 
</script>




<style scoped>
/* Add styles as needed */
.tablecontainer{

    width:100;
}
table {
  border-collapse: collapse;
  border:4px solid grey;
}

th, td {
  border: 1px solid #ddd;
  padding: 6px;
  text-align: center;
}

th {
  background-color: #f2f2f2;
}

.mb-3{
        width: 100%;             /* Make each form element take full width on smaller screens */
        box-sizing: border-box;  /* Include padding and border in the width */
        margin-left: 0.5%;

    }

    .table-responsive {
    display: block;
    width: fit-content;
    margin:0 auto;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: -ms-autohiding-scrollbar;
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
  margin-left: 10px;
}


</style>