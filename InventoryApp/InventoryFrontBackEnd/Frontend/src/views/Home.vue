<template>
  <div class="home">
    <div class="bg-image-container">
  <img src="../../public/figure5.png" class="bg-image" alt="Background Image">
  <h2 style="color: white; text-align: center; margin-top: 50px; font-size: 4em;"> Verify-B Inventory Manager </h2>
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
  height: 100vh; /* Adjust the height as needed */
  width: 100%;
  overflow: hidden; /* Hide any overflow from the image */
}

.bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* Cover the container with the image */
  z-index: -1; /* Place the image behind other content */
}
</style>