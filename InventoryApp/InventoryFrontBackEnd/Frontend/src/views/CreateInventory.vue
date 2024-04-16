<template>

<div class="row">
  
  <div class=" col-lg-2 col-md-2 col-sm-4 col-6">
    <nav class="navbar-primary">
      <ul class="navbar-primary-menu">
        <li>
          <a href="#" id="nav-options" :class="['nav-options', {'option': option1_or_option2}]" @click="showcomponents"><strong>Add Components</strong></a>
          <a href="#" @click="showinventory" :class="['nav-options', {'option': !option1_or_option2}]" ><strong>Submit Inventory</strong></a>
          <div style="margin-left:5px" class="mb-3">
                <label for="ChooseTechnology" id="temps" class="form-label"><strong>Choose Technology <span class="fa fa-search" ></span></strong></label>
                <select style="width:90%;font-size:1em;" id="ChooseTechnology" v-model="SHEET_TYPE" class="custom-select" @change="updateTypeofComponentToRender()">
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

                <div   class="mt-2 ml-2 " >
                    <label  class="form-check-label" id="temps" for="isMainInventory"><strong>No Main Inventory  </strong></label>
                        <input type="checkbox" class="form-check-input" id="isMainInventory" v-model="NotMainInventory" @change="updateTypeofComponentToRender()"  value="false" >
                </div>
            </div>
        </li>
      </ul>
    </nav>
  </div>    

  <div class="col-2 col-sm-1 col-xs-1">
  </div>


  <div  class="col-6 components" v-if="showComponentsTable">
        <table  class="table-responsive">
            <tr id="table-header">
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Actions</th>
            </tr>
          <tbody>
            <tr v-bind:class="{'coloured':inventoryComponents.includes(component)}" v-for="component in componentsPerType" :key="component.id">
                  <td>{{ component.id }}</td>
                  <td>{{ component.name }}</td>
                  <td>
                      <button id="add-buttons" class="btn btn-primary"  @click="addComponent(component)">
                          Add to Inventory
                      </button>
                  </td>
            </tr>
          </tbody>
        </table>
  </div>

  <div style="background-color: white" class="col-6" v-if=" showInventoryForm">

    <form ref="anyName" class="container mt-4" id="component"  @submit.prevent="handleSubmit">
              <p id='form-title' style="  text-align: center; font-size: 2em; font-weight:bolder;">Submit Inventory Form</p>
              <div class="group1">
            <hr><br>
                    <div>
                        <label for="name"  class="form-label">Demo Name:</label>
                        <input type="text" class="form-control" id="name" v-model="inventoryName">
                    </div>

                    <div>
                        <label for="type" class="form-label">Project Name:</label>
                        <input type="text" class="form-control" id="type" v-model="projectName">
                    </div>
                    <button type="submit" style="margin-top: 10px;" class="btn btn-primary">Submit Inventory</button>
                    <hr>
            </div>
        </form>

    <h2><strong>Inventory Components:</strong></h2>
    <h4>Components Number:{{ inventoryComponents.length }}</h4>
    <table class="table-responsive" style="max-height: 400px;">
        <thead class="thead-dark">
          <tr id="table-header">
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr  v-for="component in inventoryComponents" :key="component.id">
                <td>{{ component.id }}</td>
                <td>{{ component.name }}</td>
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
    name:"CreateInventory",
    data() {
        return { components: [],
                 componentsPerType:[],
                 SHEET_TYPE:"all types",
                 inventoryComponents:[],
                 INVENTORY_ID_COMPONENT: new Set(),
                 YouHaveAddComponent:false,
                 inventoryName:null,
                 projectName:null,
                 NotMainInventory:null,
                 showComponentsTable:true,
                 showInventoryForm:false,
                 option1_or_option2:true,

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

        this.hideBodyOverflow();
    },

    beforeDestroy() {
      this.showBodyOverflow();
  },
    methods: {

      hideBodyOverflow() {
        document.body.style.overflowX = 'hidden';
    },

    showBodyOverflow() {
      document.body.style.overflowX ='';
    },

      showcomponents(){
          this.option1_or_option2= !this.option1_or_option2
          this.showComponentsTable=true;
          this.showInventoryForm=false
      },  

      showinventory(){
          this.option1_or_option2= !this.option1_or_option2
          this.showComponentsTable=false;
          this.showInventoryForm=true
      },  
      
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
    },        
}

</script>



<style scoped>



table {
  max-height: none; /* This would override the .table-responsive max-height */
}

/* Add styles as needed */
.navbar-global {
  background-color: indigo;
}

.navbar-global .navbar-brand {
}

.navbar-global .navbar-user > li > a
{
}

.navbar-primary {
  height: 100vh;
  width: 70%;
  overflow: hidden;
  -webkit-transition: all 0.1s ease-in-out;
  -moz-transition: all 0.1s ease-in-out;
  transition: all 0.1s ease-in-out;
  background-color:white;
  margin-bottom: 0px;
  overflow-y: hidden;
}

.navbar-primary.collapsed {
  width: 60px;
}

.navbar-primary.collapsed .glyphicon {
  font-size: 22px;
}

.navbar-primary.collapsed .nav-label {
  display: none;
}

.navbar-primary-menu,
.navbar-primary-menu li {
  margin:0; padding:0;
  list-style: none;
}

.nav-options{
  display: block;
  padding: 10px 18px;
  text-align: left;
  border-bottom:solid 1px #444;
  color: #F7F7F7;
}



.option{
  background-color:#1089ff;
  text-decoration: none;
  color: #ffffff; 
  border-radius: 8px;
  margin-left:1px;
}

.navbar-primary-menu li a .glyphicon {
  margin-right: 6px;
}

.navbar-primary-menu li a:hover .glyphicon {
  color: orchid;
}

a{
  margin-top: 10px;
  margin-bottom: 10px;
}


.table-responsive{
  display: block;
  max-height: 80vh;
  overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: -ms-autohiding-scrollbar;
    border:solid grey 0.25px;
    background-color: white;
}

th, td {
  border: 1px solid #ddd;
  padding: 6px;
  text-align: center;
  text-overflow: ellipsis;
  white-space: normal;
  font-size: medium;
  word-wrap: break-word;
  width:300px;
  max-width: 300px;
}

.coloured{
  background-color: lightgrey;
}


@media screen and (max-height: 850px) {
  .navbar-primary {
    height: 90vh;
  }
}

@media screen and (max-width: 1250px) {
  .navbar-primary {
    width: 100%;
  }
}

body.hide-overflow {
  overflow: hidden;
}

.nav-label{
  color:#054673;
}

#temps{
  color:#054673;
}

#add-buttons{
  margin-right:2px;
  background-color: #2bb6a3;
}

.nav-options{
  color:#054673;
  text-decoration: none;
}



h2,h4{
  color:#054673;
}

#form-title{
  color:#054673;
}

#temps{
  color:lightslategray;
}

.components{
  margin-top: 6px;
}


</style>