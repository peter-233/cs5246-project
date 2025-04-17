<script setup lang="ts">
import TextLabelView from "./views/TextLabelView.vue";

</script>

<template>
  <n-message-provider>
    <n-dialog-provider>
      <div class="wrapper">
        <TextLabelView/>
      </div>
    </n-dialog-provider>
  </n-message-provider>
</template>

<style scoped>
.wrapper {
  width: 100%;
  height: 100%;
}
</style>

<style>

body {
  width: 100vw;
  height: 100vh;
  margin: 0;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
}


</style>
