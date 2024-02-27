<template>
    <div class="tablecontainer">

    <div>
      <div class="mb-3">
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
      <table class="table-responsive">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Type</th>
            <th scope="col">Subtype</th>
            <th scope="col">SHEET_TYPE</th>
            <th scope="col">IS_MAIN_INVENTORY</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in componentsPerType" :key="component.id">
                <td>{{ component.name }}</td>
                <td>{{ component.component_type }}</td>
                <td>{{ component.component_subtype }}</td>
                <td>{{ component.SHEET_TYPE }}</td>
                <td>{{ component.IS_MAIN_INVENTORY }}</td>
                <td>
                    <button class="btn btn-primary" style="margin-right:2px;" @click="addComponent(component)">
                        Add to Inventory
                    </button>
                </td>
          </tr>
        </tbody>
      </table>
</div>


      <div class="addedcomponents" v-if="YouHaveAddComponent">
        <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
        <div class="group1">
                <div class="mb-3">
                    <label for="name" class="form-label">Inventory Name:</label>
                    <input type="text" class="form-control" id="name" v-model="inventoryName">
                </div>

                <div class="mb-3">
                    <label for="type" class="form-label">Project Name:</label>
                    <input type="text" class="form-control" id="type" v-model="projectName">
                </div>
                <button type="submit" id="submitinventory" class="btn btn-primary">Submit Inventory</button>
        </div>
    </form>
        <h4 style="margin-top:10%;">You have add these components</h4>
      <table class="table-responsive">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Type</th>
            <th scope="col">Subtype</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="component in inventoryComponents" :key="component.id">
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
import UpdateComponent from './UpdateComponent.vue';
export default {
    name:"CreateInventory",
    data() {
        return { components: [],
                 componentsPerType:[],
                 SHEET_TYPE:"all types",
                 inventoryComponents:[],
                 INVENTORY_ID_COMPONENT: new Set(),
                 YouHaveAddComponent:false,
                 inventoryName:null,
                 projectName:null

        };
    },
    mounted() {
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
        
       // async deleteComponent(componentId) {},
        
        updateComponent(componentId) {
            this.updateComponentMode = true;
            this.EditedComponent = this.components.filter(comp=>comp.id===componentId)[0]   
        },
        addComponent(comp){
            if(!this.INVENTORY_ID_COMPONENT.has(comp.id)){
                this.inventoryComponents.push(comp)
                this.YouHaveAddComponent = true
                this.INVENTORY_ID_COMPONENT.add(comp.id)
                console.log(this.INVENTORY_ID_COMPONENT)
                console.log("id = ",comp.id)
            }else{
                console.log("Already have add this component")
            }
        },
        deleteComponent(componentId){
            this.inventoryComponents = this.inventoryComponents.filter(comp=>comp.id!==componentId) // update the components to render
            this.INVENTORY_ID_COMPONENT.delete(componentId)//remove from the set that creates the components_collection that defines
                                                           // the components at backend
        },
        async handleSubmit(){
            if(this.projectName!==null && this.intentroryName!==null){
                const inventory = {
                    name:this.inventoryName,
                    project_name:this.projectName,
                    components_collection:Array.from(this.INVENTORY_ID_COMPONENT)
                }
                console.log(inventory)
                    try{
                        console.log('wait to create inventory')
                        const {data} = await axios.post(`${TARGET_IP}/api/inventory/`,inventory);
                        alert("Success!")
                        this.$router.push({ name:'Home'}); //here add the router name from router/index.js
                    }catch(error){
                        console.log(error)
                        alert("Error")
                    }
                }
                else{
                    alert("Missing Input Data")
                }

        }
    },        
}

</script>

<style>

</style>


<style scoped>
/* Add styles as needed */
.tablecontainer{

    display:flex;
    justify-content: space-around;
    width:100;
}
table {
  margin-left: 0.5%;
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
    .addedcomponents{
        margin-top: 2.5%;
    }

    #component{
        width:100%;
    }

    #submitinventory {
    width: 55%;
    margin-bottom: 10%;
    margin-left: 0%;
}

    .table-responsive {
    display: block;
    width: fit-content;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: -ms-autohiding-scrollbar;
}
</style>