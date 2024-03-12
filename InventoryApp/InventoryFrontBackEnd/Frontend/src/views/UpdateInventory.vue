<template>

    <div class="tablecontainer">
    <div>
    <div class="mb-3">
                <label for="Choose Technology" class="form-label">Choose Technology:</label>
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
    <table class="table-responsive">
        <thead class="thead-dark">
        <tr>
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
                    <input type="text" class="form-control" id="name" v-model="inventoryElement.name">
                </div>

                <div class="mb-3">
                    <label for="type" class="form-label">Project Name:</label>
                    <input type="text" class="form-control" id="type" v-model="inventoryElement.project_name">
                    <p style="margin-top:10%;text-align:center; font-weight: bolder;">You added: {{ inventoryComponents.length }} components</p>
                </div>
                <button type="submit" id="submitinventory" class="btn btn-primary">Update Inventory</button>
             </div>
    </form>
        <table class="table-responsive">
            <thead class="thead-dark">
            <tr>
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
import {TARGET_IP} from "@/common/request_configs.js"
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
.tablecontainer{

display:flex;
justify-content: space-around;

}
table {
margin-left: 0.5%;
border-collapse: collapse;
border:0.5px solid grey;
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
    margin-top:34px;
}

#component{
    width:100%;
    margin-bottom: 5px;
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
max-height: 400px;
}

#ChooseTechnology{
    margin-top: 10px;
}

</style>