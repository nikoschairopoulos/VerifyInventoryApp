<template>
<div class="invcontainer">
    
    <div v-if="!updateMode">
        <button type="button" class="btn btn-success" id="inventorycreate" @click="createInventory()">Create New Inventory</button>
    </div>
    <div v-if="updateMode">
        <UpdateInventory :inventoryElement="inventoryToUpdate" />
    </div>
    <ul v-else class="list-group">
        <div v-for="item in inventoriesList" :key="item.id">
            <li class="list-group-item active" id="listelement" >
                <div class="info">
                    <strong >inventory id</strong> : {{ item.id   }} <br>
                    <strong >inventory name</strong>: {{ item.name }} <br>
                    <strong>project name</strong>:{{ item.project_name }}
                </div>
                    <div class="actions">
                        <button class="btn btn-primary" style="margin-right:2px;" @click="updateInventory(item)">
                            Edit
                        </button> <br>
                    <button class="btn btn-danger" @click="deleteInventory(item.id)">
                            Delete
                    </button>
                </div>
            </li>

            <hr>
        </div>
    </ul>
    

</div>
  
</template>

<script>
import { axios } from "@/common/api.service.js";
import {TARGET_IP} from "@/common/request_configs.js"
import UpdateInventory from "./UpdateInventory";
export default {
    name:"ListMyInventories",
    components:{UpdateInventory},
    data(){
        return{
            inventoriesList:[],
            updateMode:false,
            inventoryToUpdate:null
        }
    },
    mounted() {
        axios.get(`${TARGET_IP}/api/userInventories/`)
            .then(response => {
            for (let inv of response.data) {
                this.inventoriesList.push(inv)
            }
            console.log(response.data);
            console.log(this.inventoriesList);
        })
            .catch(error => {
            console.error('Error fetching data:', error);
        });
    },
    methods:{
        createInventory(){
            this.$router.push('/create-inventory')
        },
        refreshlist(id) {
            this.inventoriesList = this.inventoriesList.filter(comp => comp.id != id);
            this.updateTypeofComponentToRender()
        },
        async deleteInventory(inventoryId){
            let comp = this.inventoriesList.filter(comp => comp.id === inventoryId);
            let check = window.prompt(`Please Enter "y" if you want to delete the component (Name:${comp[0].name})  else press "n":`, "");
            if (check === "y") {
                await axios
                    .delete(`${TARGET_IP}/api/inventory/${inventoryId}/`)
                    .then(()=>this.refreshlist(inventoryId))
                    .catch(error => {
                          console.error('Error fetching data:', error)})}
        },
        updateInventory(inventoryToUpdate){
            this.updateMode=true
            this.inventoryToUpdate = inventoryToUpdate
        }
    }
}
</script>

<style scoped>

.actions button{
    width:105%;
}

#inventorycreate{
    display: block;
    margin: 0 auto;
    margin-top: 6px;
    margin-bottom: 1%;
    width: 10%;
    background: mediumblue;
    box-sizing: content-box;
}


#listelement{
    margin-left:10% ;
    margin-right:10%;
    background-color: green;
    display: flex;
    justify-content: space-between;
}
</style>