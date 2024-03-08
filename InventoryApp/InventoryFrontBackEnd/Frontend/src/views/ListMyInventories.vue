<template>
<div>
    <div>
        <button type="button" class="btn btn-success" id="inventorycreate" @click="createInventory()">Create New Inventory</button>
    </div>
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
<div class="container">
<div class="row">
	<div class="col-lg-12 mt-6">
		<div class="main-box clearfix">
			<div class="table-responsive">
				<table class="table user-list">
					<thead>
						<tr>
                            <th><span>id</span></th>
							<th><span>Created</span></th>
							<th class="text-center"><span>name</span></th>
							<th><span>project name</span></th>
							<th><span>actions</span></th>
						</tr>
					</thead>
					<tbody>
						<tr class="listrender" v-for="item in inventoriesList" :key="item.id">
                            <td>
                            {{ item.id }}
                            </td>
							<td>
								{{ item.created_at }}
							</td>
							<td class="text-center">
								<span class="label label-default">{{ item.name }}</span>
							</td>
							<td>
								<p> {{ item.project_name }}</p>
							</td>
							<td style="width: 20%;">
								<p  class="table-link" @click="updateInventory(item)">
									<span class="fa-stack" >
										<i class="fa fa-square fa-stack-2x" ></i>
										<i style="color: blue;" class="fa fa-pencil fa-stack-1x fa-inverse"></i>
									</span>
								</p>
								<p  class="table-link danger" @click="deleteInventory(item.id)">
									<span class="fa-stack">
										<i class="fa fa-square fa-stack-2x"></i>
										<i class="fa fa-trash-o fa-stack-1x fa-inverse"></i>
									</span>
								</p>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
</div>
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
        updateInventory(inventoryElement){
            console.log('redirection at Update Inventory Component')
            console.log({obj:{... inventoryElement}})
            this.$router.push({ name:'Update Inventory',
                                params:{id:inventoryElement.id}});
        }
    }
}
//this.$router.push({ name:'Update Inventory',params:{obj:{...inventoryInfo}}});
</script>

<style scoped>

body{margin-top:20px;}


/* USER LIST TABLE */
.user-list tbody td > img {
    position: relative;
	max-width: 50px;
	float: left;
	margin-right: 15px;
}
.user-list tbody td .user-link {
	display: block;
	font-size: 1.25em;
	padding-top: 3px;
	margin-left: 60px;
}
.user-list tbody td .user-subhead {
	font-size: 0.875em;
	font-style: italic;
}

/* TABLES */
.table {
    border-collapse: separate;
}
.table-hover > tbody > tr:hover > td,
.table-hover > tbody > tr:hover > th {
	background-color: #eee;
}
.table thead > tr > th {
	border-bottom: 1px solid #C2C2C2;
	padding-bottom: 0;
}
.table tbody > tr > td {
	font-size: 0.875em;
	background: #f5f5f5;
	border-top: 10px solid #fff;
	vertical-align: middle;
	padding: 12px 8px;
}
.table tbody > tr > td:first-child,
.table thead > tr > th:first-child {
	padding-left: 20px;
}
.table thead > tr > th span {
	border-bottom: 2px solid #C2C2C2;
	display: inline-block;
	padding: 0 5px;
	padding-bottom: 5px;
	font-weight: normal;
}
.table thead > tr > th > p span {
	color: blue
}
.table thead > tr > th > p span:after {
	content: "\f0dc";
	font-family: FontAwesome;
	font-style: normal;
	font-weight: normal;
	text-decoration: inherit;
	margin-left: 5px;
	font-size: 0.75em;
}
.table thead > tr > th > p.asc span:after {
	content: "\f0dd";
}
.table thead > tr > th > p.desc span:after {
	content: "\f0de";
}
.table thead > tr > th > p:hover span {
	text-decoration: none;
	color: #2bb6a3;
	border-color: #2bb6a3;
}
.table.table-hover tbody > tr > td {
	-webkit-transition: background-color 0.15s ease-in-out 0s;
	transition: background-color 0.15s ease-in-out 0s;
}
.table tbody tr td .call-type {
	display: block;
	font-size: 0.75em;
	text-align: center;
}
.table tbody tr td .first-line {
	line-height: 1.5;
	font-weight: 400;
	font-size: 1.125em;
}
.table tbody tr td .first-line span {
	font-size: 0.875em;
	color: #969696;
	font-weight: 300;
}
.table tbody tr td .second-line {
	font-size: 0.875em;
	line-height: 1.2;
}
.table p.table-link {
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

#inventorycreate{
    display: block;
    margin: 0 auto;
    margin-top: 10px;
    margin-bottom: 1%;
    width: 10%;
    background: darkgreen;
    box-sizing: content-box;
}
#inventorycreate:hover{
    cursor: pointer;
    background-color: #2bb6a3;
	border-color: #2bb6a3;
}

</style>