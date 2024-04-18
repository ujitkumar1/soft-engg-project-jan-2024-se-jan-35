<template>
  <div v-for="(i, index) in lt" :key="index">
    <NavBar :title="i" />
    <NavBar title="test" />
  </div>
</template>

<script>
// import CreateTicket from "./CreateTicket.vue";
import NavBar from "./NavBar.vue";
export default {
  name: "TestingAPI",
  components: {
    NavBar,
  },
  data() {
    return {
      lt: ['aa', 'fdaf']
    }
  }
};
</script>
