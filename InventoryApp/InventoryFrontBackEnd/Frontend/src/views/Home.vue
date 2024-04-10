<template>
  <div class="home">
    <h4 style="color: #054673; text-align: center; margin-top: 50px; margin-bottom:50px ; font-size: 4em;"> <strong>VERIFY-B LCI</strong>  </h4>
    
    <div class="row">
        <div class="col-3">
        </div>
        <div class="col-6">
          <img  src="../../public/figure6.png" id="home-page-image"  alt="lca image">
      </div>
      </div>

      <div style="" class="container mt-5">
        <button id="redirectButton" class="btn btn-primary" @click="goToVerify" >Go to VERIFY-B App</button>
        <a href="../assets/input_data.xlsx" download><button id="downloadButton" class="btn btn-info"  >Download LCI Form</button></a>
        <hr style="height: 15px; color: #054673;">
        <div  style="margin-top: 10px; color: #054673; width: fit-content;">
        <p style="margin-top: 10px;">
          <strong>This app aims to manage the inventory of the Verify Web App. It allows for the insertion, updating, or deletion of new components.<br> 
                  Additionally, it enables the definition of a new inventory for each specific Project.
                  Users can also access and update the emission factors for every fuel and country combination.
          </strong>
        </p>
        </div>
      </div>

      
    
</div>


 
</template>

<script>

export default {
  name: 'Home',
  components: {},
  methods:{
    goToVerify(){
      window.location.href = "http://192.168.101.31:3003/";
    },
    downloadForm(){
      
    }
  }
}
</script>

<style scoped>
.body{
  overflow-x: hidden;
}

#home-page-image{
  max-width: 100%;
  width: 100%;
  height: auto;
}

#downloadButton{
  margin-left:10px;
}


</style>