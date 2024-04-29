<template>
    <div class="tablecontainer">
    
      <div class="mb-3">
                <label for="ChooseTechnology" class="form-label"><strong>Choose Technology:</strong></label>
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

                    <option value="Plants">Plants</option>
                    <option value="Public">Public</option>
                    <option value="Transport">Transport</option>

                    <!--<option value="Other">Other</option>-->   
                </select>
                <div class="mb-2 ml-2 " >
                    <label class="form-check-label" for="isMainInventory"><strong> No Main Inventory   </strong></label>
                        <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="NotMainInventory" @change="updateTypeofComponentToRender()"  value="false" >
                </div>
      </div>

      <div class = "test">
      <table class="table-responsive">
        <thead class="thead-dark">
          <tr id="table-header">
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Type</th>
            <th scope="col">Subtype</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in componentsPerType" :key="component.id">
                <td>{{ component.id }}</td>
                <td>{{ component.name }}</td>
                <td>{{ component.component_type }}</td>
                <td>{{ component.component_subtype }}</td>
                <td>
                    <button class="btn btn-primary" style="margin-right:2px; background-color:green;" @click="addComponent(component)">
                        Add to Inventory
                    </button>
                </td>
          </tr>
        </tbody>
      </table>

      <div class="addedcomponents"   v-if="YouHaveAddComponent">
        <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
          <p style=" color: cadetblue; text-align: center; font-size: em;">Submit Inventory Form</p>
          <div class="group1">
        <hr><br>
                <div>
                    <label for="name"  class="form-label">Demo Name:</label>
                    <input type="text" class="form-control" id="name" v-model="inventoryElement.name">
                </div>

                <div>
                    <label for="type" class="form-label">Project Name:</label>
                    <input type="text" class="form-control" id="type" v-model="inventoryElement.project_name">
                </div>
                <button type="submit" style="margin-top: 10px;" class="btn btn-primary">Update Inventory</button>
                <hr>
        </div>
    </form>
    </div>
  </div>
  <div v-if="YouHaveAddComponent" class="form-table">
        <hr>
        <hr style="color:white; height:5px;">
      <h4 style="color:green; text-align: center;">Inserted Components:{{ inventoryComponents.length }} </h4>
      <table style="margin-top: 20px; max-height: 300px; margin-bottom: 10px; width:50%;" class="table-responsive">
        <thead class="thead-dark">
          <tr id="table-header">
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Type</th>
            <th scope="col">Subtype</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in inventoryComponents" :key="component.id">
                <td>{{ component.id }}</td>
                <td>{{ component.name }}</td>
                <td>{{ component.component_type }}</td>
                <td>{{ component.component_subtype }}</td>
                <td>
                    <button class="btn btn-danger" style="margin-right:2px;" @click="deleteComponent(component.id)">
                        Delete From Inventory
                    </button>
                </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </template>


<script>
import { axios } from "@/common/api.service.js";
import { TARGET_IP } from "@/common/request_configs.js";
export default {
    name:"UpdateInventory",
    props:["id"],
    data() {
        return { components: [],
                 componentsPerType:[],
                 SHEET_TYPE:"all types",
                 YouHaveAddComponent:true,  // is the components added to inventory (list of json) 
                 INVENTORY_ID_COMPONENT:new Set(),
                 inventoryElement: {},     // initialize there --> setting inside created
                 inventoryComponents:[],   // initialize here  --> setting inside created
                 NotMainInventory:null
        };
    },
    async created(){

        try {
            console.log("inside created")
            let response = await axios.get(`${TARGET_IP}/api/inventory/${this.$route.params.id}/`);
            console.log("inside created after axios request")
            this.inventoryElement = response.data;
            this.inventoryComponents = response.data.components;
            console.log(this.inventoryComponents)
            console.log("successfully fetched", response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        console.log(this.inventoryElement,"inside mounted")
        let tempIdCollection = this.inventoryElement.components.map((comp)=>comp.id) // is the components list of json
        this.INVENTORY_ID_COMPONENT = new Set(tempIdCollection) // is for the components_collection
        console.log("comp:",this.inventoryComponents)
        console.log("comp:",this.INVENTORY_ID_COMPONENT)
        axios.get(`${TARGET_IP}/api/component/`)
            .then(response => {
            for (let comp of response.data) {
                this.components.push(comp);
            }
            this.componentsPerType=this.components

        })
            .catch(error => {
            console.error('Error fetching data:', error);
        })},
        

    methods: {
        updateTypeofComponentToRender(){
        if(this.SHEET_TYPE==="all types"){this.componentsPerType=this.components}
        else{this.componentsPerType=this.components.filter(comp=>comp.SHEET_TYPE==this.SHEET_TYPE)}
        if(this.NotMainInventory){
            this.componentsPerType=this.componentsPerType.filter(comp=>!comp.IS_MAIN_INVENTORY)}
        },

        refreshlist(id) {
            this.components = this.components.filter(comp => comp.id != id);
            this.updateTypeofComponentToRender()
        },
    
        addComponent(comp){
            if(!this.INVENTORY_ID_COMPONENT.has(comp.id)){
                this.inventoryComponents.push(comp)
                this.INVENTORY_ID_COMPONENT.add(comp.id)
            }else{
                console.log("Already have add this component")
            }
        },
        deleteComponent(componentId){
            console.log("delete")
            this.inventoryComponents = this.inventoryComponents.filter(comp=>comp.id!==componentId) // update the components to render
            this.INVENTORY_ID_COMPONENT.delete(componentId)//remove from the set that creates the components_collection that defines
                                                           // the components at backend
        },
        async handleSubmit(){
            if(this.projectName!==null && this.intentroryName!==null){
                const inventory = {
                    name:this.inventoryElement.name,
                    project_name:this.inventoryElement.project_name,
                    components_collection:Array.from(this.INVENTORY_ID_COMPONENT)
                }
                console.log(inventory)
                    try{
                        console.log('wait to create inventory')
                        const {data} = await axios.put(`${TARGET_IP}/api/inventory/${this.inventoryElement.id}/`,inventory);
                        alert("Success!")
                        this.$router.push({ name:'ListMyInventories'}); //here add the router name from router/index.js
                    }catch(error){
                        console.log(error)
                        alert("Error")
                    }
                }
                else{
                    alert("Missing Input Data")
                }

        }
    }

}
</script>

<style scoped>
/* Add styles as needed */
.tablecontainer{   }
table {
  margin-left: 0.5%;
  border:0.5px solid grey;
  max-height: 600px;
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

.mb-3{
        width: 100%;             /* Make each form element take full width on smaller screens */
        box-sizing: border-box;  /* Include padding and border in the width */
        margin-left: 0.5%;

    }
    .addedcomponents{
      width:50%;
      margin-left:20px;
      height: 400px;
      margin-right:5%;
       background-color: aliceblue;
    }

    #component{}
      
    

    #submitinventory {
    }

#ChooseTechnology{
    margin-top: 10px;
}

  .table-responsive {
    margin: 0 auto;
    display: block;
    max-height: 400px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: -ms-autohiding-scrollbar;
}

.group1{
  margin: 0 auto;
  width:50%;
}

.test{
  background-color: white;
  margin-left:0.5%;
  display: flex;
  justify-content: flex-start;
}

#table-header{
  background-color: mediumseagreen;
}



</style>