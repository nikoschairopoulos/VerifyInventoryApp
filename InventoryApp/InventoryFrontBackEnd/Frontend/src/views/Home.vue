<template>
  <div class="home">
    <h4 style="color: #054673; text-align: center; margin-top: 50px; margin-bottom:50px ; font-size: 4em;"> <strong>VERIFY-B LCI</strong>  </h4>
    
    <div class="row">
        <div class="col-3">
        </div>
        <div class="col-8">
          <div class="bg-image-container">
          <img style="" src="../../public/figure6.png"  alt="">
        </div>
      </div>
      </div>

      <div style="" class="container mt-5">
        <button id="redirectButton" class="btn btn-primary">Go to VERIFY-B App</button>
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
  components: {}
}
</script>

<style scoped>
.body{
  overflow: hidden;
}
.pagefooter{
  font-size: 24px;
  position:fixed;
  bottom: 0;
  /*right:50%;*/
  text-align:left;
  display: block;
  margin-left: auto;
}

.card-text {
  color:darkgrey;
  font-family: 'Monospace', cursive; /* Example calligraphic font */
  font-size: 4vh;
  letter-spacing: 2px; /* Adjust letter spacing for a decorative look */
  line-height: 1.5; /* Adjust line height for better readability and style */

}

.bg-image-container {
  position: relative;
  height: 40vh; /* Adjust the height as needed */
  width: 100%;
  overflow: hidden; /* Hide any overflow from the image */
}

.bg-image {
  position: absolute;
  top: 0;
  left: 0;

  object-fit: cover; /* Cover the container with the image */
  z-index: -1; /* Place the image behind other content */
}

</style>